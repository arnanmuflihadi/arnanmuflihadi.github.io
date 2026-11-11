import bpy, math
from mathutils import Vector
scene=bpy.context.scene
rig=bpy.data.objects['D2 | FLIGHT RIG'];coll=bpy.data.collections['DRAGON | editable']
# Soften the wing fan into a tapered scalloped trailing edge.
for side in ('L','R'):
 o=bpy.data.objects['Flight membrane '+side]
 for i in range(23):
  t=i/22
  for j in range(12):
   u=j/11;v=o.data.vertices[i*12+j];old_lead=-.48+.35*t
   trailing=old_lead+(.22+1.55*math.sin(math.pi*t)**.7)*(1-.12*math.sin(3*math.pi*t)**2)
   v.co.y=old_lead+(trailing-old_lead)*u
 o.data.update()
# Tapered crest fins emphasize the neck-to-tail silhouette; all have deform weights.
mat=bpy.data.materials['D2 | warm limestone']
for i,(y,z,h,w,bone) in enumerate([(-1.82,2.75,.14,.13,'neck'),(-1.55,2.68,.19,.16,'neck'),(-1.26,2.53,.22,.17,'neck'),(-.98,2.37,.24,.17,'neck'),(.85,2.03,.19,.15,'body'),(1.30,1.79,.18,.15,'tail1'),(1.75,1.62,.15,.14,'tail1'),(2.20,1.42,.12,.13,'tail2'),(2.70,1.23,.09,.11,'tail2')]):
 verts=[(-.06,y-w,z),(.06,y-w,z),(-.045,y+w,z),(.045,y+w,z),(0,y+w*.7,z+h)]
 faces=[(0,1,3,2),(0,4,1),(1,4,3),(3,4,2),(2,4,0)]
 me=bpy.data.meshes.new('Crest');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Neck / tail crest %02d'%i,me);coll.objects.link(o);o.data.materials.append(mat);o.parent=rig;o.vertex_groups.new(name=bone).add(list(range(5)),1,'REPLACE');m=o.modifiers.new('Flight armature','ARMATURE');m.object=rig
# Saddlebow is more upright and defines a distinct rider pocket.
for name in ('Saddle front bow','Saddle rear cantle'):
 o=bpy.data.objects[name]
 for v in o.data.vertices:
  v.co.z=2.30+(v.co.z-2.30)*1.6
 o.data.update()
rig.animation_data.action=None;scene.frame_set(1)
print('Refined fan profile, dorsal silhouette and saddle; scene:',scene.name)
