import bpy,json
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/skyport-r0c3/'
s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();buckets={};triangles=0;source_count=0
for c in s.collection.children:
 if any(q in c.name for q in ['Context','Views','Export']):continue
 for o in c.objects:
  if o.type not in {'MESH','FONT','CURVE'}:continue
  source_count+=1;me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg)
  for p in me.polygons:
   m=me.materials[p.material_index];b=buckets.setdefault(m.name,{'mat':m,'v':[],'f':[]});offset=len(b['v']);ids=list(p.vertices)
   if o.matrix_world.determinant()<0:ids.reverse()
   b['v'].extend(tuple(o.matrix_world@me.vertices[i].co)for i in ids);b['f'].append(tuple(range(offset,offset+len(ids))));triangles+=len(ids)-2
  bpy.data.meshes.remove(me)
for c in list(s.collection.children):
 if 'Export' in c.name:
  for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
  bpy.data.collections.remove(c)
export=bpy.data.collections.new('Skyport / Export');s.collection.children.link(export);bpy.ops.object.select_all(action='DESELECT')
for i,b in enumerate(buckets.values()):
 me=bpy.data.meshes.new('Skyport batch');me.from_pydata(b['v'],[],b['f']);me.materials.append(b['mat']);me.update();o=bpy.data.objects.new('Pelabuhan / '+b['mat'].name,me);export.objects.link(o);o.select_set(True);bpy.context.view_layer.objects.active=o
fmt=bpy.context.window_manager.operator_properties_last('EXPORT_SCENE_OT_gltf').export_format
bpy.ops.export_scene.gltf(filepath=OUT+'pelabuhan-awan.glb',export_format=fmt,use_selection=True,export_extras=True)
export.hide_render=export.hide_viewport=True;s['delivery']=json.dumps({'triangles':triangles,'batches':len(buckets),'sourceObjects':source_count,'exportedContext':False,'textures':0})
bpy.ops.wm.save_as_mainfile(filepath=OUT+'pelabuhan-awan.blend')
print(s['delivery'])
