import bpy,math,json
from mathutils import Vector,Matrix
ROOT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio';OUT=ROOT+'/validation/skyport-r0c3'
# The MCP call supplies the measured survey as a JSON literal; no file execution or file-reading API is used in Blender.
datum=survey['datum']
source_post=bpy.data.objects.get('Shade timber post');source_shoe=bpy.data.objects.get('Shade stone shoe')
assert source_post and source_shoe,'Open the approved Guild master as the reusable component library first'
materials={n:bpy.data.materials[n] for n in ['C1 / oiled timber','C1 / terracotta','C1 / warm volcanic stone','C1 / warm limestone','C1 / weathered bronze','S2A / warm lime plaster','S2A / cut timber edges']}
scene=bpy.data.scenes.new('Pelabuhan Awan / R0-C3');bpy.context.window.scene=scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
cols={}
for n in ['Canopy','Timber structure','Landing identity','Reused furniture','Context','Views']:
 c=bpy.data.collections.new('Skyport / '+n);scene.collection.children.link(c);cols[n]=c
def link(o,c):
 for old in list(o.users_collection):old.objects.unlink(o)
 cols[c].objects.link(o);return o
def material(n,color,rough=.7,metal=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
timber=materials['C1 / oiled timber'];clay=materials['C1 / terracotta'];stone=materials['C1 / warm volcanic stone'];lime=materials['C1 / warm limestone'];bronze=materials['C1 / weathered bronze'];cream=materials['S2A / warm lime plaster'];edge=materials['S2A / cut timber edges'];jade=material('Skyport / enamel jade',(.055,.19,.165),.48,.18);letter=material('Skyport / warm ivory lettering',(.91,.82,.57),.65,.12)
def mesh(n,verts,faces,mat,c):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.materials.append(mat);me.update();o=bpy.data.objects.new(n,me);cols[c].objects.link(o);return o
def cube(n,pos,size,mat,c='Timber structure',bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=link(bpy.context.object,c);o.name=n;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 if bevel:mod=o.modifiers.new('Soft architectural arris','BEVEL');mod.width=bevel;mod.segments=1
 return o
def bar(n,a,b,w,mat,c='Timber structure'):
 a,b=Vector(a),Vector(b);o=cube(n,(a+b)/2,(w,w,(b-a).length),mat,c);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def tube(n,points,r,mat,c='Timber structure'):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=r;cu.bevel_resolution=0;s=cu.splines.new('POLY');s.points.add(len(points)-1)
 for p,v in zip(s.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(n,cu);cu.materials.append(mat);cols[c].objects.link(o);return o
def ground(x,y):
 # Measured existing support, used only to ground context/props; original terrain stays untouched.
 v=-7-y;ranked=sorted(((r['u']-x)**2+(r['v']-v)**2,i)for i,r in enumerate(survey['rows']));near=[survey['rows'][i]for d,i in ranked[:4]]
 for r in near:
  d=math.hypot(r['u']-x,r['v']-v)
  if d<.00001:return r['floor']-datum
 weights=[1/max(.001,math.hypot(r['u']-x,r['v']-v))**3 for r in near]
 return sum(r['floor']*w for r,w in zip(near,weights))/sum(weights)-datum
def component(src,n,pos,size):
 me=src.data.copy();bounds=[Vector(b) for b in src.bound_box];lo=Vector(tuple(min(p[i]for p in bounds)for i in range(3)));hi=Vector(tuple(max(p[i]for p in bounds)for i in range(3)));centre=(lo+hi)/2
 me.transform(Matrix.Translation(-centre));o=bpy.data.objects.new(n,me);cols['Timber structure'].objects.link(o);o.location=pos;o.scale=tuple(size[i]/(hi[i]-lo[i])for i in range(3));o['source_component']=src.name;return o
def roofz(x,y):return 3.48+.83*(abs(x)/4.6)**1.65+.24*((y+2.85)/2.05)**2
nx,ny=36,12;verts=[(x,y,roofz(x,y))for y in [-.8-4.1*j/ny for j in range(ny+1)]for x in [-4.6+9.2*i/nx for i in range(nx+1)]];faces=[]
for j in range(ny):
 for i in range(nx):a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
roof=mesh('Original double-wing tropical canopy',verts,[tuple(reversed(f))for f in faces],clay,'Canopy');solid=roof.modifiers.new('Editable roof thickness','SOLIDIFY');solid.thickness=.085
underside=mesh('Light soffit / visible layered eaves',[(x,y,z-.095)for x,y,z in verts],faces,cream,'Canopy')
for y in [-.8,-4.9]:
 pts=[(-4.6+9.2*i/48,y,roofz(-4.6+9.2*i/48,y)-.10)for i in range(49)];tube('Bent laminated eave beam',pts,.095,timber)
for x in [-4.6,4.6]:tube('Timber verge / deep edge',[(x,-.8-4.1*i/16,roofz(x,-.8-4.1*i/16)-.10)for i in range(17)],.08,timber)
for i in range(1,24):
 x=-4.6+9.2*i/24;tube('Restrained clay standing seam',[(x,-.82-4.06*j/12,roofz(x,-.82-4.06*j/12)+.012)for j in range(13)],.012,edge,'Canopy')
for y in [-1.25,-4.4]:
 for x in [-3.3,3.3]:
  z=ground(x,y);component(source_shoe,'Reused pavilion stone shoe',(x,y,z+.12),(.48,.48,.24));component(source_post,'Reused pavilion timber pier',(x,y,z+1.55),(.23,.23,2.9));bar('Forked canopy haunch',(x,y,z+2.35),(math.copysign(4.05,x),y,roofz(4.05,y)-.20),.15,timber);bar('Inward roof brace',(x,y,z+2.6),(math.copysign(1.6,x),y,roofz(1.6,y)-.2),.13,timber)
 tube('Structural curved canopy rib',[(-4.45+8.9*i/40,y,roofz(-4.45+8.9*i/40,y)-.22)for i in range(41)],.095,timber)
# A low continuous sign frames the open 6.3 m town-facing pedestrian portal.
cube('Arrival jade fascia',(0,-.76,2.95),(5.75,.14,.68),jade,'Landing identity',.035)
cube('Town-facing jade fascia',(0,-4.86,2.95),(5.75,.14,.68),jade,'Landing identity',.035)
def text(n,body,pos,size,mat,flip=False):
 cu=bpy.data.curves.new(n,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=size;cu.extrude=.002;cu.bevel_depth=.0008;cu.bevel_resolution=0;cu.materials.append(mat);o=bpy.data.objects.new(n,cu);cols['Landing identity'].objects.link(o);o.location=pos;o.rotation_euler=(math.pi/2,0,math.pi if not flip else 0);return o
text('Arrival identity','PELABUHAN AWAN',(0,-.67,3.075),.36,letter)
text('Arrival subtitle','Transit Kingdom · Skyport',(0,-.665,2.8),.145,letter)
text('Town return identity','PELABUHAN AWAN',(0,-4.95,3.075),.36,letter,True)
text('Town return subtitle','Transit Kingdom · Skyport',(0,-4.955,2.8),.145,letter,True)
for x in [-2.6,2.6]:bar('Fascia roof hanger',(x,-.76,3.29),(x,-.76,roofz(x,-.76)-.12),.035,bronze,'Landing identity')
# The original paving remains the actual walking deck. Thin inlays identify the inactive boarding reservation.
for r in [2.2,2.32]:
 pts=[(math.cos(a)*r,1.35+math.sin(a)*r,ground(math.cos(a)*r,1.35+math.sin(a)*r)+.012)for a in [i*math.tau/96 for i in range(97)]];tube('Flush boarding inlay',pts,.011,bronze,'Landing identity')
for i in range(8):
 a=i*math.tau/8;pts=[(math.cos(a)*.18,1.35+math.sin(a)*.18),(math.cos(a-.12)*.68,1.35+math.sin(a-.12)*.68),(math.cos(a)*(1.25 if i%2==0 else .9),1.35+math.sin(a)*(1.25 if i%2==0 else .9)),(math.cos(a+.12)*.68,1.35+math.sin(a+.12)*.68)];mesh('Windrose / future landing reservation',[(x,y,ground(x,y)+.013)for x,y in pts],[(0,1,2,3)],bronze,'Landing identity')
def import_asset(filename,n,x,y,target,rot=0):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=ROOT+'/source-assets/town-population/furniture/Models/GLTF format/'+filename);bpy.context.view_layer.update();objects=list(set(bpy.data.objects)-before);meshes=[o for o in objects if o.type=='MESH'];points=[o.matrix_world@Vector(p) for o in meshes for p in o.bound_box];lo=Vector(tuple(min(p[i]for p in points)for i in range(3)));hi=Vector(tuple(max(p[i]for p in points)for i in range(3)));factor=target/max(hi-lo);matrix=Matrix.Translation(Vector((x,y,ground(x,y))))@Matrix.Rotation(rot,4,'Z')@Matrix.Diagonal((factor,factor,factor,1))@Matrix.Translation(Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z)))
 for o in meshes:
  world=o.matrix_world.copy();o.parent=None;o.matrix_world=matrix@world;link(o,'Reused furniture');o.name=n+' / '+o.name;o['source_file']=filename
  for index,m in enumerate(o.data.materials):
   p=next((v for v in m.node_tree.nodes if v.type=='BSDF_PRINCIPLED'),None)if m.use_nodes else None;color=p.inputs['Base Color'].default_value if p else m.diffuse_color
   o.data.materials[index]=jade if max(color[:3])-min(color[:3])>.1 and color[1]>color[0]*1.15 else timber if sum(color[:3])<1.5 else edge
 for o in objects:
  if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
 return meshes
for x in [-4.5,4.5]:
 import_asset('bench.glb','Kenney / waiting bench',x,-2.7,1.8,math.pi/2 if x<0 else -math.pi/2)
 import_asset('pottedPlant.glb','Kenney / sheltered planter',x,-1.6,1.2)
for x,y,s in [(4,2.4,.6),(4.45,2.0,.45)]:import_asset('cardboardBoxClosed.glb','Kenney / arrival cargo',x,y,s,.18)
for x in [-2.5,2.5]:import_asset('lampSquareCeiling.glb','Kenney / canopy lantern',x,-2.9,.38)
# The source bench is narrow and tall at uniform 1.8 m normalization. Widen its seat instead of scaling up human height.
for o in cols['Reused furniture'].objects:
 if 'waiting bench' not in o.name:continue
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4);ps=[v.co for v in o.data.vertices];cx=(min(p.x for p in ps)+max(p.x for p in ps))/2;cy=(min(p.y for p in ps)+max(p.y for p in ps))/2;bottom=min(p.z for p in ps)
 for p in ps:p.x=cx+(p.x-cx)*.5;p.y=cy+(p.y-cy)*1.1;p.z=bottom+(p.z-bottom)*.5
# Move the reused hanging lights from ground placement to architectural height.
for o in cols['Reused furniture'].objects:
 if 'canopy lantern' in o.name:o.location.z+=2.72
# Read-only measured platform context, not exported or used as a replacement support.
rows=survey['rows'];v=[(r['u'],-(r['v']+7),r['floor']-datum-.002)for r in rows];faces=[]
lookup={(r['u'],r['v']):i for i,r in enumerate(rows)}
for (u,w),i in lookup.items():
 if all(k in lookup for k in [(u+1,w),(u+1,w+1),(u,w+1)]):faces.append((i,lookup[(u+1,w)],lookup[(u+1,w+1)],lookup[(u,w+1)]))
mesh('Measured original deck reference',v,[tuple(reversed(f))for f in faces],lime,'Context')
def camera(n,pos,target,lens=32):
 data=bpy.data.cameras.new(n);o=bpy.data.objects.new(n,data);cols['Views'].objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.lens=lens;return o
scene.camera=camera('Skyport / elevated',(12,14,10),(0,-1,1.5));camera('Skyport / arrival',(0,3,1.6),(0,-2.8,2.7),22);camera('Skyport / town return',(-6,-14,4),(0,-2.5,2),32)
world=bpy.data.worlds.new('Skyport / neutral daylight');world.use_nodes=True;next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.48,.65,.8,1);next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[1].default_value=.5;scene.world=world
data=bpy.data.lights.new('Daylight','SUN');data.energy=2.3;data.angle=.14;o=bpy.data.objects.new('Daylight',data);cols['Views'].objects.link(o);o.rotation_euler=(.5,-.55,-.65)
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1440;scene.render.resolution_y=960;scene.render.resolution_percentage=100
scene['site']=json.dumps({'centre':survey['centre'],'datum':datum,'rotationY':35,'nativeAxes':'X=u, Y=-(v+7), Z=height above centre','terrainChanges':0,'platformExtension':0,'futureTravel':'Inactive reservation only'})
scene['asset_reuse']='C1 pavilion stone shoes and timber piers; approved C1/S2A materials; actual Kenney Furniture Kit CC0 bench, pottedPlant, cardboardBoxClosed, lampSquareCeiling'
for old in list(bpy.data.scenes):
 if old!=scene:bpy.data.scenes.remove(old)
reflection=Matrix.Diagonal((1,-1,1,1))
for c in scene.collection.children:
 if 'Views' in c.name:continue
 for o in c.objects:o.matrix_world=reflection@o.matrix_world
for o in scene.objects:
 if o.type=='FONT':
  o.scale.x*=-1;o.data.resolution_u=3;o.data.bevel_depth=0;o.data.extrude=.001
for o in list(scene.objects):
 if o.name.startswith('Town-facing jade fascia'):bpy.data.objects.remove(o,do_unlink=True)
 elif o.name.startswith('Town return identity'):o.location.y=.85
 elif o.name.startswith('Town return subtitle'):o.location.y=.855
scene['site']='Native X=u, Y=v+7, Z=height above deck datum; standard glTF Y-up then world Y rotation 35 degrees'
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/pelabuhan-awan.blend')
print(json.dumps({'scene':scene.name,'objects':len(scene.objects),'file':bpy.data.filepath,'asset_reuse':scene['asset_reuse']}))
