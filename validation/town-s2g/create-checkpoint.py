"""Local checkpoint using an alternate index; leave HEAD, working files and staged changes alone."""
import os,json,hashlib,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def git(*args,env=None):return subprocess.check_output(['git',*args],cwd=ROOT,env=env).decode().strip()
paths=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT).decode().split('\0')
baseline={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths)) if p and not p.startswith('validation/town-s2g/') and (ROOT/p).is_file()}
(OUT/'before-hashes.json').write_text(json.dumps(baseline,indent=2)+'\n')
index=ROOT/'.git/index';before=hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None
head=git('rev-parse','HEAD');branch=git('branch','--show-current')
with tempfile.TemporaryDirectory(prefix='arnan-s2g-checkpoint-') as tmp:
 env=dict(os.environ,GIT_INDEX_FILE=str(Path(tmp)/'index'))
 git('read-tree','HEAD',env=env);git('add','-A','--','.',env=env);tree=git('write-tree',env=env)
 commit=git('-c','user.name=Codex checkpoint','-c','user.email=codex-checkpoint@localhost','commit-tree',tree,'-p',head,'-m','Local checkpoint: approved S2-F workspace before S2-G stabilization',env=env)
 ref='refs/heads/codex/checkpoint-s2f-before-s2g'
 if subprocess.run(['git','show-ref','--verify','--quiet',ref],cwd=ROOT).returncode==0:ref+='-'+commit[:8]
 git('update-ref',ref,commit,'0'*40)
after=hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None
assert before==after and git('rev-parse','HEAD')==head and git('branch','--show-current')==branch
record={'ref':ref,'commit':commit,'parent':head,'current_branch_unchanged':branch,'original_index_unchanged':True,'protected_files':len(baseline),'scope':'Full non-ignored working tree checkpoint; no checkout, reset, stash or deployment.'}
(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
