import bpy,math
from mathutils import Vector
s=bpy.data.scenes['S2-A Tropical Storefront'];bpy.context.window.scene=s
join=bpy.data.collections['S2A / Buildings / Joinery'];roof=bpy.data.collections['S2A / Buildings / Roof']
glass=bpy.data.materials['S2A / soft blue green glass'];wood=bpy.data.materials['S2A / oiled tropical timber']
def cube(name,loc,dim,mat,col):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name='S2A / '+name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);return o
for side in [-1,1]:
 for y in [1.35,-1.15]:cube('upper side glazed insert',(side*3.585,y,4.975),(.028,1.17,1.62),glass,join)
for x in [-1.75,1.75]:cube('upper rear glazed insert',(x,4.985,5),(1.36,.028,1.65),glass,join)
for x in [-.24,.24]:
 for y in [-.45,2.45]:cube('ridge vent support',(x,y,8.43),(.055,.055,.43),wood,roof)
for o in s.objects:
 if o.type=='LIGHT' and ('interior daylight' in o.name or 'upper room daylight' in o.name):
  if hasattr(o,'visible_glossy'):o.visible_glossy=False
  if hasattr(o,'visible_transmission'):o.visible_transmission=False
  o.data.energy=65 if 'interior' in o.name else 35
s.cycles.samples=64
c=bpy.data.objects['S2A / Facade roof detail'];c.location=(8,-12,8.9)
c.rotation_euler=(Vector((0,-2.7,5.6))-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=44
for camera,name,w,h in [('Street 1.65m','01-street-level',1500,1200),('Elevated three quarter','02-elevated',1500,1500),('Facade roof detail','03-facade-roof-detail',1500,1200)]:
 s.camera=bpy.data.objects['S2A / '+camera];s.render.resolution_x=w;s.render.resolution_y=h
 s.render.filepath='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/storefront-s2a/'+name+'.png'
 bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['S2A / Elevated three quarter'];s.render.resolution_x=1500;s.render.resolution_y=1500
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/storefront-s2a/kopi-awan-prototype.blend')
print('FINAL_THREE_VIEWS_AND_BLEND_SAVED')
