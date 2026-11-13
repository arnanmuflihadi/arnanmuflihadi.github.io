from pathlib import Path
import json,math
import numpy as np
from scipy.interpolate import RegularGridInterpolator
S=json.loads(Path('validation/reset-a/terrain-survey.json').read_text());C=json.loads(Path('validation/reset-a/comparison.json').read_text());P=json.loads(Path('validation/reset-a/profiles.json').read_text());g=S['grid'];N=g['n'];step=g['step'];axis=np.arange(N)*step+g['min'];H=np.array(g['heights']).reshape(N,N);F=np.array(g['fractions']).reshape(N,N);X,Z=np.meshgrid(axis,axis);points=np.stack([X,Z],-1);out={}
for k,r in C.items():
 a=math.radians(r['angle']);fw=np.array([math.cos(a),math.sin(a)]);right=np.array([-fw[1],fw[0]]);vmid=18 if r['template']=='hub'else 24;sstart=14 if r['template']=='hub'else 25
 def local(p):
  d=np.array(p)-np.array(r['centre']);return np.stack([d@right,d@fw+vmid],-1)
 d={}
 for kind,profile in P[k].items():
  rows=profile['rows'];dist=np.array([p['s']for p in rows]);raw=np.array([p['y']for p in rows]);line=np.array(profile['line']);ds=np.diff(dist);rg=np.abs(np.diff(raw)/ds)
  if kind=='arrival':design=raw[0]+(r['h0']-raw[0])*dist/dist[-1]
  elif kind=='core':design=r['h0']+r['grade']*np.minimum(local([[p['x'],p['z']]for p in rows])[:,1],sstart)
  else:design=raw.copy()
  turns=[]
  for b,c,e in zip(line,line[1:],line[2:]):
   v=c-b;w=e-c;turns.append(math.degrees(math.acos(np.clip(v@w/np.linalg.norm(v)/np.linalg.norm(w),-1,1))))
  d[kind]={'line':line.tolist(),'horizontalLength':profile['length'],'directDistance':float(np.linalg.norm(line[-1]-line[0])),'rawGradeP95':float(np.percentile(rg,95)*100),'rawGradeMax':float(rg.max()*100),'rawElevationRange':[float(raw.min()),float(raw.max())],'proposedLevelChange':float(design[-1]-design[0]),'proposedGradeMax':float(np.max(abs(np.diff(design)/ds))*100),'turnsDegrees':turns,'turnsOver45':sum(x>45 for x in turns),'proposed3DLength':float(np.hypot(ds,np.diff(design)).sum()),'maxCentrelineCut':float(np.maximum(raw-design,0).max()),'maxCentrelineFill':float(np.maximum(design-raw,0).max()),'sampledDesignLevels':design.tolist()}
 # Four-metre-wide approach corridor; volumes separated from the hard-programme estimates.
 line=np.array(P[k]['arrival']['line']);total=P[k]['arrival']['length'];cum=0;best=np.full(H.shape,np.inf);station=np.zeros(H.shape)
 for b,c in zip(line,line[1:]):
  v=c-b;length=np.linalg.norm(v);t=np.clip(((points-b)@v)/(length*length),0,1);dist=np.linalg.norm(points-b-t[...,None]*v,axis=-1);take=dist<best;station[take]=cum+t[take]*length;best=np.minimum(best,dist);cum+=length
 mask=(best<=2)&~np.load('validation/reset-a/'+k+'-raster.npz')['union'];floor=P[k]['arrival']['rows'][0]['y']+(r['h0']-P[k]['arrival']['rows'][0]['y'])*station/total;delta=floor-H;bnd=np.clip(delta,-1.5,1.5)
 d['approachEarthwork']={'corridorWidth':4,'area':float(mask.sum()*step**2),'estimatedCutM3':float(-np.minimum(bnd[mask],0).sum()*step**2),'estimatedFillM3':float(np.maximum(bnd[mask],0).sum()*step**2),'remainingGapMax':float(np.maximum(delta[mask]-1.5,0).max()),'cutExceedanceMax':float(np.maximum(-delta[mask]-1.5,0).max()),'note':'2D corridor study only; no smoothing/feathering, doorway aprons or optional trail included'}
 # Exact plan dimensions and original-asset roof projections.
 roofs=[]
 for i,p in enumerate(r['program'][:4]):
  cat=S['categories'][i] if False else next(c for c in S['categories']if c['name'].startswith('B'+str(i+1)+'_'));old=S['plots'][i];ox=36+old[1];oz=44-old[2]
  lu=[cat['min'][0]-ox,cat['max'][0]-ox];lv=[oz-cat['max'][2],oz-cat['min'][2]]
  q=np.array([[p['u']+u,p['v']+v]for u,v in [(lu[0],lv[0]),(lu[1],lv[0]),(lu[1],lv[1]),(lu[0],lv[1])]])
  roof=np.array(r['centre'])+q[:,0,None]*right+(q[:,1,None]-vmid)*fw;roofs.append({'id':p['id'],'polygon':roof.tolist(),'height':cat['max'][1]-cat['min'][1],'localBounds':[p['u']+lu[0],p['u']+lu[1],p['v']+lv[0],p['v']+lv[1]]})
 d['roofs']=roofs
 # Minimum centreline-to-roof lateral width at the market row; two-sided narrowest projected roof gap.
 d['minimumRoofToRoofClearGap']=min(roofs[j]['localBounds'][0]-roofs[i]['localBounds'][1]for i,j in [(0,1),(2,3)])
 # Future skyport remains provisional. Quantify consequences if its existing 17.15 m threshold is retained.
 deck=np.array([27,60]);e=np.array(r['entry']);dy=abs(17.15-r['h0']);d['futureSkyport']={'existingProvisionalThreshold':[27,17.15,60],'directToMarket':float(np.linalg.norm(deck-e)),'levelDifferenceToMarket':float(dy),'minimum8PercentRun':float(dy/.08),'notBuilt':True}
 d['totalProposedPrimaryHorizontalLength']=d['arrival']['horizontalLength']+d['core']['horizontalLength'];d['total3DLength']=d['arrival']['proposed3DLength']+d['core']['proposed3DLength'];d['atWalkSpeedSeconds']=d['total3DLength']/2.1
 incoming=line[-1]-line[-2];d['arrivalToCoreTurnDegrees']=math.degrees(math.acos(np.clip(incoming@fw/np.linalg.norm(incoming),-1,1)))
 # Half-metre sampled interior is well back from cliff boundary; silhouette is never edited.
 raster=np.load('validation/reset-a/'+k+'-raster.npz');d['maxProgrammeIslandFraction']=float(F[raster['union']].max())
 T=np.array([[t['x'],t['z']]for t in S['trees']]);line=np.array(d['arrival']['line']);distances=[]
 for aa,bb in zip(line,line[1:]):
  v=bb-aa;t=np.clip((T-aa)@v/(v@v),0,1);distances.append(np.linalg.norm(T-aa-t[:,None]*v,axis=1))
 d['arrivalTreeConflictIds']=np.where(np.min(distances,axis=0)<=3)[0].tolist();d['combinedTreeConflictIds']=sorted(set(r['treeAllConflictIds'])|set(d['arrivalTreeConflictIds']))
 out[k]=d
Path('validation/reset-a/layout-details.json').write_text(json.dumps(out,indent=2))
for k,d in out.items():print(k,json.dumps({n:v for n,v in d.items()if n not in ['roofs','arrival','core','optionalHighland']}));print('route',[(n,{a:round(d[n][a],2)for a in ['horizontalLength','directDistance','rawGradeP95','rawGradeMax','proposedGradeMax','maxCentrelineCut','maxCentrelineFill']})for n in ['arrival','core','optionalHighland']])
