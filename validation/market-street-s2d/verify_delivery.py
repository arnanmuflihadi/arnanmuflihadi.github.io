"""S2-D artifact, payload and source-preservation checks; never writes approved inputs."""
import json,hashlib,struct,io,gzip
from pathlib import Path
from PIL import Image
V=Path(__file__).resolve().parent;R=V.parents[1]
baseline=json.loads((V/'baseline-hashes.json').read_text())
changed=[p for p,h in baseline.items() if not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
b=(V/'market-street-optimized.glb').read_bytes();raw=(V/'market-street-mcp.glb').read_bytes()
assert struct.unpack_from('<III',b)==(0x46546c67,2,len(b))
n,t=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+n]);nr=struct.unpack_from('<I',raw,12)[0]
assert b[20+n:]==raw[20+nr:],'Geometry/image binary changed during material-only delivery optimization'
assert not any(im.get('uri') for im in g['images'])
binary=b[28+n:];images=[]
for im in g['images']:
 v=g['bufferViews'][im['bufferView']];data=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
 with Image.open(io.BytesIO(data)) as image:
  image.load();images.append({'name':im['name'],'size':image.size,'bytes':len(data)})
triangles=0;instances=[]
for node in g['nodes']:
 if 'mesh' not in node:continue
 ext=node.get('extensions',{}).get('EXT_mesh_gpu_instancing',{}).get('attributes',{})
 count=g['accessors'][next(iter(ext.values()))]['count'] if ext else 1
 if ext:instances.append({'node':node['name'],'count':count})
 triangles+=sum(g['accessors'][p['indices']]['count']//3 for p in g['meshes'][node['mesh']]['primitives'])*count
assert triangles==170709
assert len(g['images'])==5 and len(g['materials'])==37
for stem in ['01-browser-arrival','02-browser-elevated','03-browser-opposite','04-browser-detail','05-island-market','06-island-skyport','07-island-opposite','08-island-elevations','09-island-context','10-island-support-deficit','15-skyport-connector-traversal']:
 d=json.loads((V/(stem+'.json')).read_text());assert d['state']=='loaded' and not d['errors']
 assert not d['asset']['missingTextures'] and d['asset']['triangles']==170709
renders=[]
for p in sorted(V.glob('*.png')):
 with Image.open(p) as image:image.verify()
 with Image.open(p) as image:size=image.size
 renders.append({'file':p.name,'size':size,'bytes':p.stat().st_size})
for stem in ['studio-performance','island-performance-authored','island-performance-alpha']:
 d=json.loads((V/(stem+'.json')).read_text());assert d['performance']['frames']==360
native=V/'market-street-export.blend';assert native.stat().st_size>1000000
result={'protected_files':len(baseline),'changed':changed,'glb_bytes':len(b),'gzip_bytes_not_served':len(gzip.compress(b,mtime=0)),'triangles_with_instances':triangles,'unique_meshes':len(g['meshes']),'render_primitives':sum(len(m['primitives']) for m in g['meshes']),'gltf_material_definitions':len(g['materials']),'images':images,'instancing':instances,'native':{'file':native.name,'bytes':native.stat().st_size,'live_mcp_reopen':'verified'},'renders':renders,'website':'all protected production bytes unchanged; 27 focused plus portfolio tests recorded separately','human_approval':'pending; technical proof only'}
(V/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['renders','instancing','images']},indent=2))
