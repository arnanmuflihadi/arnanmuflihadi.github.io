from pathlib import Path
import json,math
import numpy as np
S=json.loads(Path('validation/reset-a/terrain-survey.json').read_text());L=json.loads(Path('validation/reset-b1/layout-study.json').read_text())['alternatives'];R=json.loads(Path('validation/reset-a/layout-details.json').read_text())['B']['roofs'];A=json.loads(Path('validation/reset-b1/arrival-comparison.json').read_text())['A'];results={}
def overlaps(a,b):
 for p in [a,b]:
  for x,y in zip(p,np.roll(p,-1,axis=0)):
   edge=y-x;n=np.array([-edge[1],edge[0]]);aa=a@n;bb=b@n
   if aa.max()<bb.min()or bb.max()<aa.min():return False
 return True
for k,r in L.items():
 rec=[];rt=np.array(r['worldRight']);fw=np.array(r['worldForward']);c=np.array(r['centre'])
 for i,t in enumerate(S['trees']):
  x,z,w,d=t['x'],t['z'],t['w'],t['d'];box=np.array([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]]);hits=[p['id']for p in r['programme']if overlaps(np.array(p['polygon']),box)];envelopes=[]
  for q in R:
   u0,u1,v0,v1=q['localBounds'];pp=np.array([c+rt*u+fw*(v-18)for u,v in[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]]);
   if overlaps(pp,box):envelopes.append(q['id'])
  arrival=False
  if k=='B0':
   for a,b in zip(A['line'],A['line'][1:]):
    a=np.array(a);b=np.array(b);d=b-a;n=np.array([-d[1],d[0]])/np.linalg.norm(d)*1.5
    if overlaps(np.array([a+n,b+n,b-n,a-n]),box):arrival=True
  if hits or envelopes or arrival:rec.append({'tree':i,'height':t['h']-t['minY'],'plotHits':[x for x in hits if x.startswith('B')or x=='guild'],'publicHits':[x for x in hits if not(x.startswith('B')or x=='guild')],'modelEnvelopeHits':envelopes,'arrival':arrival})
 results[k]={'actualColliderIntersections':rec,'plotIds':[q['tree']for q in rec if q['plotHits']],'programmeIds':[q['tree']for q in rec if q['plotHits']or q['publicHits']],'totalIncludingModelOverhangs':[q['tree']for q in rec],'tallIds':[q['tree']for q in rec if q['height']>=10]}
Path('validation/reset-b1/trunk-collision-check.json').write_text(json.dumps(results,indent=2));print(json.dumps({k:{n:r[n]for n in ['plotIds','programmeIds','totalIncludingModelOverhangs','tallIds']}for k,r in results.items()},indent=2))
