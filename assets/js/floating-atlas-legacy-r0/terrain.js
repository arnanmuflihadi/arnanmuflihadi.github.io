import * as T from'../vendor/three-atlas.module.js?v=16';
import{outlineControls,areas,routes,streamPoints,pads}from'./plan.js?v=56';
const sectors=156,rings=44,TAU=Math.PI*2;
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
export function segmentPoint(x,z,a,b){const dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));return{distance:Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t),x:a[0]+dx*t,z:a[1]+dz*t,t,y:a[2]+(b[2]-a[2])*t};}
export function nearestPath(x,z){let best={distance:Infinity};for(const route of routes)for(let i=1;i<route.points.length;i++){const p=segmentPoint(x,z,route.points[i-1],route.points[i]);if(p.distance<best.distance)best={...p,width:route.width,id:route.id};}return best;}
function contour(t){const n=outlineControls.length,u=t*n,i=Math.floor(u)%n,f=u-Math.floor(u),p=outlineControls[(i+n-1)%n],a=outlineControls[i],b=outlineControls[(i+1)%n],q=outlineControls[(i+2)%n];return[0,1].map(k=>.5*((2*a[k])+(-p[k]+b[k])*f+(2*p[k]-5*a[k]+4*b[k]-q[k])*f*f+(-p[k]+3*a[k]-3*b[k]+q[k])*f*f*f));}
const boundary=Array.from({length:sectors},(_,i)=>contour(i/sectors));
// Sort by polar angle so support and mesh use the same convex sector wedges.
boundary.sort((a,b)=>(Math.atan2(a[1],a[0])+TAU)%TAU-(Math.atan2(b[1],b[0])+TAU)%TAU);
const angles=boundary.map(p=>(Math.atan2(p[1],p[0])+TAU)%TAU);
function sculpt(x,z){
 let y=8+17*Math.exp(-((x+34)**2/540+(z+28)**2/720))+7*Math.exp(-((x+3)**2/900+(z+52)**2/400))+3*Math.exp(-((x-30)**2/600+(z-7)**2/700));
 y+=.65*Math.sin(x*.09+z*.04)*Math.cos(z*.085);
 for(const a of Object.values(areas)){const d=Math.hypot((x-a.x)/a.rx,(z-a.z)/a.rz),blend=1-smooth(.62,1.2,d);y+=(a.y-y)*blend;}
 for(const p of pads){const dx=x-p.x,dz=z-p.z,c=Math.cos(p.rotation),s=Math.sin(p.rotation),u=Math.abs(dx*c-dz*s)-p.w/2,v=Math.abs(dx*s+dz*c)-p.d/2,blend=1-smooth(0,3.5,Math.max(u,v));y+=(p.y-y)*blend;}
 const p=nearestPath(x,z),blend=1-smooth(p.width*.5,p.width*.5+3.5,p.distance);y+=(p.y-y)*blend;
 for(let i=1;i<streamPoints.length;i++){const s=segmentPoint(x,z,streamPoints[i-1],streamPoints[i]);const w=1-smooth(1.1,3.3,s.distance);y+=(s.y-.16-y)*w;}
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
 for(let i=0;i<vertices.length;i++){const[x,y,z]=vertices[i],p=nearestPath(x,z),path=1-smooth(p.width*.35,p.width*.53,p.distance),c=new T.Color('#6f925d').lerp(new T.Color('#b2b779'),.36+.2*Math.sin(x*.055+z*.028)+.14*Math.cos(z*.07)),stone=new T.Color(p.id==='city'?'#cbbd9b':'#c2b591');c.lerp(new T.Color('#999e80'),(1-smooth(.48,.83,g.attributes.normal.getY(i)))*.86);c.lerp(stone,path);for(const pad of pads){const dx=x-pad.x,dz=z-pad.z,cs=Math.cos(pad.rotation),sn=Math.sin(pad.rotation),u=Math.abs(dx*cs-dz*sn),v=Math.abs(dx*sn+dz*cs),edge=Math.max(u-pad.w/2,v-pad.d/2,u+v-(pad.w+pad.d)/2+1.4);c.lerp(stone,(1-smooth(-.8,.12,edge))*.94);}colors.push(c.r,c.g,c.b);}
 g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.computeBoundingSphere();return g;
}
export function createCliffGeometry(){
 const points=[],colors=[],idx=[],levels=[{s:1,y:0},{s:1.015,y:-3},{s:.91,y:-12},{s:.85,y:-21},{s:.62,y:-34},{s:.38,y:-45},{s:.02,y:-54}],palette=['#9b9c7c','#a39d80','#818978','#7a8174','#697a76','#5b7274','#5b737a'];
 for(let r=0;r<levels.length;r++)for(let i=0;i<sectors;i++){const[x,z]=boundary[i],a=i/sectors*TAU,l=levels[r],jag=r===0?0:Math.sin(i*1.7+r*.9)*(.4+r*.28),top=vertices[at(rings,i)][1],wave=Math.sin(a*3+.5)*3.5+Math.sin(a*7+1)*1.6,y=r===0?top:r===1?top-4+wave*.25:top*Math.max(0,1-r/5)+levels[r].y+wave*(r<6?1:.25),s=l.s*(r>1?1+Math.sin(a*3+1)*.16+Math.sin(a*7)*.06:1);points.push(x*s-7*r/6,y+jag,z*s+5*r/6);const c=new T.Color(palette[r]).multiplyScalar(.96+Math.sin(i*.38)*.08+Math.sin(i*1.31)*.035);colors.push(c.r,c.g,c.b);}
 for(let r=0;r<levels.length-1;r++)for(let i=0;i<sectors;i++){const a=r*sectors+i,b=r*sectors+(i+1)%sectors,c=a+sectors,d=b+sectors;idx.push(a,b,c,b,d,c);}
 const tip=points.length/3;points.push(-7,-55,5);const tipColor=new T.Color('#5b737a');colors.push(tipColor.r,tipColor.g,tipColor.b);for(let i=0;i<sectors;i++)idx.push((levels.length-1)*sectors+i,(levels.length-1)*sectors+(i+1)%sectors,tip);
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(points,3));g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.setIndex(idx);g.computeVertexNormals();return g;
}
export const terrainInfo={sectors,rings,vertices:vertices.length,triangles:indices.length/3,boundary,dimensions:{width:Math.max(...boundary.map(p=>p[0]))-Math.min(...boundary.map(p=>p[0])),depth:Math.max(...boundary.map(p=>p[1]))-Math.min(...boundary.map(p=>p[1])),surfaceMin:Math.min(...vertices.map(p=>p[1])),surfaceMax:Math.max(...vertices.map(p=>p[1])),undersideMin:-57}};
