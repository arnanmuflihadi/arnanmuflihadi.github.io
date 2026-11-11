import * as T from '../vendor/three-atlas.module.js?v=16';
import {groundHeight} from './layout.js?v=40';
import {createPlayerController} from './player-controller.js?v=50';
import {createAnimationController} from './animation-controller.js?v=22';
export const characterUrl=new URL('../../game/characters/urban-explorer/urban-explorer.glb',import.meta.url);
// All visible geometry, weights, bones and clips come from the licensed GLB.
export async function createCharacter(scene,materials,spawn,{gltf,heightAt=groundHeight,movementOptions={}}={}){
  const asset=gltf||await new T.GLTFLoader().loadAsync(characterUrl.href);
  const jumpAsset=gltf?null:await new T.GLTFLoader().loadAsync(new URL('../../game/characters/urban-explorer/jump-animations.glb',import.meta.url).href);
  const root=new T.Group();root.name='ExplorerMovementRoot';root.position.set(spawn.x,heightAt(spawn.x,spawn.z),spawn.z);root.rotation.y=Math.PI;
  const visual=new T.Group();visual.name='ExplorerVisual';root.add(visual);
  const model=asset.scene;model.name='QuaterniusAdventurer';visual.add(model);
  model.updateMatrixWorld(true);
  const bounds=new T.Box3().setFromObject(model),scale=1.9/(bounds.max.y-bounds.min.y);
  visual.scale.setScalar(scale);model.position.y=-bounds.min.y;
  // Preserve the source standard materials and skinning; no arbitrary shader swap.
  let meshCount=0,triangles=0;
  model.traverse(object=>{
    if(!object.isMesh)return;
    if(!object.isSkinnedMesh)throw new Error('Expected a genuinely skinned character mesh');
    meshCount++;triangles+=object.geometry.index.count/3;
    object.castShadow=true;object.receiveShadow=true;
    // Animated limbs may exceed bind-pose bounds. Avoid culling them mid-gait.
    object.frustumCulled=false;
  });
  if(!meshCount)throw new Error('Character GLB did not contain a skinned mesh');
  const animator=createAnimationController(model,asset.animations,scale),movement=createPlayerController(root,{heightAt,...movementOptions}),poseBounds=new T.Box3();
  let poseClearance=0,poseSettling=0;
  if(jumpAsset)animator.addClips(jumpAsset.animations);animator.reset();scene.add(root);
  return {root,model,visual,animator,movement,scale,meshCount,triangles,
    update(dt,input,obstacles,reduced,commands={}){
      const motion=movement.update(dt,input,obstacles,commands);
      const jumpPose={takeoff:'JumpStart',airborne:'JumpAir',landing:'JumpLand'}[motion.phase];
      if(jumpPose&&(!animator.state||['Idle','Walk','Run','JumpStart','JumpAir','JumpLand'].includes(animator.state)))animator.setOverride(jumpPose,{duration:jumpPose==='JumpStart'?.23:jumpPose==='JumpLand'?.22:1,loop:jumpPose==='JumpAir'});
      else if(!jumpPose&&animator.state.startsWith('Jump'))animator.setOverride(null);
      // Authored locomotion remains functional with reduced motion; no extra camera/body bob.
      animator.update(dt,motion.speed);
      // Authored rolls/falls can dip below their bind-pose floor during crossfades.
      // Fit only the visual, using the actual skinned pose; physics stays stable.
      // The vertex scan runs solely during these actions and brief settling.
      poseSettling=['Dodge','Defeat','JumpStart','JumpLand'].includes(animator.state)?.18:Math.max(0,poseSettling-dt);
      if(poseSettling>0){
        visual.position.y=0;root.updateMatrixWorld(true);
        model.traverse(o=>{if(o.isSkinnedMesh)o.computeBoundingBox();});poseBounds.setFromObject(model);
        poseClearance=Math.max(0,root.position.y+.002-poseBounds.min.y);visual.position.y=poseClearance;root.updateMatrixWorld(true);
      }else if(poseClearance>0){poseClearance=0;visual.position.y=0;}
      return {...motion,state:animator.state,animationTime:animator.actions[animator.state].time};
    },
    stop(){movement.stop();},reset(){movement.settle();animator.reset();poseClearance=0;poseSettling=0;visual.position.y=0;},
    dispose(){animator.dispose();const skeletons=new Set();model.traverse(o=>{if(o.isSkinnedMesh)skeletons.add(o.skeleton);});skeletons.forEach(s=>s.dispose());},
  };
}
