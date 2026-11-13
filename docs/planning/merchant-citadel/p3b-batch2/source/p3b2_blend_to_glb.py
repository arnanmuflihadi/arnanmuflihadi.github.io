"""Convert third-party .blend animals to GLB (all actions kept, vertex colours and material colours exported). Blender --background --python p3b2_blend_to_glb.py -- <out dir> file.blend [...]  (originals untouched)"""
import bpy, sys, os
a = sys.argv[sys.argv.index("--") + 1:]; out = a[0]; os.makedirs(out, exist_ok=True)
for f in a[1:]:
    bpy.ops.wm.open_mainfile(filepath=f); name = os.path.splitext(os.path.basename(f))[0].replace(" ", "")
    print("[blend]", name, "actions", [x.name for x in bpy.data.actions], "mats", [(m.name, tuple(round(c, 2) for c in m.diffuse_color[:3])) for m in bpy.data.materials][:4], flush=True)
    # these old packs use Diffuse BSDF nodes, which the glTF exporter ignores (everything came out white): rebuild each material as a Principled BSDF with the Diffuse/Principled colour,
    # (the farm animals carry a vertex colour layer, but it is all white: checked with p3b2 probe, 1 unique value, so it is ignored)
    vc_mats = set()
    for m in bpy.data.materials:
        if m.name in vc_mats or not m.use_nodes: continue
        col = next((tuple(n.inputs["Color"].default_value) for n in m.node_tree.nodes if n.type == "BSDF_DIFFUSE"), None) or next((tuple(n.inputs["Base Color"].default_value) for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), tuple(m.diffuse_color))
        m.node_tree.nodes.clear(); o_ = m.node_tree.nodes.new("ShaderNodeOutputMaterial"); b_ = m.node_tree.nodes.new("ShaderNodeBsdfPrincipled"); b_.inputs["Base Color"].default_value = col; b_.inputs["Roughness"].default_value = 0.9; m.node_tree.links.new(b_.outputs[0], o_.inputs[0])
    for o_ in bpy.data.objects:
        if o_.type == "MESH":
            for ca in list(o_.data.color_attributes): o_.data.color_attributes.remove(ca)
    for ob in bpy.data.objects: ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + ".glb"), export_format="GLB", export_animation_mode="ACTIONS", export_apply=False, export_yup=True, export_materials="EXPORT", export_vertex_color="ACTIVE", export_cameras=False, export_lights=False, use_selection=False)
