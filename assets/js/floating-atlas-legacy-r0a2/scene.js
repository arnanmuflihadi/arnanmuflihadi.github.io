import * as T from'../vendor/three-atlas.module.js?v=16';
import{createModelLibrary,modelMetrics}from'../urban-atlas/model-library.js?v=15';
import{createBuilder}from'../urban-atlas/geometry.js?v=22';
import{createMaterials}from'../urban-atlas/materials.js?v=22';
import{createTerrainGeometry,createCliffGeometry,groundHeight,terrainInfo}from'./terrain.js?v=67';
import{streamPoints,reservations}from'./plan.js?v=67';
import{dressLandscape}from'./nature.js?v=67';
import{createAtmosphere,distantIslandGeometry}from'./atmosphere.js?v=67';
export async function createFloatingWorld({library=createModelLibrary(),signal}={}){
 const scene=new T.Scene();scene.background=new T.Color('#8bb0c0');scene.fog=new T.Fog('#8bb0c0',170,900);
 const materials=createMaterials(),b=createBuilder(scene,materials),obstacles=[],ownedMaterials=new Set(),stats={world:'Transit Kingdom / Landscape',revision:'R0A2.67',terrainOnly:true,architectureInstances:0,reservations,imported:{},terrain:terrainInfo.dimensions};let disposed=false,world;
 const standard=(color,extra={})=>{const m=new T.MeshStandardMaterial({color,roughness:.96,...extra});ownedMaterials.add(m);return m;};
 const terrain=b.mesh(createTerrainGeometry(),standard('#ffffff',{vertexColors:true}));terrain.name='Authored landscape / exact support triangles';
 terrain.material.onBeforeCompile=s=>{s.vertexShader='attribute float trail;varying float pathAmount;varying vec2 landscapeXZ;\n'+s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\npathAmount=trail;landscapeXZ=position.xz;');s.fragmentShader='varying float pathAmount;varying vec2 landscapeXZ;\n'+s.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\nif(pathAmount>.2){vec2 cell=floor(landscapeXZ*1.8);float stone=step(.955,fract(sin(dot(cell,vec2(127.1,311.7)))*43758.5453));float edge=1.-smoothstep(.10,.24,length(fract(landscapeXZ*1.8)-.5));diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.31,.32,.26),stone*edge*pathAmount*.45);}');};terrain.material.customProgramCacheKey=()=>'r0a2-painted-soil';
 const cliffs=b.mesh(createCliffGeometry(),standard('#ffffff',{vertexColors:true,flatShading:true,emissive:'#6d8989',emissiveIntensity:.045}));cliffs.name='Chiseled geological strata / closed underside';
 scene.add(new T.HemisphereLight('#c6dfec','#66765e',1.5));
 const sun=new T.DirectionalLight('#ffebcb',2.3);sun.position.set(-85,125,75);sun.target.position.set(0,15,0);scene.add(sun,sun.target);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-110,right:110,top:110,bottom:-110,near:1,far:310});sun.shadow.normalBias=.035;sun.shadow.bias=-.00012;sun.shadow.radius=3;
 const atmosphere=createAtmosphere({scene,b,ownedMaterials});
 let profile=0;for(const[x,y,z,s]of[[-280,15,-270,1.2],[230,52,-340,1.4],[370,-24,80,.85],[-350,100,150,.9]]){
  const m=b.mesh(distantIslandGeometry(profile++),standard('#ffffff',{vertexColors:true,flatShading:true}),x,y,z);m.name='Distant uninhabited silhouette';m.scale.setScalar(s);m.rotation.y=profile*.8;m.castShadow=false;
 }
 const waterMaterial=new T.ShaderMaterial({transparent:true,side:T.DoubleSide,depthWrite:false,uniforms:{time:{value:0}},vertexShader:'varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec3 p;uniform float time;void main(){float s=.5+.5*sin(p.x*3.+p.y*.5+p.z*2.+time*.8);gl_FragColor=vec4(mix(vec3(.21,.52,.52),vec3(.75,.89,.79),s*.45),.84);}'});ownedMaterials.add(waterMaterial);
 const rp=[],ri=[];for(let j=1;j<streamPoints.length;j++){const a=streamPoints[j-1],c=streamPoints[j],n=28,dx=c[0]-a[0],dz=c[1]-a[1],length=Math.hypot(dx,dz),offset=rp.length/3;for(let i=0;i<=n;i++){const t=i/n,x=a[0]+dx*t,z=a[1]+dz*t,y=groundHeight(x,z)+.075;for(const s of[-1,1])rp.push(x-dz/length*s*.7,y,z+dx/length*s*.7);if(i<n){const k=offset+i*2;ri.push(k,k+2,k+1,k+1,k+2,k+3);}}}
 const rg=new T.BufferGeometry();rg.setAttribute('position',new T.Float32BufferAttribute(rp,3));rg.setIndex(ri);rg.computeVertexNormals();const river=b.mesh(rg,waterMaterial);river.name='Valley stream';river.castShadow=false;
 const end=streamPoints.at(-1),endY=groundHeight(end[0],end[1]),fall=b.mesh(new T.PlaneGeometry(1.8,74,2,25),waterMaterial,end[0]-.45,endY-37,end[1]+.25);fall.rotation.y=-1.1;fall.name='Cloudbreak waterfall';fall.castShadow=false;
 const dispose=()=>{if(disposed)return;disposed=true;signal?.removeEventListener('abort',dispose);const gs=new Set(b.owned),ms=new Set(ownedMaterials),ts=new Set();scene.traverse(o=>{if(o.isInstancedMesh)o.dispose();if(o.geometry)gs.add(o.geometry);for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])ms.add(m);});for(const g of gs)g.dispose();for(const m of ms){for(const t of Object.values(m))if(t?.isTexture)ts.add(t);m.dispose();}for(const t of ts)t.dispose();materials.dispose();library.dispose();sun.shadow.dispose();scene.clear();};
 try{
  const nature=await dressLandscape({scene,b,standard,library,obstacles,stats,ownedMaterials,signal,cliffLedges:cliffs.geometry.userData.ledges});b.flush();scene.updateMatrixWorld(true);
  world={scene,obstacles,materials,library,stats,terrain,groundHeight,dispose,settlement:null,setQuality:eco=>nature.setEco(eco),update(time,reduced,camera){waterMaterial.uniforms.time.value=reduced?0:time;atmosphere.update(time,reduced,camera);nature.update(time,reduced,camera);}};
  if(signal?.aborted){dispose();throw Error('Landscape load cancelled');}signal?.addEventListener('abort',dispose,{once:true});
  Object.assign(stats,{files:library.stats(),geometry:modelMetrics(scene),surfaceTriangles:terrainInfo.triangles,sourceFiles:['canopy-tree.glb','fern.glb'],cloudCount:atmosphere.cloudCount,settlement:null});
  if(stats.geometry.missingTextures.length)throw Error('Landscape texture missing');return world;
 }catch(error){dispose();throw error;}
}
