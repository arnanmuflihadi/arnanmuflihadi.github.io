"""Focused art/geometry corrections after actual player-height inspections."""
s=bpy.data.scenes['S2C Market Street'];bpy.context.window.scene=s
land=bpy.data.collections['S2C / Landscape'];props=bpy.data.collections['S2C / Props'];cams=bpy.data.collections['S2C / Cameras']
wood=bpy.data.materials['S2A / oiled tropical timber'];timber=bpy.data.materials['S2A / cut timber edges'];stone=bpy.data.materials['S2A / sandstone base'];bronze=bpy.data.materials['S2A / patinated bronze frames'];brass=bpy.data.materials['S2A / aged brass'];cream=bpy.data.materials['S2A / warm sign lettering'];sage=bpy.data.materials['S2A / recessed sage plaster'];flatglass=bpy.data.materials['S2C / shared low-cost teal glazing']
# Remove upper-storey sill remnants that protruded through the atelier's lower roof.
r3=bpy.data.objects['B3 Rupa Rimba Atelier']
for o in list(r3.children):
 if 'window stone sill' in o.name.lower():bpy.data.objects.remove(o,do_unlink=True)
# Fit the corner return glazing to its actual chamfer, instead of leaving the old full bay.
r4=bpy.data.objects['B4 Serambi Corner Shop'];c4=bpy.data.collections['S2C / B4 Serambi Corner Shop']
for o in list(r4.children):
 if 'side shop' in o.name.lower() and o.location.x<0 and o.location.y<0:bpy.data.objects.remove(o,do_unlink=True)
glazing('Fitted square-facing corner window',(-3.61,-2.15),(-3.61,-.4),.3,2.91,flatglass,bronze,c4,r4)

# A perpendicular bookshop blade gives arrival an identity beyond repeated window frames.
r2=bpy.data.objects['B2 Lembaran Shophouse'];c2=bpy.data.collections['S2C / B2 Lembaran Shophouse']
beam('Bookshop sign bracket',(2.9,-3.6,3.15),(2.9,-4.6,3.15),.045,.055,bronze,c2,r2)
box('Bookshop hanging blade',(2.9,-4.24,2.83),(.06,.70,.60),sage,c2,r2)
text('Bookshop blade letters','BUKU',(2.94,-4.24,2.75),.16,cream,c2,r2,rotation=(math.pi/2,0,math.pi/2))

# Layered pinnate palm leaves, preserving shared geometry for linked planting instances.
for o in list(land.objects):
 if not o.name.startswith('Original layered palm frond') or len(o.data.vertices)!=27:continue
 centers=[o.data.vertices[j*3+1].co.copy() for j in range(9)];widths=[(o.data.vertices[j*3+2].co-o.data.vertices[j*3].co).length/2 for j in range(9)]
 vs=[];fs=[]
 for j in range(8):
  a,b=centers[j],centers[j+1];d=(b-a).normalized();side=d.cross(Vector((0,0,1))).normalized();k=len(vs)
  vs.extend([tuple(a+side*.015),tuple(a-side*.015),tuple(b-side*.008),tuple(b+side*.008)]);fs.append((k,k+1,k+2,k+3))
 for j in range(1,8):
  center=centers[j];direction=(centers[min(8,j+1)]-centers[max(0,j-1)]).normalized();side=direction.cross(Vector((0,0,1))).normalized()
  for sign in [-1,1]:
   tip=center+side*sign*(widths[j]*1.25+.08)+direction*.10-Vector((0,0,.07));mid=center.lerp(tip,.48);k=len(vs)
   vs.extend([tuple(center),tuple(mid+direction*.045),tuple(tip),tuple(mid-direction*.045)]);fs.append((k,k+1,k+2,k+3))
 o.data.clear_geometry();o.data.from_pydata(vs,[],fs);o.data.update()

# Two palms frame the middle landing without placing trunks in the walking route.
template=[o for o in land.objects if o.name=='Original stylized palm trunk' or o.name=='Original layered palm frond' or (o.name.startswith('Original layered palm frond.') and int(o.name.rsplit('.',1)[1])<=9)]
terrain=bpy.data.objects['Measured terrain / local art grading proposal']
def ground_at(x,y):
 best=1e12;z=0
 for v in terrain.data.vertices:
  distance=(v.co.x-x)**2+(v.co.y-y)**2
  if distance<best:best=distance;z=v.co.z
 return z
originalbase=Vector((-13.5,4.2,ground_at(-13.5,4.2)))
for x,y,angle in [(-6.5,16.2,.5),(6.4,16.2,-.7)]:
 dest=Vector((x,y,ground_at(x,y)));transform=Matrix.Translation(dest)@Matrix.Rotation(angle,4,'Z')@Matrix.Diagonal((.82,.82,.82,1))@Matrix.Translation(-originalbase)
 for ob in template:
  o=ob.copy();land.objects.link(o);o.name='Middle landing shared palm';o.matrix_world=transform

# Arrival can see the actual square direction sign, rather than an unbuilt Guild mass.
beam('Square direction marker post',(3.5,28.5,3.52),(3.5,28.5,6.7),.08,.08,bronze,props)
box('Square direction marker',(3.5,28.5,6.35),(2.0,.10,.45),sage,props)
text('Square direction heading','ALUN-ALUN  >',(3.5,28.43,6.24),.19,cream,props)
box('Guild direction marker',(3.5,28.5,5.86),(2.0,.10,.32),sage,props)
text('Guild direction heading','BALAI ATLAS  >',(3.5,28.43,5.78),.16,cream,props)

# Physical daylight sky, with the sun disc disabled because the scene has a directional sun.
world=s.world;bg=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
sky=world.node_tree.nodes.new('ShaderNodeTexSky');available=[e.identifier for e in sky.bl_rna.properties['sky_type'].enum_items];sky.sky_type=next(e for e in available if e=='MULTIPLE_SCATTERING');sky.sun_disc=False;sky.sun_elevation=math.radians(48);sky.sun_rotation=-.6
world.node_tree.links.new(sky.outputs['Color'],bg.inputs['Color']);bg.inputs['Strength'].default_value=.30
s.camera=bpy.data.objects['S2C Arrival'];s.cycles.samples=32
bpy.context.view_layer.update();bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=OUT+'market-street.blend')
print('FOCUSED_STREET_POLISH_SAVED')
