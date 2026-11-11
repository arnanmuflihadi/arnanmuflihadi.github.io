import test from'node:test';
import assert from'node:assert/strict';
import{readFileSync}from'node:fs';
import * as T from'../assets/js/vendor/three-atlas.module.js?v=16';
import{fallingWaterGeometry}from'../assets/js/floating-atlas/waterfall.js?v=73';
import{groundHeight}from'../assets/js/floating-atlas/terrain.js?v=73';
import{streamPoints,reviewViews}from'../assets/js/floating-atlas/plan.js?v=73';
import{createFloatingWorld}from'../assets/js/floating-atlas/scene.js?v=73';
import{fixtureLibrary}from'./helpers/floating-fixture.mjs';

test('waterfall is a closed volume joined to the stream, with depth and a lower cloud termination',()=>{
 const g=fallingWaterGeometry();try{
  const edges=new Map(),p=g.attributes.position,end=streamPoints.at(-1);for(let i=0;i<g.index.count;i+=3)for(const[a,b]of[[0,1],[1,2],[2,0]]){const key=[g.index.getX(i+a),g.index.getX(i+b)].sort((a,b)=>a-b).join(':');edges.set(key,(edges.get(key)||0)+1);}assert.ok([...edges.values()].every(n=>n===2));
  assert.deepEqual(g.userData.source,[end[0],groundHeight(end[0],end[1])+.12,end[1]]);assert.ok(g.userData.termination[1]<-60);let width=0,depth=0;const origin=new T.Vector3(...g.userData.source),flow=new T.Vector3(-.8,0,.6),side=new T.Vector3(.6,0,.8);for(let i=0;i<12;i++){const v=new T.Vector3().fromBufferAttribute(p,i).sub(origin);width=Math.max(width,Math.abs(v.dot(side)));depth=Math.max(depth,Math.abs(v.dot(flow)));}assert.ok(width>1.7&&depth>.25);assert.ok(p.array.every(Number.isFinite));
 }finally{g.dispose();}
});

test('fall stays visible outside the cliff, trail accents clear paths, and new water motion is reducible',async()=>{
 const w=await createFloatingWorld({library:fixtureLibrary()}),camera={position:new T.Vector3(...reviewViews.waterfall.position),quaternion:new T.Object3D().quaternion},g=w.waterfall.fall.geometry,cliff=w.scene.getObjectByName('Chiseled geological strata / closed underside'),ray=new T.Raycaster();
 try{
  const channel=w.waterfall.river.geometry.attributes.position;for(let i=0;i<channel.count;i++)assert.ok(channel.getY(i)>0,'stream edge must not sample the off-island void');
  for(let row=1;row<=g.userData.rows;row++){const target=new T.Vector3();for(let i=0;i<g.userData.cols;i++)target.add(new T.Vector3().fromBufferAttribute(g.attributes.position,row*g.userData.cols+i));target.multiplyScalar(1/g.userData.cols);const d=target.clone().sub(camera.position),length=d.length();ray.set(camera.position,d.normalize());const hit=ray.intersectObject(cliff)[0];assert.ok(!hit||hit.distance>=length-.4,'fall hidden by cliff at row '+row);}
  assert.ok(w.stats.trailDetails.clusters>=12);for(const p of w.stats.trailDetails.points)assert.ok(p.pathClearance>1.25);assert.equal(Object.keys(w.stats.growthForms).length,5);assert.ok(w.stats.vegetationBatches<30);
  w.update(3,false,camera);assert.equal(w.waterfall.time.value,3);w.update(10,true,camera);const mist=w.scene.getObjectByName('Waterfall spray / dissolving into cloudscape'),still=[...mist.instanceMatrix.array];w.update(30,true,camera);assert.equal(w.waterfall.time.value,0);assert.deepEqual([...mist.instanceMatrix.array],still);
  assert.equal(readFileSync(new URL('../assets/js/floating-atlas/atmosphere.js',import.meta.url),'utf8'),readFileSync(new URL('../assets/js/floating-atlas-legacy-r0a2/atmosphere.js',import.meta.url),'utf8'),'approved sky/cloud source unchanged');
 }finally{w.dispose();}
});
