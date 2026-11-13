"""Convert third-party FBX animals to GLB, keeping every action as a named animation. Blender --background --python p3b2_fbx_to_glb.py -- <out dir> file.fbx [...]
Each file is imported into an empty scene (scale 1 m), all actions are exported (NLA-free: ACTIONS mode), textures are embedded. Originals are not modified."""
import bpy, sys, os
a = sys.argv[sys.argv.index("--") + 1:]; out = a[0]; os.makedirs(out, exist_ok=True)
for f in a[1:]:
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=f, use_anim=True, global_scale=1.0)
    name = os.path.splitext(os.path.basename(f))[0].replace(" ", "")
    acts = [x.name for x in bpy.data.actions]; print("[fbx]", name, "actions", acts, flush=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + ".glb"), export_format="GLB", export_animation_mode="ACTIONS", export_apply=False, export_yup=True, export_materials="EXPORT", export_cameras=False, export_lights=False, export_optimize_animation_size=False)
