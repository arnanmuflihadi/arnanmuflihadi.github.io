import * as T from '../vendor/three-atlas.module.js?v=16';
import {createMaterials} from './materials.js?v=22';
import {createBuilder} from './geometry.js?v=22';
import {buildArchitecture} from './architecture.js?v=40';
import {buildEnvironment} from './environment.js?v=40';
import {assembleDistrictAssets} from './district-assets.js?v=40';
export function createDistrict(){
  const scene=new T.Scene();scene.background=new T.Color('#d4e1dc');scene.fog=new T.Fog('#c6d9d2',95,240);
  const materials=createMaterials(),builder=createBuilder(scene,materials),obstacles=[];
  scene.add(new T.HemisphereLight('#e9f1f5','#82917c',2.0));
  const sun=new T.DirectionalLight('#fff0d9',2.3);sun.position.set(-32,48,22);sun.target.position.set(0,0,5);scene.add(sun.target);scene.add(sun);
  sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-49,right:49,top:49,bottom:-49,near:1,far:120});sun.shadow.normalBias=.025;sun.shadow.bias=-.0001;sun.shadow.radius=4;
  const architecture=buildArchitecture(scene,builder,materials,obstacles);
  const environment=buildEnvironment(scene,builder,materials,obstacles);builder.flush();scene.updateMatrixWorld(true);
  let assets=null,assetPromise=null,disposed=false;
  return {scene,materials,obstacles,sun,update:environment.update,
    loadAssets(options={}){if(disposed)return Promise.reject(Error('District disposed'));if(!assetPromise)assetPromise=assembleDistrictAssets(scene,{...options,obstacles}).then(value=>{if(disposed){value.dispose();throw Error('District disposed during asset loading');}assets=value;return value;}).catch(error=>{assetPromise=null;throw error;});return assetPromise;},
    dispose(){if(disposed)return;disposed=true;assets?.dispose();architecture.dispose();const geometry=new Set(),mats=new Set(),textures=new Set();scene.traverse(o=>{if(o.geometry)geometry.add(o.geometry);for(const material of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])mats.add(material);if(o.isInstancedMesh)o.dispose();});geometry.forEach(g=>g.dispose());mats.forEach(m=>{for(const value of Object.values(m))if(value?.isTexture)textures.add(value);m.dispose();});textures.forEach(t=>t.dispose());materials.dispose();sun.shadow.dispose();},
  };
}
