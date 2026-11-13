import bpy,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
s=bpy.context.scene;C={c.name.removeprefix('C1 / '):c for c in s.collection.children}
terrain=bpy.data.objects['C1 exact unchanged terrain reference'];bvh=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def G(x,z):return bvh.ray_cast(P(x,z,150),Vector((0,0,-1)))[0].z+18.6
# Ground clumps are wider than planter bays. Replant them at the retaining toe in this proposal, with original scale intact.
records=json.loads(s['replanting_proposal'])
for i,r in enumerate(records):
 o=bpy.data.objects[r['object']];x,z=17.0,4.8+2.2*i;o.matrix_world.translation=P(x,z,G(x,z)+.02);r['proposed_native']=list(o.matrix_world.translation);r['status']='isolated proposal: replant ground clump outside court, no scale change'
s['replanting_proposal']=json.dumps(records)
# Remove the wire-like veil. Water instead runs along the sculptural bronze leaves into a quiet pool.
for o in list(C['Fountain'].objects):
 if o.name.startswith('Light rain veil strand'):bpy.data.objects.remove(o,do_unlink=True)
water=bpy.data.materials['C1 / jade water'];centre=P(24,9,22.04);normal=Vector((.84,-.54,0));across=Vector((.54,.84,0))
for sign,height in[(-1,2.9),(1,3.65)]:
 vs=[]
 for i in range(25):
  t=i/24;mid=centre+across*(sign*(.08+.90*math.sin(t*math.pi/2)))+normal*(.22*math.sin(t*math.pi)+.045);mid.z+=height*t
  for e in[-1,1]:vs.append(tuple(mid+normal*.025*e))
 me=bpy.data.meshes.new('Rainwater on bronze leaf');me.from_pydata(vs,[],[(2*i,2*i+1,2*i+3,2*i+2)for i in range(24)]);me.materials.append(water);o=bpy.data.objects.new('Rainwater on bronze leaf',me);C['Fountain'].objects.link(o)
# Camera on the actual existing garden ramp center, 1.65 m above its interpolated support.
cam=bpy.data.objects['C1 Market-to-square eye 1.65m'];cam.location=P(31.4,6.7,22.332+1.65);cam.rotation_euler=(P(24,9,23.4)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=26
cam['support_height_game']=22.332;cam['eye_above_support']=1.65;cam['location_note']='Existing guarded garden ramp, market upper threshold to north landing'
cam=bpy.data.objects['C1 Square interior eye 1.65m'];cam.location=P(22.2,6.8,23.45);cam.rotation_euler=(P(25.2,10.8,23.5)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=24
cam['support_height_game']=21.8;cam['eye_above_support']=1.65
cam=bpy.data.objects['C1 Elevated composition'];cam.location=P(3,-13,44);cam.rotation_euler=(P(29,12,23)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=42
# Improve the plan crop and labels without changing geometry or hiding context.
cam=bpy.data.objects['C1 Measured top-down'];cam.location=P(23,5,100);cam.rotation_euler=(P(23,5,21)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=65
s['cameras']=json.dumps([{'name':o.name,'native_position':list(o.location),'game_position':[o.location.x+36,44-o.location.y,o.location.z+18.6],'rotation_euler':list(o.rotation_euler),'lens_mm':o.data.lens,'orthographic_width':o.data.ortho_scale if o.data.type=='ORTHO' else None,'eye_above_support':o.get('eye_above_support')}for o in C['Cameras'].objects if o.type=='CAMERA'])
s.render.resolution_percentage=67;s.camera=bpy.data.objects['C1 Market-to-square eye 1.65m'];s.render.filepath='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/town-square-r0c1a/pass4-arrival.png';bpy.ops.render.render(write_still=True)
print(s.render.filepath)
