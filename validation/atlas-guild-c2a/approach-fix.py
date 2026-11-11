import bpy,bmesh,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-c2a/';site=bpy.data.collections['C2A / Site and approach'];terrain=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,120),Vector((0,0,-1)))[0].z+18.6
for o in list(site.objects):
 if any(k in o.name for k in ['stone arrival fan','arrival fan scribed','six-riser','entrance stair']):bpy.data.objects.remove(o,do_unlink=True)
stone=bpy.data.materials['C1 / warm volcanic stone'];sand=bpy.data.materials['C1 / warm limestone'];metal=bpy.data.materials['C1 / deep green metal'];wood=bpy.data.materials['C1 / oiled timber']
def mesh(n,vs,fs,mat,walk=False,col=site):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();o=bpy.data.objects.new('Guild / '+n,me);col.objects.link(o);o['proposed_walkable']=walk
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
def beam(n,a,b,w,mat):
 a,b=P(*a),P(*b);v=(b-a).normalized();side=v.cross(Vector((0,0,1)))
 if side.length<.001:side=Vector((1,0,0))
 side.normalize();other=v.cross(side).normalized();vs=[p+side*i*w/2+other*j*w/2 for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 return mesh(n,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
p0=(40,-4);p1=(39,-3.7);p2=(37.5,-2.9);curve=[]
for i in range(41):
 t=i/40;curve.append(tuple((1-t)**2*p0[k]+2*t*(1-t)*p1[k]+t*t*p2[k]for k in range(2)))
length=sum(math.dist(a,b)for a,b in zip(curve,curve[1:]));cum=0;vs=[];rows=[]
for i,(x,z)in enumerate(curve):
 if i:cum+=math.dist(curve[i-1],curve[i])
 t=cum/length;pre=curve[max(0,i-1)];nxt=curve[min(40,i+1)];dx,dz=nxt[0]-pre[0],nxt[1]-pre[1];l=math.hypot(dx,dz);nx,nz=-dz/l,dx/l;centre=G(*p0)+(22.95-G(*p0))*t
 for j in range(7):
  q=(j/6-.5)*(1.2+.6*min(1,t*3));xx,zz=x+nx*q,z+nz*q;g=G(xx,zz);y=max(g+.025,centre+(g-G(x,z))*max(0,1-t*3));vs.append(P(xx,zz,y))
 rows.append({'x':x,'z':z,'y':max(G(x,z)+.025,centre),'nx':nx,'nz':nz,'half':(1.2+.6*min(1,t*3))/2,'t':t})
mesh('smooth stone arrival fan',vs,[(i*7+j,i*7+j+1,i*7+j+8,i*7+j+7)for i in range(40)for j in range(6)],sand,True)
for j in[0,6]:
 v=[]
 for i in range(41):
  p=vs[i*7+j];v.extend([p,P(p.x+36,44-p.y,G(p.x+36,44-p.y)-.14)])
 mesh('smooth arrival terrain edge',v,[(2*i,2*i+2,2*i+3,2*i+1)for i in range(40)],stone)
# Only the exposed upper fan edges need guards; ground-level entrance remains open.
for sign in[-1,1]:
 selected=[r for r in rows if r['t']>.35]
 for j in range(0,len(selected),9):
  r=selected[j];x,z=r['x']+r['nx']*r['half']*sign,r['z']+r['nz']*r['half']*sign;y=r['y'];beam('fan edge post',(x,z,y),(x,z,y+1),.055,metal)
 for a,b in zip(selected,selected[1:]):
  for h in[.5,1.0]:beam('fan edge rail',(a['x']+a['nx']*a['half']*sign,a['z']+a['nz']*a['half']*sign,a['y']+h),(b['x']+b['nx']*b['half']*sign,b['z']+b['nz']*b['half']*sign,b['y']+h),.05,wood)
a=(37.5,-2.9);b=(35.6,-3.4);dx,dz=b[0]-a[0],b[1]-a[1];run=math.hypot(dx,dz);nx,nz=-dz/run,dx/run;rise=(24.2-22.95)/7;w=2.3
for i in range(7):
 cs=[(a[0]+dx*t+nx*w/2*sign,a[1]+dz*t+nz*w/2*sign)for t,sign in[(i/7,-1),((i+1)/7,-1),((i+1)/7,1),(i/7,1)]];top=22.95+(i+1)*rise;v=[P(x,z,min(G(x,z)-.14,top-.12))for x,z in cs]+[P(x,z,top)for x,z in cs]
 mesh('seven-riser entrance stair',v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand,True)
for sign in[-1,1]:
 for t in[0,.5,1]:
  x,z=a[0]+dx*t+nx*w*.48*sign,a[1]+dz*t+nz*w*.48*sign;y=22.95+(24.2-22.95)*t;beam('entrance stair post',(x,z,y),(x,z,y+1.02),.06,metal)
 for h in[.5,1.02]:beam('entrance stair rail',(a[0]+nx*w*.48*sign,a[1]+nz*w*.48*sign,22.95+h),(b[0]+nx*w*.48*sign,b[1]+nz*w*.48*sign,24.2+h),.065,wood)
d=json.loads(s['c2a_design']);d['approach'].update({'fan_points':curve,'fan_run':length,'fan_end_y':22.95,'fan_nominal_grade':(22.95-G(40,-4))/length,'fan_width':[1.2,1.8],'stair_start':[37.5,22.95,-2.9],'risers':7,'riser':rise});s['c2a_design']=json.dumps(d)
# Replace only the proposed-route plan annotation.
plan=bpy.data.collections['C2A / Measured plan'];old=bpy.data.objects['Proposed Guild entrance'];mat=old.data.materials[0];bpy.data.objects.remove(old,do_unlink=True);points=curve+[[35.6,-3.4],[34.1,-4.2]];v=[];fs=[]
for a,b in zip(points,points[1:]):
 dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);nx,nz=-dz/l*.065,dx/l*.065;i=len(v);v.extend(P(x,z,48.2)for x,z in[(a[0]+nx,a[1]+nz),(a[0]-nx,a[1]-nz),(b[0]-nx,b[1]-nz),(b[0]+nx,b[1]+nz)]);fs.append((i,i+1,i+2,i+3))
o=mesh('Proposed Guild entrance',v,fs,mat,col=plan);o.visible_shadow=False
bpy.data.objects['Entrance label'].data.body='Entrance 24.20 m\n7 x 179 mm / 2.30 m wide'
# Save measured centre profile from actual fan vertices, free of folded strips.
grades=[abs(b['y']-a['y'])/math.hypot(b['x']-a['x'],b['z']-a['z'])for a,b in zip(rows,rows[1:])]
report=json.loads(s['c2a_evidence']);report['design']=d;report['approach_profile']={'fan_length':length,'max_measured_fan_grade':max(grades),'centre_samples':[[r['x'],r['z'],r['y']]for r in rows],'controller_tested':False,'local_final_route_length':length+run+1.7,'direct_branch_to_door':math.hypot(40-34.1,-4+4.2)};s['c2a_evidence']=json.dumps(report)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend');print(json.dumps({'run':length,'fan_grade_max':max(grades),'stair_riser':rise,'new_route':length+run+1.7}))
