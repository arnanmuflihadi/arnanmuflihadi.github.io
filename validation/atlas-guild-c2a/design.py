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
cols={}
for n in ['Building shell','Roof and lantern','Timber and glazing','Site and approach','Scale and cameras','Measured plan']:
 c=bpy.data.collections.new('C2A / '+n);s.collection.children.link(c);cols[n]=c
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
# Two shallow structural tiers follow the hillside rather than one deep raised platform.
footing('lower hall terrain-scribed plinth',35.8,43.8,-8.8,-6.8,25.5)
footing('upper reading-room plinth',35.8,43.8,-11.4,-8.8,26.9)
box('lower floor rim',39.8,-7.8,25.43,8.22,2.22,.14,sand)
box('upper floor rim',39.8,-10.1,26.83,8.22,2.82,.14,sand)
wall('south facade with real entrance and display openings',35.8,43.8,-6.8,25.5,29.45,[(36.15,37.5,26.05,28.7),(38.25,40.55,25.5,28.25),(41.25,43.3,26.05,28.7)])
wall('rear clerestory wall',35.8,43.8,-11.4,26.9,29.5,[(36.4,43.2,28.15,29.15)],sage)
for xx in[35.8,43.8]:
 box('lower side wing',xx,-7.8,27.5,.22,2,4,plaster)
 box('upper side wing',xx,-10.1,28.2,.22,2.6,2.6,plaster)
 box('side material reveal',xx,-9.1,27.3,.25,4.6,.12,edge)
glazing('west research window',36.825,-6.65,27.375,1.35,2.65)
glazing('east research window',42.275,-6.65,27.375,2.05,2.65)
glazing('entrance double door',39.4,-6.64,26.85,2.3,2.7)
# Existing Kopi Awan door-pull geometry, normalized in place before copying.
source=bpy.data.objects['S2A / door pull.010'];ev=[source.matrix_world@v.co for v in source.data.vertices];centre=sum(ev,Vector())/len(ev)
for x in[39.29,39.51]:
 me=source.data.copy()
 for v,p in zip(me.vertices,ev):v.co=p-centre+P(x,-6.54,26.65)
 o=bpy.data.objects.new('Guild / reused Kopi brass door pull',me);cols['Timber and glazing'].objects.link(o)
glazing('rear daylight strip',39.8,-11.54,28.65,6.8,1.0)
for x in[36,38.05,40.8,43.55]:
 box('portal timber pier',x,-6.55,27.45,.18,.22,3.9,timber,'Timber and glazing')
 beam('roof knee brace',(x,-6.55,28.15),(x+.45,-6.55,29.32),.11,.12)
# Recessed terracotta band and vertical solar screens give an institutional facade rhythm.
box('continuous lintel',39.8,-6.55,29.15,8.4,.27,.25,timber,'Timber and glazing')
for x in[36.1+i*.19 for i in range(9)]+[41.1+i*.19 for i in range(14)]:
 box('solar screen fin',x,-6.39,28.8,.055,.32,.7,timber,'Timber and glazing')
hip('Limasan research-hall roof',39.8,-9.1,9.8,6.8,29.65,31.18)
# Cantilevered entry brow: open below, deep eaves, no forest-clearing portico platform.
beam('entry brow front', (37.55,-5.62,29.0),(41.25,-5.62,29.0),.15,.22)
for x in[37.65,38.5,39.4,40.3,41.15]:
 beam('cantilevered entrance rafter',(x,-8.0,29.1),(x,-5.5,29.13),.1,.16)
mesh('entrance brow terracotta',[P(37.4,-6.9,29.32),P(41.4,-6.9,29.32),P(41.4,-5.48,29.08),P(37.4,-5.48,29.08)],[(0,1,2,3)],roof[2],'Roof and lantern')
# Slender octagonal survey lantern occupies the measured gap between mature crowns.
cx,cz=40.1,-7.2
for level,r in[(29.7,.88),(33.4,.88),(36.3,.96)]:
 for i in range(8):
  a=i*math.tau/8;b=(i+1)*math.tau/8
  beam('octagonal lantern ring',(cx+r*math.cos(a),cz+r*math.sin(a),level),(cx+r*math.cos(b),cz+r*math.sin(b),level),.11,.12,edge,'Roof and lantern')
for i in range(8):
 a=i*math.tau/8;b=(i+1)*math.tau/8;r=.88
 beam('lantern vertical timber',(cx+r*math.cos(a),cz+r*math.sin(a),29.7),(cx+r*math.cos(a),cz+r*math.sin(a),36.3),.13,.13,timber,'Roof and lantern')
 vs=[P(cx+r*math.cos(t),cz+r*math.sin(t),yy)for yy in[33.5,36.2]for t in[a,b]]
 mesh('lantern blue-green glazing',vs,[(0,1,3,2)],glass,'Roof and lantern')
 for h in[30.15,30.65,31.15,31.65,32.15,32.65]:beam('lantern ventilation louver',(cx+r*math.cos(a),cz+r*math.sin(a),h),(cx+r*math.cos(b),cz+r*math.sin(b),h),.07,.10,timber,'Roof and lantern')
# Two hovering roof plates: contemporary limasan lantern, not castle battlements.
for name,r0,r1,y0,y1 in[('lantern lower eave',1.8,.6,36.45,37.5),('lantern crown',1.12,.05,37.9,39.05)]:
 vs=[P(cx+r*math.cos(i*math.tau/8),cz+r*math.sin(i*math.tau/8),y)for r,y in[(r0,y0),(r1,y1)]for i in range(8)]
 o=mesh(name,vs,[(i,(i+1)%8,(i+1)%8+8,i+8)for i in range(8)],roof[2],'Roof and lantern');m=o.modifiers.new('Editable eave thickness','SOLIDIFY');m.thickness=.08
 for i in range(8):beam(name+' rim',tuple([cx+r0*math.cos(i*math.tau/8),cz+r0*math.sin(i*math.tau/8),y0]),tuple([cx+r0*math.cos((i+1)*math.tau/8),cz+r0*math.sin((i+1)*math.tau/8),y0]),.08,.11,edge,'Roof and lantern')
beam('survey finial',(cx,cz,39),(cx,cz,39.65),.07,.07,bronze,'Roof and lantern')
# Physical compass medallion and restrained sign identify a research hall.
def text(n,body,x,z,y,size,mat):
 cu=bpy.data.curves.new(n,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.extrude=.003;o=bpy.data.objects.new('Guild / '+n,cu);cols['Timber and glazing'].objects.link(o);o.location=P(x,z,y);o.rotation_euler=(math.pi/2,0,0);cu.materials.append(mat);return o
box('guild sign backing',39.4,-6.47,28.7,2.7,.11,.52,metal,'Timber and glazing')
text('guild name','ATLAS GUILD',39.4,-6.39,28.6,.30,ink)
text('research subtitle','BALAI RISET  /  AKSES TRANSIT',39.4,-6.38,28.35,.095,ink)
# Measured final arrival: 12 risers from the approved boundary to a small supported landing.
a=(44,-8);b=(40.9,-6.25);ya=G(*a);yb=25.5;dx,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dz);nx,nz=-dz/length,dx/length;width=2.3
for i in range(12):
 cs=[]
 for t,sign in[(i/12,-1),((i+1)/12,-1),((i+1)/12,1),(i/12,1)]:cs.append((a[0]+dx*t+nx*width/2*sign,a[1]+dz*t+nz*width/2*sign))
 top=ya+(yb-ya)*(i+1)/12;vs=[P(x,z,min(G(x,z)-.15,top-.14))for x,z in cs]+[P(x,z,top)for x,z in cs]
 mesh('final approach stone tread',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand,'Site and approach')
for sign in[-1,1]:
 for i in range(4):
  t=i/3;x=a[0]+dx*t+nx*width*.48*sign;z=a[1]+dz*t+nz*width*.48*sign;y=ya+(yb-ya)*t
  beam('stair guard post',(x,z,y),(x,z,y+1.02),.06,.06,metal,'Site and approach')
 for h in[.5,1.02]:beam('stair guard',(a[0]+nx*width*.48*sign,a[1]+nz*width*.48*sign,ya+h),(b[0]+nx*width*.48*sign,b[1]+nz*width*.48*sign,yb+h),.065,.075,timber,'Site and approach')
footing('entrance terrace',37.55,42.1,-6.8,-5.15,25.5)
box('entrance terrace arris',39.825,-5.975,25.47,4.65,1.75,.06,sand,'Site and approach')
for x in[37.6+i*.5 for i in range(10)]:box('terrace paving joint',x,-5.975,25.506,.012,1.6,.006,stone,'Site and approach')
for z in[-5.2,-5.7,-6.2,-6.7]:box('terrace cross joint',39.825,z,25.507,4.6,.012,.006,stone,'Site and approach')
# One calm planted edge protects the exposed terrace without a cluster of railings.
for x0,x1 in[(37.55,39.45)]:
 box('terrace planted seat-edge', (x0+x1)/2,-5.22,25.95,x1-x0,.4,.9,sand,'Site and approach')
 box('terrace planter soil',(x0+x1)/2,-5.22,26.39,x1-x0-.15,.28,.05,bpy.data.materials['C1 / planting soil'],'Site and approach')
# Transplant only small existing groundcover inside the new footprint, not mature trees.
replants=[]
for o in list(bpy.data.collections['C1 / Context - existing island plants'].objects):
 if o.type!='MESH' or not('fern' in o.name or 'understory' in o.name):continue
 vs=[o.matrix_world@Vector(v)for v in o.bound_box];x=sum(p.x for p in vs)/8+36;z=44-sum(p.y for p in vs)/8;y=sum(p.z for p in vs)/8+18.6
 if 35.7<x<44.2 and -11.7<z<-5 and y>0:
  dest=(45.5+len(replants)%3,-12.5-len(replants)*.3);delta=Vector((dest[0]-x,-(dest[1]-z),G(*dest)-G(x,z)));o.matrix_world.translation+=delta;replants.append({'name':o.name,'from':[x,z],'to':dest})
# Retain the approved human reference and add one equivalent person beside the entrance.
refs=list(bpy.data.collections['C1 / Scale reference'].objects)
for o in refs:
 if o.type!='MESH':continue
 new=o.copy();new.data=o.data;cols['Scale and cameras'].objects.link(new);new.name='Guild / human scale / '+o.name
 # Reference is positioned as one group; establish group bounds below.
newrefs=list(cols['Scale and cameras'].objects)
if newrefs:
 vs=[o.matrix_world@Vector(v)for o in newrefs for v in o.bound_box];c=Vector(((min(v.x for v in vs)+max(v.x for v in vs))/2,(min(v.y for v in vs)+max(v.y for v in vs))/2,min(v.z for v in vs)))
 delta=P(38.1,-6,25.5)-c
 for o in newrefs:o.matrix_world.translation+=delta
# Named cameras, exact 1.65 m pedestrian heights.
def camera(n,pos,target,lens=32,ortho=None):
 cu=bpy.data.cameras.new('C2A '+n);o=bpy.data.objects.new('C2A '+n,cu);cols['Scale and cameras'].objects.link(o);o.location=P(pos[0],pos[2],pos[1]);t=P(target[0],target[2],target[1]);o.rotation_euler=(t-o.location).to_track_quat('-Z','Y').to_euler();cu.lens=lens
 if ortho:cu.type='ORTHO';cu.ortho_scale=ortho
 return o
camera('01 Guild from Telaga Awan',[26,23.45,11.8],[39.8,29,-7.5],30)
camera('02 Entrance and forecourt',[44.8,G(44.8,-4.2)+1.65,-4.2],[39.6,28,-7.1],25)
camera('03 Town and Guild',[9,54,53],[35,26,-1],40)
camera('04 Measured site plan',[35,130,5],[35,0,5],35,54)
s['c2a_design']=json.dumps({'phase':'R0-C2A isolated design','footprint':[35.8,43.8,-11.4,-6.8],'lower_floor':25.5,'rear_floor':26.9,'entrance':[39.4,25.5,-6.8],'lantern_top':39.65,'approach':{'start':[44,ya,-8],'end':[40.9,25.5,-6.25],'risers':12,'riser':(yb-ya)/12,'run':length,'width':width},'groundcover_proposed_replants':replants,'mature_trees_moved':0,'tested_traversal':False,'production_export':False})
s.camera=bpy.data.objects['C2A 01 Guild from Telaga Awan'];s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100;s.cycles.samples=32;s.cycles.use_denoising=True
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend')
print(json.dumps({'new_objects':sum(len(c.objects)for c in cols.values()),'site':json.loads(s['c2a_design'])}))
