import * as T from'../vendor/three-atlas.module.js?v=16';
import{createRiggedActor,disposeAsset}from'../urban-atlas/rigged-actor.js?v=22';
import{npcById}from'../urban-atlas/npc-registry.js?v=22';
import{groundHeight}from'./terrain.js?v=63';
export async function createIslandGuide(scene){
 const asset=await new T.GLTFLoader().loadAsync(new URL('../../game/phase3/city-resident.glb',import.meta.url).href),spec={...npcById('nadia'),point:{x:-13,z:3},route:null},actor=createRiggedActor(scene,asset,{x:-13,z:3,height:spec.height,shirt:spec.shirt,hair:spec.hair,pants:spec.pants});actor.root.position.y=groundHeight(-13,3);let disposed=false,speaking=false;
 const person={spec,actor};return{people:[person],nearest(p){return Math.hypot(p.x+13,p.z-3)<3?spec:null;},speak(id){speaking=Boolean(id);},update(dt,player){if(player&&(speaking||Math.hypot(player.x+13,player.z-3)<8))actor.root.rotation.y=Math.atan2(player.x+13,player.z-3);actor.animator.update(dt,0);},dispose(){if(disposed)return;disposed=true;actor.dispose();disposeAsset(asset);}};
}
