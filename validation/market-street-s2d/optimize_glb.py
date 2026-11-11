"""Lossless geometry; cutout foliage avoids unnecessary blended draws."""
import json,struct,shutil
from pathlib import Path
v=Path(__file__).resolve().parent;p=v/'market-street-optimized.glb'
raw=v/'market-street-mcp.glb'
if not raw.exists():shutil.copyfile(p,raw)
b=raw.read_bytes();n,t=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+n]);tail=b[20+n:]
changed=[]
for m in g['materials']:
 if m.get('name')=='Leaves.001' and m.get('alphaMode')=='BLEND':
  m['alphaMode']='MASK';m['alphaCutoff']=.4;changed.append(m['name'])
j=json.dumps(g,separators=(',',':'),ensure_ascii=False).encode();j+=b' '*((-len(j))%4)
out=struct.pack('<III',0x46546c67,2,20+len(j)+len(tail))+struct.pack('<II',len(j),0x4e4f534a)+j+tail
p.write_bytes(out)
(v/'delivery-optimization.json').write_text(json.dumps({'mcp_export_bytes':len(b),'delivery_bytes':len(out),'geometry_changed':False,'foliage_alpha_mask':changed,'alpha_cutoff':.4,'glass_transmission_preserved':True},indent=2)+'\n')
print('Delivered bytes',len(out),'foliage cutout',changed)
