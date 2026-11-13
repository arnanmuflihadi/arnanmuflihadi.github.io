import bpy,json,math,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-c2a/';d=json.loads(s['c2a_design']);t=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([t.matrix_world@v.co for v in t.data.vertices],[list(p.vertices)for p in t.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,120),Vector((0,0,-1)))[0].z+18.6
# Refine the same concept's site only; the accepted town collections never move.
for cn in ['C2A / Building shell','C2A / Roof and lantern','C2A / Timber and glazing','C2A / Site and approach','C2A / Scale and cameras']:
 for o in bpy.data.collections[cn].objects:
  if o.type in ['MESH','FONT','CURVE']:o.matrix_world.translation+=Vector((-5.3,-2.6,-1.3))
site=bpy.data.collections['C2A / Site and approach']
for o in list(site.objects):
 if any(k in o.name for k in ['terrain-fitted entrance fan','arrival fan terrain-scribed side','six-riser entrance stair','entrance stair']):bpy.data.objects.remove(o,do_unlink=True)
# Restore the two earlier study transplants before evaluating the final selected site.
plants=bpy.data.collections['C1 / Context - existing island plants']
for r in d['groundcover_proposed_replants']:
 o=bpy.data.objects[r['name']];a,b=r['from'],r['to'];o.matrix_world.translation-=Vector((b[0]-a[0],-(b[1]-a[1]),G(*b)-G(*a)))
replants=[]
for o in list(plants.objects):
 if o.type!='MESH' or not any(k in o.name for k in ['fern','understory']):continue
 vs=[o.matrix_world@Vector(v)for v in o.bound_box];x=sum(v.x for v in vs)/8+36;z=44-sum(v.y for v in vs)/8;y=sum(v.z for v in vs)/8+18.6
 if 30.2<x<38.3 and -9<z<-4 and y>0:
  dest=(28.7+len(replants)*.9,-11.5);o.matrix_world.translation+=Vector((dest[0]-x,-(dest[1]-z),G(*dest)-G(x,z)));replants.append({'name':o.name,'from':[x,z],'to':dest})
sand=bpy.data.materials['C1 / warm limestone'];stone=bpy.data.materials['C1 / warm volcanic stone'];timber=bpy.data.materials['C1 / oiled timber'];metal=bpy.data.materials['C1 / deep green metal']
def mesh(n,vs,fs,mat,walk=False):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();o=bpy.data.objects.new('Guild / '+n,me);site.objects.link(o);o['proposed_walkable']=walk
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
def beam(n,a,b,w,mat):
 a,b=P(*a),P(*b);v=(b-a).normalized();side=v.cross(Vector((0,0,1)))
 if side.length<.001:side=Vector((1,0,0))
 side.normalize();other=v.cross(side).normalized();vs=[p+side*i*w/2+other*j*w/2 for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 return mesh(n,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
# A short final branch from the existing route at (40,-4); the boundary spur remains intact.
points=[(40,-4),(39.2,-3.0),(38.2,-2.1),(37.5,-2.9)];length=sum(math.dist(a,b)for a,b in zip(points,points[1:]));dense=[];cum=0
for a,b in zip(points,points[1:]):
 l=math.dist(a,b);n=math.ceil(l/.18)
 for j in range(n):tt=j/n;dense.append((a[0]+(b[0]-a[0])*tt,a[1]+(b[1]-a[1])*tt,(cum+l*tt)/length))
 cum+=l
dense.append((*points[-1],1));vs=[]
for i,(x,z,tt)in enumerate(dense):
 a=dense[max(0,i-1)];b=dense[min(len(dense)-1,i+1)];dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);nx,nz=-dz/l,dx/l;width=1.2+min(1,tt*2)
 for j in range(7):
  q=(j/6-.5)*width;xx,zz=x+nx*q,z+nz*q;ground=G(xx,zz);y=max(ground+.025,G(40,-4)+(23.2-G(40,-4))*tt+(ground-G(x,z))*max(0,1-tt*2));vs.append(P(xx,zz,y))
mesh('stone arrival fan from approved route',vs,[(i*7+j,i*7+j+1,i*7+j+8,i*7+j+7)for i in range(len(dense)-1)for j in range(6)],sand,True)
for j in[0,6]:
 vv=[]
 for i in range(len(dense)):
  v=vs[i*7+j];vv.extend([v,P(v.x+36,44-v.y,G(v.x+36,44-v.y)-.14)])
 mesh('arrival fan scribed edge',vv,[(2*i,2*i+2,2*i+3,2*i+1)for i in range(len(dense)-1)],stone)
a=(37.5,-2.9);b=(35.6,-3.4);dx,dz=b[0]-a[0],b[1]-a[1];run=math.hypot(dx,dz);nx,nz=-dz/run,dx/run;w=2.3
for i in range(6):
 cs=[(a[0]+dx*tt+nx*w/2*sign,a[1]+dz*tt+nz*w/2*sign)for tt,sign in[(i/6,-1),((i+1)/6,-1),((i+1)/6,1),(i/6,1)]];top=23.2+(i+1)/6;vv=[P(x,z,min(G(x,z)-.14,top-.12))for x,z in cs]+[P(x,z,top)for x,z in cs]
 mesh('six-riser entrance stair',vv,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand,True)
for sign in[-1,1]:
 for tt in[0,.5,1]:
  x,z=a[0]+dx*tt+nx*w*.48*sign,a[1]+dz*tt+nz*w*.48*sign;y=23.2+tt;beam('entrance stair post',(x,z,y),(x,z,y+1.02),.06,metal)
 for h in[.5,1.02]:beam('entrance stair rail',(a[0]+nx*w*.48*sign,a[1]+nz*w*.48*sign,23.2+h),(b[0]+nx*w*.48*sign,b[1]+nz*w*.48*sign,24.2+h),.065,timber)
# Rescribe the relocated structural walls to the actual selected ground, not the old slope.
for o in site.objects:
 if 'plinth'not in o.name and 'entrance terrace'not in o.name:continue
 if o.type!='MESH' or any(k in o.name for k in ['joint','arris']):continue
 vs=[o.matrix_world@v.co for v in o.data.vertices];top=max(v.z for v in vs)
 for v,wv in zip(o.data.vertices,vs):
  if wv.z<top-.1:
   x,z=wv.x+36,44-wv.y;target=wv.copy();target.z=G(x,z)-18.6-.18;v.co=o.matrix_world.inverted()@target
# Cameras are authored from real support points, independent of the old failed framing.
def cam(n,pos,target,lens):
 c=bpy.data.objects[n];c.location=P(pos[0],pos[2],pos[1]);c.rotation_euler=(P(target[0],target[2],target[1])-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=lens
cam('C2A 01 Guild from Telaga Awan',[26,23.45,11.8],[34.5,29,-4.8],27)
cam('C2A 02 Entrance and forecourt',[29.2,G(29.2,.8)+1.65,.8],[34.1,27,-3.9],30)
cam('C2A 03 Town and Guild',[6,54,55],[32,25,5],39)
c=bpy.data.objects['C2A 04 Measured site plan'];c.location=P(32,3,130);c.rotation_euler=(P(32,3,0)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=60
s['c2a_design']=json.dumps({**d,'footprint':[30.5,38.1,-8.8,-4.2],'lower_floor':24.2,'rear_floor':25.6,'entrance':[34.1,24.2,-4.2],'lantern_top':39.85,'site_refinement':{'delta_x':-5.3,'delta_z':2.6,'reason':'avoid the approved approach corridor; reduce structural exposure; bring the landmark toward Telaga Awan'},'approach':{'branch':[40,G(40,-4),-4],'fan_points':points,'fan_run':length,'fan_end_y':23.2,'fan_nominal_grade':(23.2-G(40,-4))/length,'stair_start':[37.5,23.2,-2.9],'stair_end':[35.6,24.2,-3.4],'stair_run':run,'risers':6,'riser':1/6,'width':2.3,'tested_traversal':False},'groundcover_proposed_replants':replants,'reservation_boundary_preserved':[44,-8],'boundary_body_clearance':'surveyed separately against complete approved route'})
s.render.resolution_x=1440;s.render.resolution_y=960;s.cycles.samples=40;s.render.filepath=OUT+'01-guild-from-square.png';s.camera=bpy.data.objects['C2A 01 Guild from Telaga Awan'];bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend');bpy.ops.render.render(write_still=True)
print(s['c2a_design'])
