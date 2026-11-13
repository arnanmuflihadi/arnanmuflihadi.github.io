"""Blender inspection sheet: lay out GLB nodes in a grid and render (front-high view). 
  Blender --background --python p3b2_sheet.py -- <out.png> <cols> <spacing> <scale> <frame|-1> file.glb [file.glb ...]   (flora: one glb; fauna: many)
Animated files are posed at <frame> (24 fps) of their first action; -1 = rest pose."""
import bpy, sys, os, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]; out, cols, sp, sc, fr = a[0], int(a[1]), float(a[2]), float(a[3]), int(a[4]); files = a[5:]
bpy.ops.wm.read_factory_settings(use_empty=True); scn = bpy.context.scene
roots = []
for f in files:
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=f); new = [o for o in bpy.data.objects if o not in before]
    tops = [o for o in new if o.parent is None]
    if len(files) > 1:                                                   # fauna: normalise each model to a 1.2 m longest side for the sheet (raw GLB units differ by 4 orders of magnitude)
        dg = bpy.context.evaluated_depsgraph_get(); mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
        for o in new:
            if o.type == "MESH":
                oe = o.evaluated_get(dg)
                for c in oe.bound_box:
                    w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
        size = max(mx - mn) or 1.0; k = 1.2 / size
        for o in tops: o.scale = (o.scale[0] * k, o.scale[1] * k, o.scale[2] * k)
    if len(files) == 1:
        roots += [(o.name, [o]) for o in tops if o.type in ("MESH", "ARMATURE", "EMPTY")]
    else:
        roots.append((os.path.basename(f), tops))
roots = [r for r in roots if not r[0].endswith("_L1")] if len(files) == 1 and "--all" not in a else roots
for i, (nm, objs) in enumerate(roots):
    p = Vector(((i % cols) * sp, -(i // cols) * sp, 0))
    for o in objs:
        o.location = p; o.scale = (o.scale[0] * sc, o.scale[1] * sc, o.scale[2] * sc)
if fr >= 0:
    for o in bpy.data.objects:
        if o.type == "ARMATURE" and o.animation_data and o.animation_data.action:
            pass
    scn.frame_set(fr)
# light, world, camera
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 4; sun.rotation_euler = (math.radians(50), 0, math.radians(30)); scn.collection.objects.link(sun)
w = bpy.data.worlds.new("w"); w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.78, 0.85, 0.93, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.2; scn.world = w
n = len(roots); rows = math.ceil(n / cols); cx = (cols - 1) * sp / 2; cy = -(rows - 1) * sp / 2
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scn.collection.objects.link(cam); scn.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = max(cols * sp * 1.05, rows * sp * 1.2 * 1.33)
tgt = Vector((cx, cy, 0.5)); cam.location = tgt + Vector((0, -60 * math.cos(math.radians(28)), 60 * math.sin(math.radians(28)))); cam.rotation_euler = (cam.location - tgt).to_track_quat('Z', 'Y').to_euler()
scn.render.resolution_x, scn.render.resolution_y = 2000, 2000 * 9 // 16 if rows < 3 else 1500
try: scn.render.engine = "BLENDER_EEVEE"
except Exception: pass
scn.render.filepath = out; bpy.ops.render.render(write_still=True); print("[sheet]", n, out)
