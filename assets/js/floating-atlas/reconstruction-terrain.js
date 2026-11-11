import * as T from '../vendor/three-atlas.module.js?v=16';
import {terrainSample,groundHeight,segmentPoint,terrainInfo} from './terrain.js?v=73';
import {streamPoints} from './plan.js?v=73';
import {townPlan as plan,toLocal,footprintDistance,civicHeight,buildingBase,optionalTrail,optionalDistance,publicArea} from './reconstruction-plan.js';
const smooth=t=>{const q=Math.max(0,Math.min(1,t));return q*q*(3-2*q);};
export function createSettlementShelf(world){
 const g=world.terrain.geometry,p=g.attributes.position,original={position:p.array.slice(),normal:g.attributes.normal.array.slice(),color:g.attributes.color.array.slice(),trail:g.attributes.trail.array.slice(),height:world.groundHeight},surface=[],changes=[];
 const features=[{u:-6,v:11.6,w:7,d:4.2},{u:0,v:6,w:9,d:19},{...plan.square,w:17,d:16},{...plan.guild,w:12,d:10},...plan.buildings.map(b=>({...b,w:b.w+1.5,d:b.d+1.5,building:true}))];
 const branchLengths=optionalTrail.slice(1).map((b,i)=>Math.hypot(b[0]-optionalTrail[i][0],b[1]-optionalTrail[i][1])),branchTotal=branchLengths.reduce((a,b)=>a+b,0),branchStart=civicHeight(14),branchEnd=groundHeight(...optionalTrail.at(-1));
 function target(x,z,y){const[u,v]=toLocal(x,z),sample=terrainSample(x,z);if(sample.fraction>.98||z<20||z>82||x< -35||x>35)return y;
  let distance=Math.min(...features.map(q=>footprintDistance(u,v,q)),Math.max(0,Math.hypot(u-plan.landing.u,v-plan.landing.v)-plan.landing.r-1.5));
  let weight=1-smooth(distance/8),height=civicHeight(v);
  for(const b of plan.buildings){const d=footprintDistance(u,v,{...b,w:b.w+1.5,d:b.d+1.5});if(d<1.2)height+=(buildingBase(b)-.025-height)*(1-smooth(d/1.2));}
  // The optional forest branch joins the existing earth trail; it is not part of the civic spine.
  let nearest=null,travelled=0;for(let i=1;i<optionalTrail.length;i++){const a=optionalTrail[i-1],b=optionalTrail[i],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz))),d=Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t);if(!nearest||d<nearest.distance)nearest={distance:d,progress:travelled+branchLengths[i-1]*t};travelled+=branchLengths[i-1];}
  if(nearest){const blend=(1-smooth(Math.max(0,nearest.distance-1.65)/4))*smooth(nearest.progress/3),targetHeight=branchStart+(branchEnd-branchStart)*smooth(nearest.progress/branchTotal);height+=(targetHeight-height)*blend;weight=Math.max(weight,blend);}
  let water=Infinity;for(let i=1;i<streamPoints.length;i++)water=Math.min(water,segmentPoint(x,z,streamPoints[i-1],streamPoints[i]).distance);weight*=smooth((water-3.4)/3);weight*=1-smooth((sample.fraction-.88)/.07);return y+(height-y)*weight;
 }
 for(let i=0;i<p.count;i++){const x=p.getX(i),z=p.getZ(i),before=p.getY(i),after=Math.fround(target(x,z,before));surface.push([x,after,z]);if(Math.abs(after-before)>.00001)changes.push({index:i,x,z,before,after,delta:after-before});}
 const sample=(x,z)=>terrainSample(x,z,surface).height;let enabled=false;
 const api={changes,get enabled(){return enabled;},heightAt:(x,z)=>enabled?sample(x,z):original.height(x,z),
  setEnabled(value){enabled=Boolean(value);p.array.set(original.position);g.attributes.normal.array.set(original.normal);g.attributes.color.array.set(original.color);g.attributes.trail.array.set(original.trail);
   if(enabled){const color=new T.Color();for(const r of changes){p.setY(r.index,r.after);color.fromArray(original.color,r.index*3).lerp(new T.Color('#709054'),Math.min(.18,Math.abs(r.delta)*.04));g.attributes.color.setXYZ(r.index,color.r,color.g,color.b);if(publicArea(r.x,r.z,.4))g.attributes.trail.setX(r.index,0);if(optionalDistance(r.x,r.z)<1.4){g.attributes.trail.setX(r.index,1);color.set('#a58e69');g.attributes.color.setXYZ(r.index,color.r,color.g,color.b);}}g.computeVertexNormals();}
   p.needsUpdate=g.attributes.normal.needsUpdate=g.attributes.color.needsUpdate=g.attributes.trail.needsUpdate=true;g.computeBoundingBox();g.computeBoundingSphere();world.groundHeight=enabled?sample:original.height;
  },summary(){let area=0,fill=0,cut=0;const ix=g.index;for(let i=0;i<ix.count;i+=3){const a=ix.getX(i),b=ix.getX(i+1),c=ix.getX(i+2),vs=[a,b,c],d=vs.map(k=>surface[k][1]-original.position[k*3+1]);if(!d.some(n=>Math.abs(n)>.01))continue;const x=vs.map(k=>surface[k][0]),z=vs.map(k=>surface[k][2]),size=Math.abs((x[1]-x[0])*(z[2]-z[0])-(z[1]-z[0])*(x[2]-x[0]))/2;area+=size;fill+=size*d.reduce((n,v)=>n+Math.max(0,v),0)/3;cut+=size*d.reduce((n,v)=>n+Math.max(0,-v),0)/3;}return{changedVertices:changes.length,changedTriangleFootprintM2:area,fillEstimateM3:fill,cutEstimateM3:cut,minDelta:Math.min(...changes.map(c=>c.delta)),maxDelta:Math.max(...changes.map(c=>c.delta)),rimChanged:changes.some(c=>c.index>=p.count-terrainInfo.sectors),waterfallAndCliffsChanged:false,method:'Existing terrain vertices and triangle sampler; bounded local blending, same topology'};},
  dispose(){api.setEnabled(false);}
 };return api;
}
