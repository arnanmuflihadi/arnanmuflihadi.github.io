import * as T from '../vendor/three-atlas.module.js?v=16';
import {groundHeight,contextBlocks} from './layout.js?v=22';
// Repeated imported primitives share geometry and maps through instance batches.
export function buildImportedArchitecture(asset){
  const container=new T.Group();container.name='Licensed Jakarta architecture';
  const batches=new Map(),counts={},finishes=new Map();
  function finish(material,tone){if(!tone||!material.name.includes('RedBrick'))return material;const key=material.uuid+tone;if(!finishes.has(key)){const copy=material.clone();copy.color.set(tone);finishes.set(key,copy);}return finishes.get(key);}
  function place(id,{x,z,y=0,w,h,d,ry=0,uniform=false,tone}){
    const source=asset.scene.getObjectByName(id);if(!source)throw Error(`Missing architectural prefab ${id}`);
    const model=source.clone(true),box=new T.Box3().setFromObject(model),size=box.getSize(new T.Vector3()),holder=new T.Group();
    model.position.add(new T.Vector3(-(box.min.x+box.max.x)/2,-box.min.y,-(box.min.z+box.max.z)/2));holder.add(model);
    const sx=w? w/size.x:1,sy=h? h/size.y:sx,sz=d? d/size.z:sx;
    if(uniform)holder.scale.setScalar(Math.min(sx,sy,sz));else holder.scale.set(sx,sy,sz);
    holder.rotation.y=ry;holder.position.set(x,groundHeight(x,z)+y,z);holder.updateMatrixWorld(true);
    holder.traverse(o=>{if(!o.isMesh)return;const material=finish(o.material,tone),key=o.geometry.uuid+material.uuid;if(!batches.has(key))batches.set(key,{geometry:o.geometry,material,matrices:[],ids:new Set()});const batch=batches.get(key);batch.matrices.push(o.matrixWorld.clone());batch.ids.add(id);});
    counts[id]=(counts[id]||0)+1;
  }
  // Dense ruko street: imported recessed windows, doors, masonry and roof detail.
  // Bespoke low arcades, shade awnings and Indonesian signs remain in architecture.js.
  for(const[x,z,w,h,id,tone]of[[-8,-20,7.45,10.8,'shop','#f2dfbc'],[.4,-21,7.45,12,'mixed','#d5dfca'],[8.7,-20,6.95,10.4,'shop','#e9c9ac'],[-30.5,25,8.95,9.6,'shop','#f2dfbc'],[-21.5,31,8.95,11.2,'mixed','#d5dfca']])place(id,{x,z,w,h,d:6.95,y:.12,tone});
  for(const[x,z]of[[-8,-16.42],[.4,-17.42],[8.7,-16.42]])place('entrance',{x,z,w:1.9,h:2.6,d:.25});
  place('office',{x:21,z:0,w:13.8,d:12.8,h:18.6,y:.12});
  place('mixed',{x:-30.5,z:-24,w:9.8,d:7.8,h:13.5,y:.12,tone:'#d7decb'});
  place('mixed',{x:29,z:-23,w:10.8,d:7.8,h:14.5,y:.12,tone:'#e5d5bc'});
  for(const[x,z,w,d,h]of contextBlocks)place('shop',{x,z,w:w-.1,d:d-.1,h,y:.1,tone:'#dce0cd'});
  // Modular commercial entrance panels form the transit hall under its vaults.
  for(let x=-32.45;x<-13;x+=2.1){place('entrance',{x,z:-.18,w:2.1,h:3.6,d:.29,y:.7});place('glazing',{x,z:-5.76,w:2.1,h:3.6,d:.29,y:.7,ry:Math.PI});}
  // Civic research pavilion: imported green-framed glazed modules and AC details.
  for(let x=24;x<35;x+=2)place('civic',{x,z:24.55,w:2,h:3.3,d:.3,y:.28,ry:Math.PI});
  for(const[x,z,ry]of[[-11.1,-16.5,0],[11.4,-16.5,0],[-25.1,34.45,0],[25.5,6.55,0]])place('aircon',{x,z,w:.85,h:.6,d:.4,y:4.2,ry});
  // A small transit shelter uses the same imported façade vocabulary and glazing.
  for(const x of[-12.1,-10.1])place('glazing',{x,z:13.9,w:2,h:2.5,d:.22,y:.2,ry:Math.PI});
  for(const x of[-33,-31,-15,-13])place('bollard',{x,z:6.8,w:.23,h:.75,d:.23,y:.02});
  // Textured threshold paving, laid over existing supports without rerouting roads.
  for(let x=-31.5;x<=-14;x+=3)place('paving',{x,z:8.6,w:3,h:.15,d:3,y:-.145});
  for(let z=-4;z<=2;z+=3)for(const x of[-1.5,1.5])place('paving',{x,z,w:3,h:.15,d:3,y:-.145});
  for(const x of[-29,-14,14,29])for(const z of[-14.75,-9.25])place('drain',{x,z,w:.65,h:.025,d:.4,y:.003});
  for(const[x,z]of[[-20,-12],[20,-12],[-40,13],[40,13]])place('manhole',{x,z,w:.7,h:.025,d:.7,y:.003});
  for(const {geometry,material,matrices,ids}of batches.values()){
    const mesh=new T.InstancedMesh(geometry,material,matrices.length);matrices.forEach((matrix,i)=>mesh.setMatrixAt(i,matrix));mesh.castShadow=true;mesh.receiveShadow=true;mesh.computeBoundingSphere();mesh.name=[...ids].join('/');mesh.userData.prefabs=[...ids];container.add(mesh);
  }
  container.userData.prefabCounts=counts;
  return container;
}
