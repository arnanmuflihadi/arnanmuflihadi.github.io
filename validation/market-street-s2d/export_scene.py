"""Run through live Blender MCP in the independent S2-D copy only."""
import bpy,json,collections
from mathutils import Matrix
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/market-street-s2d/'
assert bpy.data.filepath==OUT+'market-street-export.blend'
src=bpy.data.scenes['S2C Market Street'];bpy.context.window.scene=src;bpy.context.view_layer.update()
scene=bpy.data.scenes.new('S2D Optimized Export');scene.world=src.world;scene.unit_settings.system='METRIC'
root=bpy.data.objects.new('MarketStreet36m',None);scene.collection.objects.link(root)
root['coordinate_mapping']='Three.js origin (36,18.6,44); local Blender (u,v,h) -> game (36+u,18.6+h,44-v)'
root['source']='S2C Market Street; conditional art approval; no production deployment'
grading=['Measured terrain / local art grading proposal','Measured entrance landscape connection','Continuous planted arrival embankment']
parts={}
for c in bpy.data.collections['S2C / Buildings'].children:
 for ob in c.all_objects:parts[ob.name]=c.name.split(' / ')[-1]
for ob in bpy.data.collections['S2C / Streets'].all_objects:parts[ob.name]='WalkableStreet'
for ob in bpy.data.collections['S2C / Landscape'].all_objects:parts[ob.name]='GradingStudy' if ob.name in grading else 'Landscape'
for ob in bpy.data.collections['S2C / Props'].all_objects:parts[ob.name]='StreetFurniture'
copies=[];shared={};counts=collections.Counter(o.data.name for o in src.objects if o.type=='MESH')
for ob in src.objects:
 if ob.type not in ['MESH','FONT']:continue
 o=ob.copy();o.data=ob.data.copy();o.parent=None;o.matrix_world=ob.matrix_world.copy();scene.collection.objects.link(o)
 o['batch']=parts[ob.name]
 # Preserve source geometry sharing for public trees/ferns; the glTF exporter instances these.
 repeat=ob.type=='MESH' and not ob.modifiers and counts[ob.data.name]>1 and parts[ob.name]=='Landscape'
 o['repeat']=repeat
 if repeat:
  if ob.data.name in shared:o.data=shared[ob.data.name]
  else:shared[ob.data.name]=o.data
 copies.append(o)
bpy.context.window.scene=scene
for o in copies:o.select_set(not o.get('repeat'))
bpy.context.view_layer.objects.active=next(o for o in copies if o.type=='MESH' and not o.get('repeat'))
bpy.ops.object.convert(target='MESH')
for batch in sorted(set(parts.values())):
 obs=[o for o in scene.objects if o.type=='MESH' and o.get('batch')==batch and not o.get('repeat')]
 if not obs:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=bpy.context.object;o.name=batch
 scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.object.material_slot_remove_unused()
 if o.data.uv_layers:o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
 o['walkable']=batch=='WalkableStreet';o['study_grading']=batch=='GradingStudy'
for o in scene.objects:
 if o==root:continue
 w=o.matrix_world.copy();o.parent=root;o.matrix_world=w
 if o.type=='MESH':o['source_phase']='S2-C'
bpy.context.view_layer.update()
dg=bpy.context.evaluated_depsgraph_get();cost=[]
for o in scene.objects:
 if o.type!='MESH':continue
 me=o.evaluated_get(dg).to_mesh();me.calc_loop_triangles()
 cost.append({'name':o.name,'triangles':len(me.loop_triangles),'slots':len(me.materials),'repeat':bool(o.get('repeat'))})
 o.evaluated_get(dg).to_mesh_clear()
bpy.ops.export_scene.gltf(filepath=OUT+'market-street-optimized.glb',export_format='GLB',use_active_scene=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=True,export_shared_accessors=True,export_unused_images=False)
bpy.context.window.scene=src
bpy.ops.wm.save_as_mainfile(filepath=OUT+'market-street-export.blend')
print('S2D_EXPORT_METRICS='+json.dumps({'total_triangles':sum(c['triangles'] for c in cost),'objects':cost,'shared_repeat_meshes':len(shared),'source_scene':src.name,'export_scene':scene.name}))
