"""Merchant Citadel P3-B batch 1: render the island GLB together with the real 24-building town (Blender reference views).

  Blender --background <town.blend> --python p3b_blender_render.py -- <build_dir> <out_dir> <view,view|all> [--save <file.blend>]

The island is IMPORTED FROM THE EXPORTED GLB (what the browser loads), vegetation and props are instanced from island-instances.json, so every image shows one
production scene. The town .blend is never saved over; only a TMP_ground plane is removed in memory.
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

here = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../p3b-batch1/source")); sys.path.insert(0, here)
import p3b_model as M

argv = sys.argv[sys.argv.index("--") + 1:]
BUILD, OUT, VIEWS = argv[0], argv[1], argv[2]; os.makedirs(OUT, exist_ok=True)
SAVE = argv[argv.index("--save") + 1] if "--save" in argv else None
RES = argv[argv.index("--res") + 1] if "--res" in argv else "1600x900"

for ob in list(bpy.data.objects):
    if ob.name.startswith("TMP_ground") or ob.name.startswith("P3A_"):
        bpy.data.objects.remove(ob, do_unlink=True)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=os.path.join(BUILD, "merchant-citadel-p3b-island.glb"))
new = [o for o in bpy.data.objects if o not in before]
byname = {o.name.split(".")[0]: o for o in new}
col = bpy.data.collections.new("P3B_ISLAND"); bpy.context.scene.collection.children.link(col)
for o in new:
    for c in o.users_collection:
        c.objects.unlink(o)
    col.objects.link(o)
inst = json.load(open(os.path.join(BUILD, "island-instances.json")))
protos = {k[6:]: o for k, o in byname.items() if k.startswith("PROTO_")}
# glTF import turns node transforms into object transforms; prototypes sit at the origin, hide them
for o in protos.values():
    o.hide_render = True; o.hide_viewport = True


def spawn(proto, x, n, z, yaw, s):
    src = protos[proto]; ob = bpy.data.objects.new("I_" + proto, src.data); col.objects.link(ob)
    ob.location = (x, n, z); ob.rotation_euler = (0, 0, yaw); ob.scale = (s, s, s); return ob


cnt = 0
for kind, lst in inst["vegetation"].items():
    for (x, n, z, yaw, s) in lst:
        if kind == "rock":
            spawn(("rock_a", "rock_b", "rock_c")[cnt % 3], x, n, z - 0.12 * s, yaw, s * 0.9)
        else:
            spawn(kind, x, n, z - 0.02, yaw, s * (1.0 if kind != "shrub" else 0.9))
        cnt += 1
for p in inst["quay_props"]:
    spawn(p["proto"], p["x"], p["n"], p["z"], p["yaw"], p["s"])
print("[p3b-render] instances", cnt + len(inst["quay_props"]), flush=True)

# batch 2: third-party flora library (flora.glb) instanced from island-flora.json (same file the browser reads)
FLORA = argv[argv.index("--flora") + 1] if "--flora" in argv else None
if FLORA:
    fb = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=os.path.join(FLORA, "assets-p3b2", "flora.glb")); fnew = [o for o in bpy.data.objects if o not in fb]; fl = {o.name.split(".")[0]: o for o in fnew}
    for o in fnew: o.hide_render = True; o.hide_viewport = True
    TINT = [("Leaves_NormalTree", (0.50, 0.56, 0.40)), ("Leaves_TwistedTree", (0.30, 0.47, 0.19)), ("Leaves_Pine", (0.85, 0.88, 0.80)), ("Leaves", (0.62, 0.70, 0.52)), ("Flowers", (0.82, 0.82, 0.82)), ("Grass", (0.62, 0.70, 0.50)), ("Rocks", (0.92, 0.80, 0.66)), ("PathRocks", (0.90, 0.80, 0.68)), ("Bark", (0.85, 0.80, 0.75))]
    for m in bpy.data.materials:                                         # same albedo multipliers as merchant-citadel-p2a/flora.js (the browser applies them at load)
        base = m.name.split(".")[0]; t = next((v for k, v in TINT if base.startswith(k)), None)
        if not t or not m.use_nodes: continue
        nt = m.node_tree; bs = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if not bs: continue
        lk = bs.inputs["Base Color"].links
        if not lk: continue
        src = lk[0].from_socket; mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"; mix.inputs[0].default_value = 1.0; mix.inputs[7].default_value = (*t, 1.0)
        nt.links.new(src, mix.inputs[6]); nt.links.new(mix.outputs[2], bs.inputs["Base Color"])
    fj = json.load(open(os.path.join(FLORA, "data", "island-flora.json"))); nflora = 0
    for name, lst in fj["instances"].items():
        src = fl.get("F_%s_L0" % name)
        if not src: continue
        for (x, n, z, yaw, s) in lst:
            ob = bpy.data.objects.new("FI_" + name, src.data); col.objects.link(ob); ob.location = (x, n, z); ob.rotation_euler = (0, 0, yaw); ob.scale = (s, s, s); nflora += 1
    for lst_, nm in ((fj.get("ledge_rocks", []), "Rock_Medium_1"),):
        src = fl.get("F_%s_L0" % nm)
        for i, (x, n, z, yaw, s) in enumerate(lst_[::4]):
            ob = bpy.data.objects.new("FI_ledge", src.data); col.objects.link(ob); ob.location = (x, n, z); ob.rotation_euler = (0, 0, yaw); ob.scale = (s * 0.55,) * 3
    print("[p3b2-render] flora instances", nflora, flush=True)
sc = bpy.context.scene
w = sc.world
if w and w.use_nodes:
    for n in w.node_tree.nodes:
        if n.type == "VALTORGB":
            n.color_ramp.elements[0].color = (0.74, 0.83, 0.93, 1); n.color_ramp.elements[1].color = (0.90, 0.88, 0.84, 1)
for attr, val in (("shadow_ray_count", 1), ("taa_render_samples", 32)):
    try:
        setattr(sc.eevee, attr, val)
    except Exception:
        pass
sun = bpy.data.objects.get("SUN")
if sun:
    try:
        sun.data.shadow_cascade_max_distance = 900
    except Exception:
        pass


def camera(name, loc, look, fov=None, ortho=None):
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name)); sc.collection.objects.link(cam); cam.location = loc
    cam.rotation_euler = (Vector(loc) - Vector(look)).to_track_quat("Z", "Y").to_euler()
    if ortho:
        cam.data.type = "ORTHO"; cam.data.ortho_scale = ortho; cam.rotation_euler = (0, 0, 0)
    else:
        cam.data.sensor_fit = "VERTICAL"; cam.data.angle_y = math.radians(fov or 50)
    cam.data.clip_start, cam.data.clip_end = 0.3, 6000
    return cam


def figure(x, y):
    z = float(M.terrain(np.array(x), np.array(y)))
    z = max(z, 0.01) if M.rect_dist(np.array(x), np.array(y), M.PAD) <= 0 else z
    m = bpy.data.materials.get("TMP_explorer") or bpy.data.materials.new("TMP_explorer"); m.use_nodes = True
    bs = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"); bs.inputs["Base Color"].default_value = (0.05, 0.42, 0.45, 1)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.56, location=(x, y, z + 0.78)); a = bpy.context.object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(x, y, z + 1.73)); b = bpy.context.object
    for o in (a, b):
        o.data.materials.append(m); o.name = "P3B_figure"
    return [a, b]


views = json.load(open(os.path.join(here, "p3b_views.json"))); views.update(json.load(open(os.path.join(here, "../../p3b-batch2/source/p3b2_views.json"))))
want = list(views) if VIEWS == "all" else VIEWS.split(",")
rx, ry = [int(v) for v in RES.split("x")]
for name in want:
    pos, look, fov, ortho, who = views[name]
    fig = figure(*who) if who else []
    cam = camera(name, pos, look, fov, ortho); sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = (1500, 1500) if ortho else (rx, ry); sc.render.filepath = os.path.join(OUT, "p3b-%s.png" % name)
    bpy.ops.render.render(write_still=True); print("[p3b-render] rendered", sc.render.filepath, flush=True)
    for o in fig:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.objects.remove(cam, do_unlink=True)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE, compress=True)
print("[p3b-render] done", flush=True)
