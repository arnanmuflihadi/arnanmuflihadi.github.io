"""Source preservation, actual payload cost and terrain-contact checks."""
from pathlib import Path
import hashlib,json,struct
from PIL import Image,ImageStat
V=Path(__file__).resolve().parent;R=V.parents[1]
baseline=json.loads((V/'baseline-hashes.json').read_text());changed=[p for p,h in baseline.items() if not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
metrics={}
for p in V.glob('*.glb'):
 b=p.read_bytes();assert struct.unpack_from('<III',b)==(0x46546c67,2,len(b));n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);metrics[p.name]={'bytes':len(b),'triangles':sum(g['accessors'][x['indices']]['count']//3 for m in g.get('meshes',[]) for x in m['primitives']),'primitives':sum(len(m['primitives']) for m in g.get('meshes',[])),'materials':len(g.get('materials',[]))}
assert metrics['foundation-hybrid.glb']['triangles']==7248
assert metrics['common-interface.glb']['triangles']>8000
assert metrics['support-reference.glb']['triangles']==100
m=json.loads((V/'site-manifest.json').read_text());selected=[c for c in m['contacts'] if c['collection']!='S2E / B Braced']
assert all(all(b<=g-.1999 for b,g in zip(c['corner_bases'],c['corner_terrain'])) for c in selected)
assert len(m['landscape_alignment'])==4
d=json.loads((V/'final-seam-tests.json').read_text());assert len(d['seamResults']['tests'])==12 and all(t['success'] for t in d['seamResults']['tests'])
assert not d['errors']
for name in ['walk-two-way.json','ramp-two-way.json','movement-tests.json']:
 d=json.loads((V/name).read_text());assert not d['errors'];assert all(t['success'] for t in d['traversal'])
renders=[]
for p in sorted(V.glob('*.png')):
 with Image.open(p) as im:im.load();size=im.size;variance=max(ImageStat.Stat(im.convert('RGB')).stddev)
 assert variance>3,(p.name,'empty render')
 renders.append({'file':p.name,'size':size,'bytes':p.stat().st_size})
visible=metrics['common-interface.glb']['triangles']+metrics['foundation-hybrid.glb']['triangles'];payload=metrics['common-interface.glb']['bytes']+metrics['foundation-hybrid.glb']['bytes']
result={'protected_files':len(baseline),'changed':changed,'original_glb_bytes':(R/'validation/market-street-s2d/market-street-optimized.glb').stat().st_size,'exports':metrics,'selected_visible_triangles':visible,'selected_visible_payload_bytes':payload,'separate_collision_triangles':100,'selected_footings_checked':len(selected),'all_footing_corners_embedded':True,'four_standalone_canopies_aligned':m['landscape_alignment'],'fixed_controller_tests':12,'renders':renders,'human_design_approval':'pending','production_deployment':False}
(V/'export-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');(V/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['renders','exports','four_standalone_canopies_aligned']},indent=2))
