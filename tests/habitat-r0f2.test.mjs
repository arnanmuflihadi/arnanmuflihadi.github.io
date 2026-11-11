import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import {habitatCatalog,habitatEnabled} from '../assets/js/floating-atlas/habitat.js';

test('habitat is an independent local opt-in and selected models have their source files',async()=>{
 const flags='?dev-town=s2f&town-layout=reset-final&wildlife=r0f2&nature=r0f2';
 assert.equal(habitatEnabled('http://127.0.0.1/'+flags),true);
 assert.equal(habitatEnabled('https://example.com/'+flags),false);
 assert.equal(habitatEnabled('http://localhost/?dev-town=s2f&town-layout=reset-final&wildlife=r0f2'),false);
 for(const asset of Object.values(habitatCatalog)){
  const path=new URL(asset.url),model=JSON.parse(await readFile(path,'utf8'));
  assert.ok(model.meshes?.length);
  for(const dep of [...model.buffers,...model.images])await access(new URL(dep.uri,path));
 }
});
