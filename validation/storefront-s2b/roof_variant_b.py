"""Blender MCP: alternate editable roof and material-batched game exports."""
import bpy,math,json,random
from mathutils import Vector
OUT='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/validation/storefront-s2b/'
assert bpy.data.filepath.startswith(OUT), 'Run only in the independent S2-B master.'
assert 'S2B / Modules / Roof B' not in bpy.data.collections, 'Roof B already exists; edit its existing geometry.'
src=bpy.data.scenes['S2B Editable Modules'];bpy.context.window.scene=src
roofA=bpy.data.collections['S2B / Modules / Roof A']
roofB=bpy.data.collections.new('S2B / Modules / Roof B');src.collection.children.link(roofB)
rootB=bpy.data.objects.new('RoofBSocket',None);rootB.location=(0,.5,6.45);rootB['module']='Roof B';rootB['socket_world']=[0,.5,6.45];roofB.objects.link(rootB)
wood=bpy.data.materials['S2A / oiled tropical timber'];tiles=[bpy.data.materials['S2A / terracotta '+str(i)] for i in range(5)]
def part(name,verts,faces,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(mat)
 ob=bpy.data.objects.new('Roof B / '+name,me);roofB.objects.link(ob);ob.parent=rootB;ob.matrix_parent_inverse=rootB.matrix_world.inverted();ob['module']='Roof B';return ob
def bar(name,a,b,w,d,mat):
 v=Vector(b)-Vector(a);z=v.normalized();x=z.cross(Vector((0,1,0)))
 if x.length<.01:x=z.cross(Vector((1,0,0)))
 x.normalize();y=z.cross(x).normalized();vs=[]
 for p in [Vector(a),Vector(b)]:
  for dx,dy in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(tuple(p+x*dx*w/2+y*dy*d/2))
 return part(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat)
# Limasan-inspired straight deep eaves, steeper hip, low ventilated ridge.
patches=[
 [(-4.45,-4.85,6.72),(4.45,-4.85,6.72),(0,-1.3,8.68),(0,-1.3,8.68)],
 [(4.45,-4.85,6.72),(4.45,5.85,6.72),(0,3.1,8.68),(0,-1.3,8.68)],
 [(4.45,5.85,6.72),(-4.45,5.85,6.72),(0,3.1,8.68),(0,3.1,8.68)],
 [(-4.45,5.85,6.72),(-4.45,-4.85,6.72),(0,-1.3,8.68),(0,3.1,8.68)]]
def pt(p,u,v):
 a,b,c,d=map(Vector,p);q=a.lerp(b,u).lerp(d.lerp(c,u),v)
 # Gentle broken pitch: protective shallow skirt beneath the steeper upper hip.
 q.z-=.16*math.sin(v*math.pi);return q
random.seed(9)
for side,p in enumerate(patches):
 vs=[];fs=[]
 for j in range(9):
  for i in range(13):vs.append(tuple(pt(p,i/12,j/8)))
 for j in range(8):
  for i in range(12):k=j*13+i;fs.append((k,k+1,k+14,k+13))
 ob=part('hip shell '+str(side),vs,fs,wood);so=ob.modifiers.new('Editable roof thickness','SOLIDIFY');so.thickness=.09
 vs=[];fs=[];colors=[]
 for j in range(10):
  cols=max(2,round(18*(1-j/10 if side%2==0 else 1-j/20)))
  for i in range(cols):
   k=len(vs)
   for u,v in [(i/cols,j/10),((i+1)/cols,j/10),((i+1)/cols,min(1,(j+1.04)/10)),(i/cols,min(1,(j+1.04)/10))]:
    q=pt(p,u,v);q.z+=.045;vs.append(tuple(q))
   fs.append((k,k+1,k+2,k+3));colors.append(random.randrange(5))
 ob=part('tile courses '+str(side),vs,fs,tiles[0])
 for m in tiles[1:]:ob.data.materials.append(m)
 for f,idx in zip(ob.data.polygons,colors):f.material_index=idx
 a,b=Vector(p[0]),Vector(p[1]);bar('straight deep fascia',a-Vector((0,0,.06)),b-Vector((0,0,.06)),.10,.20,wood)
for side in [0,2]:
 for u in [0,1]:
  for j in range(10):bar('hip cover',pt(patches[side],u,j/10)+Vector((0,0,.06)),pt(patches[side],u,(j+1)/10)+Vector((0,0,.06)),.13,.12,tiles[2])
for x in [-.19,.19]:
 for z in [8.74,8.82]:bar('ridge louver',(x,-1.45,z),(x,3.25,z),.055,.045,wood)
 for y in [-1.2,3.0]:bar('ridge support',(x,y,8.68),(x,y,8.92),.05,.05,wood)
ob=part('low ridge rain cap',[(-.40,-1.6,8.90),(0,-1.6,9.06),(.40,-1.6,8.90),(-.40,3.4,8.90),(0,3.4,9.06),(.40,3.4,8.90)],[(0,3,4,1),(1,4,5,2)],tiles[2]);so=ob.modifiers.new('Ridge cap thickness','SOLIDIFY');so.thickness=.05
# Exclude the alternate from the main editable building display, retain it editable.
roofB.hide_render=True;roofB.hide_viewport=True


bpy.ops.wm.save_as_mainfile(filepath=OUT+'kopi-awan-modular.blend')
