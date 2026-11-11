from pathlib import Path
import subprocess,os,json,hashlib,tempfile
root=Path.cwd();env=os.environ.copy();index=Path(tempfile.gettempdir())/'arnan-guild-r0c2-index';env['GIT_INDEX_FILE']=str(index)
if index.exists():index.unlink()
def git(*a,text=None):return subprocess.check_output(['git',*a],env=env,input=text,text=True).strip()
parent=git('rev-parse','codex/accepted-settlement-baseline');git('read-tree',parent)
paths=['assets/js/floating-atlas','assets/game/town-population','ASSET_MANIFEST.md','tests/town-population.test.mjs','docs/urban-atlas/town-population','validation/town-population']
git('add','--',*paths);tree=git('write-tree');commit=git('commit-tree',tree,'-p',parent,text='Checkpoint accepted populated Transit Kingdom before R0-C2 Guild\n');ref='refs/heads/codex/populated-town-baseline';git('update-ref',ref,commit)
files={}
for folder in ['assets/js/floating-atlas','assets/game/town-population']:
 for p in Path(folder).rglob('*'):
  if p.is_file():files[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in ['ASSET_MANIFEST.md','validation/atlas-guild-c2a/atlas-guild-design.blend','validation/atlas-guild-reset/atlas-guild.blend','validation/reset-final/layout.json']:
 files[p]=hashlib.sha256(Path(p).read_bytes()).hexdigest()
for p in ['assets/js/floating-atlas/entry.js','assets/js/floating-atlas/town-reconstruction.js','assets/js/floating-atlas/reconstruction-review.js','ASSET_MANIFEST.md']:Path('validation/atlas-guild-r0c2/baseline',Path(p).name).write_bytes(Path(p).read_bytes())
for p in ['assets/js/floating-atlas/town-population.js','assets/js/floating-atlas/reconstruction-plan.js']:
 assert git('rev-parse',commit+':'+p)==git('hash-object',p)
Path('validation/atlas-guild-r0c2/checkpoint.json').write_text(json.dumps({'commit':commit,'ref':ref,'parent':parent,'files':files,'verified':True,'normalIndexAndBranchChanged':False},indent=2));index.unlink();print(commit,ref,'verified')
