import * as T from '../vendor/three-atlas.module.js?v=16';
import{groundHeight}from'./layout.js?v=22';
import{createAnimationController}from'./animation-controller.js?v=22';
export function createRiggedActor(scene,asset,{x=0,z=0,height=1.8,shirt,hair,pants,clone=true}={}){
  const model=clone?T.cloneSkeleton(asset.scene):asset.scene,root=new T.Group(),visual=new T.Group(),ownedMaterials=[];
  root.add(visual);visual.add(model);model.updateMatrixWorld(true);
  const box=new T.Box3().setFromObject(model),scale=height/(box.max.y-box.min.y);visual.scale.setScalar(scale);model.position.y=-box.min.y;
  model.traverse(o=>{if(!o.isMesh)return;o.castShadow=true;o.receiveShadow=true;o.frustumCulled=false;
    if(shirt||hair||pants){const alter=m=>{const color=m.name==='Hair'?hair:m.name==='LightBlue'?pants:['LightBrown','Green','LightGreen'].includes(m.name)?shirt:null;if(!color)return m;const copy=m.clone();copy.color.set(color);ownedMaterials.push(copy);return copy;};o.material=Array.isArray(o.material)?o.material.map(alter):alter(o.material);}
  });
  root.position.set(x,groundHeight(x,z),z);scene.add(root);
  const animator=createAnimationController(model,asset.animations,scale);
  animator.reset();
  return{root,model,animator,scale,dispose(){root.removeFromParent();animator.dispose();const skeletons=new Set();model.traverse(o=>{if(o.isSkinnedMesh)skeletons.add(o.skeleton);});skeletons.forEach(s=>s.dispose());ownedMaterials.forEach(m=>m.dispose());}};
}
export function disposeAsset(asset){const g=new Set(),m=new Set(),t=new Set();asset.scene.traverse(o=>{if(o.geometry)g.add(o.geometry);for(const material of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])m.add(material);});g.forEach(v=>v.dispose());m.forEach(v=>{for(const x of Object.values(v))if(x?.isTexture)t.add(x);v.dispose();});t.forEach(v=>v.dispose());}
