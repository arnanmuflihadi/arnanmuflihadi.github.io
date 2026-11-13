import bpy,bmesh,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-c2a/'
s=bpy.context.scene
assert bpy.data.filepath==OUT+'atlas-guild-design.blend'
s.name='R0-C2A / Atlas Guild / isolated design'
terrain=bpy.data.objects['C1 exact unchanged terrain reference']
bv=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,120),Vector((0,0,-1)))[0].z+18.6
cols={n:bpy.data.collections['C2A / '+n] for n in ['Building shell','Roof and lantern','Timber and glazing','Site and approach','Scale and cameras','Measured plan']}
plaster=bpy.data.materials['S2A / warm lime plaster'];sage=bpy.data.materials['S2A / recessed sage plaster'];timber=bpy.data.materials['C1 / oiled timber'];edge=bpy.data.materials['S2A / cut timber edges'];stone=bpy.data.materials['C1 / warm volcanic stone'];sand=bpy.data.materials['C1 / warm limestone'];metal=bpy.data.materials['C1 / deep green metal'];bronze=bpy.data.materials['C1 / weathered bronze'];roof=[bpy.data.materials['S2A / terracotta '+str(i)]for i in range(5)];glass=bpy.data.materials['S2C / upper blue green glazing'];ink=bpy.data.materials['C1 / sign lettering']
def mesh(name,vs,fs,mat,col):
 me=bpy.data.meshes.new(name);me.from_pydata([tuple(v)for v in vs],[],fs);me.materials.append(mat);me.update();o=bpy.data.objects.new('Guild / '+name,me);cols[col].objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
def box(n,x,z,y,w,d,h,mat,col='Building shell',bevel=0):
 vs=[P(x+i*w/2,z+j*d/2,y+k*h/2)for k in[-1,1]for j in[-1,1]for i in[-1,1]];o=mesh(n,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,col)
 if bevel:
  m=o.modifiers.new('Soft authored edge','BEVEL');m.width=bevel;m.segments=2
 return o
def beam(n,a,b,w,d,mat=timber,col='Timber and glazing'):
 a,b=P(*a),P(*b);axis=(b-a).normalized();side=axis.cross(Vector((0,0,1)))
 if side.length<.001:side=Vector((1,0,0))
 side.normalize();other=axis.cross(side).normalized();vs=[p+side*i*w/2+other*j*d/2 for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 return mesh(n,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,col)
def footing(n,x0,x1,z0,z1,top):
 cs=[(x0,z0),(x1,z0),(x1,z1),(x0,z1)];vs=[P(x,z,G(x,z)-.18)for x,z in cs]+[P(x,z,top)for x,z in cs]
 return mesh(n,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],stone,'Site and approach')
def wall(n,x0,x1,z,y0,y1,holes,mat=plaster):
 xs=sorted(set([x0,x1]+[a for h in holes for a in h[:2]]));ys=sorted(set([y0,y1]+[a for h in holes for a in h[2:]]));vs=[];fs=[]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(ys,ys[1:]):
   if any(h[0]<(a+b)/2<h[1]and h[2]<(c+d)/2<h[3]for h in holes):continue
   i=len(vs);vs.extend(P(x,zz,y)for zz in[z-.12,z+.12]for y in[c,d]for x in[a,b]);fs.extend(tuple(i+j for j in f)for f in[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)])
 return mesh(n,vs,fs,mat,'Building shell')
def glazing(n,x,z,y,w,h):
 box(n+' glass',x,z,y,w,.045,h,glass,'Timber and glazing')
 for xx in[x-w/2,x+w/2]:box(n+' jamb',xx,z+.035,y,.085,.11,h+.12,timber,'Timber and glazing')
 for yy in[y-h/2,y+h/2]:box(n+' sill',x,z+.035,yy,w+.15,.16,.09,edge,'Timber and glazing')
 box(n+' centre mullion',x,z+.06,y,.055,.09,h,timber,'Timber and glazing')
def hip(n,x,z,w,d,eave,peak):
 # Authored limasan roof: flared eaves, hipped ends, longitudinal ridge and real thickness.
 r=max(.2,(w-d)*.5);cs=[(x-w/2,z+d/2),(x+w/2,z+d/2),(x+w/2,z-d/2),(x-w/2,z-d/2)];vs=[P(a,b,eave)for a,b in cs]+[P(x-r,z,peak),P(x+r,z,peak)]
 o=mesh(n,vs,[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],roof[1],'Roof and lantern');mod=o.modifiers.new('Editable roof shell','SOLIDIFY');mod.thickness=.085
 for i in range(4):beam(n+' deep fascia',(*cs[i],eave),(*cs[(i+1)%4],eave),.13,.20,timber,'Roof and lantern')
 for i,j in[(0,4),(1,5),(2,5),(3,4)]:
  a=vs[i];b=vs[j];mesh(n+' terracotta hip cap',[a+Vector((-.055,0,.07)),a+Vector((.055,0,.07)),b+Vector((.055,0,.07)),b+Vector((-.055,0,.07))],[(0,1,2,3)],roof[3],'Roof and lantern')
 beam(n+' ridge', (x-r,z,peak+.06),(x+r,z,peak+.06),.19,.17,roof[2],'Roof and lantern')
 # Restrained tile courses retain roof rhythm without the prototype's heavy individual tiles.
 for sign in[-1,1]:
  for j in range(1,9):
   t=j/9;zz=z+sign*d*.5*t;yy=peak+(eave-peak)*t+.025;hw=r+(w*.5-r)*t
   beam(n+' tile course',(x-hw,zz,yy),(x+hw,zz,yy),.024,.024,roof[j%5],'Roof and lantern')
 return o
import bpy,math,json
from mathutils import Vector
s=bpy.context.scene
# Small planter is moved outside the entrance aperture; mature island trees stay untouched.
for n in ['Guild / terrace planted seat-edge','Guild / terrace planter soil']:
 o=bpy.data.objects[n];ys=[v.co.y for v in o.data.vertices];xs=[v.co.x for v in o.data.vertices];lo=min(xs);hi=max(xs)
 for v in o.data.vertices:v.co.x=(37.55-36)+(v.co.x-lo)/(hi-lo)*.58
# Relocate the human reference to the unobstructed east side of the doorway.
for o in bpy.data.collections['C2A / Scale and cameras'].objects:
 if o.type=='MESH':o.matrix_world.translation+=Vector((2.45,0,0))
# Replace the exposed ladder-like stem with a ventilated plaster-and-timber lantern base.
for o in list(bpy.data.collections['C2A / Roof and lantern'].objects):
 if any(k in o.name for k in ['lantern ventilation','lantern blue','lantern lower','lantern crown','survey finial','octagonal lantern ring','lantern vertical']):bpy.data.objects.remove(o,do_unlink=True)
# Helpers from design.py are already live in this MCP session; no approved file is rerun.
cx,cz=40.1,-7.2
for i in range(8):
 a=i*math.tau/8;b=(i+1)*math.tau/8;r=.86
 vs=[P(cx+r*math.cos(t),cz+r*math.sin(t),y)for y in[30.3,36.4]for t in[a,b]]
 mesh('lantern plaster shaft',vs,[(0,1,3,2)],sage,'Roof and lantern')
 beam('lantern shaft timber',(cx+r*math.cos(a),cz+r*math.sin(a),30.2),(cx+r*math.cos(a),cz+r*math.sin(a),36.4),.10,.10,timber,'Roof and lantern')
 # One narrow ventilation strip per side, rather than many open rungs.
 for h in[33.0,33.2,33.4]:beam('lantern shaft vent',(cx+(r+.02)*math.cos(a+.12),cz+(r+.02)*math.sin(a+.12),h),(cx+(r+.02)*math.cos(b-.12),cz+(r+.02)*math.sin(b-.12),h),.06,.08,metal,'Roof and lantern')
for level,r in[(36.35,1.62),(38.35,1.62)]:
 for i in range(8):
  a=i*math.tau/8;b=(i+1)*math.tau/8
  beam('observation lantern rim',(cx+r*math.cos(a),cz+r*math.sin(a),level),(cx+r*math.cos(b),cz+r*math.sin(b),level),.15,.16,edge,'Roof and lantern')
for i in range(8):
 a=i*math.tau/8;b=(i+1)*math.tau/8;r=1.57
 beam('observation lantern mullion',(cx+r*math.cos(a),cz+r*math.sin(a),36.35),(cx+r*math.cos(a),cz+r*math.sin(a),38.35),.13,.13,timber,'Roof and lantern')
 mesh('observation lantern glass',[P(cx+r*math.cos(t),cz+r*math.sin(t),y)for y in[36.45,38.25]for t in[a,b]],[(0,1,3,2)],glass,'Roof and lantern')
for name,r0,r1,y0,y1 in[('observation limasan crown',2.12,.45,38.48,40.0),('observation upper cap',.91,.05,40.15,40.75)]:
 vs=[P(cx+r*math.cos(i*math.tau/8),cz+r*math.sin(i*math.tau/8),y)for r,y in[(r0,y0),(r1,y1)]for i in range(8)]
 o=mesh(name,vs,[(i,(i+1)%8,(i+1)%8+8,i+8)for i in range(8)],roof[2],'Roof and lantern');o.modifiers.new('Roof thickness','SOLIDIFY').thickness=.08
 for i in range(8):beam(name+' fascia',(cx+r0*math.cos(i*math.tau/8),cz+r0*math.sin(i*math.tau/8),y0),(cx+r0*math.cos((i+1)*math.tau/8),cz+r0*math.sin((i+1)*math.tau/8),y0),.09,.14,edge,'Roof and lantern')
beam('survey finial',(cx,cz,40.7),(cx,cz,41.15),.055,.055,bronze,'Roof and lantern')
# Sweeping civic entrance canopy with actual curved timber trusses and glazed fanlight.
for o in list(bpy.data.collections['C2A / Timber and glazing'].objects):
 if any(k in o.name for k in ['entry brow front','cantilevered entrance rafter']):bpy.data.objects.remove(o,do_unlink=True)
for o in list(bpy.data.collections['C2A / Roof and lantern'].objects):
 if 'entrance brow terracotta'in o.name:bpy.data.objects.remove(o,do_unlink=True)
# Roof spans only the crown gap in front of the existing mature trees.
x0,x1=36.5,42.3;mid=39.4
for side in[-1,1]:
 vs=[];fs=[]
 for j in range(17):
  t=j/16;x=mid+side*2.9*t;h=32.7-3.0*(t**.68)
  for z in[-5.45,-7.9]:vs.append(P(x,z,h+(.12 if z==-5.45 else 0)))
 for j in range(16):fs.append((2*j,2*j+2,2*j+3,2*j+1))
 o=mesh('sweeping terracotta entrance roof',vs,fs,roof[side+2],'Roof and lantern');o.modifiers.new('Editable canopy shell','SOLIDIFY').thickness=.075
 for z in[-5.48,-6.4,-7.85]:
  for j in range(16):
   t=j/16;u=(j+1)/16;x=mid+side*2.9*t;xx=mid+side*2.9*u;h=32.55-3*(t**.68);hh=32.55-3*(u**.68)
   beam('curved portal timber truss',(x,z,h),(xx,z,hh),.12,.18,timber,'Timber and glazing')
 for j in range(1,9):
  t=j/9;x=mid+side*2.9*t;h=32.7-3*t**.68+.045
  beam('canopy tile seam',(x,-5.43,h+.12),(x,-7.92,h),.025,.025,roof[j%5],'Roof and lantern')
# A real fanlight, radial timber ribs and a restrained research compass.
points=[P(mid-2.7,-6.44,29.55),P(mid+2.7,-6.44,29.55)]
for j in range(17):
 t=1-j/8;x=mid+2.7*t;h=32.5-2.8*abs(t)**.68;points.append(P(x,-6.44,h))
mesh('arched research-hall fanlight',points,[tuple(range(len(points)))],glass,'Timber and glazing')
for t in[-.85,-.55,-.28,0,.28,.55,.85]:beam('fanlight radial timber',(mid,-6.37,29.55),(mid+2.65*t,-6.37,32.45-2.8*abs(t)**.68),.065,.09,edge,'Timber and glazing')
for x in[36.55,42.25]:beam('tall portal pier',(x,-6.45,25.5),(x,-6.45,29.85),.20,.22,timber,'Timber and glazing')
# Stone banding belongs to the supporting plinth, not decorative floating boxes.
for yy in[23.6,24.2,24.8]:
 for x in[36+i*.45 for i in range(18)]:
  if G(x,-6.78)+.1<yy:box('scribed plinth joint',x,-6.665,yy,.012,.012,min(.45,yy-G(x,-6.78)),sand,'Site and approach')
# Render-only context material clones retain native vegetation geometry and transforms.
clones={}
for o in bpy.data.collections['C1 / Context - existing island plants'].objects:
 if ' / tree / 'not in o.name or o.type!='MESH':continue
 for slot in o.material_slots:
  original=slot.material
  if not original:continue
  k=original.name
  if k not in clones:
   m=original.copy();m.name='C2A context / '+k
   if m.use_nodes:
    bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if bs:
     for link in list(m.node_tree.links):
      if link.to_node==bs and link.to_socket==bs.inputs['Base Color']:m.node_tree.links.remove(link)
     c=(.18,.30,.075,1)if any(w in k.lower()for w in['leaf','foliage','green','canopy'])else(.18,.27,.075,1)
     bs.inputs['Base Color'].default_value=c;bs.inputs['Roughness'].default_value=.9
   clones[k]=m
  slot.material=clones[k]
# Broaden the native square camera enough to include the entire revised crown.
s.camera=bpy.data.objects['C2A 01 Guild from Telaga Awan'];s.camera.data.lens=28
s.camera.rotation_euler=(P(39.8,-7.5,29.8)-s.camera.location).to_track_quat('-Z','Y').to_euler()
d=json.loads(s['c2a_design']);d['lantern_top']=41.15;d['concept_corrections']=['curved civic portal and fanlight','integrated plaster observation lantern','planter clear of the door'];d['context_materials']='isolated render-only tree material clones; geometry and tree positions unchanged';s['c2a_design']=json.dumps(d)
s.render.filepath=OUT+'pass2-square.png';s.render.resolution_x=1200;s.render.resolution_y=800;s.cycles.samples=24
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend');bpy.ops.render.render(write_still=True)
print(s.render.filepath)
