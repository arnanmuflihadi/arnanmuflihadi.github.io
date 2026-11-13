import test from'node:test';import assert from'node:assert/strict';
import{readFileSync}from'node:fs';import{createHash}from'node:crypto';
import{createQuestState,advanceQuest,questPlaces,questMarker}from'../assets/js/urban-atlas/quest-state.js';
import{createCombatSimulation,unobstructed,inServiceYard}from'../assets/js/urban-atlas/combat-simulation.js';
import{residents,stepResident}from'../assets/js/urban-atlas/city-life.js';
import{blocked}from'../assets/js/urban-atlas/collision.js';import{createDistrict}from'../assets/js/urban-atlas/scene.js';
import{Scene,GLTFLoader,Box3}from'../assets/js/vendor/three-atlas.module.js';
import{createCharacter}from'../assets/js/urban-atlas/character.js';
import{createRiggedActor,disposeAsset}from'../assets/js/urban-atlas/rigged-actor.js';
import{projects}from'../assets/js/project-registry.js';
import{groundHeight}from'../assets/js/urban-atlas/layout.js';
const parse=async path=>{const b=readFileSync(path);return new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');};

test('quest requires a complete ordered story and never changes the research registry',()=>{
 const registry=JSON.stringify(projects);let q=createQuestState({version:1,phase:'forged'});assert.equal(q.phase,'available');
 for(const event of ['collect','report','defeat'])assert.equal(advanceQuest(q,event).phase,'available');
 for(const[event,phase]of[['accept','searching'],['defeat','device-ready'],['collect','returning'],['report','complete']]){q=advanceQuest(q,event);assert.equal(q.phase,phase);}
 assert.equal(questMarker(q),null);assert.equal(JSON.stringify(projects),registry);assert.equal(createQuestState({version:2,phase:'complete'}).phase,'available');
});
test('one attack hits once, queued input chains a second authored punch, and walls/direction prevent hits',()=>{
 const sim=createCombatSimulation(),position={x:-20,z:37};sim.enemy.state='Recover';
 sim.step(.01,{position,facing:0,attack:true});for(let i=0;i<16;i++)sim.step(.04,{position,facing:0,attack:i===4});
 assert.equal(sim.player.combo,2);for(let i=0;i<17;i++)sim.step(.04,{position,facing:0});assert.equal(sim.enemy.health,36);
 const wrong=createCombatSimulation();wrong.enemy.state='Recover';for(let i=0;i<17;i++)wrong.step(.04,{position,facing:Math.PI,attack:i===0});assert.equal(wrong.enemy.health,96);
 const walls=[{x:-20,z:38,w:4,d:.3,h:2}],wall=createCombatSimulation(walls);assert.equal(unobstructed(position,wall.enemy,walls),false);
 for(let i=0;i<17;i++)wall.step(.04,{position,facing:0,attack:i===0});assert.equal(wall.enemy.health,96);
});
test('telegraphed enemy swings apply damage once; forward guard and timed dodge reduce or avoid it',()=>{
 const position={x:-20,z:37};
 for(const[defense,expected]of[['none',76],['guard',95],['dodge',100]]){
  const sim=createCombatSimulation();sim.enemy.state='Attack';sim.enemy.elapsed=.8;sim.enemy.yaw=Math.PI;
  if(defense==='dodge'){sim.player.state='dodge';sim.player.elapsed=.08;}
  for(let i=0;i<5;i++)sim.step(.05,{position,facing:0,guard:defense==='guard'});
  assert.equal(sim.player.health,expected,defense);
 }
 const backwards=createCombatSimulation();backwards.enemy.state='Attack';backwards.enemy.elapsed=.8;backwards.enemy.yaw=Math.PI;backwards.step(.05,{position,facing:Math.PI,guard:true});assert.equal(backwards.player.health,76);
});
test('dodge has a cooldown, defeat emits once, reset restores both actors, and leaving leashes the enemy',()=>{
 const sim=createCombatSimulation(),position={x:-20,z:37};sim.step(.01,{position,dodge:true,direction:{x:1,z:0}});assert.equal(sim.player.state,'dodge');assert.ok(sim.player.cooldown>0);
 sim.step(.05,{position,dodge:true});assert.ok(sim.player.elapsed>0);assert.ok(sim.player.cooldown<.9);
 const defeated=createCombatSimulation();let count=0;
 for(let i=0;i<5;i++){defeated.player.state='free';defeated.enemy.state='Attack';defeated.enemy.hit=false;defeated.enemy.yaw=Math.PI;defeated.enemy.elapsed=.84;count+=defeated.step(.02,{position}).events.filter(e=>e==='player-defeated').length;}
 assert.equal(defeated.player.health,0);assert.equal(count,1);assert.equal(defeated.step(.02,{position}).events.includes('player-defeated'),false);
 defeated.reset();assert.equal(defeated.player.health,100);assert.equal(defeated.enemy.health,96);
 assert.equal(inServiceYard(questPlaces.entrance),false,'recovery point is outside the encounter');
 sim.enemy.x=-15;sim.enemy.state='Chase';for(let i=0;i<200;i++)sim.step(.05,{position:{x:0,z:28}});assert.ok(Math.hypot(sim.enemy.x+20,sim.enemy.z-39)<2);assert.ok(['Idle','Patrol','Return'].includes(sim.enemy.state));
});
test('NPC routes and quest approaches use the actual reachable collision layout',()=>{
 const previous=globalThis.document;let district;
 try{globalThis.document={createElement:()=>({getContext:()=>({fillRect(){},fillText(){}})})};district=createDistrict();}finally{globalThis.document=previous;}
 try{
  for(const spec of residents){
   const points=spec.route?.map(([x,z])=>({x,z}))||[spec.point];for(const p of points)assert.equal(blocked(p.x,p.z,district.obstacles),false,spec.id);
   if(spec.route){const position={...points[0]};for(let i=1;i<=points.length;i++){const goal=points[i%points.length];let steps=0;while(Math.hypot(position.x-goal.x,position.z-goal.z)>.3&&steps++<1800){stepResident(position,goal,1.05,.05,district.obstacles);assert.equal(blocked(position.x,position.z,district.obstacles),false,spec.id);}assert.ok(steps<1800,spec.id+' reaches waypoint '+JSON.stringify({position,goal}));}}
  }
  for(const point of Object.values(questPlaces))assert.equal(blocked(point.x,point.z,district.obstacles),false);
  // Former stoop coordinates predated the +11 m street move and imported frontages.
  assert.equal(groundHeight(-24,-18.65),.26);assert.equal(groundHeight(-19.2,28),.26);assert.equal(groundHeight(-20,39),.06);
 }finally{district.dispose();}
});
test('real NPC clones have independent skeletons and animation while sharing geometry',async()=>{
 const asset=await parse('assets/game/phase3/city-resident.glb'),scene=new Scene(),a=createRiggedActor(scene,asset),b=createRiggedActor(scene,asset);
 const meshes=actor=>{const result=[];actor.model.traverse(o=>{if(o.isSkinnedMesh)result.push(o);});return result;};const aa=meshes(a),bb=meshes(b);
 assert.ok(aa.length>0);assert.notEqual(aa[0].skeleton,bb[0].skeleton);assert.notEqual(aa[0].skeleton.bones[4],bb[0].skeleton.bones[4]);assert.equal(aa[0].geometry,bb[0].geometry);
 a.animator.update(.4,1);b.animator.update(.1,0);assert.notEqual(a.animator.actions.Walk.time,b.animator.actions.Walk.time);
 const extra=await parse('assets/game/phase3/explorer-actions.glb');a.animator.addClips(extra.animations);const arm=a.model.getObjectByName('UpperArmL'),before=arm.quaternion.clone();a.animator.setOverride('Attack1',{duration:.62});a.animator.update(.24,0);assert.equal(a.animator.state,'Attack1');assert.ok(arm.quaternion.angleTo(before)>.1,'authored punch really moves the matching rig');assert.equal(a.root.position.x,0);a.animator.setOverride(null);a.animator.update(.3,0);assert.equal(a.animator.state,'Idle');a.dispose();b.dispose();disposeAsset(asset);
});
test('Phase 3 assets match hashes, carry real rigs and authored actions, and have no external buffers',()=>{
 const manifest=JSON.parse(readFileSync('assets/game/phase3/source.json','utf8'));
 for(const model of manifest.models){const bytes=readFileSync(`assets/game/phase3/${model.id}.glb`),g=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString());assert.equal(createHash('sha256').update(bytes).digest('hex'),model.outputSha256);assert.ok(g.buffers.every(b=>!b.uri));assert.ok((g.images||[]).every(i=>!i.uri));assert.equal(g.animations.length,Object.keys(model.clips).length);if(!model.animationOnly)assert.ok(g.skins[0].joints.length>=40);else assert.equal((g.meshes||[]).length,0);}
});
test('deformed roll and defeat geometry stay above paving without moving the physics root',async()=>{
 const scene=new Scene(),actor=await createCharacter(scene,{}, {x:0,z:28},{gltf:await parse('assets/game/characters/urban-explorer/urban-explorer.glb')});
 actor.animator.addClips((await parse('assets/game/phase3/explorer-actions.glb')).animations);const start=actor.root.position.clone();
 const input={keys:new Set(),touch:new Set(),yaw:0};
 for(const[name,duration,frames]of[['Dodge',.58,29],['Defeat',1.1,55]]){actor.reset();actor.animator.setOverride(name,{duration});for(let i=0;i<frames;i++){actor.update(.02,input,[],false);scene.updateMatrixWorld(true);assert.ok(new Box3().setFromObject(actor.model).min.y>start.y-.005);assert.ok(actor.visual.position.y<.5,'clearance must not accumulate across renderer matrix updates');}assert.deepEqual(actor.root.position,start);actor.animator.setOverride(null);for(let i=0;i<20;i++)actor.update(.02,input,[],false);assert.ok(actor.visual.position.y<.01);}
 actor.dispose();
});
