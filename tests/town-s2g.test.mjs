import test from'node:test';
import assert from'node:assert/strict';
import{fixture}from'../validation/town-s2g/fixture.mjs';
import * as T from'../assets/js/vendor/three-atlas.module.js?v=16';
import{createPlayerController}from'../assets/js/urban-atlas/player-controller.js?v=50';

test('stabilization is individual, reversible, LOD-safe, and leaves source terrain and buffers intact',async()=>{
 const f=await fixture(),{world,town,original}=f,s=town.stabilization;try{
  town.setEnabled(false);const far=new T.PerspectiveCamera();far.position.set(140,110,190);world.update(1,false,far);const obstacles=world.obstacles,rows=original.map(o=>({o,matrix:o.isInstancedMesh?o.instanceMatrix.array.slice():null,count:o.count,position:o.position.clone(),geometry:o.geometry,index:o.geometry.index?.array.slice(),vertices:o.geometry.attributes.position.array.slice()}));
  assert.equal(s.variant,'A');assert.equal(s.summary().unresolved.length,0);assert.equal(s.summary().grassBlades,91);assert.equal(s.summary().relocatedInstances,25);assert.equal(s.summary().palmTrunks,1);
  town.setEnabled(true);assert.notEqual(world.obstacles,obstacles);const changed=[];
  for(const r of rows){assert.deepEqual(r.o.geometry.attributes.position.array,r.vertices);if(r.matrix){assert.equal(r.o.count,r.count);for(let i=0;i<r.count;i++){const old=r.matrix.subarray(i*16,i*16+16),now=r.o.instanceMatrix.array.subarray(i*16,i*16+16);if(old.some((x,j)=>x!==now[j]))changed.push({o:r.o,i});}}}
  assert.equal(changed.length,25);const ledger=s.records.filter(r=>r.kind!=='grass blade'&&r.kind!=='palm trunk');assert.equal(ledger.length,25);
  world.update(1,false,far);let trimmed=0;for(const r of rows)if(r.o.name==='Zone grass / curved blades'&&r.o.geometry!==r.o.userData.detailLevels.near&&r.o.geometry!==r.o.userData.detailLevels.far){trimmed++;assert.ok(r.o.geometry.index.count<=r.o.userData.detailLevels.far.index.count);}assert.ok(trimmed>0);for(const r of rows)if(r.o.name==='Zone grass / curved blades')assert.equal(r.o.geometry.attributes.position,r.o.userData.detailLevels.near.attributes.position);
  for(const g of rows.filter(r=>r.o.name==='Zone grass / curved blades'))assert.deepEqual(g.geometry.index.array,g.index);
  const palm=rows.find(r=>!r.matrix&&r.o.geometry.attributes.position.count===91&&Math.abs(r.o.position.x-5)<.01);assert.ok(palm);const palmShift=palm.o.position.y-palm.position.y,frond=changed.find(c=>!c.o.name&&c.o.geometry.attributes.position.count===26);const old=rows.find(r=>r.o===frond.o);assert.ok(Math.abs(frond.o.instanceMatrix.array[frond.i*16+13]-old.matrix[frond.i*16+13]-palmShift)<.00001);
  town.setEnabled(false);assert.equal(world.obstacles,obstacles);world.update(1,false,far);for(const r of rows){if(r.matrix)assert.deepEqual(r.o.instanceMatrix.array,r.matrix);assert.deepEqual(r.o.position,r.position);assert.ok(r.o.geometry===r.geometry||r.o.userData.detailLevels?.far===r.o.geometry);assert.deepEqual(r.geometry.attributes.position.array,r.vertices);}
  town.setEnabled(true);town.setPolished(false);assert.equal(world.obstacles.filter(o=>o.tree).every(o=>obstacles.includes(o)),true);town.setPolished(true);
 }finally{f.dispose();}
});
test('glass A remains exact by default; B has zero transmission; C retains only the selected cafe-front subset',async()=>{
 const f=await fixture(),s=f.town.stabilization;try{assert.equal(s.variant,'A');assert.equal(s.glassOptions.length,1);const g=s.glassOptions[0],mat=g.source.material,geom=g.source.geometry;assert.equal(g.source.visible,true);assert.ok(mat.transmission>.95);assert.deepEqual(g.triangles,{authored:556,retainedTransmission:132,alpha:424});assert.equal(g.front.geometry.attributes.position,g.source.geometry.attributes.position);s.setGlass('B');assert.equal(g.source.visible,false);assert.equal(g.cheap.visible,true);assert.equal(g.cheap.material.type,'MeshStandardMaterial');assert.equal(g.cheap.material.side,0);assert.ok(!g.cheap.material.transmission);s.setGlass('C');assert.equal(g.front.visible,true);assert.equal(g.rest.visible,true);assert.equal(g.front.material,mat);assert.equal(g.front.geometry.index.count+g.rest.geometry.index.count,geom.index.count);s.setGlass('A');assert.equal(g.source.material,mat);assert.equal(g.source.geometry,geom);f.town.setEnabled(false);assert.equal(g.source.visible,true);assert.equal(g.cheap.visible,false);}finally{f.dispose();}
});
test('real production controller retains both directions, garden alternative, and guarded edge with clearance enabled',async()=>{
 const f=await fixture(),{town,world}=f;try{const main=[[24,66],[27,61.8],[27,60],[30,52],[36,44],[36,35],[36,27],[36,17],[36,9],[36,0]],ramp=[[36,10],[33,9],[32.3,7.9],[30.5,5.5],[31,1.2],[36,0]];
 for(const hz of[20,30,60])for(const base of[main,ramp])for(const reverse of[false,true]){const route=reverse?[...base].reverse():base,r=new T.Group();r.position.set(route[0][0],town.heightAt(...route[0]),route[0][1]);const c=createPlayerController(r,town.movementOptions(()=>r.position.y)),input={keys:new Set(['w']),touch:new Set(),yaw:0,pitch:0};let target=1,frames=0;while(target<route.length&&frames<hz*75){const t=route[target],dx=t[0]-r.position.x,dz=t[1]-r.position.z;if(Math.hypot(dx,dz)<.13){target++;continue;}input.yaw=Math.atan2(-dx,-dz);const old=r.position.y,m=c.update(1/hz,input,world.obstacles);assert.ok(Math.abs(old-r.position.y)<.42);assert.equal(m.grounded,true);frames++;}assert.equal(target,route.length,'route @'+hz);}
 }finally{f.dispose();}
});
