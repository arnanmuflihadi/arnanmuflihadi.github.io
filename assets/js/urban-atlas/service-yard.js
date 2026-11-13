import * as T from '../vendor/three-atlas.module.js?v=16';
import{createBuilder}from'./geometry.js?v=22';import{questPlaces}from'./quest-state.js?v=22';
export function createServiceYard(scene,materials){
  const b=createBuilder(scene,materials);
  // A neglected maintenance court behind the studios, separated from public uses.
  for(let x=-26;x<=-12;x+=2)for(let z=36;z<=42;z+=2)b.box(x,.015,z,1.88,.07,1.88,(x+z)%4?'#a5ad8d':'#b6b69d');
  for(const[x,z]of[[-27,37],[-27,41],[-14,42],[-25,35.8]]){b.box(x,.25,z,.5,.5,1.5,'#8e9580');b.ball(x,.5,z,.7,.45,.65,'#69885b');}
  for(const[x,z]of[[-26,42],[-26,36],[-16,42],[-14,36]])for(let i=0;i<4;i++){const leaf=b.mesh(new T.ConeGeometry(.25,1.1,5),'#69885b',x+Math.sin(i)*.3,.5,z+Math.cos(i)*.3);leaf.rotation.z=Math.sin(i)*.5;}
  b.column(-10.5,.85,35,.08,1.7,'#627064');
  const c=document.createElement('canvas');c.width=512;c.height=220;const ctx=c.getContext('2d');ctx.fillStyle='#304d3c';ctx.fillRect(0,0,512,220);ctx.fillStyle='#f8eacb';ctx.textAlign='center';ctx.font='500 36px sans-serif';ctx.fillText('OLD SERVICE YARD',256,66);ctx.font='24px sans-serif';ctx.fillText('Optional fictional encounter',256,122);ctx.fillText('Research is always open',256,162);
  const texture=new T.CanvasTexture(c);texture.colorSpace=T.SRGBColorSpace;
  const sign=new T.Mesh(new T.PlaneGeometry(3.3,1.4),new T.MeshBasicMaterial({map:texture,side:T.DoubleSide}));sign.position.set(-10.5,1.8,35);scene.add(sign);
  const device=new T.Group();device.position.set(questPlaces.device.x,.08,questPlaces.device.z);scene.add(device);
  const box=new T.Mesh(new T.BoxGeometry(.6,.4,.45),materials.toon('#cfac66'));box.position.y=.5;device.add(box);
  const aerial=new T.Mesh(new T.CylinderGeometry(.025,.025,.8,6),materials.toon('#38584b'));aerial.position.set(.15,1,0);device.add(aerial);
  const beacon=new T.Mesh(new T.TorusGeometry(.5,.035,5,32),new T.MeshBasicMaterial({color:'#dcb65c'}));beacon.rotation.x=Math.PI/2;beacon.position.y=1.5;device.add(beacon);device.visible=false;
  const telegraph=new T.Mesh(new T.TorusGeometry(2.65,.055,5,64),new T.MeshBasicMaterial({color:'#d39a41',transparent:true,opacity:.8,depthWrite:false}));telegraph.rotation.x=Math.PI/2;telegraph.visible=false;scene.add(telegraph);
  b.flush();
  return{device,telegraph,update(enemy,phase,time,reduced){device.visible=phase==='device-ready';if(device.visible&&!reduced)beacon.rotation.z=time*.5;telegraph.visible=enemy.health>0&&enemy.state==='Attack';telegraph.position.set(enemy.x,.085,enemy.z);if(telegraph.visible){const scale=.65+Math.min(1,enemy.elapsed/.85)*.35;telegraph.scale.setScalar(scale);telegraph.material.color.set(enemy.elapsed<.7?'#d39a41':'#b95746');}},};
}
