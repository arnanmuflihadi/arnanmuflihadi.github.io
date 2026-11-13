import bpy,math,json,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-c2a/'
s=bpy.context.scene;cols={n:bpy.data.collections['C2A / '+n]for n in['Building shell','Roof and lantern','Timber and glazing','Site and approach','Scale and cameras','Measured plan']}
t=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([t.matrix_world@v.co for v in t.data.vertices],[list(p.vertices)for p in t.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,120),Vector((0,0,-1)))[0].z+18.6
sand=bpy.data.materials['C1 / warm limestone'];stone=bpy.data.materials['C1 / warm volcanic stone'];timber=bpy.data.materials['C1 / oiled timber'];metal=bpy.data.materials['C1 / deep green metal']
def mesh(n,vs,fs,mat):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();o=bpy.data.objects.new('Guild / '+n,me);cols['Site and approach'].objects.link(o);o['proposed_walkable']=True
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
def beam(n,a,b,w,mat):
 a,b=P(*a),P(*b);v=(b-a).normalized();side=v.cross(Vector((0,0,1)))
 if side.length<.001:side=Vector((1,0,0))
 side.normalize();other=v.cross(side).normalized();vs=[p+side*i*w/2+other*j*w/2 for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 return mesh(n,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
for o in list(cols['Site and approach'].objects):
 if any(k in o.name for k in ['final approach stone tread','stair guard']):bpy.data.objects.remove(o,do_unlink=True)
# A short terrain-fitted arrival fan, then six regular risers. No excavation or terrain editing.
points=[(44,-8),(44,-6.5),(42.4,-6.6)];lens=[math.dist(a,b)for a,b in zip(points,points[1:])];length=sum(lens);dense=[];cum=0
for a,b,l in zip(points,points[1:],lens):
 n=math.ceil(l/.2)
 for j in range(n):
  tt=j/n;dense.append((a[0]+(b[0]-a[0])*tt,a[1]+(b[1]-a[1])*tt,(cum+l*tt)/length))
 cum+=l
dense.append((*points[-1],1));vs=[]
for i,(x,z,tt)in enumerate(dense):
 prev=dense[max(0,i-1)];nxt=dense[min(len(dense)-1,i+1)];dx,dz=nxt[0]-prev[0],nxt[1]-prev[1];l=math.hypot(dx,dz);nx,nz=-dz/l,dx/l
 centre=G(44,-8)+(24.5-G(44,-8))*tt
 for j in range(7):
  q=(j/6-.5)*2.2;xx,zz=x+nx*q,z+nz*q;ground=G(xx,zz)
  # Initially fit the complete natural crossfall, flatten progressively into the stair landing.
  top=max(ground+.025,centre+(ground-G(x,z))*max(0,1-tt*2))
  vs.append(P(xx,zz,top))
fs=[]
for i in range(len(dense)-1):
 for j in range(6):k=i*7+j;fs.append((k,k+1,k+8,k+7))
o=mesh('terrain-fitted entrance fan',vs,fs,sand)
# Real side skirts extend to the unchanged surface instead of an invisible floor.
for sign,j in[(-1,0),(1,6)]:
 vv=[]
 for i in range(len(dense)):
  v=vs[i*7+j];x,z=v.x+36,44-v.y;vv.extend([v,P(x,z,G(x,z)-.12)])
 mesh('arrival fan terrain-scribed side',vv,[(2*i,2*i+2,2*i+3,2*i+1)for i in range(len(dense)-1)],stone)
a=(42.4,-6.6);b=(40.9,-6.25);dx,dz=b[0]-a[0],b[1]-a[1];run=math.hypot(dx,dz);nx,nz=-dz/run,dx/run;w=2.3
for i in range(6):
 cs=[(a[0]+dx*tt+nx*w/2*sign,a[1]+dz*tt+nz*w/2*sign)for tt,sign in[(i/6,-1),((i+1)/6,-1),((i+1)/6,1),(i/6,1)]];top=24.5+(i+1)/6
 vv=[P(x,z,min(G(x,z)-.12,top-.12))for x,z in cs]+[P(x,z,top)for x,z in cs]
 mesh('six-riser entrance stair',vv,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand)
for sign in[-1,1]:
 for tt in[0,.5,1]:
  x,z=a[0]+dx*tt+nx*w*.48*sign,a[1]+dz*tt+nz*w*.48*sign;y=24.5+tt
  beam('entrance stair post',(x,z,y),(x,z,y+1.02),.06,metal)
 for h in[.5,1.02]:beam('entrance stair rail',(a[0]+nx*w*.48*sign,a[1]+nz*w*.48*sign,24.5+h),(b[0]+nx*w*.48*sign,b[1]+nz*w*.48*sign,25.5+h),.065,timber)
# The entrance terrace is an intentional civic balcony; guard its exposed ends.
for a,b in[((37.57,-5.18,25.5),(37.57,-6.8,25.5)),((38.2,-5.18,25.5),(40.0,-5.18,25.5))]:
 for p in[a,b]:beam('terrace edge post',p,(p[0],p[1],p[2]+1.02),.06,metal)
 for h in[.5,1.02]:beam('terrace edge rail',(a[0],a[1],a[2]+h),(b[0],b[1],b[2]+h),.065,timber)
# Reproducible pedestrian camera at the approved boundary; no fictitious standing platform.
c=bpy.data.objects['C2A 02 Entrance and forecourt'];c.location=P(44,-8,G(44,-8)+1.65);c.rotation_euler=(P(39.4,-6.4,28.5)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=24
# Broad daylight fill for native renders; production lighting is untouched.
ld=bpy.data.lights.new('C2A daylight fill','AREA');lo=bpy.data.objects.new('C2A daylight fill',ld);cols['Scale and cameras'].objects.link(lo);lo.location=P(20,22,58);lo.rotation_euler=(P(39,-8,27)-lo.location).to_track_quat('-Z','Y').to_euler();ld.energy=1800;ld.shape='DISK';ld.size=28
s['c2a_design']=json.dumps({**json.loads(s['c2a_design']),'approach':{'start':[44,G(44,-8),-8],'fan_points':points,'fan_run':length,'fan_end_y':24.5,'fan_nominal_grade':(24.5-G(44,-8))/length,'stair_start':[42.4,24.5,-6.6],'stair_end':[40.9,25.5,-6.25],'stair_run':run,'risers':6,'riser':1/6,'width':2.3,'tested_traversal':False},'entrance_clear':[38.25,40.55],'current_phase':'concept exterior; not detailed model or playable export'})
s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100;s.cycles.samples=48;s.cycles.use_denoising=True;s.render.image_settings.file_format='PNG'
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend')
print(s['c2a_design'])
