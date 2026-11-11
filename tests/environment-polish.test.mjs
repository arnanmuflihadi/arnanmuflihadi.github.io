import test from'node:test';
import assert from'node:assert/strict';
import{readFileSync}from'node:fs';
import{createHash}from'node:crypto';
import * as T from'../assets/js/vendor/three-atlas.module.js?v=16';
import{createTerrainGeometry,groundHeight}from'../assets/js/floating-atlas/terrain.js?v=73';
import{outlineControls,areas,routes,reservations}from'../assets/js/floating-atlas/plan.js?v=73';
import{createFloatingWorld}from'../assets/js/floating-atlas/scene.js?v=73';
import{fixtureLibrary}from'./helpers/floating-fixture.mjs';
const hash=a=>createHash('sha256').update(Buffer.from(a.buffer,a.byteOffset,a.byteLength)).digest('hex');

test('environmental polish preserves every ground vertex, triangle, support sample, route and reservation',()=>{
 const original=JSON.parse(readFileSync(new URL('../docs/environment-polish-review/terrain-baseline.json',import.meta.url))),g=createTerrainGeometry();
 try{assert.equal(hash(g.attributes.position.array),original.positions);assert.equal(hash(g.index.array),original.indices);assert.equal(createHash('sha256').update(JSON.stringify({outlineControls,areas,routes,reservations})).digest('hex'),original.layoutHash);for(const[x,z,y]of original.samples)assert.equal(groundHeight(x,z),y);}finally{g.dispose();}
});

test('derived tree growth preserves source buffers and detail/animation changes reuse existing geometry',async()=>{
 const lib=fixtureLibrary(),source=await lib.get('tree'),sourceHashes=[];source.scene.traverse(o=>{if(o.isMesh)sourceHashes.push(hash(o.geometry.attributes.position.array));});
 const w=await createFloatingWorld({library:lib}),camera={position:new T.Vector3(27,24,57),quaternion:new T.Object3D().quaternion},pool=()=>{const s=new Set();w.scene.traverse(o=>{if(o.geometry)s.add(o.geometry);for(const g of Object.values(o.userData.detailLevels||{}))s.add(g);});return s;},ids=()=>[...pool()].map(g=>g.uuid).sort(),tracked=pool(),released=new Set();for(const g of tracked)g.addEventListener('dispose',()=>released.add(g));
 try{const now=[];source.scene.traverse(o=>{if(o.isMesh)now.push(hash(o.geometry.attributes.position.array));});assert.deepEqual(now,sourceHashes);assert.ok(Object.values(w.stats.growthForms).every(n=>n>0));assert.equal(w.stats.derivedTreeGeometries,10);const before=ids();w.update(5,false,camera);const standard=w.stats.detail.activeGrassChunks;assert.ok(standard>0);w.setQuality(true);w.update(5,false,camera);assert.ok(w.stats.detail.activeGrassChunks>0&&w.stats.detail.activeGrassChunks<=standard);camera.position.set(400,120,400);w.update(5,false,camera);assert.equal(w.stats.detail.activeGrassChunks,0);
  const clouds=w.scene.getObjectByName('Layered cloud banks / varied puffs and horizon wisps');w.update(5,true,camera);const still=[...clouds.instanceMatrix.array];w.update(95,true,camera);assert.deepEqual([...clouds.instanceMatrix.array],still);w.update(95,false,camera);assert.notDeepEqual([...clouds.instanceMatrix.array],still);for(let i=0;i<60;i++)w.update(i,false,camera);assert.deepEqual(ids(),before);
 }finally{w.dispose();assert.equal(released.size,tracked.size,'dispose active and dormant detail geometries');}
});
