"""Execute with live Blender MCP, starting from the independent S2-B copy."""
import bpy,math,json
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/storefront-s2b/'
assert bpy.data.filepath.startswith(OUT), 'Save an independent S2-B copy first; never run on approved S2-A.'
assert bpy.context.scene.name=='S2-A Tropical Storefront', 'Module preparation runs once on the fresh S2-B copy.'
s=bpy.context.scene;s.name='S2B Editable Modules'
categories=['Building shell','Shopfront and doors','Windows','Balcony','Roof A','Timber structures','Sun screens','Planters','Decorative props','Interior']
anchors={'Building shell':(0,0,0),'Shopfront and doors':(0,-3.55,.24),'Windows':(0,0,0),'Balcony':(0,-2.85,3.5),'Roof A':(0,.5,6.45),'Timber structures':(0,0,0),'Sun screens':(1.26,-3.14,4.08),'Planters':(0,0,0),'Decorative props':(0,-3.55,0),'Interior':(0,0,0)}
collections={};roots={}
for name in categories:
 c=bpy.data.collections.new('S2B / Modules / '+name);s.collection.children.link(c);collections[name]=c
 r=bpy.data.objects.new(name.replace(' ','')+'Socket',None);r.location=anchors[name];c.objects.link(r);r['module']=name;r['unit']='metres';r['socket_world']=list(anchors[name]);roots[name]=r
bpy.context.view_layer.update()
rows=[]
for o in list(s.objects):
 if o.type not in ['MESH','FONT']:continue
 old=o.users_collection[0].name;n=o.name.lower()
 if 'Streets' in old or 'Props' in old:continue
 if 'Roof' in old:cat='Roof A'
 elif 'Landscape' in old:cat='Planters'
 elif 'Interior' in old:cat='Interior'
 elif 'screen' in n:cat='Sun screens'
 elif 'lamp' in n or 'light' in n or 'sign' in n:cat='Decorative props'
 elif 'kenney' in n or 'side shop' in n or 'rear lower glazing' in n or 'glazed insert' in n or 'window stone sill' in n:cat='Windows'
 elif 'Terrace' in old or 'balcony fascia' in n:cat='Balcony'
 elif 'Shell' in old or 'wall' in n:cat='Building shell'
 elif any(v in n for v in ['post','brace','roof header','soffit','column stone']):cat='Timber structures'
 else:cat='Shopfront and doors'
 w=o.matrix_world.copy()
 for c in list(o.users_collection):c.objects.unlink(o)
 collections[cat].objects.link(o);o.parent=roots[cat];o.matrix_world=w
 o['module']=cat
 # Preserve Roof A exactly; simplify only small bevel cross sections elsewhere.
 changes=[]
 if cat!='Roof A':
  for mod in o.modifiers:
   if mod.type=='BEVEL' and mod.width<=.03 and mod.segments>1:
    changes.append({'modifier':mod.name,'segments_before':mod.segments,'segments_after':1});mod.segments=1
 o['optimization']='Micro bevel segment reduction only' if changes else 'Original geometry retained'
 rows.append({'object':o.name,'component':cat,'changes':changes})
bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
for row in rows:
 o=bpy.data.objects[row['object']];e=o.evaluated_get(deps);me=e.to_mesh();me.calc_loop_triangles();row['optimized_triangles']=len(me.loop_triangles);e.to_mesh_clear()
print('MODULE_AUDIT '+json.dumps({'objects':rows,'sockets':anchors}))
bpy.ops.wm.save_as_mainfile(filepath=OUT+'kopi-awan-modular.blend')
