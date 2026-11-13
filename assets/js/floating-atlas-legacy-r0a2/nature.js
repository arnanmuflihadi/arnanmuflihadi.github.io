import * as T from'../vendor/three-atlas.module.js?v=16';
import{leafRibbon}from'../urban-atlas/geometry.js?v=22';
import{groundHeight,terrainSample,nearestPath,terrainInfo}from'./terrain.js?v=67';
import{treeGroves,areas}from'./plan.js?v=67';
import{createGroundcover,shrubGeometry}from'./groundcover.js?v=67';

const hash=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);};
export function chiselRock(seed=0){
 const p=[],idx=[],n=11,levels=[[-.85,.6],[-.3,1],[.43,.87],[.72,.43]];
 for(let r=0;r<levels.length;r++)for(let i=0;i<n;i++){const a=i/n*Math.PI*2,rr=levels[r][1]*(1+.12*Math.sin(a*3+seed)+.06*Math.cos(a*5-r));p.push(Math.cos(a)*rr+levels[r][0]*.14,levels[r][0]+Math.sin(a*2+seed)*.09,Math.sin(a)*rr);if(r<levels.length-1){const k=r*n+i,j=r*n+(i+1)%n;idx.push(k,k+n,j,j,k+n,j+n);}}
 const top=p.length/3;p.push(.1,.75,0);const bottom=p.length/3;p.push(-.1,-.9,0);for(let i=0;i<n;i++){idx.push(top,3*n+(i+1)%n,3*n+i);idx.push(bottom,i,(i+1)%n);}
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setIndex(idx);g.computeVertexNormals();g.computeBoundingBox();return g;
}
export async function dressLandscape({scene,b,standard,library,obstacles,stats,ownedMaterials,signal,cliffLedges=[]}){
 const batches=new Map(),finishes=new Map(),growthCache=new Map(),wind={value:0};
 function grow(root,profile){root.traverse(o=>{if(!o.isMesh)return;const key=o.geometry.uuid+':'+profile;if(!growthCache.has(key)){
  const g=o.geometry.clone(),p=g.attributes.position,form=[{x:1.3,y:.73,z:1.16,lean:.025},{x:.74,y:1.3,z:.86,lean:-.025},{x:1.14,y:.85,z:.74,lean:.17}][profile];
  for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i),dy=Math.max(0,y-2.1),t=Math.min(1,dy/2.4),blend=t*t*(3-2*t);p.setXYZ(i,x*(1+(form.x-1)*blend)+dy*form.lean,2.1+Math.min(0,y-2.1)+dy*form.y,z*(1+(form.z-1)*blend));}
  g.computeVertexNormals();g.computeBoundingBox();g.computeBoundingSphere();growthCache.set(key,g);b.owned.add(g);
 }o.geometry=growthCache.get(key);});root.updateMatrixWorld(true);}
 function batch(root,kind,variant){root.updateMatrixWorld(true);root.traverse(o=>{
  if(!o.isMesh)return;const source=o.material,key=source.uuid+':'+variant;
  if(!finishes.has(key)){const m=source.clone();m.vertexColors=false;m.roughness=.97;
   if(/leaves|foliage|leaf/i.test(m.name)){m.color.set(['#c9d6a2','#afcdb2','#cfca91'][variant%3]);m.emissive.set('#68805d');m.emissiveIntensity=.2;if(m.aoMap)m.aoMapIntensity=.12;m.onBeforeCompile=s=>{s.fragmentShader=s.fragmentShader.replace('#include <alphatest_fragment>','#include <alphatest_fragment>\nfloat canopyDistance=length(vViewPosition);if(canopyDistance<2.7&&fract(dot(floor(gl_FragCoord.xy),vec2(.754,.569)))>smoothstep(.65,2.7,canopyDistance))discard;');};m.customProgramCacheKey=()=>'a2-canopy-clearance';}
   else{m.color.set('#c5b99c');m.emissive.set('#84694b');m.emissiveIntensity=.12;}finishes.set(key,m);ownedMaterials.add(m);
  }
  const m=finishes.get(key),k=kind+o.geometry.uuid+m.uuid;if(!batches.has(k))batches.set(k,{geometry:o.geometry,material:m,transforms:[],kind});batches.get(k).transforms.push(o.matrixWorld.clone());
 });}
 const clear=(x,z,margin)=>{const p=nearestPath(x,z);return terrainSample(x,z).fraction<.94&&p.distance>p.width/2+margin&&!Object.values(areas).some(a=>Math.hypot(x-a.x,z-a.z)<(a===areas.highlands?4:6));};
 await Promise.all(['tree','fern'].map(id=>library.get(id)));
 let seed=0;stats.growthForms={spreading:0,emergent:0,windswept:0};stats.landscapeZones={forest:0,meadow:0,ridge:0};
 for(const[grove,[cx,cz,r,n]]of treeGroves.entries())for(let i=0;i<n;i++){
  if(signal?.aborted)throw Error('Landscape load cancelled');const zone=groundHeight(cx,cz)>33?'ridge':[4,5,6].includes(grove)?'meadow':'forest';if(zone==='meadow'&&i%3===1)continue;
  const a=i*2.399+cx,rr=r*Math.sqrt((i+.35)/n)*(zone==='forest'?.82:1),x=cx+Math.cos(a)*rr+Math.sin(grove)*r*.08,z=cz+Math.sin(a)*rr,k=seed++,height=zone==='ridge'?6.2+hash(k)*2.5:zone==='forest'?8.5+hash(k)*4.6:7.5+hash(k)*3;
  if(!clear(x,z,3.6)||groundHeight(x,z)<1)continue;
  const root=await library.instantiate('tree',{x,y:groundHeight(x,z)-.04,z,height,rotation:a,collision:'trunk'});
  const profile=zone==='ridge'?2:zone==='meadow'?0:k%3;grow(root,profile);batch(root,'canopy',k%3);stats.imported.tree=(stats.imported.tree||0)+1;stats.growthForms[['spreading','emergent','windswept'][profile]]++;stats.landscapeZones[zone]++;
  const bounds=new T.Box3().setFromObject(root);obstacles.push({...root.userData.collider,h:bounds.max.y,tree:true});
  for(let j=0;j<5;j++){
   const angle=a+j*2.4,rr=1.6+hash(k*7+j)*3,x1=x+Math.cos(angle)*rr,z1=z+Math.sin(angle)*rr;if(!clear(x1,z1,.6))continue;
   const fern=await library.instantiate('fern',{x:x1,y:groundHeight(x1,z1)-.03,z:z1,height:.7+hash(j+k)*.9,rotation:angle,collidable:false});batch(fern,'fern',j%3);stats.imported.fern=(stats.imported.fern||0)+1;
  }
 }
 for(let i=0;i<cliffLedges.length;i++){const p=cliffLedges[i],fern=await library.instantiate('fern',{x:p.x,y:p.y-.12,z:p.z,height:1.5+hash(i)*1.2,rotation:p.rotation,collidable:false});fern.rotation.z=.35;batch(fern,'cliff fern',i%3);stats.imported.hangingFern=(stats.imported.hangingFern||0)+1;}
 for(const{geometry,material,transforms,kind}of batches.values()){
  const m=new T.InstancedMesh(geometry,material,transforms.length);m.name='Living landscape / '+kind;transforms.forEach((t,i)=>m.setMatrixAt(i,t));m.computeBoundingSphere();m.castShadow=m.receiveShadow=true;scene.add(m);
 }
 stats.vegetationBatches=batches.size;stats.derivedTreeGeometries=growthCache.size;
 const rock=chiselRock(1);b.owned.add(rock);const rockMat=standard('#909683',{flatShading:true}),moss=standard('#738564',{flatShading:true});
 for(const[cx,cz,r,n]of[[-47,-54,13,16],[-64,-19,9,12],[45,-32,12,14],[-76,7,7,9],[5,-71,10,9],[-40,40,7,10]])for(let i=0;i<n;i++){
  const a=i*2.399,rr=r*Math.sqrt((i+.5)/n),x=cx+Math.cos(a)*rr,z=cz+Math.sin(a)*rr,s=.6+hash(i+cx)*2.2;
  if(!clear(x,z,s+1)||groundHeight(x,z)<0)continue;const y=groundHeight(x,z),sy=s*(.6+hash(i+cz)*1.6);
  b.instance(rock,i%4===0?moss:rockMat,x,y+sy*.3,z,s,sy,s*.8,a);const proxy=new T.Object3D();proxy.position.set(x,y+sy*.3,z);proxy.rotation.y=a;proxy.scale.set(s,sy,s*.8);proxy.updateMatrix();const bounds=rock.boundingBox.clone().applyMatrix4(proxy.matrix),size=bounds.getSize(new T.Vector3()),center=bounds.getCenter(new T.Vector3());obstacles.push({x:center.x,z:center.z,w:size.x,d:size.z,minY:bounds.min.y,h:bounds.max.y,rock:true});
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
 const shrub=shrubGeometry(),shrubMat=standard('#ffffff',{vertexColors:true,side:T.DoubleSide});b.owned.add(shrub);
 for(const[cx,cz,r,n]of treeGroves)for(let i=0;i<Math.floor(n*.9);i++){const a=i*2.399+cx,rr=r*Math.sqrt((i+.5)/n),x=cx+Math.cos(a)*rr,z=cz+Math.sin(a)*rr;if(!clear(x,z,1.15)||groundHeight(x,z)>39)continue;const scale=.75+hash(i+cx)*.8;b.instance(shrub,shrubMat,x,groundHeight(x,z)-.08,z,scale,scale,scale,a);stats.shrubs=(stats.shrubs||0)+1;}
 const groundcover=createGroundcover({b,standard,stats,wind});
 return{setEco:value=>groundcover.setEco(value),update(time,reduced,camera){wind.value=reduced?0:time;groundcover.update(camera);}};
}
