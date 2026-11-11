import bpy,json
from mathutils import Vector
out='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/reset-final/'
scene=bpy.context.scene
furniture=list(bpy.data.collections['C1 / Furniture'].objects)
parts={'fountain':list(bpy.data.collections['C1 / Fountain'].objects)+[o for o in furniture if o.name.startswith('Fountain name')],'pavilion':list(bpy.data.collections['C1 / Timber shade'].objects)+[o for o in furniture if o.name.startswith(('Shaded timber seat','Seat stone pier'))],'bench':[o for o in furniture if o.name.startswith('Apron-facing')],'cafe-set':[o for o in furniture if o.name.startswith(('Square cafe table','Cafe table stem','Cafe chair'))]}
origins={'fountain':Vector((-12,35,3.2)),'pavilion':Vector((-13.5,31.45,3.2))};manifest={}
for part,objects in parts.items():
 if part not in origins:
  pts=[o.matrix_world@Vector(p)for o in objects for p in o.bound_box];origins[part]=Vector(((min(p.x for p in pts)+max(p.x for p in pts))/2,(min(p.y for p in pts)+max(p.y for p in pts))/2,3.2))
 root=bpy.data.objects.new('RESET reusable '+part,None);scene.collection.objects.link(root);root['reuse_source']='C1A approved geometry unchanged'
 for o in objects:
  matrix=o.matrix_world.copy();o.parent=root;o.matrix_world=matrix
 root.location=-origins[part]
 bpy.ops.object.select_all(action='DESELECT');root.select_set(True)
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=root
 bpy.ops.export_scene.gltf(filepath=out+part+'.glb',export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_apply=True)
 root.location=Vector((0,0,0));manifest[part]={'objects':len(objects),'origin_blender':list(origins[part]),'source':'C1A / '+part,'license':'Project-original approved C1A geometry'}
bpy.ops.wm.save_as_mainfile(filepath=out+'civic-reuse.blend')
print('CIVIC_MANIFEST:'+json.dumps(manifest))
