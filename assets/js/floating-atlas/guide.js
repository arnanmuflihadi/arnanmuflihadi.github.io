import * as T from'../vendor/three-atlas.module.js?v=16';
import{createRiggedActor,disposeAsset}from'../urban-atlas/rigged-actor.js?v=22';
import{npcById}from'../urban-atlas/npc-registry.js?v=22';
import{groundHeight}from'./terrain.js?v=73';
export async function createIslandGuide(scene,{library=null,position=null,heightAt=groundHeight}={}){
 const point=position||{x:-13,z:3},asset=library?await library.get('townGuide'):await new T.GLTFLoader().loadAsync(new URL('../../game/phase3/city-resident.glb',import.meta.url).href),spec={...npcById('nadia'),point,route:null},actor=createRiggedActor(scene,asset,{x:point.x,z:point.z,height:spec.height,shirt:spec.shirt,hair:spec.hair,pants:spec.pants});actor.root.position.y=heightAt(point.x,point.z);let disposed=false,speaking=false;
 const person={spec,actor};return{people:[person],nearest(p){return Math.hypot(p.x-point.x,p.z-point.z)<2.2?spec:null;},speak(id){speaking=Boolean(id);},update(dt,player){if(player&&(speaking||Math.hypot(player.x-point.x,player.z-point.z)<8))actor.root.rotation.y=Math.atan2(player.x-point.x,player.z-point.z);actor.animator.update(dt,0);},dispose(){if(disposed)return;disposed=true;actor.dispose();if(!library)disposeAsset(asset);}};
}
