import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {boardingEnabled} from '../assets/js/floating-atlas/skyport-boarding.js';

test('flight preview requires every local development flag',()=>{
 const q='?dev-town=s2f&town-layout=reset-final&town-props=cc0&town-guild=r0c2&town-skyport=r0c3&town-skyport-polish=r0c3-1&skyport-demo=r0d1';
 assert(boardingEnabled('http://localhost/'+q));
 assert(!boardingEnabled('https://arnanmuflihadi.github.io/'+q));
 for(const key of ['dev-town','town-layout','town-props','town-guild','town-skyport','town-skyport-polish','skyport-demo']){const url=new URL('http://localhost/'+q);url.searchParams.delete(key);assert(!boardingEnabled(url.href));}
});
test('flight asset contains real skinned geometry, embedded texture and authored flight clips',()=>{
 const b=readFileSync(new URL('../assets/game/skyport/boarding/dragon.glb',import.meta.url));
 assert(b.length<500000);const g=JSON.parse(b.subarray(20,20+b.readUInt32LE(12)));
 assert(g.skins?.length);assert(g.images?.every(i=>i.bufferView!==undefined));
 assert(g.animations.some(a=>a.name==='Flying_Idle'));assert(g.animations.some(a=>a.name==='Fast_Flying'));
 assert(g.meshes.some(m=>m.primitives.some(p=>p.attributes.POSITION!==undefined&&p.attributes.JOINTS_0!==undefined)));
});
