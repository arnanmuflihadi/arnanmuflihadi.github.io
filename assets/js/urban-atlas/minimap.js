import{landmarks}from'./presentation.js?v=40';
import{streets,sidewalks,frontageWalks,publicRealmOutline,treeSites}from'./layout.js?v=40';
export function drawAtlasMap(canvas,position,obstacles,yaw,{marker,people=[]}={}){
  if(!position)return;
  const c=canvas.getContext('2d'),size=canvas.width,k=size/102;
  c.clearRect(0,0,size,size);c.save();c.beginPath();c.arc(size/2,size/2,size/2,0,Math.PI*2);c.clip();
  c.fillStyle='#283d32';c.fillRect(0,0,size,size);c.translate(size/2,size/2);c.scale(k,k);
  c.strokeStyle='#415442';c.lineWidth=.2;
  for(let i=-50;i<=50;i+=10){c.beginPath();c.moveTo(i,-50);c.lineTo(i,50);c.moveTo(-50,i);c.lineTo(50,i);c.stroke();}
  c.fillStyle='#162922';for(const r of streets)c.fillRect(r.x-r.w/2,r.z-r.d/2,r.w,r.d);
  c.fillStyle='#62745c';for(const r of[...sidewalks,...frontageWalks])c.fillRect(r.x-r.w/2,r.z-r.d/2,r.w,r.d);
  c.beginPath();publicRealmOutline.forEach(([x,z],i)=>i?c.lineTo(x,z):c.moveTo(x,z));c.closePath();c.fill();
  c.fillStyle='#96a185';for(const b of obstacles)if(!b.cameraOnly&&b.w>3&&b.d>3)c.fillRect(b.x-b.w/2,b.z-b.d/2,b.w,b.d);
  c.fillStyle='#3c593e';for(const[x,z,s]of treeSites){c.beginPath();c.arc(x,z,2*s,0,Math.PI*2);c.fill();}
  landmarks.forEach((l,i)=>{c.fillStyle='#dfaa70';c.beginPath();c.arc(l.x,l.z,2.3,0,Math.PI*2);c.fill();c.fillStyle='#172b24';c.font='bold 3.2px sans-serif';c.textAlign='center';c.fillText(String(i+1),l.x,l.z+1.1);});
  for(const p of people){c.fillStyle=p.selected?'#f6d98b':'#d5ddba';c.beginPath();c.arc(p.x,p.z,p.selected?1.5:.8,0,Math.PI*2);c.fill();}
  if(marker){c.fillStyle='#f4d085';c.beginPath();c.moveTo(marker.x,marker.z-2.8);c.lineTo(marker.x+2,marker.z);c.lineTo(marker.x,marker.z+2.8);c.lineTo(marker.x-2,marker.z);c.closePath();c.fill();}
  c.save();c.translate(position.x,position.z);c.rotate(-yaw);c.strokeStyle='#172b24';c.lineWidth=.7;c.fillStyle='#fff5cf';c.beginPath();c.moveTo(0,-3.2);c.lineTo(2.1,2.2);c.lineTo(0,1);c.lineTo(-2.1,2.2);c.closePath();c.fill();c.stroke();c.restore();c.restore();
}
