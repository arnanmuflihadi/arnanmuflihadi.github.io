"""Headless Blender: assemble the Merchant Citadel P1 ASSET-BACKED BLOCKOUT and render the concept views.

Run: Blender --background --factory-startup --python build_town.py -- <extracted> <measurements.json> <data_dir> <out_dir> [blend_path]

Everything named MV-/FP-/SN- is a real downloaded model. Temporary concept geometry is prefixed TMP_
(ground plane, dark interior cores, 1.9 m explorer). Inspection scene only - no GLB/production export.
"""
import bpy, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import citadel_lib as cl

args = sys.argv[sys.argv.index("--") + 1:]
extracted, meas, data_dir, out_dir = args[:4]
blend_path = args[4] if len(args) > 4 else None
ARCH = json.load(open(os.path.join(data_dir, "archetypes.json")))
L = json.load(open(os.path.join(data_dir, "layout.json")))
os.makedirs(out_dir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
lib = cl.Lib(extracted, meas)
town = bpy.data.collections.new("TOWN"); bpy.context.scene.collection.children.link(town)

# temporary ground (concept geometry) + real paving tiles
grass = cl.ground_material()
cl.box("TMP_ground", (-600, -500, -0.25), (600, 700, -0.02), grass, coll=town)
earth = cl.flat_material("TMP_ground_earth", (0.42, 0.33, 0.22))
for name, x0, x1, n0, n1 in L.get("yards", []):    # packed-earth courts: terrain surface treatment, temporary planes
    cl.box("TMP_yard", (x0, n0, -0.02), (x1, n1, -0.008), earth, coll=town)
cells = {}
for pv in L["paving"]:
    name, x0, x1, n0, n1 = pv[:5]
    for ix in range(int(x0), int(x1), 2):
        for iy in range(int(n0), int(n1), 2):
            cells[(ix + 1, iy + 1)] = pv[5] if len(pv) > 5 else "MV-Floor_UnevenBrick"
pave = bpy.data.objects.new("PAVING", None); town.objects.link(pave)
for (cx, cy), tile in sorted(cells.items()):
    lib.inst(tile, (cx, cy, 0.0), 0, pave, town)

for b in L["buildings"]:
    cl.build_archetype(lib, ARCH[b["archetype"]], b["id"] + "_" + b["archetype"], (b["x"], b["n"], 0), b["rz"], town, opts=b.get("opts"))
cl.build_archetype(lib, ARCH["GATE"], "G01_GATE", tuple(L["gate"]), 0, town)
if "cross" in L:
    cl.build_archetype(lib, ARCH["CROSS"], "M01_CROSS", tuple(L["cross"]), 0, town)

for s in L["stalls"]:
    kit = L["stall_kits"][s["kit"]]
    root = bpy.data.objects.new(s["id"] + "_STALL_" + s["kit"], None); town.objects.link(root)
    root.location = (s["x"], s["n"], 0); root.rotation_euler = (0, 0, math.radians(s["rz"]))
    lib.inst(kit["base"], tuple(kit.get("base_pos", (0, 0, 0))), 0, root, town)
    for pr in kit["props"]:
        lib.inst(pr[0], (pr[1], pr[2], pr[3]), pr[4], root, town, pr[5] if len(pr) > 5 else 1.0)

dress = bpy.data.objects.new("DRESSING", None); town.objects.link(dress)
for a, x, n, z, rz, sc in L["dressing"]:
    lib.inst(a, (x, n, z), rz, dress, town, sc)

stats = lib.stats()
stats["paving_tiles"] = len(cells)
stats["objects"] = len([o for o in town.objects])
tmp = [o.name for o in town.objects if o.name.startswith("TMP_")]
stats["temporary_concept_objects"] = len(tmp)
mats = {s.material.name for o in town.objects if o.type == "MESH" and not o.name.startswith("TMP_") for s in o.material_slots if s.material}
stats["materials"] = sorted(mats)
stats["material_count"] = len(mats)
json.dump(stats, open(os.path.join(out_dir, "town-stats.json"), "w"), indent=1)
print("[town] instances", stats["instances"], "unique ids", stats["unique_assets"], "downloaded models", stats["unique_downloaded_models"], "tris", stats["triangles"], "tiles", len(cells), flush=True)

cl.setup_render(px=(1920, 1080), sun_energy=4.6, sun_rot=(52, 0, -34), afternoon=True)
only = set(args[5:])
for name, (pos, look, fov, who) in L["views"].items():
    if only and name not in only:
        continue
    fig = cl.figure((who[0], who[1], 0), coll=town) if who else []
    cam = cl.camera(name, pos, look, fov_v=fov)
    cl.render(cam, os.path.join(out_dir, name + ".png"))
    for o in fig:
        bpy.data.objects.remove(o, do_unlink=True)
if not only or "plan-top" in only:
    x0, x1, n0, n1 = L["envelope"]
    cam = cl.camera("plan-top", ((x0 + x1) / 2, (n0 + n1) / 2 - 6, 400), ((x0 + x1) / 2, (n0 + n1) / 2 - 6, 0), ortho=132)
    cam.rotation_euler = (0, 0, 0)
    bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = 1500, 1800
    cam.data.ortho_scale = 132
    cl.render(cam, os.path.join(out_dir, "blockout-top-ortho.png"))
if blend_path:
    os.makedirs(os.path.dirname(blend_path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("[town] saved", blend_path)
