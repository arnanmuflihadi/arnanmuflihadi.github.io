import bpy
scene=bpy.context.scene;rig=bpy.data.objects['D2 | FLIGHT RIG'];coll=bpy.data.collections['DRAGON | editable'];temp=bpy.data.collections.new('TEMP | export batch');scene.collection.children.link(temp)
bpy.ops.object.select_all(action='DESELECT');copies=[]
for obj in list(coll.objects):
 if obj.type=='MESH':
  dup=obj.copy();dup.data=obj.data.copy();temp.objects.link(dup);dup.select_set(True);copies.append(dup)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();combined=bpy.context.view_layer.objects.active;combined.name='Dragon | batched export'
old=[slot.material for slot in combined.material_slots];unique=[]
for mat in old:
 if mat not in unique:unique.append(mat)
ids=[unique.index(old[p.material_index]) for p in combined.data.polygons];combined.data.materials.clear()
for mat in unique:combined.data.materials.append(mat)
for poly,idx in zip(combined.data.polygons,ids):poly.material_index=idx
bpy.ops.object.select_all(action='DESELECT');combined.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
path='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/skyport-r0d2-gate-b/dragon-batched.glb'
bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_skins=True)
print('Exported objects:',len(copies),'materials:',len(unique))
bpy.data.objects.remove(combined,do_unlink=True);bpy.data.collections.remove(temp)
