import bpy,bmesh,math,json,collections
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/circulation-c1c/'
s=bpy.context.scene;data=json.loads(s['c1c_data']);context=bpy.data.collections['C1 / Context - approved market']
def base(o):return o.get('approved_source',o.name).split('.')[0]
common_prefix=('Street support','Street transverse support','Stair stringer','Natural approach stair','Provisional skyport threshold','Arrival bridge','Garden path visible','Market entrance seam','Square threshold stair','Square stair-ramp','Square garden ramp','Square ground tie','Market edge','Arrival approach','Bridge guard','Garden path guard','Square stair guard','Square stair terrain','Square stair timber','Square stair bearing','Square stair support','Square ramp','Market arrival return','Provisional landing','Square edge','Garden path terrain','Garden path timber','Garden path bearing','Garden path support','Original planting support socket','Planting soil cap')
common=[o for o in context.objects if base(o).startswith(common_prefix)]
bench_names=[r['source'] for r in data['market_mask_volumes']]
props=[o for o in context.objects if o.get('c1c_status')=='relocated']
newc=[o for o in bpy.data.collections['C1C / Direct civic connections'].objects if not o.hide_render]
arrival=[o for o in bpy.data.collections['C1C / Arrival transition'].objects if not o.hide_render]
# Guild paving belongs to the square; forecourt guards belong to the common interface.
interface_extra=[o for o in newc if o.name.startswith('Forecourt')]
square_extra=[o for o in newc if o not in interface_extra]
interface_objects=[o for o in common if not o.hide_render]+arrival+props+interface_extra
square_objects=[o for n in ['Paving','Supports','Fountain','Timber shade','Planting','Furniture','Proposed routes']for o in bpy.data.collections['C1 / '+n].objects if not o.hide_render]+square_extra

def bounds_item(o):
 if o.type not in ['MESH','FONT','CURVE']:return None
 vs=[o.matrix_world@Vector(v)for v in o.bound_box];xs=[v.x+36 for v in vs];zs=[44-v.y for v in vs];ys=[v.z+18.6 for v in vs];name=base(o)
 return {'name':name,'status':o.get('c1c_status','retained'),'bounds':[min(xs),max(xs),min(zs),max(zs)],'height':[min(ys),max(ys)],'kind':'rail'if any(k in name.lower()for k in ['guard','handrail','perimeter rail','perimeter post','cheek','closure'])else 'stair'if any(k in name.lower()for k in ['stair','step'])else 'walk'}
after=[bounds_item(o)for o in interface_objects+square_objects if o.type=='MESH' and any(k in base(o).lower()for k in ['guard','rail','stair','step','ramp','bridge','landing','gate','gravel','path'])]
network={**data,'after':after,'beforeRoutes':{'arrival':[[27,57],[24,66],[27,61.8],[27,60],[30,52],[36,44]],'market':[[36,44],[36,35],[36,17],[35,12.6]],'court':[[35,12.6],[36,9],[36,0],[36.16,.2],[34.5,-1.8],[30.75,-1.6],[27.81,2.4],[26.6,4],[26.2,12.6]],'highland':[[26.2,12.6],[20.5,12.6],[17.8,12.6],[12,11],[4,8],[-5,5]]},'afterRoutes':{'arrival':[[27,57],[26.2,54],[25.1,52.7],[25.1,52],[26,52],[28.75,51.86747],[30.15,51.8],[36,44]],'market':[[36,44],[36,35],[36,27],[36,17],[35,12.6]],'court':[[35,12.6],[30,12.6],[28.02,12.6],[26.4,12.6],[26.2,12.6]],'highland':[[26.2,12.6],[20.5,12.6],[17.8,12.6],[16,12],[3,12],[-5,5]],'guild':[[26.2,12.6],[25.9,12.6],[25.9,6],[25.9,4.6],[26.6,4],[28.3,3.8],[29.8,3],[31,1.5],[33,.5],[36,0],[40,-4],[44,-8]],'optionalReturn':[[36,0],[36,9],[35,12.6]]},'nodes':{'Arrival':[27,57],'Market Street':[36,30],'Forecourt':[35,12.6],'Telaga Awan':[24,9],'Highland junction':[-5,5],'Guild boundary':[44,-8]},'source':'R0-C1B plus S2-E exact native circulation, accepted C1A.5 context; no terrain vertex edits'}
# BASE_SITE
base_site['circulation_network']={k:data[k] for k in ['market_mask_volumes','portal','guild_gate','arrival','protected','prop_instance_moves','prop_corrections']}
base_site['routes']=network['afterRoutes']
dg=bpy.context.evaluated_depsgraph_get();cost={}
def export(objects,col_name,file,key,meta):
 col=bpy.data.collections['C1C / '+col_name];batches={};colliders=[]
 for o in objects:
  if o.type not in ['MESH','FONT','CURVE']:continue
  ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();verts=[o.matrix_world@v.co for v in me.vertices];name=base(o)
  walk=bool(o.get('walkable')) or name.startswith(('Telaga Awan structural','Warm stone paver','Highland gate step'))
  for tri in me.loop_triangles:
   mat=me.materials[tri.material_index]if me.materials else None
   if not mat:continue
   k=(mat.name,walk);b=batches.setdefault(k,{'vs':[],'fs':[],'smooth':[]});i=len(b['vs']);b['vs'].extend(tuple(verts[v])for v in tri.vertices);b['fs'].append((i,i+1,i+2));b['smooth'].append(me.polygons[tri.polygon_index].use_smooth)
  # Physical rails, posts and furniture use the same existing collision system.
  solid=any(k in name.lower()for k in ['guard','handrail','perimeter rail','perimeter post','cheek','closure'])or o.get('collision') or name.startswith(('Shade timber post','Planted seating-edge trough','Seat stone pier','Cafe chair','Square cafe table','Bench frame','Bench timber seat'))
  if solid and verts:
   mn=[min(v[k]for v in verts)for k in range(3)];mx=[max(v[k]for v in verts)for k in range(3)]
   c={'x':36+(mn[0]+mx[0])/2,'z':44-(mn[1]+mx[1])/2,'w':mx[0]-mn[0],'d':mx[1]-mn[1],'minY':18.6+mn[2],'h':18.6+mx[2],'circulation':name,'square':name if key=='square_manifest'else None}
   if ('rail' in name.lower()or'infill'in name.lower())and len(verts)==8:
    a=sum(verts[:4],Vector())/4;b=sum(verts[4:],Vector())/4;dx,dz=b.x-a.x,a.y-b.y;l=math.hypot(dx,dz)
    if l>.1:c['oriented']={'rotation':-math.atan2(dz,dx),'w':l+.06,'d':.085}
   colliders.append(c)
  ev.to_mesh_clear()
 if key=='square_manifest':
  for i in range(16):a=i*math.tau/16;colliders.append({'x':24+1.12*math.cos(a),'z':9+1.12*math.sin(a),'w':.56,'d':.56,'minY':21.8,'h':22.3,'square':'Fountain basin'})
 meta['colliders']=colliders
 root=bpy.data.objects.new('C1C / '+col_name,None);col.objects.link(root);root[key]=json.dumps(meta)
 for (m,walk),b in batches.items():
  me=bpy.data.meshes.new('C1C '+m);me.from_pydata(b['vs'],[],b['fs']);me.materials.append(bpy.data.materials[m]);me.update()
  for p,sm in zip(me.polygons,b['smooth']):p.use_smooth=sm
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bm.to_mesh(me);bm.free()
  o=bpy.data.objects.new(m+(' / walking surface'if walk else' / static'),me);col.objects.link(o);o.parent=root;o['walkable']=walk
 bpy.ops.object.select_all(action='DESELECT')
 for o in col.objects:o.hide_set(False);o.select_set(True)
 bpy.context.view_layer.objects.active=root
 scene_strings={k:v for k,v in s.items()if isinstance(v,str)}
 for k in scene_strings:del s[k]
 try:
  bpy.ops.export_scene.gltf(filepath=OUT+file,export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False,export_cameras=False,export_lights=False)
 finally:
  for k,v in scene_strings.items():s[k]=v
 cost[file]={'batches':len(batches),'colliders':len(colliders),'source_objects':len(objects)};col.hide_render=col.hide_viewport=True
export(interface_objects,'Export interfaces','circulation-interfaces.glb','site_manifest',base_site)
square_meta={'phase':'R0-C1C circulation only','court_floor_y':21.8,'forecourt_floor_y':22.614,'routes':[]}
export(square_objects,'Export square','circulation-square.glb','square_manifest',square_meta)
s['c1c_network']=json.dumps(network);s['c1c_export']=json.dumps(cost)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'circulation-design.blend')
print(json.dumps(cost))
