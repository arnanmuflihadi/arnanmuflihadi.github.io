import bpy,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;C={c.name.removeprefix('C1 / '):c for c in s.collection.children}
floor=21.8
terrain=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices) for p in terrain.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,150),Vector((0,0,-1)))[0].z+18.6
def mat(n):return bpy.data.materials['C1 / '+n]
stone=mat('warm volcanic stone');sand=mat('warm limestone');wood=mat('oiled timber');metal=mat('deep green metal');clay=mat('terracotta');bronze=mat('weathered bronze');foam=mat('soft water highlights');water=mat('jade water')
def mesh(name,vs,fs,material,col):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);C[col].objects.link(o);me.materials.append(material);return o
def beam(name,a,b,w,d,material,col):
 a,b=P(*a),P(*b);up=(b-a).normalized();side=up.cross(Vector((0,1,0)))
 if side.length<.01:side=up.cross(Vector((1,0,0)))
 side.normalize();other=up.cross(side).normalized();vs=[tuple(p+side*i*w/2+other*j*d/2)for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]];return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],material,col)
def guard(a,b):
 length=math.dist(a[:2],b[:2]);n=math.ceil(length/1.3)
 for i in range(n+1):
  t=i/n;p=tuple(a[k]+(b[k]-a[k])*t for k in range(3));beam('Court edge guard post',p,(p[0],p[1],p[2]+1.05),.06,.06,metal,'Furniture')
 for h in[.38,.7,1.05]:beam('Court edge rail',(a[0],a[1],a[2]+h),(b[0],b[1],b[2]+h),.055,.06,wood if h>1 else metal,'Furniture')
# A real bench was found on the proposed west-edge access. Preserve it; remove the blocked proposal.
for o in list(C['Paving'].objects)+list(C['Furniture'].objects):
 if o.name.startswith(('Forecourt five-step','Entry handrail','Entry timber')):bpy.data.objects.remove(o,do_unlink=True)
# The protected apron remains intact, including its bench and tree. New square uses the existing north landing.
s['arrival_correction']='Blocked direct west-edge stair removed. Existing forecourt/stair or garden ramp -> north landing (36,0) -> new terrain path -> court north gate. Proposed path NOT PLAYTESTED.'
for o in list(C['Proposed routes'].objects):
 if o.name.startswith('North garden threshold step'):bpy.data.objects.remove(o,do_unlink=True)
a=(26.6,4);b=(28.2,2.4);dx,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dz);fwd=Vector((dx/length,dz/length));side=Vector((-fwd.y,fwd.x));end=G(*b)+.08
for i in range(6):
 centre=Vector(a)+fwd*(length*(i+.5)/6);top=floor+(end-floor)*(i+1)/6;vs=[]
 for h in[top-.26,top]:
  for along,across in[(-1,-1),(1,-1),(1,1),(-1,1)]:
   xz=centre+fwd*(along*length/12)+side*(across*1.3);vs.append(tuple(P(xz.x,xz.y,h)))
 o=mesh('Aligned north gate stair',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand,'Proposed routes');m=o.modifiers.new('Shallow stone arris','BEVEL');m.width=.012;m.segments=2
for v in[-1,1]:
 aa=Vector(a)+side*1.31;bb=Vector(b)+side*1.31
 if v<0:aa=Vector(a)-side*1.31;bb=Vector(b)-side*1.31
 guard((aa.x,aa.y,floor),(bb.x,bb.y,end))
# Guard only exposed retaining edges; leave two deliberate route gates.
guard((20.55,4.1,floor),(25.2,4.1,floor));guard((20.55,4.1,floor),(20.55,10.8,floor));guard((20.55,14.35,floor),(27.85,14.35,floor));guard((27.85,4.9,floor),(27.85,10.8,floor))
# Wider swept leaves provide a legible civic silhouette rather than thin wire-like stems.
for o in C['Fountain'].objects:
 if o.name.startswith('Swept bronze rain leaf'):
  for v in o.data.vertices:
   # Original ribbon spans normal (.84,-.54); increase width without increasing height.
   c=Vector((-12,35,0));delta=v.co-c;q=delta.x*.84-delta.y*.54;v.co.x+=q*.84*.65;v.co.y-=q*.54*.65
for o in list(C['Fountain'].objects):
 if o.name.startswith('Light rain veil strand'):
  # Keep a sparse intentional veil, avoiding the initial dense blue-wire impression.
  idx=int(o.name.rsplit('.',1)[-1])if'.'in o.name else 0
  if idx%2:bpy.data.objects.remove(o,do_unlink=True)
# A warm border and restrained inlaid civic ring distinguish new paving from the protected apron.
for o in C['Paving'].objects:
 if o.name.startswith('Warm stone paver'):
  centre=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices);x,z=centre.x+36,44-centre.y
  if x<21.1 or x>27.4 or z<4.6 or z>13.8:o.data.materials[0]=clay
# Daylight remains neutral and legible: softer physical sky, directional sun and local contact shading.
for n in s.world.node_tree.nodes:
 if n.type=='BACKGROUND':n.inputs['Strength'].default_value=.08
for o in C['Cameras'].objects:
 if o.type=='LIGHT' and o.data.type=='AREA':o.data.energy=950
 if o.type=='LIGHT' and o.data.type=='SUN':o.data.energy=3;o.data.angle=.12
s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True
# Reframe from the market's upper forecourt; camera remains exactly 1.65 m above protected paving.
cam=bpy.data.objects['C1 Market-to-square eye 1.65m'];cam.location=P(34.8,9.5,22.614+1.65);target=P(24,9.0,23.15);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=28
s['cameras']=json.dumps([{'name':o.name,'native_position':list(o.location),'rotation_euler':list(o.rotation_euler),'lens_mm':o.data.lens,'ortho_width':o.data.ortho_scale if o.data.type=='ORTHO' else None}for o in C['Cameras'].objects if o.type=='CAMERA'])
# Update plan text after rejecting the blocked short stair.
for o in C['Plan annotations'].objects:
 if o.type=='FONT' and o.data.body=='5 x 0.163 m':o.data.body='APPROACH VIA EXISTING NORTH LANDING';o.data.size=.42
s['north_gate'] = json.dumps({'start':[26.6,4,floor],'end':[28.2,2.4,end],'risers':6,'riser':(floor-end)/6,'tread':length/6,'width':2.6,'tested':False})
s.render.resolution_percentage=67;s.camera=cam;s.render.filepath='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/town-square-r0c1a/pass3-arrival.png'
bpy.ops.render.render(write_still=True)
print(json.dumps({'image':s.render.filepath,'north_gate_riser':(floor-end)/6,'proposed_arrival':'via existing north landing; NOT TESTED'}))
