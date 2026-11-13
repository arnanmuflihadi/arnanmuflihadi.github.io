import * as T from'../vendor/three-atlas.module.js?v=16';
import{outlineControls,areas,routes,streamPoints}from'./plan.js?v=63';
const sectors=208,rings=64,TAU=Math.PI*2;
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
export function segmentPoint(x,z,a,b){const dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));return{distance:Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t),x:a[0]+dx*t,z:a[1]+dz*t,t,y:a[2]+(b[2]-a[2])*t};}
export function nearestPath(x,z){let best={distance:Infinity};for(const route of routes)for(let i=1;i<route.points.length;i++){const p=segmentPoint(x,z,route.points[i-1],route.points[i]);if(p.distance<best.distance)best={...p,width:route.width,id:route.id};}return best;}
function contour(t){const n=outlineControls.length,u=t*n,i=Math.floor(u)%n,f=u-Math.floor(u),p=outlineControls[(i+n-1)%n],a=outlineControls[i],b=outlineControls[(i+1)%n],q=outlineControls[(i+2)%n];return[0,1].map(k=>.5*((2*a[k])+(-p[k]+b[k])*f+(2*p[k]-5*a[k]+4*b[k]-q[k])*f*f+(-p[k]+3*a[k]-3*b[k]+q[k])*f*f*f));}
const boundary=Array.from({length:sectors},(_,i)=>contour(i/sectors));
// Sort by polar angle so support and mesh use the same convex sector wedges.
boundary.sort((a,b)=>(Math.atan2(a[1],a[0])+TAU)%TAU-(Math.atan2(b[1],b[0])+TAU)%TAU);
const angles=boundary.map(p=>(Math.atan2(p[1],p[0])+TAU)%TAU);
function sculpt(x,z){
 let y=15+35*Math.exp(-((x+43)**2/700+(z+47)**2/1450))+16*Math.exp(-((x+66)**2/350+(z+2)**2/1250))+18*Math.exp(-((x-38)**2/950+(z+29)**2/650))+9*Math.exp(-((x+6)**2/600+(z+78)**2/250));
 y-=2*Math.exp(-((x+2)**2/180+(z-9)**2/1200));
 y+=1.8*Math.sin(x*.085+z*.025)*Math.cos(z*.073)+.55*Math.sin(x*.23+z*.17);
 for(const a of Object.values(areas)){const d=Math.hypot((x-a.x)/a.rx,(z-a.z)/a.rz),blend=1-smooth(.32,1.35,d);y+=(a.y-y)*blend;}
 for(let i=1;i<streamPoints.length;i++){const s=segmentPoint(x,z,streamPoints[i-1],streamPoints[i]);const w=1-smooth(.85,3.4,s.distance);y+=(s.y-.22-y)*w;}
 const p=nearestPath(x,z),blend=1-smooth(p.width*.42,p.width*.5+7,p.distance);y+=(p.y-y)*blend;
 return y;
}
const vertices=[[0,sculpt(0,0),0]];
for(let r=1;r<=rings;r++)for(let i=0;i<sectors;i++){const t=r/rings,x=boundary[i][0]*t,z=boundary[i][1]*t;vertices.push([x,sculpt(x,z),z]);}
const at=(r,i)=>r===0?0:1+(r-1)*sectors+(i+sectors)%sectors;
const indices=[];for(let i=0;i<sectors;i++)indices.push(0,at(1,i+1),at(1,i));
for(let r=1;r<rings;r++)for(let i=0;i<sectors;i++)indices.push(at(r,i),at(r,i+1),at(r+1,i),at(r,i+1),at(r+1,i+1),at(r+1,i));
function bary(x,z,a,b,c){const v0x=b[0]-a[0],v0z=b[2]-a[2],v1x=c[0]-a[0],v1z=c[2]-a[2],d=v0x*v1z-v1x*v0z;if(Math.abs(d)<1e-9)return null;const u=((x-a[0])*v1z-v1x*(z-a[2]))/d,v=(v0x*(z-a[2])-(x-a[0])*v0z)/d;return{u,v,w:1-u-v,y:a[1]+(b[1]-a[1])*u+(c[1]-a[1])*v};}
function sectorAt(x,z){let angle=(Math.atan2(z,x)+TAU)%TAU,lo=0,hi=angles.length;while(lo<hi){const m=(lo+hi)>>1;if(angles[m]<=angle)lo=m+1;else hi=m;}return(lo+sectors-1)%sectors;}
export function terrainSample(x,z){
 if(!Number.isFinite(x+z))return{height:-500,fraction:Infinity};if(Math.hypot(x,z)<1e-7)return{height:vertices[0][1],fraction:0};
 const i=sectorAt(x,z),b=boundary[i],c=boundary[(i+1)%sectors],w=bary(x,z,[0,0,0],[b[0],0,b[1]],[c[0],0,c[1]]),s=w.u+w.v;if(s>1.0000001||w.u<-.000001||w.v<-.000001)return{height:-500,fraction:s};
 const r=Math.min(rings-1,Math.floor(Math.max(0,s)*rings));let a;
 if(r===0)a=bary(x,z,vertices[0],vertices[at(1,i+1)],vertices[at(1,i)]);
 else{a=bary(x,z,vertices[at(r,i)],vertices[at(r,i+1)],vertices[at(r+1,i)]);if(a.u<-.000001||a.v<-.000001||a.w<-.000001)a=bary(x,z,vertices[at(r,i+1)],vertices[at(r+1,i+1)],vertices[at(r+1,i)]);}
 return{height:a.y,fraction:s};
}
export const groundHeight=(x,z)=>terrainSample(x,z).height;
export const safeGround=(x,z)=>{const p=terrainSample(x,z);return p.height>0&&p.fraction<.93;};
export function createTerrainGeometry(){
 const g=new T.BufferGeometry(),colors=[];
 g.setAttribute('position',new T.Float32BufferAttribute(vertices.flat(),3));g.setIndex(indices);g.computeVertexNormals();
 for(let i=0;i<vertices.length;i++){
  const[x,y,z]=vertices[i],p=nearestPath(x,z),normal=g.attributes.normal.getY(i),patch=.5+.25*Math.sin(x*.07+z*.041)+.18*Math.cos(z*.1-x*.03),path=1-smooth(p.width*.24,p.width*.54,p.distance);
  const c=new T.Color('#376b3e').lerp(new T.Color('#74974b'),patch),rock=new T.Color('#93998b').lerp(new T.Color('#b4aa8b'),.5+.35*Math.sin(y*.7));
  c.lerp(new T.Color('#a6ae65'),smooth(32,50,y)*.35);c.lerp(rock,(1-smooth(.53,.89,normal))*.96);
  c.lerp(new T.Color('#8d825e'),(1-smooth(p.width*.5,p.width*.8,p.distance))*.25);c.lerp(new T.Color('#b8a17b'),path*.93);
  colors.push(c.r,c.g,c.b);
 }
 g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.computeBoundingSphere();return g;
}
export function createCliffGeometry(){
 const points=[],colors=[],idx=[],levels=[{s:1,y:0},{s:1.006,y:-3},{s:.94,y:-10},{s:.97,y:-14},{s:.82,y:-27},{s:.84,y:-31},{s:.65,y:-44},{s:.56,y:-52},{s:.38,y:-64},{s:.2,y:-74},{s:.025,y:-83}],palette=['#8e9276','#b0a58b','#969789','#afa38a','#7c8982','#a49d87','#6c827e','#84938a','#64817f','#5d7a7e','#54767c'];
 for(let r=0;r<levels.length;r++)for(let i=0;i<sectors;i++){
  const[x,z]=boundary[i],a=i/sectors*TAU,l=levels[r],top=vertices[at(rings,i)][1],flute=Math.sin(a*13+.8)+Math.sin(a*23)*.35;
  const wave=Math.sin(a*3+.5)*5+Math.sin(a*7+1)*3+flute*1.6,jag=r===0?0:Math.sin(i*.72+r*.7)*(.25+r*.13),y=r===0?top:top*Math.max(0,1-r/7)+l.y+wave*(r<9?1:.25)+jag;
  const s=l.s*(r>1?1+Math.sin(a*3+1)*.16+Math.sin(a*7)*.06+flute*.045:1);points.push(x*s-12*r/10,y,z*s+7*r/10);
  const c=new T.Color(palette[r]).multiplyScalar(.95+Math.sin(i*.17)*.07+Math.sin(i*.71+r)*.035);colors.push(c.r,c.g,c.b);
 }
 for(let r=0;r<levels.length-1;r++)for(let i=0;i<sectors;i++){const a=r*sectors+i,b=r*sectors+(i+1)%sectors,c=a+sectors,d=b+sectors;idx.push(a,b,c,b,d,c);}
 const tip=points.length/3;points.push(-12,-85,7);const tipColor=new T.Color('#54767c');colors.push(tipColor.r,tipColor.g,tipColor.b);for(let i=0;i<sectors;i++)idx.push((levels.length-1)*sectors+i,(levels.length-1)*sectors+(i+1)%sectors,tip);
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(points,3));g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.setIndex(idx);g.computeVertexNormals();return g;
}
export const terrainInfo={sectors,rings,vertices:vertices.length,triangles:indices.length/3,boundary,dimensions:{width:Math.max(...boundary.map(p=>p[0]))-Math.min(...boundary.map(p=>p[0])),depth:Math.max(...boundary.map(p=>p[1]))-Math.min(...boundary.map(p=>p[1])),surfaceMin:Math.min(...vertices.map(p=>p[1])),surfaceMax:Math.max(...vertices.map(p=>p[1])),undersideMin:-85}};
