import bpy,bmesh,math,json,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/town-square-c1b/'
s=bpy.context.scene
assert bpy.data.filepath==OUT+'town-square-export.blend'
# TERRAIN_UPDATES
terrain=bpy.data.objects['C1 exact unchanged terrain reference']
terrain.data=terrain.data.copy()
for row in terrain_updates:terrain.data.vertices[row[0]].co=row[1:]
terrain.data.update()
bv=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def ground(x,z):return bv.ray_cast(Vector((x-36,44-z,140)),Vector((0,0,-1)))[0].z+18.6
# Preserve every paver joint and top arris, remove the underside bevel rings only.
paver_before=0
for o in bpy.data.collections['C1 / Paving'].objects:
 if not o.name.startswith('Warm stone paver'):continue
 old=o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh();paver_before+=sum(len(p.vertices)-2 for p in old.polygons)
 vs=[v.co.copy() for v in o.data.vertices];lo=Vector(tuple(min(v[k] for v in vs) for k in range(3)));hi=Vector(tuple(max(v[k] for v in vs) for k in range(3)));be=.006
 pts=[]
 for z,inset in [(lo.z,0),(hi.z-be,0),(hi.z,be)]:
  pts.extend([(lo.x+inset,lo.y+inset,z),(hi.x-inset,lo.y+inset,z),(hi.x-inset,hi.y-inset,z),(lo.x+inset,hi.y-inset,z)])
 fs=[(3,2,1,0),(8,9,10,11)]
 for k in [0,4]:
  for i in range(4):j=(i+1)%4;fs.append((k+i,k+j,k+j+4,k+i+4))
 me=bpy.data.meshes.new('C1B optimized jointed paver');me.from_pydata(pts,[],fs);me.materials.append(o.data.materials[0]);o.data=me;o.modifiers.clear()
# Local field-fit: bow the civic walk west around the preserved market ramp rail.
# The old rail endpoint intersects the original walk centre at high frame rates.
def walk_shift(x,z):
 t=abs((z-.6)/3.4)
 return -.75*(1-t*t)**2*max(0,min(1,(34.5-x)/2)) if t<1 else 0
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith(('Approach ','Graded civic approach deck')):
  for v in o.data.vertices:
   p=o.matrix_world@v.co;v.co.x+=walk_shift(p.x+36,44-p.y)
# Ground only the existing toes/bearings; leave all finished-floor elevations unchanged.
resurvey=[]
for col in ['Supports','Proposed routes']:
 for o in bpy.data.collections['C1 / '+col].objects:
  if not o.name.startswith(('Terrain-scribed retaining','Approach stone shoe','Approach timber bearing')):continue
  old=[o.matrix_world@v.co for v in o.data.vertices];floor=min(p.z for p in old);changed=0
  for v in o.data.vertices:
   p=o.matrix_world@v.co
   if 'shoe' not in o.name and p.z>floor+.2:continue
   x,z,y=p.x+36,44-p.y,p.z+18.6;g=ground(x,z)
   target=(g-.15+(p.z-floor)) if 'shoe' in o.name else (g-.15 if 'retaining' in o.name else g+.16)
   if target>y:
    v.co.z+=target-y;changed+=1
  resurvey.append({'name':o.name,'toe_vertices_adjusted':changed})
# Refit the existing earth trail to the accepted surface; the old reference locally buries it by 0.21 m.
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith('Proposed natural trail'):
  for v in o.data.vertices:
   p=o.matrix_world@v.co;v.co.z+=ground(p.x+36,44-p.y)+.08-(p.z+18.6)
  bm=bmesh.new();bm.from_mesh(o.data);boundary=[e for e in bm.edges if e.is_boundary]
  for e in boundary:
   a,b=e.verts;low=[]
   for v in [a,b]:
    p=o.matrix_world@v.co;q=v.co.copy();q.z+=ground(p.x+36,44-p.y)-.03-(p.z+18.6);low.append(bm.verts.new(q))
   bm.faces.new([a,b,low[1],low[0]])
  bm.normal_update()
  for f in bm.faces:
   if f.normal.z<-.2:f.normal_flip()
  bm.to_mesh(o.data);bm.free()
# Correct inward winding on the closed authored stair/deck solids.
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith(('Landing approach stair','Highland gate step','Graded civic approach deck')):
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Batch the evaluated surfaces by compatible material and support purpose.
export_col=bpy.data.collections.new('C1B / Optimized export');s.collection.children.link(export_col)
batches={};colliders=[];cost={};dg=bpy.context.evaluated_depsgraph_get()
walk_prefix=('Telaga Awan structural paving bed','Warm stone paver','Graded civic approach deck','Landing approach stair','Highland gate step','Proposed natural trail')
for name in ['Paving','Supports','Fountain','Timber shade','Planting','Furniture','Proposed routes']:
 tris=0
 for o in bpy.data.collections['C1 / '+name].objects:
  if o.hide_render or o.type not in ['MESH','FONT','CURVE']:continue
  ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();tris+=len(me.loop_triangles)
  verts=[o.matrix_world@v.co for v in me.vertices]
  walking=o.name.startswith(walk_prefix)
  for tri in me.loop_triangles:
   m=me.materials[tri.material_index] if me.materials else None
   if not m:continue
   key=(m.name,walking);batch=batches.setdefault(key,{'verts':[],'faces':[],'smooth':[]})
   ix=len(batch['verts']);batch['verts'].extend([tuple(verts[i]) for i in tri.vertices]);batch['faces'].append((ix,ix+1,ix+2));batch['smooth'].append(me.polygons[tri.polygon_index].use_smooth)
  # Bound real rails/posts and furniture, never roofs or paving, for the existing collision system.
  solid=(('guard' in o.name or 'perimeter' in o.name or 'exposed-edge' in o.name) and ('post' in o.name or 'rail' in o.name or 'guard' in o.name)) or o.name.startswith(('Shade timber post','Planted seating-edge trough','Seat-end planted trough','Apron-facing stone seat plinth','Seat stone pier','Cafe chair','Square cafe table'))
  if solid:
   mn=[min(v[k]for v in verts)for k in range(3)];mx=[max(v[k]for v in verts)for k in range(3)]
   colliders.append({'x':36+(mn[0]+mx[0])/2,'z':44-(mn[1]+mx[1])/2,'w':mx[0]-mn[0],'d':mx[1]-mn[1],'minY':18.6+mn[2],'h':18.6+mx[2],'square':o.name})
   if ('rail' in o.name or 'continuous guard' in o.name) and len(verts)==8:
    aa=sum(verts[:4],Vector())/4;bb=sum(verts[4:],Vector())/4;dx=bb.x-aa.x;dz=aa.y-bb.y;l=math.hypot(dx,dz)
    if l>.1:colliders[-1]['oriented']={'w':l+.07,'d':.085,'rotation':-math.atan2(dz,dx)}
  ev.to_mesh_clear()
 cost[name]=tris
# A ring of compact existing-system colliders respects the round basin rather than a large square blocker.
for i in range(16):
 a=i*math.tau/16;colliders.append({'x':24+1.12*math.cos(a),'z':9+1.12*math.sin(a),'w':.56,'d':.56,'minY':21.8,'h':22.3,'square':'Fountain basin'})
for (mat,walking),b in batches.items():
 me=bpy.data.meshes.new('C1B / '+mat);me.from_pydata(b['verts'],[],b['faces']);me.materials.append(bpy.data.materials[mat]);me.update()
 for p,sm in zip(me.polygons,b['smooth']):p.use_smooth=sm
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bm.to_mesh(me);bm.free()
 o=bpy.data.objects.new(mat+(' / walking surface'if walking else' / static'),me);export_col.objects.link(o);o['walkable']=walking
 if any(x in mat for x in ['tropical leaf','jade water','soft water']):me.materials[0].use_backface_culling=False
manifest={'phase':'R0-C1B','mapping':'Blender (u,v,h)=(X-36,44-Z,Y-18.6), export Y-up then translate (36,18.6,44)','court_floor_y':21.8,'forecourt_floor_y':22.614,'cost':cost,'paver_before':paver_before,'paver_after':6000,'colliders':colliders,'support_resurvey':resurvey,'terrain_baseline':'accepted R0-C1A.5; 539 source vertices updated in derivative context only','routes':[{**r,'points':[(x+walk_shift(x,z),z,y) for x,z,y in r['points']]} if r['name'].startswith('Graded square') else r for r in json.loads(s['routes'])],'cameras':json.loads(s['cameras'])}
root=bpy.data.objects.new('Telaga Awan / export manifest',None);export_col.objects.link(root);root['square_manifest']=json.dumps(manifest)
for o in list(export_col.objects):
 if o!=root:o.parent=root
bpy.ops.object.select_all(action='DESELECT')
for o in export_col.objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(filepath=OUT+'town-square-optimized.glb',export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_cameras=False,export_lights=False)
# Keep modular editable collections and a separate optimized collection in the derivative.
export_col.hide_render=True;export_col.hide_viewport=True
s['c1b_manifest']=json.dumps(manifest)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'town-square-export.blend')
print(json.dumps({'cost':cost,'batches':len(batches),'colliders':len(colliders),'paver_before':paver_before,'file':OUT+'town-square-optimized.glb'}))
