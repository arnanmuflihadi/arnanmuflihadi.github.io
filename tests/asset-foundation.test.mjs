import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {GLTFLoader,Box3,Vector3,Group,Mesh,BoxGeometry,MeshStandardMaterial} from '../assets/js/vendor/three-atlas.module.js?v=16';
import {createModelLibrary,modelMetrics} from '../assets/js/urban-atlas/model-library.js';
import {showcasePlan} from '../assets/js/urban-atlas/showcase-plan.js';
import {fileURLToPath} from 'node:url';
import {blocked,slide} from '../assets/js/urban-atlas/collision.js';

function glb(path){const b=readFileSync(path);assert.equal(b.readUInt32LE(0),0x46546c67);assert.equal(b.readUInt32LE(4),2);return {bytes:b,json:JSON.parse(b.subarray(20,20+b.readUInt32LE(12)).toString()),binary:b.subarray(28+b.readUInt32LE(12))};}
async function geometryAsset(path='assets/game/scenery/architecture-library.glb'){
  globalThis.ProgressEvent ||=class ProgressEvent{constructor(type,init){this.type=type;Object.assign(this,init);}};
  const {json,binary}=glb(path);
  // Texture decoding is checked in the browser; Node inspects the original mesh buffers without an image API.
  delete json.textures;delete json.images;delete json.samplers;json.materials=json.materials.map(m=>({name:m.name,pbrMetallicRoughness:{baseColorFactor:[1,1,1,1]}}));
  json.buffers[0].uri='data:application/octet-stream;base64,'+binary.toString('base64');
  return new GLTFLoader().parseAsync(JSON.stringify(json),'');
}
test('all foundation delivery files match provenance and embed real geometry and textures',()=>{
  const scenery=JSON.parse(readFileSync('assets/game/scenery/source.json','utf8'));
  const architectural=JSON.parse(readFileSync('assets/game/scenery/architecture-source.json','utf8'));
  for(const record of [...scenery.models.filter(m=>m.id!=='city-building').map(m=>({...m,output:`assets/game/scenery/${m.id}.glb`})),architectural]){
    const {bytes,json}=glb(record.output);assert.equal(bytes.length,record.bytes);assert.equal(createHash('sha256').update(bytes).digest('hex'),record.outputSha256);
    assert.ok(json.meshes.length);assert.ok(json.meshes.every(m=>m.primitives.every(p=>p.attributes.POSITION!==undefined&&p.attributes.NORMAL!==undefined)));
    assert.ok(json.images.length);assert.ok(json.images.every(i=>i.bufferView!==undefined&&!i.uri));assert.ok(json.buffers.every(b=>!b.uri));assert.equal(record.license,'CC0-1.0');
  }
  assert.ok(architectural.bytes<6_000_000);assert.equal(architectural.models.length,11);assert.ok(architectural.models.find(m=>m.id==='office').triangles>40_000);
  for(const path of['assets/game/scenery/downtown-city-megakit-LICENSE.txt','assets/game/scenery/stylized-nature-megakit-LICENSE.txt','assets/game/characters/urban-explorer/CC0-Quaternius.txt'])assert.match(readFileSync(path,'utf8'),/CC0 1.0 Universal/);
});
test('real building and shop preserve proportions, share mesh buffers, and align their collision bounds after rotation',async()=>{
  const asset=await geometryAsset();let loads=0;const library=createModelLibrary({load:async()=>{loads++;return asset;}});
  for(const model of['office','shop'])for(const rotation of[0,Math.PI/2,Math.PI]){
    const root=await library.instantiate('architecture',{model,height:model==='office'?17:10.8,x:6,y:.16,z:-4,rotation}),box=new Box3().setFromObject(root),size=box.getSize(new Vector3());
    assert.ok(Math.abs(box.min.y-.16)<.0001);assert.ok(Math.abs(size.y-(model==='office'?17:10.8))<.0001);
    assert.ok(Math.abs((box.min.x+box.max.x)/2-6)<.0001);assert.ok(Math.abs((box.min.z+box.max.z)/2+4)<.0001);
    const c=root.userData.collider;assert.ok(Math.abs(c.w-size.x)<.0001&&Math.abs(c.d-size.z)<.0001);assert.equal(c.minY,box.min.y);assert.equal(c.h,box.max.y);
    assert.ok(modelMetrics(root).triangles>(model==='office'?40_000:18_000));let shared=false;const sourceGeometry=new Set();asset.scene.getObjectByName(model).traverse(o=>{if(o.isMesh)sourceGeometry.add(o.geometry);});root.traverse(o=>{if(o.isMesh){shared=true;assert.ok(sourceGeometry.has(o.geometry));}});assert.ok(shared);
    const sourceSize=new Box3().setFromObject(asset.scene.getObjectByName(model)).getSize(new Vector3());assert.ok(Math.abs(size.x/size.y-(rotation===Math.PI/2?sourceSize.z:sourceSize.x)/sourceSize.y)<.001);
  }
  assert.equal(loads,1);assert.deepEqual(library.stats(),{requests:1,cachedFiles:1,loadedFiles:1});
  await assert.rejects(library.instantiate('architecture',{model:'absent',height:2}),/Missing model/);library.dispose();await assert.rejects(library.get('architecture'),/disposed/);
});
test('the real showcase has ten model types, aligned supports and passable paving beside solid imported buildings',async()=>{
  const library=createModelLibrary({load:async url=>{const path=new URL(url);path.search='';return geometryAsset(fileURLToPath(path));}}),roots=[];
  for(const {asset,...options} of showcasePlan)roots.push(await library.instantiate(asset,options));
  const solids=roots.map(r=>r.userData.collider).filter(Boolean);
  assert.equal(roots.length,36);assert.equal(new Set(roots.map(r=>r.name)).size,10);assert.equal(library.stats().requests,4);
  for(let i=0;i<roots.length;i++){
    const box=new Box3().setFromObject(roots[i]);assert.ok(Math.abs(box.min.y-showcasePlan[i].y)<.0001);
    if(['manhole','drain'].includes(roots[i].name))assert.ok(Math.abs(box.max.y-.005)<.0001,'street covers remain flush');
  }
  const tree=roots.find(r=>r.name==='tree');assert.ok(tree.userData.collider.w<1.3,'collision follows the trunk instead of the canopy');
  for(let x=-16;x<=16;x+=.25){assert.equal(blocked(x,6.1,solids),false,`clear walking strip at ${x}`);assert.equal(blocked(x,10.5,solids),false,'no solids in road');}
  const p={x:-7,z:6.1};slide(p,0,-40,solids);assert.ok(p.z>.7,'imported facade collision stops approach');assert.equal(blocked(p.x,p.z,solids),false);
  library.dispose();
});
test('concurrent requests share a promise; failed loads can retry without caching a broken asset',async()=>{
  let calls=0;const scene=new Group();scene.add(new Mesh(new BoxGeometry(1,1,1),new MeshStandardMaterial()));
  const library=createModelLibrary({load:async()=>{if(++calls===1)throw Error('temporary failure');return {scene};}});
  const a=library.get('tree'),b=library.get('tree');assert.equal(a,b);await assert.rejects(a,/temporary failure/);
  const root=await library.instantiate('tree',{height:6.5});assert.equal(calls,2);assert.equal(modelMetrics(root).meshes,1);assert.equal(root.userData.collider.h,6.5);
  await assert.rejects(library.instantiate('tree',{height:NaN}),/Invalid model transform/);await assert.rejects(library.get('unknown'),/Unknown asset/);library.dispose();
});
