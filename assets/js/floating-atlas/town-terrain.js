import * as T from '../vendor/three-atlas.module.js?v=16';
import {groundHeight,terrainSample} from './terrain.js?v=73';

const bell=t=>Math.abs(t)<1?(1-t*t)**2:0;
export function terrainLift(x,z,y=groundHeight(x,z)){
 if(x<15||x>35||z< -4||z>47||terrainSample(x,z).fraction>.75)return 0;
 const west=Math.max(bell((x-26)/8)*bell((z-32)/14),bell((x-25.5)/7.5)*bell((z-23)/9))*1.4;
 const civic=Math.min(1.35,Math.max(0,21.45-y))*bell((x-22)/7)*bell((z-7)/10);
 let lift=Math.max(west,civic),cap=Infinity;
 for(const [cx,cz,w,d,floor]of[[27.7,34,7.2,8,20.043],[27.7,22.2,8,8,21.96]])if(Math.abs(x-cx)<w/2+1&&Math.abs(z-cz)<d/2+1)cap=Math.min(cap,floor-.55);
 return Math.max(0,Math.min(lift,cap-y));
}

export function createTownTerrain(world,{surfaceAt}){
 const g=world.terrain.geometry,p=g.attributes.position,baseline={positions:p.array.slice(),normals:g.attributes.normal.array.slice(),colors:g.attributes.color.array.slice(),height:world.groundHeight},surface=[],changed=[],records=[],clones=new Map(),reverse=new Map();
 const objects=[];world.scene.traverse(o=>{if(o.isMesh)objects.push(o);});
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),z=p.getZ(i),y=p.getY(i),cap=surfaceAt(x,z),delta=Math.min(terrainLift(x,z,y),cap> -100?Math.max(0,cap-.4-y):Infinity);
  surface.push([x,Math.fround(y+delta),z]);if(delta>.00001)changed.push({index:i,x,z,before:y,after:surface[i][1],delta:surface[i][1]-y});
 }
 const sample=(x,z)=>terrainSample(x,z,surface).height;
 const delta=(x,z)=>sample(x,z)-groundHeight(x,z);
 const grass=objects.filter(o=>o.name==='Zone grass / curved blades');let enabled=false,disposed=false,states=[];
 const stats={vertices:changed.length,deltaMin:Math.min(...changed.map(v=>v.delta)),deltaMax:Math.max(...changed.map(v=>v.delta)),deltaMedian:[...changed].sort((a,b)=>a.delta-b.delta)[Math.floor(changed.length/2)]?.delta||0,addedTriangles:0,mode:'bounded positive earth adjustment; no terrain removal',vegetation:records};
 const previousUpdate=world.update;
 function grassGeometry(source){
  if(clones.has(source))return clones.get(source);
  const src=source.attributes.position,copy=source.clone(),a=copy.attributes.position;let moved=0;
  for(let k=0;k<src.count;k+=10){const x=(src.getX(k)+src.getX(k+1))/2,z=(src.getZ(k)+src.getZ(k+1))/2,dy=delta(x,z);if(Math.abs(dy)<.00001)continue;for(let j=0;j<10;j++)a.setY(k+j,src.getY(k+j)+dy);moved++;}
  if(!moved){copy.dispose();clones.set(source,source);return source;}
  a.needsUpdate=true;copy.computeVertexNormals();copy.computeBoundingSphere();copy.computeBoundingBox();clones.set(source,copy);reverse.set(copy,source);return copy;
 }
 world.update=function(...args){previousUpdate.apply(world,args);if(enabled)for(const o of grass)o.geometry=grassGeometry(reverse.get(o.geometry)||o.geometry);};
 function restore(){
  for(const row of states){if(row.instance!==undefined){row.object.setMatrixAt(row.instance,row.before);row.object.instanceMatrix.needsUpdate=true;row.object.computeBoundingSphere();row.object.computeBoundingBox();}}
  states=[];for(const o of grass)o.geometry=reverse.get(o.geometry)||o.geometry;
  p.array.set(baseline.positions);g.attributes.normal.array.set(baseline.normals);g.attributes.color.array.set(baseline.colors);p.needsUpdate=g.attributes.normal.needsUpdate=g.attributes.color.needsUpdate=true;g.computeBoundingBox();g.computeBoundingSphere();world.groundHeight=baseline.height;
 }
 const api={stats,changed,get enabled(){return enabled;},heightAt:(x,z)=>enabled?sample(x,z):baseline.height(x,z),
  setEnabled(value){if(disposed)return;restore();enabled=Boolean(value);records.length=0;if(!enabled)return;
   for(const row of changed)p.setY(row.index,row.after);p.needsUpdate=true;g.computeVertexNormals();g.computeBoundingBox();g.computeBoundingSphere();
   const green=new T.Color('#698b50'),c=new T.Color();for(const row of changed){c.fromArray(baseline.colors,row.index*3).lerp(green,Math.min(.16,row.delta*.09));g.attributes.color.setXYZ(row.index,c.r,c.g,c.b);}g.attributes.color.needsUpdate=true;world.groundHeight=api.heightAt;
   const m=new T.Object3D().matrix;
   for(const [ordinal,o]of objects.entries()){
    if(!o.isInstancedMesh||o.name.includes('cliff')||(!o.name.startsWith('Living landscape / canopy')&&![46,112,130,204,243].includes(o.geometry.attributes.position.count)))continue;
    for(let i=0;i<o.count;i++){o.getMatrixAt(i,m);const e=m.elements,dy=delta(e[12],e[14]);if(Math.abs(dy)<.00001)continue;states.push({object:o,instance:i,before:m.clone()});records.push({mesh:ordinal,instance:i,kind:o.name||'ground prop',x:e[12],z:e[14],deltaY:dy});e[13]+=dy;o.setMatrixAt(i,m);}
    o.instanceMatrix.needsUpdate=true;o.computeBoundingSphere();o.computeBoundingBox();
   }
   for(const o of grass)o.geometry=grassGeometry(reverse.get(o.geometry)||o.geometry);
  },
  obstacles(list){return enabled?list.map(o=>{if(!o.tree&&!o.rock)return o;const dy=delta(o.x,o.z);return Math.abs(dy)<.00001?o:{...o,minY:o.minY+dy,h:o.h+dy};}):list;},
  summary:()=>({...stats,enabled,vegetation:[...records],grassCopies:[...reverse.keys()].length,groundedProps:records.length}),
  dispose(){if(disposed)return;api.setEnabled(false);world.update=previousUpdate;for(const c of reverse.keys())c.dispose();clones.clear();reverse.clear();disposed=true;}
 };return api;
}
