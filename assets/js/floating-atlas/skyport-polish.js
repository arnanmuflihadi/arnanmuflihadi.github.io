import * as T from '../vendor/three-atlas.module.js?v=16';
import {modelMetrics} from '../urban-atlas/model-library.js?v=15';
import {skyportDevelopmentEnabled} from './skyport-integration.js?v=c3-final';
import {toWorld,right} from './reconstruction-plan.js';

export const polishCatalog={skyportDetails:{url:new URL('../../../validation/skyport-r0c3-1/skyport-details.glb?v=final',import.meta.url).href,license:'Project-original detail assembly; reused Kenney CC0 fixture and approved civic meshes/materials'}};
export function polishEnabled(url=globalThis.location?.href){return skyportDevelopmentEnabled(url)&&new URL(url).searchParams.get('town-skyport-polish')==='r0c3-1';}
export async function decorateSkyport(world,town,skyport){
 const root=(await world.library.get('skyportDetails')).scene.clone(true);root.name='Pelabuhan Awan / C3.1 three refinements';
 const palette=new Map();skyport.root.traverse(o=>{if(o.isMesh)for(const m of Array.isArray(o.material)?o.material:[o.material])palette.set(m.name,m);});let shared=0;
 root.traverse(o=>{if(!o.isMesh)return;o.castShadow=o.receiveShadow=true;const reuse=m=>{if(!palette.has(m.name))throw Error('C3.1 palette mismatch: '+m.name);shared++;return palette.get(m.name);};o.material=Array.isArray(o.material)?o.material.map(reuse):reuse(o.material);});
 const rotation=-Math.atan2(right[1],right[0]),colliders=[[-3.55,-10.5,.75,.48,2.2],[3.55,-10.5,.75,.48,2.2],[-4.6,-8.3,.55,.55,5.2]].map(([u,v,w,d,h])=>{const[x,z]=toWorld(u,v),y=town.heightAt(x,z);return{x,z,w,d,minY:y-.02,h:y+h,oriented:{w,d,rotation},skyportPolish:true};});
 let wanted=false,disposed=false;
 const api={root,colliders,get enabled(){return wanted&&skyport.enabled;},setEnabled(on){wanted=Boolean(on);world.obstacles=world.obstacles.filter(o=>!colliders.includes(o));for(const o of colliders){const i=skyport.colliders.indexOf(o);if(i>=0)skyport.colliders.splice(i,1);}root.removeFromParent();if(wanted){skyport.root.add(root);skyport.colliders.push(...colliders);if(skyport.enabled)world.obstacles.push(...colliders);}},summary(){return{enabled:api.enabled,assets:modelMetrics(root),sharedExistingMaterialSlots:shared,newMaterialDefinitions:0,textures:0,colliders:colliders.length,terrainChanges:0,guardChanges:0,travel:'Inactive docking identity only'};},dispose(){if(disposed)return;api.setEnabled(false);disposed=true;root.clear();}};api.setEnabled(true);return api;
}
