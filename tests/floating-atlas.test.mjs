import test from'node:test';import assert from'node:assert/strict';
import * as T from'../assets/js/vendor/three-atlas.module.js?v=16';
import{createTerrainGeometry,createCliffGeometry,terrainInfo,groundHeight,safeGround}from'../assets/js/floating-atlas-legacy-r0/terrain.js';
import{routes,areas,spawn,worldId,isConstructed,travelConfig}from'../assets/js/floating-atlas-legacy-r0/plan.js';
import{createFloatingWorld}from'../assets/js/floating-atlas-legacy-r0/scene.js';
import{createWorldManager}from'../assets/js/floating-atlas-legacy-r0/world-manager.js';
import{blocked,clearDistance,movementOptions}from'../assets/js/floating-atlas-legacy-r0/collision.js';
import{createPlayerController}from'../assets/js/urban-atlas/player-controller.js';
import{createFollowCamera}from'../assets/js/urban-atlas/camera.js';
import{fixtureLibrary,fixtureArtwork}from'./helpers/floating-fixture.mjs';
import{worldHeight}from'../assets/js/floating-atlas-legacy-r0/support.js';

test('the authored island has an irregular closed rock volume and physics matches its rendered top',()=>{
 const top=createTerrainGeometry(),cliff=createCliffGeometry(),mesh=new T.Mesh(top,new T.MeshBasicMaterial()),ray=new T.Raycaster();mesh.updateMatrixWorld();let samples=0,max=0;
 try{for(let x=-61;x<64;x+=2.7)for(let z=-69;z<68;z+=2.9){const y=groundHeight(x,z);if(y<0)continue;ray.set(new T.Vector3(x,80,z),new T.Vector3(0,-1,0));const hit=ray.intersectObject(mesh)[0];assert.ok(hit,'ground at '+x+','+z);max=Math.max(max,Math.abs(hit.point.y-y));samples++;}assert.ok(samples>1500);assert.ok(max<.00001);assert.ok(terrainInfo.dimensions.surfaceMax-terrainInfo.dimensions.surfaceMin>19);assert.ok(terrainInfo.dimensions.width>120);assert.equal(groundHeight(90,90),-500);
  const edgeCounts=new Map(),key=(g,i)=>[0,1,2].map(k=>Math.round(g.attributes.position.array[i*3+k]*1000)).join(',');for(const g of[top,cliff])for(let i=0;i<g.index.count;i+=3)for(const[a,b]of[[0,1],[1,2],[2,0]]){const keys=[key(g,g.index.getX(i+a)),key(g,g.index.getX(i+b))].sort(),k=keys.join('|');edgeCounts.set(k,(edgeCounts.get(k)||0)+1);}assert.ok([...edgeCounts.values()].every(n=>n===2),'watertight terrain and underside seams');
 }finally{top.dispose();cliff.dispose();mesh.material.dispose();}
});

test('the actual imported island uses only three scenery files and disposes its generated scene',async()=>{
 const art=fixtureArtwork(),w=await createFloatingWorld({library:fixtureLibrary(),artwork:art});try{assert.equal(w.stats.files.loadedFiles,3);assert.equal(w.stats.files.requests,3);assert.equal(w.stats.settlement.buildings.length,3);assert.equal(w.stats.settlement.prototypes,2);assert.equal(w.stats.geometry.missingTextures.length,0);assert.ok(w.stats.geometry.triangles>150000);assert.ok(w.stats.fernBatches<10);assert.ok(w.stats.imported.tree>20);for(const b of w.stats.settlement.buildings){assert.ok(b.metrics.triangles>2500);assert.ok(b.colliders.length>=5);assert.ok(b.position[1]>=12);}const solids=[];w.scene.traverse(o=>{if(o.isMesh&&o.name!=='')solids.push(o.name);});assert.ok(solids.includes('Layered tapered island geology'));assert.ok(solids.includes('Pelabuhan Awan / original gateway'));for(const s of w.stats.settlement.signs){const p=new T.Vector3(...s.position),normal=new T.Vector3(Math.sin(s.rotation),0,Math.cos(s.rotation)),ray=new T.Raycaster(p.clone().add(normal),normal.clone().multiplyScalar(-1)),hit=ray.intersectObjects(w.scene.children,true)[0];assert.equal(hit?.object.name,'Physical sign: '+s.text,'lettering stays in front of its backing');}}finally{w.dispose();w.dispose();art.dispose();}assert.equal(w.scene.children.length,0);
});

test('every authored route can be walked with the actual character physics and final imported collisions',async()=>{
 const art=fixtureArtwork(),w=await createFloatingWorld({library:fixtureLibrary(),artwork:art});try{for(const route of routes){const root=new T.Group(),first=route.points[0];root.position.set(first[0],worldHeight(first[0],first[1]),first[1]);const motion=createPlayerController(root,movementOptions),input={keys:new Set(['w']),touch:new Set(),yaw:0};assert.equal(blocked(root.position.x,root.position.z,w.obstacles),false,route.id+' start');for(const point of route.points.slice(1)){let frames=0;while(Math.hypot(root.position.x-point[0],root.position.z-point[1])>.17&&frames++<4000){const dx=point[0]-root.position.x,dz=point[1]-root.position.z;input.yaw=Math.atan2(-dx,-dz);motion.update(1/60,input,w.obstacles);}assert.ok(frames<4000,'reachable '+route.id+' '+point);assert.ok(Math.abs(root.position.y-worldHeight(root.position.x,root.position.z))<.01,'grounded '+route.id);}assert.equal(motion.jumps,0);assert.equal(motion.grounded,true);}
  const ray=new T.Raycaster();for(let x=-57;x<=-45;x+=.5)for(let z=-6.5;z<=3;z+=.5){if(blocked(x,z,w.obstacles))continue;const y=worldHeight(x,z);if(y<0)continue;ray.set(new T.Vector3(x,y+.1,z),new T.Vector3(0,-1,0));const hit=ray.intersectObjects(w.scene.children,true)[0];assert.ok(hit&&Math.abs(hit.point.y-y)<.02,'cantilever deck has matching physical support '+x+','+z);}
 }finally{w.dispose();art.dispose();}
});

test('jumping on elevated terrain and falling from an unguarded edge recover to real safe ground',()=>{
 const root=new T.Group();root.position.set(spawn.x,groundHeight(spawn.x,spawn.z),spawn.z);const motion=createPlayerController(root,movementOptions),input={keys:new Set(),touch:new Set(),yaw:0};let peak=root.position.y;for(let i=0;i<180;i++){motion.update(1/60,input,[],{jump:i===0});peak=Math.max(peak,root.position.y);}assert.equal(motion.jumps,1);assert.equal(motion.landings,1);assert.ok(peak>11);assert.equal(motion.grounded,true);
 const edge=new T.Group();edge.position.set(60,worldHeight(60,10),10);const falling=createPlayerController(edge,movementOptions),outward={keys:new Set(['d','shift']),touch:new Set(),yaw:0};let below=false,recovered=false;for(let i=0;i<600;i++){falling.update(1/60,outward,[]);if(edge.position.y< -20)below=true;if(below&&edge.position.y>0&&falling.grounded){recovered=true;break;}}assert.equal(below,true,'walks beyond an unguarded physical cliff');assert.equal(recovered,true,'gravity fall returns to a safe island position');assert.ok(safeGround(edge.position.x,edge.position.z));
 root.position.set(95,-66,90);motion.update(1/60,input,[]);assert.ok(safeGround(root.position.x,root.position.z));assert.ok(root.position.y>0);root.position.set(NaN,Infinity,NaN);motion.update(1/60,input,[]);assert.ok(root.position.toArray().every(Number.isFinite));assert.ok(safeGround(root.position.x,root.position.z));
});

test('the follow camera clears rising terrain and imported building proxies',async()=>{
 const art=fixtureArtwork(),w=await createFloatingWorld({library:fixtureLibrary(),artwork:art});try{for(const p of[spawn,areas.transit,areas.overlook,{x:-30,z:-9},{x:24,z:18}])for(let yaw=0;yaw<Math.PI*2;yaw+=Math.PI/4){const root=new T.Group();root.position.set(p.x,groundHeight(p.x,p.z),p.z);const follow=createFollowCamera({clearance:clearDistance,distance:9.5});for(let i=0;i<30;i++)follow.update(root,{yaw,pitch:.12},w.obstacles,1/60,false);const c=follow.camera.position;assert.ok(c.toArray().every(Number.isFinite));assert.ok(c.y>groundHeight(c.x,c.z)+.1,'terrain clearance '+p.x+','+p.z+' '+yaw);assert.ok(Math.hypot(c.x-p.x,c.z-p.z)>.2);}}finally{w.dispose();art.dispose();}
});

test('world loading deduplicates requests, rejects unbuilt realms and disposes cancelled generations',async()=>{
 let resolve,disposed=0,loads=0;const m=createWorldManager({load:()=>{loads++;return new Promise(r=>resolve=r);}}),a=m.load(worldId),b=m.load(worldId);assert.equal(loads,1);await assert.rejects(m.load('mbr'),/not constructed/);resolve({dispose(){disposed++;}});assert.equal(await a,await b);m.unload();assert.equal(disposed,1);const pending=m.load();m.unload();resolve({dispose(){disposed++;}});await assert.rejects(pending,/cancelled/);assert.equal(disposed,2);m.dispose();await assert.rejects(m.load(),/disposed/);assert.equal(isConstructed('transit'),true);assert.equal(isConstructed('mbr'),false);assert.equal(travelConfig.implemented,false);assert.ok(travelConfig.routes.every(r=>!r.enabled));
});
