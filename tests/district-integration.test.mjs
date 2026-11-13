import test from'node:test';import assert from'node:assert/strict';import{readFileSync}from'node:fs';import{fileURLToPath}from'node:url';
import * as T from'../assets/js/vendor/three-atlas.module.js?v=16';
import{createModelLibrary}from'../assets/js/urban-atlas/model-library.js';
import{createDistrict}from'../assets/js/urban-atlas/scene.js';
import{districtBuildings,buildingObstacles,buildingTransform}from'../assets/js/urban-atlas/district-plan.js';
import{groundHeight,inRoad,layout,curbRamps,inRect}from'../assets/js/urban-atlas/layout.js';
import{blocked,slide}from'../assets/js/urban-atlas/collision.js';
import{createPlayerController}from'../assets/js/urban-atlas/player-controller.js';
import{landmarks,presentations}from'../assets/js/urban-atlas/presentation.js';
import{createFollowCamera}from'../assets/js/urban-atlas/camera.js';
import{createDistrictArtwork}from'../assets/js/urban-atlas/district-artwork.js';
function district(){const previous=globalThis.document;try{globalThis.document={createElement:()=>({getContext:()=>({fillRect(){},fillText(){}})})};return createDistrict();}finally{globalThis.document=previous;}}
function fixture(){globalThis.ProgressEvent||=class{constructor(type,data){Object.assign(this,data);}};return createModelLibrary({load:async url=>{const path=new URL(url);path.search='';const b=readFileSync(fileURLToPath(path)),n=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+n));delete j.images;delete j.textures;delete j.samplers;j.materials=j.materials.map(m=>({name:m.name}));j.buffers[0].uri='data:application/octet-stream;base64,'+b.subarray(28+n).toString('base64');return new T.GLTFLoader().parseAsync(JSON.stringify(j),'');}});}
function artwork(){const maps=[],map=()=>{const t=new T.DataTexture(new Uint8Array([255,255,255,255]),1,1);maps.push(t);return t;};return{sign:map,display:map,dispose(){maps.forEach(m=>m.dispose());}};}
function pedestrian(x,z){const crosswalk=(Math.abs(x)<=2.8&&[-12,-36].some(c=>Math.abs(z-c)<=3.01))||(Math.abs(z-28)<=1.5&&x>=-16.25&&x<=-11.75);return groundHeight(x,z)>=.23||curbRamps.some(r=>inRect(x,z,r))||(inRoad(x,z)&&crosswalk);}
function reachable(obstacles){const start=[0,28],todo=[start],seen=new Set(['0,28']);for(let h=0;h<todo.length;h++){const[x,z]=todo[h];for(const[dx,dz]of[[.5,0],[-.5,0],[0,.5],[0,-.5]]){const a=x+dx,b=z+dz,key=a+','+b;if(seen.has(key)||Math.abs(a)>43||Math.abs(b)>43||!pedestrian(a,b)||blocked(a,b,obstacles)||Math.abs(groundHeight(a,b)-groundHeight(x,z))>.42)continue;seen.add(key);todo.push([a,b]);}}return seen;}

test('the real imported district uses approved prototypes, matching transforms/proxies and four cached GLBs',async()=>{
  const d=district(),assets=await d.loadAssets({library:fixture(),artwork:artwork()});try{
    assert.equal(assets.stats.loadedFiles,4);assert.equal(assets.stats.requests,4);assert.equal(assets.stats.prototypes,3);assert.equal(assets.stats.buildings.filter(b=>!b.skyline).length,8);assert.equal(assets.stats.missingTextures.length,0);assert.ok(assets.stats.triangles>400000);
    for(const p of districtBuildings){const b=assets.stats.buildings.find(b=>b.id===p.id);assert.deepEqual(b.transform,buildingTransform(p));const actual=d.obstacles.filter(o=>o.building===p.id),expected=buildingObstacles(p);assert.equal(actual.length,expected.length);for(let i=0;i<actual.length;i++)for(const k of['x','z','w','d','minY','h'])assert.ok(Math.abs(actual[i][k]-expected[i][k])<.00001,p.id+' '+k);assert.ok(b.metrics.triangles>2500);}
    assert.ok(assets.stats.importedInstances.entrance>=10);assert.ok(assets.stats.importedInstances.drain>=8);assert.ok(assets.stats.importedInstances.tree>=17);
    assert.equal(assets.stats.propColliders.length,6);for(const c of assets.stats.propColliders){assert.ok(c.w>0&&c.d>0);assert.equal(inRoad(c.x,c.z),false);if(c.importedProp==='planter')assert.ok(Math.abs(c.w-2.5)<.00001);assert.ok(d.obstacles.some(o=>Math.abs(o.x-c.x)<.00001&&Math.abs(o.z-c.z)<.00001&&Math.abs(o.w-c.w)<.00001));}
  }finally{d.dispose();}
});

test('a continuous pedestrian network connects every landmark, park and retail entrance with real asset collisions',async()=>{
  const d=district();await d.loadAssets({library:fixture(),artwork:artwork()});try{const seen=reachable(d.obstacles),goals=[...landmarks.map(l=>presentations[l.projectId].focus),{x:-28,z:13},{x:13,z:33},{x:0,z:-31.5}];
    for(const p of districtBuildings){if(p.variant==='office')goals.push({x:p.x,z:p.z+1.5});else if(p.variant==='commercial')for(const dx of[-1.3,1.3])goals.push({x:p.x+dx,z:p.z+1.5});else goals.push({x:p.x+1.2,z:p.z-1.27});}
    for(const p of goals){assert.equal(blocked(p.x,p.z,d.obstacles),false,'clear destination '+JSON.stringify(p));const x=Math.round(p.x*2)/2,z=Math.round(p.z*2)/2;assert.ok(seen.has(x+','+z),'pedestrian route to '+JSON.stringify(p));const q={x,z};slide(q,p.x-x,p.z-z,d.obstacles);assert.ok(Math.hypot(q.x-p.x,q.z-p.z)<.001);}
  }finally{d.dispose();}
});

test('thousands of unobstructed district ground samples agree with rendered geometry',()=>{
  const d=district(),ray=new T.Raycaster();let checked=0;try{for(let x=-34.87;x<35;x+=1)for(let z=-40.87;z<42;z+=1){if(blocked(x,z,d.obstacles))continue;const support=groundHeight(x,z);ray.set(new T.Vector3(x,support+.18,z),new T.Vector3(0,-1,0));const hit=ray.intersectObjects(d.scene.children,true).find(h=>h.point.y<=support+.06);assert.ok(hit,'support geometry '+x+','+z);assert.ok(Math.abs(hit.point.y-support)<.035,'render/support '+x+','+z);checked++;}assert.ok(checked>4000);}finally{d.dispose();}
});

test('the actual crosswalk ramps allow grounded movement in both street directions',()=>{
  const d=district();try{for(const[start,keys,axis,goal]of[[[0,-7.2],['w'],'z',-20],[[-10.1,28],['a'],'x',-18.5]]){const root=new T.Group();root.position.set(start[0],groundHeight(...start),start[1]);const motion=createPlayerController(root),input={keys:new Set(keys),touch:new Set(),yaw:0};let largest=0,last=root.position.y;for(let i=0;i<400&&root.position[axis]>goal;i++){motion.update(.02,input,d.obstacles);largest=Math.max(largest,Math.abs(root.position.y-last));last=root.position.y;}assert.ok(root.position[axis]<=goal);assert.ok(largest<.03,'smooth curb transition '+largest);assert.equal(motion.jumps,0);assert.equal(motion.grounded,true);}}finally{d.dispose();}
});

test('a failed imported asset rejects the district assembly without a silent primitive substitute and can retry',async()=>{
  const d=district(),broken=createModelLibrary({load:async()=>{throw Error('asset fixture missing');}});try{await assert.rejects(d.loadAssets({library:broken,artwork:artwork()}),/asset fixture missing/);assert.equal(d.scene.getObjectByName('Phase 2 verified district assets'),undefined);const recovered=await d.loadAssets({library:fixture(),artwork:artwork()});assert.equal(recovered.stats.loadedFiles,4);}finally{d.dispose();}
});

test('the follow camera stays outside actual rotated building proxies on all public approaches',()=>{
  const d=district();try{for(const point of[{x:23,z:12},{x:-24,z:-17.9},{x:-18.8,z:26.73},{x:-23,z:6}])for(let yaw=0;yaw<Math.PI*2;yaw+=Math.PI/4){const root=new T.Group();root.position.set(point.x,groundHeight(point.x,point.z),point.z);const follow=createFollowCamera();for(let i=0;i<30;i++)follow.update(root,{yaw,pitch:.19},d.obstacles,1/60,false);assert.ok(follow.camera.position.toArray().every(Number.isFinite));const origin={x:point.x,y:root.position.y+1.25,z:point.z},distance=Math.hypot(follow.camera.position.x-origin.x,follow.camera.position.y-origin.y,follow.camera.position.z-origin.z);for(const o of d.obstacles){if(follow.camera.position.y<(o.minY||0)||follow.camera.position.y>o.h)continue;assert.ok(!(Math.abs(follow.camera.position.x-o.x)<o.w/2-.02&&Math.abs(follow.camera.position.z-o.z)<o.d/2-.02),'camera inside '+o.building);}assert.ok(distance>.4);}}finally{d.dispose();}
});

test('physical district signs retain sharp mipmapped textures at their authored world aspect',()=>{
  const previous=globalThis.document;let art;try{globalThis.document={createElement:()=>({getContext:()=>({fillRect(){},fillText(){},measureText:t=>({width:t.length*80})})})};art=createDistrictArtwork({anisotropy:8});const map=art.sign('RUANG BACA','BUKU · KERTAS',9.24,.5);assert.equal(map.image.width,2048);assert.ok(map.image.height>=100);assert.equal(map.generateMipmaps,true);assert.equal(map.minFilter,1008);assert.equal(map.anisotropy,8);assert.equal(map.colorSpace,T.SRGBColorSpace);}finally{art?.dispose();globalThis.document=previous;}
});
