import bpy,math,json
from mathutils import Vector
s=bpy.context.scene
# Small planter is moved outside the entrance aperture; mature island trees stay untouched.
for n in ['Guild / terrace planted seat-edge','Guild / terrace planter soil']:
 o=bpy.data.objects[n];ys=[v.co.y for v in o.data.vertices];xs=[v.co.x for v in o.data.vertices];lo=min(xs);hi=max(xs)
 for v in o.data.vertices:v.co.x=(37.55-36)+(v.co.x-lo)/(hi-lo)*.58
# Relocate the human reference to the unobstructed east side of the doorway.
for o in bpy.data.collections['C2A / Scale and cameras'].objects:
 if o.type=='MESH':o.matrix_world.translation+=Vector((2.45,0,0))
# Replace the exposed ladder-like stem with a ventilated plaster-and-timber lantern base.
for o in list(bpy.data.collections['C2A / Roof and lantern'].objects):
 if any(k in o.name for k in ['lantern ventilation','lantern blue','lantern lower','lantern crown','survey finial','octagonal lantern ring','lantern vertical']):bpy.data.objects.remove(o,do_unlink=True)
# Helpers from design.py are already live in this MCP session; no approved file is rerun.
cx,cz=40.1,-7.2
for i in range(8):
 a=i*math.tau/8;b=(i+1)*math.tau/8;r=.86
 vs=[P(cx+r*math.cos(t),cz+r*math.sin(t),y)for y in[30.3,36.4]for t in[a,b]]
 mesh('lantern plaster shaft',vs,[(0,1,3,2)],sage,'Roof and lantern')
 beam('lantern shaft timber',(cx+r*math.cos(a),cz+r*math.sin(a),30.2),(cx+r*math.cos(a),cz+r*math.sin(a),36.4),.10,.10,timber,'Roof and lantern')
 # One narrow ventilation strip per side, rather than many open rungs.
 for h in[33.0,33.2,33.4]:beam('lantern shaft vent',(cx+(r+.02)*math.cos(a+.12),cz+(r+.02)*math.sin(a+.12),h),(cx+(r+.02)*math.cos(b-.12),cz+(r+.02)*math.sin(b-.12),h),.06,.08,metal,'Roof and lantern')
for level,r in[(36.35,1.62),(38.35,1.62)]:
 for i in range(8):
  a=i*math.tau/8;b=(i+1)*math.tau/8
  beam('observation lantern rim',(cx+r*math.cos(a),cz+r*math.sin(a),level),(cx+r*math.cos(b),cz+r*math.sin(b),level),.15,.16,edge,'Roof and lantern')
for i in range(8):
 a=i*math.tau/8;b=(i+1)*math.tau/8;r=1.57
 beam('observation lantern mullion',(cx+r*math.cos(a),cz+r*math.sin(a),36.35),(cx+r*math.cos(a),cz+r*math.sin(a),38.35),.13,.13,timber,'Roof and lantern')
 mesh('observation lantern glass',[P(cx+r*math.cos(t),cz+r*math.sin(t),y)for y in[36.45,38.25]for t in[a,b]],[(0,1,3,2)],glass,'Roof and lantern')
for name,r0,r1,y0,y1 in[('observation limasan crown',2.12,.45,38.48,40.0),('observation upper cap',.91,.05,40.15,40.75)]:
 vs=[P(cx+r*math.cos(i*math.tau/8),cz+r*math.sin(i*math.tau/8),y)for r,y in[(r0,y0),(r1,y1)]for i in range(8)]
 o=mesh(name,vs,[(i,(i+1)%8,(i+1)%8+8,i+8)for i in range(8)],roof[2],'Roof and lantern');o.modifiers.new('Roof thickness','SOLIDIFY').thickness=.08
 for i in range(8):beam(name+' fascia',(cx+r0*math.cos(i*math.tau/8),cz+r0*math.sin(i*math.tau/8),y0),(cx+r0*math.cos((i+1)*math.tau/8),cz+r0*math.sin((i+1)*math.tau/8),y0),.09,.14,edge,'Roof and lantern')
beam('survey finial',(cx,cz,40.7),(cx,cz,41.15),.055,.055,bronze,'Roof and lantern')
# Sweeping civic entrance canopy with actual curved timber trusses and glazed fanlight.
for o in list(bpy.data.collections['C2A / Timber and glazing'].objects):
 if any(k in o.name for k in ['entry brow front','cantilevered entrance rafter']):bpy.data.objects.remove(o,do_unlink=True)
for o in list(bpy.data.collections['C2A / Roof and lantern'].objects):
 if 'entrance brow terracotta'in o.name:bpy.data.objects.remove(o,do_unlink=True)
# Roof spans only the crown gap in front of the existing mature trees.
x0,x1=36.5,42.3;mid=39.4
for side in[-1,1]:
 vs=[];fs=[]
 for j in range(17):
  t=j/16;x=mid+side*2.9*t;h=32.7-3.0*(t**.68)
  for z in[-5.45,-7.9]:vs.append(P(x,z,h+(.12 if z==-5.45 else 0)))
 for j in range(16):fs.append((2*j,2*j+2,2*j+3,2*j+1))
 o=mesh('sweeping terracotta entrance roof',vs,fs,roof[side+2],'Roof and lantern');o.modifiers.new('Editable canopy shell','SOLIDIFY').thickness=.075
 for z in[-5.48,-6.4,-7.85]:
  for j in range(16):
   t=j/16;u=(j+1)/16;x=mid+side*2.9*t;xx=mid+side*2.9*u;h=32.55-3*(t**.68);hh=32.55-3*(u**.68)
   beam('curved portal timber truss',(x,z,h),(xx,z,hh),.12,.18,timber,'Timber and glazing')
 for j in range(1,9):
  t=j/9;x=mid+side*2.9*t;h=32.7-3*t**.68+.045
  beam('canopy tile seam',(x,-5.43,h+.12),(x,-7.92,h),.025,.025,roof[j%5],'Roof and lantern')
# A real fanlight, radial timber ribs and a restrained research compass.
points=[P(mid-2.7,-6.44,29.55),P(mid+2.7,-6.44,29.55)]
for j in range(17):
 t=1-j/8;x=mid+2.7*t;h=32.5-2.8*abs(t)**.68;points.append(P(x,-6.44,h))
mesh('arched research-hall fanlight',points,[tuple(range(len(points)))],glass,'Timber and glazing')
for t in[-.85,-.55,-.28,0,.28,.55,.85]:beam('fanlight radial timber',(mid,-6.37,29.55),(mid+2.65*t,-6.37,32.45-2.8*abs(t)**.68),.065,.09,edge,'Timber and glazing')
for x in[36.55,42.25]:beam('tall portal pier',(x,-6.45,25.5),(x,-6.45,29.85),.20,.22,timber,'Timber and glazing')
# Stone banding belongs to the supporting plinth, not decorative floating boxes.
for yy in[23.6,24.2,24.8]:
 for x in[36+i*.45 for i in range(18)]:
  if G(x,-6.78)+.1<yy:box('scribed plinth joint',x,-6.665,yy,.012,.012,min(.45,yy-G(x,-6.78)),sand,'Site and approach')
# Render-only context material clones retain native vegetation geometry and transforms.
clones={}
for o in bpy.data.collections['C1 / Context - existing island plants'].objects:
 if ' / tree / 'not in o.name or o.type!='MESH':continue
 for slot in o.material_slots:
  original=slot.material
  if not original:continue
  k=original.name
  if k not in clones:
   m=original.copy();m.name='C2A context / '+k
   if m.use_nodes:
    bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if bs:
     for link in list(m.node_tree.links):
      if link.to_node==bs and link.to_socket==bs.inputs['Base Color']:m.node_tree.links.remove(link)
     c=(.18,.30,.075,1)if any(w in k.lower()for w in['leaf','foliage','green','canopy'])else(.18,.27,.075,1)
     bs.inputs['Base Color'].default_value=c;bs.inputs['Roughness'].default_value=.9
   clones[k]=m
  slot.material=clones[k]
# Broaden the native square camera enough to include the entire revised crown.
s.camera=bpy.data.objects['C2A 01 Guild from Telaga Awan'];s.camera.data.lens=28
s.camera.rotation_euler=(P(39.8,-7.5,29.8)-s.camera.location).to_track_quat('-Z','Y').to_euler()
d=json.loads(s['c2a_design']);d['lantern_top']=41.15;d['concept_corrections']=['curved civic portal and fanlight','integrated plaster observation lantern','planter clear of the door'];d['context_materials']='isolated render-only tree material clones; geometry and tree positions unchanged';s['c2a_design']=json.dumps(d)
s.render.filepath=OUT+'pass2-square.png';s.render.resolution_x=1200;s.render.resolution_y=800;s.cycles.samples=24
bpy.ops.wm.save_as_mainfile(filepath=OUT+'atlas-guild-design.blend');bpy.ops.render.render(write_still=True)
print(s.render.filepath)
