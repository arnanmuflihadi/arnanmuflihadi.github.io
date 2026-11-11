import * as T from '../vendor/three-atlas.module.js?v=16';
import {createSupportIndex} from '../architecture-r0b1/preview.js?v=74';

const treeMoves=[{from:[45.64,37.88],delta:[4.8,2.8]},{from:[48.89,37.69],delta:[3.6,3.6]},{from:[49.81,27.54],delta:[4,0]},{from:[50.91,21.76],delta:[5,0]}];
const palmMove={from:[47,40],delta:[5,3]};
const near=(x,z,p)=>Math.hypot(x-p[0],z-p[1])<.06;
const inRange=b=>b.max.x>21&&b.min.x<55&&b.max.z> -4&&b.min.z<68;

export function createTownStabilization(world,models,manifest){
 const originals=[];world.scene.traverse(o=>{if(o.isMesh)originals.push(o);});
 const surfaces=[createSupportIndex(models.market,()=>-500),createSupportIndex(models.interfaces,()=>-500)],surface=(x,z)=>Math.max(...surfaces.map(s=>s(x,z)));
 const borrowed=new Set();
 function subset(source,indices){const copy=new T.BufferGeometry();for(const[k,a]of Object.entries(source.attributes))copy.setAttribute(k,a);copy.setIndex(indices);copy.boundingBox=source.boundingBox?.clone()||null;copy.boundingSphere=source.boundingSphere?.clone()||null;borrowed.add(copy);return copy;}
 const owns=[],matChanges=[],instanceChanges=[],palmChanges=[],grassChanges=[],obstacleChanges=new Map(),records=[];
 const m=new T.Object3D().matrix,v=new T.Vector3();let enabled=false,polish=true,variant='A',disposed=false;
 const hitsPath=b=>{for(const x of[b.min.x,(b.min.x+b.max.x)/2,b.max.x])for(const z of[b.min.z,(b.min.z+b.max.z)/2,b.max.z]){const h=surface(x,z);if(h> -100&&h>=b.min.y-.05&&h<=b.max.y+.1)return true;}return false;};
 const hitsBuilding=b=>manifest.plots.some(([,u,q,w,d,h])=>b.max.x>36+u-w/2-.15&&b.min.x<36+u+w/2+.15&&b.max.z>44-q-d/2-.15&&b.min.z<44-q+d/2+.15&&b.max.y>18.6+h+.1&&b.min.y<28.6+h);
 function patchInstance(o,i,dx,dz,reason,ordinal){
  o.getMatrixAt(i,m);const before=m.clone(),e=m.elements,x=e[12],z=e[14],anchor=reason.startsWith('palm')?palmMove.from:[x,z],dy=world.groundHeight(anchor[0]+dx,anchor[1]+dz)-world.groundHeight(...anchor);e[12]+=dx;e[13]+=dy;e[14]+=dz;
  instanceChanges.push({o,i,before,after:m.clone()});records.push({kind:o.name||'understory',mesh:ordinal,index:i,from:[x,before.elements[13],z],to:[e[12],e[13],e[14]],reason});
 }
 for(const [ordinal,o]of originals.entries()){
  const p=o.geometry.attributes.position;o.geometry.computeBoundingBox();
  if(o.isInstancedMesh){
   for(let i=0;i<o.count;i++){
    o.getMatrixAt(i,m);const e=m.elements,x=e[12],z=e[14],b=o.geometry.boundingBox.clone().applyMatrix4(m).applyMatrix4(o.matrixWorld);if(!inRange(b))continue;
    const tree=o.name==='Living landscape / canopy'&&treeMoves.find(t=>near(x,z,t.from));
    if(tree){patchInstance(o,i,...tree.delta,'crown intersects a building or undercroft edge',ordinal);continue;}
    if(!o.name&&p.count===26&&near(x,z,[47.4,40.4])){patchInstance(o,i,...palmMove.delta,'palm fronds intersect the shophouse roof edge',ordinal);continue;}
    if(![130,112,204,243].includes(p.count)||o.name.includes('cliff'))continue;
    if(!hitsPath(b)&&!hitsBuilding(b))continue;
    let target;for(const radius of[2.2,3.8,5.4,7]){for(const a of[0,.6,-.6,1.2,-1.2,Math.PI]){const dx=Math.cos(a)*radius*(x<36?-1:1),dz=Math.sin(a)*radius,g=world.groundHeight(x+dx,z+dz);if(g<1)continue;const moved=b.clone().translate(new T.Vector3(dx,g-world.groundHeight(x,z),dz));if(!hitsPath(moved)&&!hitsBuilding(moved)){target=[dx,dz];break;}}if(target)break;}
    if(target)patchInstance(o,i,...target,'individual understory intersects a walkable surface or building',ordinal);else records.push({kind:'unresolved',mesh:ordinal,index:i,from:[x,e[13],z]});
   }
  }else if(p.count===91){
   let x=0,z=0;for(let i=0;i<7;i++){x+=p.getX(i)/7;z+=p.getZ(i)/7;}if(near(x,z,palmMove.from)){const[dx,dz]=palmMove.delta,dy=world.groundHeight(x+dx,z+dz)-world.groundHeight(x,z);palmChanges.push({o,before:o.position.clone(),after:o.position.clone().add(new T.Vector3(dx,dy,dz))});records.push({kind:'palm trunk',mesh:ordinal,from:[x,world.groundHeight(x,z),z],to:[x+dx,world.groundHeight(x+dx,z+dz),z+dz],reason:'move with its ten fronds; retain original geometry'});}
  }
  if(o.name==='Zone grass / curved blades'){
   const levels=o.userData.detailLevels,removed=new Set(),g=levels.near,a=g.attributes.position;
   for(let k=0;k<a.count;k+=10){const b=new T.Box3();for(let j=0;j<10;j++)b.expandByPoint(v.fromBufferAttribute(a,k+j));if(!inRange(b)||!hitsPath(b)&&!hitsBuilding(b))continue;removed.add(k/10);records.push({kind:'grass blade',mesh:ordinal,index:k/10,origin:[(a.getX(k)+a.getX(k+1))/2,a.getY(k),(a.getZ(k)+a.getZ(k+1))/2],reason:'blade crosses paving or enclosed building volume'});}
   if(removed.size){const filtered={};for(const key of['near','far']){const source=levels[key],index=source.index.array,kept=[];for(let i=0;i<index.length;i+=3)if(!removed.has(Math.floor(index[i]/10)))kept.push(index[i],index[i+1],index[i+2]);const copy=subset(source,kept);filtered[key]=copy;owns.push(copy);}grassChanges.push({o,levels,filtered,removed:removed.size});}
  }
 }
 for(const t of treeMoves){const i=world.obstacles.findIndex(o=>o.tree&&Math.hypot(o.x-t.from[0],o.z-t.from[1])<1);if(i<0)throw Error('Missing tree collision proxy for '+t.from);const original=world.obstacles[i],[dx,dz]=t.delta,dy=world.groundHeight(t.from[0]+dx,t.from[1]+dz)-world.groundHeight(...t.from);obstacleChanges.set(original,{...original,x:original.x+dx,z:original.z+dz,minY:original.minY+dy,h:original.h+dy});}
 const glass=[];models.market.traverse(o=>{if(o.isMesh&&o.material.transmission>0)glass.push(o);});
 const glassOptions=glass.map(source=>{
  const a=source.material,b=new T.MeshStandardMaterial({name:a.name+' / S2G B stylized alpha',color:a.color.clone().multiplyScalar(.48),roughness:.19,metalness:.12,transparent:true,opacity:.18,depthWrite:false,vertexColors:a.vertexColors,map:a.map,aoMap:a.aoMap,aoMapIntensity:a.aoMapIntensity});owns.push(b);
  const cheap=source.clone(false);cheap.name='S2G glass B';cheap.material=b;source.parent.add(cheap);cheap.visible=false;
  const indices=source.geometry.index,positions=source.geometry.attributes.position,high=[],low=[];source.updateWorldMatrix(true,false);
  for(let i=0;i<indices.count;i+=3){const c=new T.Vector3();for(let j=0;j<3;j++)c.add(v.fromBufferAttribute(positions,indices.getX(i+j)).applyMatrix4(source.matrixWorld));c.multiplyScalar(1/3);const list=c.x>30.8&&c.y<23.2&&c.z>30&&c.z<38?high:low;list.push(indices.getX(i),indices.getX(i+1),indices.getX(i+2));}
  const detailed=subset(source.geometry,high),simple=subset(source.geometry,low);owns.push(detailed,simple);
  const front=source.clone(false),rest=source.clone(false);front.name='S2G glass C selected cafe frontage';rest.name='S2G glass C remaining alpha';front.geometry=detailed;rest.geometry=simple;rest.material=b;front.visible=rest.visible=false;source.parent.add(front,rest);
  return{source,cheap,front,rest,triangles:{authored:indices.count/3,retainedTransmission:high.length/3,alpha:low.length/3}};
 });
 for(const root of[models.market,models.interfaces,models.foundations])root.traverse(o=>{if(!o.isMesh||o.material.transmission>0||!/^S2[AC] \/ (warm pedestrian stone|limestone paving|sandstone base)/.test(o.material.name))return;const original=o.material,copy=original.clone();copy.name=original.name+' / S2G solid-stone shadow';copy.shadowSide=T.BackSide;owns.push(copy);matChanges.push({o,original,copy});});
 const originalUpdate=world.update;world.update=function(...args){originalUpdate.apply(world,args);for(const c of grassChanges){c.lastNative=c.o.geometry;if(enabled&&polish)c.o.geometry=c.lastNative===c.levels.far?c.filtered.far:c.filtered.near;}};
 function apply(){const on=enabled&&polish;for(const c of instanceChanges)c.o.setMatrixAt(c.i,on?c.after:c.before);for(const o of new Set(instanceChanges.map(c=>c.o))){o.instanceMatrix.needsUpdate=true;o.computeBoundingSphere();o.computeBoundingBox();}for(const c of palmChanges){c.o.position.copy(on?c.after:c.before);c.o.updateMatrixWorld(true);}for(const c of grassChanges)c.o.geometry=on?(c.lastNative===c.levels.far?c.filtered.far:c.filtered.near):(c.lastNative||c.levels.near);for(const c of matChanges)c.o.material=on?c.copy:c.original;
  for(const g of glassOptions){const choice=enabled?variant:'A';g.source.visible=choice==='A';g.cheap.visible=choice==='B';g.front.visible=g.rest.visible=choice==='C';}
 }
 const api={get variant(){return variant;},get polished(){return polish;},records,glassOptions,
  summary:()=>({enabled,polish,glass:variant,relocatedInstances:instanceChanges.length,palmTrunks:palmChanges.length,grassBlades:grassChanges.reduce((n,c)=>n+c.removed,0),changedGrassChunks:grassChanges.length,stoneShadowMeshes:matChanges.length,glassGeometry:glassOptions.map(g=>g.triangles),unresolved:records.filter(r=>r.kind==='unresolved')}),
  obstacles:list=>enabled&&polish?list.map(o=>obstacleChanges.get(o)||o):list,
  setEnabled(value){enabled=value;apply();},setPolished(value){polish=Boolean(value);apply();},setGlass(value){if(!['A','B','C'].includes(value))throw Error('Unknown glass variant');variant=value;apply();},
  dispose(){if(disposed)return;enabled=false;apply();disposed=true;world.update=originalUpdate;for(const g of glassOptions){g.cheap.removeFromParent();g.front.removeFromParent();g.rest.removeFromParent();}// Shared attributes stay owned by the source; only subset indices are released here.
   for(const g of borrowed)for(const k of Object.keys(g.attributes))g.deleteAttribute(k);owns.forEach(o=>o.dispose());}
 };return api;
}
