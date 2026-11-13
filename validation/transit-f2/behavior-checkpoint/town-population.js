import * as T from '../vendor/three-atlas.module.js?v=16';
import {modelMetrics} from '../urban-atlas/model-library.js?v=15';
import {toWorld,right} from './reconstruction-plan.js';
import {clearDistance} from './collision.js?v=73';
export const populationCatalog={townProps:{url:new URL('../../game/town-population/props.glb?v=1',import.meta.url).href,license:'CC0-1.0 · Kenney Furniture Kit / Food Kit'}};
export function populationEnabled(url=globalThis.location?.href){const u=new URL(url);return ['localhost','127.0.0.1','[::1]'].includes(u.hostname)&&u.searchParams.get('dev-town')==='s2f'&&u.searchParams.get('town-layout')==='reset-final'&&u.searchParams.get('town-props')==='cc0';}
export const placements=[];
const add=(id,u,v,{lift=0,turn=0,solid=false,scale=1}={})=>placements.push({id,u,v,lift,turn,solid,scale});
// Two small café settings occupy the frontage, along the paving edge; the central walking corridor stays clear.
for(const v of[3.1,9.0]){
 add('tableRound',-2.8,v,{solid:true});for(const d of[-.76,.76])add('chair',-2.8,v+d,{turn:d<0?Math.PI:0,solid:true});
 add('cup-saucer',-2.94,v+.18,{lift:.765});add('cup-coffee',-2.94,v+.18,{lift:.79});add('plate',-2.62,v-.15,{lift:.765});add('croissant',-2.62,v-.15,{lift:.79,turn:.5});
}
// Lembaran's book counter and delivery boxes leave its central entrance clear.
add('kitchenBar',3.3,3,{turn:Math.PI/2,solid:true});add('stoolBar',2.72,2.65,{solid:true});
add('books',3.3,2.65,{lift:1.025});add('books',3.3,3.1,{lift:1.025,turn:.35});add('plantSmall2',3.3,3.55,{lift:1.025});
for(const v of[8.8,9.35])add('cardboardBoxOpen',3.15,v,{solid:true,turn:.2});
add('banana',3.15,8.8,{lift:.29,turn:.8,scale:.7});add('bread',3.15,9.35,{lift:.29});
for(const[u,v]of[[-3.05,4.65],[-3.05,7.45],[3.05,4.7],[3.05,7.4],[-7,20],[7,24],[-4.8,28],[4.8,28]])add('pottedPlant',u,v,{solid:true});
// One quiet square-side seating pocket; the fountain bypass and future Guild axis stay empty.
add('bench',-6.6,18.2,{turn:Math.PI/2,solid:true});add('tableRound',5.1,22.6,{solid:true});
for(const d of[-.76,.76])add('chair',5.1+d,22.6,{turn:d<0?-Math.PI/2:Math.PI/2,solid:true});
add('cup-saucer',4.9,22.6,{lift:.765});add('cup-coffee',4.9,22.6,{lift:.79});add('plate',5.25,22.5,{lift:.765});add('coconut-half',5.25,22.5,{lift:.79});
for(const[u,v,s]of[[10.8,34,.68],[12.5,34.9,.83],[15.7,35,.65]])add('fern',u,v,{scale:s});
export async function populateTown(world,town){
 const source=(await world.library.get('townProps')).scene,fern=(await world.library.get('fern')).scene,root=new T.Group();root.name='CC0 curated town population';
 const angle=-Math.atan2(right[1],right[0]),buckets=new Map(),colliders=[],ledger=[],owned=[],originalSet=town.setEnabled,originalClear=town.clearance;let enabled=false,disposed=false;

 for(const p of placements){
  const src=p.id==='fern'?fern:source.getObjectByName(p.id);if(!src)throw Error('Missing imported prop: '+p.id);
  const item=src.clone(true),[x,z]=toWorld(p.u,p.v),anchor=new T.Group();anchor.position.set(x,town.heightAt(x,z)+.006+p.lift,z);anchor.rotation.y=angle+p.turn;anchor.scale.setScalar(p.scale);anchor.add(item);anchor.updateMatrixWorld(true);
  const box=new T.Box3().setFromObject(anchor),size=box.getSize(new T.Vector3()),centre=box.getCenter(new T.Vector3());
  if(p.solid)colliders.push({x:centre.x,z:centre.z,w:size.x,d:size.z,minY:box.min.y,h:box.max.y,prop:'CC0 '+p.id});
  ledger.push({...p,world:anchor.position.toArray(),bounds:{min:box.min.toArray(),max:box.max.toArray()}});
  anchor.traverse(o=>{if(!o.isMesh)return;const key=o.geometry.uuid+'|'+(Array.isArray(o.material)?o.material.map(m=>m.uuid).join(','):o.material.uuid),b=buckets.get(key)||{geometry:o.geometry,material:o.material,matrices:[],id:p.id};b.matrices.push(o.matrixWorld.clone());buckets.set(key,b);});
 }
 for(const b of buckets.values()){const m=new T.InstancedMesh(b.geometry,b.material,b.matrices.length);m.name='Imported '+b.id+' / shared instances';b.matrices.forEach((t,i)=>m.setMatrixAt(i,t));m.instanceMatrix.needsUpdate=true;m.castShadow=true;m.receiveShadow=true;m.computeBoundingSphere();root.add(m);owned.push(m);}
 const apply=(on)=>{enabled=Boolean(on)&&town.enabled;if(enabled){world.scene.add(root);world.obstacles=[...world.obstacles.filter(o=>!colliders.includes(o)),...colliders];}else{root.removeFromParent();world.obstacles=world.obstacles.filter(o=>!colliders.includes(o));}};
 const api={root,ledger,colliders,get enabled(){return enabled;},setEnabled:apply,summary(){return{enabled,uniqueModels:new Set(placements.map(p=>p.id)).size,newModels:16,reusedModels:1,instances:placements.length,instancedBatches:root.children.length,assets:modelMetrics(root),colliders:colliders.length,ledger};},dispose(){if(disposed)return;apply(false);disposed=true;town.setEnabled=originalSet;town.clearance=originalClear;owned.forEach(m=>m.dispose());root.clear();}};
 town.setEnabled=function(on){apply(false);originalSet.call(town,on);if(on)apply(true);};
 const ray=new T.Raycaster(),direction=new T.Vector3();town.clearance=function(a,b,list){let clear=originalClear.call(town,a,b,list);if(!enabled)return clear;clear=Math.min(clear,clearDistance(a,b,colliders,.28,town.heightAt));ray.set(a,direction.copy(b).sub(a).normalize());ray.far=a.distanceTo(b);const hit=ray.intersectObject(root,true)[0];return hit?Math.min(clear,hit.distance):clear;};
 apply(true);return api;
}
