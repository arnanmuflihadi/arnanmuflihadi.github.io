import bpy,bmesh,math
from mathutils import Vector
BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/storefront-s2a/'
plaster,stone,wood,wood_light,dark,brass,glass,plaster_shade = [bpy.data.materials['S2A / '+n] for n in ['warm lime plaster','sandstone base','oiled tropical timber','cut timber edges','patinated bronze frames','aged brass','soft blue green glass','recessed sage plaster']]
roofmats=[bpy.data.materials['S2A / terracotta '+str(i)] for i in range(5)]
def put(o,group):
 for c in list(o.users_collection):c.objects.unlink(o)
 groups[group].objects.link(o)
 return o

def mesh(name,verts,faces,mat,group='Buildings / Shell'):
 data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
 o=bpy.data.objects.new('S2A / '+name,data);groups[group].objects.link(o)
 if mat:data.materials.append(mat)
 o['authorship']='Original project geometry';return o

def bevel(o,width=.025,segments=2):
 m=o.modifiers.new('Craft edge bevel','BEVEL');m.width=width;m.segments=segments
 return o

def box(name,loc,dim,mat,group='Buildings / Joinery',edge=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name='S2A / '+name;o.dimensions=dim
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);put(o,group)
 if edge:bevel(o,edge)
 return o

def beam(name,a,b,width,depth,mat=wood,group='Buildings / Joinery'):
 v=Vector(b)-Vector(a);o=box(name,(Vector(a)+Vector(b))/2,(width,depth,v.length),mat,group)
 o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return o

def cylinder(name,loc,radius,depth,mat,group='Buildings / Joinery',vertices=16):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
 o=bpy.context.object;o.name='S2A / '+name;o.data.materials.append(mat);put(o,group);bevel(o,.01);return o

def wall(name,lo,hi,zlo,zhi,y,holes,rot=0):
 # A genuine wall mesh with openings, not a stack of opaque building boxes.
 xs=sorted(set([lo,hi]+[v for h in holes for v in h[:2]]));zs=sorted(set([zlo,zhi]+[v for h in holes for v in h[2:]]))
 verts=[];faces=[]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(zs,zs[1:]):
   if any(h[0]<(a+b)/2<h[1] and h[2]<(c+d)/2<h[3] for h in holes):continue
   k=len(verts);verts += [(a,y,c),(b,y,c),(b,y,d),(a,y,d)];faces.append((k,k+1,k+2,k+3))
 o=mesh(name,verts,faces,plaster);o.rotation_euler.z=rot
 so=o.modifiers.new('Real wall thickness 220mm','SOLIDIFY');so.thickness=.22;so.offset=0
 bevel(o,.018);return o

roofpatches=[
 [(-4.3,-4.65,6.66),(4.3,-4.65,6.66),(0,-.65,8.02),(0,-.65,8.02)],
 [(4.3,-4.65,6.66),(4.3,5.65,6.66),(0,2.65,8.02),(0,-.65,8.02)],
 [(4.3,5.65,6.66),(-4.3,5.65,6.66),(0,2.65,8.02),(0,2.65,8.02)],
 [(-4.3,5.65,6.66),(-4.3,-4.65,6.66),(0,-.65,8.02),(0,2.65,8.02)]]
def point(p,u,v):
 a,b,c,d=map(Vector,p);q=(a.lerp(b,u)).lerp(d.lerp(c,u),v)
 q.z += .20*(abs(u-.5)*2)**4*(1-v)**4 - .12*math.sin(v*math.pi)
 return q
"""Focused corrections after inspecting the first actual renders; execute via MCP."""
import bpy,bmesh,math
from mathutils import Vector
s=bpy.data.scenes['S2-A Tropical Storefront'];bpy.context.window.scene=s
groups={c.name[6:]:c for c in s.collection.children if c.name.startswith('S2A / ')}
# Reuse functions/materials from the authored build without rebuilding the scene.

# 1. Remove unintended panel seams and align side openings to real elevations.
for o in list(s.objects):
 if o.type=='MESH' and ('shop wall' in o.name or 'upper wall' in o.name) and ('east' in o.name or 'west' in o.name):bpy.data.objects.remove(o,do_unlink=True)
for left in [False,True]:
 o=wall(('west' if left else 'east')+' shop wall',-5,3.55,.20,3.23,3.6,[(-2.8,-.8,1.0,2.7),(.4,2.55,.7,2.7)],-math.pi/2)
 if left:o.location.x=-7.2
 o=wall(('west' if left else 'east')+' upper wall',-5,2.85,3.5,6.45,3.6,[(-2.0,-.7,4.1,5.85),(.5,1.8,4.1,5.85)],-math.pi/2)
 if left:o.location.x=-7.2
for o in s.objects:
 if o.type=='MESH' and any(m.type=='SOLIDIFY' and 'wall' in m.name.lower() for m in o.modifiers):
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

windows=[o for o in s.objects if o.get('source','').startswith('Kenney')]
placements=[(3.63,1.35,4.975,-math.pi/2),(3.63,-1.15,4.975,-math.pi/2),(-3.63,1.35,4.975,math.pi/2),(-3.63,-1.15,4.975,math.pi/2),(1.75,5.02,5,math.pi),(-1.75,5.02,5,math.pi)]
for i,(o,pos) in enumerate(zip(windows,placements)):
 x,y,z,angle=pos;o.rotation_mode='XYZ';o.rotation_euler=(0,0,angle)
 o.scale=(1.3/.3125,4,1.75/.38) if i<4 else (1.5/.3125,4,1.8/.38)
 bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for v in o.bound_box]
 mid=Vector(tuple((min(p[k] for p in pts)+max(p[k] for p in pts))/2 for k in range(3)))
 o.location+=Vector((x,y,z))-mid
 # Add an intentional thin sandstone sill, tied to each wall rather than projecting frames.
 if i<4:box('side window stone sill',(x,y,4.075),(.32,1.48,.07),stone)
 else:box('rear window stone sill',(x,y,4.08),(1.65,.30,.07),stone)
for o in s.objects:
 if 'side shop glass' in o.name:
  if o.location.y<0:o.location.z=1.70;o.dimensions.z=1.98
  else:o.location.z=1.85;o.dimensions.z=1.68
# The side transoms now sit at the actual respective sill height.
for o in list(s.objects):
 if 'side shop transom' in o.name and o.location.y<0 and o.location.z<1.5:o.location.z=.72
 if 'side shop mullion' in o.name and o.location.y<0:o.location.z=1.70;o.dimensions.z=2.04

# 2. Clearer glass, a timber-framed entrance and visible shaded interior.
p=next(n for n in glass.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
p.inputs['Base Color'].default_value=(.64,.82,.78,1);p.inputs['Transmission Weight'].default_value=.96
p.inputs['Metallic'].default_value=0;p.inputs['Roughness'].default_value=.10;p.inputs['IOR'].default_value=1.42
for o in s.objects:
 if o.name.startswith('S2A / entrance') and o.type=='MESH' and 'glass' not in o.name:
  o.data.materials.clear();o.data.materials.append(wood_light)
# A grounded door surround and a small contrasting threshold mark the way in.
box('door stone threshold',(.30,-3.50,.245),(1.66,.48,.04),stone)
box('entrance head transom',(.30,-3.37,2.65),(1.57,.12,.075),wood_light)
box('entrance threshold brass inlay',(.30,-3.62,.27),(1.35,.035,.012),brass)
for name,pos,power,size in [('interior daylight bounce',(-.5,.2,2.9),180,3),('upper room daylight',(-1,.2,6.2),100,2.2)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='S2A / '+name;o.data.energy=power;o.data.size=size;put(o,'Cameras')
# A shaded backdrop behind upper sliders adds a real interior instead of opaque panels.
box('upper room sage back wall',(0,4.82,4.98),(6.8,.035,2.85),plaster_shade,'Buildings / Interior')
for x in [-2.0,.25]:
 cylinder('upper timber table leg',(x,0,3.97),.055,.85,wood,'Buildings / Interior')
 cylinder('upper timber table top',(x,0,4.43),.47,.06,wood_light,'Buildings / Interior',24)

# 3. Close the eave construction. Fascia follows the curved roof profile exactly.
for o in list(s.objects):
 if 'timber eave fascia' in o.name or 'hip ridge cover' in o.name:bpy.data.objects.remove(o,do_unlink=True)
for side,pch in enumerate(roofpatches):
 vs=[];fs=[]
 for i in range(25):
  q=point(pch,i/24,0)
  vs.extend([tuple(q+Vector((0,0,.025))),tuple(q-Vector((0,0,.15)))])
 for i in range(24):k=i*2;fs.append((k,k+2,k+3,k+1))
 o=mesh('continuous curved eave fascia '+str(side),vs,fs,wood,'Buildings / Roof')
 so=o.modifiers.new('Fascia thickness','SOLIDIFY');so.thickness=.07;bevel(o,.015)
for side in [0,2]:
 for u in [0,1]:
  pch=roofpatches[side]
  for j in range(12):
   a=point(pch,u,j/12)+Vector((0,0,.06));b=point(pch,u,(j+1)/12)+Vector((0,0,.06))
   beam('fitted hip cap',a,b,.12,.12,roofmats[2],'Buildings / Roof')
# Strengthen roof pitch slightly while keeping all fascia and caps aligned.
for o in groups['Buildings / Roof'].objects:
 if o.type=='MESH':
  for v in o.data.vertices:
   w=o.matrix_world@v.co
   if w.z>6.66:
    w.z=6.66+(w.z-6.66)*1.13;v.co=o.matrix_world.inverted()@w
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT+'kopi-awan-prototype.blend')
print('S2A_CORRECTIONS_SAVED')
