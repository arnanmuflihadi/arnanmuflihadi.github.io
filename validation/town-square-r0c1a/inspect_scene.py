import bpy,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;report=json.loads(s['measurement_report']);t=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([t.matrix_world@v.co for v in t.data.vertices],[list(p.vertices)for p in t.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bv.ray_cast(P(x,z,150),Vector((0,0,-1)))[0].z+18.6
# All deck edge vertices, not just the bearing grid, are checked against the exact terrain.
o=bpy.data.objects['Graded civic approach deck'];vs=list(o.data.vertices);edge_exposures=[v.co.z+18.6-G(v.co.x+36,44-v.co.y)for v in vs[len(vs)//2:]]
stair_clearances=[]
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith('Landing approach stair'):
  stair_clearances.extend(v.co.z+18.6-G(v.co.x+36,44-v.co.y)for v in list(o.data.vertices)[4:])
# Actual guard-face rays measure clear width at 0.70 m above each deck cross-section.
route=next(r for r in json.loads(s['routes'])if r['name'].startswith('Graded square'))
guards=[o for o in bpy.data.collections['C1 / Proposed routes'].objects if o.name.startswith(('Approach continuous guard','Approach guard post'))];widths=[]
for i,p in enumerate(route['points'][1:-1],1):
 a=route['points'][i-1];b=route['points'][i+1];d=Vector((b[0]-a[0],0,-(b[1]-a[1]))).normalized();side=Vector((-d.z,d.x,0));side=Vector((-(b[1]-a[1]),-(b[0]-a[0]),0)).normalized();origin=P(p[0],p[1],p[2]+.7);near=[]
 for sign in[-1,1]:
  direction=side*sign;hits=[]
  for ob in guards:
   inv=ob.matrix_world.inverted();hit=ob.ray_cast(inv@origin,(inv.to_3x3()@direction).normalized())
   if hit[0]:
    dist=(ob.matrix_world@hit[1]-origin).length
    if .01<dist<3:hits.append(dist)
  near.append(min(hits)if hits else None)
 if all(x is not None for x in near):widths.append(sum(near))
# Reserve a view toward a hypothetical Guild upper-level target. No Guild mass is authored.
origin=P(26.4,6,23.45);target=P(44,-8,G(44,-8)+5);direction=(target-origin).normalized();length=(target-origin).length;blocked=[]
for c in s.collection.children:
 if c.name in['C1 / Cameras','C1 / Plan annotations','C1 / Scale reference']:continue
 for ob in c.objects:
  if ob.type!='MESH' or ob.hide_render:continue
  inv=ob.matrix_world.inverted();hit=ob.ray_cast(inv@origin,(inv.to_3x3()@direction).normalized())
  if hit[0]:
   d=(ob.matrix_world@hit[1]-origin).length
   if .02<d<length-.1:blocked.append({'name':ob.name,'distance_m':d})
headers=[v.co.z+o.location.z+18.6-21.8 for o in bpy.data.collections['C1 / Timber shade'].objects if o.name.startswith(('Shade header','Shade side beam'))for v in o.data.vertices]
report['detailed_checks']={'deck_edge_floor_to_ground_min_m':min(edge_exposures),'deck_edge_floor_to_ground_max_m':max(edge_exposures),'deck_edge_vertices_checked':len(edge_exposures),'landing_stair_top_to_terrain_min_m':min(stair_clearances),'landing_stair_top_corners_checked':len(stair_clearances),'guard_clear_width_sample_count':len(widths),'minimum_guard_face_clear_width_m':min(widths)if widths else None,'shade_header_clearance_m':min(headers),'guild_planning_ray':{'from_game':[26.4,6,23.45],'target_game':[44,-8,G(44,-8)+5],'target_note':'hypothetical upper-level target 5 m above actual ground; Guild unbuilt','mesh_intersections':blocked,'not_a_full_vista_or_gameplay_test':True},'packed_source_images':[{'name':i.name,'size':list(i.size),'packed':i.packed_file is not None}for i in bpy.data.images if i.type=='IMAGE' and i.source!='GENERATED']}
# Fit plan backing plates to actual glyph bounds, including the second line below the baseline.
pc=bpy.data.collections['C1 / Plan annotations'];texts=[o for o in pc.objects if o.type=='FONT'];plates=[o for o in pc.objects if o.name.startswith('Plan label backing')]
bpy.context.view_layer.update()
for text,plate in zip(texts,plates):
 b=[text.matrix_world@Vector(v)for v in text.bound_box];x0=min(v.x for v in b)-.22;x1=max(v.x for v in b)+.22;y0=min(v.y for v in b)-.16;y1=max(v.y for v in b)+.16;z=text.location.z-.035
 for v,co in zip(plate.data.vertices,[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)]):v.co=co
s['measurement_report']=json.dumps(report)
print('C1_JSON_BEGIN'+json.dumps(report)+'C1_JSON_END')
