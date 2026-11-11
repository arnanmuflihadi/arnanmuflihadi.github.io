import{readFileSync,writeFileSync,existsSync}from'node:fs';
import{createHash}from'node:crypto';
import{execFileSync}from'node:child_process';
import * as T from'../../assets/js/vendor/three-atlas.module.js?v=16';
import{fixture}from'../town-s2g/fixture.mjs';
import{groundHeight}from'../../assets/js/floating-atlas/terrain.js';
const base=new URL('../../',import.meta.url),out=new URL('./',import.meta.url),files=execFileSync('git',['ls-files','-z','--cached','--others','--exclude-standard']).toString().split('\0').filter(p=>p&&!p.startsWith('validation/town-square-r0c1a/')&&!p.startsWith('docs/urban-atlas/town-square-r0c1a/'));
const hashes={};for(const p of files)try{hashes[p]=createHash('sha256').update(readFileSync(new URL(p,base))).digest('hex');}catch{}if(!existsSync(new URL('before-hashes.json',out)))writeFileSync(new URL('before-hashes.json',out),JSON.stringify(hashes,null,2));
const f=await fixture(),geometry=new Map(),materials=new Map(),instances=[],m=new T.Object3D().matrix,rotate=new T.Object3D().matrix;rotate.set(1,0,0,0,0,0,-1,0,0,1,0,0,0,0,0,1);const inverse=rotate.clone().invert();
function nativeMatrix(matrix){const n=rotate.clone().multiply(matrix).multiply(inverse);n.elements[12]-=36;n.elements[13]+=44;n.elements[14]-=18.6;return n.elements;}
for(const[ordinal,o]of f.original.entries()){
 const p=o.geometry.attributes.position;const kind=o.name==='Living landscape / canopy'?'tree':o.name.includes('fern')?'fern':!o.name&&p.count===26&&o.count===100?'palm frond':!o.name&&[130,112,204].includes(p.count)?'understory':!o.isInstancedMesh&&p.count===91?'palm trunk':null;if(!kind)continue;
 const count=o.isInstancedMesh?o.count:1;for(let i=0;i<count;i++){
  if(o.isInstancedMesh)o.getMatrixAt(i,m);else m.identity();const matrix=o.matrixWorld.clone().multiply(m);o.geometry.computeBoundingBox();const b=o.geometry.boundingBox.clone().applyMatrix4(matrix);if(b.max.x< -9||b.min.x>61||b.max.z< -29||b.min.z>32)continue;
  const key=o.geometry.uuid;if(!geometry.has(key)){const idx=o.geometry.index;geometry.set(key,{vertices:Array.from({length:p.count},(_,i)=>[p.getX(i),-p.getZ(i),p.getY(i)]),indices:idx?Array.from(idx.array):Array.from({length:p.count},(_,j)=>j),uv:o.geometry.attributes.uv?Array.from(o.geometry.attributes.uv.array):null,colors:o.geometry.attributes.color?Array.from(o.geometry.attributes.color.array):null,normals:o.geometry.attributes.normal?Array.from(o.geometry.attributes.normal.array):null});}
  if(!materials.has(o.material.uuid))materials.set(o.material.uuid,{name:o.material.name,kind,color:o.material.color.toArray(),roughness:o.material.roughness});instances.push({kind,mesh:ordinal,index:i,geometry:key,material:o.material.uuid,matrix:nativeMatrix(matrix),bounds:[b.min.toArray(),b.max.toArray()],source:'Actual R0A3 instance; approved S2G clearance applied'});
 }
}
const samples=[];for(let x=14;x<=48;x+=.5)for(let z=-10;z<=18;z+=.5)samples.push([x,z,groundHeight(x,z)]);
const manifest={site_point_order:'[game X, game Z, elevation/game Y]',phase:'R0-C1A isolated design only',mapping:'Blender (u,v,h) = (game x-36,44-game z,game y-18.6)',proposal:{name:'Telaga Awan / stepped pocket square',court:{x:[20.5,28],z:[4,14.4],floor:21.8},existingApron:{x:[28,44],z:[8,14.2],floor:22.614,unchanged:true},fountain:[24,9,21.8],arrival:{width:3.4,clearWidth:3.1,risers:5,riser:(22.614-21.8)/5,run:1.5},guildReservation:{endpoint:[44,-8,groundHeight(44,-8)+.08],unbuilt:true},highlandInterface:{point:[-5,5,groundHeight(-5,5)+.08],existingRoute:'ridge'}},samples,context:{geometries:Object.fromEntries(geometry),materials:Object.fromEntries(materials),instances}};
writeFileSync(new URL('site-context.json',out),JSON.stringify(manifest));console.log({protectedFiles:Object.keys(hashes).length,geometry:geometry.size,instances:instances.length,courtArea:7.5*10.4});f.dispose();
