from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
out=Path(__file__).parent
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',22)
def pair(left,right,name,label_left,label_right,crop_right=False):
 a=Image.open(left).convert('RGB');b=Image.open(right).convert('RGB')
 if crop_right:b=b.crop((0,64,1280,720))
 assert a.size==b.size,(name,a.size,b.size)
 w,h=a.size;im=Image.new('RGB',(w*2,h+42),'#f3eddf');im.paste(a,(0,42));im.paste(b,(w,42));d=ImageDraw.Draw(im);d.text((18,10),label_left,font=font,fill='#173a37');d.text((w+18,10),label_right,font=font,fill='#173a37');im.save(out/name,quality=93)
for n in ['01-market-arrival','02-square-interior','03-elevated-town','04-square-foundations','05-full-island']:
 pair(out/('before-'+n+'.jpg'),out/(n+'.jpg'),'comparison-'+n+'.jpg','Square OFF / accepted C1A.5','Square ON / C1B')
for n in ['arrival','interior','elevated']:
 pair(out/('blender-'+n+'.png'),out/('browser-match-'+n+'.jpg'),'comparison-blender-'+n+'.jpg','Blender derivative / existing Cycles daylight','Actual game / existing daylight + Glass B',True)
r=[]
for p in out.glob('*.jpg'):
 if p.name.startswith(('0','before-0','comparison-','browser-match-')):r.append({'file':p.name,'pixels':Image.open(p).size})
(out/'image-dimensions.json').write_text(json.dumps(r,indent=2))
print('5 OFF/ON pairs and 3 Blender/browser sheets; raw images preserved')
