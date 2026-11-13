#!/usr/bin/env node
// Bake onto the explorer rig offline; ship three clips without the library mannequin.
import {readFile,writeFile,copyFile} from 'node:fs/promises';
import {resolve} from 'node:path';import {pathToFileURL} from 'node:url';import {createHash} from 'node:crypto';
const arg=n=>{const i=process.argv.indexOf(n);if(i<0)throw Error(`Required ${n}`);return resolve(process.argv[i+1]);};
const deps=arg('--deps'),three=arg('--three'),source=arg('--source');
const T=await import(pathToFileURL(resolve(three,'three/build/three.module.js')));
const {GLTFLoader}=await import(pathToFileURL(resolve(three,'three/examples/jsm/loaders/GLTFLoader.js')));
const {NodeIO}=await import(pathToFileURL(resolve(deps,'@gltf-transform/core/dist/index.modern.js')));
const {prune,dedup}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const parse=async p=>{const b=await readFile(p);return new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');};
const path=resolve(source,'UAL1_Standard.glb'),targetPath='assets/game/characters/urban-explorer/urban-explorer.glb';
const src=await parse(path),target=await parse(targetPath);
for(const a of[src,target]){const skeletons=new Set();a.scene.traverse(o=>{if(o.isSkinnedMesh)skeletons.add(o.skeleton);});skeletons.forEach(s=>s.pose());a.scene.updateMatrixWorld(true);}
const mapping={Body:'pelvis',Abdomen:'spine_01',Torso:'spine_02',Chest:'spine_03',Neck:'neck_01',Head:'Head'};
for(const side of ['L','R']){
 const s=side.toLowerCase();for(const[t,f]of Object.entries({Shoulder:'clavicle',UpperArm:'upperarm',LowerArm:'lowerarm',Wrist:'hand',UpperLeg:'thigh',LowerLeg:'calf',Foot:'foot'}))mapping[t+side]=f+'_'+s;
 for(const finger of ['Index','Middle','Ring','Pinky','Thumb'])for(let i=1;i<=(finger==='Thumb'?3:4);i++)mapping[finger+i+side]=finger.toLowerCase()+'_'+String(i).padStart(2,'0')+(i===4?'_leaf':'')+'_'+s;
}
const rest=new Map();target.scene.traverse(n=>{if(n.isBone)rest.set(n.name,{node:n,rotation:n.quaternion.clone(),position:n.position.clone(),world:n.getWorldQuaternion(new T.Quaternion())});});
const sourceRest=new Map(Object.values(mapping).map(name=>{const n=src.scene.getObjectByName(name);if(!n)throw Error('Unmapped source bone '+name);return[name,{node:n,world:n.getWorldQuaternion(new T.Quaternion()),position:n.getWorldPosition(new T.Vector3())}];}));
const ordered=[...rest.values()].filter(b=>mapping[b.node.name]);
const depth=n=>{let v=0;for(let p=n.parent;p;p=p.parent)v++;return v;};ordered.sort((a,b)=>depth(a.node)-depth(b.node));
const footOffsets={};for(const side of ['L','R'])footOffsets[side]=target.scene.getObjectByName('LowerLeg'+side).worldToLocal(target.scene.getObjectByName('Foot'+side).getWorldPosition(new T.Vector3()));
const body=target.scene.getObjectByName('Body'),bodyRest=body.position.clone(),ratio=body.getWorldPosition(new T.Vector3()).y/sourceRest.get('pelvis').position.y;
const io=new NodeIO(),doc=await io.read(targetPath),buffer=doc.getRoot().listBuffers()[0];
for(const a of doc.getRoot().listAnimations())a.dispose();for(const n of doc.getRoot().listNodes()){n.setMesh(null);n.setSkin(null);}for(const s of doc.getRoot().listSkins())s.dispose();
const targetNodes=new Map(doc.getRoot().listNodes().map(n=>[n.getName().replaceAll('.',''),n]));
const clips={Jump_Start:'JumpStart',Jump_Loop:'JumpAir',Jump_Land:'JumpLand'},report=[];
for(const [sourceName,name]of Object.entries(clips)){
 const clip=src.animations.find(c=>c.name===sourceName);if(!clip)throw Error('Missing '+sourceName);
 const mixer=new T.AnimationMixer(src.scene),action=mixer.clipAction(clip);action.setLoop(T.LoopOnce,1);action.clampWhenFinished=true;action.play();
 const times=[],rotations=new Map(ordered.map(b=>[b.node.name,[]])),positions=new Map(['Body','FootL','FootR'].map(n=>[n,[]]));
 const frames=Math.ceil(clip.duration*30);
 for(let i=0;i<=frames;i++){
  const time=Math.min(clip.duration,i/30);times.push(time);mixer.setTime(time);src.scene.updateMatrixWorld(true);
  // Restore target's original bone lengths each sample. No scale tracks are emitted.
  for(const r of rest.values()){r.node.quaternion.copy(r.rotation);r.node.position.copy(r.position);}target.scene.updateMatrixWorld(true);
  for(const r of ordered){
   const from=sourceRest.get(mapping[r.node.name]),delta=from.node.getWorldQuaternion(new T.Quaternion()).multiply(from.world.clone().invert()),world=delta.multiply(r.world);
   const parent=r.node.parent.getWorldQuaternion(new T.Quaternion());r.node.quaternion.copy(parent.invert().multiply(world)).normalize();r.node.updateMatrixWorld(true);
  }
  const shift=sourceRest.get('pelvis').node.getWorldPosition(new T.Vector3()).sub(sourceRest.get('pelvis').position);
  body.position.copy(bodyRest);body.position.y+=shift.y*ratio;target.scene.updateMatrixWorld(true);
  for(const side of ['L','R']){
   const foot=target.scene.getObjectByName('Foot'+side),calf=target.scene.getObjectByName('LowerLeg'+side),world=calf.localToWorld(footOffsets[side].clone());foot.position.copy(foot.parent.worldToLocal(world));
  }
  target.scene.updateMatrixWorld(true);
  for(const r of ordered){const values=rotations.get(r.node.name),q=r.node.quaternion;if(values.length&&new T.Quaternion().fromArray(values,values.length-4).dot(q)<0)q.set(-q.x,-q.y,-q.z,-q.w);values.push(q.x,q.y,q.z,q.w);}
  for(const[key,values]of positions)values.push(...target.scene.getObjectByName(key).position.toArray());
 }
 const animation=doc.createAnimation(name),input=doc.createAccessor(name+' time').setType('SCALAR').setArray(new Float32Array(times)).setBuffer(buffer);
 const channel=(node,path,values,type)=>{const output=doc.createAccessor().setType(type).setArray(new Float32Array(values)).setBuffer(buffer),sampler=doc.createAnimationSampler().setInput(input).setOutput(output).setInterpolation('LINEAR');animation.addSampler(sampler).addChannel(doc.createAnimationChannel().setTargetNode(targetNodes.get(node)).setTargetPath(path).setSampler(sampler));};
 for(const[node,values]of rotations)channel(node,'rotation',values,'VEC4');for(const[node,values]of positions)channel(node,'translation',values,'VEC3');
 report.push({sourceName,name,duration:clip.duration,samples:times.length,bones:rotations.size});mixer.stopAllAction();mixer.uncacheRoot(src.scene);
}
await doc.transform(prune(),dedup());const output='assets/game/characters/urban-explorer/jump-animations.glb';await io.write(output,doc);
const sha=b=>createHash('sha256').update(b).digest('hex');await copyFile(resolve(source,'License.txt'),'assets/game/characters/urban-explorer/jump-LICENSE.txt');
await writeFile('assets/game/characters/urban-explorer/jump-source.json',JSON.stringify({author:'Quaternius',source:'https://quaternius.com/packs/universalanimationlibrary.html',edition:'Universal Animation Library Standard, in-place Unreal-Godot GLB',license:'CC0-1.0',sourceSha256:sha(await readFile(path)),targetSha256:sha(await readFile(targetPath)),outputSha256:sha(await readFile(output)),bytes:(await readFile(output)).length,clips:report,retarget:['World-space rotational deltas from inverse-bind rest poses, converted into each destination parent space','Preserve original target bone lengths and scales','Reconstruct legacy sibling Foot targets from their original calf-relative offsets','Keep pelvis vertical pose movement; strip horizontal and root displacement so physics owns travel','Bake 30 Hz; emit animation channels only, without the library mannequin, meshes or textures']},null,2)+'\n');console.log(report,{bytes:(await readFile(output)).length});
