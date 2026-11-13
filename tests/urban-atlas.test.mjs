import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {createDistrict} from '../assets/js/urban-atlas/scene.js';
import {shellRoof} from '../assets/js/urban-atlas/geometry.js';
import {layout,groundHeight} from '../assets/js/urban-atlas/layout.js';
import {blocked,slide,clearDistance} from '../assets/js/urban-atlas/collision.js';
import {createCharacter} from '../assets/js/urban-atlas/character.js';
import {createFollowCamera} from '../assets/js/urban-atlas/camera.js';
import {createMaterials} from '../assets/js/urban-atlas/materials.js';
import {Scene,Vector3,Group,GLTFLoader} from '../assets/js/vendor/three-atlas.module.js';
test('bounded substep movement cannot tunnel through a major building',()=>{
 const obstacles=[{x:0,z:0,w:12,d:8,h:7}],p={x:0,z:20};slide(p,0,-50,obstacles);
 assert.ok(p.z>=4.34-.001);assert.equal(blocked(p.x,p.z,obstacles),false);
 slide(p,30,0,obstacles);assert.ok(p.x>20);slide(p,200,200,obstacles);assert.ok(Math.abs(p.x)<44&&Math.abs(p.z)<44);
});
test('camera swept line detects walls and passes above low furniture',()=>{
 const wall=[{x:0,z:5,w:10,d:1,h:8}];
 assert.ok(clearDistance({x:0,y:1.3,z:0},{x:0,y:3,z:9},wall)<5);
 assert.equal(clearDistance({x:0,y:10,z:0},{x:0,y:12,z:9},wall),Math.hypot(9,2));
 assert.equal(clearDistance({x:20,y:1,z:0},{x:20,y:3,z:9},wall),Math.hypot(9,2));
});
test('camera recovers behind a player near a wall without NaN or wall penetration',()=>{
 const follow=createFollowCamera(),player=new Group();player.position.set(0,0,0);const obstacle=[{x:0,z:4,w:8,d:2,h:9}];
 for(let i=0;i<120;i++)follow.update(player,{yaw:0,pitch:.19},obstacle,1/60,false);
 assert.ok(Number.isFinite(follow.camera.position.x));assert.ok(follow.camera.position.z<2.75);
});
test('imported character walks, runs, damps and stops against obstacles',async()=>{
 const bytes=readFileSync('assets/game/characters/urban-explorer/urban-explorer.glb');
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 const scene=new Scene(),materials=createMaterials(),actor=await createCharacter(scene,materials,{x:0,z:28},{gltf}),input={keys:new Set(['w']),touch:new Set(),yaw:0};
 for(let i=0;i<60;i++)actor.update(1/60,input,[],false);const walked=28-actor.root.position.z;assert.ok(walked>1.8&&walked<2.2);
 const before=actor.root.position.z;input.keys.add('shift');for(let i=0;i<60;i++)actor.update(1/60,input,[],false);assert.ok(before-actor.root.position.z>walked*1.6);
 actor.stop();input.keys.clear();const stopped=actor.root.position.clone();actor.update(1/60,input,[],true);assert.deepEqual(actor.root.position,stopped);
 actor.dispose();scene.traverse(o=>{o.geometry?.dispose();o.material?.dispose();});materials.dispose();
});
test('scene core stays independent of portfolio DOM and legacy missions; art-review route remains noindex',()=>{
 const html=readFileSync('urban-atlas.html','utf8');assert.ok(html.includes('noindex,nofollow'));assert.ok(html.includes('data-enter'));
 for(const file of ['entry','preview','scene','layout','architecture','environment','character','camera','collision','input','geometry','materials']){
 const code=readFileSync(`assets/js/urban-atlas/${file}.js`,'utf8');assert.ok(!code.includes('project-registry'));assert.ok(!code.includes('experience-controller'));assert.ok(!code.includes('missionProgress'));
 }
 assert.ok(existsSync('assets/js/vendor/THREE-LICENSE.txt'));assert.equal(Object.keys(layout.viewpoints).length,3);
});

test('unobstructed camera stays outside the character at every review viewpoint',()=>{
 for(const view of Object.values(layout.viewpoints)){
   const follow=createFollowCamera(),player=new Group();player.position.set(view.x,.12,view.z);
   for(let i=0;i<30;i++)follow.update(player,view,[],1/60,false);
   assert.ok(follow.camera.position.distanceTo(player.position)>7);
 }
});
test('vaulted roof has outward upper and lower surface normals',()=>{
 const g=shellRoof(29,5.6,2.1),n=g.getAttribute('normal');
 assert.ok(n.getY(16)>0);assert.ok(n.getY(82)<0);g.dispose();
});

test('actual authored district has safe viewpoints and walkable routes between them',()=>{
 // Only text-canvas drawing is stubbed; real geometry, layout and collision data run.
 const previous=globalThis.document;globalThis.document={createElement:()=>({width:0,height:0,getContext:()=>({fillRect(){},fillText(){}})})};
 const district=createDistrict();globalThis.document=previous;
 const obstacles=district.obstacles;
 for(const view of Object.values(layout.viewpoints))assert.equal(blocked(view.x,view.z,obstacles),false);
 const queue=[[layout.spawn.x,layout.spawn.z]],seen=new Set();let head=0;
 while(head<queue.length){const [x,z]=queue[head++],key=x+','+z;if(seen.has(key)||blocked(x,z,obstacles))continue;seen.add(key);for(const [dx,dz]of[[1,0],[-1,0],[0,1],[0,-1]])if(Math.abs(x+dx)<44&&Math.abs(z+dz)<44)queue.push([x+dx,z+dz]);}
 for(const view of Object.values(layout.viewpoints))assert.ok(seen.has(view.x+','+view.z));
 district.dispose();
});

test('feet follow paving and the rising station access ramp',()=>{
 assert.equal(groundHeight(0,28),.24);assert.equal(groundHeight(20,27),.24,'new park loop');
 assert.equal(groundHeight(-23,7),.24);assert.equal(groundHeight(-23,6),.38);
 assert.equal(groundHeight(-23,5),.52);
});
