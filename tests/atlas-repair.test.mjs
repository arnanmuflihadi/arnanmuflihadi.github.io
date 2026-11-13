import test from 'node:test';import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';import{createHash}from'node:crypto';
import{createPlayerController,jumpPhysics}from'../assets/js/urban-atlas/player-controller.js';
import{separateFromPeople,blocked}from'../assets/js/urban-atlas/collision.js';
import{groundHeight}from'../assets/js/urban-atlas/layout.js';
import{npcRegistry,researchConversation}from'../assets/js/urban-atlas/npc-registry.js';
import{projectById}from'../assets/js/project-registry.js';
import{Scene,Group,GLTFLoader,Box3,Vector3}from'../assets/js/vendor/three-atlas.module.js';
import{createCharacter}from'../assets/js/urban-atlas/character.js';
import{createInput}from'../assets/js/urban-atlas/input.js';
const input=(keys=[])=>({keys:new Set(keys),touch:new Set(),yaw:0});
const rootAt=(x=0,z=28)=>{const root=new Group();root.position.set(x,groundHeight(x,z),z);return root;};
const parse=async path=>{const b=readFileSync(path);return new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');};
const json=path=>{const b=readFileSync(path);return JSON.parse(b.subarray(20,20+b.readUInt32LE(12)).toString());};

test('jump follows gravity, has a consistent apex across frame rates, and lands once',()=>{
 const apex=[];
 for(const dt of[1/30,1/60,1/120]){
  const root=rootAt(),m=createPlayerController(root),floor=root.position.y;let top=floor,air=false;
  for(let i=0;i<2/dt;i++){const state=m.update(dt,input(),[],{jump:i===0});top=Math.max(top,root.position.y);air||=!state.grounded;assert.ok(root.position.y>=floor-.001);}
  assert.ok(air);assert.equal(m.landings,1);assert.equal(m.jumps,1);assert.equal(m.phase,'grounded');assert.equal(root.position.y,floor);apex.push(top-floor);
 }
 const expected=jumpPhysics.launchSpeed**2/(2*jumpPhysics.gravity);for(const h of apex)assert.ok(Math.abs(h-expected)<.015,`${h} versus ${expected}`);
});
test('walk/run jumps retain directional movement; airborne jump requests cannot add launches',()=>{
 for(const keys of[['w'],['w','shift']]){
  const root=rootAt(),m=createPlayerController(root);let maximum=0;
  for(let i=0;i<65;i++){m.update(.02,input(keys),[],{jump:i===0||(!m.grounded&&i%2===0)});maximum=Math.max(maximum,root.position.y);}
  assert.equal(m.jumps,1);assert.equal(m.landings,1);assert.ok(root.position.z<26);assert.ok(maximum>1.2);
 }
});
test('steps and the real station ramp support jumping, while walls and low ceilings remain solid',()=>{
 const root=rootAt(-23,7.1),m=createPlayerController(root);let jumped=false;
 for(let i=0;i<200;i++){m.update(.02,input(['w']),[],{jump:i===70});jumped||=!m.grounded;}
 assert.ok(jumped);assert.equal(m.grounded,true);assert.equal(root.position.y,groundHeight(root.position.x,root.position.z));assert.ok(root.position.y>.5);
 const wall=rootAt(0,0),w=createPlayerController(wall,{heightAt:()=>0}),obstacles=[{x:0,z:-1,w:5,d:.4,h:6}];
 for(let i=0;i<80;i++)w.update(.02,input(['w']),obstacles,{jump:i===0});assert.ok(wall.position.z>-.47);assert.equal(w.grounded,true);
 const low=rootAt(0,0),c=createPlayerController(low,{heightAt:()=>0}),roof=[{x:0,z:0,w:5,d:5,minY:2.5,h:2.7,cameraOnly:true}];let highest=0;
 for(let i=0;i<100;i++){c.update(.01,input(),roof,{jump:i===0});highest=Math.max(highest,low.position.y);}assert.ok(highest<=.6);assert.equal(c.grounded,true);
});
test('support drops cause a fall; unsafe positions recover and mode handoff settles vertical state',()=>{
 const root=rootAt(0,0);root.position.y=1;const m=createPlayerController(root,{heightAt:(x,z)=>z<-.2?0:1});
 let airborne=false;for(let i=0;i<100;i++){m.update(.02,input(['w']),[]);airborne||=!m.grounded;}assert.ok(airborne);assert.equal(root.position.y,0);
 root.position.y=NaN;m.update(.02,input(),[]);assert.ok(Number.isFinite(root.position.y));
 m.update(.02,input(),[],{jump:true});for(let i=0;i<20;i++)m.update(.02,input(),[]);assert.equal(m.grounded,false);m.settle();assert.equal(m.grounded,true);assert.equal(m.verticalVelocity,0);assert.equal(root.position.y,0);
});
test('retargeted authored jump clips animate the original rig without stretching bones or moving physics',async()=>{
 const actor=await createCharacter(new Scene(),{}, {x:0,z:28},{gltf:await parse('assets/game/characters/urban-explorer/urban-explorer.glb')});
 const extra=await parse('assets/game/characters/urban-explorer/jump-animations.glb');actor.animator.addClips(extra.animations);
 const start=actor.root.position.clone(),lengths=new Map();actor.model.traverse(o=>{if(o.isBone&&!['Body','FootL','FootR','PTL','PTR'].includes(o.name))lengths.set(o.name,o.position.length());});
 const phases=new Set(),poses=new Set();let width=0,clearance=0;
 for(let i=0;i<130;i++){
  const motion=actor.update(.01,input(),[],false,{jump:i===0});phases.add(motion.phase);poses.add(actor.animator.state);actor.root.updateMatrixWorld(true);
  const size=new Box3().setFromObject(actor.model).getSize(new Vector3());width=Math.max(width,size.x);clearance=Math.max(clearance,actor.visual.position.y);
  actor.model.traverse(o=>{if(lengths.has(o.name))assert.ok(Math.abs(o.position.length()-lengths.get(o.name))<.003,o.name+' bone length (including original locomotion translation tracks)');});
 }
 assert.deepEqual(phases,new Set(['takeoff','airborne','landing','grounded']));for(const pose of['JumpStart','JumpAir','JumpLand','Idle'])assert.ok(poses.has(pose));
 assert.deepEqual(actor.root.position,start);assert.ok(width<2.3);assert.ok(clearance<.65);assert.equal(actor.movement.jumps,1);actor.dispose();
});
test('every fictional guide has a verified project, distinct identity, behavior, and research choices',()=>{
 const names=['Nadia','Raka','Kirana','Damar','Bima','Sinta'];assert.equal(new Set(npcRegistry.map(n=>n.id)).size,npcRegistry.length);
 for(const name of names){const n=npcRegistry.find(n=>n.name===name);assert.ok(n);assert.equal(n.fictional,true);const p=projectById(n.study);assert.ok(existsSync(p.caseStudyUrl));assert.equal(n.district,p.district);assert.ok(n.animations.idle&&n.animations.walk);if(n.active)assert.ok(n.point||n.route);else assert.equal(n.interactionState,'region-planned');for(const topic of['greeting','research','limitations']){const copy=researchConversation(n.id,topic);assert.ok(copy.text.length>30);assert.equal(copy.caseStudyUrl,p.caseStudyUrl);assert.deepEqual(copy.actions.map(a=>a.id),['research','study','limitations','close']);}}
 assert.match(researchConversation('damar','limitations').text,/not a household income estimate/);
});
test('selected imported architecture is self-contained, quantized, hash verified and within budget',()=>{
 const manifest=JSON.parse(readFileSync('assets/game/scenery/architecture-source.json','utf8')),b=readFileSync(manifest.output),g=json(manifest.output);
 assert.equal(createHash('sha256').update(b).digest('hex'),manifest.outputSha256);assert.ok(b.length<6_000_000);assert.equal(manifest.models.length,11);assert.ok(g.extensionsUsed.includes('KHR_mesh_quantization'));assert.ok(g.buffers.every(v=>!v.uri));assert.ok(g.images.every(v=>!v.uri));assert.equal(g.scenes[g.scene].nodes.length,11);assert.ok(manifest.models.find(m=>m.id==='office').triangles>40_000);for(const id of['drain','manhole'])assert.ok(manifest.models.some(m=>m.id===id));
 const provenance=JSON.parse(readFileSync('assets/game/characters/urban-explorer/jump-source.json','utf8')),jump=readFileSync('assets/game/characters/urban-explorer/jump-animations.glb'),a=json('assets/game/characters/urban-explorer/jump-animations.glb');assert.equal(createHash('sha256').update(jump).digest('hex'),provenance.outputSha256);assert.deepEqual(a.animations.map(v=>v.name),['JumpStart','JumpAir','JumpLand']);assert.equal(a.meshes?.length||0,0);assert.equal(a.images?.length||0,0);assert.ok(!a.animations.some(v=>v.channels.some(c=>c.target.path==='scale')));
});

test('an approaching resident cannot trap a player inside its collision footprint',()=>{const player={x:0,z:0},people=[{x:0,z:.55}],obstacles=people.map(p=>({...p,w:.6,d:.6,h:1.9}));assert.equal(blocked(player.x,player.z,obstacles),true);separateFromPeople(player,people,[]);assert.equal(blocked(player.x,player.z,obstacles),false);});

test('the pavilion floor and approach ramp support walking and a full jump',()=>{
 assert.equal(groundHeight(29,12.5),.24);assert.equal(groundHeight(29,15.5),.57);assert.equal(groundHeight(29,21),.57);
 assert.equal(groundHeight(22.1,15.6),-.02,'clipped slab corners do not create invisible support');
 const root=rootAt(29,12),motion=createPlayerController(root);
 for(let i=0;i<140;i++)motion.update(.02,input(['s']),[]);
 assert.ok(root.position.z>16);assert.equal(root.position.y,.57);
 for(let i=0;i<100;i++)motion.update(.02,input(),[],{jump:i===0});
 assert.equal(motion.landings,1);assert.equal(root.position.y,.57);
});

test('keyboard controls isolate dialogue, reject repeated jumps, and operate focused walking buttons',()=>{
 const old={document:globalThis.document,addEventListener:globalThis.addEventListener},window=new EventTarget(),canvas=new EventTarget(),button=new EventTarget();
 let modal=false;button.dataset={move:'w'};
 const host={hidden:false,querySelectorAll:selector=>selector==='[data-move]'?[button]:[]};
 globalThis.document={querySelector:selector=>selector==='dialog[open]'&&modal?{}:null};globalThis.addEventListener=window.addEventListener.bind(window);
 const emit=(target,type,key,extra={})=>{const event=new Event(type,{cancelable:true});Object.assign(event,{key,repeat:false,...extra});target.dispatchEvent(event);return event;};
 let controls;
 try{
  controls=createInput(canvas,host,()=>{});
  assert.equal(emit(window,'keydown',' ').defaultPrevented,true);assert.deepEqual([...controls.consumeActions()],['jump']);
  emit(window,'keydown',' ',{repeat:true});assert.equal(controls.consumeActions().size,0);
  assert.equal(emit(window,'keydown','r',{metaKey:true}).defaultPrevented,false);assert.equal(controls.keys.has('r'),false);
  modal=true;emit(window,'keydown',' ');assert.equal(controls.consumeActions().size,0);modal=false;
  emit(window,'keydown','q');controls.updateCamera(.5);assert.ok(controls.yaw>.8);emit(window,'keyup','q');
  emit(button,'keydown','Enter');assert.equal(controls.touch.has('w'),true);emit(button,'keyup','Enter');assert.equal(controls.touch.has('w'),false);
  emit(button,'keydown',' ');button.dispatchEvent(new Event('blur'));assert.equal(controls.touch.has('w'),false);
  controls.enabled=false;emit(window,'keydown',' ');assert.equal(controls.consumeActions().size,0);
 }finally{controls?.destroy();globalThis.document=old.document;globalThis.addEventListener=old.addEventListener;}
});
