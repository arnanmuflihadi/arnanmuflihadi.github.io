import{clearDistance as solidClearance}from'../urban-atlas/collision.js?v=40';
import{worldHeight as groundHeight,safePosition as safeGround}from'./support.js?v=73';
import{spawn}from'./plan.js?v=73';
export function blocked(x,z,obstacles,radius=.34){return Math.abs(x)>105||Math.abs(z)>105||obstacles.some(o=>{if(o.cameraOnly)return false;const dx=x-o.x,dz=z-o.z;if(o.oriented){const c=Math.cos(o.oriented.rotation),s=Math.sin(o.oriented.rotation);return Math.abs(dx*c-dz*s)<o.oriented.w/2+radius&&Math.abs(dx*s+dz*c)<o.oriented.d/2+radius;}return Math.abs(dx)<o.w/2+radius&&Math.abs(dz)<o.d/2+radius;});}
export function slide(p,dx,dz,obstacles){const n=Math.max(1,Math.ceil(Math.max(Math.abs(dx),Math.abs(dz))/.1));for(let i=0;i<n;i++){if(!blocked(p.x+dx/n,p.z,obstacles))p.x+=dx/n;if(!blocked(p.x,p.z+dz/n,obstacles))p.z+=dz/n;}}
export function clearDistance(a,b,obstacles,padding=.28){const length=Math.hypot(b.x-a.x,b.y-a.y,b.z-a.z);let clear=solidClearance(a,b,obstacles,padding);const n=Math.max(8,Math.ceil(length/.25));for(let i=1;i<=n;i++){const t=i/n,x=a.x+(b.x-a.x)*t,y=a.y+(b.y-a.y)*t,z=a.z+(b.z-a.z)*t;if(groundHeight(x,z)+.35>y){clear=Math.min(clear,length*(i-1)/n);break;}}return clear;}
export const movementOptions={heightAt:groundHeight,collision:{blocked,slide},bounds:105,minY:-100,maxY:130,recoveryPoint:spawn,isSafe:safeGround};
