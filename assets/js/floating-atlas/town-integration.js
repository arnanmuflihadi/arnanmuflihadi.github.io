import * as T from '../vendor/three-atlas.module.js?v=16';
import {createModelLibrary,assetCatalog,modelMetrics} from '../urban-atlas/model-library.js?v=15';
import {createSupportIndex} from '../architecture-r0b1/preview.js?v=74';
import {worldHeight as groundHeight} from './support.js?v=73';
import {blocked,slide,clearDistance,movementOptions} from './collision.js?v=73';
import {createTownStabilization} from './town-stabilization.js';
import {createTownTerrain} from './town-terrain.js';
import {createTownSquare,squareAsset} from './town-square.js';
import {circulationCatalog,createCirculationMasks,prepareCirculationStone} from './town-circulation.js';

export const townCatalog=Object.freeze(Object.fromEntries(Object.entries({
 market:'market-street-s2d/market-street-optimized.glb',interfaces:'market-street-s2e/common-interface.glb',
 foundations:'market-street-s2e/foundation-hybrid.glb',support:'market-street-s2e/support-reference.glb'
}).map(([id,p])=>[id,{url:new URL('../../../validation/'+p,import.meta.url).href,license:'See preserved S2-C/D/E asset records'}])));
export function createTownLibrary(){const loader=new T.GLTFLoader();return createModelLibrary({catalog:{...assetCatalog,...townCatalog,square:squareAsset,...circulationCatalog},load:url=>loader.loadAsync(url)});}
function ancestor(o,key){for(let p=o;p;p=p.parent)if(p.userData[key])return true;return false;}

export async function integrateTown(world,{terrainStudy=false,squareStudy=false,circulationStudy=false}={}){
 const group=new T.Group();group.name='S2-F local development town';
 squareStudy=squareStudy||circulationStudy;
 const catalog=circulationStudy?{...townCatalog,circulationInterfaces:circulationCatalog.circulationInterfaces}:townCatalog;
 const models=Object.fromEntries(await Promise.all(Object.keys(catalog).map(async id=>[id,(await world.library.get(id)).scene])));
 let manifest,circulationManifest;models.circulationInterfaces?.traverse(o=>{if(o.userData.site_manifest)circulationManifest=JSON.parse(o.userData.site_manifest);});models.interfaces.traverse(o=>{if(o.userData.site_manifest)manifest=JSON.parse(o.userData.site_manifest);});
 if(!manifest)throw Error('S2-E interface manifest is missing');
 for(const [id,r]of Object.entries(models)){
  r.position.set(36,18.6,44);r.traverse(o=>{if(o.userData.study_grading)o.visible=false;if(o.isMesh){o.castShadow=o.receiveShadow=true;if(ancestor(o,'walkable'))o.userData.walkable=true;}});
  r.updateMatrixWorld(true);if(id!=='support')group.add(r);
 }
 const raw=createSupportIndex(models.market,()=>-500),site=createSupportIndex(models.interfaces,()=>-500),support=createSupportIndex(models.support,()=>-500);
 const circulationSite=models.circulationInterfaces?createSupportIndex(models.circulationInterfaces,()=>-500):null;
 const original=world.obstacles,solids=[...original,...manifest.plots.map(([id,u,v,w,d,h])=>({x:36+u,z:44-v,w,d,minY:18.6+h,h:28.6+h,building:id})),...manifest.colliders];
 const instances=new Map();models.market.traverse(o=>{if(o.isInstancedMesh&&o.count===7)instances.set(o,o.instanceMatrix.array.slice());});
 const metrics=Object.fromEntries(Object.entries(models).map(([k,r])=>[k,modelMetrics(r)])),stabilization=createTownStabilization(world,models,manifest);
 const terrain=(terrainStudy||squareStudy)?createTownTerrain(world,{surfaceAt:(x,z)=>Math.max(raw(x,z),site(x,z),support(x,z))}):null;
 let terrainRequested=terrainStudy||squareStudy;
 const square=squareStudy?createTownSquare(world,(await world.library.get('square')).scene):null;if(square)group.add(square.root);let squareRequested=squareStudy;
 const repairedSquare=circulationStudy?createTownSquare(world,(await world.library.get('circulationSquare')).scene,{clearanceAt:circulationSite}):null;if(repairedSquare)group.add(repairedSquare.root);
 const masks=circulationStudy?createCirculationMasks(models.market,circulationManifest.circulation_network.market_mask_volumes,circulationManifest.circulation_network.prop_instance_moves):null;let circulationRequested=circulationStudy;
 const restoreCirculationStone=circulationStudy?prepareCirculationStone(models.circulationInterfaces):null;
 const activeSquare=()=>circulationRequested&&repairedSquare?repairedSquare:square;
 const clearSquares=()=>{repairedSquare?.setEnabled(false);square?.setEnabled(false);};
 if(terrainStudy||squareStudy)stabilization.setGlass('B');
 let enabled=false,disposed=false;const ray=new T.Raycaster(),direction=new T.Vector3();
 const active=(y,list)=>enabled?list.filter(o=>!Number.isFinite(o.minY)||y+1.9>o.minY&&y<o.h-.05):list;
 function applyTerrain(){clearSquares();terrain?.setEnabled(enabled&&terrainRequested&&stabilization.polished);world.obstacles=enabled?stabilization.obstacles(solids):original;if(terrain?.enabled)world.obstacles=terrain.obstacles(world.obstacles);if(circulationManifest&&circulationRequested&&enabled){const oldGuards=new Set(manifest.colliders);world.obstacles=world.obstacles.filter(o=>!oldGuards.has(o));world.obstacles.push(...circulationManifest.colliders);}models.interfaces.visible=!(enabled&&circulationRequested);if(models.circulationInterfaces)models.circulationInterfaces.visible=enabled&&circulationRequested;masks?.setEnabled(enabled&&circulationRequested);const current=activeSquare();if(current){current.setEnabled(enabled&&squareRequested);if(current.enabled)world.obstacles=[...world.obstacles,...current.colliders];}}
 const api={group,models,manifest,stabilization,terrain,get square(){return activeSquare();},circulation:circulationStudy?{manifest:circulationManifest.circulation_network,masks:()=>masks.summary(),metrics:()=>repairedSquare.metrics}:null,
  get circulationEnabled(){return enabled&&circulationRequested;},setCirculationEnabled(value){circulationRequested=Boolean(value);applyTerrain();},
  setSquareEnabled(value){squareRequested=Boolean(value);applyTerrain();},
  setTerrainEnabled(value){clearSquares();terrain?.setEnabled(false);terrainRequested=Boolean(value);applyTerrain();},
  setPolished(value){clearSquares();terrain?.setEnabled(false);stabilization.setPolished(value);applyTerrain();},
  metrics,
  get enabled(){return enabled;},heightAt:(x,z)=>enabled?Math.max(terrain?.heightAt(x,z)??groundHeight(x,z),raw(x,z),circulationRequested&&circulationSite?circulationSite(x,z):site(x,z),support(x,z),activeSquare()?.enabled?activeSquare().support(x,z):-500):groundHeight(x,z),
  movementOptions(getY){return {...movementOptions,heightAt:api.heightAt,collision:{blocked:(x,z,list,r)=>blocked(x,z,active(getY(),list),r),slide:(p,dx,dz,list)=>slide(p,dx,dz,active(p.y,list))}};},
  clearance(a,b,list){let distance=clearDistance(a,b,list,.28,terrain?.enabled?terrain.heightAt:groundHeight);if(!enabled)return distance;const length=a.distanceTo(b);ray.set(a,direction.copy(b).sub(a).normalize());ray.far=length;const hit=ray.intersectObject(group,true).find(h=>{for(let p=h.object;p;p=p.parent)if(!p.visible)return false;return !ancestor(h.object,'study_grading');});return hit?Math.min(distance,hit.distance):distance;},
  setEnabled(value){if(disposed)return;clearSquares();terrain?.setEnabled(false);enabled=Boolean(value);if(enabled)world.scene.add(group);else group.removeFromParent();stabilization.setEnabled(enabled);applyTerrain();
   for(const[o,before]of instances){o.instanceMatrix.array.set(before);if(enabled){const m=new T.Object3D().matrix;for(let i=0;i<o.count;i++){o.getMatrixAt(i,m);const e=m.elements,p=manifest.landscape_alignment.find(p=>Math.abs(e[12]-p.u)<.01&&Math.abs(e[14]+p.v)<.01);if(p){e[13]+=p.delta_h;o.setMatrixAt(i,m);}}}o.instanceMatrix.needsUpdate=true;o.computeBoundingSphere();o.computeBoundingBox();}
   masks?.setEnabled(enabled&&circulationRequested);
  },
  cache:()=>world.library.stats(),dispose(){if(disposed)return;api.setEnabled(false);disposed=true;restoreCirculationStone?.();masks?.dispose();repairedSquare?.dispose();square?.dispose();terrain?.dispose();stabilization.dispose();for(const[o,before]of instances)o.instanceMatrix.array.set(before);group.clear();}
 };api.setEnabled(true);return api;
}
