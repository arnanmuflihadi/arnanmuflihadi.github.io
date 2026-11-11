import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const bytes=readFileSync(new URL('./dragon-batched.glb',import.meta.url)),jsonLength=bytes.readUInt32LE(12),g=JSON.parse(bytes.subarray(20,20+jsonLength)),binaryOffset=20+jsonLength+8;
assert.equal(bytes.toString('ascii',0,4),'glTF');assert.equal(g.skins.length,1);assert(g.skins[0].joints.length>=10);
let triangles=0;for(const mesh of g.meshes)for(const p of mesh.primitives){assert.notEqual(p.attributes.JOINTS_0,undefined);assert.notEqual(p.attributes.WEIGHTS_0,undefined);triangles+=g.accessors[p.indices].count/3;}
assert(triangles>5000&&triangles<40000);
const clip=g.animations.find(x=>x.name==='Wing_Powered_Flight');assert(clip);const channel=clip.channels.find(c=>g.nodes[c.target.node].name==='wing_L'&&c.target.path==='rotation');assert(channel);
const accessor=g.accessors[clip.samplers[channel.sampler].output],view=g.bufferViews[accessor.bufferView],start=binaryOffset+(view.byteOffset||0)+(accessor.byteOffset||0),samples=[];
for(let i=0;i<accessor.count;i++)samples.push(Array.from({length:4},(_,k)=>bytes.readFloatLE(start+i*16+k*4)));
const range=Math.max(...samples.map(q=>q[0]))-Math.min(...samples.map(q=>q[0]));assert(range>.01,'Wing rotation must change across the flight clip');
console.log(JSON.stringify({bytes:bytes.length,triangles,skins:g.skins.length,joints:g.skins[0].joints.length,primitives:g.meshes.reduce((n,m)=>n+m.primitives.length,0),materials:g.materials.length,clips:g.animations.map(a=>a.name),wingRotationSampleRange:range},null,2));
