import * as T from'../vendor/three-atlas.module.js?v=16';
import{leafRibbon}from'../urban-atlas/geometry.js?v=22';
import{groundHeight,terrainSample,nearestPath,terrainInfo}from'./terrain.js?v=63';
import{treeGroves,areas}from'./plan.js?v=63';

const hash=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);};
export function chiselRock(seed=0){
 const g=new T.SphereGeometry(1,9,5),p=g.attributes.position;
 for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i),f=1+.12*Math.sin(x*7+z*4+seed)+.07*Math.sin(y*9+seed);p.setXYZ(i,x*f+Math.max(0,y)*.12,Math.round(y*7)/7,z*f);}
 g.computeVertexNormals();return g;
}
export async function dressLandscape({scene,b,standard,library,obstacles,stats,ownedMaterials,signal}){
 const batches=new Map(),finishes=new Map(),wind={value:0};
 function batch(root,kind,variant){root.updateMatrixWorld(true);root.traverse(o=>{
  if(!o.isMesh)return;const source=o.material,key=source.uuid+':'+variant;
  if(!finishes.has(key)){const m=source.clone();m.vertexColors=false;m.roughness=.97;
   if(/leaves|foliage|leaf/i.test(m.name)){m.color.set(['#c8d59b','#aaca9f','#d6dc9f'][variant%3]);m.emissive.set('#7d9864');m.emissiveIntensity=.28;if(m.aoMap)m.aoMapIntensity=.1;}
   else{m.color.set('#c1b699');m.emissive.set('#84694b');m.emissiveIntensity=.14;}finishes.set(key,m);ownedMaterials.add(m);
  }
  const m=finishes.get(key),k=kind+o.geometry.uuid+m.uuid;if(!batches.has(k))batches.set(k,{geometry:o.geometry,material:m,transforms:[],kind});batches.get(k).transforms.push(o.matrixWorld.clone());
 });}
 const clear=(x,z,margin)=>{const p=nearestPath(x,z);return terrainSample(x,z).fraction<.94&&p.distance>p.width/2+margin&&!Object.values(areas).some(a=>Math.hypot(x-a.x,z-a.z)<(a===areas.highlands?4:6));};
 await Promise.all(['tree','fern'].map(id=>library.get(id)));
 let seed=0;
 for(const[cx,cz,r,n]of treeGroves)for(let i=0;i<n;i++){
  if(signal?.aborted)throw Error('Landscape load cancelled');const a=i*2.399+cx,rr=r*Math.sqrt((i+.35)/n),x=cx+Math.cos(a)*rr,z=cz+Math.sin(a)*rr,k=seed++,height=7.2+hash(k)*6;
  if(!clear(x,z,3.6)||groundHeight(x,z)<1)continue;
  const root=await library.instantiate('tree',{x,y:groundHeight(x,z)-.04,z,height,rotation:a,collision:'trunk'});
  batch(root,'canopy',k%3);stats.imported.tree=(stats.imported.tree||0)+1;
  obstacles.push({...root.userData.collider,tree:true});
  for(let j=0;j<5;j++){
   const angle=a+j*2.4,rr=1.6+hash(k*7+j)*3,x1=x+Math.cos(angle)*rr,z1=z+Math.sin(angle)*rr;if(!clear(x1,z1,.6))continue;
   const fern=await library.instantiate('fern',{x:x1,y:groundHeight(x1,z1)-.03,z:z1,height:.7+hash(j+k)*.9,rotation:angle,collidable:false});batch(fern,'fern',j%3);stats.imported.fern=(stats.imported.fern||0)+1;
  }
 }
 for(let i=2;i<terrainInfo.boundary.length;i+=5){const[x,z]=terrainInfo.boundary[i],x1=x*.985,z1=z*.985,fern=await library.instantiate('fern',{x:x1,y:groundHeight(x1,z1)-2.4,z:z1,height:2.5+hash(i)*1.6,rotation:i,collidable:false});fern.rotation.z=.5;batch(fern,'cliff fern',i%3);stats.imported.hangingFern=(stats.imported.hangingFern||0)+1;}
 for(const{geometry,material,transforms,kind}of batches.values()){
  const m=new T.InstancedMesh(geometry,material,transforms.length);m.name='Living landscape / '+kind;transforms.forEach((t,i)=>m.setMatrixAt(i,t));m.computeBoundingSphere();m.castShadow=m.receiveShadow=true;scene.add(m);
 }
 stats.vegetationBatches=batches.size;
 const rock=chiselRock(1);b.owned.add(rock);const rockMat=standard('#909683',{flatShading:true}),moss=standard('#738564',{flatShading:true});
 for(const[cx,cz,r,n]of[[-47,-54,13,16],[-64,-19,9,12],[45,-32,12,14],[-76,7,7,9],[5,-71,10,9],[-40,40,7,10]])for(let i=0;i<n;i++){
  const a=i*2.399,rr=r*Math.sqrt((i+.5)/n),x=cx+Math.cos(a)*rr,z=cz+Math.sin(a)*rr,s=.6+hash(i+cx)*2.2;
  if(!clear(x,z,s+1)||groundHeight(x,z)<0)continue;const y=groundHeight(x,z),sy=s*(.6+hash(i+cz)*1.6);
  b.instance(rock,i%4===0?moss:rockMat,x,y+sy*.3,z,s,sy,s*.8,a);obstacles.push({x,z,w:s*1.8,d:s*1.5,minY:y,h:y+sy*1.4,rock:true});
 }
 // Buttresses attach below the lip; none are walking-surface placeholders.
 for(const[i,scale]of[[7,1.2],[34,1],[62,1.1],[94,1.3],[123,1],[157,1.4],[187,.9]]){
  const[x,z]=terrainInfo.boundary[i],y=groundHeight(x*.98,z*.98);b.instance(rock,rockMat,x*.87,y-19,z*.87,6*scale,21*scale,6*scale,i,.12);b.instance(rock,moss,x*.94,y-4,z*.94,5*scale,4,4*scale,i);
 }
 const frond=leafRibbon(4.5),palmMat=standard('#6d984e',{side:T.DoubleSide});b.owned.add(frond);
 for(const[x,z,h,lean]of[[12,46,10,.8],[38,54,12,-.6],[47,40,11,.4],[39,3,13,.8],[20,-12,11,-.5],[-22,37,12,.6],[-46,29,10,-.5],[-56,42,9,.7],[7,33,11,-.4],[52,17,13,.8]]){
  if(!clear(x,z,2.2))continue;const y=groundHeight(x,z),pp=[],ii=[];
  for(let r=0;r<=12;r++)for(let i=0;i<7;i++){const t=r/12,a=i/7*Math.PI*2,radius=.23-t*.09;pp.push(x+lean*t*t+Math.cos(a)*radius,y-.12+h*t,z+.4*t*t+Math.sin(a)*radius);if(r<12){const a0=r*7+i,b0=r*7+(i+1)%7;ii.push(a0,b0,a0+7,b0,b0+7,a0+7);}}
  const trunk=new T.BufferGeometry();trunk.setAttribute('position',new T.Float32BufferAttribute(pp,3));trunk.setIndex(ii);trunk.computeVertexNormals();b.mesh(trunk,standard('#8c7953'));
  for(let j=0;j<10;j++)b.instance(frond,palmMat,x+lean,y+h,z+.4,1,1,1,j/10*Math.PI*2,0,-.16);stats.palms=(stats.palms||0)+1;
 }
 const pos=[],colors=[],tips=[],idx=[],base=new T.Color('#4f793c'),tip=new T.Color('#a2b85b');let blades=0;
 for(let x=-84;x<85;x+=2)for(let z=-88;z<85;z+=2){
  const n=x*3.71+z*9.31,xx=x+(hash(n)-.5)*1.6,zz=z+(hash(n+1)-.5)*1.6,s=terrainSample(xx,zz),p=nearestPath(xx,zz);
  if(s.height<0||s.fraction>.97||p.distance<p.width/2+.4||Math.abs(groundHeight(xx+.3,zz)-s.height)>.35||Math.abs(groundHeight(xx,zz+.3)-s.height)>.35)continue;
  const density=.5+.3*Math.sin(xx*.08+zz*.04);if(hash(n+2)>density)continue;
  for(let j=0;j<12;j++){
   const angle=hash(n+j+3)*Math.PI*2,h=.4+hash(n+j+7)*.6,w=.075+hash(n+j+9)*.07,cx=xx+Math.cos(j*2.4)*.4,cz=zz+Math.sin(j*2.4)*.4,y=groundHeight(cx,cz)-.035,vi=pos.length/3;
   for(let row=0;row<3;row++)for(const side of[-1,1]){const t=row/2,ww=w*(1-t*.92),bend=t*t*.21;pos.push(cx+Math.cos(angle)*ww*side+Math.sin(angle)*bend,y+h*t,cz+Math.sin(angle)*ww*side-Math.cos(angle)*bend);tips.push(t);const c=base.clone().lerp(tip,t*.65+hash(n)*.22);colors.push(c.r,c.g,c.b);}
   idx.push(vi,vi+2,vi+1,vi+1,vi+2,vi+3,vi+2,vi+4,vi+3,vi+3,vi+4,vi+5);blades++;
  }
 }
 const gg=new T.BufferGeometry();gg.setAttribute('position',new T.Float32BufferAttribute(pos,3));gg.setAttribute('color',new T.Float32BufferAttribute(colors,3));gg.setAttribute('sway',new T.Float32BufferAttribute(tips,1));gg.setIndex(idx);gg.computeVertexNormals();
 const gm=standard('#ffffff',{vertexColors:true,side:T.DoubleSide});gm.onBeforeCompile=shader=>{shader.uniforms.landscapeTime=wind;shader.vertexShader='uniform float landscapeTime;attribute float sway;\n'+shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\ntransformed.x += sin(landscapeTime*1.4+position.z*.38+position.x*.13)*sway*sway*.14;');};gm.customProgramCacheKey=()=>'r0a-grass-wind-1';
 const grass=b.mesh(gg,gm);grass.name='Wind meadow / authored blade geometry';grass.castShadow=false;stats.grassBlades=blades;
 return{update(time,reduced){wind.value=reduced?0:time;}};
}
