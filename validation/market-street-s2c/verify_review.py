"""S2-C artifact/preservation checks only; no production tests, export or mutation."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'validation/market-street-s2c';D=ROOT/'docs/urban-atlas/market-street-s2c';D.mkdir(parents=True,exist_ok=True)
baseline=json.loads((V/'baseline-hashes.json').read_text());changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
m=json.loads((V/'metrics.json').read_text());assert len(m['buildings'])==4
assert all(im['packed'] and im['has_data'] for im in m['textures'])
assert not list(V.glob('*.glb')),'S2-C must not export a new GLB'
c=json.loads((V/'circulation-check.json').read_text());assert not c['blockers']
evidence=[]
for p in sorted(V.glob('0*.png')):
 with Image.open(p) as image:
  image.verify()
 with Image.open(p) as image:size=image.size
 evidence.append({'file':p.name,'size':size,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(evidence)==6
with (D/'geometry-by-object.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['name','category','triangles','material_slots']);w.writeheader();w.writerows(m['object_costs'])
native=V/'market-street.blend'
report={'protected_files_checked':len(baseline),'changed':changed,'approved_assets_unchanged':True,'main_scene':'S2C Market Street','building_count':4,'total_evaluated_triangles':m['total_triangles'],'material_count':m['material_count'],'packed_images':len(m['textures']),'central_corridor_AABB_check':c,'new_glb_exports':0,'production_game_tests':'not run; isolated Blender art phase','browser_rendering':'not tested; S2-C export/integration explicitly prohibited','native':{'file':str(native.relative_to(ROOT)),'bytes':native.stat().st_size,'sha256':hashlib.sha256(native.read_bytes()).hexdigest()},'renders':evidence}
(V/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['renders','central_corridor_AABB_check']},indent=2))
