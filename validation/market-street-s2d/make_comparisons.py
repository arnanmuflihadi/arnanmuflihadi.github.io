"""Lay out unchanged captured pixels for review; never synthesizes scene imagery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];V=Path(__file__).resolve().parent;D=R/'docs/urban-atlas/market-street-s2d'
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',25)
def sheet(name,items,cols=2):
 w,h=900,600;rows=(len(items)+cols-1)//cols
 out=Image.new('RGB',(cols*w,rows*(h+48)),(239,235,224));draw=ImageDraw.Draw(out)
 for i,(file,label) in enumerate(items):
  im=Image.open(file).convert('RGB');im=im.resize((w,h),Image.Resampling.LANCZOS);x=(i%cols)*w;y=(i//cols)*(h+48)
  draw.text((x+16,y+11),label,font=font,fill=(33,60,54));out.paste(im,(x,y+48))
 out.save(D/name,quality=93)
sheet('street-comparison.jpg',[(V.parent/'market-street-s2c/01-arrival.png','Approved Blender camera'),(V/'01-browser-arrival.png','Actual Three.js · same camera / authored glass')])
sheet('aerial-comparison.jpg',[(V.parent/'market-street-s2c/03-elevated.png','Approved Blender aerial'),(V/'02-browser-elevated.png','Actual Three.js · same camera')])
sheet('island-evidence.jpg',[(V/'06-island-skyport.png','Skyport reservation · original island'),(V/'05-island-market.png','Market → square · forest termination'),(V/'07-island-opposite.png','Opposite pedestrian view'),(V/'08-island-elevations.png','Rear elevations · natural terrain'),(V/'09-island-context.png','Whole-island context · no terrain edits'),(V/'17-foundation-closeup.png','Exposed undersides · grading removed')])
sheet('glass-comparison.jpg',[(V/'13-authored-glass-detail.png','Authored transmission · retained in GLB'),(V/'12-alpha-glass-detail.png','Optional alpha study · explicitly selected')])
print('Four comparison sheets saved; raw captures remain unchanged.')
