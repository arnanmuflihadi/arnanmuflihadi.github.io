"""Native Blender convert/join path; preserves source normals and editable modules."""
import bpy,json
from mathutils import Matrix
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/storefront-s2b/'
assert bpy.data.filepath.startswith(OUT), 'Run only in the independent S2-B master.'
src=bpy.data.scenes['S2B Editable Modules'];bpy.context.window.scene=src
rb=bpy.data.collections['S2B / Modules / Roof B'];rb.hide_viewport=False
rootb=bpy.data.objects['RoofBSocket'];bpy.context.view_layer.update()
for o in rb.objects:
 if o.type=='MESH':
  o.parent=None;o.matrix_world=Matrix.Identity(4);o.parent=rootb;o.matrix_world=Matrix.Identity(4)
rb.hide_viewport=True
for old in list(bpy.data.scenes):
 if old.name.startswith('S2B Native Batched') or old.name.startswith('S2B Roof B Export'):
  for ob in list(old.objects):
   if len(ob.users_scene)==1:bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.scenes.remove(old)

def native_export(name,filename,lod=False,roofonly=False):
 bpy.context.window.scene=src
 scene=bpy.data.scenes.new(name);scene.world=src.world;scene.unit_settings.system='METRIC'
 root=bpy.data.objects.new('KopiAwanRoofB' if roofonly else 'KopiAwan',None);scene.collection.objects.link(root)
 cols=[rb] if roofonly else [c for c in src.collection.children if c.name.startswith('S2B / Modules / ') and c!=rb]
 for c in cols:
  for ob in c.objects:
   if ob.type not in ['MESH','FONT'] or (lod and 'laid terracotta tile courses' in ob.name):continue
   o=ob.copy();o.data=ob.data.copy();o.parent=None;o.matrix_world=ob.matrix_world.copy();scene.collection.objects.link(o)
   if lod:
    for mod in list(o.modifiers):
     if mod.type=='BEVEL' and mod.width<=.02:o.modifiers.remove(mod)
    if 'hip roof structural surface' in o.name:
     o.data.materials.clear();o.data.materials.append(bpy.data.materials['S2A / terracotta 2'])
 bpy.context.window.scene=scene
 for o in scene.objects:o.select_set(o.type in ['MESH','FONT'])
 bpy.context.view_layer.objects.active=next(o for o in scene.objects if o.type=='MESH');bpy.ops.object.convert(target='MESH')
 cats=sorted({o.get('module','Roof B') for o in scene.objects if o.type=='MESH'})
 for cat in cats:
  bpy.ops.object.select_all(action='DESELECT');obs=[o for o in scene.objects if o.type=='MESH' and o.get('module','Roof B')==cat]
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=bpy.context.object;o.name=cat.replace(' ','')+'Module'
  ref=next(a for a in src.objects if a.type=='EMPTY' and a.get('module')==cat)
  scene.cursor.location=ref.location;bpy.ops.object.origin_set(type='ORIGIN_CURSOR');bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);o.parent=root
  bpy.ops.object.material_slot_remove_unused()
  if o.data.uv_layers:
   o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
  if lod:
   mod=o.modifiers.new('Dissolve coplanar detail for distance','DECIMATE');mod.decimate_type='DISSOLVE';mod.angle_limit=.02
 bpy.ops.export_scene.gltf(filepath=OUT+filename,export_format='GLB',use_active_scene=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=True)
 return scene

native_export('S2B Native Batched LOD0','kopi-awan-optimized.glb')
native_export('S2B Native Batched LOD1','kopi-awan-lod1.glb',lod=True)
native_export('S2B Roof B Export','kopi-awan-roof-b.glb',roofonly=True)
bpy.context.window.scene=src
bpy.ops.wm.save_as_mainfile(filepath=OUT+'kopi-awan-modular.blend')
print('NATIVE_LOD1_AND_ROOF_B_SAVED')
