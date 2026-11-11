import * as T from '../vendor/three-atlas.module.js?v=16';
import {buildImportedArchitecture} from './architectural-prefabs.js?v=22';
import {treeSites,planterSites,groundHeight} from './layout.js?v=22';
const assetUrl=id=>new URL(`../../game/scenery/${id}.glb${id==='architecture-library'?'?v=30':''}`,import.meta.url).href;
// Actual, locally delivered CC0 models; no fetch to an asset service at runtime.
export async function enhanceScenery(scene,{eco=false,signal}={}){
  const loader=new T.GLTFLoader(),trees=[],container=new T.Group();let alive=true;
  const ids=['canopy-tree','fern','architecture-library',...(!eco?['city-planter']:[])];
  const results=await Promise.allSettled(ids.map(id=>loader.loadAsync(assetUrl(id))));
  const assets=results.filter(r=>r.status==='fulfilled').map(r=>r.value);
  const hidden=[];
  function dispose(){
    if(!alive)return;
    alive=false;container.traverse(o=>{if(o.isInstancedMesh)o.dispose();});hidden.forEach(o=>o.visible=true);
    const geometries=new Set(),materials=new Set(),textures=new Set();
    container.traverse(o=>{if(o.geometry)geometries.add(o.geometry);for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])materials.add(m);});container.removeFromParent();
    for(const asset of assets)asset.scene.traverse(o=>{if(o.geometry)geometries.add(o.geometry);for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])materials.add(m);});
    geometries.forEach(g=>g.dispose());materials.forEach(m=>{for(const value of Object.values(m))if(value?.isTexture)textures.add(value);m.dispose();});textures.forEach(t=>t.dispose());
  }
  if(signal?.aborted||results.some(r=>r.status==='rejected')){dispose();throw new Error('Scenery load cancelled or unavailable');}
  signal?.addEventListener('abort',dispose,{once:true});scene.add(container);
  const [treeAsset,fernAsset,architecture,planter]=assets;
  architecture.scene.traverse(o=>{if(o.isMesh&&o.material.aoMap)o.material.aoMapIntensity=.3;});
  let buildings;try{buildings=buildImportedArchitecture(architecture);}catch(error){dispose();throw error;}container.add(buildings);
  container.userData.prefabCounts=buildings.userData.prefabCounts;
  scene.traverse(o=>{if(['placeholder-station','placeholder-office','placeholder-shops','placeholder-civic','legacy-residential-west','residential-east','context-fallbacks'].includes(o.userData.atlasGroup)){hidden.push(o);o.visible=false;}});
  treeAsset.scene.traverse(o=>{if(o.isMesh&&o.material.name.includes('Leaves')){o.material.emissive.set('#526741');o.material.emissiveIntensity=.08;}});
  function place(source,{x,z,height,width=Infinity,depth=Infinity,rotation=0}){
    const model=source.clone(true),box=new T.Box3().setFromObject(model),size=box.getSize(new T.Vector3());
    const scale=Math.min(height/size.y,width/size.x,depth/size.z),group=new T.Group();
    model.position.set(-(box.min.x+box.max.x)/2,-box.min.y,-(box.min.z+box.max.z)/2);group.add(model);group.scale.setScalar(scale);group.position.set(x,groundHeight(x,z),z);group.rotation.y=rotation;
    group.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=false;}});container.add(group);return group;
  }
  for(const[x,z,size]of treeSites){const tree=place(treeAsset.scene,{x,z,height:5.8*size,rotation:(x+z)*.17});tree.userData.canopySize=size;trees.push(tree);}
  scene.traverse(o=>{if(o.userData.atlasGroup==='legacy-trees'){hidden.push(o);o.visible=false;}});
  for(const[x,z]of[[-17,15],[-18,17],[17,15],[18,17],[-31,9],[27,8.5],[-24,16],[33,16.8]])place(fernAsset.scene,{x,z,height:.8,width:1.7,depth:1.7,rotation:x});
  if(!eco){

    for(const[x,z]of planterSites)place(planter.scene,{x,z,height:.75,width:1.3,depth:1.3});
  }
  scene.updateMatrixWorld(true);
  return {prefabCounts:container.userData.prefabCounts,update(t,reduced){if(!alive||reduced)return;trees.forEach((tree,i)=>{tree.rotation.z=Math.sin(t*.4+i)*.003;});},
    frameCamera(camera,adventure){
      // Cut only nearby leaf meshes when the follow camera enters a canopy.
      // Mesh visibility is per instance; shared materials/other trees stay intact.
      for(const tree of trees){const size=tree.userData.canopySize,d=Math.hypot(camera.position.x-tree.position.x,camera.position.z-tree.position.z),limit=(tree.userData.cutCanopy?4.8:4.2)*size;
        const cut=adventure&&d<limit&&camera.position.y>size*1.6&&camera.position.y<size*8.5;tree.userData.cutCanopy=cut;
        tree.traverse(o=>{if(o.isMesh&&o.material.name.includes('Leaves'))o.visible=!cut;});
      }
    },dispose(){signal?.removeEventListener('abort',dispose);dispose();}};
}
