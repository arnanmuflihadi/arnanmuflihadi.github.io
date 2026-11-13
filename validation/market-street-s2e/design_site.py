"""Live MCP authoring in an independent S2-E file; metre-scale site proposals only."""
import bpy,math,json,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/market-street-s2e/'
assert bpy.data.filepath==OUT+'site-interface.blend'
src=bpy.data.scenes['S2C Market Street'];bpy.context.window.scene=src;bpy.context.view_layer.update()
for old in list(bpy.data.scenes):
 if old.name.startswith('S2E '):
  for ob in list(old.objects):
   if len(ob.users_scene)==1:bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.scenes.remove(old)
for c in list(bpy.data.collections):
 if c.name.startswith('S2E / '):bpy.data.collections.remove(c)
for me in list(bpy.data.meshes):
 if me.users==0:bpy.data.meshes.remove(me)
for m in list(bpy.data.materials):
 if m.name.startswith('S2E / ') and m.users==0:bpy.data.materials.remove(m)
terrain=bpy.data.objects['Exact R0A3 Terrain']
bvh=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices) for p in terrain.data.polygons])
def ground(u,v):
 hit=bvh.ray_cast(Vector((u,v,120)),Vector((0,0,-1)))[0]
 assert hit is not None,(u,v)
 return hit.z
def P(x,z,y):return(x-36,44-z,y-18.6)
grading={'Measured terrain / local art grading proposal','Measured entrance landscape connection','Continuous planted arrival embankment'}
parts={}
for cat in ['Buildings','Streets','Landscape','Props','Cameras']:
 for o in bpy.data.collections['S2C / '+cat].all_objects:parts[o.name]=cat
saved=[(o,o.matrix_world.copy()) for o in src.objects if o.name not in grading and o!=terrain]
s=bpy.data.scenes.new('S2E Interface Design');s.world=src.world;s.unit_settings.system='METRIC';s.render.engine=src.render.engine
s.render.resolution_x=1800;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.cycles.samples=48
s.view_settings.view_transform=src.view_settings.view_transform;s.view_settings.look=src.view_settings.look;s.view_settings.exposure=src.view_settings.exposure
cols={}
def col(name):
 c=bpy.data.collections.new('S2E / '+name);s.collection.children.link(c);cols[name]=c;return c
for name in ['Buildings','Streets','Landscape','Props','Cameras','Terrain Reference','Common Interface','A Terraced','B Braced','H Hybrid','Collision References']:col(name)
landscape_patches=[]
for ob,matrix in saved:
 o=ob.copy();o.parent=None;o.matrix_world=matrix;cols[parts.get(ob.name,'Cameras')].objects.link(o)
 if 'shared canopy' in ob.name.lower() and 0<matrix.translation.y<30:
  u,v=matrix.translation.x,matrix.translation.y;old=matrix.translation.z;g=ground(u,v)
  if old-g>.15:
   o.location.z+=g-old;landscape_patches.append({'u':u,'v':v,'before_h':old,'after_h':g,'delta_h':g-old,'source':'standalone showcase canopy; original GLB unchanged'})
 if ob.type=='CAMERA' and ob.name=='S2C Arrival':s.camera=o
o=terrain.copy();cols['Terrain Reference'].objects.link(o)
bpy.context.window.scene=s
common=cols['Common Interface'];A=cols['A Terraced'];B=cols['B Braced'];H=cols['H Hybrid'];collision=cols['Collision References']
def mat(name,rgb,rough=.9,metal=0):
 m=bpy.data.materials.new('S2E / '+name);m.use_nodes=True;m.diffuse_color=(*rgb,1)
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*rgb,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
stone=mat('volcanic stone',(.26,.30,.265));stone2=mat('mineral stone variation',(.31,.335,.285));cap=bpy.data.materials['S2A / sandstone base'];timber=bpy.data.materials['S2A / oiled tropical timber'];metal=bpy.data.materials['S2A / patinated bronze frames'];soil=mat('planting soil',(.12,.17,.10));leaf=bpy.data.materials['S2C / tropical meadow 0'];paving=bpy.data.materials['S2C / warm pedestrian stone 1']
def mesh(name,vs,fs,material,c):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);c.objects.link(o)
 if material:me.materials.append(material)
 return o
def box(name,p,size,m,c):
 x,y,z=p;a,b,d=[v/2 for v in size];vs=[(x+sx*a,y+sy*b,z+sz*d) for sz in[-1,1] for sy in[-1,1] for sx in[-1,1]]
 return mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],m,c)
def beam(name,a,b,w,d,m,c):
 a,b=Vector(a),Vector(b);z=(b-a).normalized();x=z.cross(Vector((0,1,0)))
 if x.length<.01:x=z.cross(Vector((1,0,0)))
 x.normalize();y=z.cross(x).normalized();vs=[tuple(p+x*dx*w/2+y*dy*d/2) for p in[a,b] for dx,dy in[(-1,-1),(1,-1),(1,1),(-1,1)]]
 return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],m,c)
colliders=[];contacts=[];routes={};volumes={}
def rail(a,b,c,name='Guard'):
 a,b=Vector(a),Vector(b);length=(b-a).xy.length
 if length<.05:return
 n=max(1,math.ceil(length/1.25))
 for i in range(n+1):
  p=a.lerp(b,i/n);beam(name+' upright',p-Vector((0,0,.18)),p+Vector((0,0,1.1)),.075,.075,metal,c)
 for h in[.48,.78]:beam(name+' infill',a+Vector((0,0,h)),b+Vector((0,0,h)),.035,.035,metal,c)
 beam(name+' timber handrail',a+Vector((0,0,1.1)),b+Vector((0,0,1.1)),.10,.095,timber,c)
 du,dv=b.x-a.x,b.y-a.y;colliders.append({'x':36+(a.x+b.x)/2,'z':44-(a.y+b.y)/2,'w':abs(du)+.12,'d':abs(dv)+.12,'oriented':{'rotation':math.atan2(dv,du),'w':length,'d':.12},'minY':18.6+min(a.z,b.z),'h':18.6+max(a.z,b.z)+1.12,'guard':True})
def pier(u,v,top,c,label,braced=True):
 g=ground(u,v);h=top-g
 if h<.12:return
 foot=min(1.15,max(.35,h*.35));foot=min(foot,h)
 corners=[(u-.45,v-.45),(u+.45,v-.45),(u+.45,v+.45),(u-.45,v+.45)]
 gs=[ground(x,y) for x,y in corners];tops=g+foot
 vs=[(x,y,min(h-.20,tops-.10)) for (x,y),h in zip(corners,gs)]+[(x,y,tops) for x,y in corners]
 mesh(label+' terrain-scribed stone footing',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],stone,c)
 contacts.append({'u':u,'v':v,'terrain':g,'bottom':g-.20,'top':top,'role':label,'collection':c.name,'corner_terrain':gs,'corner_bases':[min(h-.20,tops-.10) for h in gs]})
 if h>foot+.05:beam(label+' timber column',(u,v,g+foot-.04),(u,v,top),.28,.28,timber,c)
 box(label+' bearing plate',(u,v,top-.025),(.44,.44,.05),metal,c)
 return g+foot
def wall(a,b,top,c,label,depth=.38):
 a,b=Vector(a),Vector(b);d=b-a;n=Vector((-d.y,d.x,0)).normalized()*depth/2
 ga,gb=ground(a.x,a.y)-.15,ground(b.x,b.y)-.15
 if min(top-ga,top-gb)<.08:return
 vs=[tuple(Vector((p.x,p.y,h))+sign*n) for p,h in[(a,ga),(b,gb),(b,top),(a,top)] for sign in[-1,1]]
 o=mesh(label,vs,[(0,2,4,6),(1,7,5,3),(0,1,3,2),(6,4,5,7),(0,6,7,1),(2,3,5,4)],stone,c)
 for z in range(1,int((top-min(ga,gb))/.72)+1):
  h=min(ga,gb)+z*.72
  if h>max(ga,gb)+.03 and h<top-.12:beam(label+' stone course',(a.x+n.x,a.y+n.y,h),(b.x+n.x,b.y+n.y,h),.024,.025,stone2,c)
 beam(label+' coping',(a.x,a.y,top+.045),(b.x,b.y,top+.045),depth+.12,.09,cap,c)
 return o
plots=[('B1',-8.3,10,8.55,7.2,1.202857142857),('B2',8.3,11.2,7.9515,5.904,1.394285714286),('B3',-8.3,21.8,7.9515,7.992,3.12),('B4',8.3,22.6,8.208,7.992,3.12)]
for name,u,v,w,d,top in plots:
 volume=0
 for i in range(16):
  for j in range(16):volume+=max(0,top-ground(u-w/2+(i+.5)*w/16,v-d/2+(j+.5)*d/16))*w*d/256
 volumes[name]=volume
 # Alternative A: three localized stone retaining tiers; actual ground clips each band.
 for level in range(4):
  ext=level*.68;y=top-level*1.8;ww=w+.4+ext*2;dd=d+.4+ext*2
  corners=[(u-ww/2,v-dd/2),(u+ww/2,v-dd/2),(u+ww/2,v+dd/2),(u-ww/2,v+dd/2)]
  for k in range(4):
   aa,bb=corners[k],corners[(k+1)%4];length=math.dist(aa,bb);n=math.ceil(length/2)
   for j in range(n):
    a=(aa[0]+(bb[0]-aa[0])*j/n,aa[1]+(bb[1]-aa[1])*j/n,0);b=(aa[0]+(bb[0]-aa[0])*(j+1)/n,aa[1]+(bb[1]-aa[1])*(j+1)/n,0)
    if max(ground(a[0],a[1]),ground(b[0],b[1]))<y-.08:
     # The lower levels meet ground; upper levels only face the next retained bench.
     z0=max(y-1.8,max(ground(a[0],a[1]),ground(b[0],b[1]))-.1)
     box(name+' retained tier',( (a[0]+b[0])/2,(a[1]+b[1])/2,(z0+y)/2),((abs(b[0]-a[0]) or .48),(abs(b[1]-a[1]) or .48),y-z0),stone if (j+level)%3 else stone2,A)
  box(name+' retained bench',(u,v,y-.055),(ww,dd,.11),cap,A)
 for c in[B,H]:
  pts=[]
  for i in range(3):
   row=[]
   for j in range(3):
    x=u+(i-1)*(w-.9)/2;y=v+(j-1)*(d-.9)/2;foot=pier(x,y,top-.32,c,name);row.append((x,y,foot))
   pts.append(row)
  for i in range(3):beam(name+' transverse floor bearer',(u-w/2,v+(i-1)*(d-.9)/2,top-.16),(u+w/2,v+(i-1)*(d-.9)/2,top-.16),.30,.32,timber,c)
  for side in[-1,1]:beam(name+' perimeter bearer',(u+side*(w-.9)/2,v-d/2,top-.16),(u+side*(w-.9)/2,v+d/2,top-.16),.30,.32,timber,c)
  for face in[[(0,0),(1,0),(2,0)],[(0,2),(1,2),(2,2)],[(0,0),(0,1),(0,2)],[(2,0),(2,1),(2,2)]]:
   for k in range(2):
    a=pts[face[k][0]][face[k][1]];b=pts[face[k+1][0]][face[k+1][1]]
    if a[2] is None or b[2] is None:continue
    low=max(a[2],b[2])+.2
    if top-low>1.4:
     beam(name+' diagonal brace',(a[0],a[1],low),(b[0],b[1],top-.55),.15,.17,metal,c);beam(name+' diagonal brace',(b[0],b[1],low),(a[0],a[1],top-.55),.15,.17,metal,c)
    elif c==H:wall((a[0],a[1],0),(b[0],b[1],0),top-.30,H,name+' short stone infill',.40)
 # Hybrid planted stone toe at the street-facing slope; no blanket fill.
 face=u+(w/2 if u<0 else -w/2)
 for off in[-d*.25,d*.25]:
  x=face;y=v+off;g=ground(x,y);h=min(1.05,max(.3,top-g-.6))
  wall((x,y-.85,0),(x,y+.85,0),g+h,H,name+' planted retaining toe',.5)
  box(name+' toe planting',(x,y,g+h+.05),(.52,1.65,.08),soil,H)
def profile(v):
 if v<4:return .1*v
 if v<6.4:return .4+min(6,math.floor((v-4)/.4+1e-6))*(1.042857142857/6)
 if v<14.4:return 1.442857142857
 if v<18:return 1.442857142857+min(11,math.floor((v-14.4)/(3.6/11)+1e-6))*((3.36-1.442857142857)/11)
 if v<28:return 3.36
 if v<30:return 3.36+min(4,math.floor((v-28)/.5+1e-6))*.16
 return 4
prof=[(0,.014),(4,.414)]
for start,count,tread,base,rise in[(4,6,.4,.4,1.042857142857/6),(14.4,11,3.6/11,1.442857142857,(3.36-1.442857142857)/11),(28,4,.5,3.36,.16)]:
 if prof[-1][0]<start:prof.append((start,base+.014))
 for i in range(1,count+1):prof.extend([(start+i*tread,base+(i-1)*rise+.014),(start+i*tread,base+i*rise+.014)])
prof.append((36,4.014))
def strip(name,points,width,c,material,solid=True):
 vs=[]
 for i,p in enumerate(points):
  a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)]);d=b-a;d.z=0
  if d.length<.000001:d=Vector((0,1,0))
  d.normalize();n=Vector((-d.y,d.x,0))*width/2
  vs.extend([tuple(Vector(p)-n),tuple(Vector(p)+n)])
 fs=[(2*i,2*i+2,2*i+3,2*i+1) for i in range(len(points)-1)]
 o=mesh(name,vs,fs,material,c);o['walkable']=True
 if solid:m=o.modifiers.new('Deck depth','SOLIDIFY');m.thickness=.18;m.offset=-1
 return o,vs
mesh('Exact market stair collision deck',[p for v,h in prof for p in[(-3,v,h),(3,v,h)]],[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(prof)-1)],None,collision)['walkable']=True
# Structural rows and stringers below the already-approved public paving.
for v in[0,4,6.4,10,14.4,18,22,26,28,30,34,36]:
 h=profile(v)+.014-.26
 for u in[-4.65,0,4.65]:pier(u,v,h,common,'Street support')
 beam('Street transverse support',(-5.1,v,h+.1),(5.1,v,h+.1),.24,.28,timber,common)
for a,b in[(4,6.4),(14.4,18),(28,30)]:
 for u in[-4.6,4.6]:beam('Stair stringer',(u,a,profile(a)-.2),(u,b,profile(b)-.2),.23,.32,timber,common)
# Natural ground approach: shallow steps to a minimal provisional landing, not a skyport building.
start=P(24,66,0);end=P(27,61.8,17.15);start=(start[0],start[1],ground(start[0],start[1])+.02);rise=(end[2]-start[2])/13
entry=[start];dx,dy=end[0]-start[0],end[1]-start[1]
for i in range(1,14):
 f=i/13;p=(start[0]+dx*f,start[1]+dy*f,start[2]+(i-1)*rise);entry.extend([p,(p[0],p[1],start[2]+i*rise)])
strip('Natural approach stair',entry,3.2,common,paving);routes['natural_approach']=[list(P(24,66,18.6+start[2])),list(end)]
box('Provisional skyport threshold landing',(-9,-16,-1.45-.12),(3.6,3.6,.24),cap,common)['walkable']=True
bridge=[P(27,60,17.15),P(30.15,51.8,17.442)];strip('Arrival bridge',bridge,3,common,paving)
arrival=[(.75*v,v,.15*v+.012) for v in[-8,-6,-4,-2,0]]
strip('Garden path visible bearing deck',[(u,v,h-.002) for u,v,h in arrival],2.8,common,paving)
strip('Garden path support collar',arrival,2.79,collision,None,False)
box('Market entrance seam landing',(0,0,.014-.09),(3.1,1.0,.18),paving,common)['walkable']=True
# Broad stair down to a small terrain-level threshold at the north end of the reservation.
sqY=ground(0,44)+.02;sqRise=(4.014-sqY)/11;square=[(0,35.7,4.014),(0,36.2,4.014)]
for i in range(1,12):square.extend([(0,36.2+i*.45,4.014-(i-1)*sqRise),(0,36.2+i*.45,4.014-i*sqRise)])
square.append((0,44,sqY));strip('Square threshold stair',square,4.4,common,paving)
box('Square stair-ramp junction collar',(-3.15,36.12,4.014-.09),(2.7,.94,.18),paving,common)['walkable']=True
loop=[P(33,9,22.614),P(32.3,7.9,22.614),P(30.5,5.5,22.05),P(31,1.2,21.6),P(36,0,18.6+sqY)]
strip('Square garden ramp alternate',loop,2.4,common,paving)
# End interfaces meet the actual cross-slope, with no terrain sculpting.
for u in[-1.95,1.95]:
 h=ground(u,44)+.025
 mesh('Square ground tie',[(0,42.6,sqY),(u,42.6,max(sqY,h)),(u,44,h),(0,44,sqY)],[(0,1,2,3) if u>0 else (0,3,2,1)],paving,common)['walkable']=True
# Guard the designed exposed edges; keep the original shopfronts open.
for sign,ranges in[(-1,[(0,6.1),(14,17.7),(26.3,29.8)]),(1,[(0,7.95),(14.45,18.2),(27.1,29.8)])]:
 for a,b in ranges:
  pts=[(sign*5.05,a+(b-a)*i/max(1,math.ceil((b-a)/1.1)),0) for i in range(max(1,math.ceil((b-a)/1.1))+1)]
  for i in range(len(pts)-1):
   aa,bb=pts[i],pts[i+1];rail((aa[0],aa[1],profile(aa[1])+.014),(bb[0],bb[1],profile(bb[1])+.014),common,'Market edge')
def guard_strip(points,width,label):
 # The guard is inset from the slab edge; entry/exit remain open.
 for sign in[-1,1]:
  edge=[]
  for i,p in enumerate(points):
   a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)]);d=b-a;d.z=0
   if d.length<.001:d=Vector((0,1,0))
   d.normalize();n=Vector((-d.y,d.x,0))*(width/2-.08)*sign;edge.append(tuple(Vector(p)+n))
  for a,b in zip(edge,edge[1:]):rail(a,b,common,label)
guard_strip([entry[0],entry[-1]],3.2,'Arrival approach guard');guard_strip(bridge,3,'Bridge guard');guard_strip(arrival,2.8,'Garden path guard');guard_strip([(0,36.2,4.014),(0,41.15,sqY),(0,42,sqY)],4.4,'Square stair guard');guard_strip(loop[:-1]+[P(32.6,.816,21.3295185)],2.4,'Square ramp guard')
rail((-5.1,0,.014),(-1.58,0,.014),common,'Market arrival return');rail((1.58,0,.014),(5.1,0,.014),common,'Market arrival return')
rail((-10.8,-17.8,-1.45),(-10.8,-14.2,-1.45),common,'Provisional landing side');rail((-7.2,-17.8,-1.45),(-7.2,-14.2,-1.45),common,'Provisional landing side')
rail((-8.1,-17.8,-1.45),(-7.2,-17.8,-1.45),common,'Provisional landing corner');rail((-10.8,-14.2,-1.45),(-10.1,-14.2,-1.45),common,'Provisional landing corner')
rail((-8,36,4.014),(-5.1,36,4.014),common,'Square edge');rail((2.25,36,4.014),(8,36,4.014),common,'Square edge')
# Bearers and grounded feet for the added connectors, including the natural-ground tie.
for label,points,width in[('Arrival approach',entry,3.2),('Arrival bridge',bridge,3),('Garden path',arrival,2.8),('Square stair',square,4.4),('Square ramp',loop,2.4)]:
 selected=points if len(points)<8 else points[::4]+[points[-1]]
 for p in selected:
  for sign in[-1,1]:pier(p[0]+sign*(width/2-.35),p[1],p[2]-.25,common,label)
  beam(label+' support header',(p[0]-width/2,p[1],p[2]-.20),(p[0]+width/2,p[1],p[2]-.20),.22,.27,timber,common)
# Localized earth/stone planting sockets support original palms/trees that stood on study grading.
for ob,matrix in saved:
 if ob.type!='MESH':continue
 bounds=[matrix@Vector(corner) for corner in ob.bound_box];size=Vector(tuple(max(v[k] for v in bounds)-min(v[k] for v in bounds) for k in range(3)))
 is_tree='shared canopy' in ob.name.lower();is_palm='palm' in ob.name.lower() and size.z>3 and size.x<1 and size.y<1
 if not(is_tree or is_palm):continue
 if is_tree and any(abs(matrix.translation.x-p['u'])<.01 and abs(matrix.translation.y-p['v'])<.01 for p in landscape_patches):continue
 u,v=matrix.translation.x,matrix.translation.y;top=min(p.z for p in bounds)-.015;g=ground(u,v)
 if top-g<.15:continue
 r=1.2 if is_tree else .65;vs=[]
 for h in[0,1]:
  for i in range(12):
   a=math.tau*i/12;x=u+r*math.cos(a);y=v+r*math.sin(a);vs.append((x,y,top if h else ground(x,y)-.15))
 fs=[(i,(i+1)%12,(i+1)%12+12,i+12) for i in range(12)]+[tuple(range(12,24))]
 mesh('Original planting support socket',vs,fs,stone,common);box('Planting soil cap',(u,v,top+.02),(r*1.15,r*1.15,.04),soil,common)
# Collision references are authoritative for support, never visible paving replacements.
collision.hide_render=True
for o in collision.objects:o.hide_render=True;o.display_type='WIRE'
for c in[A,B]:c.hide_render=True;c.hide_viewport=True
routes.update({'deck_to_square':[list(P(27,60,17.15)),list(P(30,52,17.412)),list(P(36,44,18.614)),list(P(36,8,22.614)),list(P(36,0,18.6+sqY))],'square_alternate':[list(p) for p in loop]})
metadata={'mapping':'game (36+u,18.6+h,44-v)','plots':plots,'landscape_alignment':landscape_patches,'fill_estimate_m3':volumes,'colliders':colliders,'contacts':contacts,'routes':routes,'square_risers':11,'square_step_height':sqRise,'arrival_risers':13,'arrival_step_height':rise,'source_glb':'../market-street-s2d/market-street-optimized.glb','structural_status':'Visual game-environment proposal, not certified structural engineering'}
s['S2E_manifest']=json.dumps(metadata)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'site-interface.blend')
print('S2E_SITE='+json.dumps(metadata))
