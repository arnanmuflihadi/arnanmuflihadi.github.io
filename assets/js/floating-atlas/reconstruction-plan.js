// One coordinated development town. Distances are metres; v points from arrival toward the civic court.
export const townPlan=Object.freeze({origin:[-1,47],heading:235*Math.PI/180,datum:15.2,grade:.02,square:{u:0,v:21,w:15,d:14},guild:{u:0,v:32,w:10,d:8},landing:{u:0,v:-7,r:6.5},buildings:[
 {id:'B1',name:'Kopi Awan',source:'B1_Kopi_Awan001',u:-8.3,v:6,w:8.55,d:7.2,old:[-8.3,1.202857142857,-10]},
 {id:'B2',name:'Lembaran',source:'B2_Lembaran_Shophouse001',u:8.3,v:6,w:7.9515,d:5.904,old:[8.3,1.394285714286,-11.2]},
 {id:'B3',name:'Rupa Rimba',source:'B3_Rupa_Rimba_Atelier001',u:-12,v:21,w:7.9515,d:7.992,old:[-8.3,3.12,-21.8]},
 {id:'B4',name:'Serambi',source:'B4_Serambi_Corner_Shop001',u:12,v:21,w:8.208,d:7.992,old:[8.3,3.12,-22.6]}
]});
export const forward=[Math.cos(townPlan.heading),Math.sin(townPlan.heading)],right=[-forward[1],forward[0]];
export const toWorld=(u,v)=>[townPlan.origin[0]+right[0]*u+forward[0]*(v-18),townPlan.origin[1]+right[1]*u+forward[1]*(v-18)];
export const toLocal=(x,z)=>{const dx=x-townPlan.origin[0],dz=z-townPlan.origin[1];return[dx*right[0]+dz*right[1],18+dx*forward[0]+dz*forward[1]];};
export const civicHeight=v=>townPlan.datum+townPlan.grade*Math.min(14,Math.max(-15,v));
export const buildingBase=p=>civicHeight(p.v)-.08;
export const footprintDistance=(u,v,p)=>Math.hypot(Math.max(0,Math.abs(u-p.u)-p.w/2),Math.max(0,Math.abs(v-p.v)-p.d/2));
const street={u:0,v:6,w:6,d:16};
const frontage=(u,v,margin)=>townPlan.buildings.some(b=>{const curb=Math.sign(b.u)*(b.v<14?3:7.5),face=b.u-Math.sign(b.u)*b.w/2;return footprintDistance(u,v,{u:(curb+face)/2,v:b.v,w:Math.abs(curb-face)+.1+margin*2,d:b.d+.3+margin*2})===0;});
export function publicArea(x,z,margin=0){const[u,v]=toLocal(x,z),p=townPlan;return frontage(u,v,margin)||footprintDistance(u,v,{...street,w:street.w+margin*2,d:street.d+margin*2})===0||footprintDistance(u,v,{...p.square,w:p.square.w+margin*2,d:p.square.d+margin*2})===0||footprintDistance(u,v,{...p.guild,w:p.guild.w+margin*2,d:p.guild.d+margin*2})===0||Math.hypot(u-p.landing.u,v-p.landing.v)<p.landing.r+margin||footprintDistance(u,v,{u:-6,v:11.6,w:6+margin*2,d:3.2+margin*2})===0||optionalDistance(x,z)<1.35+margin;}
export function inBuilding(x,z,margin=0){const[u,v]=toLocal(x,z);return townPlan.buildings.some(p=>footprintDistance(u,v,{...p,w:p.w+margin*2,d:p.d+margin*2})===0);}
export const mainRoute=[toWorld(0,-10),toWorld(0,-1),toWorld(0,10),toWorld(0,16),toWorld(-3.1,19),toWorld(-3.1,23),toWorld(0,27),toWorld(0,32)];
export const optionalTrail=[toWorld(7.5,28),toWorld(6.5,34),toWorld(18,34),[11,22]];
export function optionalDistance(x,z){let best=Infinity;for(let i=1;i<optionalTrail.length;i++){const a=optionalTrail[i-1],b=optionalTrail[i],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));best=Math.min(best,Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t));}return best;}
export const entryPoints=townPlan.buildings.map(p=>({id:p.id,point:toWorld(p.u-Math.sign(p.u)*(p.w/2+.65),p.v)}));
