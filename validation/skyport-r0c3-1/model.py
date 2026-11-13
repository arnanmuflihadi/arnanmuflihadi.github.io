import bpy,math,json
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/skyport-r0c3-1/'
s=bpy.context.scene;s.name='Pelabuhan Awan / C3.1 independent derivative'
post=next(o for o in s.objects if o.name.startswith('Reused pavilion timber pier'))
shoe=next(o for o in s.objects if o.name.startswith('Reused pavilion stone shoe'))
lamp=next(o for o in s.objects if o.name.startswith('Kenney / canopy lantern'))
wood=bpy.data.materials['C1 / oiled timber'];bronze=bpy.data.materials['C1 / weathered bronze'];jade=next(m for m in bpy.data.materials if m.name.startswith('Skyport / enamel jade'))
details=bpy.data.collections.new('C3.1 / Editable additions');s.collection.children.link(details)
def mesh(name,verts,faces,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);me.update();o=bpy.data.objects.new(name,me);details.objects.link(o);return o
def component(src,name,pos,size,mat):
 dg=bpy.context.evaluated_depsgraph_get();old=bpy.data.meshes.new_from_object(src.evaluated_get(dg),depsgraph=dg);points=[src.matrix_world@v.co for v in old.vertices];lo=Vector(tuple(min(p[i]for p in points)for i in range(3)));hi=Vector(tuple(max(p[i]for p in points)for i in range(3)));c=(lo+hi)/2;verts=[tuple(pos[i]+(p[i]-c[i])*size[i]/(hi[i]-lo[i])for i in range(3))for p in points];faces=[tuple(reversed(p.vertices))if src.matrix_world.determinant()<0 else tuple(p.vertices)for p in old.polygons];o=mesh(name,verts,faces,mat);o['source']=src.name;bpy.data.meshes.remove(old);return o
def box(name,pos,size,mat):
 x,y,z=pos;a,b,c=[v/2 for v in size];v=[(x+dx*a,y+dy*b,z+dz*c)for dx,dy,dz in[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]];return mesh(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
def ring(name,x,y,z,r=.19,t=.035):
 verts=[];n,m=16,4
 for i in range(n):
  a=i*math.tau/n
  for j in range(m):
   b=j*math.tau/m;verts.append((x+(r+t*math.cos(b))*math.cos(a),y+t*math.sin(b),z+(r+t*math.cos(b))*math.sin(a)))
 return mesh(name,verts,[(i*m+j,((i+1)%n)*m+j,((i+1)%n)*m+(j+1)%m,i*m+(j+1)%m)for i in range(n)for j in range(m)],bronze)
def footing(u,v,z):
 o=component(shoe,'Reused civic shoe / bronze dock anchor',(u,v+7,z+.10),(.55,.55,.20),bronze)
 for p in o.data.vertices:
  if p.co.z<z+.01:
   key=f'{p.co.x:.6f},{p.co.y-7:.6f}';p.co.z=site['sample'][key]-.015
 return o
for a in site['anchors'][:2]:
 x,v,z=a['u'],a['v'],a['offset'];y=v+7;footing(x,v,z);component(post,'Reused timber / mooring pylon',(x,y,z+1.09),(.25,.25,1.95),wood)
 box('Bronze pylon cap',(x,y,z+2.09),(.36,.36,.13),bronze);box('Forged cross-cleat',(x,y,z+1.57),(.72,.15,.13),bronze)
 for d in [-.30,.30]:box('Cleat upturned horn',(x+d,y,z+1.65),(.09,.15,.17),bronze)
 box('Eye mounting plate',(x,y+.145,z+1.88),(.18,.06,.32),bronze);ring('Closed docking eye / no active rope',x,y+.205,z+1.90)
a=site['anchors'][2];x,v,z=a['u'],a['v'],a['offset'];y=v+7;footing(x,v,z);component(post,'Reused timber / single wind standard',(x,y,z+2.45),(.18,.18,4.5),wood)
for h in [.3,3.55,4.48]:box('Bronze mast band',(x,y,z+h),(.235,.235,.09),bronze)
component(lamp,'Reused Kenney fixture / navigation lantern',(x,y,z+4.73),(.34,.34,.40),bronze)
box('Jade beacon lens',(x,y+.18,z+4.73),(.20,.018,.17),jade)
mesh('Compact copper beacon cap',[(x-.24,y-.24,z+4.93),(x+.24,y-.24,z+4.93),(x+.24,y+.24,z+4.93),(x-.24,y+.24,z+4.93),(x,y,z+5.10)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)],bronze)
box('Wind-standard arm',(x-.66,y,z+4.48),(1.5,.10,.10),bronze)
# Static shaped pennant, not a wind/boarding simulation. Two shallow folds keep it architectural rather than a flat UI card.
verts=[(x-.12,y,z+4.4),(x-.72,y+.04,z+4.4),(x-1.35,y-.015,z+4.4),(x-1.15,y-.015,z+4.04),(x-1.35,y-.015,z+3.66),(x-.72,y+.04,z+3.66),(x-.12,y,z+3.66)]
mesh('Jade wind pennant / static reserved transport identity',verts,[(0,1,5,6),(1,2,3,5),(3,4,5)],jade)
for h in [3.88,4.13]:mesh('Bronze wind-direction chevron',[(x-.37,y+.052,z+h+.09),(x-.53,y+.058,z+h),(x-.37,y+.052,z+h-.09),(x-.42,y+.052,z+h-.09),(x-.60,y+.058,z+h),(x-.42,y+.052,z+h+.09)],[(0,1,4,5),(1,2,3,4)],bronze)
for corners in site['ticks']:mesh('North-aligned bronze navigation tick',[(u,v+7,h)for u,v,h in corners],[(0,1,2,3)],bronze)
s['c31']='Three additions only: paired mooring pylons, one wind/beacon standard, four cardinal deck ticks. No base geometry or guard edits.'
s.render.filepath=OUT+'native-reference.png'
bpy.ops.wm.save_as_mainfile(filepath=OUT+'pelabuhan-awan-polish.blend')
print(json.dumps({'source':post.name,'shoe':shoe.name,'lantern':lamp.name,'newObjects':len(details.objects),'newMaterials':0,'file':bpy.data.filepath}))
