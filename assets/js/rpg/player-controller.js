import * as T from '../vendor/three-rpg.module.js';
import {move} from './collision-system.js';
export function createPlayer(scene,spawn) {
  const group=new T.Group(),limbs=[];
  const material=color=>new T.MeshStandardMaterial({color,roughness:.85});
  const coat=material('#be365d'),skin=material('#d4a17f'),pants=material('#283b3c'),hair=material('#302d29');
  function part(w,h,d,x,y,z,mat,parent=group){const mesh=new T.Mesh(new T.BoxGeometry(w,h,d),mat);mesh.position.set(x,y,z);mesh.castShadow=true;parent.add(mesh);return mesh;}
  part(.65,.75,.36,0,1.15,0,coat);part(.4,.42,.4,0,1.78,0,skin);part(.44,.13,.43,0,2.01,0,hair);
  for(const side of [-1,1]){
    const leg=new T.Group();leg.position.set(side*.19,.83,0);group.add(leg);part(.24,.72,.28,0,-.36,0,pants,leg);part(.26,.13,.4,0,-.75,-.05,hair,leg);limbs.push(leg);
    const arm=new T.Group();arm.position.set(side*.45,1.48,0);group.add(arm);part(.19,.64,.22,0,-.3,0,coat,arm);limbs.push(arm);
  }
  group.position.set(spawn.x,0,spawn.z);scene.add(group);
  let vx=0,vz=0,phase=0;
  return {group,update(dt,input,obstacles,reduced){
    const has=k=>input.keys.has(k)||input.touch.has(k);
    let x=Number(has('d')||has('arrowright'))-Number(has('a')||has('arrowleft'));
    let z=Number(has('s')||has('arrowdown'))-Number(has('w')||has('arrowup'));
    const length=Math.hypot(x,z)||1;x/=length;z/=length;
    const speed=has('shift')?8:4.5,c=Math.cos(input.yaw),s=Math.sin(input.yaw),blend=1-Math.exp(-12*dt);
    vx+=((x*c+z*s)*speed-vx)*blend;vz+=((-x*s+z*c)*speed-vz)*blend;
    move(group.position,vx*dt,vz*dt,obstacles);
    const moving=Math.hypot(vx,vz)>.1;
    if(moving){const target=Math.atan2(vx,vz);const delta=Math.atan2(Math.sin(target-group.rotation.y),Math.cos(target-group.rotation.y));group.rotation.y+=delta*(1-Math.exp(-14*dt));}
    phase+=dt*(has('shift')?14:9);
    limbs.forEach((limb,i)=>limb.rotation.x=moving&&!reduced?Math.sin(phase+(i===0||i===3?0:Math.PI))*.55:0);
  },stop(){vx=0;vz=0;}};
}
