import test from'node:test';
import assert from'node:assert/strict';
import * as T from'../assets/js/vendor/three-atlas.module.js?v=16';
import{createTerrainGeometry,createCliffGeometry,terrainInfo,groundHeight,terrainSample,safeGround}from'../assets/js/floating-atlas/terrain.js?v=73';
import{routes,areas,spawn,reservations,isConstructed}from'../assets/js/floating-atlas/plan.js?v=73';
import{createFloatingWorld}from'../assets/js/floating-atlas/scene.js?v=73';
import{blocked,clearDistance,movementOptions}from'../assets/js/floating-atlas/collision.js?v=73';
import{worldHeight,decks}from'../assets/js/floating-atlas/support.js?v=73';
import{createPlayerController}from'../assets/js/urban-atlas/player-controller.js';
import{createFollowCamera}from'../assets/js/urban-atlas/camera.js';
import{fixtureLibrary}from'./helpers/floating-fixture.mjs';

test('R0-A rendered terrain support is exact and the chiseled underside is watertight',()=>{
 const top=createTerrainGeometry(),cliff=createCliffGeometry(),material=new T.MeshBasicMaterial(),mesh=new T.Mesh(top,material),ray=new T.Raycaster(),edges=new Map();mesh.updateMatrixWorld();let n=0;
 try{
  for(let x=-87;x<88;x+=3.1)for(let z=-92;z<89;z+=3.7){const y=groundHeight(x,z);if(y<0)continue;ray.set(new T.Vector3(x,120,z),new T.Vector3(0,-1,0));const hit=ray.intersectObject(mesh)[0];assert.ok(hit);assert.ok(Math.abs(hit.point.y-y)<.00002);assert.equal(worldHeight(x,z),y);n++;}assert.ok(n>1800);assert.ok(terrainInfo.dimensions.surfaceMax-terrainInfo.dimensions.surfaceMin>36);assert.equal(decks.length,0);
  const key=(g,i)=>[0,1,2].map(k=>Math.round(g.attributes.position.array[i*3+k]*1000)).join(',');for(const g of[top,cliff])for(let i=0;i<g.index.count;i+=3)for(const[a,b]of[[0,1],[1,2],[2,0]]){const k=[key(g,g.index.getX(i+a)),key(g,g.index.getX(i+b))].sort().join('|');edges.set(k,(edges.get(k)||0)+1);}assert.ok([...edges.values()].every(n=>n===2));cliff.computeBoundingBox();assert.ok(cliff.boundingBox.min.y<=-85);
 }finally{top.dispose();cliff.dispose();material.dispose();}
});

test('R0-A active graph has no rejected architecture, uses two scenery GLBs, and disposes every observed resource',async()=>{
 const w=await createFloatingWorld({library:fixtureLibrary()}),disposed={geometry:0,material:0,texture:0},sets={geometry:new Set(),material:new Set(),texture:new Set()};
 try{
  assert.equal(w.stats.architectureInstances,0);assert.equal(w.settlement,null);assert.deepEqual(w.stats.sourceFiles,['canopy-tree.glb','fern.glb']);assert.equal(w.stats.files.loadedFiles,2);assert.equal(w.stats.geometry.missingTextures.length,0);assert.ok(w.stats.imported.tree>70);assert.ok(w.stats.imported.fern>250);assert.ok(w.stats.grassBlades>5000);assert.ok(w.stats.vegetationBatches<30);
  w.scene.traverse(o=>{assert.ok(!/Building_|gateway|Stasiun|Pasar|Pelabuhan|parapet|shopfront/i.test(o.name));if(!o.isMesh)return;assert.notEqual(o.geometry.type,'BoxGeometry');sets.geometry.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:[o.material]){sets.material.add(m);for(const t of Object.values(m))if(t?.isTexture)sets.texture.add(t);}});
  for(const[k,set]of Object.entries(sets))for(const v of set)v.addEventListener('dispose',()=>disposed[k]++);
  assert.ok(Object.values(reservations).every(p=>!p.constructed&&safeGround(p.x,p.z)));assert.equal(isConstructed('transit'),false);assert.equal(isConstructed('mbr'),false);
 }finally{w.dispose();}assert.equal(w.scene.children.length,0);assert.equal(w.library.stats().cachedFiles,0);for(const[k,set]of Object.entries(sets))assert.ok(disposed[k]>=set.size,k+' disposal');
});

test('R0-A every ridge and valley route is reachable using unchanged locomotion with final nature colliders',async()=>{
 const w=await createFloatingWorld({library:fixtureLibrary()});try{for(const route of routes){const first=route.points[0],root=new T.Group();root.position.set(first[0],groundHeight(first[0],first[1]),first[1]);const motion=createPlayerController(root,movementOptions),input={keys:new Set(['w']),touch:new Set(),yaw:0};assert.equal(blocked(root.position.x,root.position.z,w.obstacles),false,route.id+' start');for(const p of route.points.slice(1)){let n=0;while(Math.hypot(root.position.x-p[0],root.position.z-p[1])>.18&&n++<4000){input.yaw=Math.atan2(p[0]-root.position.x, p[1]-root.position.z)+Math.PI;motion.update(1/60,input,w.obstacles);}assert.ok(n<4000,'route '+route.id+' '+p);assert.ok(Math.abs(root.position.y-groundHeight(root.position.x,root.position.z))<.03);}assert.equal(motion.grounded,true);assert.equal(motion.jumps,0);}}finally{w.dispose();}
});

test('R0-A character jumps, lands, falls and recovers; camera clears natural elevation at all areas',async()=>{
 const root=new T.Group();root.position.set(spawn.x,groundHeight(spawn.x,spawn.z),spawn.z);const motion=createPlayerController(root,movementOptions),input={keys:new Set(),touch:new Set(),yaw:0};let peak=root.position.y;for(let i=0;i<180;i++){motion.update(1/60,input,[],{jump:i===0});peak=Math.max(peak,root.position.y);}assert.equal(motion.jumps,1);assert.equal(motion.landings,1);assert.ok(peak>groundHeight(spawn.x,spawn.z)+1);
 root.position.set(98,-101,98);motion.update(1/60,input,[]);assert.ok(safeGround(root.position.x,root.position.z));root.position.set(NaN,Infinity,NaN);motion.update(1/60,input,[]);assert.ok(root.position.toArray().every(Number.isFinite));
 const edge=new T.Group();let ex=88;while(terrainSample(ex,30).height<0)ex-=.5;edge.position.set(ex-.5,groundHeight(ex-.5,30),30);const fall=createPlayerController(edge,movementOptions);let below=false,recovered=false;for(let i=0;i<900;i++){fall.update(1/60,{keys:new Set(['d','shift']),touch:new Set(),yaw:0},[]);if(edge.position.y<-35)below=true;if(below&&edge.position.y>0&&fall.grounded){recovered=true;break;}}assert.ok(below&&recovered);
 const w=await createFloatingWorld({library:fixtureLibrary()});try{for(const p of Object.values(areas))for(let yaw=0;yaw<Math.PI*2;yaw+=Math.PI/4){root.position.set(p.x,groundHeight(p.x,p.z),p.z);const follow=createFollowCamera({clearance:clearDistance,distance:9.5});for(let i=0;i<45;i++)follow.update(root,{yaw,pitch:.12},w.obstacles,1/60,false);assert.ok(follow.camera.position.toArray().every(Number.isFinite));const c=follow.camera.position;assert.ok(c.y>groundHeight(c.x,c.z)+.1);}}finally{w.dispose();}
});
