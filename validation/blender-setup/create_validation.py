"""Offline bpy proof only. This script does not verify MCP communication."""
import bpy
from mathutils import Vector
from pathlib import Path

root = Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
collections = {}
for name in ['Buildings', 'Streets', 'Landscape', 'Props', 'Collision References']:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    collections[name] = c

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*color, 1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = .8
    return m

plaster = material('Warm plaster', (.65, .60, .47))
roof = material('Muted tropical green roof', (.13, .28, .23))
ground = material('Ground', (.34, .40, .29))
scale = material('1.8 metre reference', (.68, .28, .12))

def box(name, pos, dimensions, mat, collection='Buildings'):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = bpy.context.object
    o.name = name
    o.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    for c in list(o.users_collection):
        c.objects.unlink(o)
    collections[collection].objects.link(o)
    return o

box('Ground 12m', (0, 0, -.1), (12, 12, .2), ground, 'Landscape')
box('Left door pier', (-1.65, -1.75, 1.5), (1.7, .25, 3), plaster)
box('Right door pier', (1.65, -1.75, 1.5), (1.7, .25, 3), plaster)
box('Door lintel 1.6m wide opening / 2.2m clear', (0, -1.75, 2.6), (1.6, .25, .8), plaster)
box('Rear wall', (0, 1.75, 1.5), (5, .25, 3), plaster)
box('Left wall', (-2.375, 0, 1.5), (.25, 3.5, 3), plaster)
box('Right wall', (2.375, 0, 1.5), (.25, 3.5, 3), plaster)
box('Shading roof', (0, 0, 3.15), (5.8, 4.6, .3), roof)
box('Human height reference 1.8m', (3.4, -2.4, .9), (.45, .35, 1.8), scale, 'Props')
bpy.ops.object.camera_add(location=(9, -12, 8))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 1.2)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.lens = 45
scene.camera = camera
bpy.ops.object.light_add(type='AREA', location=(1, -5, 9))
bpy.context.object.data.energy = 1600
bpy.context.object.data.shape = 'DISK'
bpy.context.object.data.size = 7
scene.world.color = (.25, .25, .25)
scene.render.engine = 'CYCLES'
scene.cycles.samples = 24
scene.render.resolution_x = 1000
scene.render.resolution_y = 750
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(root / 'validation-render.png')
bpy.ops.export_scene.gltf(filepath=str(root / 'validation.glb'), export_format='GLB', export_yup=True)
bpy.ops.wm.save_as_mainfile(filepath=str(root / 'validation.blend'))
bpy.ops.render.render(write_still=True)
print('OFFLINE_VALIDATION_SAVED; MCP_NOT_TESTED')
