import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import * as T from '../assets/js/vendor/three-atlas.module.js?v=16';
import {createModelLibrary,modelMetrics} from '../assets/js/urban-atlas/model-library.js';
import {createArchitectureDesignSystem,architecturalVariants} from '../assets/js/urban-atlas/architecture-design-system.js';
import {blocked,slide,clearDistance} from '../assets/js/urban-atlas/collision.js';

async function fixture(){
  globalThis.ProgressEvent ||=class{constructor(type,data){this.type=type;Object.assign(this,data);}};
  return createModelLibrary({load:async url=>{
    const path=new URL(url);path.search='';const b=readFileSync(fileURLToPath(path)),json=JSON.parse(b.subarray(20,20+b.readUInt32LE(12)));
    delete json.images;delete json.textures;delete json.samplers;json.materials=json.materials.map(m=>({name:m.name}));
    json.buffers[0].uri='data:application/octet-stream;base64,'+b.subarray(28+b.readUInt32LE(12)).toString('base64');
    return new T.GLTFLoader().parseAsync(JSON.stringify(json),'');
  }});
}
function fingerprint(root){const hash=createHash('sha256');root.traverse(o=>{if(o.isMesh){for(const a of Object.values(o.geometry.attributes))hash.update(Buffer.from(a.array.buffer));hash.update(o.material.uuid);}});return hash.digest('hex');}
function sourceMeshes(root){const result=[];root.traverse(o=>{if(o.isMesh&&!o.userData.projectAuthored&&!o.userData.terraceVegetation)result.push(o);});return result;}
function glassDepth(root,front){root.updateMatrixWorld(true);let max=-Infinity;root.traverse(o=>{if(o.isMesh&&o.material.name==='MI_Glass'){const a=o.geometry.attributes.position;for(let i=0;i<a.count;i++){const v=new T.Vector3().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);if(v.z>front-.5)max=Math.max(max,v.z);}}});return max;}

test('three enhanced variants retain genuine imported meshes without changing cached source buffers or baseline materials',async()=>{
  const library=await fixture(),asset=await library.get('architecture'),original=fingerprint(asset.scene),system=createArchitectureDesignSystem(library),styles=[];
  for(const id of Object.keys(architecturalVariants)){
    const root=await system.create(id),spec=architecturalVariants[id];styles.push(root);
    assert.equal(root.userData.imported.model,spec.source);assert.equal(root.userData.architecture.id,id);
    assert.ok(sourceMeshes(root).some(o=>o.geometry.attributes.position.count>100));assert.ok(root.userData.architecture.details>60);assert.ok(root.userData.architecture.batches<=10);
    assert.equal(fingerprint(asset.scene),original,'source cache remains immutable');
    const size=new T.Box3().setFromObject(root).getSize(new T.Vector3());assert.ok(size.y>(id==='office'?23:id==='commercial'?14:7));
  }
  assert.ok(modelMetrics(styles[2]).triangles<modelMetrics(styles[1]).triangles,'cropped neighborhood model is smaller, not a five-story building scaled down');
  assert.equal(library.stats().requests,2,'architecture and imported ferns reuse their promises');system.dispose();library.dispose();
});

test('office glass is physically recessed while the uniform source scale and source footprint remain unchanged',async()=>{
  const library=await fixture(),system=createArchitectureDesignSystem(library),baseline=await library.instantiate('architecture',{model:'office',height:22.4}),enhanced=await system.create('office');
  const front=architecturalVariants.office.front;assert.ok(Math.abs(glassDepth(baseline,front)-glassDepth(enhanced,front)-.22)<.001);
  assert.equal(enhanced.userData.imported.scale,baseline.userData.imported.scale);assert.deepEqual(enhanced.userData.collider,baseline.userData.collider);
  assert.ok(enhanced.userData.localColliders.some(c=>c.cameraOnly&&c.minY===3.08));system.dispose();library.dispose();
});

test('all three frontages support character clearance and exported collision remains valid after translation and rotation',async()=>{
  const library=await fixture(),system=createArchitectureDesignSystem(library);
  for(const id of Object.keys(architecturalVariants)){
    const root=await system.create(id),front=root.userData.architecture.front;root.position.set(0,.16,-front);root.updateMatrixWorld(true);
    const bodies=system.collisionBodies(root);assert.ok(root.userData.architecture.groundClearance>=2.8);
    for(let x=-1.8;x<=1.8;x+=.2)assert.equal(blocked(x,1.6,bodies),false,id+' clear covered footway');
    const point={x:.4,z:6};slide(point,0,-20,bodies);assert.ok(point.z>-.01);assert.equal(blocked(point.x,point.z,bodies),false);
    const rayStart={x:0,y:5,z:7},rayEnd={x:0,y:5,z:-3};assert.ok(clearDistance(rayStart,rayEnd,bodies)<10,'camera cannot pass through elevated facade');
    root.position.set(20,.16,-10);root.rotation.y=Math.PI/2;root.updateMatrixWorld(true);const transformed=system.collisionBodies(root);
    assert.ok(transformed.every(c=>[c.x,c.z,c.w,c.d,c.minY,c.h].every(Number.isFinite)&&c.w>0&&c.d>0&&c.h>=c.minY));
    assert.equal(blocked(transformed[0].x,transformed[0].z,transformed),true);
  }system.dispose();library.dispose();
});

test('instanced architectural geometry is counted per visible instance',()=>{
  const mesh=new T.InstancedMesh(new T.BoxGeometry(),new T.MeshStandardMaterial(),7),root=new T.Group();root.add(mesh);assert.equal(modelMetrics(root).triangles,84);mesh.geometry.dispose();mesh.material.dispose();
});

test('enhancement prototypes are cached while instances retain independent transforms and collision data',async()=>{
  const library=await fixture(),system=createArchitectureDesignSystem(library),[a,b]=await Promise.all([system.create('office'),system.create('office')]);
  assert.notEqual(a,b);assert.equal(system.stats().templates,1);const ma=sourceMeshes(a),mb=sourceMeshes(b);assert.equal(ma.length,mb.length);
  ma.forEach((mesh,i)=>{assert.equal(mesh.geometry,mb[i].geometry);assert.equal(mesh.material,mb[i].material);});
  a.position.x=20;a.userData.localColliders[0].x=100;assert.equal(b.position.x,0);assert.equal(b.userData.localColliders[0].x,0);
  system.dispose();await assert.rejects(system.create('office'),/disposed/);library.dispose();
});

test('the enhancement record binds the unchanged source GLB and current generator to their verified digests',()=>{
  const record=JSON.parse(readFileSync('assets/game/scenery/architecture-enhancements.json','utf8'));
  const sha=path=>createHash('sha256').update(readFileSync(path)).digest('hex');
  assert.equal(sha(record.sourceLibrary),record.sourceLibrarySha256);assert.equal(sha(record.generator),record.generatorSha256);
  assert.equal(record.variants.length,3);assert.equal(record.sourceLicense,'CC0-1.0');assert.equal(record.humanReview.score,null);assert.equal(record.humanReview.approved,false);
});

test('captured original and enhanced pairs use identical camera tuples and retain all requested views without a fabricated human score',()=>{
  const evidence=JSON.parse(readFileSync('assets/img/architecture-review/scene-evidence.json','utf8'));
  assert.deepEqual(evidence['office-before'].camera,evidence['office-after'].camera);assert.deepEqual(evidence['shop-before'].camera,evidence['shop-after'].camera);
  for(const id of['office-before','office-after','shop-before','shop-after','variants','detail','street-level','neighborhood']){
    assert.ok(readFileSync(`assets/img/architecture-review/${id}.jpg`).length>10_000);assert.equal(evidence[id].state,'ready');assert.equal(evidence[id].missingTextures.length,0);assert.equal(evidence[id].humanReview.score,null);
  }
  assert.ok(Math.abs(evidence['street-level'].camera.eyeHeight-1.65)<.0001);assert.equal(evidence.variants.architectureCache.templates,3);
});
