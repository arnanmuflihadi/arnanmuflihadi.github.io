import bpy,bmesh,math,json
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-r0c2/'
assert bpy.data.filepath.endswith('/atlas-guild-reset/atlas-guild.blend')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild.blend')
s=bpy.context.scene
roof=bpy.data.collections['Guild reset / Roof and lantern'];detail=bpy.data.collections['Guild reset / Timber and glazing'];ground=bpy.data.collections['Guild reset / Ground and entrance']
# Replace the obsolete tall neck with a broad, roof-integrated observation drum.
for o in list(roof.objects):
 if o.type!='MESH' or not any(k in o.name.lower()for k in ['lantern','observation','survey finial']):continue
 shaft='shaft' in o.name.lower()
 inv=o.matrix_world.inverted()
 for v in o.data.vertices:
  p=o.matrix_world@v.co;p.x=.4+(p.x-.7)*(1.75 if shaft else 1.0);p.y+=.6
  p.z=5.27+(p.z-5.27)*1.4/4.7 if shaft else 6.65+(p.z-9.879)*.78
  v.co=inv@p
 o.data.update()
stone=bpy.data.materials['C1 / warm limestone'];timber=bpy.data.materials['C1 / oiled timber'];bronze=bpy.data.materials['C1 / weathered bronze'];green=bpy.data.materials['C1 / deep green metal'];cream=bpy.data.materials['C1 / sign lettering']
def mesh(name,vs,fs,mat,col=roof):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o=bpy.data.objects.new('Guild C2 / '+name,me);col.objects.link(o);return o
boxfaces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box(name,x0,x1,y0,y1,z0,z1,mat,col=detail):return mesh(name,[(x,y,z)for z in[z0,z1]for x,y in[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]],boxfaces,mat,col)
def beam(name,a,b,width,depth,mat):
 a=Vector(a);b=Vector(b);d=b-a;q=d.to_track_quat('Z','Y');vs=[tuple((a+b)*.5+q@Vector((x,y,z)))for z in[-d.length*.5,d.length*.5]for x,y in[(-width/2,-depth/2),(width/2,-depth/2),(width/2,depth/2),(-width/2,depth/2)]];return mesh(name,vs,boxfaces,mat)
# Remove the old site's tree-avoidance cut, retaining the same roof vocabulary and eaves.
for o in list(roof.objects):
 if o.name.startswith('Atlas / Limasan research-hall roof')or 'tree-aware corner fascia' in o.name:bpy.data.objects.remove(o,do_unlink=True)
vs=[(-4.5,-3.238,4.72),(4.875,-3.238,4.72),(4.875,3.562,4.72),(-4.5,3.562,4.72),(-1.1,.162,6.25),(1.9,.162,6.25)]
vs+= [(x,y,z-.13)for x,y,z in vs]
faces=[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4),(10,11,7,6),(11,8,7),(11,10,9,8),(10,6,9),(0,6,7,1),(1,7,8,2),(2,8,9,3),(3,9,6,0)]
mesh('complete limasan research roof',vs,faces,bpy.data.materials['S2A / terracotta 1'])
for i in range(4):beam('deep eave fascia '+str(i),vs[i],vs[(i+1)%4],.15,.22,timber)
for i,j in [(0,4),(3,4),(1,5),(2,5),(4,5)]:beam('terracotta hip cap',Vector(vs[i])+Vector((0,0,.055)),Vector(vs[j])+Vector((0,0,.055)),.11,.10,bpy.data.materials['S2A / terracotta 3'])
for side in [-1,1]:
 for i in range(1,9):
  dy=i*3.4/9;y=.162+side*dy;z=6.25-dy*(1.53/3.4)+.015
  beam('roof tile course',(-1.1-dy,y,z),(1.9+dy*2.975/3.4,y,z),.025,.018,bpy.data.materials['S2A / terracotta '+str(i%5)])
# Secondary civic identity is real, editable lettering above the protected 2.7 m doorway.
for o in list(detail.objects):
 if o.name=='Atlas / research subtitle':bpy.data.objects.remove(o,do_unlink=True)
box('secondary identity plaque',-1.404,1.404,-1.925,-1.81,3.27,3.52,green)
data=bpy.data.curves.new('Balai Riset identity','FONT');data.body='Balai Riset · Transit Kingdom';data.align_x='CENTER';data.size=.19;data.extrude=.0015
obj=bpy.data.objects.new('Guild C2 / secondary identity lettering',data);detail.objects.link(obj);obj.location=(0,-1.94,3.34);obj.rotation_euler=(math.pi/2,0,0);obj.data.materials.append(cream)
bpy.context.view_layer.update()
if obj.dimensions.x>2.62:obj.scale*=2.62/obj.dimensions.x
# A restrained survey compass belongs to the research hall's fanlight, not a new prop system.
verts=[];faces=[]
for i in range(48):
 a=i*math.tau/48
 for r in [.40,.425]:verts.append((math.cos(a)*r,-3.10,5.3+math.sin(a)*r))
for i in range(48):faces.append((2*i,2*((i+1)%48),2*((i+1)%48)+1,2*i+1))
for i in range(8):
 a=i*math.tau/8;r=.35 if i%2 else .56;b=len(verts);verts.extend([(math.cos(a)*r,-3.104,5.3+math.sin(a)*r),(math.cos(a+.18)*.16,-3.104,5.3+math.sin(a+.18)*.16),(math.cos(a-.18)*.16,-3.104,5.3+math.sin(a-.18)*.16)]);faces.append((b,b+1,b+2))
mesh('survey compass inlay',verts,faces,bronze,detail)
s.name='Atlas Guild / R0-C2 integrated landmark';s['design_scope']='R0-C2 local-only Guild; accepted populated town unchanged'
for camera_name in ['01 Guild from Telaga Awan','03 Guild in town']:
 cam=bpy.data.objects[camera_name];target=Vector((0,0,4.6)) if camera_name.startswith('01')else Vector((0,-9,3.2));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
s.camera=bpy.data.objects['01 Guild from Telaga Awan']
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild.blend')
print(json.dumps({'lanternTop':9.31448,'floorDatum':.57,'secondaryIdentity':data.body,'floorWorld':16.05,'sourcePreserved':True}))
