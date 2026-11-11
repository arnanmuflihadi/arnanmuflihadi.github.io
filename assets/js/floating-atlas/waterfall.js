import * as T from'../vendor/three-atlas.module.js?v=16';
import{groundHeight}from'./terrain.js?v=73';
import{streamPoints}from'./plan.js?v=73';

const end=streamPoints.at(-1),previous=streamPoints.at(-2),flow=new T.Vector3(end[0]-previous[0],0,end[1]-previous[1]).normalize(),side=new T.Vector3(flow.z,0,-flow.x),drop=78;
export function watercourseFixEnabled(url=globalThis.location?.href){if(!url)return false;const u=new URL(url);return ['localhost','127.0.0.1','[::1]'].includes(u.hostname)&&u.searchParams.get('watercourse')==='refined';}
export function fallingWaterGeometry(improved=watercourseFixEnabled()){
 const p=[],uv=[],idx=[],rows=42,cols=12,y0=groundHeight(end[0],end[1])+.12;
 for(let r=0;r<=rows;r++){
  const t=r/rows,push=10*(1-Math.exp(-t*12))+t*t*2,width=improved?3.6+t*1.2+Math.sin(t*9)*.25:3.6+t*2.1+Math.sin(t*17)*.14,depth=.58+t*(improved?.6:.85),cx=end[0]+flow.x*push,cz=end[1]+flow.z*push;
  for(let i=0;i<cols;i++){
   const a=i/cols*Math.PI*2,w=Math.cos(a)*width/2*(1+.045*Math.sin(t*29+i*2.7)),d=Math.sin(a)*depth/2;
   p.push(cx+side.x*w+flow.x*d,y0-drop*t,cz+side.z*w+flow.z*d);uv.push(i/cols,t);
   if(r<rows){const k=r*cols+i,j=r*cols+(i+1)%cols;idx.push(k,j,k+cols,j,j+cols,k+cols);}
  }
 }
 const top=p.length/3;p.push(end[0],y0,end[1]);uv.push(.5,0);const bottom=p.length/3;p.push(end[0]+flow.x*12,y0-drop,end[1]+flow.z*12);uv.push(.5,1);
 for(let i=0;i<cols;i++)idx.push(top,(i+1)%cols,i,bottom,rows*cols+i,rows*cols+(i+1)%cols);
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();g.computeBoundingBox();g.userData={source:[end[0],y0,end[1]],termination:[end[0]+flow.x*12,y0-drop,end[1]+flow.z*12],rows,cols};return g;
}

export function channelGeometry(improved=watercourseFixEnabled()){
 if(!improved){
  const p=[],uv=[],idx=[];let length=0;
  for(let j=1;j<streamPoints.length;j++){
   const a=streamPoints[j-1],c=streamPoints[j],dx=c[0]-a[0],dz=c[1]-a[1],len=Math.hypot(dx,dz),offset=p.length/3;
   for(let i=0;i<=32;i++){
    const t=i/32,x=a[0]+dx*t,z=a[1]+dz*t,width=1.05+j*.11+Math.sin((length+t*len)*.7)*.09;
    for(const s of[-1,1]){const xx=x+dz/len*s*width,zz=z-dx/len*s*width;p.push(xx,groundHeight(x,z)+.075,zz);uv.push((s+1)/2,(length+t*len)/60);}
    if(i<32){const k=offset+i*2;idx.push(k,k+1,k+2,k+1,k+3,k+2);}
   }length+=len;
  }
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();return g;
 }
 const p=[],uv=[],idx=[],steps=(streamPoints.length-1)*32;let length=0,previous;
 function pointAt(t){const n=streamPoints.length-1,u=Math.min(n,Math.max(0,t*n)),i=Math.min(n-1,Math.floor(u)),f=u-i,at=k=>streamPoints[Math.max(0,Math.min(n,k))];return new T.Vector3(...[0,1].map(axis=>{const a=at(i-1)[axis],b=at(i)[axis],c=at(i+1)[axis],d=at(i+2)[axis];return .5*((2*b)+(-a+c)*f+(2*a-5*b+4*c-d)*f*f+(-a+3*b-3*c+d)*f*f*f);}).flatMap((value,axis)=>axis===0?[value,0]:[value]));}
 for(let i=0;i<=steps;i++){
  const t=i/steps,point=pointAt(t),tangent=pointAt(Math.min(1,t+.001)).sub(pointAt(Math.max(0,t-.001))).normalize();if(previous)length+=point.distanceTo(previous);previous=point;
  const width=1.12+.48*t+Math.sin(length*.32)*.08,center=groundHeight(point.x,point.z);
  for(const s of[-1,1]){const x=point.x+tangent.z*s*width,z=point.z-tangent.x*s*width,edge=groundHeight(x,z);p.push(x,(edge>0?edge:center)+.075,z);uv.push((s+1)/2,length/60);}
  if(i<steps){const k=i*2;idx.push(k,k+1,k+2,k+1,k+3,k+2);}
 }
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();return g;
}

export function createWaterfall({scene,b,standard,ownedMaterials,rocks,rockMaterial,stats}){
 const time={value:0},vertex=`uniform float time;uniform float falling;varying vec2 waterUV;varying float waterDistance;
 void main(){waterUV=uv;vec3 p=position;p.x+=sin(time*1.4+uv.y*19.+uv.x*5.)*.065*sin(uv.y*3.14159)*falling;vec4 mv=modelViewMatrix*vec4(p,1.);waterDistance=length(mv.xyz);gl_Position=projectionMatrix*mv;}`;
 function material(falling){
  const m=new T.ShaderMaterial({transparent:true,depthWrite:false,side:falling?0:T.DoubleSide,uniforms:{time,falling:{value:falling?1:0},deep:{value:new T.Color('#64a2a5')},foam:{value:new T.Color('#e1eee2')},haze:{value:new T.Color('#8bb0c0')}},vertexShader:vertex,
   fragmentShader:`uniform float time;uniform float falling;uniform vec3 deep;uniform vec3 foam;uniform vec3 haze;varying vec2 waterUV;varying float waterDistance;
   void main(){vec2 uv=waterUV;float veins=pow(.5+.5*sin(uv.x*77.+sin(uv.y*17.+uv.x*13.)*1.2+sin(uv.y*42.+uv.x*7.)*.4),6.);float current=pow(.5+.5*sin(uv.y*107.+time*7.+sin(uv.x*25.)*6.),16.);float bank=smoothstep(.68,1.,abs(uv.x*2.-1.));float froth=mix(bank*.30+current*.3,veins*.33+current*.35,falling);vec3 col=mix(deep,foam,.18+froth);float alpha=mix(.88,.91*(1.-smoothstep(.77,1.,uv.y)),falling);col=mix(col,haze,clamp((waterDistance-170.)/730.,0.,.75));gl_FragColor=vec4(col,alpha);
    #include <tonemapping_fragment>
    #include <colorspace_fragment>
   }`});ownedMaterials.add(m);return m;
 }
 const river=b.mesh(channelGeometry(),material(false));river.name='Valley stream / widened shallow channel';river.castShadow=false;
 const fall=b.mesh(fallingWaterGeometry(),material(true));fall.name='Cloudbreak waterfall / sculpted flowing volume';fall.castShadow=false;
 const wet=standard('#687c70',{roughness:1,vertexColors:true,flatShading:true}),bankPoints=[];
 for(let j=0;j<streamPoints.length;j++){
  const p=streamPoints[j];for(const sign of[-1,1]){const d=1.6+j*.13,x=p[0]+side.x*d*sign,z=p[1]+side.z*d*sign,y=groundHeight(x,z);if(y<0)continue;const s=j===streamPoints.length-1?1.8:.65+j%2*.45;b.instance(rocks[j%3],j%2?wet:rockMaterial,x,y+.12,z,s,s*(j===streamPoints.length-1?1:.65),s*.85,j*.7+sign,.1*sign);bankPoints.push([x,y,z]);}
 }
 const source=streamPoints[0],pool=new T.BufferGeometry(),pp=[source[0],groundHeight(source[0],source[1])+.08,source[1]],puv=[.5,.5],pi=[];
 for(let i=0;i<=30;i++){const a=i/30*Math.PI*2,x=source[0]+Math.cos(a)*2.2,z=source[1]+Math.sin(a)*1.6;pp.push(x,groundHeight(x,z)+.08,z);puv.push(.5+Math.cos(a)*.5,.5+Math.sin(a)*.5);if(i<30)pi.push(0,i+2,i+1);}pool.setAttribute('position',new T.Float32BufferAttribute(pp,3));pool.setAttribute('uv',new T.Float32BufferAttribute(puv,2));pool.setIndex(pi);pool.computeVertexNormals();const spring=b.mesh(pool,material(false));spring.name='Visible spring pool / stream source';spring.castShadow=false;
 const foamMat=new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,uniforms:{time,color:{value:new T.Color('#e2eadb')}},vertexShader:'varying vec2 v;void main(){v=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'uniform float time;uniform vec3 color;varying vec2 v;void main(){float edge=smoothstep(0.,.15,v.x)*(1.-smoothstep(.85,1.,v.x));float a=(.45+.18*sin(v.x*39.+time*1.7))*edge;gl_FragColor=vec4(color,a);\n#include <colorspace_fragment>\n}'});ownedMaterials.add(foamMat);
 const lip=new T.PlaneGeometry(3.6,.65,20,1);lip.rotateX(-Math.PI/2);lip.rotateY(Math.atan2(-side.z,side.x));const foam=b.mesh(lip,foamMat,end[0],groundHeight(end[0],end[1])+.15,end[1]);foam.name='Spill edge / aerated water';foam.castShadow=false;
 const mistMat=new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,uniforms:{time,color:{value:new T.Color('#ccded9')}},vertexShader:'varying vec2 v;varying float seed;void main(){v=uv;vec4 p=instanceMatrix*vec4(position,1.);seed=instanceMatrix[3].y;gl_Position=projectionMatrix*modelViewMatrix*p;}',fragmentShader:'varying vec2 v;varying float seed;uniform float time;uniform vec3 color;void main(){vec2 p=(v-.5)*2.;float edge=1.-length(p*vec2(1.,1.15));float lobes=.05*sin(p.x*12.+seed)+.035*sin(p.y*15.-seed);float a=smoothstep(0.,.6,edge+lobes)*(.18+.025*sin(time*.6+seed));gl_FragColor=vec4(color,a);\n#include <colorspace_fragment>\n}'});ownedMaterials.add(mistMat);
 const mistGeo=new T.PlaneGeometry(1,1);b.owned.add(mistGeo);const mist=new T.InstancedMesh(mistGeo,mistMat,9);mist.name='Waterfall spray / dissolving into cloudscape';mist.castShadow=mist.receiveShadow=false;mist.frustumCulled=false;scene.add(mist);const dummy=new T.Object3D(),y0=groundHeight(end[0],end[1]);
 function update(t,reduced,camera){time.value=reduced?0:t;if(!camera)return;for(let i=0;i<9;i++){const lower=i>2,depth=lower?50+(i-3)*4:1.5+i*3,push=lower?9:1.5+i*.8,offset=(i%3-1)*(lower?4.5:1.1);dummy.position.set(end[0]+flow.x*push+side.x*offset,y0-depth,end[1]+flow.z*push+side.z*offset);dummy.position.y+=(reduced?0:Math.sin(t*.3+i)*.32);dummy.quaternion.copy(camera.quaternion);dummy.scale.set(lower?12+i%3*2:4.2,lower?8:2.5,1);dummy.updateMatrix();mist.setMatrixAt(i,dummy.matrix);}mist.instanceMatrix.needsUpdate=true;}
 stats.waterfall={source:fall.geometry.userData.source,termination:fall.geometry.userData.termination,widthAtLip:3.6,fallHeight:drop,volumeTriangles:fall.geometry.index.count/3,bankRocks:bankPoints.length,mistCards:9};return{update,fall,river,bankPoints,time};
}
