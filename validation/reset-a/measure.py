from pathlib import Path
import json,math
import numpy as np
from scipy.ndimage import label
from scipy.spatial import ConvexHull
exec(Path('validation/reset-a/study.py').read_text().split('A=[];B=[]')[0])
sel=json.loads(Path('validation/reset-a/selected.json').read_text());results={};queries=[]
gz,gx=np.gradient(H,step);slope=np.hypot(gx,gz);X,Z=np.meshgrid(axis,axis)
for name,r in sel.items():
 setup(r['template']);centre=np.array(r['centre']);a=math.radians(r['angle']);fw=np.array([math.cos(a),math.sin(a)]);right=np.array([-fw[1],fw[0]]);u=(X-centre[0])*right[0]+(Z-centre[1])*right[1];vv=(X-centre[0])*fw[0]+(Z-centre[1])*fw[1]+VMID
 masks=[];targets=[];floors=[];polys=[]
 for p in parts:
  poly=transform([[p['u']-p['w']/2,p['v']-p['d']/2-VMID],[p['u']+p['w']/2,p['v']-p['d']/2-VMID],[p['u']+p['w']/2,p['v']+p['d']/2-VMID],[p['u']-p['w']/2,p['v']+p['d']/2-VMID]],centre,r['angle']);polys.append(poly)
  m=(abs(u-p['u'])<=p['w']/2)&(abs(vv-p['v'])<=p['d']/2);masks.append(m)
  qv=np.minimum(p['v'] if p['kind']!='public'else vv,SQUARE_START);target=r['h0']+r['grade']*qv+p['offset'];floors.append(np.broadcast_to(target,H.shape));targets.append(np.broadcast_to(target-(.2 if p['kind']!='public'else 0),H.shape))
 # Dense evaluation tightens the same cut ceiling; adjustment is reported rather than hidden.
 lift=max(0,max(np.max(H[m]-t[m])-1.5 for m,t in zip(masks,targets)));r['h0']+=lift
 floors=[f+lift for f in floors];targets=[t+lift for t in targets];union=np.any(masks,axis=0);target=np.full(H.shape,np.nan);floor=np.full(H.shape,np.nan)
 for m,t,f in zip(masks,targets,floors):target[m]=t[m];floor[m]=f[m]
 delta=target-H;bounded=np.clip(delta,-1.5,1.5);after=H+bounded;support=floor-after
 hull=ConvexHull(np.concatenate(polys));hp=np.concatenate(polys)[hull.vertices]
 from matplotlib.path import Path as MPath
 hullmask=MPath(hp).contains_points(np.column_stack([X.ravel(),Z.ravel()])).reshape(H.shape);window=hullmask&(F<.82);low=window&(slope<=.12);labs,n=label(low);counts=np.bincount(labs.ravel());largest=(counts[1:].max()if n else 0)*step**2
 area=union.sum()*step**2;retaining=0
 for dz,dx in[(1,0),(-1,0),(0,1),(0,-1)]:retaining+=np.sum(union&~np.roll(union,(dz,dx),(0,1))&(np.nan_to_num(floor-H)>.6))*step
 # Four door connectors are reservations; all footprints and routes remain unbuilt.
 plot=[]
 for p,m,f,t,poly in zip(parts,masks,floors,targets,polys):
  ps=H[m];plot.append({**p,'polygon':poly.tolist(),'floor':float(np.median(f[m])),'groundMin':float(ps.min()),'groundMax':float(ps.max()),'naturalGapMin':float(np.min(f[m]-ps)),'naturalGapMax':float(np.max(f[m]-ps)),'supportAfterBoundedGradingMin':float(np.min(support[m])),'supportAfterBoundedGradingMax':float(np.max(support[m]))})
 square=next(p for p in parts if p['id']=='square');s0=square['v']-square['d']/2;s1=square['v']+square['d']/2;end=next(p for p in parts if p['id']=='guild')['v']-4
 routeLocal=[[0,0],[0,s0-1],[-2.7,square['v']-2],[-2.7,square['v']+2],[0,s1-1],[0,end]]
 route=transform([[u,v-VMID]for u,v in routeLocal],centre,r['angle']);core=sum(math.dist(p,q)for p,q in zip(route,route[1:]));bends=[]
 for i in range(1,len(route)-1):
  v1=route[i]-route[i-1];v2=route[i+1]-route[i];angle=math.degrees(math.acos(np.clip(v1@v2/np.linalg.norm(v1)/np.linalg.norm(v2),-1,1)));bends.append(angle)
 entry=route[0];tie=np.array(r['tie']);spawn=np.array([27,57]);tieY=float(ground([tie])[0]);extra=max(0,abs(r['h0']-tieY)/.08-math.dist(entry,tie))
 # A deliberately visible approach allowance; no imaginary straight-line traversal claim.
 approach=r['tieDistance']+math.dist(entry,tie)+extra
 # Trees counted by trunk centres in the hard program plus one-metre placement buffer.
 rel=trees-centre;tu=rel@right;tv=rel@fw+VMID;plotTrees=[];publicTrees=[];bufferTrees=[]
 for i,(xx,zz)in enumerate(trees):
  hits=[p for p in parts if abs(tu[i]-p['u'])<p['w']/2+1 and abs(tv[i]-p['v'])<p['d']/2+1]
  if hits:bufferTrees.append(i)
  if any(p['kind']in['building','reserve']for p in hits):plotTrees.append(i)
  if any(p['kind']=='public'for p in hits):publicTrees.append(i)
 result={**r,'denseFloorLift':lift,'program':plot,'hull':hp.tolist(),'areaHardProgramme':area,'areaContiguousEnvelope':float(hull.volume),'rawTerrainEnvelopeRange':[float(H[window].min()),float(H[window].max())],'rawProgrammeElevationRange':[float(H[union].min()),float(H[union].max())],'rawSlopePercentiles':(np.percentile(slope[union],[10,50,90,100])*100).tolist(),'rawProgrammeLowSlopeArea':float(np.sum(union&(slope<=.12))*step**2),'largestContiguousLowSlopePatch':float(largest),'requiredCutEstimateM3':float(-np.minimum(delta[union],0).sum()*step**2),'requiredFillEstimateM3':float(np.maximum(delta[union],0).sum()*step**2),'boundedCutEstimateM3':float(-np.minimum(bounded[union],0).sum()*step**2),'boundedFillEstimateM3':float(np.maximum(bounded[union],0).sum()*step**2),'beyondGradeBudgetArea':float(np.sum(union&(delta>1.5))*step**2),'naturalSupportDepthRange':[float(np.min((floor-H)[union])),float(np.max((floor-H)[union]))],'supportAfterBoundedGradingRange':[float(np.min(support[union])),float(np.max(support[union]))],'raisedBoundaryProxyM':float(retaining),'primaryCoreRoute':route.tolist(),'primaryCoreLength':float(core),'primaryTurnsDegrees':bends,'arrivalApproachMinimumLength':float(approach),'arrivalExtraLengthAllowance':float(extra),'totalPrimaryMinimumLength':float(approach+core),'treePlotConflictIds':plotTrees,'treePublicConflictIds':publicTrees,'treeAllConflictIds':bufferTrees,'camera':{'clearPromenade':6,'squareWidth':14,'followDistance':9.5,'fullOrbitGuaranteed':False},'method':'0.5 m samples from accepted game sampler; cut/fill volumes are raster estimates; floors are flat per building; public grade capped at 8%; plaza and Guild apron share one level; grading cap +/-1.5 m'}
 results[name]=result
 # Exact sampler queries for reproducible longitudinal profiles and approach audit.
 for kind,line in [('core',route),('arrival',np.array([spawn,entry]))]:
  for k,(a,b)in enumerate(zip(line,line[1:])):
   n=math.ceil(math.dist(a,b)/.5)
   for j in range(n):p=a+(b-a)*j/n;queries.append({'alternative':name,'kind':kind,'segment':k,'x':p[0],'z':p[1]})
  queries.append({'alternative':name,'kind':kind,'segment':len(line)-2,'x':line[-1][0],'z':line[-1][1]})
 np.savez('validation/reset-a/'+name+'-raster.npz',union=union,delta=delta,support=support,hullmask=hullmask,target=floor)
Path('validation/reset-a/comparison.json').write_text(json.dumps(results,indent=2));Path('validation/reset-a/height-queries.json').write_text(json.dumps(queries))
for name,r in results.items():print(name,json.dumps({k:r[k]for k in ['centre','angle','template','h0','denseFloorLift','areaHardProgramme','areaContiguousEnvelope','rawProgrammeElevationRange','rawSlopePercentiles','largestContiguousLowSlopePatch','boundedCutEstimateM3','boundedFillEstimateM3','requiredFillEstimateM3','supportAfterBoundedGradingRange','raisedBoundaryProxyM','primaryCoreLength','arrivalApproachMinimumLength','totalPrimaryMinimumLength','treePlotConflictIds','treePublicConflictIds']}))
