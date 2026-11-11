import bpy,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;C={c.name.removeprefix('C1 / '):c for c in s.collection.children}
t=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([t.matrix_world@v.co for v in t.data.vertices],[list(p.vertices)for p in t.data.polygons])
def G(x,z):return bv.ray_cast(Vector((x-36,44-z,140)),Vector((0,0,-1)))[0].z+18.6
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
sand=bpy.data.materials['C1 / warm limestone'];stone=bpy.data.materials['C1 / warm volcanic stone'];wood=bpy.data.materials['C1 / oiled timber'];metal=bpy.data.materials['C1 / deep green metal']
def mesh(name,vs,fs,mat,col='Proposed routes'):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();me.materials.append(mat);o=bpy.data.objects.new(name,me);C[col].objects.link(o);return o
def beam(name,a,b,w,d,mat,col='Proposed routes'):
 a,b=P(*a),P(*b);up=(b-a).normalized();side=up.cross(Vector((0,1,0)))
 if side.length<.01:side=up.cross(Vector((1,0,0)))
 side.normalize();other=up.cross(side).normalized();vs=[tuple(p+side*i*w/2+other*j*d/2)for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]];return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,col)
def rails(a,b,name):
 n=max(1,math.ceil(math.dist(a[:2],b[:2])/1.25))
 for i in range(n+1):
  t=i/n;p=tuple(a[k]+(b[k]-a[k])*t for k in range(3));beam(name+' post',p,(p[0],p[1],p[2]+1.05),.055,.055,metal)
 for h in[.40,.70,1.05]:beam(name+' rail',(a[0],a[1],a[2]+h),(b[0],b[1],b[2]+h),.065,.065,wood if h>1 else metal)
# Remove the steep ground-following sketch and its redundant small flight. The protected landing is retained.
for c in[C['Proposed routes'],C['Furniture']]:
 for o in list(c.objects):
  if o.name.startswith(('Aligned north gate stair','Proposed square to Guild approach','Court edge guard post','Court edge rail')):bpy.data.objects.remove(o,do_unlink=True)
path=[(26.6,4,21.8),(28.2,2.4,22.03),(31,-1.6,22.45),(34.5,-1.8,22.45)]
pts=[]
for a,b in zip(path,path[1:]):
 n=math.ceil(math.dist(a[:2],b[:2])/.55)
 for i in range(n):pts.append(tuple(a[k]+(b[k]-a[k])*i/n for k in range(3)))
pts.append(path[-1]);edges=[]
for i,p in enumerate(pts):
 a=pts[max(0,i-1)];b=pts[min(len(pts)-1,i+1)];dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);edges.append([(p[0]+dz/l*1.3*v,p[1]-dx/l*1.3*v,p[2])for v in[-1,1]])
vs=[tuple(P(x,z,y+h))for h in[-.16,0]for edge in edges for x,z,y in edge];n=len(edges)*2;fs=[]
for i in range(len(edges)-1):
 k=2*i;fs.extend([(n+k,n+k+1,n+k+3,n+k+2),(k,k+2,k+3,k+1),(k,k+n,k+2+n,k+2),(k+1,k+3,k+3+n,k+1+n)])
fs.extend([(0,1,1+n,n),(n-2,2*n-2,2*n-1,n-1)]);mesh('Graded civic approach deck',vs,fs,sand)
contacts=[]
for i in range(0,len(edges),3):
 edge=edges[i]
 for j,(x,z,y)in enumerate(edge):
  # Shoes and timber posts are visible; toe heights use the actual triangle mesh.
  g=G(x,z);beam('Approach stone shoe',(x,z,g-.15),(x,z,g+.18),.34,.34,stone);beam('Approach timber bearing',(x,z,g+.16),(x,z,y-.16),.15,.15,wood);contacts.append({'x':x,'z':z,'ground_y':g,'deck_y':y,'exposure_m':y-g})
 beam('Approach transverse bearer',(edge[0][0],edge[0][1],edge[0][2]-.21),(edge[1][0],edge[1][1],edge[1][2]-.21),.15,.18,wood)
for i in range(len(edges)-1):
 for j in[0,1]:
  a,b=edges[i][j],edges[i+1][j]
  for h in[.40,.70,1.05]:beam('Approach continuous guard',(a[0],a[1],a[2]+h),(b[0],b[1],b[2]+h),.065,.065,wood if h>1 else metal)
for i in range(0,len(edges),2):
 for p in edges[i]:beam('Approach guard post',p,(p[0],p[1],p[2]+1.05),.055,.055,metal)
# Nine treads rise from the verified existing terrain landing. The actual source deck is not edited.
a=Vector((36,0));b=Vector((34.5,-1.8));v=(b-a).normalized();side=Vector((-v.y,v.x));run=(b-a).length;bottom=20.754735;rise=(22.45-bottom)/9
for i in range(9):
 cen=a+(b-a)*(i+.5)/9;top=bottom+rise*(i+1);vs=[]
 for upper in[False,True]:
  for along,across in[(-1,-1),(1,-1),(1,1),(-1,1)]:
   xz=cen+v*(along*run/18)+side*(across*1.3);vs.append(tuple(P(xz.x,xz.y,top if upper else G(xz.x,xz.y)-.15)))
 mesh('Landing approach stair',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand)
for sign in[-1,1]:
 aa=a+side*1.3*sign;bb=b+side*1.3*sign;rails((aa.x,aa.y,bottom),(bb.x,bb.y,22.45),'Landing stair guard')
for a,b in[((20.55,4.1,21.8),(25.2,4.1,21.8)),((20.55,4.1,21.8),(20.55,10.8,21.8)),((20.55,14.35,21.8),(27.85,14.35,21.8)),((27.85,4.9,21.8),(27.85,10.8,21.8))]:rails(a,b,'Court perimeter')
we=G(17.8,12.6)+.08
for z in[11.30,13.90]:rails((20.5,z,21.8),(17.8,z,we),'Highland stair guard')
oldroutes=json.loads(s['routes']);r=[{'name':'Graded square approach from existing north landing','width':2.6,'points':pts,'playable':'NOT TESTED - isolated design'},{'name':'Future Guild approach reservation','width':2.6,'points':[(36,0,20.754735),(40,-4,G(40,-4)+.08),(44,-8,G(44,-8)+.08)],'playable':'UNBUILT - plan reservation only'},next(x for x in oldroutes if'natural trail'in x['name'])];s['routes']=json.dumps(r)
s['north_gate']=json.dumps({'start':list(path[0]),'end':list(path[-1]),'risers':0,'width':2.6,'max_designed_grade':max(abs((b[2]-a[2])/math.dist(a[:2],b[:2]))for a,b in zip(path,path[1:])),'tested':False})
s['landing_stair']=json.dumps({'start':[36,0,bottom],'end':[34.5,-1.8,22.45],'risers':9,'riser_m':rise,'tread_m':run/9,'width':2.6,'tested':False});s['approach_ground_contacts']=json.dumps(contacts)
s['arrival_correction']='Unchanged market stair/garden ramp -> existing (36,0) landing -> nine proposed risers -> terrain-supported shallow civic walk -> new court. No existing rail or furniture moved. New route NOT PLAYTESTED.'
# Update the symbolic plan route to the authored walk and stair, keeping future Guild a reservation.
for o in list(C['Plan annotations'].objects):
 if o.name.startswith('Plan main arrival')or o.name.startswith('Plan Proposed square'):bpy.data.objects.remove(o,do_unlink=True)
plan=[(36,14.2,0),(36,0,0),(34.5,-1.8,0),(31,-1.6,0),(28.2,2.4,0),(26.6,4,0)];vs=[]
for i,p in enumerate(plan):
 a=plan[max(0,i-1)];b=plan[min(len(plan)-1,i+1)];dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz)or 1;vs.extend([tuple(P(p[0]+dz/l*.12,p[1]-dx/l*.12,52)),tuple(P(p[0]-dz/l*.12,p[1]+dx/l*.12,52))])
mesh('Plan graded main route',vs,[(2*i,2*i+1,2*i+3,2*i+2)for i in range(len(plan)-1)],bpy.data.materials['C1 / terracotta'],'Plan annotations')
print(json.dumps({'stair_riser':rise,'stair_tread':run/9,'walk_max_grade':json.loads(s['north_gate'])['max_designed_grade'],'max_support':max(c['exposure_m']for c in contacts),'min_support':min(c['exposure_m']for c in contacts)}))
