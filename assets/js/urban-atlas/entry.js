import * as T from '../vendor/three-atlas.module.js?v=16';
import {createDistrict} from './scene.js?v=40';
import {createFollowCamera} from './camera.js?v=40';
import {createInput} from './input.js?v=22';
import {layout,groundHeight} from './layout.js?v=40';
import {blocked} from './collision.js?v=40';
import {presentations,presentationFor,landmarks,mixComposition} from './presentation.js?v=40';
import{createDistrictArtwork}from'./district-artwork.js?v=40';
import {createNameplates} from './npc-nameplates.js?v=22';
import{districtReviewViews}from'./district-review.js?v=40';
// A persistent scene serves editorial presentation AND control; the GLB loads on demand.
export async function mountUrbanAtlas(host,{mode='adventure',savedAdventure,onError=()=>{},onFrame=()=>{}}={}){
  const canvas=host.querySelector('canvas'),renderer=new T.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});
  renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1;renderer.shadowMap.type=T.PCFSoftShadowMap;
  const compact=innerWidth<700;renderer.setPixelRatio(Math.min(devicePixelRatio,compact?1.15:1.5));renderer.shadowMap.enabled=!compact;
  const district=createDistrict(),follow=createFollowCamera(),camera=follow.camera;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const isReduced=()=>reduced.matches||host.dataset.reducedMotion==='true';
  let character=null,characterLoading=null,adventure=null,life=null,active=false,paused=false,frame=0,last=0,time=0,frames=0,sample=0,totalFrames=0,firstEditorial=true,modeRequest=0;
  const yard={update(){}},lifeAbort=new AbortController();
  let currentMode=mode,composition=presentations.arrival,nearest=null,disposed=false,reviewPreset=null;
  const intervals=[],renderTimes=[],walkingIntervals=[];
  const frameStats=values=>{const sorted=[...values].sort((a,b)=>a-b),mean=values.reduce((a,b)=>a+b,0)/Math.max(1,values.length);return{samples:values.length,meanFrameMs:mean,medianFrameMs:sorted[Math.floor(sorted.length*.5)]||0,p95FrameMs:sorted[Math.floor(sorted.length*.95)]||0,measuredFps:mean?1000/mean:0};};
  const look=new T.Vector3(...composition.target),goalPosition=new T.Vector3(),goalTarget=new T.Vector3();
  host.dataset.sceneId=district.scene.uuid;host.dataset.rendererCount='1';host.dataset.characterReady='false';host.dataset.mode=mode;
  let scenery=null;const sceneryAbort=new AbortController();
  let lifeLoading=null;
  function ensureLife(){
    if(!lifeLoading)lifeLoading=import('./city-life.js?v=40').then(({createCityLife})=>createCityLife(district.scene,district.obstacles,{signal:lifeAbort.signal,researchOnly:true})).then(value=>{if(disposed){value?.dispose();return;}life=value;host.dataset.npcReady=String(Boolean(value));host.dataset.npcCount=String(value?.people.length||0);}).catch(error=>{lifeLoading=null;if(!disposed)console.warn('City residents unavailable; research and exploration remain accessible.',error);});
    return lifeLoading;
  }
  if(mode==='adventure')ensureLife();
  let sceneryLoading=null;
  function ensureScenery(){
    if(!sceneryLoading)sceneryLoading=district.loadAssets({signal:sceneryAbort.signal,artwork:createDistrictArtwork({anisotropy:renderer.capabilities.getMaxAnisotropy()})}).then(value=>{if(disposed){value.dispose();throw Error('District disposed');}scenery=value;host.dataset.sceneryReady='true';host.dataset.architecturalPrefabs=JSON.stringify(value.prefabCounts);host.dataset.districtAssets=JSON.stringify(value.stats);return value;}).catch(error=>{sceneryLoading=null;host.dataset.sceneryReady='error';throw error;});
    return sceneryLoading;
  }
  const nameplates=createNameplates(host,district.obstacles);
  const input=createInput(canvas,host,()=>host.dispatchEvent(new CustomEvent('atlas:pause')));input.enabled=mode==='adventure';
  const interact=e=>{if(e.key.toLowerCase()==='e'&&!e.repeat&&!e.defaultPrevented&&input.enabled&&currentMode==='adventure'&&!paused&&!document.querySelector('dialog[open]')&&!e.target.closest?.('button,a,input,select,textarea,[contenteditable=true]')){e.preventDefault();api.interact();}};
  addEventListener('keydown',interact);
  function resize(){const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
  const observer=new ResizeObserver(resize);observer.observe(host);
  async function ensureCharacter(){
    if(character)return character;
    if(!characterLoading)characterLoading=Promise.all([import('./character.js?v=40'),import('./adventure.js?v=40')]).then(async([{createCharacter},{createAdventure}])=>{
      const actor=await createCharacter(district.scene,district.materials,layout.spawn);
      if(disposed){actor.dispose();throw new Error('Atlas was disposed during loading');}
      character=actor;adventure=createAdventure({scene:district.scene,character,input,obstacles:district.obstacles,life:()=>life,yard,saved:savedAdventure,explorationOnly:true,onEvent:type=>host.dispatchEvent(new CustomEvent('atlas:adventure-event',{detail:{type}}))});host.dataset.characterReady='true';return actor;
    }).catch(error=>{characterLoading=null;throw error;});
    return characterLoading;
  }
  function tick(now){
    frame=0;if(!active||document.hidden||disposed)return;
    const measured=Boolean(last),wallDt=last?(now-last)/1000:.016,dt=Math.min(.04,wallDt);last=now;
    if(!paused){time+=dt;district.update(time,isReduced());scenery?.update(time,isReduced());life?.update(dt,currentMode==='adventure'&&character?character.root.position:camera.position,character?.root.position);}
    let moving=false;
    if(currentMode==='adventure'&&character){
      if(!paused){input.updateCamera(dt);const motion=adventure.update(dt,isReduced());moving=motion.speed>.1;host.dataset.locomotion=motion.state;host.dataset.animationTime=motion.animationTime.toFixed(3);}else character.stop();
      follow.update(character.root,input,district.obstacles,dt,isReduced());
      nearest=landmarks.find(l=>Math.hypot(l.x-character.root.position.x,l.z-character.root.position.z)<l.radius)||null;
    }else{
      character?.stop();if(character&&!paused&&!isReduced())character.animator.update(dt,0);nearest=null;goalPosition.fromArray(composition.position);goalTarget.fromArray(composition.target);
      const blend=firstEditorial||isReduced()?1:1-Math.exp(-4.5*dt);camera.position.lerp(goalPosition,blend);look.lerp(goalTarget,blend);camera.lookAt(look);firstEditorial=false;
    }
    if(reviewPreset&&input.keys.size+input.touch.size>0){reviewPreset=null;host.dataset.viewpoint='live-follow';intervals.length=renderTimes.length=walkingIntervals.length=0;}
    if(reviewPreset){camera.fov=50;camera.position.fromArray(reviewPreset.position);camera.lookAt(new T.Vector3(...reviewPreset.target));camera.updateProjectionMatrix();}else if(camera.fov!==60){camera.fov=60;camera.updateProjectionMatrix();}
    scenery?.frameCamera?.(camera,currentMode==='adventure');const renderStart=performance.now();renderer.render(district.scene,camera);const renderMs=performance.now()-renderStart;
    if(measured&&totalFrames>60&&!paused){intervals.push(wallDt*1000);renderTimes.push(renderMs);if(moving){walkingIntervals.push(wallDt*1000);if(walkingIntervals.length>600)walkingIntervals.shift();}if(intervals.length>600){intervals.shift();renderTimes.shift();}}
    nameplates.update(dt,camera,life?.people||[],character?.root.position,host.dataset.selectedProject,currentMode==='adventure');frames++;sample+=wallDt;host.dataset.frames=String(++totalFrames);
    host.dataset.reviewEvidence=JSON.stringify({view:reviewPreset?.label||'live follow',camera:{position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),fov:camera.fov,aspect:camera.aspect},player:character?.root.position.toArray(),sceneId:district.scene.uuid});
    if(character){host.dataset.jumpPhase=character.movement.phase;host.dataset.grounded=String(character.movement.grounded);host.dataset.verticalVelocity=character.movement.verticalVelocity.toFixed(3);host.dataset.jumpCount=String(character.movement.jumps);host.dataset.landingCount=String(character.movement.landings);host.dataset.cameraY=camera.position.y.toFixed(3);host.dataset.playerY=character.root.position.y.toFixed(3);host.dataset.playerX=character.root.position.x.toFixed(3);host.dataset.playerZ=character.root.position.z.toFixed(3);host.dataset.poseClearance=character.visual.position.y.toFixed(3);}
    if(life)host.dataset.walkingResidents=String(life.people.filter(p=>p.actor.animator.state==='Walk').length);
    if(sample>=2){host.dataset.fps=String(Math.round(frames/sample));host.dataset.triangles=String(renderer.info.render.triangles);host.dataset.drawCalls=String(renderer.info.render.calls);const buffer=renderer.getDrawingBufferSize(new T.Vector2());host.dataset.performanceEvidence=JSON.stringify({...frameStats(intervals),walking:frameStats(walkingIntervals),meanRenderSubmissionMs:renderTimes.reduce((a,b)=>a+b,0)/Math.max(1,renderTimes.length),triangles:renderer.info.render.triangles,drawCalls:renderer.info.render.calls,viewport:[host.clientWidth,host.clientHeight],drawingBuffer:buffer.toArray(),pixelRatio:renderer.getPixelRatio(),shadows:renderer.shadowMap.enabled,mode:currentMode,userAgent:navigator.userAgent,metric:'Actual requestAnimationFrame intervals after 60-frame warmup; walking samples require measured displacement; submission time is CPU only'});frames=0;sample=0;}
    const story=adventure?.snapshot();if(story){host.dataset.questPhase=story.save.phase;host.dataset.enemyState=story.enemyState;host.dataset.playerHealth=String(story.playerHealth);host.dataset.enemyHealth=String(story.enemyHealth);}
    onFrame({mode:currentMode,position:character?{x:character.root.position.x,z:character.root.position.z}:null,yaw:input.yaw,near:nearest?.projectId||null,interaction:adventure?.getInteraction(),adventure:story,people:life?.people.map(p=>({x:p.actor.root.position.x,z:p.actor.root.position.z,id:p.spec.id,selected:p.spec.study===host.dataset.selectedProject}))});
    frame=requestAnimationFrame(tick);
  }
  function stop(){active=false;cancelAnimationFrame(frame);frame=0;input.clear();character?.stop();}
  function start(){if(active&&frame)return;active=true;last=0;resize();if(!document.hidden)frame=requestAnimationFrame(tick);}
  function visibility(){input.clear();character?.stop();cancelAnimationFrame(frame);frame=0;if(active&&!document.hidden){last=0;frame=requestAnimationFrame(tick);}}
  document.addEventListener('visibilitychange',visibility);
  const lost=e=>{e.preventDefault();stop();onError('The 3D view was interrupted. Your research remains available. Reload to restore the world.');};canvas.addEventListener('webglcontextlost',lost);
  function goToViewpoint(name){const view=layout.viewpoints[name];if(!view||!character)return;character.root.position.set(view.x,groundHeight(view.x,view.z),view.z);character.root.rotation.y=Math.PI;character.reset();input.clear();input.yaw=view.yaw;input.pitch=view.pitch;follow.reset();host.dataset.viewpoint=name;}
  const api={start,stop,goToViewpoint,ensureCharacter,mapData:district.obstacles.filter(o=>!o.cameraOnly),
    reviewView(id){const preset=districtReviewViews[id];if(!preset||!character)return false;const[x,z]=preset.player;if(!blocked(x,z,district.obstacles)){character.root.position.set(x,groundHeight(x,z),z);character.reset();}input.clear();reviewPreset=preset;host.dataset.viewpoint=id;intervals.length=renderTimes.length=walkingIntervals.length=0;return true;},
    getAdventureSave(){return adventure?.getSave()||savedAdventure;},getAdventureSnapshot(){return adventure?.snapshot();},getDialogue:interaction=>adventure?.dialogue(interaction),
    requestAdventureAction:action=>adventure?.request(action),speakTo:id=>life?.speak(id,character?.root.position),
    async interact(){const interaction=adventure?.getInteraction();if(interaction){if(interaction.kind==='device')await adventure.request('collect');host.dispatchEvent(new CustomEvent('atlas:dialogue',{detail:interaction}));}else if(nearest)host.dispatchEvent(new CustomEvent('atlas:interact',{detail:{projectId:nearest.projectId}}));},
    setEditorialComposition(a='arrival',b=a,t=0){composition=mixComposition(presentationFor(a),presentationFor(b),isReduced()?(t<.5?0:1):t);host.dataset.cameraPreset=t>.5?b:a;},
    async setMode(next,{focusProject=null,position=null}={}){
      const request=++modeRequest;
      input.clear();character?.stop();reviewPreset=null;
      if(next==='adventure'){
        await ensureScenery();ensureLife();
        const existed=Boolean(character),actor=await ensureCharacter();if(request!==modeRequest)return;
        const focus=presentations[focusProject]?.focus;
        const point=focus||(!existed?position:null);
        if(point&&Number.isFinite(point.x)&&Number.isFinite(point.z)&&!blocked(point.x,point.z,district.obstacles))actor.root.position.set(point.x,groundHeight(point.x,point.z),point.z);
        actor.reset();if(point||!existed){input.yaw=0;input.pitch=.19;}follow.handoff();
        currentMode='adventure';input.enabled=!paused;adventure.begin();
      }else{currentMode='editorial';input.enabled=false;adventure?.stop();firstEditorial=false;look.copy(character?.root.position||new T.Vector3(0,3,0));}
      host.dataset.mode=currentMode;
    },
    setPaused(value){paused=value;host.dataset.paused=String(value);input.enabled=currentMode==='adventure'&&!value;input.clear();character?.stop();if(!value&&currentMode==='adventure')canvas.focus({preventScroll:true});},
    setQuality(eco){renderer.setPixelRatio(Math.min(devicePixelRatio,eco?1:1.5));renderer.shadowMap.enabled=!eco;resize();},
    destroy(){disposed=true;sceneryAbort.abort();lifeAbort.abort();stop();observer.disconnect();document.removeEventListener('visibilitychange',visibility);removeEventListener('keydown',interact);removeEventListener('hashchange',reviewChange);canvas.removeEventListener('webglcontextlost',lost);input.destroy();nameplates.dispose();adventure?.dispose();character?.dispose();scenery?.dispose();district.dispose();renderer.dispose();},
  };
  const reviewChange=()=>{if(new URLSearchParams(location.search).has('district-review')&&location.hash.startsWith('#district-'))api.reviewView(location.hash.slice(10));};
  addEventListener('hashchange',reviewChange);
  try{await ensureScenery();}catch(error){api.destroy();throw error;}
  api.mapData=district.obstacles.filter(o=>!o.cameraOnly);
  if(mode==='adventure'){try{await ensureCharacter();goToViewpoint('plaza');}catch(error){api.destroy();throw error;}}
  else{camera.position.fromArray(composition.position);camera.lookAt(look);}
  return api;
}
