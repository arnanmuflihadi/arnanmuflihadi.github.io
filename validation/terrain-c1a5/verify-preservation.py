from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2];out=Path(__file__).resolve().parent
before=json.loads((out/'before-hashes.json').read_text());allowed={f'assets/js/floating-atlas/{f}.js'for f in['terrain','entry','collision','town-integration','town-review']};changed=[p for p,h in before.items()if not (root/p).is_file()or hashlib.sha256((root/p).read_bytes()).hexdigest()!=h];unexpected=[p for p in changed if p not in allowed];assert not unexpected,unexpected
assets=[p for p in before if Path(p).suffix.lower()in['.glb','.blend','.zip']or 'license'in Path(p).name.lower()];assert not set(assets)&set(changed)
record={'checked_existing_files':len(before),'expected_source_changes':changed,'unexpected_changes':unexpected,'protected_assets_and_licenses_checked':len(assets),'approved_asset_changes':[],'unchanged_existing_files':len(before)-len(changed),'new_runtime_module':'assets/js/floating-atlas/town-terrain.js','rollback':'Remove terrain-study=c1a5, use Terrain before, or disable dev-town; backups of the five changed source files are in pre-change. No deploy.'}
(out/'preservation.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
