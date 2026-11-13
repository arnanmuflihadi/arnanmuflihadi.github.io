import * as T from '../vendor/three-rpg.module.js';
import {createWorld} from './world.js';
import {createInput} from './input-manager.js';
import {createPlayer} from './player-controller.js';
import {createCamera} from './third-person-camera.js';
import {drawMinimap} from './minimap.js';
import {blocked} from './collision-system.js';
import {district} from './district.js';
export function createGame(root, api) {
  const canvas=root.querySelector('[data-world]'),renderer=new T.WebGLRenderer({canvas,antialias:innerWidth>700,powerPreference:'low-power'});
  renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;
  renderer.setPixelRatio(Math.min(devicePixelRatio,innerWidth<700?1.25:1.7));renderer.shadowMap.enabled=innerWidth>=700;
  const world=createWorld(),player=createPlayer(world.scene,district.spawn),follow=createCamera();
  if(api.savedPosition&&!blocked(api.savedPosition.x,api.savedPosition.z,world.obstacles))player.group.position.set(api.savedPosition.x,0,api.savedPosition.z);
  const reduced=matchMedia('(prefers-reduced-motion: reduce)'),map=root.querySelector('[data-minimap]'),prompt=root.querySelector('[data-interact]');
  let active=false,paused=false,frame=0,last=0,near=null,elapsed=0,frames=0,measure=0;
  const input=createInput(canvas,root,key=>{
    if(key==='e'&&!paused&&near)api.encounter(near.projectId);
    if(key==='m')root.querySelector('[data-map-wrap]').hidden=!root.querySelector('[data-map-wrap]').hidden;
    if(key==='escape'){paused=!paused;input.clear();root.querySelector('[data-pause]').textContent=paused?'Resume walk':'Pause';}
  });
  const resize=()=>{const w=root.clientWidth,h=root.clientHeight;renderer.setSize(w,h,false);follow.camera.aspect=w/h;follow.camera.updateProjectionMatrix();};
  const observer=new ResizeObserver(resize);observer.observe(root);
  function tick(now){frame=0;if(!active||document.hidden)return;
    const wallDt=last?(now-last)/1000:.016;const dt=Math.min(.05,wallDt);last=now;
    if(!paused&&!api.panelOpen())player.update(dt,input,world.obstacles,reduced.matches);else {input.clear();player.stop();}
    follow.update(player.group,input,world.cameraObjects,dt,reduced.matches);
    const next=district.landmarks.find(l=>Math.hypot(l.focus.x-player.group.position.x,l.focus.z-player.group.position.z)<4.7)||null;
    if(next!==near){near=next;prompt.disabled=!near;prompt.textContent=near?`E · Inspect ${near.projectId==='transit'?'transit station':'business plaza'}`:'Walk toward a numbered research marker';}
    elapsed+=dt;world.markers.forEach(m=>{m.rotation.y=reduced.matches?0:elapsed*.65;});
    drawMinimap(map,player.group.position,input.yaw,api.progress());
    renderer.render(world.scene,follow.camera);frames++;measure+=wallDt;
    if(measure>=2){root.dataset.fps=String(Math.round(frames/measure));frames=0;measure=0;}
    api.position({x:player.group.position.x,z:player.group.position.z});
    root.dataset.playerX=player.group.position.x.toFixed(3);root.dataset.playerZ=player.group.position.z.toFixed(3);
    frame=requestAnimationFrame(tick);
  }
  const quality=()=>{renderer.shadowMap.enabled=!renderer.shadowMap.enabled;};document.addEventListener('rpg:quality',quality);
  const visibility=()=>{input.clear();player.stop();cancelAnimationFrame(frame);frame=0;if(active&&!document.hidden){last=0;frame=requestAnimationFrame(tick);}};
  document.addEventListener('visibilitychange',visibility);
  const lost=e=>{e.preventDefault();stop();api.error('The 3D graphics context was interrupted. Return to your portfolio, then reload to retry.');};canvas.addEventListener('webglcontextlost',lost);
  function stop(){active=false;cancelAnimationFrame(frame);frame=0;input.clear();player.stop();}
  prompt.addEventListener('click',()=>{if(near&&!paused)api.encounter(near.projectId);});
  const pauseButton=root.querySelector('[data-pause]');pauseButton.addEventListener('click',()=>{paused=!paused;input.clear();pauseButton.textContent=paused?'Resume walk':'Pause';});
  return {start(){active=true;resize();visibility();canvas.focus({preventScroll:true});},stop,
    focus(id){const l=district.landmarks.find(l=>l.projectId===id);if(l){player.group.position.set(l.focus.x,0,l.focus.z);player.stop();follow.reset();}},
    destroy(){stop();observer.disconnect();document.removeEventListener('rpg:quality',quality);document.removeEventListener('visibilitychange',visibility);canvas.removeEventListener('webglcontextlost',lost);input.destroy();world.dispose();renderer.dispose();}};
}
