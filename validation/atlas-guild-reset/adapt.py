import bpy,bmesh,math,json
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-reset/'
assert bpy.data.filepath==OUT+'atlas-guild.blend'
old=bpy.context.scene
assert old.name.startswith('R0-C2A'), 'Start from a fresh independent copy of the C2A prototype, not the adapted scene'
dg_source=bpy.context.evaluated_depsgraph_get()
source_groups={n:list(bpy.data.collections['C2A / '+n].objects)for n in['Building shell','Roof and lantern','Timber and glazing','Scale and cameras']}
s=bpy.data.scenes.new('Atlas Guild / accepted settlement site');bpy.context.window.scene=s;s.unit_settings.scale_length=1
s.world=old.world.copy() if old.world else bpy.data.worlds.new('Guild daylight')
cols={}
for name in['Building shell','Roof and lantern','Timber and glazing','Ground and entrance','Scale references','Frozen context','Views']:
 c=bpy.data.collections.new('Guild reset / '+name);s.collection.children.link(c);cols[name]=c
floor=.57

def position(p,roof=False):
 u=(p.x+1.9)*(1 if roof else 1.04)
 v=28.1+p.y-46.438 if roof else 30.35+(p.y-48.08)*4.7/4.84
 h=p.z-5.6
 if h>5.9:h=5.9+(h-5.9)*.70
 return Vector((u,v-32,h+floor))

def copy_geometry(o,category):
 evaluated=o.evaluated_get(dg_source);me=bpy.data.meshes.new_from_object(evaluated,depsgraph=dg_source)
 upper=category=='Building shell' and ('upper side wing' in o.name or 'rear clerestory wall' in o.name)
 roof=category=='Roof and lantern'
 for vertex in me.vertices:
  p=o.matrix_world@vertex.co
  if upper and p.z<7.11:p.z=5.6
  vertex.co=position(p,roof)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
 obj=bpy.data.objects.new(o.name.replace('Guild /','Atlas /',1),me);cols[category].objects.link(obj);obj['source_object']=o.name;obj['source']='Approved R0-C2A native prototype; derivative proportions and entrance'
 if roof and any(k in obj.name.lower()for k in ['lantern','observation','survey finial']):obj.location.y+=1.1
 return obj

for category in ['Building shell','Roof and lantern','Timber and glazing']:
 for o in source_groups[category]:
  if o.type not in {'MESH','FONT','CURVE'} or 'floor rim' in o.name:continue
  copy_geometry(o,category)
stone=bpy.data.materials['C1 / warm volcanic stone'];sand=bpy.data.materials['C1 / warm limestone']
def mesh(name,vs,fs,material,walkable=False):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(material);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('Atlas / '+name,me);cols['Ground and entrance'].objects.link(o);o['walkable']=walkable;return o
faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def slab(name,x0,x1,y0,y1,z0,z1,material):return mesh(name,[(x,y,z)for z in[z0,z1]for x,y in[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]],faces,material,True)
slab('low continuous stone foundation',-4.02,4.36,30.0-32,35.05-32,-.08,.545,stone)
slab('limestone threshold and hall floor',-4.02,4.36,30.0-32,35.05-32,.545,.57,sand)
front=30.35+(48.04-48.08)*4.7/4.84
slab('direct entrance landing',-1.4,1.4,29.2-32,30.0-32,-.02,.57,sand)
for i in range(3):slab('entrance tread '+str(i+1),-1.4,1.4,28.3+i*.3-32,28.6+i*.3-32,-.02,.035+(i+1)*(.535/3),sand)
# A preserved 1.8 m reference stays outside the door; it is never exported as an NPC.
for o in source_groups['Scale and cameras']:
 if o.type!='MESH':continue
 me=bpy.data.meshes.new_from_object(o.evaluated_get(dg_source),depsgraph=dg_source)
 for v in me.vertices:
  p=o.matrix_world@v.co;v.co=Vector((p.x+.75-1.85,p.y-47.4-3.35,p.z-5.6+.035))
 obj=bpy.data.objects.new('Scale / '+o.name,me);cols['Scale references'].objects.link(obj)
# Opaque stylized glazing shares the existing material family; no transmission pass is introduced.
for mat in {m for c in cols.values()for o in c.objects if o.type=='MESH'for m in o.data.materials if m and 'glaz' in m.name.lower()}:
 clone=mat.copy();clone.name='Guild / stylized blue-green glazing';node=next((n for n in clone.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if node:
  node.inputs['Roughness'].default_value=.25;node.inputs['Metallic'].default_value=.12
  if 'Transmission Weight' in node.inputs:node.inputs['Transmission Weight'].default_value=0
 for c in cols.values():
  for o in c.objects:
   if o.type=='MESH':
    for slot in o.material_slots:
     if slot.material==mat:slot.material=clone
# The context is a read-only snapshot of the accepted Three.js geometry, in Guild-local coordinates.
prior=set(s.objects);bpy.ops.import_scene.gltf(filepath=OUT+'accepted-context.glb')
for o in set(s.objects)-prior:
 for c in list(o.users_collection):c.objects.unlink(o)
 cols['Frozen context'].objects.link(o)
 for slot in o.material_slots if o.type=='MESH' else []:
  for name in ['Bark_NormalTree.002','Leaves_NormalTree.002']:
   if name.split('.')[0] in slot.material.name:slot.material=bpy.data.materials[name]
for light in [o for o in old.objects if o.type=='LIGHT']:
 data=light.data.copy();o=bpy.data.objects.new('Guild review / '+light.name,data);cols['Views'].objects.link(o);o.rotation_euler=light.rotation_euler
 if data.type=='SUN':o.location=(8,-12,25)
 else:o.location=(-12,-16,20);o.rotation_euler=(Vector((0,0,2))-o.location).to_track_quat('-Z','Y').to_euler();data.energy=1200;data.size=18

def cam(name,p,t,lens=30):
 data=bpy.data.cameras.new(name);data.lens=lens;data.clip_end=500;o=bpy.data.objects.new(name,data);cols['Views'].objects.link(o);o.location=p;o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler();return o
cam('01 Guild from Telaga Awan',(-2.8,17-32,1.685),(0,0,5.8),20.7846096908)
cam('02 Guild entrance',(-4.3,-7.8,1.685),(0,-1.65,2.65),28)
cam('03 Guild in town',(-27,-34,27),(0,-9,3.2),34)
cam('04 Guild roof detail',(8,-10,9.5),(0,0,5.4),42)
s.camera=bpy.data.objects['01 Guild from Telaga Awan'];s.render.engine=old.render.engine;s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100
s.render.image_settings.file_format=next(i.identifier for i in bpy.types.ImageFormatSettings.bl_rna.properties['file_format'].enum_items if i.identifier=='PNG')
s.view_settings.view_transform=old.view_settings.view_transform;s.view_settings.look=old.view_settings.look;s.view_settings.exposure=old.view_settings.exposure
s['design_scope']='Guild-only derivative. Accepted settlement unchanged. No production integration.'
s['guild_entrance']=json.dumps({'local_u':0,'local_v':front,'world_y':16.05,'door_width':2.392,'door_height':2.7,'landing_depth':front-29.2,'stair_run':.9,'riser':.535/3,'stairs':3})
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild.blend')
pts=[o.matrix_world@v.co for name,c in cols.items()if name in ['Building shell','Roof and lantern','Timber and glazing','Ground and entrance']for o in c.objects if o.type=='MESH'for v in o.data.vertices]
print(json.dumps({'guildMeshes':sum(len(cols[n].objects)for n in['Building shell','Roof and lantern','Timber and glazing','Ground and entrance']),'bounds':[[min(p[i]for p in pts),max(p[i]for p in pts)]for i in range(3)],'entrance':json.loads(s['guild_entrance'])}))
