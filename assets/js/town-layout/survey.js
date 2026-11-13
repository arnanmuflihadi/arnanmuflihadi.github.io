import{selected,journeyRoutes,densify,routeSurvey,entryOf}from'./plan.js?v=composition-3';
import{blocked}from'../floating-atlas/collision.js?v=73';

export function measureLayout(preview,world){
 const safe=(x,z,y,radius=0)=>!blocked(x,z,world.obstacles.filter(o=>!Number.isFinite(o.minY)||(y+1.9>o.minY&&y<o.h-.06)),radius);
 function surveyRoute(route,paved=false){
  const pts=densify(route.points,.25).map(([x,z])=>[x,z,preview.heightAt(x,z)]),base=routeSurvey(pts,{authored:true,width:route.width||0});let minimum=Infinity,gaps=0,blockedSamples=0,maxTransition=0,maxThreeMetreGrade=0;const stations=[0];for(let i=1;i<pts.length;i++)stations.push(stations[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));
  const widths=[];
  for(let i=0;i<pts.length;i++){
   const[x,z,y]=pts[i];if(!safe(x,z,y,.34))blockedSamples++;
   if(i)maxTransition=Math.max(maxTransition,Math.abs(y-pts[i-1][2]));let previous=i-1;while(previous>0&&stations[i]-stations[previous]<3)previous--;if(previous>=0&&stations[i]-stations[previous]>=3)maxThreeMetreGrade=Math.max(maxThreeMetreGrade,Math.abs(y-pts[previous][2])/(stations[i]-stations[previous]));
   if(!route.width)continue;
   const a=pts[Math.max(0,i-1)],b=pts[Math.min(pts.length-1,i+1)],length=Math.hypot(b[0]-a[0],b[1]-a[1])||1,nx=-(b[1]-a[1])/length,nz=(b[0]-a[0])/length;
   if(paved&&preview.surfaceAt(x,z)<0){gaps++;minimum=0;continue;}
   let width=0;
   for(const sign of[-1,1]){let lastHeight=y;for(let off=.05;off<=route.width/2+.001;off+=.05){const xx=x+nx*off*sign,zz=z+nz*off*sign,h=paved?preview.surfaceAt(xx,zz):preview.heightAt(xx,zz);if(h<0||Math.abs(h-lastHeight)>.42||!safe(xx,zz,h))break;width+=.05;lastHeight=h;}}
   widths.push(width);minimum=Math.min(minimum,width);
  }
  return{...base,minimumClearWidth:route.width?minimum:null,minimumClearPavedWidth:paved?minimum:null,nominalWidth:route.width||null,widthMethod:'0.05 m cross sections capped at nominal width; continuous support (rendered paving for urban routes), adjacent steps below 0.42 m and no solid intersection; capsule-centre span is 0.68 m narrower',pavingGaps:gaps,blockedSamples,maxRisePerQuarterMetre:maxTransition,maxThreeMetreGrade,points:pts};
 }
 const streets=selected.streets.map(r=>({id:r.id,kind:r.kind,...surveyRoute(r,!['trail'].includes(r.kind))}));
 const journeys=Object.entries(journeyRoutes).map(([id,r])=>({id,name:r.name,...surveyRoute(r)}));
 const entrances=selected.lots.map(l=>{const e=entryOf(l),q=l.publicPoint,out=l.face==='east'?[1,0]:l.face==='west'?[-1,0]:[0,1],v=[q[0]-e[0],q[1]-e[1]],len=Math.hypot(...v),samples=densify([[q[0],q[1]],[e[0],e[1]]],.1),blockedSamples=samples.filter(([x,z])=>!safe(x,z,preview.heightAt(x,z),.34)).length;return{id:l.id,face:l.face,entry:e,publicPoint:q,facingDot:(out[0]*v[0]+out[1]*v[1])/len,entrySupport:preview.surfaceAt(...e),floor:l.y,clearApproach:blockedSamples===0,blockedSamples,approachDistance:len,door:l.id==='G'?[3.6,5.5]:[2.4,2.9],canopyClearance:l.id==='G'?5.81:3.11};});
 let gross=0,levelClear=0,coreClear=true;const step=.25,s=selected.square;
 for(let x=s.x-s.w/2+step/2;x<s.x+s.w/2;x+=step)for(let z=s.z-s.d/2+step/2;z<s.z+s.d/2;z+=step){const cornerX=Math.max(0,Math.abs(x-s.x)-(s.w/2-2)),cornerZ=Math.max(0,Math.abs(z-s.z)-(s.d/2-2));if(cornerX+cornerZ>2)continue;gross+=step*step;const y=preview.heightAt(x,z),clear=Math.abs(y-s.y)<.05&&safe(x,z,y,.34);if(clear)levelClear+=step*step;if(x>=s.clear[0]&&x<=s.clear[2]&&z>=s.clear[1]&&z<=s.clear[3]&&!clear)coreClear=false;}
 const guild=selected.lots.find(l=>l.id==='G'),e=entryOf(guild),toSquare=[s.x-e[0],s.z-e[1]],guildFacingDot=toSquare[1]/Math.hypot(...toSquare);
 const sightlines=[];
 for(const[id,x,z]of[['arrival',27,60],['market',36,38],['square',35,22]])for(const[part,dx,dz,height]of[['hall',0,0,7.8],['tower',1,-1.8,10],['peak',1,-1.8,15.8]]){const from=[x,preview.heightAt(x,z)+1.65,z],to=[guild.x+dx,guild.y+height,guild.z+dz];let blocker=null;for(let t=.005;t<.985;t+=.005){const q=from.map((v,i)=>v+(to[i]-v)*t);if(world.groundHeight(q[0],q[2])>q[1]){blocker='terrain';break;}const o=preview.solids.find(o=>o.planning&&o.planning!=='G'&&Math.abs(q[0]-o.x)<o.w/2&&Math.abs(q[2]-o.z)<o.d/2&&q[1]>o.minY&&q[1]<o.h);if(o){blocker=o.planning;break;}}sightlines.push({from:id,part,eye:from,target:to,clear:!blocker,blocker,method:'Exact terrain and opaque planning masses, three actual landmark heights; foliage excluded and checked in browser'});}
 return{units:'metres; grade is rise/run',sampling:{routes:.25,crossSections:.05,plots:.5,plaza:.25},streets,journeys,entrances,plots:preview.plots,plaza:{grossPavedArea:s.w*s.d-8,sampledGrossArea:gross,levelCapsuleClearArea:levelClear,centralClearRectangle:s.clear,centralClearArea:(s.clear[2]-s.clear[0])*(s.clear[3]-s.clear[1]),coreClear},guild:{centre:[guild.x,guild.z],face:guild.face,facingDotToSquare:guildFacingDot,sightlines},frontageAlignment:{westRowFaceX:selected.lots.filter(l=>/^M[1357]$/.test(l.id)).map(l=>l.x+l.w/2),eastRowFaceX:selected.lots.filter(l=>/^M[2468]$/.test(l.id)).map(l=>l.x-l.w/2),marketFrontageGap:9.5,canopyGap:5.9},planningGeometry:preview.metrics};
}
