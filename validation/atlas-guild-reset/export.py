import bpy,bmesh,json
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-reset/'
s=bpy.context.scene;names=['Building shell','Roof and lantern','Timber and glazing','Ground and entrance'];buckets={};dg=bpy.context.evaluated_depsgraph_get();source_count=0;tris=0
for name in names:
 for o in bpy.data.collections['Guild reset / '+name].objects:
  if o.type!='MESH':continue
  source_count+=1;ev=o.evaluated_get(dg);me=bpy.data.meshes.new_from_object(ev,depsgraph=dg)
  for p in me.polygons:
   mat=me.materials[p.material_index];key=(mat.name,bool(o.get('walkable',False)))
   if key not in buckets:buckets[key]={'material':mat,'vertices':[],'faces':[],'walkable':key[1]}
   b=buckets[key];offset=len(b['vertices']);b['vertices'].extend(tuple(o.matrix_world@me.vertices[i].co)for i in p.vertices);b['faces'].append(tuple(range(offset,offset+len(p.vertices))));tris+=len(p.vertices)-2
  bpy.data.meshes.remove(me)
previous=bpy.data.collections.get('Guild reset / Export batches')
if previous:
 for obj in list(previous.objects):bpy.data.objects.remove(obj,do_unlink=True)
 bpy.data.collections.remove(previous)
collection=bpy.data.collections.new('Guild reset / Export batches');s.collection.children.link(collection)
bpy.ops.object.select_all(action='DESELECT')
for i,b in enumerate(buckets.values()):
 me=bpy.data.meshes.new('Guild delivery batch');me.from_pydata(b['vertices'],[],b['faces']);me.materials.append(b['material']);me.update();obj=bpy.data.objects.new('Guild delivery '+str(i)+' / '+b['material'].name,me);collection.objects.link(obj);obj['walkable']=b['walkable'];obj['source']='Original R0-C2A Guild adapted to accepted RESET-FINAL reservation';obj.select_set(True);bpy.context.view_layer.objects.active=obj
fmt=bpy.context.window_manager.operator_properties_last('EXPORT_SCENE_OT_gltf').export_format
bpy.ops.export_scene.gltf(filepath=OUT+'atlas-guild.glb',export_format=fmt,use_selection=True,export_extras=True)
collection.hide_render=True;collection.hide_viewport=True
s['guild_delivery']=json.dumps({'sourceMeshes':source_count,'batches':len(buckets),'triangles':tris,'floorElevation':16.05,'datum':15.48,'origin':'Guild reservation centre; local u,v; no old site coordinates','fit':'All roof and entrance geometry inside 10 x 8 m reservation','nativeSourcePreserved':True})
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild.blend')
print(s['guild_delivery'])
