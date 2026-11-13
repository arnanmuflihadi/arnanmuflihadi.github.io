"""Run through Blender MCP; isolated S1 asset inspection, not production design."""
import bpy
import math
from mathutils import Vector

BASE = '/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT = BASE + 'validation/asset-selection-s1/'
scene = bpy.data.scenes['S1 Asset Comparison']
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
groups = {}
for name in ['Buildings', 'Streets', 'Landscape', 'Props', 'Collision References', 'Labels', 'Cameras']:
    c = bpy.data.collections.new('S1 / ' + name)
    scene.collection.children.link(c)
    groups[name] = c

def move_collection(o, name):
    for c in list(o.users_collection): c.objects.unlink(o)
    groups[name].objects.link(o)

def mat(name, color):
    m = bpy.data.materials.new('S1 / ' + name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1)
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = .8
    return m

mineral = mat('mineral paving', (.55, .51, .42))
ink = mat('label ink', (.025, .06, .055))
human_mat = mat('scale marker', (.12, .30, .32))
atlas = mat('original Quaternius light atlas', (1, 1, 1))
tex = atlas.node_tree.nodes.new('ShaderNodeTexImage')
tex.image = bpy.data.images.load(OUT + 'acquired/quaternius-ultimate-buildings/Texture_Light.png', check_existing=True)
tex.image.pack()
atlas.node_tree.links.new(tex.outputs['Color'], next(n for n in atlas.node_tree.nodes if n.type == 'BSDF_PRINCIPLED').inputs['Base Color'])

def bounds(objects):
    points = [o.matrix_world @ Vector(v) for o in objects if o.type == 'MESH' for v in o.bound_box]
    return Vector(tuple(min(p[i] for p in points) for i in range(3))), Vector(tuple(max(p[i] for p in points) for i in range(3)))

def box(name, pos, size, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = bpy.context.object; o.name = 'S1 / ' + name; o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    move_collection(o, 'Streets')
    return o

def label(text, pos, size=.35):
    curve = bpy.data.curves.new('S1 label', 'FONT'); curve.body = text; curve.size = size; curve.align_x = 'CENTER'
    o = bpy.data.objects.new('S1 / label ' + text, curve)
    groups['Labels'].objects.link(o); o.location = pos
    curve.materials.append(ink)
    return o

records = []
files = [('A1', '2Story_Balcony.fbx', -14), ('A2', '2Story_Columns.fbx', -5), ('A3', '1Story_GableRoof.fbx', 4), ('A4', '2Story_RoundRoof.fbx', 13)]
for cid, filename, x in files:
    old = bpy.data.objects.get('2Story_Balcony') if cid == 'A1' else None
    if old:
        objs = [old]
    else:
        before = set(scene.objects)
        bpy.ops.import_scene.fbx(filepath=OUT + 'acquired/quaternius-ultimate-buildings/' + filename)
        objs = [o for o in scene.objects if o not in before]
    for o in objs:
        o.name = 'S1 / ' + cid + ' / ' + o.name
        o.scale *= 2.4
        if o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(atlas)
        move_collection(o, 'Buildings')
    bpy.context.view_layer.update()
    lo, hi = bounds(objs); offset = Vector((x-(lo.x+hi.x)/2, -(lo.y+hi.y)/2, -lo.z))
    for o in objs: o.location += offset
    bpy.context.view_layer.update(); lo, hi = bounds(objs)
    for o in objs: o['candidate_id'] = cid; o['source_file'] = filename; o['license'] = 'CC0-1.0'
    box(cid+' display paving', (x, 0, -.1), (8, 9, .2), mineral)
    label(cid+' / '+filename.replace('.fbx',''), (x, -4.25, .015), .32)
    records.append({'id':cid,'source':filename,'scale_factor':2.4,'size':tuple(hi-lo),'min':tuple(lo),'triangles':sum(len(p.vertices)-2 for o in objs if o.type=='MESH' for p in o.data.polygons)})

# Import existing authored Guild as a reference, not a newly selected external kit.
before = set(scene.objects)
bpy.ops.import_scene.gltf(filepath=BASE+'assets/game/architecture-r0b1/transit-kingdom.glb')
new = [o for o in scene.objects if o not in before]
guild = next(o for o in new if o.name.startswith('AtlasResearchCentre'))
keep = [guild] + list(guild.children_recursive)
for o in new:
    if o not in keep: bpy.data.objects.remove(o, do_unlink=True)
lo, hi = bounds(keep)
guild.location += Vector((28-(lo.x+hi.x)/2, 7-(lo.y+hi.y)/2, -lo.z))
for o in keep: move_collection(o, 'Buildings'); o['candidate_id'] = 'G0'
label('G0 / existing Atlas Guild prototype', (28, -1, .015), .42)
box('Guild display paving', (28, 7, -.1), (18, 18, .2), mineral)

for filename, x, y, height in [('canopy-tree.glb',-22,3,6), ('canopy-tree.glb',39,9,6), ('fern.glb',-19,-2,1.0)]:
    before = set(scene.objects)
    bpy.ops.import_scene.gltf(filepath=BASE+'assets/game/scenery/'+filename)
    obs = [o for o in scene.objects if o not in before]
    root = bpy.data.objects.new('S1 / vegetation carrier', None); groups['Landscape'].objects.link(root)
    for o in obs:
        if o.parent not in obs:
            w = o.matrix_world.copy(); o.parent = root; o.matrix_world = w
        move_collection(o, 'Landscape')
    lo, hi = bounds(obs); root.scale *= height/(hi.z-lo.z)
    bpy.context.view_layer.update(); lo, hi = bounds(obs)
    root.location += Vector((x-(lo.x+hi.x)/2,y-(lo.y+hi.y)/2,-lo.z))

# Reuse the already licensed imported planter as the prop sample.
before=set(scene.objects)
bpy.ops.import_scene.gltf(filepath=BASE+'assets/game/scenery/city-planter.glb')
obs=[o for o in scene.objects if o not in before]
for o in obs: move_collection(o,'Props')
lo,hi=bounds(obs)
carrier=bpy.data.objects.new('S1 / planter carrier',None);groups['Props'].objects.link(carrier)
for o in obs:
    if o.parent not in obs:
        w=o.matrix_world.copy();o.parent=carrier;o.matrix_world=w
carrier.scale*=1.2/max(hi-lo)
bpy.context.view_layer.update();lo,hi=bounds(obs)
carrier.location+=Vector((20-(lo.x+hi.x)/2,-3-(lo.y+hi.y)/2,-lo.z))

# Explicit human scale gauge, not an NPC or a finished character.
for x in [-18,-9,0,9]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=.19, depth=1.35, location=(x,-3,.675))
    o=bpy.context.object;o.name='S1 / human scale torso';o.data.materials.append(human_mat);move_collection(o,'Props')
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.225,location=(x,-3,1.575))
    o=bpy.context.object;o.name='S1 / human scale head / 1.8m';o.data.materials.append(human_mat);move_collection(o,'Props')
label('All gauges 1.80 m / comparison only',(-4,-6,.015),.36)

world=bpy.data.worlds.new('S1 neutral world');world.use_nodes=True
next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs['Color'].default_value=(.65,.75,.85,1)
next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs['Strength'].default_value=.45
scene.world=world
bpy.ops.object.light_add(type='AREA',location=(-10,-12,27))
light=bpy.context.object;light.name='S1 soft daylight';light.data.energy=15000;light.data.size=22;move_collection(light,'Cameras')

def camera(name, pos, target, lens):
    bpy.ops.object.camera_add(location=pos)
    o=bpy.context.object;o.name=name;o.data.lens=lens;o.data.clip_end=500
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    move_collection(o,'Cameras');return o

camera('S1 Aerial',(35,-48,36),(7,3,4),42)
camera('S1 Pedestrian',(0,-27,1.65),(0,0,3.0),23)
camera('S1 Detail',(-11,-10,7),(-14,0,4),48)
scene.camera=bpy.data.objects['S1 Aerial']
scene.render.engine='CYCLES';scene.cycles.samples=24
scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT+'asset-comparison.blend')
print('S1_IMPORTED_CANDIDATES',records)
print('S1_MESHES',sum(o.type=='MESH' for o in scene.objects))
print('S1_TEXTURES',[(i.name,i.size[:],bool(i.packed_file)) for i in bpy.data.images if i.users and i.source=='FILE'])
