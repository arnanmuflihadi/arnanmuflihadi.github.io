from pathlib import Path
import json,math
import numpy as np
from scipy.spatial import ConvexHull
exec(Path('validation/reset-a/study.py').read_text().split('A=[];B=[]')[0]);setup('hub')
prior=json.loads(Path('validation/reset-a/comparison.json').read_text())['B'];oldD=json.loads(Path('validation/reset-a/layout-details.json').read_text())['B'];a=math.radians(prior['angle']);fw=np.array([math.cos(a),math.sin(a)]);right=np.array([-fw[1],fw[0]])
# Exactly one alternative: translate the entire programme 3.5 m along its right axis.
positions={'B0':np.array(prior['centre']),'B1':np.array(prior['centre'])+3.5*right};X,Z=np.meshgrid(axis,axis);out={}
# Equal local samples for a global vertical translation; no building or plaza redesign.
proto=np.array([[u,v-18]for p in parts for u in np.arange(p['u']-p['w']/2,p['u']+p['w']/2,.5)for v in np.arange(p['v']-p['d']/2,p['v']+p['d']/2,.5)])
for key,c in positions.items():
 q=transform(proto,c,prior['angle']);old=transform(proto,prior['centre'],prior['angle']);h0=prior['h0']+(np.median(ground(q)-ground(old))if key=='B1'else 0);u=(X-c[0])*right[0]+(Z-c[1])*right[1];v=(X-c[0])*fw[0]+(Z-c[1])*fw[1]+18;records=[];masks=[];targets=[];floors=[]
 for p in parts:
  mask=(abs(u-p['u'])<=p['w']/2)&(abs(v-p['v'])<=p['d']/2);dv=np.minimum(v if p['kind']=='public'else p['v'],14);floor=np.broadcast_to(h0+.02*dv+p['offset'],H.shape);target=floor-(.2 if p['kind']!='public'else 0);masks.append(mask);targets.append(target);floors.append(floor)
 lift=max(0,max(np.max(H[m]-t[m])-1.5 for m,t in zip(masks,targets)));h0+=lift;union=np.any(masks,axis=0);target=np.zeros_like(H);floor=np.zeros_like(H)
 for p,m,t,f in zip(parts,masks,targets,floors):
  f=f+lift;t=t+lift;target[m]=t[m];floor[m]=f[m];poly=transform([[p['u']-p['w']/2,p['v']-p['d']/2-18],[p['u']+p['w']/2,p['v']-p['d']/2-18],[p['u']+p['w']/2,p['v']+p['d']/2-18],[p['u']-p['w']/2,p['v']+p['d']/2-18]],c,prior['angle']);records.append({**p,'polygon':poly.tolist(),'floor':float(np.median(f[m])),'groundRange':[float(H[m].min()),float(H[m].max())],'rawGap':[float((f-H)[m].min()),float((f-H)[m].max())]})
 delta=target-H;bounded=np.clip(delta,-1.5,1.5);sup=floor-H-bounded;rel=trees-c;tu=rel@right;tv=rel@fw+18;plotIds=[];allIds=[]
 for i,t in enumerate(trees):
  hits=[p for p in parts if abs(tu[i]-p['u'])<=p['w']/2+1 and abs(tv[i]-p['v'])<=p['d']/2+1]
  if hits:allIds.append(i)
  if any(p['kind']in ['building','reserve']for p in hits):plotIds.append(i)
 entry=transform([[0,-18]],c,prior['angle'])[0];arrival=np.array([[27,57],[27,65],[22,67],entry]);ds=[]
 for aa,bb in zip(arrival,arrival[1:]):
  vv=bb-aa;t=np.clip((trees-aa)@vv/(vv@vv),0,1);ds.append(np.linalg.norm(trees-aa-t[:,None]*vv,axis=1))
 arrivalIds=np.where(np.min(ds,axis=0)<=3)[0].tolist();combined=sorted(set(allIds)|set(arrivalIds));mature=[i for i in combined if S['trees'][i]['h']-S['trees'][i]['minY']>=10]
 # Distance from programme vertices to the actual cliff lip, not a normalized radius assumption.
 boundary=np.array(S['boundary']);pp=np.concatenate([p['polygon']for p in records]);edge=[]
 for aa,bb in zip(boundary,np.roll(boundary,-1,axis=0)):
  vv=bb-aa;t=np.clip((pp-aa)@vv/(vv@vv),0,1);edge.append(np.linalg.norm(pp-aa-t[:,None]*vv,axis=1))
 hull=ConvexHull(pp)
 # The moved threshold is on-axis; reserve a 15 m disc immediately behind it, no skyport architecture.
 threshold=transform([[0,-5-18]],c,prior['angle'])[0];land=transform([[0,-12.5-18]],c,prior['angle'])[0];circle=np.array([land+[math.cos(t),math.sin(t)]*np.array([rad,rad]) for rad in [0,2.5,5,7.5]for t in np.linspace(0,2*math.pi,49)[:-1]]);allYs=ground(circle);outsideSamples=int(np.sum(allYs< -100));ys=allYs[allYs> -100];landingY=max(float(np.median(ys))+.1,float(ys.max())-1.5);rise=landingY-h0;steps=math.ceil(abs(rise)/.18)
 out[key]={'centre':c.tolist(),'angleDegreesFromPositiveX':prior['angle'],'worldForward':fw.tolist(),'worldRight':right.tolist(),'h0':float(h0),'programme':records,'entry':[float(entry[0]),float(h0),float(entry[1])],'squareY':float(h0+.28),'guildEntryY':float(h0+.43),'plotTreeConflictIds':plotIds,'programmeTreeConflictIds':allIds,'oldArrivalTreeIds':arrivalIds,'combinedOldArrivalTreeIds':combined,'tallTreeConflictIds':mature,'cutEstimateM3':float(-np.minimum(delta[union],0).sum()*.25),'boundedFillEstimateM3':float(np.maximum(bounded[union],0).sum()*.25),'fullFillEstimateM3':float(np.maximum(delta[union],0).sum()*.25),'supportAfterGradingMax':float(sup[union].max()),'rawGapRange':[float((floor-H)[union].min()),float((floor-H)[union].max())],'minCliffLipDistance':float(np.min(edge)),'areaEnvelope':float(hull.volume),'programmeArea':float(union.sum()*.25),'maxProgrammeFraction':float(F[union].max()),'arrivalRetain':{'threshold':[27,17.15,60],'directHorizontal':float(np.linalg.norm(entry-[27,60])),'levelDifference':float(17.15-h0),'risersAtMax018':math.ceil(abs(17.15-h0)/.18)},'arrivalReposition':{'threshold':[float(threshold[0]),landingY,float(threshold[1])],'thresholdMove':float(np.linalg.norm(threshold-[27,60])),'landingCentre':land.tolist(),'landingDiameter':15,'landingY':landingY,'landingGroundRange':[float(ys.min()),float(ys.max())],'landingCutMax':float(max(0,ys.max()-landingY)),'landingFillMax':float(max(0,landingY-ys.min())),'landingMaxIslandFraction':float(FR(circle[:,[1,0]]).max()),'routeHorizontal':5,'levelDifference':float(rise),'risersAtMax018':steps,'sampledDiscOnly':True,'outsideSurfaceSamples':outsideSamples,'surfaceSamples':len(allYs),'groundRangeExcludesOffIslandSentinel':True}}
Path('validation/reset-b1/layout-study.json').write_text(json.dumps({'scope':'only B0 and one 3.5 m lateral translation; no search or new geometry','tallTreeDefinition':'survey height >=10 m is only a size proxy, not a measured age','alternatives':out},indent=2));print(json.dumps({k:{n:r[n]for n in ['centre','h0','plotTreeConflictIds','combinedOldArrivalTreeIds','tallTreeConflictIds','cutEstimateM3','boundedFillEstimateM3','supportAfterGradingMax','minCliffLipDistance','arrivalRetain','arrivalReposition']}for k,r in out.items()},indent=2))
