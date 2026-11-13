import * as T from '../vendor/three-atlas.module.js?v=16';
export const circulationCatalog={
 circulationInterfaces:{url:new URL('../../../validation/circulation-c1c/circulation-interfaces.glb',import.meta.url).href,license:'Project-original and preserved S2-E components; see C1C asset record'},
 circulationSquare:{url:new URL('../../../validation/circulation-c1c/circulation-square.glb',import.meta.url).href,license:'Approved C1B fountain/pavilion plus project-original circulation derivative'}
};
export const circulationRoutes={
 journey:[[27,57],[26.2,54],[25.1,52.7],[25.1,52],[26,52],[30.15,51.8],[36,44],[36,35],[36,27],[36,17],[35,12.6],[30,12.6],[28.02,12.6],[26.4,12.6],[25.4,12.6],[20.5,12.6],[17.8,12.6],[16,12],[3,12],[-5,5]],
 portal:[[35,12.6],[30,12.6],[28.02,12.6],[26.4,12.6],[26.2,12.6]],
 guild:[[26.2,12.6],[25.9,12.6],[25.9,6],[25.9,4.6],[26.6,4],[28.3,3.8],[29.8,3],[31,1.5],[33,.5],[36,0],[40,-4],[44,-8]],
 guard:[[26.2,6],[30,6]],
};
export function prepareCirculationStone(root){
 const changes=[],clones=new Map();root.traverse(o=>{if(!o.isMesh||!/^C1 \/ warm (limestone|volcanic stone)$/.test(o.material.name))return;const original=o.material;let copy=clones.get(original);if(!copy){copy=original.clone();copy.shadowSide=T.BackSide;clones.set(original,copy);}o.material=copy;changes.push({o,original});});
 return()=>{for(const c of changes)c.o.material=c.original;for(const m of clones.values())m.dispose();};
}
export function createCirculationMasks(market,volumes,moves=[]){
 const changes=[],instances=[],v=new T.Vector3();market.updateMatrixWorld(true);
 market.traverse(o=>{if(!o.isInstancedMesh)return;const m=new T.Object3D().matrix;for(let i=0;i<o.count;i++){o.getMatrixAt(i,m);v.setFromMatrixPosition(m).applyMatrix4(o.matrixWorld);const move=moves.find(p=>Math.hypot(v.x-p.from[0],v.z-p.from[1])<.02);if(!move)continue;const destination=v.clone().add(new T.Vector3(move.delta[0],0,move.delta[1])).applyMatrix4(o.matrixWorld.clone().invert()),after=m.clone().setPosition(destination);instances.push({o,i,before:m.clone(),after});}});
 function category(o){for(let p=o;p;p=p.parent)if(['StreetFurniture','Landscape'].includes(p.name))return p.name;return null;}
 for(const o of market.getObjectsByProperty('isMesh',true)){
  if(o.isInstancedMesh)continue;const scope=category(o),boxes=scope==='StreetFurniture'?volumes:scope==='Landscape'?volumes.filter(b=>b.object&&(b.source.startsWith('Square focal tree bed')||b.source.startsWith('Ginger flower')||b.source.startsWith('Broadleaf garden clump'))):[];if(!boxes.length)continue;const g=o.geometry,a=g.attributes.position,ix=g.index,kept=[];let removed=0;
  for(let i=0;i<ix.count;i+=3){const points=[0,1,2].map(j=>v.fromBufferAttribute(a,ix.getX(i+j)).applyMatrix4(o.matrixWorld).toArray());if(boxes.some(b=>points.every(p=>p.every((x,k)=>x>=b.min[k]-.025&&x<=b.max[k]+.025))))removed++;else kept.push(ix.getX(i),ix.getX(i+1),ix.getX(i+2));}
  if(!removed)continue;const copy=new T.BufferGeometry();for(const[k,a]of Object.entries(g.attributes))copy.setAttribute(k,a);copy.setIndex(kept);copy.boundingBox=g.boundingBox?.clone();copy.boundingSphere=g.boundingSphere?.clone();changes.push({o,source:g,copy,removed});
 }
 function setEnabled(value){for(const c of changes)c.o.geometry=value?c.copy:c.source;for(const c of instances){c.o.setMatrixAt(c.i,value?c.after:c.before);c.o.instanceMatrix.needsUpdate=true;c.o.computeBoundingSphere();c.o.computeBoundingBox();}}
 return{setEnabled,summary:()=>({meshes:changes.length,removedTriangles:changes.reduce((n,c)=>n+c.removed,0),relocatedTreeComponents:instances.length,scope:'Selected furniture and planter-bed triangles plus one town planter tree; original building meshes unchanged'}),dispose(){setEnabled(false);for(const c of changes){for(const k of Object.keys(c.copy.attributes))c.copy.deleteAttribute(k);c.copy.dispose();}}};
}
