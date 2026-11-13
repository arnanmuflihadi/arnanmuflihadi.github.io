import bpy,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;c=bpy.data.collections['C1 / Proposed routes'];t=bpy.data.objects['C1 exact unchanged terrain reference'];bv=BVHTree.FromPolygons([t.matrix_world@v.co for v in t.data.vertices],[list(p.vertices)for p in t.data.polygons])
def G(x,z):return bv.ray_cast(Vector((x-36,44-z,140)),Vector((0,0,-1)))[0].z+18.6
def lift(x,z):return .08*max(0,min(1,((x-31)*3.5+(z+1.6)*(-.2))/(3.5*3.5+.2*.2)))
for o in c.objects:
 if o.name.startswith('Landing approach stair'):
  for v in list(o.data.vertices)[4:]:v.co.z+=.08
 elif o.name.startswith(('Approach ','Graded civic approach deck')):
  verts=list(o.data.vertices);bottom=None
  if o.name.startswith(('Approach stone shoe','Approach timber bearing')):bottom=min(v.co.z for v in verts)+.001
  for v in verts:
   if bottom is not None and v.co.z<=bottom:continue
   v.co.z+=lift(v.co.x+36,44-v.co.y)
 elif o.name.startswith('Landing stair guard'):
  for v in o.data.vertices:
   x,z=v.co.x+36,44-v.co.y;t0=((x-36)*(-1.5)+z*(-1.8))/(1.5*1.5+1.8*1.8);v.co.z+=.08*max(0,min(1,t0))
a=Vector((36,0));b=Vector((34.5,-1.8));forward=(b-a).normalized();side=Vector((-forward.y,forward.x));tread=(b-a).length/9;bottom=20.754735;oldrise=(22.45-bottom)/9;newfirst=(oldrise+.08)/2;cen=a-forward*tread/2;vs=[]
for upper in[False,True]:
 for along,across in[(-1,-1),(1,-1),(1,1),(-1,1)]:
  xz=cen+forward*(along*tread/2)+side*(across*1.3);y=bottom+newfirst if upper else G(xz.x,xz.y)-.15;vs.append((xz.x-36,44-xz.y,y-18.6))
me=bpy.data.meshes.new('Shallow landing threshold tread');me.from_pydata(vs,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.materials.append(bpy.data.materials['C1 / warm limestone']);o=bpy.data.objects.new('Landing approach stair - shallow first tread',me);c.objects.link(o)
routes=json.loads(s['routes'])
for r in routes:
 if r['name'].startswith('Graded square'):r['points']=[(x,z,y+lift(x,z))for x,z,y in r['points']]
s['routes']=json.dumps(routes);gate=json.loads(s['north_gate']);gate['end'][-1]=22.53;s['north_gate']=json.dumps(gate)
start=a-forward*tread;s['landing_stair']=json.dumps({'start':[start.x,start.y,bottom],'end':[34.5,-1.8,22.53],'risers':10,'risers_m':[newfirst,newfirst]+[oldrise]*8,'max_riser_m':oldrise,'min_riser_m':newfirst,'tread_m':tread,'width':2.6,'tested':False})
contacts=json.loads(s['approach_ground_contacts'])
for p in contacts:p['deck_y']+=lift(p['x'],p['z']);p['exposure_m']=p['deck_y']-p['ground_y']
s['approach_ground_contacts']=json.dumps(contacts)
for o in bpy.data.collections['C1 / Plan annotations'].objects:
 if o.type=='FONT' and o.name.startswith('Landing stair dimension'):o.data.body='10 RISERS 0.134-0.188 m / min 2.41 m clear'
s['arrival_correction']='Protected market stair/garden ramp -> unchanged north landing -> ten proposed shallow risers -> terrain-supported civic walk -> court. Existing geometry and furniture untouched. New route NOT PLAYTESTED.'
s.camera=bpy.data.objects['C1 Elevated composition'];s.render.filepath='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/town-square-r0c1a/03-elevated.png';bpy.ops.render.render(write_still=True)
print(s.render.filepath)
