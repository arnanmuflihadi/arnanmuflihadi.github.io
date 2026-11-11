import bpy,bmesh,math,json,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/circulation-c1c/'
s=bpy.context.scene
assert bpy.data.filepath==OUT+'circulation-design.blend'
# BASE_SITE
context=bpy.data.collections['C1 / Context - approved market']
terrain=bpy.data.objects['C1 exact unchanged terrain reference']
bv=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices)for p in terrain.data.polygons])
def G(x,z):return bv.ray_cast(Vector((x-36,44-z,130)),Vector((0,0,-1)))[0].z+18.6
def P(x,z,y):return Vector((x-36,44-z,y-18.6))
def base(o):return o.get('approved_source',o.name).split('.')[0]
common_prefix=('Street support','Street transverse support','Stair stringer','Natural approach stair','Provisional skyport threshold','Arrival bridge','Garden path visible','Market entrance seam','Square threshold stair','Square stair-ramp','Square garden ramp','Square ground tie','Market edge','Arrival approach','Bridge guard','Garden path guard','Square stair','Square ramp','Market arrival return','Provisional landing','Square edge','Garden path terrain','Garden path timber','Garden path bearing','Garden path support','Original planting support socket','Planting soil cap')
common=[o for o in context.objects if base(o).startswith(common_prefix)]
remove_common=('Natural approach stair','Provisional skyport threshold','Arrival bridge','Bridge guard','Arrival approach','Provisional landing','Square stair-ramp','Square garden ramp','Square ramp')
old_common=[o for o in common if base(o).startswith(remove_common)]
bench=[]
# Select the nine pieces of the obstructing bench by actual bounds, not a global prop group.
for o in context.objects:
 if o.type!='MESH' or not base(o).startswith(('Bench timber','Bench frame','Bench back frame')):continue
 vs=[o.matrix_world@Vector(v)for v in o.bound_box];cx=sum(p.x for p in vs)/8+36;cz=44-sum(p.y for p in vs)/8
 if 28.8<cx<29.6 and 11.5<cz<14:bench.append(o)
markers=[o for o in context.objects if base(o).startswith(('Square direction marker','Square direction heading'))]
changed_context=set(common+bench+markers)
def signature(o):return (tuple(v for row in o.matrix_world for v in row),tuple(tuple(v.co)for v in o.data.vertices) if o.type=='MESH'else None)
protected={o.name:signature(o)for o in context.objects if o not in changed_context and o.type=='MESH'}
protected_art={o.name:signature(o)for n in ['Fountain','Timber shade'] for o in bpy.data.collections['C1 / '+n].objects if o.type=='MESH'}
cols={}
for name in ['Direct civic connections','Arrival transition','Relocated furniture','Export interfaces','Export square']:
 c=bpy.data.collections.new('C1C / '+name);s.collection.children.link(c);cols[name]=c
stone=bpy.data.materials['C1 / warm volcanic stone'];sand=bpy.data.materials['C1 / warm limestone'];clay=bpy.data.materials['C1 / terracotta'];wood=bpy.data.materials['C1 / oiled timber'];metal=bpy.data.materials['C1 / deep green metal'];earth=bpy.data.materials['C1 / compacted highland earth']
def mesh(name,vs,fs,mat,col,walking=False):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update();o=bpy.data.objects.new(name,me);cols[col].objects.link(o);o['walkable']=walking;o['c1c_status']='added';return o
def box(name,x,z,top,w,d,bottom,mat,col,walking=False):
 a,b=w/2,d/2;vs=[tuple(P(x+sx*a,z+sz*b,y))for y in[bottom,top]for sz in[-1,1]for sx in[-1,1]]
 o=mesh(name,vs,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],mat,col,walking)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();return o
def beam(name,a,b,w,d,mat,col):
 a,b=P(*a),P(*b);up=(b-a).normalized();side=up.cross(Vector((0,1,0)))
 if side.length<.001:side=up.cross(Vector((1,0,0)))
 side.normalize();other=up.cross(side).normalized();vs=[tuple(p+side*i*w/2+other*j*d/2)for p in[a,b]for i,j in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 o=mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,col);o['collision']=True
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();return o
def guard(a,b,name,col):
 n=max(1,math.ceil(math.dist(a[:2],b[:2])/1.8))
 for i in range(n+1):
  p=tuple(a[k]+(b[k]-a[k])*i/n for k in range(3));beam(name+' post',p,(p[0],p[1],p[2]+1.02),.06,.06,metal,col)
 for h in[.52,1.02]:beam(name+' rail',(a[0],a[1],a[2]+h),(b[0],b[1],b[2]+h),.065,.075,wood if h>1 else metal,col)
def flight(name,a,b,ya,yb,width,count,col):
 # Every tread is a real closed stone solid with terrain-scribed lower corners.
 dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);tx,tz=dx/l,dz/l;nx,nz=-tz,tx
 for i in range(count):
  v=[];top=ya+(yb-ya)*(i+1)/count
  if yb<ya:top=ya+(yb-ya)*i/count
  for upper in[False,True]:
   for t,sign in[(i/count,-1),((i+1)/count,-1),((i+1)/count,1),(i/count,1)]:
    t=t-.4/l if name=='Guild garden gate' and i==0 and t==0 else t
    x=a[0]+dx*t+nx*width*.5*sign;z=a[1]+dz*t+nz*width*.5*sign;v.append(tuple(P(x,z,(top+.003 if name=='Guild garden gate' and i==0 else top) if upper else min(G(x,z)-.1,top-.15))))
  o=mesh(name+' tread',v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],sand,col,True)
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for sign in[-1,1]:
  t=2/count if name=='Market trail gateway' else 0;aa=(a[0]+dx*t,a[1]+dz*t,ya+(yb-ya)*t)
  guard((aa[0]+nx*(width/2-.06)*sign,aa[1]+nz*(width/2-.06)*sign,aa[2]),(b[0]+nx*(width/2-.06)*sign,b[1]+nz*(width/2-.06)*sign,yb),name+' handrail',col)
 return {'start':[*a,ya],'end':[*b,yb],'risers':count,'riser':abs(ya-yb)/count,'run':l,'width':width}
def ribbon(name,points,width,col,material=earth):
 dense=[]
 for a,b in zip(points,points[1:]):
  n=max(1,math.ceil(math.dist(a[:2],b[:2])/.4))
  for j in range(n):
   t=j/n;x=a[0]+(b[0]-a[0])*t;z=a[1]+(b[1]-a[1])*t;dense.append((x,z,a,b,t))
 dense.append((points[-1][0],points[-1][1],points[-2],points[-1],1))
 vs=[];across=6
 for i,(x,z,a,b,t)in enumerate(dense):
  dx,dz=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dz);nx,nz=-dz/l,dx/l
  for j in range(across+1):
   side=j/across-.5;xx,zz=x+nx*width*side,z+nz*width*side
   ga=G(a[0]+nx*width*side,a[1]+nz*width*side)+.025;gb=G(b[0]+nx*width*side,b[1]+nz*width*side)+.025
   yy=G(xx,zz)+.025 if a[2] is None and b[2] is None else (a[2] if a[2] is not None else ga)*(1-t)+(b[2] if b[2] is not None else gb)*t
   vs.append(tuple(P(xx,zz,yy)))
 fs=[]
 for i in range(len(dense)-1):
  for j in range(across):k=i*(across+1)+j;fs.append((k,k+across+1,k+across+2,k+1))
 o=mesh(name,vs,fs,material,col,True);bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update()
 for f in bm.faces:
  if f.normal.z<0:f.normal_flip()
 boundary=[e for e in bm.edges if e.is_boundary]
 for e in boundary:
  a,b=e.verts;low=[]
  for v in[a,b]:p=v.co;q=p.copy();q.z=G(p.x+36,44-p.y)-18.6-.04;low.append(bm.verts.new(q))
  bm.faces.new([a,b,low[1],low[0]])
 bm.to_mesh(o.data);bm.free();return o
# Snapshot exact existing public hardware for the scaled before/after plan.
def plan_item(o,status):
 if o.type!='MESH':return None
 vs=[o.matrix_world@v.co for v in o.data.vertices];xs=[p.x+36 for p in vs];zs=[44-p.y for p in vs];ys=[p.z+18.6 for p in vs]
 return {'name':base(o),'status':status,'bounds':[min(xs),max(xs),min(zs),max(zs)],'height':[min(ys),max(ys)],'kind':'rail'if any(k in base(o).lower()for k in ['guard','handrail','perimeter rail','perimeter post'])else 'stair'if any(k in base(o).lower()for k in ['stair','step'])else 'walk'}
before=[plan_item(o,'existing')for o in common if any(k in base(o).lower()for k in ['guard','handrail','stair','ramp','bridge','landing'])]
before+=[plan_item(o,'existing')for o in bpy.data.collections['C1 / Proposed routes'].objects]
# Remove the redundant upper-to-lower detour and garden ramp, leaving the Guild-facing north stair.
removed=[]
for o in old_common:o.hide_render=True;o.hide_set(True);o['c1c_status']='removed';removed.append(base(o))
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith(('Graded civic','Approach ','Landing approach','Landing stair','Proposed natural trail')):o.hide_render=True;o.hide_set(True);o['c1c_status']='removed';removed.append(o.name)
for n in ['Furniture','Planting']:
 for o in bpy.data.collections['C1 / '+n].objects:
  if o.name.startswith(('Apron-facing','Seat-end')):o.hide_render=True;o.hide_set(True);o['c1c_status']='removed';removed.append(o.name)
# Relocate only the obstructing source bench; preserve the approved GLB via a runtime triangle subset.
mask_volumes=[]
marker_points=[o.matrix_world@Vector(v) for o in markers for v in o.bound_box];marker_centre=sum(marker_points,Vector())/len(marker_points);marker_delta=P(30.3,13.95,23)-marker_centre
for o in bench+markers:
 vs=[o.matrix_world@Vector(v)for v in o.bound_box];mask_volumes.append({'source':base(o),'min':[min(v.x for v in vs)+36,min(v.z for v in vs)+18.6,44-max(v.y for v in vs)],'max':[max(v.x for v in vs)+36,max(v.z for v in vs)+18.6,44-min(v.y for v in vs)]})
 old=o.matrix_world.copy();o.data=o.data.copy();o.matrix_world.translation+=Vector((13,-(-1.8),0))if o in bench else Vector((0,0,0));o['c1c_status']='relocated'
 if o in markers:
  o.matrix_world.translation+=Vector((marker_delta.x,marker_delta.y,0))
  if o.type=='FONT':o.data.body='TELAGA AWAN  <'
# Remove only the old east-court railing at the direct opening; its southern guard stays.
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith('Court perimeter'):
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  if min(p.x+36 for p in vs)>27.7 and max(44-p.y for p in vs)>10.7:o.hide_render=True;o.hide_set(True);o['c1c_status']='removed'
# Trim the southern perimeter to meet the new stair cheek without doubled rails.
for o in bpy.data.collections['C1 / Proposed routes'].objects:
 if o.name.startswith('Court perimeter') and not o.hide_render:
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  if min(44-p.y for p in vs)>14.2:
   if min(p.x+36 for p in vs)>26.4:o.hide_render=True;o.hide_set(True);o['c1c_status']='removed'
   else:
    for v in o.data.vertices:
     if v.co.x+36>26.4:v.co.x=26.4-36
# Compact direct five-riser stair: 0.814 m level change, aligned on the two public floors.
portal=flight('Direct Telaga stair',(28.02,12.6),(26.4,12.6),22.614,21.8,2.8,5,'Direct civic connections')
# Close the short southern cheek where the court's old perimeter ended at the stair.
guard((26.4,14.35,21.8),(28,14.35,22.614),'Direct stair south closure','Direct civic connections')
guard((27.85,4.9,21.8),(27.85,8.08,21.8),'Court exposed north-east edge','Direct civic connections')
# One calm forecourt guard replaces the former ramp junction, not another elevated loop.
guard((28.1,8.08,22.614),(33.75,8.08,22.614),'Forecourt north edge','Direct civic connections')
guard((28.08,8.08,22.614),(28.08,11.12,22.614),'Forecourt west cheek','Direct civic connections')
# A ground-based Guild-facing exit replaces the raised C1B civic walk.
guild_bottom=max(G(28.3,2.6),G(28.3,5),G(28.3,3.8))+.035
exit_flight=flight('Guild garden gate',(26.6,4),(28.3,3.8),21.8,guild_bottom,2.4,4,'Direct civic connections')
ribbon('Guild gate gravel fan',[(28.3,3.8,guild_bottom),(29.8,3,None)],2.4,'Direct civic connections',sand)
points=[(29.8,3,None),(31,1.5,None),(33,.5,None),(36,0,None),(40,-4,None),(44,-8,None)]
ribbon('Guild reservation ground path',points,2.4,'Direct civic connections')
# Match the original highland/clearing trail; remove the parallel C1B dirt ribbon.
ribbon('Highland existing-trail tie',[(17.8,12.6,20.7815),(16.7,12.3,None),(15.8,12,None)],2.4,'Direct civic connections',sand)
# Arrival now follows the existing dirt trail, without the southern 13-step/bridge detour.
arrival=flight('Market trail gateway',(26,52),(30.15,51.8),G(26,52)+.025,17.444,3,6,'Arrival transition')
ribbon('Market trail gravel fan',[(26.2,54,None),(26.1,53,None),(26,52,G(26,52)+.025)],3,'Arrival transition',sand)
# Protect exact architectural mesh data and transforms in the native derivative.
for name,value in protected.items():assert signature(bpy.data.objects[name])==value,name
for name,value in protected_art.items():assert signature(bpy.data.objects[name])==value,name
s['c1c_protected_check']=json.dumps({'context_meshes':len(protected),'fountain_pavilion_meshes':len(protected_art),'changes':[]})
s['c1c_data']=json.dumps({'before':before,'removed_names':removed,'market_mask_volumes':mask_volumes,'portal':portal,'guild_gate':exit_flight,'arrival':arrival,'protected':json.loads(s['c1c_protected_check'])})
bpy.ops.wm.save_as_mainfile(filepath=OUT+'circulation-design.blend')
print(json.dumps({'common':len(common),'removed_common':len(old_common),'bench_pieces':len(bench),'portal':portal,'guild_gate':exit_flight,'arrival':arrival,'protected':json.loads(s['c1c_protected_check'])}))
