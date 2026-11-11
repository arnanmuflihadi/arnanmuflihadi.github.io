import * as T from '../vendor/three-atlas.module.js?v=16';
import {nearestPath} from './terrain.js?v=73';
import {safePosition} from './support.js?v=73';
import {blocked} from './collision.js?v=73';

export const wildlifeCatalog=Object.fromEntries(['deer','fox','cow'].map(id=>['wildlife-'+id,{url:new URL('../../game/wildlife-r0f2/'+id+'.gltf',import.meta.url).href,license:'CC0-1.0 · Quaternius Ultimate Animated Animals'}]));
export function wildlifeEnabled(url=globalThis.location?.href){const u=new URL(url);return ['localhost','127.0.0.1','[::1]'].includes(u.hostname)&&u.searchParams.get('dev-town')==='s2f'&&u.searchParams.get('town-layout')==='reset-final'&&u.searchParams.get('wildlife')==='r0f2';}
// Habitat candidates are kept off the walking network and filtered against actual terrain and obstacles.
const animals=[['deer',-48,8,1.45],['deer',-52,7,1.3],['deer',-59,2,1.4],['fox',-40,11,.72],['fox',-56,-9,.72],['fox',-23,-9,.7],['cow',15,5,1.3],['cow',20,5,1.35],['cow',25,3,1.25],['deer',-30,-38,1.3],['deer',-23,-37,1.25],['fox',-48,-30,.7],['deer',38,8,1.35],['cow',39,15,1.3],['deer',-66,0,1.3]];
const patches=[[-47,8],[-54,3],[-61,1],[-36,10],[-20,1],[8,4],[19,5],[30,4],[-29,-38],[-48,-28],[34,6],[-57,-13]];
export function findWanderTarget(x,z,seed,valid){
 for(const distance of [2,1.5,1])for(let i=0;i<8;i++){
  const a=(seed+i)*Math.PI/4,dx=Math.cos(a)*distance,dz=Math.sin(a)*distance;
  if(Array.from({length:8},(_,n)=>valid(x+dx*(n+1)/8,z+dz*(n+1)/8,1.25)).every(Boolean))return {x:x+dx,z:z+dz};
 }
 return null;
}
export async function populateWildlife(world,town){
 const root=new T.Group();root.name='R0-F2 wildlife and forest understory';const creatures=[],batches=new Map(),instances=[];let disposed=false;
 const valid=(x,z,margin=1)=>{if(!safePosition(x,z)||blocked(x,z,world.obstacles,margin))return false;const path=nearestPath(x,z);if(path.distance<path.width/2+margin+1.2)return false;if(Math.hypot(x+80,z-5)<6||Math.hypot(x+43.04,z+48.2)<7)return false;const y=town.heightAt(x,z);return Number.isFinite(y)&&Math.abs(town.heightAt(x+.55,z)-y)<.35&&Math.abs(town.heightAt(x,z+.55)-y)<.35;};
 const sources=Object.fromEntries(await Promise.all(['deer','fox','cow'].map(async id=>[id,await world.library.get('wildlife-'+id)])));
 for(const [i,[id,x,z,height]] of animals.entries()){
  if(!valid(x,z,1.25))continue;const asset=sources[id],model=T.cloneSkeleton(asset.scene),visual=new T.Group(),anchor=new T.Group();model.updateMatrixWorld(true);const box=new T.Box3().setFromObject(model),size=box.getSize(new T.Vector3());if(!(size.y>0))continue;
  visual.scale.setScalar(height/size.y);model.position.y=-box.min.y;visual.add(model);anchor.add(visual);anchor.position.set(x,town.heightAt(x,z),z);anchor.rotation.y=i*2.37;root.add(anchor);
  model.traverse(o=>{if(o.isMesh){o.castShadow=false;o.receiveShadow=true;if(o.isSkinnedMesh){o.computeBoundingSphere();o.boundingSphere.radius*=2;}o.frustumCulled=true;}});
  const mixer=new T.AnimationMixer(model),clip=asset.animations.find(a=>a.name===(i%3===0?'Eating':'Idle_2'))||asset.animations.find(a=>a.name==='Idle'),walk=asset.animations.find(a=>a.name==='Walk'),alternate=asset.animations.find(a=>a.name===(clip?.name==='Eating'?'Idle_2':'Eating'));if(!clip||!walk)throw Error('Missing ambient or walk animation for '+id);const action=mixer.clipAction(clip),walkAction=mixer.clipAction(walk),alternateAction=alternate?mixer.clipAction(alternate):action;action.play();mixer.setTime((i*1.73)%Math.max(clip.duration,.01));const home={x,z},endpoint=findWanderTarget(x,z,i,valid);creatures.push({id,anchor,model,mixer,clip:clip.name,restClips:[clip.name,alternate?.name||clip.name],restActions:[action,alternateAction],rests:0,x,z,home,endpoint,target:endpoint,mode:'idle',timer:3+i%4,action,walkAction,atHome:true,speed:id==='fox'?.48:.36});
 }
 // Reuse the cached, licensed fern; mesh/material data remain owned by the library.
 for(const [i,[cx,cz]] of patches.entries())for(let j=0;j<5;j++){
  const a=j*2.4+i,dist=.5+j*.43,x=cx+Math.cos(a)*dist,z=cz+Math.sin(a)*dist;if(!valid(x,z,.35))continue;
  const fern=await world.library.instantiate('fern',{x,y:town.heightAt(x,z)-.04,z,height:.8+(j%3)*.25,rotation:a,collidable:false});fern.updateMatrixWorld(true);fern.traverse(o=>{if(!o.isMesh)return;const key=o.geometry.uuid+'|'+o.material.uuid,b=batches.get(key)||{geometry:o.geometry,material:o.material,matrices:[]};b.matrices.push(o.matrixWorld.clone());batches.set(key,b);});
 }
 for(const b of batches.values()){const mesh=new T.InstancedMesh(b.geometry,b.material,b.matrices.length);b.matrices.forEach((m,i)=>mesh.setMatrixAt(i,m));mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();mesh.receiveShadow=true;mesh.castShadow=false;root.add(mesh);instances.push(mesh);}
 world.scene.add(root);
 function animation(c,walking){const next=walking?c.walkAction:c.action;if(c.current===next)return;if(c.current)c.current.fadeOut(.35);next.reset().fadeIn(.35).play();c.current=next;}
 return {root,creatures,summary:()=>({animals:creatures.map(({id,x,z,clip,endpoint})=>({id,x,z,clip,endpoint})),fernInstances:instances.reduce((n,m)=>n+m.count,0),batches:instances.length}),runtime:()=>creatures.map(c=>({id:c.id,home:c.home,position:[c.anchor.position.x,c.anchor.position.y,c.anchor.position.z],mode:c.mode,clip:c.current===c.walkAction?'Walk':c.clip})),update(dt,camera,reduced,player){for(const c of creatures){const active=!reduced&&camera.position.distanceToSquared(c.anchor.position)<75*75;if(!active)continue;const nearPlayer=player&&Math.hypot(player.x-c.anchor.position.x,player.z-c.anchor.position.z)<2.8,nearAnimal=creatures.some(other=>other!==c&&Math.hypot(other.anchor.position.x-c.anchor.position.x,other.anchor.position.z-c.anchor.position.z)<1.4);
   if(c.mode==='idle'){animation(c,false);if(c.endpoint&&!nearPlayer&&!nearAnimal&&(c.timer-=dt)<=0)c.mode='walk';}
   else if(nearPlayer||nearAnimal){animation(c,false);}else{const dx=c.target.x-c.anchor.position.x,dz=c.target.z-c.anchor.position.z,d=Math.hypot(dx,dz),step=Math.min(d,c.speed*dt);if(d<.025){c.atHome=!c.atHome;c.target=c.atHome?c.endpoint:c.home;c.mode='idle';c.timer=3.5+(Math.abs(c.x+c.z)%3);c.rests++;c.action=c.restActions[c.rests%2];c.clip=c.restClips[c.rests%2];animation(c,false);}else{const x=c.anchor.position.x+dx/d*step,z=c.anchor.position.z+dz/d*step;if(!valid(x,z,1.25)){c.mode='idle';c.endpoint=null;animation(c,false);}else{animation(c,true);c.anchor.position.set(x,town.heightAt(x,z),z);const desired=Math.atan2(dx,dz),delta=Math.atan2(Math.sin(desired-c.anchor.rotation.y),Math.cos(desired-c.anchor.rotation.y));c.anchor.rotation.y+=delta*Math.min(1,dt*3);}}}c.mixer.update(dt);}},dispose(){if(disposed)return;disposed=true;root.removeFromParent();for(const c of creatures){c.mixer.stopAllAction();c.mixer.uncacheRoot(c.model);const skeletons=new Set();c.model.traverse(o=>{if(o.isSkinnedMesh)skeletons.add(o.skeleton);});skeletons.forEach(s=>s.dispose());}instances.forEach(m=>m.dispose());root.clear();}};
}
