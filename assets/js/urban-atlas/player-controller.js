import {slide,blocked} from './collision.js?v=40';
import {groundHeight} from './layout.js?v=40';
export const locomotion=Object.freeze({walkSpeed:2.1,runSpeed:4.6,walkClipSpeed:1.20,runClipSpeed:2.695});
export const jumpPhysics=Object.freeze({gravity:16.5,launchSpeed:6.2,launchDelay:.13,takeoffDuration:.23,landingDuration:.22,maxStep:.42,height:1.9});
// Physics owns world travel; pose displacement stays on the visual rig.
// Pause freezes integration, while mode handoff settles onto the current support.
export function createPlayerController(root,{heightAt=groundHeight,collision={slide,blocked},bounds=44,minY=-8,maxY=50,recoveryPoint={x:0,z:28},isSafe=()=>true}={}){
 const isBlocked=collision.blocked,move=collision.slide;
 let vx=0,vz=0,vy=0,grounded=true,phase='grounded',elapsed=0,jumps=0,landings=0,support=heightAt(root.position.x,root.position.z),safe={x:root.position.x,z:root.position.z};
 function settle(){vx=0;vz=0;vy=0;grounded=true;phase='grounded';elapsed=0;support=heightAt(root.position.x,root.position.z);root.position.y=support;}
 function recover(obstacles){if(!Number.isFinite(safe.x)||isBlocked(safe.x,safe.z,obstacles)||!isSafe(safe.x,safe.z))safe={...recoveryPoint};root.position.x=safe.x;root.position.z=safe.z;settle();}
 return {
  get grounded(){return grounded;},get phase(){return phase;},get verticalVelocity(){return vy;},get jumps(){return jumps;},get landings(){return landings;},get support(){return support;},
  update(delta,input,obstacles,{jump=false}={}){
   const dt=Math.min(.05,Math.max(0,Number.isFinite(delta)?delta:0));
   if(![root.position.x,root.position.y,root.position.z,vy].every(Number.isFinite)||root.position.y<minY||root.position.y>maxY||Math.abs(root.position.x)>bounds||Math.abs(root.position.z)>bounds)recover(obstacles);
   if(jump&&grounded&&phase==='grounded'){phase='takeoff';elapsed=0;jumps++;}
   const has=k=>input.keys.has(k)||input.touch.has(k);
   let x=Number(has('d')||has('arrowright'))-Number(has('a')||has('arrowleft')),z=Number(has('s')||has('arrowdown'))-Number(has('w')||has('arrowup'));
   const magnitude=Math.hypot(x,z)||1;x/=magnitude;z/=magnitude;
   const sprint=has('shift'),speed=sprint?locomotion.runSpeed:locomotion.walkSpeed,c=Math.cos(input.yaw),s=Math.sin(input.yaw),blend=1-Math.exp(-(grounded?13:8)*dt);
   vx+=((x*c+z*s)*speed-vx)*blend;vz+=((-x*s+z*c)*speed-vz)*blend;
   const oldX=root.position.x,oldZ=root.position.z,oldY=root.position.y,previousSupport=heightAt(oldX,oldZ);
   move(root.position,vx*dt,vz*dt,obstacles);support=heightAt(root.position.x,root.position.z);
   // Only small steps snap. A taller discontinuity cannot teleport the capsule up.
   if(support-oldY>jumpPhysics.maxStep){root.position.x=oldX;root.position.z=oldZ;support=previousSupport;vx=0;vz=0;}
   const actual=Math.hypot(root.position.x-oldX,root.position.z-oldZ)/Math.max(dt,.001);
   if(actual>.05){const target=Math.atan2(vx,vz),angle=Math.atan2(Math.sin(target-root.rotation.y),Math.cos(target-root.rotation.y));root.rotation.y+=angle*(1-Math.exp(-12*dt));}
   elapsed+=dt;
   let airborneDt=dt;
   if(phase==='takeoff'&&grounded&&elapsed>=jumpPhysics.launchDelay){grounded=false;vy=jumpPhysics.launchSpeed;airborneDt=elapsed-jumpPhysics.launchDelay;}
   if(grounded){
    if(previousSupport-support>jumpPhysics.maxStep){grounded=false;phase='airborne';vy=0;}
    else root.position.y=support;
   }
   if(!grounded){
    let nextY=root.position.y+vy*airborneDt-jumpPhysics.gravity*airborneDt*airborneDt/2;vy-=jumpPhysics.gravity*airborneDt;
    // Thin overhead roofs are cameraOnly for walking, but solid to an ascending head.
    for(const o of obstacles){if(!Number.isFinite(o.minY))continue;const under=Math.abs(root.position.x-o.x)<o.w/2+.3&&Math.abs(root.position.z-o.z)<o.d/2+.3;if(under&&vy>0&&oldY+jumpPhysics.height<=o.minY+.02&&nextY+jumpPhysics.height>=o.minY){nextY=o.minY-jumpPhysics.height-.015;vy=0;}}
    root.position.y=nextY;
    if(vy<=0&&nextY<=support){root.position.y=support;vy=0;grounded=true;phase='landing';elapsed=0;landings++;}
    else if(phase==='takeoff'&&elapsed>=jumpPhysics.takeoffDuration)phase='airborne';
   }
   if(phase==='landing'&&elapsed>=jumpPhysics.landingDuration){phase='grounded';elapsed=0;}
   if(grounded&&!isBlocked(root.position.x,root.position.z,obstacles)&&isSafe(root.position.x,root.position.z))safe={x:root.position.x,z:root.position.z};
   return {speed:actual,running:sprint&&actual>locomotion.walkSpeed+.15,grounded,phase,verticalVelocity:vy,support,jumps,landings};
  },
  stop(){vx=0;vz=0;},settle,
 };
}
