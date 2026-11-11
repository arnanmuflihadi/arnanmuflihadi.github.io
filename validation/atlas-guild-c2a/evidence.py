import bpy,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-c2a/';d=json.loads(s['c2a_design']);terrain=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,120),Vector((0,0,-1)))[0].z+18.6
# Entrance inspection from the proposed lower landing, not an invented exterior platform.
c=bpy.data.objects['C2A 02 Entrance and forecourt'];c.location=P(37.5,-2.9,23.2+1.65);c.rotation_euler=(P(34.1,-4.2,25.8)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=20
c=bpy.data.objects['C2A 03 Town and Guild'];c.location=P(3,64,64);c.rotation_euler=(P(32,16,25)-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=35
plan=bpy.data.collections['C2A / Measured plan'];ink=bpy.data.materials['C1 / plan ink'];route_mat=bpy.data.materials['C1 / deep green metal'];gold=bpy.data.materials['C1 / terracotta']
def line(n,points,mat=ink,w=.045):
 vs=[];fs=[]
 for a,b in zip(points,points[1:]):
  dx,dz=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dz)
  if length<.001:continue
  nx,nz=-dz/length*w/2,dx/length*w/2;i=len(vs);vs.extend(P(x,z,48)for x,z in[(a[0]+nx,a[1]+nz),(a[0]-nx,a[1]-nz),(b[0]-nx,b[1]-nz),(b[0]+nx,b[1]+nz)]);fs.append((i,i+1,i+2,i+3))
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.materials.append(mat);ob=bpy.data.objects.new(n,me);plan.objects.link(ob)
def text(n,body,x,z,size=.52):
 cu=bpy.data.curves.new(n,'FONT');cu.body=body;cu.size=size;cu.align_x='LEFT';cu.space_line=1.2;cu.materials.append(ink);o=bpy.data.objects.new(n,cu);plan.objects.link(o);o.location=P(x,z,48.1)
# Actual metric dimensions, elevations and route references, separate from beauty geometry.
line('Footprint outline',[(30.5,-8.8),(38.1,-8.8),(38.1,-4.2),(30.5,-4.2),(30.5,-8.8)])
line('Guild width',[(30.5,-10.5),(38.1,-10.5)])
for x in[30.5,38.1]:line('width tick',[(x,-9.9),(x,-11.1)])
text('Width label','7.60 m',32.8,-11.0,.55)
line('Guild depth',[(28.7,-8.8),(28.7,-4.2)])
for z in[-8.8,-4.2]:line('depth tick',[(28.2,z),(29.2,z)])
text('Depth label','4.60 m',25.2,-6.5,.5)
existing=[[26.2,12.6],[25.9,12.6],[25.9,6],[25.9,4.6],[26.6,4],[28.3,3.8],[29.8,3],[31,1.5],[33,.5],[36,0],[40,-4],[44,-8]]
line('Approved C1C route',existing,route_mat,.11)
new=d['approach']['fan_points']+[[35.6,-3.4],[34.1,-4.2]];line('Proposed Guild entrance',new,gold,.13)
text('Title','ATLAS GUILD / R0-C2A SITE STUDY',11,-14,.7)
text('Guild label','GUILD\n34.96 m2 footprint\nFloor 24.20 / 25.60 m\nLantern top 39.85 m',11,-9,.5)
text('Entrance label','Entrance 24.20 m\n6 x 167 mm / 2.30 m wide',40,-.7,.47)
text('Boundary label','44,-8 boundary\nretained / not an entrance',45,-9,.42)
text('Court label','TELAGA AWAN\nCourt floor 21.80 m',16,8,.48)
text('Market label','MARKET STREET\napproved / unchanged',39,16,.48)
text('Highland label','Highland branch\ncontinues west',7,13,.42)
text('Legend','Green: approved route\nTerracotta: proposed branch\nNo terrain editing\n1 fern replant proposed',44,6,.43)
line('10 metre scale',[(10,19),(20,19)],ink,.08)
for x in[10,15,20]:line('scale tick',[(x,18.7),(x,19.3)])
text('Scale label','0        5        10 m / N up',10,18.3,.42)
plan.hide_render=True
# Resurvey the selected footprint on the exact mesh.
report={'design':d,'supports':{},'visibility':{},'geometry':{},'cameras':{}}
for n,x0,x1,z0,z1,floor in [('lower_hall',30.5,38.1,-6.2,-4.2,24.2),('rear_hall',30.5,38.1,-8.8,-6.2,25.6),('terrace',32.25,36.8,-4.2,-2.55,24.2)]:
 values=[]
 for i in range(41):
  for j in range(21):values.append(floor-G(x0+(x1-x0)*i/40,z0+(z1-z0)*j/20))
 values.sort();report['supports'][n]={'floor':floor,'area':(x1-x0)*(z1-z0),'gap_min':values[0],'gap_max':values[-1],'gap_median':values[len(values)//2],'footing_embed':.18}
dg=bpy.context.evaluated_depsgraph_get();total=0;mats=set()
for col in s.collection.children:
 if not col.name.startswith('C2A /')or col.name.endswith(('cameras','plan')):continue
 count=0;objects=0
 for o in col.objects:
  if o.type not in ['MESH','FONT','CURVE']:continue
  ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();count+=len(me.loop_triangles);objects+=1;mats.update(m.name for m in me.materials if m);ev.to_mesh_clear()
 report['geometry'][col.name]={'triangles':count,'objects':objects};total+=count
report['geometry']['total_triangles']=total;report['geometry']['materials']=sorted(mats)
for name in ['C2A 01 Guild from Telaga Awan','C2A 02 Entrance and forecourt','C2A 03 Town and Guild','C2A 04 Measured site plan']:
 c=bpy.data.objects[name];p=c.location;report['cameras'][name]={'position':[p.x+36,p.z+18.6,44-p.y],'quaternion':list(c.rotation_euler.to_quaternion()),'lens_mm':c.data.lens,'horizontal_fov_degrees':math.degrees(c.data.angle),'type':c.data.type,'ortho_width':c.data.ortho_scale if c.data.type=='ORTHO'else None,'resolution':[1440,960]}
for origin_name,origin in [('court',[26,23.45,11.8]),('market',[36,23.61,17])]:
 results=[]
 for target in [[34.1,26.3,-4.2],[34.1,29.8,-4.2],[34.8,36.5,-4.6]]:
  a=P(origin[0],origin[2],origin[1]);b=P(target[0],target[2],target[1]);h=s.ray_cast(dg,a,(b-a).normalized(),distance=(b-a).length+.1);results.append({'target':target,'first_hit':h[4].name if h[0]else None,'distance':(h[1]-a).length if h[0]else None,'guild_visible':bool(h[0]and h[4].name.startswith('Guild /'))})
 report['visibility'][origin_name]=results
s['c2a_evidence']=json.dumps(report);s.render.resolution_x=1440;s.render.resolution_y=960;s.cycles.samples=48;s.camera=bpy.data.objects['C2A 01 Guild from Telaga Awan'];bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend')
print(json.dumps(report))
