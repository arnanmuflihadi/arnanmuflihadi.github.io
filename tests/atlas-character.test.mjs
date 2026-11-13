import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import * as T from '../assets/js/vendor/three-atlas.module.js';
import {createCharacter,characterUrl} from '../assets/js/urban-atlas/character.js';
import {groundHeight} from '../assets/js/urban-atlas/layout.js';
const bytes=readFileSync('assets/game/characters/urban-explorer/urban-explorer.glb');
const manifest=JSON.parse(readFileSync('assets/game/characters/urban-explorer/source.json','utf8'));
async function fixture(){const gltf=await new T.GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');return createCharacter(new T.Scene(),null,{x:0,z:28},{gltf});}
function cleanup(actor){actor.dispose();actor.model.traverse(o=>{o.geometry?.dispose();o.material?.dispose();});}
test('real self-contained GLB matches documented Quaternius asset and CC0 provenance',()=>{
 assert.equal(bytes.toString('ascii',0,4),'glTF');const size=bytes.readUInt32LE(12),json=JSON.parse(bytes.subarray(20,20+size).toString('utf8'));
 assert.equal(manifest.outputSha256,createHash('sha256').update(bytes).digest('hex'));assert.equal(manifest.author,'Quaternius');assert.equal(manifest.license,'CC0-1.0');
 assert.equal(json.skins[0].joints.length,62);assert.deepEqual(json.animations.map(a=>a.name).sort(),['Idle','Run','Walk']);
 assert.ok(json.buffers.every(b=>!b.uri));assert.equal((json.images||[]).length,0);assert.ok(bytes.length<2*1024*1024);
 assert.ok(characterUrl.pathname.endsWith('/assets/game/characters/urban-explorer/urban-explorer.glb'));
});
test('imported skinned geometry has normalized weights, valid bind poses and human scale',async()=>{
 const actor=await fixture();assert.equal(actor.meshCount,15);assert.equal(actor.triangles,10202);
 const bounds=new T.Box3().setFromObject(actor.root);assert.ok(bounds.max.y-bounds.min.y>1.85&&bounds.max.y-bounds.min.y<1.95);
 actor.model.traverse(o=>{if(!o.isMesh)return;assert.ok(o.isSkinnedMesh);assert.equal(o.skeleton.bones.length,62);assert.equal(o.skeleton.boneInverses.length,62);assert.ok(o.material.isMeshStandardMaterial);
 const w=o.geometry.getAttribute('skinWeight');for(let i=0;i<w.count;i++)assert.ok(Math.abs(w.getX(i)+w.getY(i)+w.getZ(i)+w.getW(i)-1)<.0001);});
 assert.ok(!readFileSync('assets/js/urban-atlas/character.js','utf8').includes('SphereGeometry'));cleanup(actor);
});
test('idle, walk and run crossfade continuously and use displacement-based playback speed',async()=>{
 const actor=await fixture(),a=actor.animator;
 a.update(1/60,2.1);assert.ok(a.weights.Idle>0&&a.weights.Walk>0);
 for(let i=0;i<120;i++)a.update(1/60,2.1);assert.equal(a.state,'Walk');assert.ok(a.weights.Walk>.99);
 const before=a.actions.Walk.time;a.update(1/60,2.1);assert.ok(Math.abs(a.actions.Walk.time-before)<.1);
 for(let i=0;i<120;i++)a.update(1/60,4.6);assert.equal(a.state,'Run');assert.ok(a.weights.Run>.99);
 assert.ok(Math.abs(a.actions.Run.getEffectiveTimeScale()-4.6/(2.695*actor.scale))<.00001);
 for(let i=0;i<120;i++)a.update(1/60,0);assert.equal(a.state,'Idle');assert.ok(a.weights.Idle>.99);
 assert.equal(a.actions.Walk.getEffectiveTimeScale(),0);assert.equal(a.actions.Run.getEffectiveTimeScale(),0);
 assert.ok(Math.abs(a.weights.Idle+a.weights.Walk+a.weights.Run-1)<.00001);cleanup(actor);
});
test('stationary feet stay planted and animation never moves the physics/camera root',async()=>{
 const actor=await fixture(),input={keys:new Set(),touch:new Set(),yaw:0};actor.root.updateMatrixWorld(true);
 const left=actor.model.getObjectByName('FootL'),right=actor.model.getObjectByName('FootR');const initial=[left.getWorldPosition(new T.Vector3()),right.getWorldPosition(new T.Vector3())];
 for(let i=0;i<120;i++){actor.update(1/60,input,[],false);actor.root.updateMatrixWorld(true);assert.ok(left.getWorldPosition(new T.Vector3()).distanceTo(initial[0])<1e-5);assert.ok(right.getWorldPosition(new T.Vector3()).distanceTo(initial[1])<1e-5);assert.equal(actor.root.position.y,groundHeight(0,28));}
 assert.equal(actor.root.position.x,0);assert.equal(actor.root.position.z,28);cleanup(actor);
});
test('holding movement against a wall resolves to idle instead of sliding a walk pose',async()=>{
 const actor=await fixture(),input={keys:new Set(['w']),touch:new Set(),yaw:0},wall=[{x:0,z:26,w:10,d:1,h:10}];
 for(let i=0;i<300;i++)actor.update(1/60,input,wall,false);
 assert.ok(actor.root.position.z>=26.84-.001);assert.equal(actor.animator.state,'Idle');assert.ok(actor.animator.weights.Idle>.99);
 assert.ok(Math.abs(actor.visual.scale.x-actor.scale)<1e-6);cleanup(actor);
});
