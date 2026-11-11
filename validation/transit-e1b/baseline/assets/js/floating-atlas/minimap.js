import{terrainInfo}from'./terrain.js?v=73';
import{routes,areas}from'./plan.js?v=73';
export function drawAtlasMap(canvas,position,obstacles,yaw,{people=[]}={}){
 if(!position)return;const c=canvas.getContext('2d'),size=canvas.width,k=size/216;c.clearRect(0,0,size,size);c.save();c.beginPath();c.arc(size/2,size/2,size/2,0,Math.PI*2);c.clip();c.fillStyle='#284b53';c.fillRect(0,0,size,size);c.translate(size/2,size/2);c.scale(k,k);
 c.beginPath();terrainInfo.boundary.forEach(([x,z],i)=>i?c.lineTo(x,z):c.moveTo(x,z));c.closePath();c.fillStyle='#687e53';c.fill();c.strokeStyle='#b5b88b';c.lineWidth=1;c.stroke();
 c.strokeStyle='#d2c393';for(const route of routes){c.lineWidth=route.width*.55;c.beginPath();route.points.forEach(([x,z],i)=>i?c.lineTo(x,z):c.moveTo(x,z));c.stroke();}
 c.fillStyle='#c3b493';for(const o of obstacles)if(o.building&&!o.cameraOnly)c.fillRect(o.x-o.w/2,o.z-o.d/2,o.w,o.d);
 for(const a of Object.values(areas)){c.strokeStyle='#a6b69a';c.lineWidth=.6;c.beginPath();c.arc(a.x,a.z,2,0,Math.PI*2);c.stroke();}
 for(const p of people){c.fillStyle='#f6e6b5';c.beginPath();c.arc(p.x,p.z,1.4,0,Math.PI*2);c.fill();}
 c.save();c.translate(position.x,position.z);c.rotate(-yaw);c.fillStyle='#fff2c9';c.strokeStyle='#233b32';c.lineWidth=.8;c.beginPath();c.moveTo(0,-4);c.lineTo(2.7,2.7);c.lineTo(0,1.2);c.lineTo(-2.7,2.7);c.closePath();c.fill();c.stroke();c.restore();c.restore();
}
