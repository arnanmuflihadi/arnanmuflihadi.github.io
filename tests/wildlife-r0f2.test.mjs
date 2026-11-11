import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {wildlifeEnabled,wildlifeCatalog,findWanderTarget} from '../assets/js/floating-atlas/wildlife.js';

test('wildlife is opt-in on localhost and each source contains a rig and ambient clips',async()=>{
 const flags='?dev-town=s2f&town-layout=reset-final&wildlife=r0f2';
 assert.equal(wildlifeEnabled('http://localhost/'+flags),true);
 assert.equal(wildlifeEnabled('https://example.com/'+flags),false);
 assert.equal(wildlifeEnabled('http://localhost/?dev-town=s2f&town-layout=reset-final'),false);
 for(const id of ['deer','fox','cow']){
  const data=JSON.parse(await readFile(new URL(wildlifeCatalog['wildlife-'+id].url),'utf8'));
  assert.ok(data.skins?.[0]?.joints?.length>0,id);
  assert.ok(data.animations.some(a=>a.name==='Idle_2'&&a.channels.length>0),id);
  assert.ok(data.animations.some(a=>a.name==='Eating'&&a.channels.length>0),id);
  assert.ok(data.buffers.every(b=>b.uri.startsWith('data:')),id);
 }
});

test('wander destinations require a clear path, not just a clear endpoint',()=>{
 const valid=(x,z)=>!(x>.2&&x<1.9&&Math.abs(z)<.15);
 const result=findWanderTarget(0,0,0,valid);
 assert.ok(result);
 assert.ok(Math.abs(result.z)>.15,'the obstructed straight path is rejected');
 assert.equal(findWanderTarget(0,0,0,()=>false),null);
});
