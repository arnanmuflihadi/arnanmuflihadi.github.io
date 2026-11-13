"""Headless Blender: evidence tiles for P1.4 - the custom street elements, the Quaternius modules first used in P1.4 and the
examined-and-rejected Alefran models. Each tile shows the item as built / as authored beside the 1.9 m figure.
Run: Blender --background --factory-startup --python inspect_p14.py -- <extracted> <measurements.json> <out_dir>
"""
import bpy, json, math, os, sys
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import citadel_lib as cl
extracted, meas, out = sys.argv[sys.argv.index("--") + 1:][:3]
os.makedirs(out, exist_ok=True)
ALE = os.path.join(extracted, "alefran-medieval-stylized-free", "MedievalAssets GLTF with textures free")
ITEMS = [("CUS-Awning_burgundy", None, 2.4), ("CUS-Awning_blue", None, 2.4), ("CUS-Bunting_10", None, 3.2), ("CUS-PavingSeal", None, 0), ("CUS-Sign_Cup_wood", None, 2.6), ("CUS-Seal_NiagaAwan", None, 1.2),
         ("MV-Roof_RoundTiles_8x10", None, 0), ("MV-Roof_RoundTiles_4x8", None, 0), ("MV-Balcony_Cross_Straight", None, 0), ("MV-Overhang_Plaster_Short", None, 0), ("MV-Wall_Arch", None, 0),
         ("ALE-Streetlamp01", "Streetlamp01.gltf", 0), ("ALE-Market03", "Market03.gltf", 0), ("ALE-Sign01", "Sign01.gltf", 0), ("ALE-Brazier", "Brazier.gltf", 0), ("ALE-Bench01", "Bench01.gltf", 0)]
rows = []
for name, f, z in ITEMS:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lib = cl.Lib(extracted, meas)
    if f:
        before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(ALE, f)); objs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    else:
        objs = [lib.inst(name, (0, 0, z), 0)]
    bpy.context.view_layer.update()
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3); tris = 0
    for o in objs:
        o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    dims = [round(hi.x - lo.x, 2), round(hi.y - lo.y, 2), round(hi.z - lo.z, 2)]      # true bounds of the item, before framing
    cl.figure((hi.x + 0.9, lo.y, 0))
    cl.setup_render(px=(360, 360), sky=(0.82, 0.84, 0.88), sun_energy=3.2, sun_rot=(52, 0, -38), transparent=True)
    lo.z = min(lo.z, 0); hi.z = max(hi.z, 1.9); hi.x += 1.2
    c = (lo + hi) / 2; size = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z)
    cam = cl.camera("c", c + Vector((0.95, -1.55, 0.95)).normalized() * 200, c, ortho=size * 1.35)
    cl.render(cam, os.path.join(out, name + ".png"))
    rows.append({"id": name, "source_file": f, "dimensions_m": dims, "triangles": tris,
                 "materials": sorted({s.material.name.split(".")[0] for o in objs for s in o.material_slots if s.material})})
json.dump(rows, open(os.path.join(out, "p14-items.json"), "w"), indent=1)
print("[inspect] done", [(r["id"], r["triangles"]) for r in rows])
