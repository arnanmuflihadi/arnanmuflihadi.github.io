import * as T from'../vendor/three-atlas.module.js?v=16';
import{createModelLibrary,modelMetrics}from'../urban-atlas/model-library.js?v=15';
import{createBuilder}from'../urban-atlas/geometry.js?v=22';
import{createMaterials}from'../urban-atlas/materials.js?v=22';
import{createTerrainGeometry,createCliffGeometry,groundHeight,terrainInfo}from'./terrain.js?v=73';
import{reservations}from'./plan.js?v=73';
import{dressLandscape}from'./nature.js?v=73';
import{createAtmosphere,distantIslandGeometry}from'./atmosphere.js?v=73';
import{dressCliff}from'./geology.js?v=73';
import{createWaterfall}from'./waterfall.js?v=73';
export async function createFloatingWorld({library=createModelLibrary(),signal}={}){
 const scene=new T.Scene();scene.background=new T.Color('#8bb0c0');scene.fog=new T.Fog('#8bb0c0',170,900);
 const materials=createMaterials(),b=createBuilder(scene,materials),obstacles=[],ownedMaterials=new Set(),stats={world:'Transit Kingdom / Landscape',revision:'R0A3.73',terrainOnly:true,architectureInstances:0,reservations,imported:{},terrain:terrainInfo.dimensions};let disposed=false,world;
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
 const geology=dressCliff({cliffs,b,standard,stats}),waterfall=createWaterfall({scene,b,standard,ownedMaterials,rocks:geology.rocks,rockMaterial:geology.material,stats});
 const dispose=()=>{if(disposed)return;disposed=true;signal?.removeEventListener('abort',dispose);const gs=new Set(b.owned),ms=new Set(ownedMaterials),ts=new Set();scene.traverse(o=>{if(o.isInstancedMesh)o.dispose();if(o.geometry)gs.add(o.geometry);for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])ms.add(m);});for(const g of gs)g.dispose();for(const m of ms){for(const t of Object.values(m))if(t?.isTexture)ts.add(t);m.dispose();}for(const t of ts)t.dispose();materials.dispose();library.dispose();sun.shadow.dispose();scene.clear();};
 try{
  const nature=await dressLandscape({scene,b,standard,library,obstacles,stats,ownedMaterials,signal,cliffLedges:cliffs.geometry.userData.ledges});b.flush();scene.updateMatrixWorld(true);
  world={scene,obstacles,materials,library,stats,terrain,groundHeight,dispose,settlement:null,waterfall,setQuality:eco=>nature.setEco(eco),update(time,reduced,camera){waterfall.update(time,reduced,camera);atmosphere.update(time,reduced,camera);nature.update(time,reduced,camera);}};
  if(signal?.aborted){dispose();throw Error('Landscape load cancelled');}signal?.addEventListener('abort',dispose,{once:true});
  Object.assign(stats,{files:library.stats(),geometry:modelMetrics(scene),surfaceTriangles:terrainInfo.triangles,sourceFiles:['canopy-tree.glb','fern.glb'],cloudCount:atmosphere.cloudCount,settlement:null});
  if(stats.geometry.missingTextures.length)throw Error('Landscape texture missing');return world;
 }catch(error){dispose();throw error;}
}
