from pathlib import Path
import subprocess,os,json,tempfile
root=Path.cwd();env=os.environ.copy();index=Path(tempfile.gettempdir())/'arnan-reset-final-index';env['GIT_INDEX_FILE']=str(index)
if index.exists():index.unlink()
def run(*args,stdin=None):return subprocess.check_output(['git',*args],cwd=root,env=env,input=stdin,text=True).strip()
head=run('rev-parse','HEAD');run('read-tree',head);run('add','-u');run('add','--','AGENTS.md','ASSET_MANIFEST.md','assets/js','assets/css','assets/game','tests')
extra=['validation/market-street-s2d/market-street-optimized.glb','validation/market-street-s2e/common-interface.glb','validation/market-street-s2e/foundation-hybrid.glb','validation/market-street-s2e/support-reference.glb','validation/town-square-c1b/town-square-optimized.glb','validation/circulation-c1c/circulation-interfaces.glb','validation/circulation-c1c/circulation-square.glb']
run('add','--',*extra);tree=run('write-tree');commit=run('commit-tree',tree,'-p',head,stdin='Checkpoint current Urban Atlas before coordinated RESET-FINAL reconstruction\n');ref='refs/heads/codex/reset-final-checkpoint';run('update-ref',ref,commit)
Path('validation/reset-final/checkpoint.json').write_text(json.dumps({'commit':commit,'ref':ref,'parent':head,'method':'Separate temporary Git index; current branch, working tree and normal index unchanged','scope':'Tracked baseline, existing game code/assets/tests and deployed town GLBs; Blender masters/source archives preserved separately by hashes'},indent=2));index.unlink();print(commit,ref)
