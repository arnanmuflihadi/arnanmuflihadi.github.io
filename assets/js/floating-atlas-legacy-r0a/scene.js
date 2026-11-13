import * as T from'../vendor/three-atlas.module.js?v=16';
import{createModelLibrary,modelMetrics}from'../urban-atlas/model-library.js?v=15';
import{createBuilder}from'../urban-atlas/geometry.js?v=22';
import{createMaterials}from'../urban-atlas/materials.js?v=22';
import{createTerrainGeometry,createCliffGeometry,groundHeight,terrainInfo}from'./terrain.js?v=63';
import{streamPoints,reservations}from'./plan.js?v=63';
import{dressLandscape,chiselRock}from'./nature.js?v=63';
import{createAtmosphere}from'./atmosphere.js?v=63';
export async function createFloatingWorld({library=createModelLibrary(),signal}={}){
 const scene=new T.Scene();scene.background=new T.Color('#b9d3d2');scene.fog=new T.Fog('#b9d3d2',140,630);
 const materials=createMaterials(),b=createBuilder(scene,materials),obstacles=[],ownedMaterials=new Set(),stats={world:'Transit Kingdom / Landscape',revision:'R0A.63',terrainOnly:true,architectureInstances:0,reservations,imported:{},terrain:terrainInfo.dimensions};let disposed=false,world;
 const standard=(color,extra={})=>{const m=new T.MeshStandardMaterial({color,roughness:.96,...extra});ownedMaterials.add(m);return m;};
 const terrain=b.mesh(createTerrainGeometry(),standard('#ffffff',{vertexColors:true}));terrain.name='Authored landscape / exact support triangles';
 const cliffs=b.mesh(createCliffGeometry(),standard('#ffffff',{vertexColors:true,flatShading:true,emissive:'#6d8989',emissiveIntensity:.08}));cliffs.name='Chiseled geological strata / closed underside';
 scene.add(new T.HemisphereLight('#e6f1e9','#64716a',1.65));
 const sun=new T.DirectionalLight('#ffe5b8',2.6);sun.position.set(-85,125,75);sun.target.position.set(0,15,0);scene.add(sun,sun.target);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-110,right:110,top:110,bottom:-110,near:1,far:310});sun.shadow.normalBias=.035;sun.shadow.bias=-.00012;sun.shadow.radius=3;
 const atmosphere=createAtmosphere({scene,b,ownedMaterials});
 const rock=chiselRock(4);b.owned.add(rock);
 for(const[x,y,z,s]of[[-280,15,-270,.68],[230,52,-340,.75],[370,-24,80,.42],[-350,100,150,.35]]){
  const group=new T.Group();group.name='Distant uninhabited silhouette';group.position.set(x,y,z);scene.add(group);
  const m=new T.Mesh(rock,standard('#729b96',{flatShading:true}));m.scale.set(50*s,28*s,36*s);m.position.y=-15*s;group.add(m);
  const cap=new T.Mesh(rock,standard('#8aab8b',{flatShading:true}));cap.scale.set(50*s,9*s,36*s);cap.position.y=8*s;group.add(cap);
 }
 const waterMaterial=new T.ShaderMaterial({transparent:true,side:T.DoubleSide,depthWrite:false,uniforms:{time:{value:0}},vertexShader:'varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec3 p;uniform float time;void main(){float s=.5+.5*sin(p.x*3.+p.y*.5+p.z*2.+time*.8);gl_FragColor=vec4(mix(vec3(.21,.52,.52),vec3(.75,.89,.79),s*.45),.84);}'});ownedMaterials.add(waterMaterial);
 const rp=[],ri=[];for(let j=1;j<streamPoints.length;j++){const a=streamPoints[j-1],c=streamPoints[j],n=28,dx=c[0]-a[0],dz=c[1]-a[1],length=Math.hypot(dx,dz),offset=rp.length/3;for(let i=0;i<=n;i++){const t=i/n,x=a[0]+dx*t,z=a[1]+dz*t,y=groundHeight(x,z)+.075;for(const s of[-1,1])rp.push(x-dz/length*s*.7,y,z+dx/length*s*.7);if(i<n){const k=offset+i*2;ri.push(k,k+2,k+1,k+1,k+2,k+3);}}}
 const rg=new T.BufferGeometry();rg.setAttribute('position',new T.Float32BufferAttribute(rp,3));rg.setIndex(ri);rg.computeVertexNormals();const river=b.mesh(rg,waterMaterial);river.name='Valley stream';river.castShadow=false;
 const end=streamPoints.at(-1),endY=groundHeight(end[0],end[1]),fall=b.mesh(new T.PlaneGeometry(1.8,74,2,25),waterMaterial,end[0]-.45,endY-37,end[1]+.25);fall.rotation.y=-1.1;fall.name='Cloudbreak waterfall';fall.castShadow=false;
 const dispose=()=>{if(disposed)return;disposed=true;signal?.removeEventListener('abort',dispose);const gs=new Set(b.owned),ms=new Set(ownedMaterials),ts=new Set();scene.traverse(o=>{if(o.isInstancedMesh)o.dispose();if(o.geometry)gs.add(o.geometry);for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])ms.add(m);});for(const g of gs)g.dispose();for(const m of ms){for(const t of Object.values(m))if(t?.isTexture)ts.add(t);m.dispose();}for(const t of ts)t.dispose();materials.dispose();library.dispose();sun.shadow.dispose();scene.clear();};
 try{
  const nature=await dressLandscape({scene,b,standard,library,obstacles,stats,ownedMaterials,signal});b.flush();scene.updateMatrixWorld(true);
  world={scene,obstacles,materials,library,stats,terrain,groundHeight,dispose,settlement:null,update(time,reduced,camera){waterMaterial.uniforms.time.value=reduced?0:time;atmosphere.update(time,reduced,camera);nature.update(time,reduced);}};
  if(signal?.aborted){dispose();throw Error('Landscape load cancelled');}signal?.addEventListener('abort',dispose,{once:true});
  Object.assign(stats,{files:library.stats(),geometry:modelMetrics(scene),surfaceTriangles:terrainInfo.triangles,sourceFiles:['canopy-tree.glb','fern.glb'],cloudCount:atmosphere.cloudCount,settlement:null});
  if(stats.geometry.missingTextures.length)throw Error('Landscape texture missing');return world;
 }catch(error){dispose();throw error;}
}
