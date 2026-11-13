import * as T from'../vendor/three-atlas.module.js?v=16';
import{groundHeight,terrainSample,nearestPath}from'./terrain.js?v=67';
const hash=n=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);};

export function shrubGeometry(){
 const p=[],colors=[],idx=[],dark=new T.Color('#3f7255'),light=new T.Color('#8ea66b');
 for(let leaf=0;leaf<13;leaf++){
  const a=leaf*2.399,h=.12+hash(leaf)*.5,length=.4+hash(leaf+1)*.45,k=p.length/3;
  for(let row=0;row<5;row++)for(const side of[-1,1]){const t=row/4,w=Math.sin(t*Math.PI)*.16,forward=.12+t*length;p.push(Math.cos(a)*forward-Math.sin(a)*w*side,h+Math.sin(t*Math.PI)*.17+t*.15,Math.sin(a)*forward+Math.cos(a)*w*side);const c=dark.clone().lerp(light,t*.45+hash(leaf)*.3);colors.push(c.r,c.g,c.b);}
  for(let row=0;row<4;row++){const n=k+row*2;idx.push(n,n+2,n+1,n+1,n+2,n+3);}
 }
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.setIndex(idx);g.computeVertexNormals();return g;
}

export function createGroundcover({b,standard,stats,wind}){
 const chunks=new Map(),base=new T.Color('#477744'),tip=new T.Color('#91ac60');let blades=0,eco=false;
 for(let x=-84;x<85;x+=1.4)for(let z=-88;z<85;z+=1.4){
  const n=x*3.71+z*9.31,xx=x+(hash(n)-.5)*1.25,zz=z+(hash(n+1)-.5)*1.25,s=terrainSample(xx,zz),path=nearestPath(xx,zz);
  if(s.height<0||s.fraction>.97||path.distance<path.width/2+.35||Math.abs(groundHeight(xx+.3,zz)-s.height)>.35||Math.abs(groundHeight(xx,zz+.3)-s.height)>.35)continue;
  const patch=.5+.28*Math.sin(xx*.13+zz*.057)+.18*Math.sin(zz*.19-xx*.071),ridge=s.height>35;if(hash(n+2)>(ridge?.15:.2)+patch*(ridge?.25:.46))continue;
  const key=Math.floor(xx/30)+':'+Math.floor(zz/30);if(!chunks.has(key))chunks.set(key,{pos:[],colors:[],tips:[],idx:[],farIdx:[],x:Math.floor(xx/30)*30+15,z:Math.floor(zz/30)*30+15});const c=chunks.get(key),count=4+Math.floor(hash(n+6)*8);
  for(let j=0;j<count;j++){
   const angle=hash(n+j+3)*Math.PI*2,h=(ridge?.18:.28)+hash(n+j+7)*(ridge?.28:.48),w=.035+hash(n+j+9)*.035,r=.15+hash(j+n)*.55,cx=xx+Math.cos(j*2.4)*r,cz=zz+Math.sin(j*2.4)*r,y=groundHeight(cx,cz)-.025,vi=c.pos.length/3;
   if(nearestPath(cx,cz).distance<path.width/2+.08)continue;
   for(let row=0;row<5;row++)for(const side of[-1,1]){const t=row/4,ww=w*(.15+Math.sin(Math.PI*t)*.85)*(1-t*.92),bend=t*t*(.1+hash(n+j)*.16);c.pos.push(cx+Math.cos(angle)*ww*side+Math.sin(angle)*bend,y+h*t,cz+Math.sin(angle)*ww*side-Math.cos(angle)*bend);c.tips.push(t);const col=base.clone().lerp(tip,t*.48+patch*.2);c.colors.push(col.r,col.g,col.b);}
   for(let row=0;row<4;row++){const k=vi+row*2,tri=[k,k+2,k+1,k+1,k+2,k+3];c.idx.push(...tri);if(blades%7===0)c.farIdx.push(...tri);}blades++;
  }
 }
 const material=standard('#ffffff',{vertexColors:true,side:T.DoubleSide});material.onBeforeCompile=s=>{s.uniforms.landscapeTime=wind;s.vertexShader='uniform float landscapeTime;attribute float sway;\n'+s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\ntransformed.x += sin(landscapeTime*1.35+position.z*.3+position.x*.1)*sway*sway*.09;');};material.customProgramCacheKey=()=>'r0a2-curved-grass';
 const pieces=[];for(const c of chunks.values()){if(!c.idx.length)continue;const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(c.pos,3));g.setAttribute('color',new T.Float32BufferAttribute(c.colors,3));g.setAttribute('sway',new T.Float32BufferAttribute(c.tips,1));g.setIndex(c.idx);g.computeVertexNormals();g.computeBoundingSphere();const far=new T.BufferGeometry();for(const k of['position','normal','color','sway'])far.setAttribute(k,g.attributes[k]);far.setIndex(c.farIdx);far.boundingSphere=g.boundingSphere.clone();b.owned.add(far);const m=b.mesh(g,material);m.name='Zone grass / curved blades';m.castShadow=false;m.userData.detailLevels={near:g,far};pieces.push({mesh:m,near:g,far,x:c.x,z:c.z,y:Math.max(10,groundHeight(c.x,c.z))});}
 stats.grassBlades=blades;stats.detail={grassChunks:pieces.length,activeGrassChunks:pieces.length,nearGrassChunks:pieces.length,farGrassChunks:0,eco:false};
 return{setEco(value){eco=value;},update(camera){let visible=0,near=0,far=0;for(const p of pieces){const distance=camera?Math.hypot(camera.position.x-p.x,camera.position.y-p.y,camera.position.z-p.z):0;p.mesh.visible=distance<(eco?145:290);const detailed=distance<(eco?48:87);p.mesh.geometry=detailed?p.near:p.far;if(p.mesh.visible){visible++;if(detailed)near++;else far++;}}Object.assign(stats.detail,{activeGrassChunks:visible,nearGrassChunks:near,farGrassChunks:far,eco});}};
}
