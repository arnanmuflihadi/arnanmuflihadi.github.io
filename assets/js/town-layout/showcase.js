import * as T from'../vendor/three-atlas.module.js?v=16';
import{createFloatingWorld}from'../floating-atlas/scene.js?v=73';
import{createCharacter}from'../urban-atlas/character.js?v=50';
import{createInput}from'../urban-atlas/input.js?v=22';
import{createFollowCamera}from'../urban-atlas/camera.js?v=50';
import{clearDistance}from'../floating-atlas/collision.js?v=73';
import{disposeAsset}from'../urban-atlas/rigged-actor.js?v=22';
import{modelMetrics}from'../urban-atlas/model-library.js?v=74';
import{projects}from'../project-registry.js';
import{mountBlockout}from'./blockout.js?v=composition-junction-final';
import{revision,selected,destinations,journeyRoutes,alternatives,surveyAlternative}from'./plan.js?v=composition-3';
import{views}from'./views.js?v=composition-3';

const host=document.querySelector('[data-town-review]'),canvas=host.querySelector('canvas'),status=host.querySelector('[data-status]'),selector=host.querySelector('[data-view]'),routeSelect=host.querySelector('[data-route]'),navigation=host.querySelector('[data-navigation]'),abort=new AbortController(),events={signal:abort.signal};
const renderer=new T.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'}),follow=createFollowCamera({distance:8.5,clearance:clearDistance}),camera=follow.camera;
renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.96;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.shadowMap.enabled=true;renderer.setPixelRatio(Math.min(devicePixelRatio,1.35));camera.far=1600;
let world,preview,actor,disposed=false,loading=false,frame=0,last=0,time=0,paused=false,current='aerial',orbit=null,drag=null,check=null,serial=0,measurement=0,frames=0;
const target=new T.Vector3(),point=new T.Vector3(),intervals=[],walking=[],cpu=[],checks=[],annotations=[],input=createInput(canvas,host,()=>pause(!paused));input.enabled=false;
for(const[id,v]of Object.entries(views)){const o=document.createElement('option');o.value=id;o.textContent=v.label;selector.append(o);}
for(const[id,r]of Object.entries(journeyRoutes)){const o=document.createElement('option');o.value=id;o.textContent=r.name;routeSelect.append(o);}
for(const p of projects){const a=document.createElement('a');a.href=p.caseStudyUrl;a.textContent=p.title;host.querySelector('[data-research]').append(a);}
const labels=host.querySelector('[data-plan-labels]');
for(const[id,text]of Object.entries({skyport:'1 · Pelabuhan Awan',market:'2 · Market Street',square:'3 · Town Square',guild:'4 · Atlas Guild',lookout:'5 · Highland Lookout'})){const el=document.createElement('div');el.className='plan-label';el.textContent=text;labels.append(el);annotations.push({el,id,position:destinations[id]});}
for(const lot of selected.lots.filter(l=>l.id!=='G')){const el=document.createElement('div');el.className='plan-label';el.textContent=lot.id;labels.append(el);annotations.push({el,id:lot.id,position:[lot.x,lot.z],height:lot.y+lot.h+.5,planOnly:true});}
const key=document.createElement('div');key.className='plan-key';key.innerHTML='<strong>N ↑</strong><span>Temporary town plan</span><span>Ochre paving · main street</span><span>Gravel · optional meadow loop</span><span>M1–M10 · commercial envelopes</span><span>G · research landmark</span>';labels.append(key);
function resize(){renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();}
const observer=new ResizeObserver(resize);observer.observe(host);
function resetMetrics(){intervals.length=walking.length=cpu.length=0;frames=0;}
function view(id){
 current=views[id]?id:'aerial';const v=views[current];selector.value=current;host.dataset.view=current;history.replaceState(null,'','#'+current);orbit=null;input.clear();input.enabled=current==='walk';follow.reset();
 if(v.eye&&preview){const[x,z]=v.eye,y=preview.heightAt(x,z)+1.65;camera.position.set(x,y,z);host.dataset.eyeHeight='1.65';}else{camera.position.fromArray(v.position||views.aerial.position);delete host.dataset.eyeHeight;}
 target.fromArray(v.target);camera.lookAt(target);if(v.quaternion)camera.quaternion.fromArray(v.quaternion);camera.fov=v.fov;camera.updateProjectionMatrix();host.querySelector('[data-place]').textContent=v.label.split(' / ')[0];key.hidden=current!=='plan';resetMetrics();
 if(actor&&current==='walk'&&!check){actor.root.position.set(27,preview.heightAt(27,60),60);actor.reset();input.yaw=0;canvas.focus({preventScroll:true});}
 if(actor&&current!=='walk'){actor.root.visible=['market','square','guild','arrival','trail'].includes(current);const p=current==='guild'?[40,5]:current==='square'?[33,9]:current==='market'?[37,30]:current==='trail'?[10,12]:[30,51];actor.root.position.set(p[0],preview.heightAt(...p),p[1]);actor.reset();}
 if(actor&&current==='walk')actor.root.visible=true;
}
function pause(value){paused=value;host.querySelector('[data-pause]').setAttribute('aria-pressed',String(value));host.querySelector('[data-pause]').textContent=value?'Resume atmosphere':'Pause atmosphere';}
function startCheck(){if(!actor||!preview.enabled)return;check=null;view('walk');const id=routeSelect.value,route=journeyRoutes[id],p=route.points[0];actor.root.position.set(p[0],preview.heightAt(p[0],p[1]),p[1]);actor.reset();actor.root.visible=true;follow.reset();check={id,run:++serial,waypoint:1,points:route.points,complete:false,elapsed:0,movingSeconds:0,distance:0,ascent:0,descent:0,blockedSeconds:0,maxSupportError:0,minCameraDistance:Infinity,maxCrossTrack:0,jumpsStart:actor.movement.jumps,landingsStart:actor.movement.landings,start:actor.root.position.toArray(),samples:[],guided:host.querySelector('[data-bearing]').checked};checks.push(check);navigation.textContent='Ready. Hold W to walk this route.';canvas.focus({preventScroll:true});}
function segmentDistance(x,z,a,b){const dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/Math.max(.000001,dx*dx+dz*dz)));return Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t);}
function updateCheck(dt,before,motion){
 if(!check||check.complete)return;const p=actor.root.position,q=check.points[check.waypoint],d=Math.hypot(p.x-q[0],p.z-q[1]),actual=p.distanceTo(before),requested=input.keys.has('w')||input.touch.has('w');
 check.elapsed+=dt;check.distance+=actual;if(actual>.001)check.movingSeconds+=dt;if(motion.grounded){check.ascent+=Math.max(0,p.y-before.y);check.descent+=Math.max(0,before.y-p.y);check.maxSupportError=Math.max(check.maxSupportError,Math.abs(p.y-preview.heightAt(p.x,p.z,p.y)));}
 if(requested&&motion.speed<.08)check.blockedSeconds+=dt;check.minCameraDistance=Math.min(check.minCameraDistance,camera.position.distanceTo(p));check.maxCrossTrack=Math.max(check.maxCrossTrack,segmentDistance(p.x,p.z,check.points[check.waypoint-1],q));
 if(frames%8===0)check.samples.push({position:p.toArray(),waypoint:check.waypoint,grounded:motion.grounded,phase:motion.phase,camera:camera.position.toArray()});
 if(d<.55){check.waypoint++;if(check.waypoint===check.points.length){check.complete=true;check.end=p.toArray();check.jumps=motion.jumps-check.jumpsStart;check.landings=motion.landings-check.landingsStart;input.clear();}}
 navigation.textContent=check.complete?'Route complete · '+check.distance.toFixed(1)+' m walked · '+check.blockedSeconds.toFixed(2)+' s blocked':journeyRoutes[check.id].name+' · waypoint '+check.waypoint+'/'+(check.points.length-1)+' · '+d.toFixed(1)+' m to next';
 host.dataset.navigation=JSON.stringify(check);host.dataset.checks=JSON.stringify(checks);
}
async function load(){if(loading||disposed)return;loading=true;delete host.dataset.error;host.querySelector('[data-retry]').hidden=true;const start=performance.now();try{
 world=await createFloatingWorld({signal:abort.signal});if(disposed){world.dispose();return;}preview=mountBlockout(world);
 actor=await createCharacter(world.scene,world.materials,{x:27,z:60},{heightAt:(x,z)=>preview.heightAt(x,z,actor?.root.position.y??Infinity),movementOptions:preview.movementOptions(()=>actor?.root.position.y??17.15)});if(disposed){release();return;}
 const inventory={revision,temporary:true,productionModified:false,planning:preview.metrics,landscape:modelMetrics(world.scene),character:{meshes:actor.meshCount,triangles:actor.triangles,height:1.9},envelopes:selected.lots.length,architectureGLBsLoaded:0,landscapeAssets:world.stats.imported,files:world.library.stats(),alternatives:alternatives.map(surveyAlternative)};
 host.dataset.inventory=JSON.stringify(inventory);host.dataset.ready='true';host.dataset.loadedMs=(performance.now()-start).toFixed(1);host.querySelector('[data-diagnostics]').textContent=JSON.stringify(inventory,null,2);status.textContent='Planning layer ready. Approved landscape retained. Owner review pending.';view(location.hash.slice(1)||'aerial');
 }catch(error){release();world?.dispose();world=null;status.textContent='Preview could not load: '+error.message;host.dataset.error=error.message;host.querySelector('[data-retry]').hidden=false;}finally{loading=false;}}
selector.addEventListener('change',()=>{check=null;view(selector.value);},events);addEventListener('hashchange',()=>{check=null;view(location.hash.slice(1));},events);host.querySelector('[data-start]').addEventListener('click',startCheck,events);host.querySelector('[data-retry]').addEventListener('click',load,events);
host.querySelector('[data-panel]').addEventListener('click',e=>{const hidden=host.classList.toggle('panel-hidden');e.currentTarget.textContent=hidden?'Show panel':'Hide panel';e.currentTarget.setAttribute('aria-expanded',String(!hidden));},events);
host.querySelector('[data-pause]').addEventListener('click',()=>pause(!paused),events);host.querySelector('[data-preview]').addEventListener('change',e=>{check=null;preview?.setEnabled(e.target.checked);if(actor){actor.root.position.set(27,preview.heightAt(27,60),60);actor.reset();}view(current);},events);
host.querySelector('[data-quality]').addEventListener('change',e=>{const eco=e.target.value==='eco';renderer.setPixelRatio(Math.min(devicePixelRatio,eco?1:1.35));renderer.shadowMap.enabled=!eco;world?.setQuality(eco);resize();resetMetrics();},events);
canvas.addEventListener('pointerdown',e=>{if(current==='walk')return;drag={x:e.clientX,y:e.clientY};const off=camera.position.clone().sub(target);orbit={yaw:Math.atan2(off.x,off.z),pitch:Math.asin(off.y/off.length()),distance:off.length()};canvas.setPointerCapture(e.pointerId);},events);for(const type of['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,()=>drag=null,events);
canvas.addEventListener('pointermove',e=>{if(!drag||!orbit)return;orbit.yaw-=(e.clientX-drag.x)*.005;orbit.pitch=Math.max(-.35,Math.min(1.56,orbit.pitch+(e.clientY-drag.y)*.005));drag={x:e.clientX,y:e.clientY};},events);
canvas.addEventListener('wheel',e=>{if(current==='walk')return;e.preventDefault();if(!orbit){const o=camera.position.clone().sub(target);orbit={yaw:Math.atan2(o.x,o.z),pitch:Math.asin(o.y/o.length()),distance:o.length()};}orbit.distance=Math.max(2,Math.min(500,orbit.distance*Math.exp(e.deltaY*.001)));},{...events,passive:false});
const statistics=a=>{const sorted=[...a].sort((a,b)=>a-b),mean=a.reduce((v,n)=>v+n,0)/Math.max(1,a.length);return{samples:a.length,meanFrameMs:mean,p95FrameMs:sorted[Math.floor(sorted.length*.95)]||0,fps:mean?1000/mean:0};};
function tick(now){if(disposed)return;const wall=last?(now-last)/1000:0,dt=Math.min(.04,wall||.016);last=now;frames++;let moving=false;
 if(world&&actor){if(!paused&&!document.hidden)time+=dt;
  if(current==='walk'&&!document.hidden){
   input.updateCamera(dt);if(check&&!check.complete&&host.querySelector('[data-bearing]').checked){const q=check.points[check.waypoint];input.yaw=Math.atan2(actor.root.position.x-q[0],actor.root.position.z-q[1]);}
   const before=actor.root.position.clone(),motion=actor.update(dt,input,world.obstacles,matchMedia('(prefers-reduced-motion:reduce)').matches,{jump:input.consumeActions().has('jump')});moving=motion.speed>.1;follow.update(actor.root,input,world.obstacles,dt,false);updateCheck(dt,before,motion);
   Object.assign(host.dataset,{player:JSON.stringify(actor.root.position.toArray()),jumps:String(motion.jumps),landings:String(motion.landings),jumpPhase:motion.phase,locomotion:motion.state});
  }else actor.animator.update(dt,0);
  if(orbit){const c=Math.cos(orbit.pitch);camera.position.set(target.x+Math.sin(orbit.yaw)*c*orbit.distance,target.y+Math.sin(orbit.pitch)*orbit.distance,target.z+Math.cos(orbit.yaw)*c*orbit.distance);camera.lookAt(target);}
  world.update(time,paused||matchMedia('(prefers-reduced-motion:reduce)').matches,camera);const began=performance.now();renderer.render(world.scene,camera);const submission=performance.now()-began;
  if(frames>60&&wall&&!document.hidden){intervals.push(wall*1000);cpu.push(submission);if(moving)walking.push(wall*1000);if(intervals.length>600){intervals.shift();cpu.shift();}if(walking.length>600)walking.shift();}
  host.dataset.camera=JSON.stringify({position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),fov:camera.fov,aspect:camera.aspect,eyeHeight:views[current]?.eye?1.65:null});
  for(const a of annotations){a.el.hidden=!host.querySelector('[data-labels]').checked||!preview.enabled||!['plan','aerial','context'].includes(current)||(a.planOnly&&current!=='plan');if(a.el.hidden)continue;point.set(a.position[0],a.height??preview.heightAt(...a.position)+(['guild'].includes(a.id)?22:2),a.position[1]).project(camera);a.el.style.left=(point.x*.5+.5)*host.clientWidth+'px';a.el.style.top=(-point.y*.5+.5)*host.clientHeight+'px';a.el.hidden=point.z>1;}
  key.hidden=current!=='plan'||!host.querySelector('[data-labels]').checked;host.querySelector('[data-guild-link]').hidden=!(current==='guild'||current==='walk'&&actor.root.position.distanceTo(new T.Vector3(destinations.guild[0],selected.lots.find(l=>l.id==='G').y,destinations.guild[1]))<7);
  measurement+=wall;if(measurement>1){measurement=0;host.dataset.performanceEvidence=JSON.stringify({...statistics(intervals),walking:statistics(walking),meanRenderSubmissionMs:cpu.reduce((n,v)=>n+v,0)/Math.max(1,cpu.length),drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,memory:{...renderer.info.memory,programs:renderer.info.programs.length},viewport:[innerWidth,innerHeight],canvas:[host.clientWidth,host.clientHeight],buffer:renderer.getDrawingBufferSize(new T.Vector2()).toArray(),quality:host.querySelector('[data-quality]').value,preview:preview.enabled,lighting:'Unchanged R0-A3 sunlight / exposure .96',metric:'Actual rAF, 60 warmup, up to 600 samples. CPU submission is not GPU time.'});}
 }
 frame=requestAnimationFrame(tick);
}
function release(){actor?.dispose();if(actor){actor.root.removeFromParent();disposeAsset({scene:actor.model});actor=null;}preview?.dispose();preview=null;}
function destroy(){if(disposed)return;disposed=true;cancelAnimationFrame(frame);abort.abort();observer.disconnect();input.destroy();release();world?.dispose();renderer.dispose();host.dataset.rendererCount='0';}
addEventListener('pagehide',destroy,{once:true});canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();destroy();status.textContent='3D view interrupted. Reload to restore the preview.';},{once:true});host.dataset.rendererCount='1';resize();frame=requestAnimationFrame(tick);load();
