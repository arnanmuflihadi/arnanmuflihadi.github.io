import * as T from '../vendor/three-atlas.module.js?v=16';
import {nearestPath} from './terrain.js?v=73';
import {safePosition} from './support.js?v=73';
import {blocked} from './collision.js?v=73';
import {chiselRock} from './nature.js?v=73';
import {fracturedRock} from './geology.js?v=73';
import {trailPlantGeometry} from './trail-plants.js?v=73';

export const habitatCatalog=Object.fromEntries([['bush','Bush_Small.gltf'],['bloom','Bush_Small_Flowers.gltf'],['flower','Flower_3_Clump.gltf']].map(([id,file])=>['habitat-'+id,{url:new URL('../../game/nature-r0f2/'+file,import.meta.url).href,license:'CC0-1.0 · Quaternius Ultimate Stylized Nature'}]));
export function habitatEnabled(url=globalThis.location?.href){const u=new URL(url);return ['localhost','127.0.0.1','[::1]'].includes(u.hostname)&&u.searchParams.get('dev-town')==='s2f'&&u.searchParams.get('town-layout')==='reset-final'&&u.searchParams.get('wildlife')==='r0f2'&&u.searchParams.get('nature')==='r0f2';}
// Small composed masses on the existing trail margins; none modify support or colliders.
const clusters=[
 {zone:'forest',x:-14,z:23,r:4}, {zone:'forest',x:-28,z:22,r:4}, {zone:'forest',x:-39,z:12,r:4}, {zone:'forest',x:-52,z:13,r:4}, {zone:'forest',x:-60,z:5,r:3}, {zone:'forest',x:16,z:26,r:3},{zone:'forest',x:5,z:20,r:3},
 {zone:'valley',x:-8,z:-1,r:4},{zone:'valley',x:-18,z:13,r:3},{zone:'valley',x:-26,z:-8,r:4},{zone:'valley',x:1,z:12,r:4},{zone:'valley',x:-34,z:-7,r:3},{zone:'valley',x:-29,z:3,r:3},
 {zone:'meadow',x:17,z:0,r:4},{zone:'meadow',x:24,z:8,r:4},{zone:'meadow',x:35,z:5,r:4},{zone:'meadow',x:42,z:15,r:4},{zone:'meadow',x:30,z:23,r:4},
 {zone:'cloudbreak',x:-74,z:8,r:2.8},{zone:'cloudbreak',x:-76,z:-2,r:3},{zone:'cloudbreak',x:-69,z:4,r:3},
 {zone:'ridge',x:-40,z:-43,r:2.8},{zone:'ridge',x:-50,z:-45,r:2.5},{zone:'ridge',x:-35,z:-36,r:3},{zone:'ridge',x:-53,z:-34,r:3}
];
const rand=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);};
export async function populateHabitat(world,town,wildlife){
 const root=new T.Group(),batches=new Map(),instances=[],ledger=[],materials=new Map(),rock=chiselRock(3),fractured=fracturedRock(1),broadleaf=trailPlantGeometry(),flowering=trailPlantGeometry(true),stone=new T.MeshStandardMaterial({color:'#919883',roughness:1,flatShading:true}),rockMaterial=new T.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:1,flatShading:true}),plantMaterial=new T.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:1,side:T.DoubleSide});root.name='R0-F2 local habitat composition';
 const homes=wildlife?.creatures||[];
 const valid=(x,z,r)=>{if(!safePosition(x,z)||blocked(x,z,world.obstacles,r))return false;const p=nearestPath(x,z);if(p.distance<p.width/2+r+.85)return false;if(Math.hypot(x+80,z-5)<4.5||Math.hypot(x+43.04,z+48.2)<5)return false;if(homes.some(a=>Math.hypot(x-a.x,z-a.z)<3.3||a.endpoint&&Math.hypot(x-a.endpoint.x,z-a.endpoint.z)<2.5))return false;const y=town.heightAt(x,z);return Number.isFinite(y)&&Math.abs(town.heightAt(x+.5,z)-y)<.27&&Math.abs(town.heightAt(x,z+.5)-y)<.27;};
 const addMesh=(geometry,material,matrix,key)=>{const b=batches.get(key)||{geometry,material,matrices:[]};b.matrices.push(matrix);batches.set(key,b);};
 await Promise.all(['habitat-bush','habitat-bloom','habitat-flower'].map(id=>world.library.get(id)));
 for(const [i,c] of clusters.entries())for(let j=0;j<32;j++){
  const seed=i*41+j,a=j*2.4+i*.7,dist=c.r*Math.sqrt((j+.4)/32),x=c.x+Math.cos(a)*dist,z=c.z+Math.sin(a)*dist;
  const ridge=c.zone==='ridge',kind=j%10===0?'outcrop':j%7===0?'rock':j%6===0?'broadleaf-flower':j%4===0?'bloom':j%3===0?'broadleaf':j%5===0?'flower':'bush',height=kind==='outcrop'?(ridge?.75:1.05)+rand(seed)*.35:kind==='rock'?(ridge?.44:.58)+rand(seed)*.26:kind==='flower'?.3+rand(seed)*.18:kind.startsWith('broadleaf')?(ridge?.52:.86)+rand(seed)*.22:ridge?.45+rand(seed)*.25:.95+rand(seed)*.5;
  if(!valid(x,z,kind==='outcrop'?1:kind==='rock'?.7:.45))continue;const y=town.heightAt(x,z),turn=rand(seed+90)*Math.PI*2;
  if(kind==='rock'||kind==='outcrop'){const o=new T.Object3D();o.position.set(x,y+height*.43,z);o.rotation.y=turn;o.scale.set(height*.85,height*.56,height*.72);o.updateMatrix();addMesh(kind==='rock'?rock:fractured,kind==='rock'?stone:rockMaterial,o.matrix.clone(),kind);}
  else if(kind.startsWith('broadleaf')){const o=new T.Object3D();o.position.set(x,y-.04,z);o.rotation.y=turn;o.scale.setScalar(height);o.updateMatrix();addMesh(kind==='broadleaf'?broadleaf:flowering,plantMaterial,o.matrix.clone(),kind);}
  else{const item=await world.library.instantiate('habitat-'+kind,{x,y:y-.035,z,height,rotation:turn,collidable:false});item.updateMatrixWorld(true);item.traverse(o=>{if(!o.isMesh)return;let material=materials.get(o.material.uuid);if(!material){material=o.material.clone();material.transparent=false;material.alphaTest=.45;material.depthWrite=true;materials.set(o.material.uuid,material);}const key=o.geometry.uuid+'|'+material.uuid;addMesh(o.geometry,material,o.matrixWorld.clone(),key);});}
  ledger.push({zone:c.zone,kind,x:Number(x.toFixed(2)),z:Number(z.toFixed(2)),y:Number(y.toFixed(2)),height:Number(height.toFixed(2))});
 }
 for(const b of batches.values()){const m=new T.InstancedMesh(b.geometry,b.material,b.matrices.length);b.matrices.forEach((t,i)=>m.setMatrixAt(i,t));m.instanceMatrix.needsUpdate=true;m.computeBoundingBox();m.computeBoundingSphere();m.castShadow=false;m.receiveShadow=true;root.add(m);instances.push(m);}world.scene.add(root);
 return {root,ledger,summary:()=>({instances:ledger.length,batches:instances.length,ledger}),dispose(){root.removeFromParent();instances.forEach(i=>i.dispose());materials.forEach(m=>m.dispose());for(const item of [rock,fractured,broadleaf,flowering,stone,rockMaterial,plantMaterial])item.dispose();root.clear();}};
}
