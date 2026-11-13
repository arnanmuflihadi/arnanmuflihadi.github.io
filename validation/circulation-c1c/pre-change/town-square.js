import * as T from '../vendor/three-atlas.module.js?v=16';
import {createSupportIndex} from '../architecture-r0b1/preview.js?v=74';
import {modelMetrics} from '../urban-atlas/model-library.js?v=15';

export const squareAsset={url:new URL('../../../validation/town-square-c1b/town-square-optimized.glb',import.meta.url).href,license:'Project-original C1A geometry; see docs/urban-atlas/town-square-c1b/ASSET-RECORD.md'};
export function createTownSquare(world,root){
 root.name='Telaga Awan / C1B approved design export';root.position.set(36,18.6,44);
 const materialChanges=[],materialClones=new Map();
 let manifest;root.traverse(o=>{if(o.userData.square_manifest)manifest=JSON.parse(o.userData.square_manifest);if(o.isMesh){o.castShadow=o.receiveShadow=true;if(/weathered bronze|warm limestone|warm volcanic stone/.test(o.material.name)){const original=o.material;let m=materialClones.get(original);if(!m){m=original.clone();if(/bronze/.test(m.name)){m.metalness=.28;m.roughness=.42;m.emissive.copy(m.color);m.emissiveIntensity=.14;}else m.shadowSide=T.BackSide;materialClones.set(original,m);}materialChanges.push({mesh:o,original,copy:m});o.material=m;}}});
 if(!manifest)throw Error('Telaga Awan export manifest is missing');
 root.updateMatrixWorld(true);const support=createSupportIndex(root,()=>-500),metrics=modelMetrics(root),moves=[],records=[],grass=[],cache=new Map();
 const originals=[];world.scene.traverse(o=>{if(o.isMesh)originals.push(o);});
 const matrix=new T.Object3D().matrix;
 for(const o of originals){
  if(!o.isInstancedMesh||o.name.includes('cliff')||![112,130,204,243].includes(o.geometry.attributes.position.count))continue;
  for(let i=0;i<o.count;i++){o.getMatrixAt(i,matrix);const e=matrix.elements;if(e[12]>20.5&&e[12]<28&&e[14]>4&&e[14]<14.4){moves.push({o,i,before:matrix.clone()});records.push({kind:o.name||'groundcover',instance:i,from:[e[12],e[13],e[14]]});}}
 }
 let enabled=false,disposed=false;const previousUpdate=world.update;
 function filtered(source){if(cache.has(source))return cache.get(source);const p=source.attributes.position,indices=source.index.array,removed=new Set();for(let i=0;i<p.count;i+=10){const x=(p.getX(i)+p.getX(i+1))/2,z=(p.getZ(i)+p.getZ(i+1))/2,h=support(x,z);if(h> -100&&h>p.getY(i)-.15&&h<p.getY(i)+.75)removed.add(i/10);}if(!removed.size){cache.set(source,source);return source;}const g=new T.BufferGeometry();for(const[k,a]of Object.entries(source.attributes))g.setAttribute(k,a);const kept=[];for(let i=0;i<indices.length;i+=3)if(!removed.has(Math.floor(indices[i]/10)))kept.push(indices[i],indices[i+1],indices[i+2]);g.setIndex(kept);g.boundingBox=source.boundingBox?.clone();g.boundingSphere=source.boundingSphere?.clone();cache.set(source,g);return g;}
 for(const o of originals)if(o.name==='Zone grass / curved blades')grass.push({o,source:o.geometry});
 world.update=function(...args){previousUpdate.apply(world,args);if(enabled)for(const r of grass){r.source=r.o.geometry;r.o.geometry=filtered(r.source);}};
 const api={root,manifest,metrics,support,get enabled(){return enabled;},colliders:manifest.colliders,
  setEnabled(value){if(enabled){for(const r of moves)r.o.setMatrixAt(r.i,r.before);for(const r of grass)r.o.geometry=r.source;}enabled=Boolean(value);if(enabled){for(const r of moves){r.o.getMatrixAt(r.i,matrix);r.before=matrix.clone();}for(const r of grass)r.source=r.o.geometry;}
   if(enabled)for(const[index,r]of moves.entries()){const m=r.before.clone(),e=m.elements,x=e[12],z=e[14],nx=17,nz=4.8+2.2*index;e[12]=nx;e[14]=nz;e[13]+=world.groundHeight(nx,nz)-world.groundHeight(x,z);r.o.setMatrixAt(r.i,m);records[index].to=[e[12],e[13],e[14]];}
   for(const o of new Set(moves.map(r=>r.o))){o.instanceMatrix.needsUpdate=true;o.computeBoundingSphere();o.computeBoundingBox();}
   root.visible=enabled;
  },summary:()=>({enabled,metrics,clearances:records,colliders:manifest.colliders.length,floorY:manifest.court_floor_y,solidStoneShadowMaterials:[...materialClones.values()].filter(m=>m.shadowSide===T.BackSide).length,bronze:materialChanges.filter(r=>/bronze/.test(r.copy.name)).map(({copy:m})=>({name:m.name,metalness:m.metalness,roughness:m.roughness,emissiveIntensity:m.emissiveIntensity})),grassGeometryCopies:[...cache].filter(([a,b])=>a!==b).length}),
  dispose(){if(disposed)return;api.setEnabled(false);disposed=true;world.update=previousUpdate;for(const r of materialChanges)r.mesh.material=r.original;for(const m of materialClones.values())m.dispose();for(const[source,g]of cache)if(g!==source){for(const k of Object.keys(g.attributes))g.deleteAttribute(k);g.dispose();}cache.clear();}
 };return api;
}
