import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {readAtlasRoute,atlasRoute,createAtlasState} from '../assets/js/living-atlas-state.js';
import {projects} from '../assets/js/project-registry.js';
import {presentations,landmarks,mixComposition} from '../assets/js/urban-atlas/presentation.js';
import {createDistrict} from '../assets/js/urban-atlas/scene.js';
import {layout} from '../assets/js/urban-atlas/layout.js';
import {blocked,slide} from '../assets/js/urban-atlas/collision.js';

test('editorial, adventure and study routes roundtrip under a Pages project path',()=>{
  for(const mode of ['editorial','adventure'])for(const activeProject of [null,...projects.map(p=>p.id)])for(const panel of [false,true]){
    const panelOpen=Boolean(panel&&activeProject),state={mode,activeProject,panelOpen};
    const url=atlasRoute('https://example.test/atlas/portfolio.html?lang=id#selected-work',state);
    assert.deepEqual(readAtlasRoute(url),state);
    assert.equal(url.pathname,'/atlas/portfolio.html');assert.equal(url.searchParams.get('lang'),'id');assert.equal(url.hash,'#selected-work');
  }
  assert.equal(readAtlasRoute('https://example.test/?experience=rpg').mode,'adventure');
  assert.deepEqual(readAtlasRoute('https://example.test/?experience=bogus&project=%3Cscript%3E&panel=study'),{mode:'editorial',activeProject:null,panelOpen:false});
});

test('stored positions cannot replace route context or introduce an invalid player transform',()=>{
  const route=readAtlasRoute('https://example.test/?experience=adventure&project=transit');
  for(const playerPosition of [null,{x:NaN,z:0},{x:Infinity,z:0},{x:45,z:0},{x:'2',z:0}])assert.equal(createAtlasState(route,{playerPosition}).playerPosition,null);
  const saved={mode:'editorial',activeDistrict:'bandung',playerPosition:{x:2,z:3}},state=createAtlasState(route,saved);
  assert.deepEqual(state.playerPosition,{x:2,z:3});assert.equal(state.mode,'adventure');assert.equal(state.activeDistrict,'jakarta');assert.equal(state.activeProject,'transit');
  saved.playerPosition.x=40;assert.equal(state.playerPosition.x,2);assert.equal(state.characterReady,false);assert.ok(state.selectedLandmark);
});

test('all research has a finite cinematic composition and only constructed landmarks permit walking',()=>{
  for(const p of projects){
    const preset=presentations[p.id];assert.ok(preset,p.id);
    assert.ok([...preset.position,...preset.target].every(Number.isFinite));
    assert.equal(Boolean(preset.focus),p.availableInGame);
    if(!p.availableInGame)assert.ok(preset.label.includes('pavilion'));
  }
  assert.deepEqual(landmarks.map(l=>l.projectId).sort(),projects.filter(p=>p.availableInGame).map(p=>p.id).sort());
});

test('camera interpolation clamps endpoints and keeps independent source compositions intact',()=>{
  const a=presentations.arrival,b=presentations.transit,original=JSON.stringify([a,b]);
  assert.deepEqual(mixComposition(a,b,-1).position,a.position);assert.deepEqual(mixComposition(a,b,2).target,b.target);
  assert.deepEqual(mixComposition(a,b,.5).position,a.position.map((v,i)=>(v+b.position[i])/2));
  assert.equal(JSON.stringify([a,b]),original);
});

test('three shared landmark spawns are reachable, interactable and protected by actual district collision',()=>{
  const previous=globalThis.document;let district;
  try{globalThis.document={createElement:()=>({getContext:()=>({fillRect(){},fillText(){}})})};district=createDistrict();}finally{globalThis.document=previous;}
  try{
    const todo=[[layout.spawn.x,layout.spawn.z]],seen=new Set();let head=0;
    while(head<todo.length){const [x,z]=todo[head++],key=x+','+z;if(seen.has(key)||blocked(x,z,district.obstacles))continue;seen.add(key);for(const [dx,dz]of[[1,0],[-1,0],[0,1],[0,-1]])if(Math.abs(x+dx)<44&&Math.abs(z+dz)<44)todo.push([x+dx,z+dz]);}
    for(const l of landmarks){const p=presentations[l.projectId].focus,approach={x:Math.round(p.x),z:Math.ceil(p.z)};assert.ok(seen.has(approach.x+','+approach.z),l.projectId);slide(approach,p.x-approach.x,p.z-approach.z,district.obstacles);assert.ok(Math.hypot(p.x-approach.x,p.z-approach.z)<.001,l.projectId+' exact fractional approach');assert.ok(Math.hypot(l.x-p.x,l.z-p.z)<l.radius);}
    const p={...presentations.transit.focus};slide(p,0,-50,district.obstacles);const atWall={...p};slide(p,0,-5,district.obstacles);
    assert.deepEqual(p,atWall);assert.equal(blocked(p.x,p.z,district.obstacles),false);
    const station=landmarks.find(l=>l.projectId==='transit');assert.ok(Math.hypot(station.x-p.x,station.z-p.z)<station.radius,'research remains reachable at the station entrance');
  }finally{district.dispose();}
});

test('imported scenery matches provenance and contains real self-contained glTF meshes and textures',()=>{
  const manifest=JSON.parse(readFileSync('assets/game/scenery/source.json','utf8'));
  assert.equal(manifest.models.length,4);
  for(const model of manifest.models){
    const bytes=readFileSync(`assets/game/scenery/${model.id}.glb`);
    assert.equal(bytes.readUInt32LE(0),0x46546c67);assert.equal(bytes.readUInt32LE(4),2);assert.equal(bytes.length,model.bytes);
    assert.equal(createHash('sha256').update(bytes).digest('hex'),model.outputSha256);
    const json=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString());
    assert.ok(json.meshes.length);assert.ok(json.meshes.every(m=>m.primitives.every(p=>p.attributes.POSITION!==undefined&&p.attributes.NORMAL!==undefined)));
    assert.ok(json.images.length);assert.ok(json.images.every(i=>i.bufferView!==undefined&&!i.uri));assert.ok(json.buffers.every(b=>!b.uri));
    assert.equal(model.license,'CC0-1.0');assert.ok(existsSync(`assets/game/scenery/${model.pack}-LICENSE.txt`));
  }
});

test('Home and Work preserve semantic research and use one living scene host with a static fallback',()=>{
  for(const page of ['index.html','portfolio.html']){
    const html=readFileSync(page,'utf8');
    assert.equal((html.match(/data-living-world/g)||[]).length,1);assert.equal((html.match(/data-atlas-canvas/g)||[]).length,1);assert.equal((html.match(/<header\b[^>]*data-site-header/g)||[]).length,1);
    assert.ok(html.includes('living-world-poster'));assert.ok(html.includes('data-atlas-mode hidden'));assert.ok(!html.includes('three-hero.min.js'));assert.ok(!html.includes('analyst-3d.js'));
    const expected=page==='portfolio.html'?projects:projects.filter(p=>['transit','pangan','cbd'].includes(p.id));
    for(const p of expected)assert.ok(html.includes(`href="${p.caseStudyUrl}"`));
  }
});
