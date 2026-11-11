import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import * as T from '../assets/js/vendor/three-atlas.module.js?v=16';
import {townDevelopmentEnabled} from '../assets/js/floating-atlas/town-flag.js';
import {townCatalog,integrateTown} from '../assets/js/floating-atlas/town-integration.js';
import {createModelLibrary,assetCatalog} from '../assets/js/urban-atlas/model-library.js?v=15';
import {createFloatingWorld} from '../assets/js/floating-atlas/scene.js';
import {createPlayerController} from '../assets/js/urban-atlas/player-controller.js?v=50';
const sha=b=>createHash('sha256').update(b).digest('hex');
async function load(url){globalThis.ProgressEvent||=class{constructor(type,data){Object.assign(this,data);}};const u=new URL(url);u.search='';const b=readFileSync(u),n=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+n));delete j.images;delete j.textures;delete j.samplers;j.materials=(j.materials||[]).map(m=>({name:m.name}));j.buffers[0].uri='data:application/octet-stream;base64,'+b.subarray(28+n).toString('base64');return new T.GLTFLoader().parseAsync(JSON.stringify(j),'');}
test('town requires exact local development flag and is off on every public/default route',()=>{
 for(const host of ['localhost','127.0.0.1','[::1]'])assert.equal(townDevelopmentEnabled('http://'+host+':4173/index.html?dev-town=s2f'),true);
 for(const u of ['https://arnanmuflihadi.github.io/?dev-town=s2f','http://127.0.0.1:4173/','http://127.0.0.1:4173/?dev-town=1','https://localhost.example.com/?dev-town=s2f'])assert.equal(townDevelopmentEnabled(u),false);
});
test('approved assets are byte-identical to pre-integration checkpoint',()=>{
 const files=JSON.parse(readFileSync('validation/town-s2f/before-hashes.json'));let checked=0;for(const [p,h]of Object.entries(files))if(/\.(blend[0-9]*|glb|zip)$/.test(p)){assert.equal(sha(readFileSync(p)),h,p);checked++;}assert.ok(checked>25);
});
test('approved S2-F baseline with S2-G polish disabled preserves terrain and vegetation; off restores cached instances',async()=>{
 const library=createModelLibrary({catalog:{...assetCatalog,...townCatalog},load}),w=await createFloatingWorld({library}),original=w.obstacles,positions=w.terrain.geometry.attributes.position.array.slice(),scene=w.scene.uuid,instances=[];
 w.scene.traverse(o=>{if(o.isInstancedMesh)instances.push({o,count:o.count,matrix:o.instanceMatrix.array.slice()});});
 const town=await integrateTown(w);town.setPolished(false);try{
  assert.equal(w.scene.uuid,scene);assert.equal(town.group.parent,w.scene);assert.equal(town.metrics.market.triangles,170709);assert.equal(town.metrics.interfaces.triangles,8404);assert.equal(town.metrics.foundations.triangles,7248);assert.equal(town.metrics.support.triangles,100);assert.equal(town.models.support.parent,null);
  for(const v of instances){assert.equal(v.o.count,v.count);assert.deepEqual(v.o.instanceMatrix.array,v.matrix);}
  assert.deepEqual(w.terrain.geometry.attributes.position.array,positions);
  for(const hz of [20,30,60])for(const name of ['main','return','ramp','ramp return']){
   const main=[[24,66],[27,61.8],[27,60],[30,52],[36,44],[36,35],[36,27],[36,17],[36,9],[36,0]],ramp=[[36,10],[33,9],[32.3,7.9],[30.5,5.5],[31,1.2],[36,0]];let route=name.includes('ramp')?ramp:main;if(name.includes('return'))route=[...route].reverse();const r=new T.Group();r.position.set(route[0][0],town.heightAt(...route[0]),route[0][1]);const c=createPlayerController(r,town.movementOptions(()=>r.position.y)),i={keys:new Set(['w']),touch:new Set(),yaw:0,pitch:0};let target=1,frames=0,air=0;
   while(target<route.length&&frames<hz*75){const t=route[target],dx=t[0]-r.position.x,dz=t[1]-r.position.z;if(Math.hypot(dx,dz)<.13){target++;continue;}i.yaw=Math.atan2(-dx,-dz);const old=r.position.y,m=c.update(1/hz,i,w.obstacles);assert.ok(Math.abs(r.position.y-old)<.42,name+' support seam');if(!m.grounded)air++;frames++;}assert.equal(target,route.length,name+' @'+hz);assert.equal(air,0,name+' unexpected fall');
  }
  const cached=library.stats().requests;town.setEnabled(false);assert.equal(w.obstacles,original);assert.equal(town.group.parent,null);town.setEnabled(true);assert.equal(library.stats().requests,cached);assert.equal(w.scene.uuid,scene);town.setEnabled(false);
  for(const v of instances)assert.deepEqual(v.o.instanceMatrix.array,v.matrix);
 }finally{town.dispose();w.dispose();}
});
