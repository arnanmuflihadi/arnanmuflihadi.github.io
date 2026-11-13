import {district} from './district.js';
export function drawMinimap(canvas,position,yaw,progress) {
  const c=canvas.getContext('2d'),size=canvas.width,k=size/68;
  c.fillStyle='#e6e7d7';c.fillRect(0,0,size,size);c.save();c.translate(size/2,size/2);c.scale(k,k);
  c.fillStyle='#8e9c91';c.fillRect(-4,-32,8,64);c.fillRect(-32,-3.5,64,7);
  c.fillStyle='#adad9b';district.buildings.forEach(b=>c.fillRect(b.x-b.w/2,b.z-b.d/2,b.w,b.d));
  district.landmarks.forEach((l,i)=>{c.fillStyle=progress[l.projectId]?'#356956':'#b52d57';c.beginPath();c.arc(l.focus.x,l.focus.z,1.8,0,Math.PI*2);c.fill();c.fillStyle='#fff';c.font='2.7px sans-serif';c.textAlign='center';c.fillText(String(i+1),l.focus.x,l.focus.z+.9);});
  c.translate(position.x,position.z);c.rotate(-yaw);c.fillStyle='#1c3e3a';c.beginPath();c.moveTo(0,-2);c.lineTo(1.6,1.8);c.lineTo(0,1);c.lineTo(-1.6,1.8);c.closePath();c.fill();c.restore();
}
