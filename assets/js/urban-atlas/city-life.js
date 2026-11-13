import * as T from '../vendor/three-atlas.module.js?v=16';
import{createRiggedActor,disposeAsset}from'./rigged-actor.js?v=22';
import{groundHeight}from'./layout.js?v=40';import{slide,blocked}from'./collision.js?v=40';
import {residents} from './npc-registry.js?v=22';
export {residents} from './npc-registry.js?v=22';
export function stepResident(position,target,speed,dt,obstacles,others=[]){
  let dx=target.x-position.x,dz=target.z-position.z;const distance=Math.hypot(dx,dz);if(distance<.1)return 0;
  dx/=distance;dz/=distance;
  for(const p of others){const x=position.x-p.x,z=position.z-p.z,d=Math.hypot(x,z);if(d>.001&&d<1.1){dx+=x/d*(1.1-d)*3.6;dz+=z/d*(1.1-d)*3.6;}}
  const length=Math.hypot(dx,dz)||1;dx/=length;dz/=length;
  if(blocked(position.x+dx*.65,position.z+dz*.65,obstacles,.4)){
    for(const angle of[.85,-.85,1.6,-1.6]){const x=dx*Math.cos(angle)-dz*Math.sin(angle),z=dx*Math.sin(angle)+dz*Math.cos(angle);if(!blocked(position.x+x*.7,position.z+z*.7,obstacles,.4)){dx=x;dz=z;break;}}
  }
  const x=position.x,z=position.z;slide(position,dx*Math.min(speed*dt,distance),dz*Math.min(speed*dt,distance),obstacles);return Math.hypot(position.x-x,position.z-z)/Math.max(.001,dt);
}
export async function createCityLife(scene,obstacles,{signal,researchOnly=false}={}){
  const loader=new T.GLTFLoader(),results=await Promise.allSettled([loader.loadAsync(new URL('../../game/phase3/city-resident.glb',import.meta.url).href),loader.loadAsync(new URL('../../game/characters/urban-explorer/urban-explorer.glb',import.meta.url).href)]);
  const assets=results.filter(r=>r.status==='fulfilled').map(r=>r.value);
  if(signal?.aborted||assets.length!==2){assets.forEach(disposeAsset);if(signal?.aborted)return null;throw Error('Residents unavailable');}
  const [asset,explorer]=assets;
  const people=residents.filter(spec=>!researchOnly||spec.id!=='sari').map((spec,i)=>{const p=spec.point||{x:spec.route[0][0],z:spec.route[0][1]};return{spec,actor:createRiggedActor(scene,spec.model==='explorer'?explorer:asset,{...p,shirt:spec.shirt,hair:spec.hair,pants:spec.pants,height:spec.height}),interactionState:'available',waypoint:1,wait:i*.35,age:i*1.7,budget:0,wave:0};});
  let speaking=null,disposed=false;
  function dispose(){if(disposed)return;disposed=true;people.forEach(p=>p.actor.dispose());assets.forEach(disposeAsset);signal?.removeEventListener('abort',dispose);}
  signal?.addEventListener('abort',dispose,{once:true});
  return{people,speak(id,player){speaking=id;for(const person of people){person.interactionState=person.spec.id===id?'speaking':'available';if(person.spec.id===id&&player)person.actor.root.rotation.y=Math.atan2(player.x-person.actor.root.position.x,player.z-person.actor.root.position.z);}},nearest(p){return people.map(n=>({...n.spec,distance:Math.hypot(n.actor.root.position.x-p.x,n.actor.root.position.z-p.z)})).filter(n=>n.distance<3).sort((a,b)=>a.distance-b.distance)[0]||null;},
    update(dt,anchor,player){
      for(const person of people){
        const{actor,spec}=person,pos=actor.root.position,distance=anchor?Math.hypot(pos.x-anchor.x,pos.z-anchor.z):0;person.budget+=dt;
        const interval=distance>35?.125:distance>20?.05:0;if(person.budget<interval)continue;
        const step=Math.min(.2,person.budget);person.budget=0;person.age+=step;let speed=0;
        if(speaking===spec.id&&player){actor.root.rotation.y=Math.atan2(player.x-pos.x,player.z-pos.z);}
        else if(spec.route){
          person.wait-=step;const target={x:spec.route[person.waypoint][0],z:spec.route[person.waypoint][1]};
          if(person.wait<=0){const x=pos.x,z=pos.z;speed=stepResident(pos,target,1.05,step,obstacles,people.filter(p=>p!==person).map(p=>p.actor.root.position).concat(player?[player]:[]));if(speed>.02){const yaw=Math.atan2(pos.x-x,pos.z-z),angle=Math.atan2(Math.sin(yaw-actor.root.rotation.y),Math.cos(yaw-actor.root.rotation.y));actor.root.rotation.y+=angle*(1-Math.exp(-8*step));}}
          if(Math.hypot(pos.x-target.x,pos.z-target.z)<.3){person.waypoint=(person.waypoint+1)%spec.route.length;person.wait=1.2+(person.waypoint%3)*.5;}
        }else if(player&&Math.hypot(player.x-pos.x,player.z-pos.z)<7){
          actor.root.rotation.y=Math.atan2(player.x-pos.x,player.z-pos.z);if(person.age>8&&person.wave<=0){person.wave=1.6;person.age=0;}
        }
        person.wave=Math.max(0,person.wave-step);const pose=person.wave>0&&actor.animator.actions.Wave?'Wave':speed<.05&&spec.idle==='Interact'&&person.age%12>9?'Interact':null;actor.animator.setOverride(pose,{duration:pose==='Wave'?1.6:2});
        pos.y=groundHeight(pos.x,pos.z);actor.animator.update(step,speed);
      }
    },dispose,
  };
}
