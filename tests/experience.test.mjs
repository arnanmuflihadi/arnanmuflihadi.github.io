import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {projects,projectById} from '../assets/js/project-registry.js';
import {readRoute,routeUrl,createState} from '../assets/js/experience-state.js';
import {move,blocked} from '../assets/js/rpg/collision-system.js';
import {district} from '../assets/js/rpg/district.js';
import {createPlayer} from '../assets/js/rpg/player-controller.js';
import {createCamera} from '../assets/js/rpg/third-person-camera.js';
import {Scene,Group,Mesh,BoxGeometry,MeshBasicMaterial} from '../assets/js/vendor/three-rpg.module.js';
test('registry contains six unique, existing research routes',()=>{
 assert.equal(projects.length,6);assert.equal(new Set(projects.map(p=>p.id)).size,6);
 for(const p of projects){assert.ok(existsSync(p.caseStudyUrl));const html=readFileSync(p.caseStudyUrl,'utf8');assert.ok(html.includes('<h1'));for(const m of p.mapUrls||[])assert.ok(existsSync(m.url));}
 assert.equal(projects.filter(p=>p.availableInGame).length,3);
 assert.ok(readFileSync(projectById('transit').caseStudyUrl,'utf8').includes('26.6%'));
});
test('URL roundtrip preserves hosting path, hash, unrelated parameters and project context',()=>{
 for(const experience of ['professional','rpg'])for(const activeProject of [null,...projects.map(p=>p.id)]){
 const url=routeUrl('https://example.test/portfolio/index.html?lang=en#selected-work',{experience,activeProject});
 assert.deepEqual(readRoute(url),{experience,activeProject});assert.equal(url.pathname,'/portfolio/index.html');assert.equal(url.searchParams.get('lang'),'en');assert.equal(url.hash,'#selected-work');}
});
test('invalid deep links and saved mission values are sanitized',()=>{
 assert.deepEqual(readRoute('https://example.test/?experience=bad&project=%3Cscript%3E'),{experience:'professional',activeProject:null});
 assert.equal(createState(readRoute('https://example.test/'),null).playerPosition,null);
 assert.equal(createState(readRoute('https://example.test/'),{playerPosition:{x:Infinity,z:0}}).playerPosition,null);
 assert.deepEqual(createState(readRoute('https://example.test/'),{playerPosition:{x:2,z:3}}).playerPosition,{x:2,z:3});
 assert.deepEqual(createState(readRoute('https://example.test/'),{missionProgress:{transit:true,cbd:'true',forged:true}}).missionProgress,{transit:true});
});
test('collision prevents tunnelling, permits wall sliding and bounds the district',()=>{
 const blocks=[{x:0,z:0,w:4,d:4}];const p={x:0,z:6};move(p,0,-30,blocks);assert.ok(p.z>=2.42-.001);assert.equal(blocked(p.x,p.z,blocks),false);
 move(p,20,0,blocks);assert.ok(p.x>10);move(p,1000,1000,blocks);assert.ok(p.x<=30.58&&p.z<=30.58);
});
test('both landmark focus positions are safe and reachable from the spawn',()=>{
 for(const l of district.landmarks){assert.equal(blocked(l.focus.x,l.focus.z,district.buildings),false);
 // Breadth-first walk across the actual collision layout on a half-unit lattice.
 const todo=[[district.spawn.x,district.spawn.z]],seen=new Set();let found=false;
 while(todo.length){const [x,z]=todo.shift(),key=x+','+z;if(seen.has(key)||blocked(x,z,district.buildings))continue;seen.add(key);if(Math.hypot(x-l.focus.x,z-l.focus.z)<1){found=true;break;}for(const [dx,dz]of[[.5,0],[-.5,0],[0,.5],[0,-.5]])todo.push([x+dx,z+dz]);}
 assert.equal(found,true,l.projectId);}
});
test('player controls move, sprint, turn, animate and stop against real collision data',()=>{
 const player=createPlayer(new Scene(),district.spawn),input={keys:new Set(['w']),touch:new Set(),yaw:0};
 for(let i=0;i<60;i++)player.update(1/60,input,district.buildings,false);const walked=district.spawn.z-player.group.position.z;assert.ok(walked>3&&walked<5);
 input.keys.add('shift');const before=player.group.position.z;for(let i=0;i<60;i++)player.update(1/60,input,district.buildings,false);assert.ok(before-player.group.position.z>walked);
 input.keys.clear();player.stop();const stopped=player.group.position.z;player.update(1/60,input,district.buildings,true);assert.equal(player.group.position.z,stopped);
});

test('camera pulls ahead of a building behind the player',()=>{
 const player=new Group();player.position.set(14,0,14.18);
 const building=new Mesh(new BoxGeometry(8,5.3,6),new MeshBasicMaterial());building.position.set(11,2.65,23);building.updateMatrixWorld(true);
 const follow=createCamera();follow.update(player,{yaw:0,pitch:.48},[building],.016);
 assert.ok(follow.camera.position.z<20,'camera should remain in front of the obstruction');
 building.geometry.dispose();building.material.dispose();
});
