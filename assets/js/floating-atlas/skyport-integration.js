import * as T from '../vendor/three-atlas.module.js?v=16';
import {modelMetrics} from '../urban-atlas/model-library.js?v=15';
import {toWorld,toLocal,right} from './reconstruction-plan.js';

export const skyportCatalog={pelabuhanAwan:{url:new URL('../../game/skyport/pelabuhan-awan.glb?v=c3-final',import.meta.url).href,license:'Project-original canopy and reused civic components; Kenney Furniture Kit 2.0 CC0-1.0'}};
export function skyportDevelopmentEnabled(url=globalThis.location?.href){const u=new URL(url);return ['localhost','127.0.0.1','[::1]'].includes(u.hostname)&&['dev-town=s2f','town-layout=reset-final','town-props=cc0','town-guild=r0c2','town-skyport=r0c3'].every(pair=>{const[k,v]=pair.split('=');return u.searchParams.get(k)===v;});}
export const skyportSite=Object.freeze({u:0,v:-7,datum:15.095,diameter:13,rotation:35,extension:0,vegetationMoves:0});

export async function integrateSkyport(world,town){
 const root=new T.Group(),source=(await world.library.get('pelabuhanAwan')).scene,[x,z]=toWorld(0,-7),angle=-Math.atan2(right[1],right[0]);root.name='Pelabuhan Awan / R0-C3';root.position.set(x,skyportSite.datum,z);root.rotation.y=angle;root.add(source.clone(true));root.traverse(o=>{if(o.isMesh)o.castShadow=o.receiveShadow=true;});root.updateMatrixWorld(true);
 const oldSet=town.setEnabled,oldClear=town.clearance,colliders=[];
 function solid(u,v,w,d,top,prop){const[x,z]=toWorld(u,v),floor=town.heightAt(x,z);colliders.push({x,z,w,d,minY:floor-.02,h:floor+top,oriented:{w,d,rotation:angle},skyport:true,prop});}
 for(const u of[-3.3,3.3])for(const v of[-5.75,-2.6])solid(u,v,.48,.48,3.6,'Terminal timber pier and stone shoe');
 for(const u of[-4.5,4.5]){solid(u,-4.3,.4,1.7,.92,'Waiting bench');solid(u,-5.4,.5,.5,1.22,'Sheltered planter');}
 solid(4,-9.4,.65,.65,.65,'Cargo');solid(4.45,-9,.5,.5,.5,'Cargo');
 // Head-stop cells sample the visible canopy and sign underside; they never supply walking support.
 const upRay=new T.Raycaster(),up=new T.Vector3(0,1,0),bounds=new T.Box3().setFromObject(root);
 for(let x=bounds.min.x;x<bounds.max.x;x+=.55)for(let z=bounds.min.z;z<bounds.max.z;z+=.55){const heights=[];for(const[dx,dz]of[[0,0],[-.24,-.24],[-.24,.24],[.24,-.24],[.24,.24]]){upRay.set(new T.Vector3(x+dx,town.heightAt(x+dx,z+dz)+1.95,z+dz),up);upRay.far=5;const hit=upRay.intersectObject(root,true)[0];if(hit)heights.push(hit.point.y);}if(heights.length===5)colliders.push({x,z,w:.55,d:.55,minY:Math.min(...heights),h:Math.max(...heights)+.12,cameraOnly:true,skyport:true,roof:true});}
 for(let u=-2.8;u<=2.8;u+=.14){const[x,z]=toWorld(u,-6.24);colliders.push({x,z,w:.14,d:.14,minY:skyportSite.datum+2.61,h:skyportSite.datum+3.29,cameraOnly:true,skyport:true,roof:true,prop:'Visible identity fascia head-stop'});}
 let enabled=false,wanted=true,disposed=false;const ray=new T.Raycaster(),direction=new T.Vector3();
 function apply(on){enabled=Boolean(on)&&town.enabled;world.obstacles=world.obstacles.filter(o=>!colliders.includes(o));if(enabled){world.scene.add(root);world.obstacles.push(...colliders);}else root.removeFromParent();}
 town.setEnabled=function(on){apply(false);oldSet.call(town,on);apply(on&&wanted);};
 town.clearance=(a,b,list)=>{let clear=oldClear.call(town,a,b,enabled?list.filter(o=>!colliders.includes(o)):list);if(!enabled)return clear;ray.set(a,direction.copy(b).sub(a).normalize());ray.far=a.distanceTo(b);const hit=ray.intersectObject(root,true)[0];return hit?Math.min(clear,hit.distance):clear;};
 const api={root,colliders,get enabled(){return enabled;},contains(p){if(!enabled||!p)return false;const[u,v]=toLocal(p.x,p.z);return Math.hypot(u,v+7)<6.5;},setEnabled(on){wanted=Boolean(on);apply(wanted);},summary(){return{enabled,site:skyportSite,assets:modelMetrics(root),colliderCount:colliders.length,cache:world.library.stats(),travel:'Future boarding reservation only; no active travel interaction',terrainEdits:0,vegetationMoves:0};},dispose(){if(disposed)return;apply(false);disposed=true;town.setEnabled=oldSet;town.clearance=oldClear;root.clear();}};apply(true);return api;
}
