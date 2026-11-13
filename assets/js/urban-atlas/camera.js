import * as T from '../vendor/three-atlas.module.js?v=16';
import {clearDistance} from './collision.js?v=40';
export function createFollowCamera({clearance=clearDistance,distance:followDistance=11.8}={}) {
  const camera=new T.PerspectiveCamera(60,1,.12,460),desired=new T.Vector3(),origin=new T.Vector3(),target=new T.Vector3();
  let distance=followDistance,first=true,followY=null;
  return {camera,handoff(){first=false;distance=followDistance;},reset(){first=true;distance=followDistance;followY=null;},update(player,input,obstacles,dt,reduced,localDistance=followDistance){
    followY=followY===null?player.position.y:followY+(player.position.y-followY)*(1-Math.exp(-7*dt));
    origin.copy(player.position);origin.y+=1.25;
    desired.set(player.position.x+Math.sin(input.yaw)*localDistance,followY+6.6*(localDistance/followDistance)+input.pitch*3,player.position.z+Math.cos(input.yaw)*localDistance);
    const length=origin.distanceTo(desired),clear=clearance(origin,desired,obstacles);
    const available=Math.max(.8,clear-.28),wanted=Math.min(length,available);
    // Fast inward movement protects against clipping; slow outward recovery avoids pops.
    distance=first?wanted:distance+(wanted-distance)*(1-Math.exp(-(wanted<distance?32:4)*dt));
    distance=Math.min(distance,available);
    desired.sub(origin).normalize().multiplyScalar(distance).add(origin);
    // Tight obstruction: smoothly gain elevation rather than snap to a top-down camera.
    const lift=localDistance<followDistance?0:Math.max(0,2.8-distance)*1.9;
    desired.y+=lift;
    target.copy(player.position);target.y=followY+2.1-Math.min(1,lift*.35);
    camera.position.lerp(desired,first||reduced?1:1-Math.exp(-11*dt));
    // Guard the interpolated position, including after a corner or fast turn.
    const safe=clearance(origin,camera.position,obstacles);
    if(safe<origin.distanceTo(camera.position)-.001){
      const direction=camera.position.clone().sub(origin).normalize();
      camera.position.copy(origin).addScaledVector(direction,Math.max(.5,safe-.2));
    }
    camera.lookAt(target);first=false;
  }};
}
