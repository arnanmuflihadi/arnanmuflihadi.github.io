import json,math
from pathlib import Path
import numpy as np
from scipy.interpolate import RegularGridInterpolator
S=json.loads(Path('validation/reset-a/terrain-survey.json').read_text());g=S['grid'];N=g['n'];step=g['step'];axis=np.arange(N)*step+g['min'];H=np.array(g['heights']).reshape(N,N);F=np.array(g['fractions']).reshape(N,N);G=RegularGridInterpolator((axis,axis),H,bounds_error=False,fill_value=-500);FR=RegularGridInterpolator((axis,axis),F,bounds_error=False,fill_value=2)
def ground(p):return G(np.asarray(p)[:,[1,0]])
# The identical program is tested at both sites, using actual structural footprints.
def setup(template):
 global parts,local,ids,weights,off,v,q,qbar,var,outer,VMID,SQUARE_START
 hub=template=='hub';VMID=18 if hub else 24;SQUARE_START=14 if hub else 25;parts=[]
 for i,(id,uu,vv,w,d,h)in enumerate(S['plots']):
  parts.append(dict(id=id,name=['Kopi Awan','Lembaran','Rupa Rimba','Serambi'][i],u=((-11.4 if i==2 else 11.4)if hub and i>=2 else(-8.3 if i in[0,2]else 8.3)),v=((6 if i<2 else 20)if hub else(7 if i<2 else 19.5)),w=w,d=d,kind='building',offset=.15))
 parts += [dict(id='market',name='Market promenade',u=0,v=7 if hub else 12.5,w=6,d=14 if hub else 25,kind='public',offset=0),dict(id='square',name='Telaga Awan',u=0,v=20.5 if hub else 31.5,w=14,d=13,kind='public',offset=0),dict(id='guildfore',name='Guild approach',u=0,v=27.5 if hub else 39,w=6,d=1 if hub else 2,kind='public',offset=0),dict(id='guild',name='Guild reservation',u=0,v=32 if hub else 44,w=10,d=8,kind='reserve',offset=.15)]
 local=[];ids=[];weights=[];off=[];outer=[]
 for k,p in enumerate(parts):
  for vv in np.arange(p['v']-p['d']/2+.7,p['v']+p['d']/2,.9):
   for u in np.arange(p['u']-p['w']/2+.7,p['u']+p['w']/2,.9):local.append([u,vv-VMID]);ids.append(k);weights.append(2.5 if p['kind']=='public'else 1);off.append(p['offset'])
  outer.extend([[u,vv-VMID]for u in np.linspace(p['u']-p['w']/2-2,p['u']+p['w']/2+2,4)for vv in np.linspace(p['v']-p['d']/2-2,p['v']+p['d']/2+2,4)])
 local=np.array(local);ids=np.array(ids);weights=np.array(weights);off=np.array(off);v=local[:,1]+VMID;q=np.minimum(np.where(np.isin(ids,[0,1,2,3,7]),np.array([parts[k]['v']for k in ids]),v),SQUARE_START);qbar=np.average(q,weights=weights);var=np.average((q-qbar)**2,weights=weights);outer=np.array(outer)
stream=np.array(S['stream'])[:,:2];trees=np.array([[t['x'],t['z']]for t in S['trees']]);trail=np.array(S['trails'][0]['points']);traildense=[];cum=0
for a,b in zip(trail,trail[1:]):
 l=np.linalg.norm(b[:2]-a[:2]);n=math.ceil(l)
 for j in range(n):traildense.append([*(a[:2]+(b[:2]-a[:2])*j/n),cum+l*j/n])
 cum+=l
traildense=np.array(traildense);ty=ground(traildense[:,:2])
def transform(p,c,angle):
 a=math.radians(angle);forward=np.array([math.cos(a),math.sin(a)]);right=np.array([-forward[1],forward[0]]);return c+np.asarray(p)[:,0,None]*right+np.asarray(p)[:,1,None]*forward

def evaluate(c,angle,full=False):
 c=np.array(c);p=transform(local,c,angle);o=transform(outer,c,angle)
 if np.any(FR(o[:,[1,0]])>.82):return None
 gh=ground(p)
 if gh.max()>31 or np.min(np.linalg.norm(p[:,None,:]-stream[None,:,:],axis=2))<9:return None
 y=gh-off;ybar=np.average(y,weights=weights)
 baseoff=off-np.where(np.isin(ids,[0,1,2,3,7]),.2,0)
 grades=np.linspace(-.08,.08,17);h0s=np.maximum(ybar-grades*qbar,np.max(gh[None,:]-grades[:,None]*q-baseoff,axis=1)-1.5)
 deltas=h0s[:,None]+grades[:,None]*q+baseoff-gh;resids=np.maximum(deltas-1.5,0)
 objectives=np.mean(abs(deltas),axis=1)*4+np.max(resids,axis=1)*2+np.mean(resids,axis=1)*8
 kk=int(np.argmin(objectives));grade=grades[kk];h0=h0s[kk];delta=deltas[kk];bounded=np.clip(delta,-1.5,1.5);residual=resids[kk];support=np.maximum(h0+grade*q+off-(gh+np.maximum(bounded,0)),0)
 entry=transform([[0,-VMID]],c,angle)[0];forward=np.array([math.cos(math.radians(angle)),math.sin(math.radians(angle))]);spawn_delta=entry-np.array([27,57]);spawn_cos=spawn_delta@forward/max(np.linalg.norm(spawn_delta),.01)
 if spawn_cos<math.cos(math.radians(75)):return None
 direct=np.linalg.norm(traildense[:,:2]-entry,axis=1);dy=np.abs(ty-h0);extra=np.maximum(dy/.08-direct,0);approachCost=traildense[:,2]+direct+2*extra
 # Avoid a reversed entry; incoming travel must broadly follow the town axis.
 incoming=(entry-traildense[:,:2])/np.maximum(direct[:,None],.001);alignment=np.arccos(np.clip(incoming@forward,-1,1))*180/np.pi;approachCost+=np.maximum(alignment-65,0)*.10;approachCost[alignment>75]=np.inf
 if not np.isfinite(approachCost).any():return None
 k=int(np.argmin(approachCost));approach=traildense[k,2]+direct[k]+extra[k]
 rel=trees-c;a=math.radians(angle);u=rel@np.array([-math.sin(a),math.cos(a)]);vv=rel@forward+VMID
 affected=np.zeros(len(trees),bool)
 for pp in parts:
  if pp['kind']!='building'and pp['id']!='guild':continue
  affected|=(np.abs(u-pp['u'])<pp['w']/2+1)&(np.abs(vv-pp['v'])<pp['d']/2+1)
 # A read-only search score, not an artistic score: prioritize support and infrastructure costs.
 score=np.mean(np.abs(delta))*4+np.max(residual)*2.0+np.mean(residual)*8+approach*.05+affected.sum()*.06+extra[k]*.03
 out=dict(centre=c.tolist(),angle=angle,score=float(score),h0=float(h0),grade=float(grade),meanAdjustment=float(np.mean(abs(delta))),maxUnfilled=float(np.max(residual)),maxSupport=float(np.max(support)),treePlotConflicts=int(affected.sum()),entry=entry.tolist(),tie=traildense[k,:2].tolist(),tieDistance=float(traildense[k,2]),spurDirect=float(direct[k]),extraApproachLength=float(extra[k]),approachLength=float(approach),approachMeanGrade=float(dy[k]/max(direct[k]+extra[k],.01)),entryAngle=float(alignment[k]))
 return out
A=[];B=[];programs={}
for template in ['linear','hub']:
 setup(template);programs[template]={'parts':parts,'VMID':VMID,'squareStart':SQUARE_START}
 for x in range(24,46,3):
  for z in range(15,40,3):
   if math.hypot(x-36,z-27)>12:continue
   for angle in range(0,360,15):
    r=evaluate([x,z],angle)
    if r:r['template']=template;A.append(r)
 for x in range(-50,51,5):
  for z in range(-10,66,5):
   if math.hypot(x-36,z-27)<22:continue
   for angle in range(0,360,15):
    r=evaluate([x,z],angle)
    if r:r['template']=template;B.append(r)
A.sort(key=lambda x:x['score']);B.sort(key=lambda x:x['score'])
Path('validation/reset-a/search.json').write_text(json.dumps({'programs':programs,'A':A[:30],'B':B[:30],'counts':{'A':len(A),'B':len(B)},'constraints':{'maxCivicGrade':.08,'maxCutFill':1.5,'edgeFraction':.82,'streamBuffer':9,'guildReserve':[10,8],'programs':'same four assets, 182 m2 square reservation, six-metre clear promenade; linear or compact civic hub'}},indent=2))
print(json.dumps({'counts':[len(A),len(B)],'A':A[:3],'B':B[:3]},indent=2))
