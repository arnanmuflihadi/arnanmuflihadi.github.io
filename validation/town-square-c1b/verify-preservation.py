from pathlib import Path
import hashlib,json
root=Path.cwd();out=root/'validation/town-square-c1b';before=json.loads((out/'before-hashes.json').read_text());changes=[];missing=[];unchanged=0;assets=0
for p,h in before.items():
 f=root/p
 if not f.exists():missing.append(p);continue
 if hashlib.sha256(f.read_bytes()).hexdigest()!=h:changes.append(p)
 else:
  unchanged+=1
  if f.suffix in ['.blend','.glb','.zip'] or 'license' in f.name.lower():assets+=1
expected=['assets/js/floating-atlas/entry.js','assets/js/floating-atlas/town-integration.js','assets/js/floating-atlas/town-review.js']
r={'checkpoint_files':len(before),'unchanged':unchanged,'changed':changes,'missing':missing,'asset_license_files_unchanged':assets,'only_expected_changes':sorted(changes)==sorted(expected) and not missing}
(out/'preservation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
