import * as T from '../vendor/three-atlas.module.js?v=16';

export const assetCatalog=Object.freeze({
  architecture:{url:new URL('../../game/scenery/architecture-library.glb?v=30',import.meta.url).href,license:'CC0-1.0'},
  tree:{url:new URL('../../game/scenery/canopy-tree.glb',import.meta.url).href,license:'CC0-1.0'},
  fern:{url:new URL('../../game/scenery/fern.glb',import.meta.url).href,license:'CC0-1.0'},
  planter:{url:new URL('../../game/scenery/city-planter.glb',import.meta.url).href,license:'CC0-1.0'}
});

export function modelMetrics(root){
  let meshes=0,triangles=0;const geometries=new Set(),materials=new Set(),textures=new Set();
  root.traverse(o=>{if(!o.isMesh)return;meshes++;geometries.add(o.geometry);
    triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3*(o.isInstancedMesh?o.count:1);
    for(const m of Array.isArray(o.material)?o.material:[o.material]){materials.add(m);for(const value of Object.values(m))if(value?.isTexture)textures.add(value);}
  });
  return {meshes,triangles,geometries:geometries.size,materials:materials.size,textures:textures.size,
    missingTextures:[...textures].filter(t=>!((t.image?.width||t.image?.naturalWidth)>0&&(t.image?.height||t.image?.naturalHeight)>0)).map(t=>t.name||t.uuid)};
}

export function createModelLibrary({load=url=>new T.GLTFLoader().loadAsync(url),catalog=assetCatalog}={}){
  const pending=new Map(),assets=new Set(),finishes=new Map();let disposed=false,requests=0;
  function release(asset){
    const geometries=new Set(),materials=new Set(),textures=new Set();
    asset.scene.traverse(o=>{if(o.geometry)geometries.add(o.geometry);for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])materials.add(m);});
    geometries.forEach(g=>g.dispose());materials.forEach(m=>{for(const v of Object.values(m))if(v?.isTexture)textures.add(v);m.dispose();});
    textures.forEach(t=>t.dispose());
  }
  function get(id){
    if(disposed)return Promise.reject(Error('Model library has been disposed'));
    const entry=catalog[id];if(!entry)return Promise.reject(Error(`Unknown asset ${id}`));
    if(!pending.has(entry.url)){
      requests++;
      const request=Promise.resolve().then(()=>load(entry.url)).then(asset=>{
        if(disposed){release(asset);throw Error('Model library disposed during loading');}
        if(!asset.scene||!modelMetrics(asset.scene).meshes){if(asset.scene)release(asset);throw Error(`No imported meshes in ${id}`);}
        assets.add(asset);return asset;
      }).catch(error=>{pending.delete(entry.url);throw Error(`Could not load ${id}: ${error.message}`,{cause:error});});
      pending.set(entry.url,request);
    }
    return pending.get(entry.url);
  }
  function palette(material){
    if(finishes.has(material.uuid))return finishes.get(material.uuid);
    const m=material.clone();m.metalness=0;m.roughness=.86;if(m.aoMap)m.aoMapIntensity=.3;
    // Downtown vertex colors encode the source engine's wear controls, not façade paint.
    if(m.name.startsWith('MI_'))m.vertexColors=false;
    if(/RedBrick/.test(m.name))m.color.set('#ead8b5');
    if(/Concrete|Trim/.test(m.name))m.color.multiply(new T.Color('#f3e9d4'));
    if(/Glass|FakeInterior/.test(m.name)){m.color.set('#547e78');m.roughness=.48;m.envMapIntensity=.28;}
    if(/Ornaments/.test(m.name)){m.map=null;m.color.set('#9aa58d');}
    if(/Leaves/.test(m.name)){m.color.set('#c3d8a3');m.emissive.set('#91a475');m.emissiveIntensity=.25;if(m.aoMap)m.aoMapIntensity=0;}
    finishes.set(material.uuid,m);return m;
  }
  async function instantiate(id,{model,height=1,x=0,y=0,z=0,rotation=0,collidable=true,collision='bounds'}={}){
    if(!(height>0)||![height,x,y,z,rotation].every(Number.isFinite))throw Error('Invalid model transform');
    const asset=await get(id),source=model?asset.scene.getObjectByName(model):asset.scene;
    if(!source)throw Error(`Missing model ${model} in ${id}`);
    if(source.getObjectByProperty('isSkinnedMesh',true))throw Error('Use the character loader for skinned models');
    const meshRoot=source.clone(true),rotated=new T.Group();rotated.add(meshRoot);rotated.rotation.y=rotation;rotated.updateMatrixWorld(true);
    const bounds=new T.Box3().setFromObject(rotated),size=bounds.getSize(new T.Vector3());
    if(!(size.y>0))throw Error(`Empty bounds for ${id}/${model||'scene'}`);
    const scale=height/size.y,root=new T.Group();rotated.scale.setScalar(scale);
    rotated.position.set(-(bounds.min.x+bounds.max.x)*scale/2,-bounds.min.y*scale,-(bounds.min.z+bounds.max.z)*scale/2);
    root.add(rotated);root.position.set(x,y,z);root.name=model||id;
    root.traverse(o=>{if(!o.isMesh)return;o.material=Array.isArray(o.material)?o.material.map(palette):palette(o.material);o.castShadow=true;o.receiveShadow=true;});
    root.updateMatrixWorld(true);
    const worldBounds=new T.Box3().setFromObject(root),collisionBounds=worldBounds.clone();
    if(collision==='trunk'){
      const low=new T.Box3(),point=new T.Vector3(),ceiling=worldBounds.min.y+Math.min(height*.28,2);
      root.traverse(o=>{if(!o.isMesh)return;const positions=o.geometry.attributes.position;for(let i=0;i<positions.count;i++){point.fromBufferAttribute(positions,i).applyMatrix4(o.matrixWorld);if(point.y<=ceiling)low.expandByPoint(point);}});
      if(!low.isEmpty())collisionBounds.copy(low);
    }
    const extent=collisionBounds.getSize(new T.Vector3()),center=collisionBounds.getCenter(new T.Vector3());
    root.userData.imported={asset:id,model:model||null,url:catalog[id].url,license:catalog[id].license,scale,rotation};
    root.userData.collider=collidable?{x:center.x,z:center.z,w:extent.x,d:extent.z,minY:collisionBounds.min.y,h:collisionBounds.max.y}:null;
    return root;
  }
  return {get,instantiate,stats:()=>({requests,cachedFiles:pending.size,loadedFiles:assets.size}),dispose(){
    if(disposed)return;disposed=true;assets.forEach(release);finishes.forEach(m=>m.dispose());assets.clear();pending.clear();finishes.clear();
  }};
}
