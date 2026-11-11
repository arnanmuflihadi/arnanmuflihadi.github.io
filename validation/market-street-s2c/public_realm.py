"""36m terraced pedestrian realm, local grading study and selective tropical planting."""
s=bpy.data.scenes['S2C Market Street'];bpy.context.window.scene=s
cols={}
for name in ['Streets','Landscape','Props','Collision References','Cameras']:
 c=bpy.data.collections.new('S2C / '+name);s.collection.children.link(c);cols[name]=c
street=cols['Streets'];land=cols['Landscape'];props=cols['Props'];cams=cols['Cameras']
stone=bpy.data.materials['S2A / sandstone base'];wood=bpy.data.materials['S2A / oiled tropical timber'];timber=bpy.data.materials['S2A / cut timber edges'];bronze=bpy.data.materials['S2A / patinated bronze frames'];brass=bpy.data.materials['S2A / aged brass'];cream=bpy.data.materials['S2A / warm sign lettering'];sage=bpy.data.materials['S2A / recessed sage plaster'];soil=bpy.data.materials['S2A / planter soil']
pave=[mat('warm pedestrian stone '+str(i),(.49+i*.018,.45+i*.017,.35+i*.013),.91) for i in range(4)]
grasses=[mat('tropical meadow '+str(i),(.16+i*.02,.25+i*.026,.07+i*.012),.95) for i in range(3)]
leaves=[mat('broad tropical leaf '+str(i),(.06+i*.038,.19+i*.052,.035+i*.014),.82) for i in range(3)]
bark=mat('palm bark',(.22,.14,.065),.92);flower=mat('coral ginger bloom',(.66,.18,.09),.8)
plots=[(-8.3,10,9.4,8.5,1.442857142857),(8.3,11.2,8.7,7.3,1.634285714286),(-8.3,21.8,9.2,9.3,3.36),(8.3,22.6,9.6,9.3,3.36)]
samples={(u,v):h for u,v,h in SURVEY_GRID}
def raw_h(u,v):
 u=max(-18,min(18,u));v=max(-2,min(40,v));a=math.floor(u/2)*2;b=math.floor(v/2)*2
 a=min(16,a);b=min(38,b);tx=(u-a)/2;ty=(v-b)/2
 return (samples[(a,b)]*(1-tx)+samples[(a+2,b)]*tx)*(1-ty)+(samples[(a,b+2)]*(1-tx)+samples[(a+2,b+2)]*tx)*ty
def grade(u,v):
 h=raw_h(u,v)
 # Local proposed infill terraces only. Approved production terrain is untouched.
 for x,y,w,d,z in plots:
  dist=math.hypot(max(0,abs(u-x)-w/2),max(0,abs(v-y)-d/2))
  t=max(0,1-dist/3.5);t=t*t*(3-2*t);h=max(h,h+(z-.25-h)*t)
 if abs(u)<5.6 and 0<=v<=36:h=max(h,main_h(v)-.17)
 if 29<=v<=36 and abs(u)<8.1:h=max(h,4-.17)
 return h
# An actual sampled natural ground surface with explicitly proposed local fill under the art slice.
vs=[];fs=[];xs=list(range(-18,19));ys=list(range(-2,41))
for v in ys:
 for u in xs:vs.append((u,v,grade(u,v)))
for j in range(len(ys)-1):
 for i in range(len(xs)-1):k=j*len(xs)+i;fs.append((k,k+1,k+len(xs)+1,k+len(xs)))
ground=mesh('Measured terrain / local art grading proposal',vs,fs,grasses[0],land)
for m in grasses[1:]:ground.data.materials.append(m)
for p in ground.data.polygons:p.material_index=(p.index*7+p.index//19)%3;p.use_smooth=True

# Connected 10.4m public realm; 6m central route remains free of furniture.
profile=[(0,0),(4,.4)]
for a,b,z0,z1,n in [(4,6.4,.4,1.442857142857,6),(14.4,18,1.442857142857,3.36,11),(28,30,3.36,4,4)]:
 if profile[-1]!=(a,z0):profile.append((a,z0))
 for i in range(1,n+1):
  y=a+(b-a)*i/n;profile.append((y,z0+(z1-z0)*(i-1)/n));profile.append((y,z0+(z1-z0)*i/n))
profile.append((36,4))
vs=[];fs=[]
for y,z in profile:vs.extend([(-5.2,y,z),(5.2,y,z)])
for i in range(len(profile)-1):k=i*2;fs.append((k,k+1,k+3,k+2))
base=mesh('Continuous stepped market paving',vs,fs,stone,street)
so=base.modifiers.new('Paving build up','SOLIDIFY');so.thickness=.16
random.seed(27);vs=[];fs=[];colors=[]
for (ya,za),(yb,zb) in zip(profile,profile[1:]):
 if yb-ya<.02:continue
 ny=max(1,math.ceil((yb-ya)/1.1))
 for j in range(ny):
  a=ya+(yb-ya)*j/ny+.008;b=ya+(yb-ya)*(j+1)/ny-.008
  for i in range(16):
   x0=-5.2+10.4*i/16+.008;x1=-5.2+10.4*(i+1)/16-.008;k=len(vs)
   az=za+(zb-za)*(a-ya)/(yb-ya)+.012;bz=za+(zb-za)*(b-ya)/(yb-ya)+.012
   vs.extend([(x0,a,az),(x1,a,az),(x1,b,bz),(x0,b,bz)]);fs.append((k,k+1,k+2,k+3));colors.append(random.randrange(4))
tiles=mesh('Laid pedestrian pavers',vs,fs,pave[0],street)
for m in pave[1:]:tiles.data.materials.append(m)
for p,idx in zip(tiles.data.polygons,colors):p.material_index=idx
# Gathering space at the street's head, opening toward the existing square reservation.
box('Square opening / gathering apron',(0,32.9,3.91),(16,6.2,.18),pave[1],street,edge=.05)
for x in range(-7,8):beam('Square paving joint',(x,30,4.008),(x,36,4.008),.012,.008,stone,street)
for y in [30.7,31.8,32.9,34,35.1]:beam('Square cross joint',(-7.8,y,4.008),(7.8,y,4.008),.012,.008,stone,street)
# Broad stair landings and retaining sides read as one terraced public space.
for side in [-1,1]:
 for a,b,z in [(5.9,14.4,1.442857142857),(18,27.5,3.36)]:
  box('Continuous frontage terrace',(side*5.8,(a+b)/2,z-.12),(1.4,b-a,.24),pave[1],street)
  # Foundation infill continues to the measured ground instead of floating podiums.
  for y in [a+.6,b-.6]:
   lo=grade(side*6.0,y)-.08
   if lo<z-.1:box('Terrace stone return',(side*6.2,y,(lo+z-.1)/2),(.20,1.2,z-.1-lo),stone,land,edge=.025)
# A single shallow bookshop threshold step, aligned to its door; the other three are flush.
box('Lembaran threshold landing',(4.90,10.95,1.54),(1.35,2.0,.19),pave[0],street,edge=.025)

def planter(name,x,y,z,w,d,h=.52):
 o=box(name,(x,y,z+h/2),(w,d,h),stone,land,edge=.06)
 box(name+' soil',(x,y,z+h-.06),(w-.12,d-.12,.045),soil,land,edge=.01)
 return z+h-.05
def bench(x,y,z,angle=0):
 c=bpy.data.collections.new('Bench assembly');props.children.link(c);r=bpy.data.objects.new('Bench carrier',None);c.objects.link(r)
 for yy in [-.18,0,.18]:box('Bench timber seat',(0,yy,.48),(2.1,.15,.065),timber,c,r)
 for zz in [.76,.96]:box('Bench timber back',(0,.26,zz),(2.1,.055,.14),wood,c,r)
 for xx in [-.83,.83]:beam('Bench frame',(xx,-.18,.04),(xx,-.18,.48),.065,.065,bronze,c,r);beam('Bench back frame',(xx,.26,.04),(xx,.26,1.02),.065,.065,bronze,c,r)
 r.location=(x,y,z);r.rotation_euler.z=angle
bench(-6.8,31.2,4,math.pi/2);bench(6.8,33.4,4,-math.pi/2)
def chair(x,y,z,angle):
 c=bpy.data.collections.new('Cafe chair assembly');props.children.link(c);r=bpy.data.objects.new('Cafe chair carrier',None);c.objects.link(r)
 for xx in [-.18,.18]:
  for yy in [-.18,.18]:beam('Chair leg',(xx,yy,.03),(xx,yy,.43),.03,.03,bronze,c,r)
 for yy in [-.14,0,.14]:box('Chair slat',(0,yy,.45),(.44,.12,.045),timber,c,r,edge=.01)
 for xx in [-.18,.18]:beam('Chair back upright',(xx,.18,.40),(xx,.18,.91),.03,.03,bronze,c,r)
 for zz in [.70,.85]:box('Chair back slat',(0,.18,zz),(.43,.045,.09),wood,c,r,edge=.01)
 r.location=(x,y,z);r.rotation_euler.z=angle
def table(x,y,z):
 # Circular top with actual radial mesh, shared frame material.
 vs=[(x+.43*math.cos(i*2*math.pi/24),y+.43*math.sin(i*2*math.pi/24),z+.77) for i in range(24)]
 o=mesh('Outdoor cafe table top',vs,[tuple(range(24))],timber,props);mod=o.modifiers.new('Table thickness','SOLIDIFY');mod.thickness=.05
 beam('Cafe table stem',(x,y,z+.05),(x,y,z+.73),.055,.055,bronze,props)
 for dx,dy in [(.3,0),(-.3,0),(0,.3),(0,-.3)]:beam('Cafe table foot',(x,y,z+.05),(x+dx,y+dy,z+.05),.035,.035,bronze,props)
for y in [7.6,12.65]:
 table(-3.95,y,1.442857142857);chair(-3.95,y-.67,1.442857142857,math.pi);chair(-3.95,y+.67,1.442857142857,0)
table(6.35,30.7,4);chair(5.7,30.7,4,math.pi/2);chair(7.0,30.7,4,-math.pi/2)

# Selective tropical planting: existing licensed canopy tree and fern, original palm accents.
before=set(s.objects);bpy.ops.import_scene.gltf(filepath=BASE+'assets/game/scenery/canopy-tree.glb')
tree=next(o for o in s.objects if o not in before and o.type=='MESH');tree.name='Quaternius shared canopy tree'
for c in list(tree.users_collection):c.objects.unlink(tree)
land.objects.link(tree);tree.data=tree.data.copy();tree.data.transform(tree.matrix_world);tree.matrix_world=Matrix.Identity(4)
lo=Vector(tuple(min(v.co[i] for v in tree.data.vertices) for i in range(3)));hi=Vector(tuple(max(v.co[i] for v in tree.data.vertices) for i in range(3)));center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));scale=4.8/(hi.z-lo.z)
for v in tree.data.vertices:v.co=(v.co-center)*scale
tree.data.update();tree['source']='Quaternius Stylized Nature MegaKit Standard / canopy-tree.glb';tree['license']='CC0-1.0'
for i,(x,y,sc) in enumerate([(-14.2,10.2,1.1),(14.4,16.2,1.0),(-14.6,25.4,1.10),(13.5,28.0,.95),(-5.6,33.1,.82)]):
 o=tree if i==0 else tree.copy()
 if i:land.objects.link(o)
 z=grade(x,y)
 if i==4:z=planter('Square focal tree bed',x,y,4,2.4,2.4,.54)
 o.location=(x,y,z);o.scale=(sc,sc,sc);o.rotation_mode='XYZ';o.rotation_euler.z=i*1.3

fern_source=next(o for o in bpy.data.scenes['S2B Editable Modules'].objects if o.get('source','').startswith('Quaternius'))
fern_lo=min(v.co.z for v in fern_source.data.vertices);fern_hi=max(v.co.z for v in fern_source.data.vertices)
patches=[(-5.55,5.5,1.44),(-5.55,14.0,1.44),(5.55,8.0,1.44),(5.55,14.0,1.44),(-5.55,18.5,3.36),(-5.55,26.8,3.36),(5.55,18.5,3.36),(5.55,26.8,3.36),(-7.0,35,4),(7,35,4)]
for i,(x,y,z) in enumerate(patches):
 top=planter('Street fern trough',x,y,z,1.0,1.3,.48)
 for j,dy in enumerate([-.32,.24]):
  o=fern_source.copy();o.parent=None;land.objects.link(o);o.name='Shared source fern / street planter';o.rotation_mode='XYZ';o.rotation_euler=(0,0,(i+j)*1.4);sc=(.5+j*.14)/(fern_hi-fern_lo);o.scale=(sc,sc,sc);o.location=(x,y+dy,top-fern_lo*sc-.06)

def palm(x,y,height):
 z=grade(x,y);rings=8;ns=8;vs=[];fs=[]
 for j in range(rings):
  t=j/(rings-1);cx=x+.32*t*t;cy=y+.12*math.sin(t*math.pi);rr=.16*(1-.45*t)
  for i in range(ns):a=i*math.tau/ns;vs.append((cx+rr*math.cos(a),cy+rr*math.sin(a),z+height*t))
 for j in range(rings-1):
  for i in range(ns):a=j*ns+i;b=j*ns+(i+1)%ns;fs.append((a,b,b+ns,a+ns))
 mesh('Original stylized palm trunk',vs,fs,bark,land)
 crown=Vector((x+.32,y,z+height))
 for k in range(10):
  a=k*math.tau/10;direction=Vector((math.cos(a),math.sin(a),0));side=Vector((-math.sin(a),math.cos(a),0));vs=[];fs=[]
  for j in range(9):
   t=j/8;center=crown+direction*(2.0*t)+Vector((0,0,.55*math.sin(t*math.pi)-.75*t*t));width=.34*math.sin(t*math.pi)**.7
   for sign in [-1,0,1]:vs.append(tuple(center+side*sign*width+Vector((0,0,-.07*abs(sign)))))
  for j in range(8):
   a0=j*3;fs.extend([(a0,a0+3,a0+4,a0+1),(a0+1,a0+4,a0+5,a0+2)])
  mesh('Original layered palm frond',vs,fs,leaves[k%3],land)
for x,y,h in [(-13.5,4.2,5.9),(13.9,7.3,6.2),(-12.5,29,5.6),(11.7,34.8,5.7)]:palm(x,y,h)
# Purposeful low greenery on retaining edges, not scattered across the walking line.
for x,y in [(-14.3,7),(-14.8,18),(-13.7,28),(13.8,19),(14.8,30),(-7.3,32),(7.1,34.5)]:
 z=grade(x,y)
 for k in range(7):
  a=k*math.tau/7;tip=(x+.65*math.cos(a),y+.65*math.sin(a),z+.35+.12*(k%2));mid=(x+.28*math.cos(a),y+.28*math.sin(a),z+.72)
  mesh('Broadleaf garden clump',[(x,y,z),mid,tip,(x+.24*math.cos(a+.5),y+.24*math.sin(a+.5),z+.45)],[(0,1,2,3)],leaves[k%3],land)
 for dx in [-.12,.13]:
  beam('Ginger flower stem',(x+dx,y,z+.2),(x+dx,y,z+.72),.022,.022,leaves[0],land)
  box('Ginger flower head',(x+dx,y,z+.78),(.11,.14,.23),flower,land,edge=.045)

# Restrained lights and real wayfinding point to the unbuilt destinations.
for side,y in [(-1,5.2),(1,15.0),(-1,27.2),(1,34.5)]:
 x=side*6.5;z=main_h(y);beam('Pedestrian lamp post',(x,y,z),(x,y,z+2.65),.065,.065,bronze,props)
 box('Lamp rain cap',(x,y,z+2.68),(.38,.32,.08),wood,props)
 box('Lamp diffuser',(x,y,z+2.49),(.18,.18,.28),cream,props)
 if y==27.2:
  box('Town square wayfinding',(x,y,z+2.20),(1.45,.10,.36),sage,props)
  text('Wayfinding square','ALUN-ALUN  >',(x,y-.065,z+2.12),.15,cream,props)
  box('Atlas wayfinding',(x,y,z+1.79),(1.45,.10,.30),sage,props)
  text('Wayfinding guild','BALAI ATLAS  >',(x,y-.065,z+1.72),.14,cream,props)

# Natural daylight and four reproducible review cameras, plus a real top-down plan.
world=bpy.data.worlds.new('S2C tropical daytime');world.use_nodes=True;s.world=world
bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Color'].default_value=(.58,.76,.93,1);bg.inputs['Strength'].default_value=.55
bpy.ops.object.light_add(type='SUN',location=(-5,-8,20));o=bpy.context.object;o.name='S2C warm daylight';o.data.energy=2.3;o.data.angle=.10;o.data.color=(1,.87,.70);o.rotation_euler=(math.radians(28),math.radians(-20),math.radians(-28))
for c in list(o.users_collection):c.objects.unlink(o)
cams.objects.link(o)
bpy.ops.object.light_add(type='AREA',location=(0,10,20));o=bpy.context.object;o.name='S2C broad sky fill';o.data.energy=3500;o.data.size=22
for c in list(o.users_collection):c.objects.unlink(o)
cams.objects.link(o)
def camera(name,pos,target,lens,ortho=0):
 bpy.ops.object.camera_add(location=pos);o=bpy.context.object;o.name='S2C '+name;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens;o.data.clip_end=250
 if ortho:o.data.type='ORTHO';o.data.ortho_scale=ortho
 for c in list(o.users_collection):c.objects.unlink(o)
 cams.objects.link(o)
 return o
camera('Arrival',(0,-3,1.65),(0,18,5.5),26)
camera('Opposite',(1,34,5.65),(-.3,12,4.4),28)
camera('Elevated',(33,-25,33),(0,18,4),39)
camera('Detail',(2.0,12.5,main_h(12.5)+1.65),(-5.1,14.0,4.7),30)
camera('Plan',(0,18,58),(0,18,0),45,48)
s.camera=bpy.data.objects['S2C Elevated'];s.render.engine='CYCLES';s.cycles.samples=40;s.cycles.use_denoising=True;s.render.resolution_percentage=100;s.render.resolution_x=1600;s.render.resolution_y=1200;s.render.image_settings.file_format='PNG'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=OUT+'market-street.blend')
print('PUBLIC_REALM_READY',len(s.objects))
