import bpy,math,json
from mathutils import Vector
s=bpy.context.scene;C={c.name.removeprefix('C1 / '):c for c in s.collection.children}
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
stone=bpy.data.materials['C1 / warm volcanic stone'];wood=bpy.data.materials['C1 / oiled timber'];metal=bpy.data.materials['C1 / deep green metal'];soil=bpy.data.materials['C1 / planting soil'];leaf=bpy.data.materials['C1 / tropical leaf']
def mesh(name,vs,fs,mat,col='Furniture'):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();me.materials.append(mat);o=bpy.data.objects.new(name,me);C[col].objects.link(o);return o
def box(name,p,size,mat,col='Furniture'):
 c=P(*p);a,b,h=[v/2 for v in size];vs=[tuple(c+Vector((i*a,j*b,k*h)))for k in[-1,1]for j in[-1,1]for i in[-1,1]];return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,col)
# Lower-court rail is unnecessary where the approved higher apron already retains the edge.
# A seat against that existing wall makes a coherent two-level gathering edge instead.
for o in list(C['Proposed routes'].objects):
 if not o.name.startswith('Court perimeter'):continue
 c=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices);x,z=c.x+36,44-c.y
 if abs(x-27.85)<.1 and 4.8<z<10.9:bpy.data.objects.remove(o,do_unlink=True)
for z in[4.9,5.9,6.9,7.9]:box('Retained exposed-edge post',(27.85,z,22.325),(.055,.055,1.05),metal,'Proposed routes')
for h in[.40,.70,1.05]:box('Retained exposed-edge rail',(27.85,6.4,21.8+h),(.065,3.0,.065),wood if h>1 else metal,'Proposed routes')
box('Apron-facing stone seat plinth',(27.55,11.1,22.0),(.90,5.0,.40),stone)
for x in[27.20,27.46,27.72]:box('Apron-facing timber seat',(x,11.1,22.225),(.23,5.0,.05),wood)
for z in[8.25,13.95]:
 box('Seat-end planted trough',(27.55,z,22.125),(.9,.7,.65),stone,'Planting');box('Seat-end soil',(27.55,z,22.45),(.76,.56,.025),soil,'Planting')
 for k in range(6):
  a=k*math.tau/6;p=P(27.55,z,22.47);mid=p+Vector((.18*math.cos(a),.18*math.sin(a),.45));tip=p+Vector((.3*math.cos(a),.3*math.sin(a),.25));side=Vector((-.075*math.sin(a),.075*math.cos(a),0));mesh('Seat-end tropical leaf',[tuple(p),tuple(mid+side),tuple(tip),tuple(mid-side)],[(0,1,2,3)],leaf,'Planting')
# Eliminate coincident cylindrical faces below the basin rim: a deliberate narrower stone foot.
o=bpy.data.objects['Fountain stone foot'];center=P(24,9,0)
for v in o.data.vertices:
 v.co.x=center.x+(v.co.x-center.x)*.97;v.co.y=center.y+(v.co.y-center.y)*.97
# Keep both leaf tips and the pool in the second pedestrian view.
o=bpy.data.objects['C1 Square interior eye 1.65m'];o.data.lens=23;target=P(24,8,23.9);o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
s['eastern_seating_edge']='New lower-court timber seat abuts protected raised apron; only redundant new rail removed. Original market and interfaces untouched.'
s['minimum_fountain_east_clearance_m']=27.10-(24+1.42)
s.camera=bpy.data.objects['C1 Market-to-square eye 1.65m'];s.render.filepath='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/town-square-r0c1a/01-market-arrival.png';bpy.ops.render.render(write_still=True)
print(s.render.filepath)
