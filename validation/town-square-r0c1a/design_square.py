import bpy,math,json,bmesh
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/town-square-r0c1a/'
assert bpy.data.filepath==OUT+'town-square-design.blend'
source=bpy.data.scenes['S2E Interface Design'];bpy.context.window.scene=source;bpy.context.view_layer.update()
scene=bpy.data.scenes.new('R0-C1A / Telaga Awan');scene.world=source.world.copy();scene.unit_settings.system='METRIC';scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1800;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.view_settings.view_transform=source.view_settings.view_transform;scene.view_settings.look=source.view_settings.look
if hasattr(scene.eevee,'taa_render_samples'):scene.eevee.taa_render_samples=64
C={}
for name in ['Context - approved market','Context - exact terrain','Context - existing island plants','Paving','Supports','Fountain','Timber shade','Planting','Furniture','Proposed routes','Scale reference','Cameras','Plan annotations']:
 c=bpy.data.collections.new('C1 / '+name);scene.collection.children.link(c);C[name]=c
context_record=[]
for name in ['Buildings','Streets','Landscape','Props','Common Interface','H Hybrid']:
 for original in bpy.data.collections['S2E / '+name].objects:
  o=original.copy();o.parent=None;o.matrix_world=original.matrix_world.copy();C['Context - approved market'].objects.link(o);o['context_only']=True;o['approved_source']=original.name
  context_record.append((o.name,list(v for row in original.matrix_world for v in row)))
for original in source.objects:
 if original.type=='LIGHT':
  o=original.copy();o.data=original.data.copy();C['Cameras'].objects.link(o)
terrain_original=next(o for o in source.objects if o.name.startswith('Exact R0A3'))
terrain=terrain_original.copy();terrain.name='C1 exact unchanged terrain reference';C['Context - exact terrain'].objects.link(terrain)
bvh=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices) for p in terrain.data.polygons])
def G(x,z):
 hit=bvh.ray_cast(Vector((x-36,44-z,140)),Vector((0,0,-1)))[0]
 return hit.z+18.6

def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def material(name,color,rough=.8,metal=0):
 m=bpy.data.materials.new('C1 / '+name);m.use_nodes=True;m.diffuse_color=(*color,1);p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
stone=material('warm volcanic stone',(.28,.30,.255),.95);sand=material('warm limestone',(.53,.48,.36),.9);clay=material('terracotta',(.40,.155,.065),.84);wood=material('oiled timber',(.24,.112,.046),.72);bronze=material('weathered bronze',(.32,.23,.095),.32,.65);metal=material('deep green metal',(.045,.09,.075),.7,.3);soil=material('planting soil',(.12,.14,.075),1);leaf=material('tropical leaf',(.11,.27,.13),.9);water=material('jade water',(.075,.35,.31),.18,.16);foam=material('soft water highlights',(.57,.74,.65),.3);cream=material('sign lettering',(.87,.78,.55),.7)
def mesh(name,vs,fs,mat,col):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);C[col].objects.link(o)
 if mat:me.materials.append(mat)
 return o
def box(name,point,size,mat,col='Furniture',bevel=.02):
 x,y,z=P(*point);a,b,c=[v/2 for v in size];vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in[-1,1] for sy in[-1,1] for sx in[-1,1]];o=mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],mat,col)
 if bevel:m=o.modifiers.new('Craft arris','BEVEL');m.width=bevel;m.segments=2
 return o
def beam(name,a,b,w,d,mat,col='Furniture'):
 a,b=P(*a),P(*b);up=(b-a).normalized();side=up.cross(Vector((0,1,0)))
 if side.length<.01:side=up.cross(Vector((1,0,0)))
 side.normalize();other=up.cross(side).normalized();vs=[tuple(p+side*i*w/2+other*j*d/2) for p in[a,b] for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]];return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,col)
def cylinder(name,x,z,y,radius,height,mat,col='Fountain',n=48):
 vs=[tuple(P(x+radius*math.cos(i*math.tau/n),z+radius*math.sin(i*math.tau/n),y+h)) for h in[0,height] for i in range(n)];fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n)for i in range(n)];return mesh(name,vs,fs,mat,col)
def ring(name,x,z,y,inner,outer,depth,mat,col='Fountain',n=64):
 vs=[tuple(P(x+r*math.cos(i*math.tau/n),z+r*math.sin(i*math.tau/n),y+h)) for h in[0,depth] for r in[inner,outer] for i in range(n)];fs=[]
 for i in range(n):
  j=(i+1)%n;fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,mat,col)
def lettering(name,text,point,size,mat,angle=0,col='Furniture',flat=False):
 cu=bpy.data.curves.new(name,'FONT');cu.body=text;cu.size=size;cu.align_x='CENTER';cu.extrude=.002;o=bpy.data.objects.new(name,cu);C[col].objects.link(o);o.location=P(*point);o.rotation_euler=(0,0,angle)if flat else(math.pi/2,0,angle);cu.materials.append(mat);return o

# Only this scene receives development glass B; original source materials remain untouched.
glass_copies={}
for o in C['Context - approved market'].objects:
 if o.type!='MESH':continue
 for slot in o.material_slots:
  m=slot.material
  if not m or 'soft blue green glass' not in m.name:continue
  if m.name not in glass_copies:
   m2=m.copy();m2.name='C1 context / development glass B';p=next(n for n in m2.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Transmission Weight'].default_value=0;p.inputs['Roughness'].default_value=.19;p.inputs['Metallic'].default_value=.12;p.inputs['Alpha'].default_value=.18
   color=p.inputs['Base Color'].default_value;p.inputs['Base Color'].default_value=(color[0]*.48,color[1]*.48,color[2]*.48,1);m2.use_backface_culling=True;glass_copies[m.name]=m2
  slot.link='OBJECT';slot.material=glass_copies[m.name]

bpy.context.window.scene=scene
before=set(scene.objects);bpy.ops.import_scene.gltf(filepath=OUT+'island-context-reference.glb')
replant=[];palette={}
for o in list(scene.objects):
 if o in before:continue
 for c in list(o.users_collection):c.objects.unlink(o)
 C['Context - existing island plants'].objects.link(o);o['context_only']=True
 if o.type!='MESH':continue
 for slot in o.material_slots:
  m=slot.material
  if not m:continue
  if m.name not in palette:
   native_name=m.get('source_material',m.name.split('|')[1]if'|'in m.name else'');old=bpy.data.materials.get(native_name);copy=old.copy()if old else m.copy();copy.name='C1 actual island / '+m.name;pn=next(n for n in copy.node_tree.nodes if n.type=='BSDF_PRINCIPLED');color=list(m.get('palette',m.diffuse_color[:3]));pn.inputs['Roughness'].default_value=.96
   if pn.inputs['Base Color'].is_linked:
    link=pn.inputs['Base Color'].links[0];socket=link.from_socket;copy.node_tree.links.remove(link);mul=copy.node_tree.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(*color,1);copy.node_tree.links.new(socket,mul.inputs[1]);copy.node_tree.links.new(mul.outputs[0],pn.inputs['Base Color'])
   else:pn.inputs['Base Color'].default_value=(*color,1)
   palette[m.name]=copy
  slot.link='OBJECT';slot.material=palette[m.name]
 for p in o.data.polygons:p.use_smooth=True
 x,z=o.matrix_world.translation.x+36,44-o.matrix_world.translation.y
 if o.get('context_kind')in['understory','fern']and 20.5<x<28 and 4<z<14.4:
  old=list(o.matrix_world.translation);q=len(replant);o.matrix_world.translation=P(20.88,6.2+(q%6)*.72,22.27);replant.append({'object':o.name,'original_native':old,'proposed_native':list(o.matrix_world.translation),'status':'isolated proposed replanting only'})

floor=21.8;xa,xb,za,zb=20.5,28.0,4.0,14.4
# Retaining bases meet the unchanged measured terrain, rather than a flat datum.
contacts=[]
for side,a,b in [('west',(xa,za),(xa,zb)),('south',(xa,zb),(xb,zb)),('north',(xa,za),(xb,za)),('east',(xb,za),(xb,zb))]:
 length=math.dist(a,b);n=math.ceil(length/.8)
 for i in range(n):
  t0=i/n;t1=(i+1)/n;p0=(a[0]+(b[0]-a[0])*t0,a[1]+(b[1]-a[1])*t0);p1=(a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1);g0,g1=G(*p0)-.15,G(*p1)-.15
  vs=[tuple(P(*p0,g0)),tuple(P(*p1,g1)),tuple(P(*p1,floor-.12)),tuple(P(*p0,floor-.12))];o=mesh('Terrain-scribed retaining / '+side,vs,[(0,1,2,3)],stone,'Supports');mod=o.modifiers.new('Retaining wall depth','SOLIDIFY');mod.thickness=.24
  contacts.extend([(p0[0],p0[1],g0),(p1[0],p1[1],g1)])
box('Telaga Awan structural paving bed',(24.25,9.2,floor-.14),(7.5,10.4,.28),sand,'Paving',.025)
for i in range(15):
 for j in range(20):
  x=xa+(i+.5)*7.5/15;z=za+(j+.5)*10.4/20;mat=sand
  box('Warm stone paver', (x,z,floor+.012),(7.5/15-.012,10.4/20-.012,.024),mat,'Paving',.006)
# Five shallow risers meet the protected forecourt's open west edge.
for i in range(5):
 x=28-(i+.5)*.30;top=22.614-(i+1)*((22.614-floor)/5);g=min(G(x,13),top-.2);box('Forecourt five-step connection',(x,13,(g+top)/2),(.30,3.4,top-g),sand,'Paving',.014)
for z in[11.4,14.6]:
 for x in[26.5,27.1,27.7,28.05]:
  top=floor+(x-26.5)/1.55*(22.614-floor);beam('Entry handrail upright',(x,z,top-.1),(x,z,top+1.05),.055,.055,metal,'Furniture')
 beam('Entry timber handrail',(26.5,z,floor+1.05),(28.05,z,22.614+1.05),.085,.075,wood)

# One civic focal feature: split bronze leaves collecting water into a low circular basin.
fx,fz=24,9
cylinder('Fountain stone foot',fx,fz,floor+.024,1.42,.18,stone)
ring('Fountain limestone seat rim',fx,fz,floor+.18,1.20,1.42,.22,sand)
cylinder('Quiet jade basin',fx,fz,floor+.23,1.19,.025,water)
normal=Vector((.84,-.54,0));across=Vector((.54,.84,0));centre=P(fx,fz,floor+.24)
for sign,height in[(-1,2.9),(1,3.65)]:
 vs=[]
 for i in range(19):
  t=i/18;mid=centre+across*(sign*(.08+.90*math.sin(t*math.pi/2)))+normal*(.22*math.sin(t*math.pi));mid.z+=height*t;w=.04+.24*math.sin(t*math.pi)**.8
  for e in[-1,1]:vs.append(tuple(mid+normal*w*e))
 o=mesh('Swept bronze rain leaf',vs,[(2*i,2*i+1,2*i+3,2*i+2)for i in range(18)],bronze,'Fountain');mod=o.modifiers.new('Editable leaf thickness','SOLIDIFY');mod.thickness=.055;be=o.modifiers.new('Bronze edge glint','BEVEL');be.width=.025;be.segments=2
 for p in o.data.polygons:p.use_smooth=True
for k in range(13):
 a=-1.1+2.2*k/12;vs=[]
 for j in range(13):
  t=j/12;h=2.7*(1-t)+.10;u=a*(.25+.62*t);p=centre+across*u+normal*(.1+.5*math.sin(t*math.pi));p.z+=h
  for e in[-1,1]:vs.append(tuple(p+across*.012*e))
 mesh('Light rain veil strand',vs,[(2*j,2*j+1,2*j+3,2*j+2)for j in range(12)],foam if k%4==0 else water,'Fountain')
for r in[.55,.90]:ring('Water ripple',fx,fz,floor+.262,r,r+.012,.008,foam)
lettering('Fountain name','TELAGA AWAN',(fx+.84*1.4,fz+.54*1.4,floor+.32),.15,cream,1.0)

# An open limasan-family shade bay frames the square, without becoming another shop.
for x in[20.7,24.3]:
 for z in[10.95,14.15]:
  box('Shade stone shoe',(x,z,floor+.09),(.35,.35,.18),stone,'Timber shade');beam('Shade timber post',(x,z,floor+.16),(x,z,floor+2.65),.13,.13,wood,'Timber shade')
for z in[10.95,14.15]:beam('Shade header',(20.55,z,floor+2.65),(24.45,z,floor+2.65),.18,.20,wood,'Timber shade')
for x in[20.7,24.3]:beam('Shade side beam',(x,10.75,floor+2.65),(x,14.35,floor+2.65),.14,.18,wood,'Timber shade')
roof_pts=[P(20.25,10.5,floor+2.70),P(24.75,10.5,floor+2.70),P(24.75,14.6,floor+2.70),P(20.25,14.6,floor+2.70),P(21.8,12.55,floor+3.15),P(23.2,12.55,floor+3.15)]
roof=mesh('Low protective limasan roof',[tuple(p)for p in roof_pts],[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],clay,'Timber shade');mod=roof.modifiers.new('Editable roof thickness','SOLIDIFY');mod.thickness=.065
for x in[20.3+i*.3 for i in range(16)]:
 t=max(0,1-abs(x-22.5)/2.25);beam('Roof clay articulation',(x,10.5,floor+2.74),(x,12.55,floor+2.74+.40*t),.025,.035,clay,'Timber shade');beam('Roof clay articulation',(x,12.55,floor+2.74+.40*t),(x,14.6,floor+2.74),.025,.035,clay,'Timber shade')
for z in[11.2,13.9]:
 for k in range(3):box('Shaded timber seat',(22.5,z+(k-1)*.14,floor+.46),(3.0,.12,.06),wood)
 for x in[21.3,23.7]:box('Seat stone pier',(x,z,floor+.22),(.22,.42,.44),stone)
for z in[6.2,7.7,9.2]:
 box('Planted seating-edge trough',(20.82,z,floor+.22),(.62,1.35,.44),stone,'Planting');box('Planter soil',(20.82,z,floor+.43),(.48,1.18,.035),soil,'Planting')
 for k in range(7):
  a=k*2.4;p=P(20.82,z,floor+.46);mid=p+Vector((.22*math.cos(a),.22*math.sin(a),.55));tip=p+Vector((.40*math.cos(a),.40*math.sin(a),.30));side=Vector((-.08*math.sin(a),.08*math.cos(a),0));mesh('Tropical planted edge leaf',[tuple(p),tuple(mid+side),tuple(tip),tuple(mid-side)],[(0,1,2,3)],leaf,'Planting')
# A single two-person table supports gathering; it leaves the principal loop clear.
cylinder('Square cafe table',22.2,5.5,floor+.74,.42,.045,wood,'Furniture',24)
beam('Cafe table stem',(22.2,5.5,floor+.05),(22.2,5.5,floor+.74),.06,.06,metal)
for z in[4.8,6.2]:
 box('Cafe chair seat',(22.2,z,floor+.45),(.44,.44,.05),wood)
 for x in[22.02,22.38]:
  for zz in[z-.18,z+.18]:beam('Cafe chair leg',(x,zz,floor+.03),(x,zz,floor+.44),.035,.035,metal)
 box('Cafe chair back',(22.2,z+(.2 if z>5.5 else-.2),floor+.75),(.43,.04,.24),wood)
# Distinct warm paving links the new court to two reserved interfaces, following actual ground.
route_record=[]
def ribbon(name,points,width,mat):
 vs=[]
 for i,(x,z,y)in enumerate(points):
  a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)];dx,dz=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dz)or 1
  for sign in[-1,1]:
   xx=x+dz/ln*width/2*sign;zz=z-dx/ln*width/2*sign;yy=y if abs(y-(G(x,z)+.08))>.01 else G(xx,zz)+.08;vs.append(tuple(P(xx,zz,yy)))
 mesh(name,vs,[(2*i,2*i+1,2*i+3,2*i+2)for i in range(len(points)-1)],mat,'Proposed routes');route_record.append({'name':name,'width':width,'points':points,'playable':'NOT TESTED - isolated design'})
def groundline(points,step=.45):
 out=[]
 for a,b in zip(points,points[1:]):
  n=max(1,math.ceil(math.dist(a,b)/step))
  for i in range(n):x=a[0]+(b[0]-a[0])*i/n;z=a[1]+(b[1]-a[1])*i/n;out.append((x,z,G(x,z)+.08))
 x,z=points[-1];out.append((x,z,G(x,z)+.08));return out
north_start=(26.6,4.0,floor);north_end=(28.2,2.4,G(28.2,2.4)+.08)
for i in range(6):
 t=(i+.5)/6;x=north_start[0]+(north_end[0]-north_start[0])*t;z=north_start[1]+(north_end[1]-north_start[1])*t;top=floor+(north_end[2]-floor)*(i+1)/6;box('North garden threshold step',(x,z,top-.11),(.41,2.6,.22),sand,'Proposed routes')
north=groundline([(28.2,2.4),(31,-1.6),(35,-1.2),(36,0),(40,-4),(44,-8)]);ribbon('Proposed square to Guild approach',north,2.6,sand)
west_end=(17.8,12.6,G(17.8,12.6)+.08);rise=(floor-west_end[2])/9
for i in range(9):
 x=20.5-(i+.5)*.30;top=floor-(i+1)*rise;box('Highland gate step',(x,12.6,top-.12),(.30,2.6,.24),sand,'Proposed routes')
trail=groundline([(17.8,12.6),(12,11),(4,8),(-5,5)]);ribbon('Proposed natural trail to existing ridge junction',trail,2.6,stone)
lettering('Highland beam direction','PUNCAK  /  HIGHLAND',(20.6,12.6,floor+2.26),.14,cream,math.pi/2)
# A measured silhouette only: no NPC or controller is introduced.
for x,z in[(26.6,10.7)]:
 box('1.8 m scale reference torso',(x,z,floor+1.14),(.38,.21,.62),metal,'Scale reference',.08)
 cylinder('Scale reference head',x,z,floor+1.50,.12,.25,wood,'Scale reference',16)
 for dx in[-.12,.12]:beam('Scale reference leg',(x+dx,z,floor+.05),(x+dx,z,floor+.85),.13,.14,metal,'Scale reference')
 for dx in[-.27,.27]:beam('Scale reference arm',(x+dx,z,floor+.86),(x+dx,z,floor+1.37),.10,.12,metal,'Scale reference')

# Camera presets use the same metre mapping as the game and measured support heights.
camera_record=[]
def camera(name,p,t,lens=28,ortho=None):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);C['Cameras'].objects.link(o);o.location=P(*p);o.rotation_euler=(P(*t)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_end=1000
 if ortho:d.type='ORTHO';d.ortho_scale=ortho
 camera_record.append({'name':name,'game_position':p,'game_target':t,'lens_mm':lens,'orthographic_width':ortho});return o
arrival=camera('C1 Market-to-square eye 1.65m',(35,16.6,22.614+1.65),(24,9,23.1),26)
interior=camera('C1 Square interior eye 1.65m',(21.75,5.7,floor+1.65),(25.4,11.7,23.5),25)
elevated=camera('C1 Elevated composition',(5,34,42),(27,10,22.5),40)
plan=camera('C1 Measured top-down',(31,18,100),(31,18,21),40,72)
scene.camera=arrival
# Plan-only native geometry labels and dimensions remain hidden in pedestrian renders.
planmat=material('plan ink',(.045,.09,.08),1)
for body,pos,size in [('NEW COURT 7.5 x 10.4 m / 21.80 m',(24.25,3.2,52),.55),('EXISTING FORECOURT / 22.614 m',(36,7.3,52),.55),('5 x 0.163 m',(28.5,15.7,52),.48),('GUILD APPROACH - RESERVATION ONLY',(42,-10.8,52),.55),('HIGHLAND / existing ridge trail',(1,3,52),.55),('N',(15,-8,52),1.2)]:lettering('Plan annotation',body,pos,size,planmat,0,'Plan annotations',True)
for x in[20.5,28]:beam('Measured court width tick',(x,3.5,51.9),(x,2.9,51.9),.025,.025,planmat,'Plan annotations')
beam('Measured court width',(20.5,3.2,51.9),(28,3.2,51.9),.022,.022,planmat,'Plan annotations')
C['Plan annotations'].hide_render=True
scene['phase']='R0-C1A DESIGN ONLY';scene['mapping']='game = (36+u,18.6+h,44-v)';scene['court_floor']=floor;scene['new_court_m2']=78.0;scene['existing_forecourt_m2']=99.2;scene['route_test_status']='Proposed routes NOT PLAYTESTED';scene['cameras']=json.dumps(camera_record);scene['source_context_transforms']=json.dumps(context_record);scene['replanting_proposal']=json.dumps(replant);scene['routes']=json.dumps(route_record);scene['terrain_contacts']=json.dumps(contacts)
for s in list(bpy.data.scenes):
 if s!=scene:bpy.data.scenes.remove(s)
bpy.data.orphans_purge(do_recursive=True)
bpy.context.view_layer.update();bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=OUT+'town-square-design.blend')
print(json.dumps({'scene':scene.name,'objects':len(scene.objects),'new_court_floor':floor,'replanting_proposals':replant,'cameras':camera_record,'contact_count':len(contacts)}))
