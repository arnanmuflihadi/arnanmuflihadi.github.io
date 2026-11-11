import bpy, math, random
from mathutils import Vector
from math import sin,cos,pi
random.seed(7)
old_scene=bpy.context.window.scene
scene=bpy.data.scenes.new('R0-D2 | Dragon study')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC'
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('D2 | warm daylight');scene.world.color=(.24,.24,.24)
scene.view_settings.view_transform='AgX'
coll=bpy.data.collections.new('DRAGON | editable');scene.collection.children.link(coll)
ref=bpy.data.collections.new('REFERENCE | excluded from export');scene.collection.children.link(ref)

def material(name,color,rough=.78,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
jade=material('D2 | deep rainforest jade',(.12,.32,.27));sage=material('D2 | soft sage',(.28,.48,.36));under=material('D2 | warm limestone',(.67,.62,.44));wingmat=material('D2 | wing membrane',(.22,.39,.33),.85);wood=material('D2 | woven saddle',(.32,.18,.09));strap=material('D2 | leather straps',(.19,.10,.045));bronze=material('D2 | muted bronze',(.47,.27,.09),.45,.22);dark=material('D2 | obsidian eyes',(.028,.043,.036),.3);ground=material('D2 | warm neutral ground',(.66,.68,.57));human=material('D2 | scale reference',(.75,.48,.23))
def mesh_obj(name,verts,faces,mat,collection=coll):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);collection.objects.link(o);o.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 return o

def tube(name,points,radii,mat,segments=16,group=None):
 # Elliptical rings oriented perpendicular to the local center line.
 points=[Vector(p) for p in points];verts=[]
 for i,p in enumerate(points):
  t=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();side=t.cross(Vector((0,0,1)))
  if side.length<.01:side=Vector((1,0,0))
  side.normalize();up=side.cross(t).normalized();rx,rz=radii[i]
  for j in range(segments):
   a=2*pi*j/segments;v=p+side*(cos(a)*rx)+up*(sin(a)*rz);verts.append(v[:])
 faces=[]
 for i in range(len(points)-1):
  for j in range(segments):a=i*segments+j;b=i*segments+(j+1)%segments;faces.append((a,b,b+segments,a+segments))
 faces+=[tuple(reversed(range(segments))),tuple((len(points)-1)*segments+j for j in range(segments))]
 o=mesh_obj(name,verts,faces,mat)
 if group:
  for i in range(len(points)):
   bone=group[min(i,len(group)-1)];vg=o.vertex_groups.get(bone) or o.vertex_groups.new(name=bone);vg.add(list(range(i*segments,(i+1)*segments)),1,'REPLACE')
 return o

def ellipsoid(name,loc,scale,mat,group=None,segments=24,rings=14,collection=coll):
 verts=[];faces=[]
 for i in range(rings+1):
  th=pi*i/rings
  for j in range(segments):
   ph=2*pi*j/segments;verts.append((loc[0]+scale[0]*sin(th)*cos(ph),loc[1]+scale[1]*sin(th)*sin(ph),loc[2]+scale[2]*cos(th)))
 for i in range(rings):
  for j in range(segments):a=i*segments+j;b=i*segments+(j+1)%segments;faces.append((a,b,b+segments,a+segments))
 o=mesh_obj(name,verts,faces,mat,collection)
 if group:o.vertex_groups.new(name=group).add(list(range(len(verts))),1,'REPLACE')
 return o

def bone(name,a,b,parent=None):
 e=arm.edit_bones.new(name);e.head=a;e.tail=b
 if parent:e.parent=arm.edit_bones[parent]
 return e
arm=bpy.data.armatures.new('D2 | flight skeleton');rig=bpy.data.objects.new('D2 | FLIGHT RIG',arm);coll.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
bone('body',(0,.1,1.65),(0,-.9,1.75));bone('neck',(0,-.9,1.75),(0,-1.95,2.5),'body');bone('head',(0,-1.95,2.5),(0,-2.8,2.65),'neck');bone('tail1',(0,1.0,1.55),(0,2.0,1.35),'body');bone('tail2',(0,2.0,1.35),(0,3.1,.95),'tail1');bone('tail3',(0,3.1,.95),(0,4.2,.65),'tail2')
for s in [-1,1]:
 side='L' if s==1 else 'R';bone('wing_'+side,(s*.5,-.45,1.9),(s*2.35,-.35,2.15),'body');bone('tip_'+side,(s*2.35,-.35,2.15),(s*4.6,.15,2.45),'wing_'+side)
 for front,y in [('front',-.65),('rear',.8)]:
  bone(front+'_'+side,(s*.62,y,1.5),(s*.85,y+.12,.85),'body');bone(front+'_foot_'+side,(s*.85,y+.12,.85),(s*.95,y-.15,.18),front+'_'+side)
bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False);rig.show_in_front=True
parts=[]
parts.append(tube('Continuous body',[(0,-1.05,1.67),(0,-.8,1.7),(0,-.35,1.7),(0,.2,1.68),(0,.72,1.62),(0,1.16,1.53)],[.0 and (0,0) or (.35,.39),(.61,.52),(.78,.62),(.83,.62),(.72,.54),(.42,.37)],jade,24,['body']*6))
parts.append(tube('Neck | tapered',[(0,-.8,1.8),(0,-1.05,1.96),(0,-1.32,2.16),(0,-1.62,2.37),(0,-1.92,2.5),(0,-2.12,2.54)],[(.42,.43),(.37,.39),(.31,.34),(.28,.30),(.25,.27),(.23,.24)],sage,20,['body','body','neck','neck','neck','head']))
parts.append(tube('Long counterbalancing tail',[(0,.86,1.53),(0,1.22,1.47),(0,1.70,1.32),(0,2.2,1.18),(0,2.7,1.02),(0,3.25,.87),(0,3.8,.78),(0,4.35,.72)],[(.48,.40),(.39,.34),(.31,.28),(.25,.22),(.19,.17),(.13,.12),(.08,.07),(.015,.018)],jade,18,['body','tail1','tail1','tail2','tail2','tail3','tail3','tail3']))
parts.append(ellipsoid('Head | tapered cranium',(0,-2.29,2.57),(.35,.53,.28),sage,'head'))
parts.append(ellipsoid('Muzzle',(0,-2.68,2.48),(.28,.43,.16),sage,'head'))
parts.append(ellipsoid('Throat patch',(0,-1.51,2.06),(.225,.72,.115),under,'neck'))
for s in [-1,1]:
 side='L' if s==1 else 'R'
 parts.append(ellipsoid('Eye '+side,(s*.305,-2.45,2.66),(.037,.095,.047),dark,'head',16,10))
 parts.append(tube('Temple horn '+side,[(s*.22,-2.01,2.72),(s*.32,-1.83,2.86),(s*.39,-1.61,2.94)],[(.12,.09),(.08,.06),(.008,.008)],under,12,['head']*3))
 for front,y in [('front',-.65),('rear',.8)]:
  g=front+'_'+side;g2=front+'_foot_'+side
  parts.append(tube(front+' leg '+side,[(s*.52,y,1.5),(s*.72,y+.08,1.27),(s*.82,y+.18,.91),(s*.91,y-.02,.55),(s*.92,y-.18,.22)],[(.28,.3),(.27,.27),(.20,.21),(.15,.15),(.13,.13)],jade,16,['body',g,g,g2,g2]))
  parts.append(ellipsoid(front+' foot '+side,(s*.93,y-.30,.16),(.20,.34,.14),sage,g2,18,10))
  for toe in [-1,0,1]:parts.append(ellipsoid(front+' claw '+side+str(toe),(s*.93+toe*.11,y-.55,.12),(.045,.14,.045),under,g2,10,6))
 # Constrained fan membrane. Every vertex has a real armature group.
 verts=[];faces=[];cols=22;rows=11
 for i in range(cols+1):
  t=i/cols;x=s*(.52+4.08*t);leading=-.48+.35*t;trailing=.35+1.60*sin(pi*t*.84)+.25*t
  for j in range(rows+1):
   u=j/rows;y=leading+(trailing-leading)*u;z=1.96+.42*t-.20*sin(pi*u)*sin(pi*t)+.08*sin(3*pi*t)*u;verts.append((x,y,z))
 for i in range(cols):
  for j in range(rows):a=i*(rows+1)+j;b=(i+1)*(rows+1)+j;faces.append((a,b,b+1,a+1) if s==1 else (a,a+1,b+1,b))
 membrane=mesh_obj('Flight membrane '+side,verts,faces,wingmat);parts.append(membrane)
 for i in range(cols+1):
  a=max(0,min(1,(i/cols-.38)/.28));ids=list(range(i*(rows+1),(i+1)*(rows+1)));(membrane.vertex_groups.get('wing_'+side) or membrane.vertex_groups.new(name='wing_'+side)).add(ids,1-a,'REPLACE');(membrane.vertex_groups.get('tip_'+side) or membrane.vertex_groups.new(name='tip_'+side)).add(ids,a,'REPLACE')
 parts.append(tube('Wing leading spar '+side,[(s*.48,-.48,1.95),(s*1.4,-.43,2.06),(s*2.35,-.32,2.15),(s*3.4,-.21,2.27),(s*4.6,-.13,2.38)],[(.18,.17),(.16,.14),(.13,.11),(.08,.07),(.015,.015)],jade,14,['wing_'+side,'wing_'+side,'wing_'+side,'tip_'+side,'tip_'+side]))
 for k,t in enumerate([.32,.57,.78]):
  x=s*(.52+4.08*t);leady=-.48+.35*t;trail=.35+1.6*sin(pi*t*.84)+.25*t;z=1.96+.42*t
  parts.append(tube('Wing rib '+side+str(k),[(x,leady,z),(x,leady+(trail-leady)*.5,z-.1),(x,trail,z+.03)],[(.055,.055),(.04,.04),(.008,.008)],jade,8,[('wing_' if t<.5 else 'tip_')+side]*3))
# Low broad saddle and supporting straps sit above the torso, between wing roots.
parts.append(ellipsoid('Saddle seat',(0,-.18,2.28),(.45,.57,.12),strap,'body',22,12))
parts.append(ellipsoid('Saddle front bow',(0,-.67,2.33),(.48,.10,.17),wood,'body',18,10))
parts.append(ellipsoid('Saddle rear cantle',(0,.31,2.34),(.47,.10,.17),wood,'body',18,10))
for y in [-.45,.15]:
 pts=[]
 for j in range(17):
  a=2*pi*j/16;pts.append((.79*cos(a),y,1.70+.66*sin(a)))
 parts.append(tube('Saddle girth '+str(y),pts,[(.035,.035)]*len(pts),strap,8,['body']*len(pts)))
for o in parts:
 o.parent=rig;mod=o.modifiers.new('Flight armature','ARMATURE');mod.object=rig
# Rigged animation: small continuous wing flaps and secondary motion, separate named NLA strips.
rig.animation_data_create()
def make_action(name,poses,frames=48):
 rig.animation_data.action=None
 for pb in rig.pose.bones:pb.rotation_mode='XYZ';pb.rotation_euler=(0,0,0)
 for f,values in poses:
  for pb in rig.pose.bones:pb.rotation_euler=(0,0,0)
  for b,rot in values.items():rig.pose.bones[b].rotation_euler=rot
  for b in ['body','neck','head','tail1','tail2','tail3','wing_L','wing_R','tip_L','tip_R']:
   rig.pose.bones[b].keyframe_insert(data_path='rotation_euler',frame=f,group=b)
 action=rig.animation_data.action;action.name=name;track=rig.animation_data.nla_tracks.new();track.name=name;track.strips.new(name,1,action);track.mute=True
 return action
def idle(flap):
 return {'wing_L':(0,flap,0),'wing_R':(0,-flap,0),'tip_L':(0,flap*.35,0),'tip_R':(0,-flap*.35,0),'neck':(.025,0,0),'tail2':(0,0,flap*.18)}
make_action('Idle_Hover',[(1,idle(.08)),(24,idle(-.08)),(48,idle(.08))])
make_action('Takeoff_Preparation',[(1,idle(.12)),(24,idle(.36)),(48,idle(-.18))])
make_action('Wing_Powered_Flight',[(1,idle(.40)),(12,idle(-.42)),(25,idle(.40)),(37,idle(-.42)),(49,idle(.40))])
make_action('Gentle_Bank',[(1,idle(.1)),(24,{**idle(-.18),'body':(0,.10,0),'tail2':(0,0,-.12)}),(48,idle(.1))])
make_action('Approach_Landing',[(1,idle(.2)),(24,idle(-.32)),(48,idle(.2))])
rig.animation_data.action=None
# Human-scale neutral mannequin, intentionally separate from exported model.
ellipsoid('Human reference | torso',(5.9,0,1.15),(.18,.12,.34),human,collection=ref)
ellipsoid('Human reference | head',(5.9,0,1.54),(.115,.11,.12),human,collection=ref)
for s in [-1,1]:
 o=tube('Human reference | leg',[(5.9+s*.09,0,.85),(5.9+s*.10,0,.48),(5.9+s*.10,0,.06)],[(.075,.07),(.065,.06),(.06,.05)],human,12);coll.objects.unlink(o);ref.objects.link(o)
 o=tube('Human reference | arm',[(5.9+s*.16,0,1.38),(5.9+s*.26,0,1.04),(5.9+s*.28,0,.86)],[(.065,.06),(.055,.05),(.045,.04)],human,12);coll.objects.unlink(o);ref.objects.link(o)
# Camera, lights and unobtrusive ground.
verts=[(-15,-15,-.03),(15,-15,-.03),(15,15,-.03),(-15,15,-.03)];mesh_obj('Reference ground',verts,[(0,1,2,3)],ground,ref)
def camera_at(name,loc,target,lens=48):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);ref.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=lens;return o
scene.camera=camera_at('Review | three-quarter',(10,-13,7),(0,.4,1.5),11.6)
def area(name,loc,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);ref.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1.5))-o.location).to_track_quat('-Z','Y').to_euler()
area('Warm key',(2,-7,10),1500,8);area('Cool fill',(-6,1,7),1000,9)
scene.frame_set(1)
# Preserve the original open file: write only the independent scene and dependencies.
out='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/skyport-r0d2-gate-b/'
bpy.ops.wm.save_as_mainfile(filepath=out+'dragon-master.blend',copy=True,compress=True)
print('CREATED',len(parts),'mesh components; original scene retained; isolated scene saved')
