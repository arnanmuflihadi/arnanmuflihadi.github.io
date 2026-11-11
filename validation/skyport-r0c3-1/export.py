import bpy,json
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/skyport-r0c3-1/'
s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();buckets={};triangles=0
for o in bpy.data.collections['C3.1 / Editable additions'].objects:
 me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg)
 for p in me.polygons:
  mat=me.materials[p.material_index];b=buckets.setdefault(mat.name,{'mat':mat,'v':[],'f':[]});offset=len(b['v']);ids=list(p.vertices)
  if o.matrix_world.determinant()<0:ids.reverse()
  b['v'].extend(tuple(o.matrix_world@me.vertices[i].co)for i in ids);b['f'].append(tuple(range(offset,offset+len(ids))));triangles+=len(ids)-2
 bpy.data.meshes.remove(me)
old=bpy.data.collections.get('C3.1 / Export')
if old:
 for o in list(old.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.collections.remove(old)
c=bpy.data.collections.new('C3.1 / Export');s.collection.children.link(c);bpy.ops.object.select_all(action='DESELECT')
for name,b in buckets.items():
 me=bpy.data.meshes.new('Dock detail batch');me.from_pydata(b['v'],[],b['f']);me.materials.append(b['mat']);me.update();o=bpy.data.objects.new('C3.1 / '+name,me);c.objects.link(o);o.select_set(True);bpy.context.view_layer.objects.active=o
fmt=bpy.context.window_manager.operator_properties_last('EXPORT_SCENE_OT_gltf').export_format
bpy.ops.export_scene.gltf(filepath=OUT+'skyport-details-raw.glb',export_format=fmt,use_selection=True,export_extras=True)
c.hide_render=c.hide_viewport=True
s['c31_delivery']=json.dumps({'triangles':triangles,'materialBatches':len(buckets),'textures':0,'sourcePreserved':True})
bpy.ops.wm.save_as_mainfile(filepath=OUT+'pelabuhan-awan-polish.blend')
print(s['c31_delivery'])
