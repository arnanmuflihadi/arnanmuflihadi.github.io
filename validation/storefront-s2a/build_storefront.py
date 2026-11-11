"""Execute through live Blender MCP. One authored building, isolated from the game."""
import bpy, math, random
from mathutils import Vector

BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/storefront-s2a/'
s=bpy.data.scenes['S2-A Tropical Storefront'];bpy.context.window.scene=s
s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
groups={}
for name in ['Buildings / Shell','Buildings / Joinery','Buildings / Roof','Buildings / Terrace','Buildings / Interior','Streets','Landscape','Props','Collision References','Cameras']:
 c=bpy.data.collections.new('S2A / '+name);s.collection.children.link(c);groups[name]=c

def put(o,group):
 for c in list(o.users_collection):c.objects.unlink(o)
 groups[group].objects.link(o)
 return o

def material(name,color,rough=.7,metal=0):
 m=bpy.data.materials.new('S2A / '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m

plaster=material('warm lime plaster',(.76,.65,.48))
plaster_shade=material('recessed sage plaster',(.25,.35,.27))
stone=material('sandstone base',(.39,.36,.29))
wood=material('oiled tropical timber',(.20,.085,.035),.53)
wood_light=material('cut timber edges',(.36,.18,.07),.58)
dark=material('patinated bronze frames',(.045,.085,.075),.4,.55)
brass=material('aged brass',(.52,.30,.09),.34,.7)
glass=material('soft blue green glass',(.11,.29,.31),.19,.12)
p=next(n for n in glass.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
p.inputs['Transmission Weight'].default_value=.60;p.inputs['IOR'].default_value=1.45
roofmats=[material('terracotta '+str(i),(.38+i*.015,.105+i*.006,.046+i*.003),.83) for i in range(5)]
cream=material('warm sign lettering',(.91,.79,.54))
paving=material('limestone paving',(.54,.50,.40),.88)
soil=material('planter soil',(.07,.045,.022),.95)
leaf=material('tropical leaf',(.12,.29,.075),.8)
leaflight=material('leaf light',(.23,.40,.10),.82)
fabric=material('interior soft ivory',(.77,.72,.59),.85)

def mesh(name,verts,faces,mat,group='Buildings / Shell'):
 data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
 o=bpy.data.objects.new('S2A / '+name,data);groups[group].objects.link(o)
 if mat:data.materials.append(mat)
 o['authorship']='Original project geometry';return o

def bevel(o,width=.025,segments=2):
 m=o.modifiers.new('Craft edge bevel','BEVEL');m.width=width;m.segments=segments
 return o

def box(name,loc,dim,mat,group='Buildings / Joinery',edge=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name='S2A / '+name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);put(o,group)
 if edge:bevel(o,edge)
 return o

def beam(name,a,b,width,depth,mat=wood,group='Buildings / Joinery'):
 v=Vector(b)-Vector(a);o=box(name,(Vector(a)+Vector(b))/2,(width,depth,v.length),mat,group)
 o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return o

def cylinder(name,loc,radius,depth,mat,group='Buildings / Joinery',vertices=16):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
 o=bpy.context.object;o.name='S2A / '+name;o.data.materials.append(mat);put(o,group);bevel(o,.01);return o

def wall(name,lo,hi,zlo,zhi,y,holes,rot=0):
 # A genuine wall mesh with openings, not a stack of opaque building boxes.
 xs=sorted(set([lo,hi]+[v for h in holes for v in h[:2]]));zs=sorted(set([zlo,zhi]+[v for h in holes for v in h[2:]]))
 verts=[];faces=[]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(zs,zs[1:]):
   if any(h[0]<(a+b)/2<h[1] and h[2]<(c+d)/2<h[3] for h in holes):continue
   k=len(verts);verts += [(a,y,c),(b,y,c),(b,y,d),(a,y,d)];faces.append((k,k+1,k+2,k+3))
 o=mesh(name,verts,faces,plaster);o.rotation_euler.z=rot
 so=o.modifiers.new('Real wall thickness 220mm','SOLIDIFY');so.thickness=.22;so.offset=0
 bevel(o,.018);return o

# Floors, inhabited shell and continuous step-free frontage.
box('foundation',(0,.7,.08),(7.4,8.8,.16),stone,'Buildings / Shell',.06)
box('ground floor',(0,.7,.19),(7.15,8.5,.10),paving,'Buildings / Shell')
box('upper floor',(0,.40,3.36),(7.3,9.5,.24),stone,'Buildings / Shell',.035)
box('upper interior floor',(0,.8,3.50),(6.9,8.3,.06),wood_light,'Buildings / Interior')
box('roof ceiling',(0,.75,6.45),(7.15,8.5,.12),wood,'Buildings / Shell')
front_openings=[(-3.23,-.67,.28,2.94),(-.48,1.08,.24,2.94),(1.27,3.23,.28,2.94)]
wall('shop facade',-3.6,3.6,.20,3.23,-3.55,front_openings)
wall('terrace facade',-3.6,3.6,3.5,6.45,-2.85,[(-3.0,.95,3.58,6.12),(1.34,3.08,4.1,6.05)])
# Side coordinates u run from -5 to 3.55 after rotating (u,y)->(-y,u).
for sign in [-1,1]:
 rot=sign*math.pi/2
 side=wall(('east' if sign==-1 else 'west')+' shop wall',-5,3.55,.20,3.23,3.6,[(-2.8,-.8,1.0,2.7),(.4,2.55,.7,2.7)],rot)
 side=wall(('east' if sign==-1 else 'west')+' upper wall',-5,2.85,3.5,6.45,3.6,[(-2.0,-.7,4.1,5.85),(.5,1.8,4.1,5.85)],rot)
wall('rear ground wall',-3.6,3.6,.20,3.23,5.0,[(-.6,.6,.24,2.65),(-2.8,-1.5,1.2,2.7),(1.5,2.8,1.2,2.7)])
wall('rear upper wall',-3.6,3.6,3.5,6.45,5.0,[(-2.5,-1.0,4.1,5.9),(1.0,2.5,4.1,5.9)])

def glazing(name,x0,x1,z0,z1,y,div=2):
 box(name+' glass',((x0+x1)/2,y,(z0+z1)/2),(x1-x0,.035,z1-z0),glass,edge=.003)
 for x in [x0,x1]:box(name+' jamb',(x,y-.025,(z0+z1)/2),(.065,.12,z1-z0+.10),dark)
 for z in [z0,z1]:box(name+' rail',((x0+x1)/2,y-.025,z),(x1-x0+.07,.12,.07),dark)
 for i in range(1,div):box(name+' mullion',(x0+(x1-x0)*i/div,y-.05,(z0+z1)/2),(.045,.10,z1-z0),dark)

glazing('west display',-3.23,-.67,.30,2.91,-3.52,3)
glazing('entrance',-.48,1.08,.25,2.91,-3.30,2)
glazing('east display',1.27,3.23,.30,2.91,-3.52,2)
for x in [.14,.46]:beam('door pull',(x,-3.41,1.08),(x,-3.41,1.51),.025,.035,brass)
glazing('balcony sliding glazing',-3.0,.95,3.60,6.09,-2.82,4)
glazing('upper east glazing',1.34,3.08,4.12,6.02,-2.80,2)

# Shaded shop soffit, slender structural posts and coherent balcony framing.
for x in [-3.46,3.46]:
 box('veranda post',(x,-4.08,1.76),(.18,.18,3.12),wood)
 box('column stone shoe',(x,-4.08,.37),(.25,.25,.32),stone)
 beam('front knee brace',(x,-4.08,2.62),(x+(.55 if x<0 else -.55),-4.08,3.20),.10,.12)
box('balcony fascia',(0,-4.33,3.37),(7.3,.16,.30),wood)
for i in range(13):box('veranda soffit slat',(-3.3+i*.55,-3.78,3.20),(.10,1.28,.09),wood_light)
for x in [-3.46,3.46]:
 box('upper roof post',(x,-4.06,5.02),(.16,.16,3.0),wood)
 beam('upper cantilever brace',(x,-4.06,5.80),(x+(.6 if x<0 else -.6),-4.06,6.45),.09,.11)
box('front roof header',(0,-4.06,6.40),(7.15,.18,.20),wood)
for y in [-4.02,-3.4]:box('balcony deck edge',(0,y,3.54),(7.0,.04,.055),wood_light,'Buildings / Terrace')
# Board decking follows the veranda, with a shared array modifier.
deck=box('balcony decking board',(-3.4,-3.52,3.525),(.21,1.45,.04),wood_light,'Buildings / Terrace',.008)
ar=deck.modifiers.new('Reusable deck board array','ARRAY');ar.count=31;ar.relative_offset_displace=(1.06,0,0)
for x in [-3.36,-.9,1.3,3.36]:box('balcony rail upright',(x,-4.18,4.07),(.055,.055,1.05),dark,'Buildings / Terrace')
box('balcony timber handrail',(0,-4.18,4.60),(6.85,.10,.09),wood_light,'Buildings / Terrace')
for z in [3.79,4.03,4.27]:beam('balcony thin rail',(-3.36,-4.18,z),(3.36,-4.18,z),.022,.022,dark,'Buildings / Terrace')
for x in [-3.37,3.37]:
 beam('return handrail',(x,-4.18,4.60),(x,-2.87,4.60),.075,.08,wood_light,'Buildings / Terrace')
 for z in [3.79,4.03,4.27]:beam('return rail',(x,-4.18,z),(x,-2.87,z),.022,.022,dark,'Buildings / Terrace')
# Functional operable screen: frame, repeated angled blades and brass pivot detail.
for x in [1.26,3.18]:box('screen edge',(x,-3.14,5.08),(.065,.13,2.05),wood_light)
for z in [4.08,6.08]:box('screen top bottom',(2.22,-3.14,z),(1.98,.13,.07),wood_light)
slat=box('angled sun screen blade',(1.38,-3.14,5.08),(.115,.08,1.95),wood)
slat.rotation_euler.z=math.radians(27)
ar=slat.modifiers.new('Sun screen blade rhythm','ARRAY');ar.count=13;ar.use_relative_offset=False;ar.use_constant_offset=True;ar.constant_offset_displace=(.132*math.cos(math.radians(27)),-.132*math.sin(math.radians(27)),0)

# Reuse actual Kenney window geometry for small upper side and rear windows.
template=bpy.data.objects['window-brown-detailed'];template.name='S2A / Kenney window east rear'
put(template,'Buildings / Joinery')
for i,(x,y,z,angle) in enumerate([(3.72,.85,4.98,-math.pi/2),(3.72,-1.15,4.98,-math.pi/2),(-3.72,-.85,4.98,math.pi/2),(-3.72,1.15,4.98,math.pi/2),(1.75,5.12,5,math.pi),(-1.75,5.12,5,math.pi)]):
 o=template if i==0 else template.copy()
 if i:groups['Buildings / Joinery'].objects.link(o)
 o.scale=(4,4,4);o.rotation_euler.z=angle
 # Imported bounds, centre at the requested opening centre.
 bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for v in o.bound_box];mid=(Vector(tuple(min(p[k] for p in pts) for k in range(3)))+Vector(tuple(max(p[k] for p in pts) for k in range(3))))/2
 o.location+=Vector((x,y,z))-mid;o['source']='Kenney Modular Buildings 2.1 / window-brown-detailed.glb';o['license']='CC0-1.0'

# Side shop windows use the same bronze/glass palette and actual wall openings.
for side in [-1,1]:
 for yc,wid in [(1.8,2),(-1.475,2.15)]:
  box('side shop glass',(side*3.61,yc,1.85),(.035,wid,1.65),glass)
  for yy in [yc-wid/2,yc,yc+wid/2]:box('side shop mullion',(side*3.65,yy,1.85),(.10,.055,1.72),dark)
  for zz in [1.02,2.68]:box('side shop transom',(side*3.65,yc,zz),(.10,wid,.06),dark)
box('rear service door',(0,5.01,1.44),(1.16,.06,2.4),wood)
for x in [-2.15,2.15]:box('rear lower glazing',(x,5.01,1.95),(1.25,.035,1.45),glass)

# A complete low-cost interior keeps the glazing from reading as an opaque panel.
box('rear interior sage wall',(0,4.86,1.75),(6.9,.05,2.9),plaster_shade,'Buildings / Interior')
box('cafe counter',(-1.6,1.45,.79),(2.8,.72,1.10),wood,'Buildings / Interior',.04)
box('counter stone top',(-1.6,1.45,1.38),(2.95,.85,.09),stone,'Buildings / Interior',.04)
for z in [.9,1.6,2.3]:box('rear display shelf',(-1.5,4.55,z),(3.5,.38,.065),wood_light,'Buildings / Interior')
for j in range(9):
 o=cylinder('coffee jar',(-2.9+j*.35,4.53,1.77),.09,.27,roofmats[j%5],'Buildings / Interior')
for x,y in [(-2.3,-1.4),(2.3,.6)]:
 cylinder('cafe table foot',(x,y,.58),.055,.65,dark,'Buildings / Interior')
 cylinder('cafe table top',(x,y,.93),.52,.065,wood_light,'Buildings / Interior',32)
for x in [-2.6,-1.8,1.9,2.7]:box('interior stool',(x,-1.35,.55),(.32,.32,.60),wood_light,'Buildings / Interior')

# Main roof: authored four hip surfaces with lifted corners and separate laid tiles.
roofpatches=[
 [(-4.3,-4.65,6.66),(4.3,-4.65,6.66),(0,-.65,8.02),(0,-.65,8.02)],
 [(4.3,-4.65,6.66),(4.3,5.65,6.66),(0,2.65,8.02),(0,-.65,8.02)],
 [(4.3,5.65,6.66),(-4.3,5.65,6.66),(0,2.65,8.02),(0,2.65,8.02)],
 [(-4.3,5.65,6.66),(-4.3,-4.65,6.66),(0,-.65,8.02),(0,2.65,8.02)]]
def point(p,u,v):
 a,b,c,d=map(Vector,p);q=(a.lerp(b,u)).lerp(d.lerp(c,u),v)
 q.z += .20*(abs(u-.5)*2)**4*(1-v)**4 - .12*math.sin(v*math.pi)
 return q
random.seed(62)
verts=[];faces=[];mis=[]
for side,p in enumerate(roofpatches):
 # Continuous structural roof/soffit under the tiling.
 vs=[];fs=[];nu=16;nv=12
 for j in range(nv+1):
  for i in range(nu+1):vs.append(tuple(point(p,i/nu,j/nv)))
 for j in range(nv):
  for i in range(nu):k=j*(nu+1)+i;fs.append((k,k+1,k+nu+2,k+nu+1))
 o=mesh('hip roof structural surface '+str(side),vs,fs,wood,'Buildings / Roof')
 so=o.modifiers.new('Roof build up 90mm','SOLIDIFY');so.thickness=.09
 # Taper tile counts toward the triangular hips, retaining quad strip surfaces.
 for j in range(12):
  cols=max(2,round((20 if side%2 else 18)*(1-j/12 if side%2==0 else 1-j/24)))
  for i in range(cols):
   k=len(verts);v0=j/12;v1=min(1,(j+1.06)/12)
   for jj in range(3):
    for ii in range(3):
     u=(i+ii/2)/cols;v=v0+(v1-v0)*jj/2;q=point(p,u,v)
     q.z+=.035+.022*math.sin(ii/2*math.pi);verts.append(tuple(q))
   color=random.randrange(5)
   for jj in range(2):
    for ii in range(2):n=k+jj*3+ii;faces.append((n,n+1,n+4,n+3));mis.append(color)
o=mesh('laid terracotta tile courses',verts,faces,roofmats[0],'Buildings / Roof')
for m in roofmats[1:]:o.data.materials.append(m)
for poly,mi in zip(o.data.polygons,mis):poly.material_index=mi
# Eave edges, diagonal hips and a ventilated ridge cap.
for a,b in [((-4.3,-4.65,6.86),(4.3,-4.65,6.86)),((4.3,-4.65,6.86),(4.3,5.65,6.86)),((4.3,5.65,6.86),(-4.3,5.65,6.86)),((-4.3,5.65,6.86),(-4.3,-4.65,6.86))]:beam('timber eave fascia',a,b,.10,.14,wood,'Buildings / Roof')
for a,b in [((-4.3,-4.65,6.85),(0,-.65,8.08)),((4.3,-4.65,6.85),(0,-.65,8.08)),((-4.3,5.65,6.85),(0,2.65,8.08)),((4.3,5.65,6.85),(0,2.65,8.08))]:beam('hip ridge cover',a,b,.12,.12,roofmats[2],'Buildings / Roof')
for x in [-.23,.23]:
 for z in [8.07,8.18,8.29]:box('ridge ventilation louver',(x,1,z),(.07,3.65,.045),wood,'Buildings / Roof')
# Small expressive ridge canopy, lofted rather than a box.
vs=[(-.48,-1.03,8.37),(0,-1.08,8.52),(.48,-1.03,8.37),(-.48,3.05,8.37),(0,3.10,8.52),(.48,3.05,8.37)]
o=mesh('raised ridge rain cap',vs,[(0,3,4,1),(1,4,5,2)],roofmats[2],'Buildings / Roof');so=o.modifiers.new('Cap thickness','SOLIDIFY');so.thickness=.055;bevel(o,.025)
beam('subtle brass ridge crest',(0,-1.07,8.54),(0,3.09,8.54),.035,.035,brass,'Buildings / Roof')

# Integrated planter shells: open trough meshes with soil and real vegetation.
def planter(name,x,y,z,w,d,h):
 vs=[(x+sx*w/2,y+sy*d/2,z+zz*h) for zz in [0,1] for sy in [-1,1] for sx in [-1,1]]
 o=mesh(name,vs,[(0,1,3,2),(0,4,5,1),(1,5,7,3),(3,7,6,2),(2,6,4,0)],stone,'Landscape')
 so=o.modifiers.new('Planter thickness','SOLIDIFY');so.thickness=.06;bevel(o,.025)
 box(name+' soil',(x,y,z+h-.08),(w-.10,d-.10,.05),soil,'Landscape')
 return z+h
plantpositions=[]
for x,y,z,w,d,h in [(-2.1,-4.10,3.55,1.9,.42,.48),(2.65,-4.10,3.55,.92,.42,.48),(-2.7,-4.65,.04,1.45,.58,.48),(3.0,-4.65,.04,.85,.58,.48)]:
 top=planter('integrated stone trough',x,y,z,w,d,h)
 for dx in [-w*.27,0,w*.27]:plantpositions.append((x+dx,y,top))
before=set(s.objects)
bpy.ops.import_scene.gltf(filepath=BASE+'assets/game/scenery/fern.glb')
fern=next(o for o in s.objects if o not in before and o.type=='MESH');put(fern,'Landscape')
for i,(x,y,z) in enumerate(plantpositions):
 o=fern if i==0 else fern.copy()
 if i:groups['Landscape'].objects.link(o)
 o.scale=(.46,.46,.46);o.rotation_euler.z=i*1.9
 bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for v in o.bound_box]
 mid=Vector(((min(p.x for p in pts)+max(p.x for p in pts))/2,(min(p.y for p in pts)+max(p.y for p in pts))/2,min(p.z for p in pts)))
 o.location+=Vector((x,y,z-.08))-mid;o['source']='Quaternius Stylized Nature MegaKit Standard / Fern_1';o['license']='CC0-1.0'

# Attached shop identity is physical geometry, not a UI overlay.
box('sign backing',(-1.88,-3.72,3.02),(2.75,.10,.40),plaster_shade)
cu=bpy.data.curves.new('shop lettering','FONT');cu.body='KOPI  AWAN';cu.align_x='CENTER';cu.size=.25;cu.extrude=.004
ob=bpy.data.objects.new('S2A / shop sign',cu);groups['Buildings / Joinery'].objects.link(ob);ob.location=(-1.88,-3.78,2.93);ob.rotation_euler.x=math.pi/2;cu.materials.append(cream)
for x in [-3.12,3.12]:
 beam('lamp bracket',(x,-3.62,2.67),(x,-3.94,2.67),.035,.035,dark)
 cylinder('veranda light',(x,-3.94,2.52),.10,.23,brass)
 cylinder('lamp glass',(x,-3.94,2.51),.074,.16,cream)

# Neutral surrounding ground, a thin paved apron and a credible shallow ramp.
box('ground plane',(0,.2,-.12),(28,28,.20),paving,'Streets',.02)
box('shop apron',(0,-4.0,.055),(7.45,2.1,.11),paving,'Streets',.05)
mesh('entry threshold ramp',[(-.65,-5.2,0),(1.3,-5.2,0),(1.3,-4.65,.11),(-.65,-4.65,.11)],[(0,1,2,3)],paving,'Streets')
for x in range(-6,7):box('paving joint',(x,-6.45,-.012),(.012,3.2,.008),stone,'Streets',0)
for y in [-5,-6,-7,-8]:box('paving cross joint',(0,y,-.012),(13,.012,.008),stone,'Streets',0)

# Human scale mannequin is a neutral inspection reference, not an NPC.
human=material('scale reference indigo',(.07,.13,.17))
hx,hy=-4.65,-4.9
for dx in [-.11,.11]:beam('scale reference leg',(hx+dx,hy,.09),(hx+dx,hy,.87),.12,.12,human,'Props')
o=box('scale reference torso',(hx,hy,1.13),(.36,.21,.58),human,'Props',.08)
for dx in [-.24,.24]:beam('scale reference arm',(hx+dx,hy,1.36),(hx+dx*1.2,hy, .88),.085,.085,human,'Props')
bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.125,location=(hx,hy,1.625));o=bpy.context.object;o.name='S2A / reference head / 1.75 m';o.data.materials.append(human);put(o,'Props')

world=bpy.data.worlds.new('S2A soft daylight');world.use_nodes=True;s.world=world
bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND');bg.inputs['Color'].default_value=(.62,.76,.92,1);bg.inputs['Strength'].default_value=.48
bpy.ops.object.light_add(type='SUN',location=(-5,-8,12));o=bpy.context.object;o.name='S2A / warm daylight';o.data.energy=2.3;o.data.angle=.10;o.data.color=(1,.86,.68);o.rotation_euler=(math.radians(26),math.radians(-24),math.radians(-28));put(o,'Cameras')
bpy.ops.object.light_add(type='AREA',location=(0,-8,7));o=bpy.context.object;o.name='S2A / sky bounce';o.data.energy=650;o.data.shape='DISK';o.data.size=9;o.rotation_euler=(Vector((0,0,3))-o.location).to_track_quat('-Z','Y').to_euler();put(o,'Cameras')
def camera(name,pos,target,lens):
 bpy.ops.object.camera_add(location=pos);o=bpy.context.object;o.name='S2A / '+name;o.data.lens=lens;o.data.clip_end=200;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();put(o,'Cameras');return o
camera('Street 1.65m',(10,-19,1.65),(0,-.5,3.65),37)
camera('Elevated three quarter',(13,-17,11),(0,.3,3.8),45)
camera('Facade roof detail',(6.8,-10,7.8),(0,-2.9,5.5),46)
s.camera=bpy.data.objects['S2A / Elevated three quarter']
s.render.engine='CYCLES';s.cycles.samples=40;s.cycles.use_denoising=True
s.render.resolution_x=1500;s.render.resolution_y=1500;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT+'kopi-awan-prototype.blend')
print('S2A_BUILD_READY',len(s.objects),'objects')
