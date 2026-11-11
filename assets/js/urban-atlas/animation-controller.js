import {AnimationMixer,MathUtils,LoopOnce,LoopRepeat} from '../vendor/three-atlas.module.js?v=16';
import {locomotion} from './player-controller.js?v=22';
export function createAnimationController(model,clips,scale){
  const mixer=new AnimationMixer(model),actions={};
  for(const name of ['Idle','Walk','Run']){
    const clip=clips.find(c=>c.name===name);if(!clip)throw new Error(`Character GLB is missing ${name}`);
    actions[name]=mixer.clipAction(clip);actions[name].setEffectiveWeight(name==='Idle'?1:0).play();
  }
  let current='Idle',override=null,overrideWeight=0;const weights={Idle:1,Walk:0,Run:0};
  function addClips(extra){for(const clip of extra)if(!actions[clip.name]){actions[clip.name]=mixer.clipAction(clip);actions[clip.name].clampWhenFinished=true;}}
  addClips(clips.filter(c=>!['Idle','Walk','Run'].includes(c.name)));
  function setOverride(name,{duration,loop=false}={}){
    if(name===override)return;
    if(override)actions[override]?.fadeOut(.12);
    override=actions[name]?name:null;
    if(override){const action=actions[override];action.reset().setLoop(loop?LoopRepeat:LoopOnce,loop?Infinity:1).setEffectiveWeight(1).setEffectiveTimeScale(1);if(duration)action.setDuration(duration);action.fadeIn(.08).play();}
  }
  return {mixer,actions,weights,addClips,setOverride,get state(){return override||current;},
    update(dt,speed){
      const moving=MathUtils.smoothstep(speed,.04,.45);
      const running=MathUtils.smoothstep(speed,locomotion.walkSpeed+.05,locomotion.runSpeed-.4);
      const target={Idle:1-moving,Walk:moving*(1-running),Run:moving*running};
      const next=speed<.12?'Idle':running>.5?'Run':'Walk';
      // Preserve gait phase across walk/run changes; never restart a clip per frame.
      if(next!==current&&next!=='Idle'&&current!=='Idle'){
        actions[next].time=(actions[current].time/actions[current].getClip().duration)*actions[next].getClip().duration;
      }
      current=next;const blend=1-Math.exp(-dt/ .12);
      overrideWeight+=(Number(Boolean(override))-overrideWeight)*(1-Math.exp(-dt/.08));
      for(const name of ['Idle','Walk','Run']){
        weights[name]+=(target[name]-weights[name])*blend;
        actions[name].setEffectiveWeight(weights[name]*(1-overrideWeight));
      }
      actions.Walk.setEffectiveTimeScale(speed/(locomotion.walkClipSpeed*scale));
      actions.Run.setEffectiveTimeScale(speed/(locomotion.runClipSpeed*scale));
      mixer.update(dt);
    },
    reset(){if(override)actions[override].stop();override=null;overrideWeight=0;for(const name of ['Idle','Walk','Run']){actions[name].reset().play();weights[name]=name==='Idle'?1:0;actions[name].setEffectiveWeight(weights[name]);}current='Idle';mixer.update(0);},
    dispose(){mixer.stopAllAction();mixer.uncacheRoot(model);},
  };
}
