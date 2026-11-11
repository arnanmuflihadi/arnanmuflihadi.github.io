"""Read-only export checks and cost records for S2-B; no production mutations."""
import json,struct,hashlib,csv,io
from pathlib import Path
from collections import defaultdict
from PIL import Image
V=Path(__file__).resolve().parent;ROOT=V.parents[1];D=ROOT/'docs/urban-atlas/storefront-s2b';D.mkdir(parents=True,exist_ok=True)
audit=json.loads((V/'source-geometry-audit.json').read_text());before={r['name']:r for r in audit['before']}
costs=defaultdict(lambda:{'before':0,'after':0,'objects':0})
with (D/'geometry-by-object.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['object','component','original_triangles','optimized_editable_triangles','changes'])
 for r in audit['optimizedEditable']['objects']:
  old=before[r['object']]['triangles'];c=costs[r['component']];c['before']+=old;c['after']+=r['optimized_triangles'];c['objects']+=1
  w.writerow([r['object'],r['component'],old,r['optimized_triangles'],json.dumps(r['changes'])])
exports=[]
for p in sorted(V.glob('*.glb')):
 raw=p.read_bytes();assert raw[:4]==b'glTF' and struct.unpack_from('<I',raw,4)[0]==2 and struct.unpack_from('<I',raw,8)[0]==len(raw)
 n=struct.unpack_from('<I',raw,12)[0];j=json.loads(raw[20:20+n]);binary=raw[28+n:]
 assert len(j['scenes'])==1
 assert all('uri' not in x for x in j.get('images',[]));assert all('uri' not in x for x in j.get('buffers',[]))
 tris=0;comp={};primitives=0
 for mi,m in enumerate(j['meshes']):
  t=0
  for pr in m['primitives']:
   assert 'NORMAL' in pr['attributes'];assert pr.get('mode',4)==4
   cnt=j['accessors'][pr['indices']]['count'];assert cnt%3==0;t+=cnt//3;primitives+=1
  node=next(n for n in j['nodes'] if n.get('mesh')==mi)
  comp[node.get('extras',{}).get('module',node.get('name',m['name']))]=t;tris+=t
 for node in j['nodes']:assert all(abs(v-1)<1e-6 for v in node.get('scale',[1,1,1]))
 images=[]
 for im in j.get('images',[]):
  bv=j['bufferViews'][im['bufferView']];off=bv.get('byteOffset',0)
  with Image.open(io.BytesIO(binary[off:off+bv['byteLength']])) as image:images.append({'size':image.size,'mime':im['mimeType']})
 exports.append({'file':p.name,'bytes':len(raw),'triangles':tris,'primitives':primitives,'module_meshes':len(j['meshes']),'component_triangles':comp,'materials':len(j.get('materials',[])),'embedded_images':images,'extensions':j.get('extensionsUsed',[]),'sha256':hashlib.sha256(raw).hexdigest()})
base=json.loads((V/'baseline-hashes.json').read_text());changed=[k for k,h in base.items() if not (ROOT/k).exists() or hashlib.sha256((ROOT/k).read_bytes()).hexdigest()!=h]
assert not changed,changed
report={'components':dict(costs),'exports':exports,'preservation':{'checked_files':len(base),'changed':changed,'approved_s2a_sha256':base['validation/storefront-s2a/kopi-awan-prototype.blend']},'checks':'GLB headers, active scene only, embedded images, triangle modes/counts, normals, unit node scales, decoded image dimensions, SHA256 preservation'}
(D/'geometry-costs.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
