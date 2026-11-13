"""Headless Blender: assemble each archetype from the verified modules and render it alone (assembly evidence).

Run: Blender --background --factory-startup --python render_archetypes.py -- <extracted> <measurements.json> <archetypes.json> <out_dir> [ids]
"""
import bpy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import citadel_lib as cl
from mathutils import Vector

extracted, meas, arch_json, out_dir = sys.argv[sys.argv.index("--") + 1:][:4]
only = sys.argv[sys.argv.index("--") + 5:]
ARCH = json.load(open(arch_json))
os.makedirs(out_dir, exist_ok=True)
report = {}
for aid, arch in ARCH.items():
    if only and aid not in only:
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lib = cl.Lib(extracted, meas)
    cl.setup_render(px=(900, 760), sky=(0.82, 0.84, 0.88), sun_energy=3.4, sun_rot=(52, 0, -38), transparent=True)
    root = cl.build_archetype(lib, arch, aid)
    W, D = arch["footprint"]
    cl.figure((W / 2 + 1.5, -D / 2 - 1.5, 0))
    bpy.context.view_layer.update()
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in bpy.context.scene.objects:
        if o.type == "MESH" and not o.hide_render:
            for c in o.bound_box:
                w = o.matrix_world @ Vector(c)
                for i in range(3):
                    lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    centre = (lo + hi) / 2
    size = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z)
    for tag, d in (("front", Vector((0.85, -1.6, 0.8))), ("rear", Vector((-1.2, 1.3, 0.9))), ("top", Vector((0.0, -0.001, 1.0)))):
        cam = cl.camera("cam_" + tag, centre + d.normalized() * 300, centre, ortho=size * 1.45)
        cl.render(cam, os.path.join(out_dir, f"{aid}-{tag}.png"))
    st = lib.stats()
    report[aid] = {"name": arch["name"], "measured_bounds_m": [round(hi.x - lo.x, 2), round(hi.y - lo.y, 2), round(hi.z - lo.z, 2)],
                   "instances": st["instances"], "unique_assets": st["unique_assets"], "triangles": st["triangles"], "usage": st["usage"],
                   "triangles_custom": st["triangles_custom"], "material_variant_ids": st["material_variant_ids"]}
    print("[arch]", aid, report[aid]["measured_bounds_m"], st["instances"], st["triangles"], flush=True)
p = os.path.join(out_dir, "archetype-report.json")
prev = json.load(open(p)) if os.path.exists(p) else {}
prev.update(report)
json.dump(prev, open(p, "w"), indent=1)
