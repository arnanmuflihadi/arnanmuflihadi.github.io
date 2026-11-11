import bpy,bmesh,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/atlas-guild-c2a/'
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
# Remove the coincident structural top beneath the separate visible paving cap.
o=bpy.data.objects['Guild / entrance terrace'];bm=bmesh.new();bm.from_mesh(o.data);faces=[]
for f in bm.faces:
 if all(abs((o.matrix_world@v.co).z+18.6-24.2)<.001 for v in f.verts):faces.append(f)
bmesh.ops.delete(bm,geom=faces,context='FACES');bm.to_mesh(o.data);bm.free()
# High-contrast Blender plan annotations; never included in the architectural geometry.
plan=bpy.data.collections['C2A / Measured plan']
def material(n,c):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=next(q for q in m.node_tree.nodes if q.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=c;p.inputs['Roughness'].default_value=1;p.inputs['Emission Color'].default_value=c;p.inputs['Emission Strength'].default_value=.7;return m
paper=material('C2A / plan paper',(.93,.89,.74,1));ink=material('C2A / plan ink',(.025,.07,.07,1));green=material('C2A / approved route',(.02,.32,.32,1));red=material('C2A / proposed route',(.75,.20,.055,1))
for ob in list(plan.objects):
 ob.visible_shadow=False
 if ob.type=='FONT':ob.data.materials.clear();ob.data.materials.append(ink)
 elif 'Approved C1C'in ob.name:ob.data.materials[0]=green
 elif 'Proposed Guild'in ob.name:ob.data.materials[0]=red
 else:ob.data.materials[0]=ink
bpy.context.view_layer.update()
for ob in list(plan.objects):
 if ob.type!='FONT':continue
 vs=[ob.matrix_world@Vector(v)for v in ob.bound_box];x0,x1=min(v.x for v in vs)-.18,max(v.x for v in vs)+.18;y0,y1=min(v.y for v in vs)-.16,max(v.y for v in vs)+.16;z=ob.location.z-.025
 me=bpy.data.meshes.new('Plan label backing');me.from_pydata([(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],[],[(0,1,2,3)]);me.materials.append(paper);bb=bpy.data.objects.new('Plan label backing',me);plan.objects.link(bb);bb.visible_shadow=False
# Actual native support-surface profile, kept separate from a traversal claim.
verts=[];faces=[]
for ob in bpy.data.collections['C2A / Site and approach'].objects:
 if not ob.get('proposed_walkable')and'entrance terrace arris'not in ob.name:continue
 offset=len(verts);verts.extend(ob.matrix_world@v.co for v in ob.data.vertices);faces.extend([offset+i for i in p.vertices]for p in ob.data.polygons)
walk=BVHTree.FromPolygons(verts,faces)
def H(x,z):
 h=walk.ray_cast(P(x,z,100),Vector((0,0,-1)))
 return h[0].z+18.6 if h[0]else None
d=json.loads(s['c2a_design']);path=d['approach']['fan_points'];profile=[];maxgrade=0;dist=0
for a,b in zip(path,path[1:]):
 length=math.dist(a,b);n=math.ceil(length/.08)
 for j in range(n):
  u=j/n;v=(j+1)/n;x,z=a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u;xx,zz=a[0]+(b[0]-a[0])*v,a[1]+(b[1]-a[1])*v;y,yy=H(x,z),H(xx,zz)
  if y is not None and yy is not None:maxgrade=max(maxgrade,abs(yy-y)/(length/n))
  profile.append([x,z,y]);dist+=length/n
report=json.loads(s['c2a_evidence']);report['approach_profile']={'fan_length':dist,'max_measured_fan_grade':maxgrade,'centre_samples':profile,'controller_tested':False,'local_final_route_length':d['approach']['fan_run']+d['approach']['stair_run']+math.hypot(35.6-34.1,-3.4+4.2),'direct_branch_to_door':math.hypot(40-34.1,-4+4.2)}
# Refresh saved camera records after entrance framing was corrected.
for n in report['cameras']:
 c=bpy.data.objects[n];p=c.location;report['cameras'][n]={'position':[p.x+36,p.z+18.6,44-p.y],'quaternion':list(c.rotation_euler.to_quaternion()),'lens_mm':c.data.lens,'horizontal_fov_degrees':math.degrees(c.data.angle),'type':c.data.type,'ortho_width':c.data.ortho_scale if c.data.type=='ORTHO'else None,'resolution':[1440,960]}
report['cameras']['C2A 02 Entrance and forecourt']['description']='Elevated entrance/forecourt inspection; pedestrian-height view is camera 01'
report['design']=d;s['c2a_evidence']=json.dumps(report)
plan.hide_render=True;s.camera=bpy.data.objects['C2A 02 Entrance and forecourt'];s.render.filepath=OUT+'02-entrance.png';bpy.ops.render.render(write_still=True)
plan.hide_render=False;s.camera=bpy.data.objects['C2A 04 Measured site plan'];s.render.filepath=OUT+'04-measured-plan.png';bpy.ops.render.render(write_still=True)
plan.hide_render=True;s.camera=bpy.data.objects['C2A 01 Guild from Telaga Awan'];bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend')
print(json.dumps({'fan_max_grade':maxgrade,'final_route':report['approach_profile']['local_final_route_length'],'coplanar_faces_removed':len(faces)}))
