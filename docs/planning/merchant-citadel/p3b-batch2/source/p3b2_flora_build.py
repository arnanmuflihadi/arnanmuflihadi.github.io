"""Build the island flora library GLB from the prepared Quaternius files. Blender --background --python p3b2_flora_build.py -- <flora-src dir> <out.glb> [--ratio 0.33]
Trees get an L1 level (collapse decimation, UVs kept). Output nodes: F_<name>_L0 / F_<name>_L1 (trees), z up in Blender, y up in glTF, origin at the base."""
import bpy, sys, os, json, glob, math
argv = sys.argv[sys.argv.index("--") + 1:]; SRC, OUT = argv[0], argv[1]; RATIO = float(argv[argv.index("--ratio") + 1]) if "--ratio" in argv else 0.33
bpy.ops.wm.read_factory_settings(use_empty=True)
TREES = ("CommonTree", "Pine", "TwistedTree", "DeadTree")
stats = {}
for f in sorted(glob.glob(os.path.join(SRC, "*.gltf"))):
    name = os.path.basename(f)[:-5]; before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=f); new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == "MESH"]
    for o in new:
        o.select_set(o in meshes)
    for o in meshes: o.parent = None
    bpy.context.view_layer.objects.active = meshes[0]
    for o in meshes: o.select_set(True)
    for o in meshes:
        bpy.context.view_layer.objects.active = o; bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1: bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active; ob.name = "F_%s_L0" % name; ob.data.name = ob.name
    for o in new:
        if o.type != "MESH" and o.name in bpy.data.objects: bpy.data.objects.remove(o, do_unlink=True)
    t0 = len(ob.data.polygons); stats[name] = dict(l0_tris=sum(len(p.vertices) - 2 for p in ob.data.polygons))
    if name.startswith(TREES):
        bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True); bpy.context.view_layer.objects.active = ob; bpy.ops.object.duplicate(); d = bpy.context.view_layer.objects.active; d.name = "F_%s_L1" % name; d.data.name = d.name
        m = d.modifiers.new("dec", "DECIMATE"); m.ratio = RATIO if name != "TwistedTree_2" else 0.2; bpy.ops.object.modifier_apply(modifier="dec")
        stats[name]["l1_tris"] = sum(len(p.vertices) - 2 for p in d.data.polygons)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_image_format="AUTO", export_materials="EXPORT", export_cameras=False, export_lights=False)
stats["_glb_bytes"] = os.path.getsize(OUT); json.dump(stats, open(OUT + ".stats.json", "w"), indent=1); print("[flora]", len(stats) - 1, "models", stats["_glb_bytes"])
