import bpy,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;C={c.name.removeprefix('C1 / '):c for c in s.collection.children}
terrain=bpy.data.objects['C1 exact unchanged terrain reference'];bvh=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bvh.ray_cast(P(x,z,150),Vector((0,0,-1)))[0].z+18.6
# Finished paving elevation is exactly the documented 21.800 m, not the paving-bed datum.
for o in C['Paving'].objects:
 if o.name.startswith(('Warm stone paver','Telaga Awan structural paving bed')):o.location.z-=.024
for o in C['Fountain'].objects:o.location.z-=.024
# Keep the measured scale reference available in the workspace; no mannequin/NPC in the design photographs.
C['Scale reference'].hide_render=True
for o in list(C['Fountain'].objects):
 if o.name.startswith('Rainwater on bronze leaf'):bpy.data.objects.remove(o,do_unlink=True)
for o in C['Furniture'].objects:
 if o.name.startswith('Fountain name'):o.hide_render=True
# Visible stair foundations meet the actual ground at each corner; no invisible support deck.
for o in C['Proposed routes'].objects:
 if o.name.startswith(('Aligned north gate stair','Highland gate step')):
  for v in list(o.data.vertices)[:4]:v.co.z=G(v.co.x+36,44-v.co.y)-18.6-.15
# A dedicated symbolic plan layer contains route traces, not finished Guild geometry.
ink=bpy.data.materials['C1 / terracotta']
routes=json.loads(s['routes'])
def planline(name,points,material,width=.09):
 vs=[]
 for i,(x,z,y)in enumerate(points):
  a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)];dx,dz=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dz)or 1
  vs.extend([tuple(P(x-dz/ln*width,z+dx/ln*width,52)),tuple(P(x+dz/ln*width,z-dx/ln*width,52))])
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],[(2*i,2*i+1,2*i+3,2*i+2)for i in range(len(points)-1)]);me.materials.append(material);o=bpy.data.objects.new(name,me);C['Plan annotations'].objects.link(o)
planline('Plan main arrival via existing landing',[(36,14.2,0),(36,0,0),(35,-1.2,0),(31,-1.6,0),(28.2,2.4,0),(26.6,4,0)],ink,.10)
for r in routes:planline('Plan '+r['name'],r['points'],ink,.07)
# Numeric inspection is geometry-based, not a gameplay test.
rows=[];deps=bpy.context.evaluated_depsgraph_get();new_tris=0;new_mats=set();context_tris=0
for key,c in C.items():
 tris=0;objects=0
 for o in c.objects:
  if o.type not in ['MESH','FONT','CURVE']:continue
  objects+=1;e=o.evaluated_get(deps);me=e.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles);e.to_mesh_clear()
  if not key.startswith('Context')and key not in['Plan annotations','Scale reference','Cameras']:new_mats.update(slot.material.name for slot in o.material_slots if slot.material)
 rows.append({'collection':key,'geometry_objects':objects,'evaluated_triangles':tris})
 if key.startswith('Context'):context_tris+=tris
 elif key not in['Plan annotations','Scale reference','Cameras']:new_tris+=tris
samples=[(20.5+i*.25,4+j*.26)for i in range(31)for j in range(41)];ground=[G(x,z)for x,z in samples]
route_metrics=[]
for r in routes:
 pts=r['points'];horizontal=sum(math.dist(a[:2],b[:2])for a,b in zip(pts,pts[1:]));length=sum(math.dist(a,b)for a,b in zip(pts,pts[1:]));grades=[(b[2]-a[2])/math.dist(a[:2],b[:2])for a,b in zip(pts,pts[1:])]
 route_metrics.append({'name':r['name'],'horizontal_length_m':horizontal,'surface_length_m':length,'start':pts[0],'end':pts[-1],'net_rise_m':pts[-1][2]-pts[0][2],'max_abs_longitudinal_grade':max(abs(v)for v in grades),'width_m':r['width'],'status':'terrain geometry measured; controller NOT TESTED'})
transforms=json.loads(s['source_context_transforms']);bad=[]
for name,values in transforms:
 o=bpy.data.objects.get(name)
 if not o or max(abs(a-b)for a,b in zip(values,[v for row in o.matrix_world for v in row]))>.00001:bad.append(name)
cameras=[]
for o in C['Cameras'].objects:
 if o.type!='CAMERA':continue
 cameras.append({'name':o.name,'game_position':[o.location.x+36,44-o.location.y,o.location.z+18.6],'native_position':list(o.location),'rotation_euler':list(o.rotation_euler),'lens_mm':o.data.lens,'horizontal_fov_deg':math.degrees(o.data.angle_x),'eye_above_support_m':o.get('eye_above_support'),'support_height_game':o.get('support_height_game'),'ortho_width_m':o.data.ortho_scale if o.data.type=='ORTHO' else None})
west_end=G(17.8,12.6)+.08
report={'phase':'R0-C1A DESIGN ONLY','mapping':'native (u,v,h)=(game x-36,44-game z,game y-18.6)','court':{'x':[20.5,28],'z':[4,14.4],'dimensions_m':[7.5,10.4],'area_m2':78,'finished_floor_y':21.8,'terrain_sample_count':len(ground),'terrain_min_y':min(ground),'terrain_max_y':max(ground),'floor_to_ground_min_m':21.8-max(ground),'floor_to_ground_max_m':21.8-min(ground)},'existing_forecourt':{'x':[28,44],'z':[8,14.2],'finished_floor_y':22.614,'area_m2':99.2,'modified':False},'north_gate':json.loads(s['north_gate']),'highland_gate':{'start':[20.5,12.6,21.8],'end':[17.8,12.6,west_end],'risers':9,'riser_m':(21.8-west_end)/9,'tread_m':.3,'nominal_width_m':2.6,'tested':False},'route_metrics':route_metrics,'geometry':{'collections':rows,'new_design_evaluated_triangles':new_tris,'new_design_materials':sorted(new_mats),'context_evaluated_triangles':context_tris,'browser_draw_calls':'NOT MEASURED: no runtime export or game integration','GLB_export_bytes':'NOT MEASURED: no new square GLB exported'},'context_preservation':{'objects_compared':len(transforms),'transform_differences':bad},'replanting_proposal':json.loads(s['replanting_proposal']),'cameras':cameras,'render':{'engine':s.render.engine,'samples':s.cycles.samples,'resolution':[s.render.resolution_x,s.render.resolution_y],'view_transform':s.view_settings.view_transform,'world_strength':.08,'sun_energy':3,'area_fill_watts':950},'approval':'Human approval pending before R0-C1B','playability':'All new routes NOT PLAYTESTED'}
s['measurement_report']=json.dumps(report);s['cameras']=json.dumps(cameras)
print(json.dumps(report))
