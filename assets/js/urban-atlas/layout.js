import{parkPond,buildingPorches}from'./district-plan.js?v=40';
export const cityPlan=Object.freeze({northShift:11,plazaRadius:9.8});
export const contextBlocks=[];
export const layout=Object.freeze({bounds:44,spawn:{x:0,z:28},viewpoints:{
  plaza:{x:0,z:28,yaw:0,pitch:.19,name:'Taman Atlas · Arrival plaza'},
  station:{x:-23,z:9,yaw:.12,pitch:.16,name:'Stasiun Taman · Transit promenade'},
  commercial:{x:21,z:13,yaw:-.06,pitch:.08,name:'Menara Teras · Garden offices'},
}});
export const streets=Object.freeze([{id:'avenue',x:0,z:-12,w:74.5,d:6},{id:'secondary',x:0,z:-36,w:74.5,d:6},{id:'west',x:-40,z:0,w:5.5,d:88},{id:'east',x:40,z:0,w:5.5,d:88},{id:'neighborhood',x:-14,z:28,w:4.5,d:24}]);
export const sidewalks=[
  ...[-1,1].flatMap(s=>[{x:s*20.025,z:-17.5,w:34.45,d:5},{x:s*20.025,z:-8,w:34.45,d:2},{x:s*20.025,z:-40.5,w:34.45,d:3},{x:s*20.025,z:-31.5,w:34.45,d:3}]),
  ...[-1,1].flatMap(s=>[[-41.5,5],[-24,18],[17.5,53]].map(([z,d])=>({x:s*36.5,z,w:1.5,d}))),
  {x:0,z:-18.25,w:5.6,d:3.5},{x:0,z:-7.25,w:5.6,d:.5},{x:0,z:-41.25,w:5.6,d:1.5},{x:0,z:-30.75,w:5.6,d:1.5},
  {x:-18.25,z:27,w:3.5,d:26},{x:-10.25,z:28,w:3,d:24},
];
export const walks=[{x:0,z:-.5,w:6,d:13},{x:-20.75,z:10,w:29.5,d:6},{x:20.75,z:11,w:29.5,d:8},{x:0,z:28.5,w:7,d:21}];
export const frontageWalks=[{x:-30,z:11,w:12,d:12},{x:-18.25,z:14.5,w:3.5,d:3},{x:-10.25,z:14.5,w:3,d:3},{x:-6,z:28,w:7,d:3},{x:0,z:-25,w:5.6,d:10},{x:29,z:17,w:8,d:7},{x:13,z:21,w:16,d:2.5},{x:13,z:34,w:16,d:2.5},{x:6.25,z:27.5,w:2.5,d:13},{x:19.75,z:27.5,w:2.5,d:13},{x:4.25,z:21,w:3.5,d:2.5}];
export const curbRamps=[
  {x:0,z:-15.75,w:5.6,d:1.5,front:-15,rotation:0,base:.055,rise:.185},
  {x:0,z:-8.25,w:5.6,d:1.5,front:-9,rotation:Math.PI,base:.055,rise:.185},
  {x:0,z:-39.75,w:5.6,d:1.5,front:-39,rotation:0,base:.055,rise:.185},
  {x:0,z:-32.25,w:5.6,d:1.5,front:-33,rotation:Math.PI,base:.055,rise:.185},
  {axis:'x',x:-17,z:28,w:1.5,d:3,front:-16.25,rotation:Math.PI/2,base:.055,rise:.185},
  {axis:'x',x:-11,z:28,w:1.5,d:3,front:-11.75,rotation:-Math.PI/2,base:.055,rise:.185},
];
export const shopStoops=[];
export const treeSites=[[-10.5,18,1],[10.5,18,1],[-8,-4,.9],[9,-4,.85],[-18,-16.5,.85],[4,-19,.8],[18,-16.5,.85],[-34,6,.9],[-34,16,.8],[-26,6,.9],[-26,15,.75],[33,14,.9],[-9,35,.8],[9,35,.9],[32.5,-4,.85],[-33,-31.5,.8],[33,-31.5,.8],[11,26,1.05],[16,30,.9]];
export const palmSites=[[-18,10,8],[13,16,8.5],[-7,-2,7.5],[8,-3,8],[-33,3,7.5],[33,30,8]];
export const planterSites=[[-9,0],[33,6],[-33,18],[31,17]];
export const inRect=(x,z,r,padding=0)=>Math.abs(x-r.x)<=r.w/2+padding&&Math.abs(z-r.z)<=r.d/2+padding;
export const inRoad=(x,z,padding=0)=>streets.some(r=>inRect(x,z,r,padding));
const radius=cityPlan.plazaRadius,cy=10;
const arc=(a,b,n=16)=>Array.from({length:n+1},(_,i)=>[radius*Math.cos(a+(b-a)*i/n),cy+radius*Math.sin(a+(b-a)*i/n)]);
const north=Math.acos(3/radius),south=Math.acos(3.5/radius),shoulder=Math.asin(3/radius);
export const publicRealmOutline=[[-3,-7],[3,-7],...arc(-north,-shoulder),[35.5,7],[35.5,15],...arc(Math.asin(5/radius),south),[3.5,39],[-3.5,39],...arc(Math.PI-south,Math.PI-shoulder),[-35.5,13],[-35.5,7],...arc(Math.PI+shoulder,Math.PI+north)];
export function inPublicRealm(x,z){let inside=false;for(let i=0,j=publicRealmOutline.length-1;i<publicRealmOutline.length;j=i++){const a=publicRealmOutline[i],b=publicRealmOutline[j];if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside;}
export function groundHeight(x,z){
  if(x>-28&&x<-17&&z>38.4&&z<43.5)return .06;
  if(Math.abs(x+23)<=12.5&&Math.abs(z+1)<=6&&Math.abs(x+23)+Math.abs(z+1)<17.1)return .52;
  if(x>-27&&x<-19&&z>5&&z<7)return .24+(7-z)/2*.28;
  const px=Math.abs(x-29),pz=Math.abs(z-21);if(px<7&&pz<5.5&&px+pz<11.6)return .57;
  if(px<2.5&&z>=12.5&&z<=15.5)return Math.min(.57,.24+(z-12.5)/3*.33);
  for(const r of curbRamps)if(inRect(x,z,r))return r.base+r.rise*Math.abs((r.axis==='x'?x:z)-r.front)/(r.axis==='x'?r.w:r.d);
  for(const r of buildingPorches)if(inRect(x,z,r))return r.height;
  if(inRoad(x,z))return .055;
  if(inRect(x,z,parkPond))return -.02;
  if(inPublicRealm(x,z)||[...sidewalks,...walks,...frontageWalks].some(r=>inRect(x,z,r)))return .24;
  return -.02;
}
