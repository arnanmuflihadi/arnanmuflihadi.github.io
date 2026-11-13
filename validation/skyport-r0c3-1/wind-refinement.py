import bpy,math
s=bpy.context.scene;c=bpy.data.collections['C3.1 / Editable additions'];wood=bpy.data.materials['C1 / oiled timber'];bronze=bpy.data.materials['C1 / weathered bronze'];jade=next(m for m in bpy.data.materials if m.name.startswith('Skyport / enamel jade'))
for o in list(c.objects):
 if any(o.name.startswith(n)for n in ['Jade wind pennant','Bronze wind-direction chevron','Wind-standard arm']):bpy.data.objects.remove(o,do_unlink=True)
x,y,z=-4.6,-1.3,.04417677556889465
def mesh(name,v,f,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.materials.append(mat);me.update();o=bpy.data.objects.new(name,me);c.objects.link(o);return o
verts=[];n=12;rows=7
for i in range(rows):
 t=i/(rows-1);r=.23*(1-t)+.075*t
 for j in range(n):
  a=j*math.tau/n;verts.append((x-.28-1.12*t,y+.04*t+r*math.cos(a),z+4.30-.18*t+r*math.sin(a)))
me=bpy.data.meshes.new('Static wind sleeve');me.from_pydata(verts,[],[(i*n+j,(i+1)*n+j,(i+1)*n+(j+1)%n,i*n+(j+1)%n)for i in range(rows-1)for j in range(n)]);me.materials.append(jade);me.materials.append(bronze)
for p in me.polygons:p.material_index=1 if p.index//n in [0,3]else 0
me.update();o=bpy.data.objects.new('Static jade and bronze wind sleeve / no animation',me);c.objects.link(o)
# Slim bracket physically attaches the sleeve mouth; the old long flag arm is omitted.
v=[(x+dx,y+dy,z+dz)for dx,dy,dz in[(-.38,-.05,4.54),(.10,-.05,4.54),(.10,.05,4.54),(-.38,.05,4.54),(-.38,-.05,4.64),(.10,-.05,4.64),(.10,.05,4.64),(-.38,.05,4.64)]]
mesh('Wind sleeve bronze mounting arm',v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],bronze)
print('Replaced flat flag with a tapered static wind sleeve on the same mast; no extra materials')
