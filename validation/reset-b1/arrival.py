from pathlib import Path
import json,math
import numpy as np
exec(Path('validation/reset-a/study.py').read_text().split('A=[];B=[]')[0])
D=json.loads(Path('validation/reset-b1/layout-study.json').read_text());B=D['alternatives']['B0'];a=np.array([27.,60.]);end=np.array(B['entry'])[[0,2]];line=np.array([a,[20,58.8],end]);segments=np.linalg.norm(np.diff(line,axis=0),axis=1);length=segments.sum();drop=17.15-B['h0'];risers=math.ceil(drop/.18);n1=risers//2;n2=risers-n1;riser=drop/risers;rows=[]
# A two-flight paper section, with long deliberate landings. It is never made into collision geometry.
for s in np.linspace(0,length,201):
 if s<3.7:y=17.15
 elif s<3.7+n1*.32:y=17.15-min(n1,math.floor((s-3.7)/.32)+1)*riser
 elif s<12:y=17.15-n1*riser
 elif s<12+n2*.32:y=17.15-(n1+min(n2,math.floor((s-12)/.32)+1))*riser
 else:y=B['h0']
 j=0 if s<=segments[0]else 1;t=(s-(0 if j==0 else segments[0]))/segments[j];p=line[j]+(line[j+1]-line[j])*t;rows.append({'s':float(s),'x':float(p[0]),'z':float(p[1]),'ground':float(ground([p])[0]),'proposed':float(y)})
delta=np.array([p['proposed']-p['ground']for p in rows]);T=np.array([[t['x'],t['z']]for t in S['trees']]);dist=[]
for aa,bb in zip(line,line[1:]):
 v=bb-aa;t=np.clip((T-aa)@v/(v@v),0,1);dist.append(np.linalg.norm(T-aa-t[:,None]*v,axis=1))
ids=np.where(np.min(dist,axis=0)<=2.5)[0].tolist()
A={'selected':True,'strategy':'Retain provisional skyport threshold; two direct stair flights in an unbuilt section','line':line.tolist(),'start':[27,17.15,60],'end':B['entry'],'horizontalLength':float(length),'lengthAlongStairPolyline':float(length+(risers*riser)),'levelChange':float(-drop),'risers':risers,'riserHeight':float(riser),'treadDepth':.32,'flightRisers':[n1,n2],'flightStarts':[3.7,12],'minimumLandingRun':float(min(3.7,12-(3.7+n1*.32),length-(12+n2*.32))),'clearWidth':3,'centrelineCutMax':float(max(0,-delta.min())),'centrelineSupportMax':float(max(0,delta.max())),'approachTreeConflictIds':ids,'totalTrunkConflicts':sorted(set(ids)|set(B['programmeTreeConflictIds'])),'rows':rows,'controllerStatus':'NOT TESTED; section arithmetic only; no stairs or support colliders built'}
# B's straight-axis threshold is screened using a 15 m future-landing disc; clipping is a failing constraint.
R=B['arrivalReposition'];R['selected']=False;R['reason']='15 m landing reserve crosses the actual cliff lip; 5 m connector also needs six risers. Reject this on-axis threshold under minimal-disturbance gate.';R['cliffLipConflict']=True
Path('validation/reset-b1/arrival-comparison.json').write_text(json.dumps({'A':A,'B':R},indent=2));print(json.dumps({k:v for k,v in A.items()if k!='rows'},indent=2))
