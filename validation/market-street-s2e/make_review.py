"""Arrange actual captured pixels; no synthesized environment imagery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
V=Path(__file__).resolve().parent;D=V.parents[1]/'docs/urban-atlas/market-street-s2e';D.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',25)
def sheet(name,items,cols=2):
 w,h=900,600;rows=(len(items)+cols-1)//cols;out=Image.new('RGB',(w*cols,(h+48)*rows),(239,235,224));draw=ImageDraw.Draw(out)
 for i,(file,label) in enumerate(items):
  im=Image.open(V/file).convert('RGB').resize((w,h),Image.Resampling.LANCZOS);x=i%cols*w;y=i//cols*(h+48);draw.text((x+14,y+10),label,font=font,fill=(33,60,54));out.paste(im,(x,y+48))
 out.save(D/name,quality=93)
for key,title in [('arrival','Skyport arrival'),('foundations','Foundation / actual slope'),('market','Market at player eye height'),('square','Square threshold'),('aerial','Complete interface')]:sheet(key+'-comparison.jpg',[(f'before-{key}.png',title+' · baseline'),(f'after-{key}.png',title+' · hybrid proposal')])
sheet('native-alternatives.jpg',[('blender-a-side.png','Blender A · terraced stone bases'),('blender-b-side.png','Blender B · braced supports')])
sheet('browser-alternatives.jpg',[('alternative-A.png','Browser A · terraced bases'),('alternative-B.png','Browser B · braced supports'),('after-foundations.png','Browser · selected hybrid')],3)
print('Seven comparison sheets saved; raw renders and captures retained.')
