import bpy,json,math
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/market-street-s2e/'
assert bpy.data.filepath==OUT+'site-interface.blend'
src=bpy.data.scenes['S2E Interface Design'];bpy.context.window.scene=src;bpy.context.view_layer.update()
def camera(name,p,t,lens):
 if name in bpy.data.objects:return bpy.data.objects[name]
 data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);bpy.data.collections['S2E / Cameras'].objects.link(o);o.location=p;o.rotation_euler=(Vector(t)-Vector(p)).to_track_quat('-Z','Y').to_euler();data.lens=lens;return o
camera('S2E Side',(20,18,-1.91906081308613),(8.3,22.6,1.8),30)
camera('S2E Complete Site',(49,-39,48),(0,13,1),37)
camera('S2E Square',(0,34,5.664),(0,45,1.5),26)
camera('S2E Skyport',(-9,-16,.2),(0,15,4.8),26)
# Reuse the approved fern geometry/UVs as modest planting on the selected low retaining toes.
original=bpy.data.scenes['S2C Market Street'];bpy.context.window.scene=original;bpy.context.view_layer.update()
fern=next(o for o in original.objects if o.name=='Shared source fern / street planter')
me=fern.data.copy();points=[fern.matrix_world@v.co for v in me.vertices];lo=Vector(tuple(min(p[k] for p in points) for k in range(3)));hi=Vector(tuple(max(p[k] for p in points) for k in range(3)));centre=(lo+hi)/2;centre.z=lo.z;scale=.5/(hi.z-lo.z)
for vertex,p in zip(me.vertices,points):vertex.co=(p-centre)*scale
me.update();bpy.context.window.scene=src
h=bpy.data.collections['S2E / H Hybrid']
for old in list(h.objects):
 if old.name.startswith('Reused fern on retaining toe'):bpy.data.objects.remove(old,do_unlink=True)
for bed in list(h.objects):
 if 'toe planting' not in bed.name:continue
 pts=[bed.matrix_world@Vector(v) for v in bed.bound_box];centre=Vector(tuple((min(v[k] for v in pts)+max(v[k] for v in pts))/2 for k in range(3)));centre.z=max(v.z for v in pts)
 for sign in[-1,1]:
  ob=bpy.data.objects.new('Reused fern on retaining toe',me);h.objects.link(ob);ob.location=centre+Vector((0,sign*.45,.015));ob.rotation_euler.z=sign*.8
for old in list(bpy.data.scenes):
 if old.name.startswith('S2E Export') or old.name.startswith('S2E Debug'):
  for ob in list(old.objects):
   if len(ob.users_scene)==1:bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.scenes.remove(old)
manifest=json.loads(src['S2E_manifest']);results={} 
def export(name,collections,filename,ref=False):
 bpy.context.window.scene=src;bpy.context.view_layer.update();stage=bpy.data.scenes.new('S2E Export '+name);root=bpy.data.objects.new(name,None);stage.collection.objects.link(root)
 if name=='Common':root['site_manifest']=src['S2E_manifest']
 for c in collections:
  for ob in list(c.all_objects):
   if ob.type!='MESH':continue
   o=ob.copy();o.data=ob.data.copy();o.parent=None;o.matrix_world=ob.matrix_world.copy();o.hide_render=False;o.hide_viewport=False;stage.collection.objects.link(o);o['export_group']='Walkable' if o.get('walkable') else 'Structure'
 bpy.context.window.scene=stage;bpy.context.view_layer.update()
 for o in stage.objects:o.select_set(o.type=='MESH')
 bpy.context.view_layer.objects.active=next(o for o in stage.objects if o.type=='MESH');bpy.ops.object.convert(target='MESH')
 for key in['Walkable','Structure']:
  obs=[o for o in stage.objects if o.type=='MESH' and o.get('export_group')==key]
  if not obs:continue
  bpy.ops.object.select_all(action='DESELECT')
  for o in obs:o.select_set(True)
  expected=sum(len(o.data.vertices) for o in obs);bpy.context.view_layer.objects.active=obs[0];bpy.context.view_layer.update();bpy.ops.object.join();o=bpy.context.view_layer.objects.active;assert len(o.data.vertices)==expected,(name,key,len(o.data.vertices),expected);o.name=name+key;o['walkable']=key=='Walkable';o['collision_support_only']=ref;o.parent=root
  
  if len(o.material_slots):bpy.ops.object.material_slot_remove_unused()
  if o.data.uv_layers:o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
 bpy.context.view_layer.update();cost=[]
 for o in stage.objects:
  if o.type=='MESH':o.data.calc_loop_triangles();cost.append({'name':o.name,'triangles':len(o.data.loop_triangles),'material_slots':len(o.data.materials)})
 bpy.ops.export_scene.gltf(filepath=OUT+filename,export_format='GLB',use_active_scene=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=True,export_shared_accessors=True)
 results[name]={'objects':cost,'triangles':sum(c['triangles'] for c in cost),'file':filename}
export('Common',[bpy.data.collections['S2E / Common Interface']],'common-interface.glb')
export('A',[bpy.data.collections['S2E / A Terraced']],'foundation-a.glb')
export('B',[bpy.data.collections['S2E / B Braced']],'foundation-b.glb')
export('H',[bpy.data.collections['S2E / H Hybrid']],'foundation-hybrid.glb')
export('Collision',[bpy.data.collections['S2E / Collision References']],'support-reference.glb',True)
bpy.context.window.scene=src;src.camera=bpy.data.objects['S2E Side'];bpy.ops.wm.save_as_mainfile(filepath=OUT+'site-interface.blend')
print('S2E_EXPORT='+json.dumps(results))
