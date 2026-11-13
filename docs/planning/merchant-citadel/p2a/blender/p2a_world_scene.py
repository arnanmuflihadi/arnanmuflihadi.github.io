"""Merchant Citadel P2-A: assemble the slice in world coordinates (the Blender source assembly), sample the walkable
height field from the real geometry, and render the parity cameras.

Run: Blender --background --factory-startup --disable-autoexec --python p2a_world_scene.py -- <inspection_dir> <out_dir> <scene.json> <data_out_dir> [views...]

Outputs: <out_dir>/merchant-citadel-p2a-slice-source.blend, <out_dir>/renders/<view>.png (original P1.4 materials and light),
         <data_out_dir>/heightfield.bin + heightfield.json (uint8 centimetres, row = n, column = x).
"""
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

args = sys.argv[sys.argv.index("--") + 1:]
INSPECT, OUT, SCENE, DATA = args[:4]
ONLY = set(a for a in args[4:] if not a.startswith('--'))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "p1.4", "blender-inspection"))
import citadel_lib as cl                                         # noqa: E402
sys.path.insert(0, HERE)
from p2a_hall import hall_modules                                # noqa: E402
from p2a_bazaar import hall_archetype, HALL_VARIANTS, register_custom   # noqa: E402
register_custom(cl)                                              # batch 4: CUS-Hoist, CUS-Sign_Leaf_*, CUS-Awning_tea

SC = json.load(open(SCENE)); ARCH = json.load(open(os.path.join(INSPECT, "p1.4", "data", "archetypes.json")))
os.makedirs(os.path.join(OUT, "renders"), exist_ok=True); os.makedirs(DATA, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
lib = cl.Lib(os.path.join(INSPECT, "extracted"), os.path.join(INSPECT, "measurements.json"))
town = bpy.data.collections.new("SLICE"); bpy.context.scene.collection.children.link(town)

cl.box("TMP_ground", (-600, -500, -0.25), (600, 700, -0.02), cl.ground_material(), coll=town)
walk_tiles, walk_stairs, podium_floors = [], [], []
TILE = {"cobble": "MV-Floor_UnevenBrick", "brick": "MV-Floor_Brick", "red": "MV-Floor_RedBrick"}
pave = bpy.data.objects.new("PAVING", None); town.objects.link(pave)
for k, items in SC["tiles"].items():
    for x, zt, z in items:
        lib.inst(TILE[k], (x, -zt, z), 0, pave, town); walk_tiles.append((x, -zt, z))
podium = {"parts": [], "extras": [e for e in ARCH["A01"]["extras"] if e["asset"].startswith(("MV-Floor_Brick", "MV-Stairs_"))]}
archs = dict(ARCH); archs.update(hall_modules(ARCH["A01"])); archs["PODIUM"] = podium; archs["ARCH"] = {"parts": [], "extras": [{"asset": "MV-Wall_Arch", "pos": [0, 0, 0]}]}
def strip_signs(a):
    b = dict(a); b["extras"] = [e for e in a.get("extras", []) if e.get("role") != "sign"]
    return b


for i in SC["instances"]:
    if i["node"].startswith("SIGN_"):                                      # signs and banners are placed objects, exactly as in the kit
        sg = SC["signs"][i["node"]]; lib.inst(sg["asset"], (i["x"], -i["z"], i["y"]), i["ry"], None, town, sg["scale"]); continue
    arch_i = hall_archetype(i["node"], ARCH) if i["node"] in HALL_VARIANTS else archs[i["node"]]
    root = cl.build_archetype(lib, strip_signs(arch_i), i["id"] + "_" + i["node"], (i["x"], -i["z"], i["y"]), i["ry"], town, opts=None)
    if i["node"] in ("TERRACE", "PODIUM"):
        for o in root.children_recursive:
            base = o.name.split(".")[0]
            if base.startswith("MV-Stairs_Exterior_Straight"):
                walk_stairs.append(o)
            if base == "MV-Floor_Brick" and i["node"] == "PODIUM":
                podium_floors.append(o)
for a, x, n, z, rz, sc in SC["dressing"]:
    lib.inst(a, (x, n, z), rz, None, town, sc)
HALL_STANDIN = "--standin" in sys.argv                                  # P2-A baseline only: the grey massing the hall replaced
if HALL_STANDIN:
    sm = cl.flat_material("TMP_standin", (0.55, 0.55, 0.56), 0.9)
    cl.box("TMP_hall_standin_body", (-13, 80, 2.0), (13, 88, 9.0), sm, coll=town); cl.box("TMP_hall_standin_tower", (-2, 82, 2.0), (2, 86, 21.0), sm, coll=town)
for o in bpy.data.objects:
    if o.name.startswith("TPL_"):
        o.hide_viewport = True
bpy.context.view_layer.update()
bpy.context.view_layer.update()
for o in podium_floors:
    m = o.matrix_world.translation; walk_tiles.append((m.x, m.y, m.z))
print("[world] objects", len(town.objects), "tiles", len(walk_tiles), "stair modules", len(walk_stairs))

# ---------------------------------------------------------------- height field from the geometry
X0, N0, CELL, NX, NN = -36.0, -12.0, 0.2, 430, 560
hf = np.zeros((NN, NX), dtype=np.float32)
for x, n, z in walk_tiles:                                         # flat tiles: exact analytic top (the tile mesh is 2 x 2 m, +-0.01)
    i0, i1 = int((x - 1 - X0) / CELL + 0.5), int((x + 1 - X0) / CELL + 0.5); j0, j1 = int((n - 1 - N0) / CELL + 0.5), int((n + 1 - N0) / CELL + 0.5)
    i0, j0 = max(i0, 0), max(j0, 0)
    hf[j0:j1, i0:i1] = np.maximum(hf[j0:j1, i0:i1], z + 0.01)
dg = bpy.context.evaluated_depsgraph_get()
for o in walk_stairs:                                              # stair modules: ray cast the actual treads
    bvh = BVHTree.FromObject(o, dg)                                # local space: transform the rays
    mw = o.matrix_world; inv = mw.inverted(); down = inv.to_3x3() @ Vector((0, 0, -1))
    pts = [mw @ Vector(c) for c in o.bound_box]
    xs, ys = [p.x for p in pts], [p.y for p in pts]
    for j in range(max(0, int((min(ys) - N0) / CELL)), min(NN, int((max(ys) - N0) / CELL) + 1)):
        for i in range(max(0, int((min(xs) - X0) / CELL)), min(NX, int((max(xs) - X0) / CELL) + 1)):
            hit = bvh.ray_cast(inv @ Vector((X0 + (i + 0.5) * CELL, N0 + (j + 0.5) * CELL, 6.0)), down.normalized(), 100.0)
            if hit[0] is not None:
                hf[j, i] = max(hf[j, i], (mw @ hit[0]).z)
u8 = np.clip(np.round(hf * 100), 0, 255).astype(np.uint8)
u8.tofile(os.path.join(DATA, "heightfield.bin"))
json.dump({"x0": X0, "n0": N0, "cell": CELL, "nx": NX, "nn": NN, "unit_m": 0.01, "max_m": float(hf.max()), "tiles": len(walk_tiles), "stair_modules": len(walk_stairs)}, open(os.path.join(DATA, "heightfield.json"), "w"))
print("[world] heightfield", NX, "x", NN, "max", hf.max(), "levels", sorted(set(np.round(hf[::5, ::5].ravel(), 2)))[:14])

# ---------------------------------------------------------------- parity renders
cl.setup_render(px=(1600, 900), sun_energy=4.6, sun_rot=(52, 0, -34), afternoon=True)
for name, v in SC["views"].items():
    if ONLY and name not in ONLY:
        continue
    pos, look = (v["pos"][0], -v["pos"][2], v["pos"][1]), (v["look"][0], -v["look"][2], v["look"][1])
    fig = cl.figure((v["who"][0], v["who"][1], v["who"][2] if len(v["who"]) > 2 else 0), coll=town) if v["who"] else []
    cam = cl.camera(name, pos, look, fov_v=v["fov"])
    cl.render(cam, os.path.join(OUT, "renders", name + ".png"))
    for o in fig:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.objects.remove(cam, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "merchant-citadel-p2a-slice-source.blend"), compress=True)
print("[world] done")
