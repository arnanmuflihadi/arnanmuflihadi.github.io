from pathlib import Path
import hashlib,json,os,subprocess,tempfile
root=Path.cwd();out=root/'validation/skyport-r0c3';env=os.environ.copy()
index=Path(tempfile.gettempdir())/'arnan-skyport-checkpoint-index';env['GIT_INDEX_FILE']=str(index)
if index.exists():index.unlink()
def git(*args,text=None):return subprocess.check_output(['git',*args],env=env,input=text,text=True).strip()
parent=git('rev-parse','codex/populated-town-baseline');git('read-tree',parent)
paths=['assets/js/floating-atlas','assets/game/atlas-guild','validation/atlas-guild-r0c2','docs/urban-atlas/atlas-guild-r0c2','tests/atlas-guild.test.mjs','ASSET_MANIFEST.md']
git('add','--',*paths);tree=git('write-tree');commit=git('commit-tree',tree,'-p',parent,text='Preserve accepted Atlas Guild and populated settlement before R0-C3 skyport\n');ref='refs/heads/codex/guild-town-baseline';git('update-ref',ref,commit)
files={}
for folder in ['assets/js/floating-atlas','assets/game/atlas-guild','assets/game/town-population']:
 for p in Path(folder).rglob('*'):
  if p.is_file():files[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['ASSET_MANIFEST.md','assets/js/living-atlas-controller.js','assets/js/project-registry.js','assets/js/urban-atlas/player-controller.js','assets/js/urban-atlas/camera.js','validation/reset-final/layout.json']:
 p=Path(name);files[name]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in Path('validation').glob('*/*.blend'):files[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['entry.js','reconstruction-review.js']:(out/'baseline'/name).write_bytes((Path('assets/js/floating-atlas')/name).read_bytes())
(out/'baseline/ASSET_MANIFEST.md').write_bytes(Path('ASSET_MANIFEST.md').read_bytes())
for name in ['assets/js/floating-atlas/guild-integration.js','assets/game/atlas-guild/atlas-guild.glb']:
 assert git('rev-parse',commit+':'+name)==git('hash-object',name)
(out/'checkpoint.json').write_text(json.dumps(dict(commit=commit,ref=ref,parent=parent,files=files,verified=True,normalIndexAndBranchChanged=False),indent=2))
index.unlink();print(commit,ref,'verified')
