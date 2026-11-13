import * as T from '../vendor/three-rpg.module.js';
export function createCamera() {
  const camera=new T.PerspectiveCamera(48,1,.1,150),ray=new T.Raycaster(),target=new T.Vector3(),desired=new T.Vector3(),direction=new T.Vector3(),origin=new T.Vector3();
  let first=true;
  return {camera,update(player,input,objects,dt,reduced=false){
    target.copy(player.position);target.y=1.5;
    const distance=9,vertical=3+input.pitch*7;
    desired.set(Math.sin(input.yaw)*distance,vertical,Math.cos(input.yaw)*distance).add(target);
    origin.copy(target);origin.y=.25;
    direction.copy(desired).sub(origin);const length=direction.length();direction.normalize();ray.set(origin,direction);ray.far=length;
    const hit=ray.intersectObjects(objects,false)[0];if(hit){
      desired.copy(origin).addScaledVector(direction,Math.max(.7,hit.distance-.45));
      // A tight wall must not push the camera inside the character.
      if(hit.distance<4){desired.copy(target);desired.y+=7;desired.z+=.01;}
    }
    camera.position.lerp(desired,first||reduced||hit?1:1-Math.exp(-9*dt));camera.lookAt(target);first=false;
  },reset(){first=true;}};
}
