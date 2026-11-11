from pathlib import Path
import hashlib,json,struct
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
baseline=json.loads((OUT/'before-hashes.json').read_text());changed=[p for p,h in baseline.items()if not (ROOT/p).is_file()or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
site=json.loads((OUT/'site-plan.json').read_text());checks=site['detailed_checks'];captures=[]
for name in ['01-market-arrival.png','02-square-interior.png','03-elevated.png','04-measured-plan.png']:
 p=OUT/name;b=p.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';size=list(struct.unpack('>II',b[16:24]));assert size==[1800,1200];captures.append({'file':name,'resolution':size,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
native=OUT/'town-square-design.blend';header=native.read_bytes()[:12];assert header.startswith((b'BLENDER',b'\x28\xb5\x2f\xfd',b'\x1f\x8b'))
assert not changed
assert not site['context_preservation']['transform_differences']
assert checks['deck_edge_floor_to_ground_min_m']>0
assert checks['landing_stair_top_to_terrain_min_m']>0
assert checks['minimum_guard_face_clear_width_m']>2.4
assert all(i['packed']and min(i['size'])>0 for i in checks['packed_source_images'])
result={'phase':'R0-C1A DESIGN ONLY','protected_files_checked':len(baseline),'protected_files_changed':changed,'copied_context_transforms_checked':site['context_preservation']['objects_compared'],'transform_differences':[],'native_file':str(native.relative_to(ROOT)),'native_bytes':native.stat().st_size,'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'native_header_valid':True,'native_reopen_test':'NOT RUN','captures':captures,'terrain_and_width_checks':'PASS: native geometry samples; not gameplay','packed_source_images':len(checks['packed_source_images']),'new_routes_controller_test':'NOT TESTED','whole_game_regressions':'NOT RUN: isolated design phase','browser_export_and_performance':'NOT TESTED: no square GLB exported or integrated','human_visual_approval':'PENDING before R0-C1B','production_integration':False,'public_deployment':False}
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='captures'},indent=2))
