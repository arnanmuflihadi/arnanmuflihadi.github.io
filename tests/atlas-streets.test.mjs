import test from 'node:test';
import assert from 'node:assert/strict';
import{createDistrict}from'../assets/js/urban-atlas/scene.js';
import{streets,sidewalks,walks,treeSites,palmSites,planterSites,shopStoops,publicRealmOutline,groundHeight,inRoad}from'../assets/js/urban-atlas/layout.js';
import{blocked,slide}from'../assets/js/urban-atlas/collision.js';
import{createPlayerController}from'../assets/js/urban-atlas/player-controller.js';
import{Group,Raycaster,Vector3}from'../assets/js/vendor/three-atlas.module.js?v=16';
function district(){const original=globalThis.document;try{globalThis.document={createElement:()=>({getContext:()=>({fillRect(){},fillText(){}})})};return createDistrict();}finally{globalThis.document=original;}}

test('carriageways contain no trees, planters, shop steps or static obstacles',()=>{
 for(const[x,z,s]of treeSites)assert.equal(inRoad(x,z,1.2*s),false,`tree pit ${x},${z}`);
 for(const[x,z]of palmSites)assert.equal(inRoad(x,z,.4),false,`palm ${x},${z}`);
 for(const[x,z]of planterSites)assert.equal(inRoad(x,z,.65),false,`planter ${x},${z}`);
 for(const[x,z,w,d]of shopStoops)for(const sx of[-1,1])for(const sz of[-1,1])assert.equal(inRoad(x+sx*w/2,z+sz*d/2),false,'shop threshold');
 const d=district();try{for(const r of streets)for(let x=r.x-r.w/2+.4;x<r.x+r.w/2-.4;x+=.5)for(let z=r.z-r.d/2+.4;z<r.z+r.d/2-.4;z+=.5)assert.equal(blocked(x,z,d.obstacles),false,`road ${x},${z}`);}finally{d.dispose();}
});

test('north sidewalk and curb ramps form a continuous walkable research approach',()=>{
 const d=district();try{
  const p={x:-35,z:-17.9};for(let i=0;i<700;i++)slide(p,.1,0,d.obstacles);assert.ok(p.x>34.9,'north footway crosses the full block');
  for(const x of[-36.5,36.5])for(let z=-42;z<=42;z+=.25)assert.equal(blocked(x,z,d.obstacles),false,`side footway ${x},${z}`);
  for(let x=-35;x<=35;x+=.25)assert.equal(blocked(x,-8,d.obstacles),false,`south footway ${x},-8`);
  const root=new Group();root.position.set(0,groundHeight(0,-7.2),-7.2);const motion=createPlayerController(root),input={keys:new Set(['w']),touch:new Set(),yaw:0};
  let highStep=0,last=root.position.y;for(let i=0;i<400&&root.position.z>-20.7;i++){motion.update(.02,input,d.obstacles);highStep=Math.max(highStep,Math.abs(root.position.y-last));last=root.position.y;}
  assert.ok(root.position.z<-20.5);assert.ok(highStep<.03,`ramp discontinuity ${highStep}`);assert.equal(motion.jumps,0);assert.equal(motion.grounded,true);
 }finally{d.dispose();}
});

test('rendered shared paving matches support height and never bridges the carriageway',()=>{
 const d=district(),ray=new Raycaster();try{
  const samples=[[0,-23],[-18,-15.4],[-40,-23],[40,-23],[0,-27],[0,-19],[-23,6],[21,13],[0,28],[5,14]];
  for(const[x,z]of samples){ray.set(new Vector3(x,1,z),new Vector3(0,-1,0));const hits=ray.intersectObjects(d.scene.children,true).filter(h=>h.point.y<=.6);assert.ok(hits.length,`${x},${z}`);assert.ok(Math.abs(hits[0].point.y-groundHeight(x,z))<.035,`${x},${z}: rendered ${hits[0].point.y}, support ${groundHeight(x,z)}`);}
  assert.ok(publicRealmOutline.length>50);assert.equal(sidewalks.length,20);assert.equal(walks.length,4);
 }finally{d.dispose();}
});
