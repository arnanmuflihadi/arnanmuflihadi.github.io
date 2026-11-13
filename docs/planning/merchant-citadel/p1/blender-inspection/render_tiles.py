"""Headless Blender: render one neutral-lit tile per real downloaded asset, with a 1.9 m scale figure.

Run:  Blender --background --factory-startup --python render_tiles.py -- <spec.json> <out_dir> [px]
spec.json: [{"id": "MV-Wall_Plaster_Straight", "path": "/abs/file.gltf", "scale": 1.0}, ...]
"scale" is a disclosed presentation scale (1.0 = as authored). Source files are never modified.
"""
import bpy, json, math, os, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
spec, out_dir = json.load(open(argv[0])), argv[1]
PX = int(argv[2]) if len(argv) > 2 else 360
os.makedirs(out_dir, exist_ok=True)


def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    sc.render.resolution_x = sc.render.resolution_y = PX
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("neutral"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.82, 0.84, 0.88, 1); bg.inputs[1].default_value = 0.9
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.2; sun.data.angle = math.radians(6)
    sun.rotation_euler = (math.radians(52), 0, math.radians(-38))
    sc.collection.objects.link(sun)
    return sc


def figure(x, y):
    """1.9 m reference figure (body + head), flat teal."""
    m = bpy.data.materials.new("scale_fig"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.05, 0.42, 0.45, 1); b.inputs["Roughness"].default_value = 0.9
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.56, location=(x, y, 0.78)); body = bpy.context.object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(x, y, 1.73)); head = bpy.context.object
    for o in (body, head):
        o.data.materials.append(m)
    return [body, head]


def bounds(objs):
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    return lo, hi


def frame(sc, lo, hi, direction=(0.95, -1.55, 0.95)):
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"
    d = Vector(direction).normalized()
    cam.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    bpy.context.view_layer.update()
    inv = cam.rotation_euler.to_matrix().inverted()
    pts = [inv @ Vector((x, y, z)) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
    xs, ys = [p.x for p in pts], [p.y for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    cam.data.ortho_scale = max(max(xs) - min(xs), max(ys) - min(ys)) * 1.12
    centre = cam.rotation_euler.to_matrix() @ Vector((cx, cy, 0))
    cam.location = centre + d * 200
    cam.data.clip_start, cam.data.clip_end = 1, 600


for item in spec:
    sc = setup_scene()
    try:
        bpy.ops.import_scene.gltf(filepath=item["path"])
    except Exception as e:
        print("[tile] FAILED", item["id"], repr(e)[:120]); continue
    meshes = [o for o in sc.objects if o.type == "MESH"]
    s = float(item.get("scale", 1.0))
    if s != 1.0:
        for o in sc.objects:
            if o.parent is None:
                o.scale = [v * s for v in o.scale]
        bpy.context.view_layer.update()
    lo, hi = bounds(meshes)
    lo.z = min(lo.z, 0.0)
    fig = figure(hi.x + 0.55, lo.y + 0.2)
    bpy.context.view_layer.update()
    lo2, hi2 = bounds(meshes + fig)
    lo2.z = min(lo2.z, 0.0)
    frame(sc, lo2, hi2)
    sc.render.filepath = os.path.join(out_dir, item["id"] + ".png")
    bpy.ops.render.render(write_still=True)
    print("[tile] ok", item["id"], sc.render.engine, flush=True)
