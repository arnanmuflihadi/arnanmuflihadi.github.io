import {Vector3} from '../vendor/three-atlas.module.js?v=16';
import {clearDistance} from './collision.js?v=22';
// Project head anchors into HTML for crisp type, capped at two unoccluded labels.
export function createNameplates(host,obstacles){
 const layer=document.createElement('div');layer.className='atlas-nameplates';layer.setAttribute('aria-label','Nearby fictional guides');host.append(layer);
 const labels=new Map(),head=new Vector3(),direction=new Vector3();let age=0;
 return {update(dt,camera,people,player,project,enabled){
  age+=dt;if(age<.08)return;age=0;const occupied=[];
  for(const label of labels.values())label.hidden=true;
  if(!enabled||!player)return;
  const width=host.clientWidth,height=host.clientHeight;
  const candidates=people.map(p=>({...p,distance:Math.hypot(p.actor.root.position.x-player.x,p.actor.root.position.z-player.z)})).filter(p=>p.distance<10||(p.spec.study===project&&p.distance<18)).sort((a,b)=>Number(b.spec.study===project)-Number(a.spec.study===project)||a.distance-b.distance);
  for(const person of candidates){
   const {spec,actor}=person;head.copy(actor.root.position);head.y+=spec.height+.48;
   direction.subVectors(head,camera.position);const distance=direction.length();direction.normalize();if(clearDistance(camera.position,head,obstacles,.02)<distance-.25)continue;
   head.project(camera);if(head.z< -1||head.z>1||Math.abs(head.x)>.85||Math.abs(head.y)>.88)continue;
   const x=(head.x*.5+.5)*width,y=(-head.y*.5+.5)*height,half=(width<700?180:208)/2,plateX=Math.max(half+8,Math.min(width-half-8,x));
   if(occupied.some(p=>Math.abs(p.x-plateX)<216&&Math.abs(p.y-y)<66))continue;
   let label=labels.get(spec.id);if(!label){label=document.createElement('div');label.className='atlas-nameplate';label.dataset.npc=spec.id;const name=document.createElement('strong'),role=document.createElement('span');name.textContent=spec.name;role.textContent=spec.role;label.append(name,role);layer.append(label);labels.set(spec.id,label);}
   label.hidden=false;label.dataset.selected=String(spec.study===project);label.style.transform=`translate(${Math.round(plateX)}px,${Math.round(y)}px) translate(-50%,-100%)`;occupied.push({x:plateX,y});if(occupied.length===2)break;
  }
 },dispose(){layer.remove();labels.clear();}};
}
