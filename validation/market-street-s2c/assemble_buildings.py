"""Build four related storefronts from approved S2-B components; no export."""
assert bpy.data.filepath.startswith(OUT),'Independent S2-C project required'
assert 'S2C Market Street' not in bpy.data.scenes,'Edit the existing slice rather than duplicate it'
src=bpy.data.scenes['S2B Editable Modules'];batched=bpy.data.scenes['S2B Native Batched LOD0'];roofBscene=bpy.data.scenes['S2B Roof B Export']
source_transforms={}
for scene in [src,batched,roofBscene]:
 bpy.context.window.scene=scene;bpy.context.view_layer.update()
 for ob in scene.objects:source_transforms[ob.name]=ob.matrix_world.copy()
s=bpy.data.scenes.new('S2C Market Street');bpy.context.window.scene=s;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
rootcol=bpy.data.collections.new('S2C / Buildings');s.collection.children.link(rootcol)
cream=bpy.data.materials['S2A / warm lime plaster'];wood=bpy.data.materials['S2A / oiled tropical timber'];timber=bpy.data.materials['S2A / cut timber edges'];stone=bpy.data.materials['S2A / sandstone base'];bronze=bpy.data.materials['S2A / patinated bronze frames'];brass=bpy.data.materials['S2A / aged brass'];signink=bpy.data.materials['S2A / warm sign lettering'];sage=bpy.data.materials['S2A / recessed sage plaster']
ochre=mat('soft ochre plaster',(.66,.49,.30));clay=mat('dusty clay plaster',(.53,.29,.19));ivory=mat('corner ivory plaster',(.80,.73,.56))
flatglass=mat('shared low-cost teal glazing',(.15,.29,.29),.22,.20)
p=next(n for n in flatglass.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Alpha'].default_value=.62
opaque=mat('upper blue green glazing',(.14,.29,.28),.26,.28)
def copy_ob(ob,col,parent,name=None):
 o=ob.copy();o.name=name or ob.name;o.parent=None;col.objects.link(o)
 o.parent=parent;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=source_transforms[ob.name].copy();return o
def palette(o,plaster=None,cheapglass=False):
 if o.type!='MESH':return
 replacements=[]
 for old in o.data.materials:
  replacements.append(plaster if old==cream and plaster else flatglass if cheapglass and old and 'soft blue green glass' in old.name else old)
 if any(a!=b for a,b in zip(replacements,o.data.materials)):
  o.data=o.data.copy();o.data.materials.clear()
  for m in replacements:o.data.materials.append(m)
def newbuilding(name):
 c=bpy.data.collections.new('S2C / '+name);rootcol.children.link(c);r=bpy.data.objects.new(name,None);c.objects.link(r);r['building']=name;r['units']='metres';return c,r
def source_parts(col,root,variant,plaster=None,cheapglass=False):
 out=[]
 for ob in src.objects:
  if ob.type not in ['MESH','FONT'] or not ob.get('module') or ob.get('module')=='Roof B':continue
  keep=keep2(ob) if variant==2 else keep3(ob) if variant==3 else keep4(ob)
  if not keep:continue
  o=copy_ob(ob,col,root);palette(o,plaster,cheapglass);out.append(o)
 return out
def roof_b(col,root,offset=0):
 ob=next(o for o in roofBscene.objects if o.type=='MESH');o=copy_ob(ob,col,root,'Reused editable roof B assembly');o.location.z+=offset;o['module']='Roof B';return o
def place(root,loc,angle,scale=(1,1,1)):
 root.location=loc;root.rotation_euler.z=angle;root.scale=scale

# 1: approved café preserved as the full S2-B optimized assembly, including roof A.
c1,r1=newbuilding('B1 Kopi Awan')
for ob in batched.objects:
 if ob.type=='MESH' and ob.get('module'):copy_ob(ob,c1,r1)
place(r1,(-8.3,10,1.442857142857-.24),math.pi/2)
r1['design']='Approved cafe identity, roof A, 7.2m frontage; source unchanged'

# 2: narrower bookshop; same construction kit, different upper opening rhythm.
c2,r2=newbuilding('B2 Lembaran Shophouse')
def keep2(o):
 n=o.name.lower()
 return o.get('module') not in ['Roof A','Sun screens','Decorative props','Interior'] and not any(a in n for a in ['terrace facade','balcony sliding glazing','upper east glazing'])
source_parts(c2,r2,2,ochre,True);roof_b(c2,r2)
holes=[(-3.05,-1.65,3.95,6.02),(-1.35,.05,3.95,6.02),(.35,1.75,3.95,6.02)]
wall('B2 three-bay upper facade',-3.6,3.6,3.5,6.45,-2.85,holes,ochre,c2,r2)
for a,b,lo,hi in holes:
 glazing('B2 timber window',(a,-2.90),(b,-2.90),lo,hi,opaque,timber,c2,r2)
 beam('B2 sill shade',(a-.08,-3.15,lo-.05),(b+.08,-3.15,lo-.05),.12,.25,timber,c2,r2)
for i in range(9):box('B2 compact louver',(2.0+i*.13,-3.13,5.05),(.065,.10,1.95),wood,c2,r2)
box('Lembaran shop sign',(-1.85,-3.74,3.01),(2.8,.11,.40),sage,c2,r2)
text('Lembaran letters','LEMBARAN',(-1.85,-3.81,2.92),.26,signink,c2,r2)
# Only shallow book-display geometry visible from the street, no complete interior.
for z in [.7,1.2,1.7]:box('Bookshop display ledge',(-1.8,-2.8,z),(2.7,.45,.065),timber,c2,r2)
for i in range(12):box('Book display volume',(-3.0+i*.21,-2.72,1.39),(.13,.22,.32+(i%3)*.04),[sage,clay,cream][i%3],c2,r2,edge=.005)
place(r2,(8.3,11.2,1.634285714286-.24),-math.pi/2,(.82,.93,1))
r2['design']='5.9m frontage; three timber windows, ochre plaster, narrow arcade, roof B'

# 3: one-storey artisan shop with deep open/recessed bays and a lower covered terrace.
c3,r3=newbuilding('B3 Rupa Rimba Atelier')
def keep3(o):
 n=o.name.lower();cat=o.get('module')
 if cat in ['Roof A','Sun screens','Balcony','Planters','Decorative props','Interior']:return False
 if any(v in n for v in ['upper','terrace facade','balcony sliding','kenney','roof ceiling','roof header']):return False
 if cat=='Building shell' and 'rear upper wall' in n:return False
 return True
parts3=source_parts(c3,r3,3,clay,False)
for o in list(parts3):
 n=o.name.lower()
 if ('display' in n and 'glass' in n) or ('entrance' in n and 'glass' in n):bpy.data.objects.remove(o,do_unlink=True)
 elif any(t in n for t in ['west display','east display','entrance','door pull']):o.location.y+=.65
# Reuse the upper-floor slab as the veranda ceiling; roof B becomes a lower single-storey hip.
floor=next(o for o in src.objects if o.name=='S2A / upper floor');copy_ob(floor,c3,r3,'Atelier reused canopy slab')
roof_b(c3,r3,-3.1)
for y in [-4.1,-2.9]:beam('Atelier canopy header',(-3.5,y,3.48),(3.5,y,3.48),.14,.18,timber,c3,r3)
for i in range(14):box('Atelier ventilated attic blade',(-3.2+i*.49,-2.9,3.52),(.26,.08,.30),wood,c3,r3)
for x in [-3.20,3.20]:
 for i in range(8):box('Atelier side terrace screen',(x,-4.08+i*.16,1.65),(.08,.085,2.4),wood,c3,r3)
box('Atelier shop sign',(0,-3.75,3.06),(3.3,.10,.38),wood,c3,r3)
text('Atelier lettering','RUPA RIMBA',(0,-3.82,2.97),.27,signink,c3,r3)
box('Artisan display counter',(-1.9,-2.35,.72),(2.4,.65,.95),timber,c3,r3)
for i in range(7):
 # Revolved pottery silhouettes are a small authored shop detail, not prefab buildings.
 vs=[];fs=[];profile=[(0,.10),(.08,.16),(.29,.19),(.42,.10),(.47,.11)]
 for zz,rr in profile:
  for k in range(12):a=2*math.pi*k/12;vs.append((-2.8+i*.30+rr*math.cos(a),-2.35+rr*math.sin(a),1.21+zz))
 for j in range(len(profile)-1):
  for k in range(12):a=j*12+k;b=j*12+(k+1)%12;fs.append((a,b,b+12,a+12))
 mesh('Artisan pottery',vs,fs,[clay,ochre,sage][i%3],c3,r3)
place(r3,(-8.3,21.8,3.36-.24),math.pi/2,(1.11,.93,1))
r3['design']='8m single-storey recessed open atelier; lower roof B; screened covered terrace'

# 4: a corner shop with a genuinely chamfered ground-floor entrance and square-facing terrace.
c4,r4=newbuilding('B4 Serambi Corner Shop')
def keep4(o):
 n=o.name.lower()
 return o.get('module') not in ['Decorative props','Interior'] and not any(t in n for t in ['shop facade','west shop wall','west display','door pull'])
source_parts(c4,r4,4,ivory,True)
wall('Corner front wall',-2.35,3.6,.20,3.23,-3.55,[(-2.20,-.67,.28,2.94),(-.48,1.08,.24,2.94),(1.27,3.23,.28,2.94)],ivory,c4,r4)
ob=wall('Corner square return wall',-5,2.30,.20,3.23,3.6,[(-2.8,-.8,1.0,2.7),(.4,2.15,.28,2.94)],ivory,c4,r4,-math.pi/2);ob.location.x=-7.2
glazing('Corner front display',(-2.2,-3.52),(-.67,-3.52),.30,2.91,flatglass,bronze,c4,r4)
glazing('Chamfered corner entrance',(-3.59,-2.30),(-2.35,-3.54),.25,2.91,flatglass,timber,c4,r4)
beam('Corner entrance pull',(-2.98,-2.93,1.0),(-2.98,-2.93,1.55),.035,.035,brass,c4,r4)
beam('Corner lintel',(-3.6,-2.30,3.10),(-2.35,-3.55,3.10),.16,.20,timber,c4,r4)
# Extend the upper terrace around the square-facing side: this corner treatment has purpose.
box('Square-facing balcony deck',(-4.1,-.65,3.40),(1.05,4.7,.19),stone,c4,r4)
for y in [-2.8,-.6,1.5]:beam('Corner balcony upright',(-4.52,y,3.5),(-4.52,y,4.6),.05,.05,bronze,c4,r4)
beam('Corner balcony return handrail',(-4.52,-2.9,4.6),(-4.52,1.7,4.6),.08,.10,timber,c4,r4)
for z in [3.8,4.05,4.3]:beam('Corner return rail',(-4.52,-2.9,z),(-4.52,1.7,z),.025,.025,bronze,c4,r4)
box('Corner street sign',(1.9,-3.75,3.03),(2.3,.10,.38),sage,c4,r4)
text('Corner letters','SERAMBI',(1.9,-3.82,2.95),.27,signink,c4,r4)
# A sign on the square return makes the turn legible at pedestrian height.
o=box('Corner return sign',(-3.76,-.6,2.96),(.10,2.4,.42),sage,c4,r4)
text('Square-facing letters','SERAMBI',(-3.83,-.6,2.84),.27,signink,c4,r4,rotation=(math.pi/2,0,-math.pi/2))
place(r4,(8.3,22.6,3.36-.24),-math.pi/2,(1.11,.96,1))
r4['design']='8m corner shop; chamfered entrance; wraparound square-facing balcony; roof A'
bpy.context.view_layer.update()
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=OUT+'market-street.blend')
print('FOUR_REUSED_STOREFRONTS_READY',len(s.objects))
