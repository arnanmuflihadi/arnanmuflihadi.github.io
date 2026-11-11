"""Small Blender-native helpers, sent with each MCP authoring step."""
import bpy,math,random,bmesh
from mathutils import Vector,Matrix
BASE='/Users/arnanmuflihadi/Documents/ChatGPT/Gaming portofolio/'
OUT=BASE+'validation/market-street-s2c/'
def mat(name,color,rough=.75,metal=0):
 m=bpy.data.materials.new('S2C / '+name);m.use_nodes=True;m.diffuse_color=(*color,1)
 p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m
def mesh(name,verts,faces,material,col,parent=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o)
 if material:me.materials.append(material)
 if parent:o.parent=parent
 return o
def box(name,loc,size,material,col,parent=None,edge=.015):
 x,y,z=loc;a,b,c=[v/2 for v in size]
 vs=[(x+sx*a,y+sy*b,z+sz*c) for sz in [-1,1] for sy in [-1,1] for sx in [-1,1]]
 o=mesh(name,vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)],material,col,parent)
 if edge:m=o.modifiers.new('Small craft bevel','BEVEL');m.width=edge;m.segments=1
 return o
def beam(name,a,b,width,depth,material,col,parent=None):
 a,b=Vector(a),Vector(b);z=(b-a).normalized();x=z.cross(Vector((0,1,0)))
 if x.length<.01:x=z.cross(Vector((1,0,0)))
 x.normalize();y=z.cross(x).normalized();vs=[]
 for p in [a,b]:
  for dx,dy in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(tuple(p+x*dx*width/2+y*dy*depth/2))
 return mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],material,col,parent)
def wall(name,lo,hi,zlo,zhi,y,holes,material,col,parent,rotate=0):
 xs=sorted(set([lo,hi]+[v for h in holes for v in h[:2]]));zs=sorted(set([zlo,zhi]+[v for h in holes for v in h[2:]]));vs=[];fs=[]
 for a,b in zip(xs,xs[1:]):
  for c,d in zip(zs,zs[1:]):
   if any(h[0]<(a+b)/2<h[1] and h[2]<(c+d)/2<h[3] for h in holes):continue
   k=len(vs);vs.extend([(a,y,c),(b,y,c),(b,y,d),(a,y,d)]);fs.append((k,k+1,k+2,k+3))
 o=mesh(name,vs,fs,material,col,parent);o.rotation_euler.z=rotate
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 m=o.modifiers.new('220mm wall depth','SOLIDIFY');m.thickness=.22;m.offset=0
 m=o.modifiers.new('Plaster arris','BEVEL');m.width=.014;m.segments=1
 return o
def glazing(name,a,b,z0,z1,material,frame,col,parent):
 ax,ay=a;bx,by=b
 o=mesh(name+' pane',[(ax,ay,z0),(bx,by,z0),(bx,by,z1),(ax,ay,z1)],[(0,1,2,3)],material,col,parent)
 for x,y in [a,b]:beam(name+' jamb',(x,y,z0),(x,y,z1),.065,.085,frame,col,parent)
 for z in [z0,z1]:beam(name+' sill/head',(ax,ay,z),(bx,by,z),.065,.085,frame,col,parent)
 return o
def text(name,body,loc,size,material,col,parent=None,rotation=(math.pi/2,0,0)):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.size=size;cu.extrude=.003
 o=bpy.data.objects.new(name,cu);col.objects.link(o);o.location=loc;o.rotation_euler=rotation;cu.materials.append(material)
 if parent:o.parent=parent
 return o
def main_h(v):
 if v<4:return .4*max(0,v)/4
 if v<6.4:return .4+math.floor((v-4)/.4+1e-6)*(1.042857142857/6)
 if v<14.4:return 1.442857142857
 if v<18:return 1.442857142857+math.floor((v-14.4)/(3.6/11)+1e-6)*((3.36-1.442857142857)/11)
 if v<28:return 3.36
 if v<30:return 3.36+math.floor((v-28)/.5+1e-6)*.16
 return 4.0
