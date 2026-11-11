import{projects,projectById}from'./project-registry.js?v=22';
import{readAtlasRoute,atlasRoute,createAtlasState}from'./living-atlas-state.js?v=22';
import{createProjectPanel}from'./project-panel.js?v=e1b';
import{presentationFor}from'./floating-atlas/presentation.js?v=73';
import{drawAtlasMap}from'./floating-atlas/minimap.js?v=73';
import{isConstructed,worldId}from'./floating-atlas/plan.js?v=73';
import{createAdventureUI}from'./adventure-ui.js?v=f1';
import{townDevelopmentEnabled}from'./floating-atlas/town-flag.js';
const storyEnabled=()=>{const p=new URLSearchParams(location.search);return townDevelopmentEnabled()&&[['town-layout','reset-final'],['town-props','cc0'],['town-guild','r0c2'],['town-story','r0e1']].every(([k,v])=>p.get(k)===v);};
export function bootLivingAtlas(){
  const sessionKey=storyEnabled()?'arnan:living-atlas:transit-field-note:v1':townDevelopmentEnabled()?'arnan:living-atlas:dev-town-s2f':'arnan:living-atlas';
  const route=readAtlasRoute(location.href);let saved={};try{saved=JSON.parse(sessionStorage.getItem(sessionKey)||'{}');}catch{}
  const state=createAtlasState({...route,mode:'editorial'},saved.worldId===worldId?saved:{}),host=document.querySelector('[data-living-world]'),main=document.querySelector('main'),header=document.querySelector('[data-site-header]');
  if(saved.worldId===worldId&&Number.isFinite(saved.playerPosition?.x)&&Number.isFinite(saved.playerPosition?.z))state.playerPosition=saved.playerPosition;
  host.querySelector('.living-world-caption span').textContent='AR(N)AN / THE FLOATING URBAN ATLAS';
  host.querySelector('.living-world-caption small').textContent='Fictional sky island · real urban research';
  host.setAttribute('aria-label','The Floating Urban Atlas');
  host.querySelector('.living-minimap p').textContent='Transit Kingdom · Island 01';
  host.querySelector('[data-atlas-map]').setAttribute('aria-label','Transit Kingdom landscape, walking trails, clearings and player position');
  const canvas=host.querySelector('[data-atlas-canvas]'),modeButton=document.querySelector('[data-atlas-mode]'),status=host.querySelector('[data-atlas-status]');
  const chapters=[...document.querySelectorAll('[data-world-project]')],hero=document.querySelector('[data-world-arrival]');
  const stops=[hero,...chapters].filter(Boolean),interact=host.querySelector('[data-landmark-interact]'),hud=host.querySelector('[data-adventure-hud]'),map=host.querySelector('[data-atlas-map]');
  interact.innerHTML='<kbd>E</kbd><span data-interact-label>Find a guide or landmark</span>';
  const interactionLabel=interact.querySelector('[data-interact-label]');
  let world=null,worldPromise=null,frameRequest=0,transition=0,pendingControl=false,near=null,lastScroll=0,restoring=false,failed=false,projectPinned=Boolean(route.activeProject),ambientPaused=false,reviewApplied=false;
  const ambient=document.createElement('button');ambient.type='button';ambient.className='atlas-ambient-toggle';ambient.textContent='Pause background';ambient.setAttribute('aria-pressed','false');ambient.setAttribute('aria-controls','living-world');
  const arrivalActions=hero.querySelector('.living-arrival-actions')||hero.appendChild(Object.assign(document.createElement('div'),{className:'living-arrival-actions'}));arrivalActions.append(ambient);
  ambient.onclick=()=>{ambientPaused=!ambientPaused;ambient.textContent=ambientPaused?'Resume background':'Pause background';ambient.setAttribute('aria-pressed',String(ambientPaused));refreshPause();};
  const canWalk=id=>isConstructed(id)||(id==='transit'&&storyEnabled()&&Boolean(world?.getCapabilities?.().transitTown));
  const panel=createProjectPanel({canExplore:()=>!failed,canWalk,onClose(){state.panelOpen=false;refreshPause();sync(true);},onExplore(id){closePanel();enterAdventure(id);}});
  const story=createAdventureUI(host,{world:()=>world,onClose:refreshPause,onStudy:id=>select(id),onLeave:()=>exitEditorial()});
  const help=document.createElement('dialog');help.className='experience-panel';help.setAttribute('aria-labelledby','atlas-guide-title');help.dataset.lenisPrevent='';help.innerHTML=`
    <button data-close>Close guide</button>
    <p class="research-kicker">TRANSIT KINGDOM / CONTROLS</p><h2 id="atlas-guide-title">Walk the floating atlas</h2>
    <p>WASD or arrow keys move. Shift runs, Space jumps, and E talks to a nearby guide or opens a study. Drag the scene or hold Q/R to turn the camera. Escape pauses.</p>
    <p>Hold the direction buttons on a touchscreen. You can also focus one with Tab and hold Enter to walk. Tap Jump to leave the ground. In a conversation, Enter chooses an option; Space stays inactive.</p>
    <p>Follow the dirt trails from Arrival Meadow through the valley, up Crown Ridge and around to Cloudbreak Overlook. Nadia remains on the valley trail for the existing transit research conversation.</p>
    <label class="atlas-motion-choice"><input type="checkbox" data-reduce-motion> Reduce camera and environmental motion</label>
    <p>This landscape is fictional. Buildings and physical research landmarks have not been constructed. All six real case studies remain available through Work. Cliff edges allow gravity falls and recovery to safe ground. Keep back from the unguarded natural edge.</p>`;document.body.append(help);
  const reduce=help.querySelector('[data-reduce-motion]');reduce.checked=matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{reduce.checked=reduce.checked||localStorage.getItem('arnan:reduce-world-motion')==='true';}catch{}
  host.dataset.reducedMotion=String(reduce.checked);reduce.onchange=()=>{host.dataset.reducedMotion=String(reduce.checked);try{localStorage.setItem('arnan:reduce-world-motion',String(reduce.checked));}catch{}};
  function refreshPause(){world?.setPaused(panel.dialog.open||help.open||story.dialog.open||header.dataset.menuOpen==='true'||(state.mode==='editorial'&&ambientPaused));}
  help.querySelector('[data-close]').onclick=()=>help.close();help.addEventListener('close',refreshPause);
  function persist(){try{sessionStorage.setItem(sessionKey,JSON.stringify({worldId,playerPosition:state.playerPosition,activeProject:state.activeProject,adventure:world?.getAdventureSave()||saved.adventure,exploration:world?.getExplorationSave?.()||saved.exploration}));}catch{}}
  function sync(replace=false){history[replace?'replaceState':'pushState']({},'',atlasRoute(location.href,state));persist();}
  function closePanel(){panel.close({notify:false,restoreFocus:false});state.panelOpen=false;refreshPause();}
  function setStatus(text){status.textContent=text;status.hidden=!text;}
  function highlight(){
    for(const chapter of chapters)chapter.toggleAttribute('data-current-project',chapter.dataset.worldProject===state.activeProject);
    host.querySelector('[data-world-place]').textContent=storyEnabled()&&world?.getCapabilities?.().transitTown&&state.activeProject==='transit'?'Transit Kingdom / Transit research':presentationFor(state.activeProject).label;
    host.dataset.selectedProject=state.activeProject||'';
    for(const link of header.querySelectorAll('[data-site-nav] a[href]')){
      const target=new URL(link.href,location.href);
      if(target.origin===location.origin&&target.pathname.endsWith('/portfolio.html')){if(state.activeProject)target.searchParams.set('project',state.activeProject);else target.searchParams.delete('project');link.href=target.href;}
    }
  }
  function select(id,{open=true,push=true,scroll=false,origin=null}={}){
    if(!projectById(id))return;projectPinned=true;state.activeProject=id;state.selectedLandmark=projectById(id).landmarkId||null;state.panelOpen=open;highlight();
    if(scroll)scrollProject(id);
    if(open){world?.setPaused(true);panel.show(id,{fileFieldNote:origin==='guild'&&state.mode==='adventure'&&id==='transit'&&Boolean(world?.canFileFieldNote?.()),onFileFieldNote:()=>{if(!world?.canFileFieldNote?.())return;world.requestAdventureAction('transit:submit-guild');closePanel();story.show({kind:'complete'});sync(true);}});}if(push)sync();
  }
  function scrollProject(id){
    const chapter=chapters.find(c=>c.dataset.worldProject===id);if(!chapter){if(projectById(id)){state.activeProject=id;state.panelOpen=true;highlight();panel.show(id);world?.setPaused(true);world?.setEditorialComposition(id);}return;}
    restoring=true;chapter.scrollIntoView({block:'center',behavior:'instant'});requestAnimationFrame(()=>{restoring=false;updateScroll(false);});
  }
  function onFrame(info){
    if(info.position)state.playerPosition=info.position;
    if(state.mode!=='adventure')return;
    near=info.near;const p=projectById(near);interact.disabled=!p&&!info.interaction;
    const label=info.interaction?info.interaction.label:p?`Inspect ${p.category.toLowerCase()}`:info.adventure?.objective||'Find a guide or landmark';
    if(interactionLabel.textContent!==label)interactionLabel.textContent=label;
    story.update(info.adventure);drawAtlasMap(map,info.position,world?.mapData||[],info.yaw,{marker:info.adventure?.marker,people:info.people,townRoute:info.townRoute});
  }
  function fail(message){failed=true;state.worldReady=false;host.dataset.worldFailed='true';host.dataset.worldReady='false';if(state.mode==='adventure'||pendingControl)exitEditorial(false);setStatus(message);modeButton.textContent='World unavailable';modeButton.disabled=true;document.querySelectorAll('[data-take-control],[data-walk]').forEach(b=>b.disabled=true);}
  async function ensureWorld(){
    if(world)return world;
    if(!worldPromise)worldPromise=import('./floating-atlas/entry.js?v=f1').then(({mountUrbanAtlas})=>mountUrbanAtlas(host,{mode:'editorial',savedAdventure:saved.adventure,savedExploration:saved.exploration,onFrame,onError:fail})).then(value=>{
      world=value;state.worldReady=true;host.dataset.worldReady='true';const transitStatus=chapters.find(c=>c.dataset.worldProject==='transit')?.querySelector('.living-chapter-tools span');if(transitStatus&&storyEnabled()&&world.getCapabilities?.().transitTown)transitStatus.textContent='Research available · town open for local review';world.start();refreshPause();updateScroll(false);setStatus('');return world;
    }).catch(error=>{console.error(error);fail('The live view is unavailable on this device. Every study remains readable below.');throw error;});
    return worldPromise;
  }
  function applyMode(){
    const adventure=state.mode==='adventure';document.documentElement.dataset.experience=adventure?'rpg':'professional';document.body.dataset.atlasMode=state.mode;
    for(const element of [main,document.querySelector('.site-footer'),document.querySelector('.skip-link')].filter(Boolean)){element.inert=adventure;element.setAttribute('aria-hidden',String(adventure));}
    hud.hidden=!adventure;canvas.tabIndex=adventure?0:-1;canvas.setAttribute('aria-label',adventure?'Third-person Transit Kingdom exploration. WASD walks, Shift runs, Space jumps, drag looks, E inspects.':'The Floating Urban Atlas, coordinated with the research sections.');
    modeButton.textContent=pendingControl?'Cancel control':adventure?'Read the atlas':'Take control';modeButton.setAttribute('aria-pressed',String(adventure));
    document.dispatchEvent(new CustomEvent('experience:change',{detail:{experience:adventure?'rpg':'professional'}}));
    state.cameraMode=adventure?'follow':'cinematic';host.dataset.interactionMode=state.mode;
    if(adventure){document.body.classList.remove('world-outside-story');world?.start();canvas.focus({preventScroll:true});}refreshPause();
  }
  async function enterAdventure(focusProject=null,push=true){
    if(failed)return;const request=++transition;pendingControl=true;lastScroll=scrollY;closePanel();story.close();if(help.open)help.close();
    if(focusProject){state.activeProject=focusProject;projectPinned=true;}highlight();applyMode();setStatus('Preparing the explorer on Transit Kingdom…');
    try{
      const scene=await ensureWorld();if(request!==transition)return;
      const first=!state.characterReady,implicit=first&&!state.playerPosition&&projectById(state.activeProject)?.availableInGame?state.activeProject:null;
      await scene.setMode('adventure',{focusProject:focusProject||implicit,position:state.playerPosition});
      const reviewURL=new URL(location.href);if(!reviewApplied&&reviewURL.searchParams.has('island-review')){scene.reviewView(reviewURL.hash.startsWith('#island-')?reviewURL.hash.slice(8):reviewURL.searchParams.get('island-review'));reviewApplied=true;}
      if(request!==transition)return;
      pendingControl=false;state.mode='adventure';state.panelOpen=false;state.characterReady=true;setStatus('');applyMode();if(focusProject&&!canWalk(focusProject)){select(focusProject,{push:false});sync(true);}else if(push)sync();
    }catch(error){console.error('Explorer load failed',error);if(!failed){setStatus('The explorer could not load. Keep reading the live atlas or reload to retry.');pendingControl=false;state.mode='editorial';applyMode();sync(true);}}
  }
  function exitEditorial(push=true){
    ++transition;pendingControl=false;projectPinned=Boolean(state.activeProject);state.mode='editorial';closePanel();story.close();if(help.open)help.close();world?.setMode('editorial');setStatus('');applyMode();
    if(state.activeProject)scrollProject(state.activeProject);else{scrollTo({top:lastScroll,behavior:'instant'});updateScroll(false);}
    if(push)sync();modeButton.focus({preventScroll:true});
  }
  function updateScroll(write=true){
    frameRequest=0;if(state.mode!=='editorial'||pendingControl||header.dataset.menuOpen==='true'||document.documentElement.dataset.menuLocked==='true')return;
    if(state.panelOpen||projectPinned){world?.setEditorialComposition(state.activeProject);return;}
    const center=innerHeight*.52,positions=stops.map(s=>s.getBoundingClientRect().top+s.getBoundingClientRect().height/2);
    let index=0;while(index<positions.length-1&&positions[index+1]<center)index++;
    const next=Math.min(index+1,stops.length-1),span=positions[next]-positions[index];const t=next===index?0:Math.max(0,Math.min(1,(center-positions[index])/span));
    const id=i=>stops[i]?.dataset.worldProject||'arrival';world?.setEditorialComposition(id(index),id(next),t);
    const selected=t>.5?id(next):id(index),project=selected==='arrival'?null:selected;
    if(!state.panelOpen&&!restoring&&state.activeProject!==project){state.activeProject=project;highlight();if(write)sync(true);}
    const last=stops[stops.length-1];const outside=last&&last.getBoundingClientRect().bottom<0;document.body.classList.toggle('world-outside-story',Boolean(outside));
    if(outside)world?.stop();else world?.start();
  }
  for(const chapter of chapters){
    const p=projectById(chapter.dataset.worldProject);if(!p)continue;
    const tools=document.createElement('div');tools.className='living-chapter-tools';tools.innerHTML=`<button data-inspect>Inspect study</button>${isConstructed(p.id)?'<button data-walk>Walk here</button>':'<span>Research available · realm not constructed</span>'}`;chapter.querySelector('.living-chapter-board').append(tools);
    tools.querySelector('[data-inspect]').onclick=()=>select(p.id);
    tools.querySelector('[data-walk]')?.addEventListener('click',()=>enterAdventure(p.id));
  }
  modeButton.onclick=()=>pendingControl||state.mode==='adventure'?exitEditorial():enterAdventure();
  document.querySelectorAll('[data-take-control]').forEach(button=>button.onclick=()=>enterAdventure());
  host.querySelector('[data-landmark-interact]').onclick=()=>world?.interact();host.addEventListener('atlas:interact',event=>select(event.detail.projectId,{origin:event.detail.origin}));
  host.addEventListener('atlas:dialogue',event=>story.show(event.detail));
  host.addEventListener('atlas:adventure-event',event=>{if(event.detail.type==='defeat')story.show({kind:'defeat'});else if(event.detail.type==='quest-change')persist();else if(event.detail.type==='encounter-error')setStatus('The optional encounter could not load. Research and exploration remain available.');});
  const openHelp=()=>{if(pendingControl)return;if(world?.getCapabilities?.().transitTown&&storyEnabled()){const ps=help.querySelectorAll('p');ps[3].textContent='From Pelabuhan Awan, follow Market Street toward Telaga Awan and Atlas Guild. Meet Nadia by Kopi Awan.';ps[4].textContent='This island is fictional. The transit research and all six real case studies remain available through Work. Natural cliff edges remain unguarded.';}world?.setPaused(true);help.showModal();};host.addEventListener('atlas:pause',openHelp);host.querySelector('[data-atlas-help]').onclick=openHelp;
  host.querySelector('[data-atlas-quality]').onchange=event=>world?.setQuality(event.target.value==='eco');
  // Layout, menu restoration and resize are not project choices. Only actual
  // editorial navigation releases an explicit URL/selection's camera ownership.
  const releaseProject=()=>{if(state.mode==='editorial'&&!pendingControl&&!panel.dialog.open&&!help.open&&!story.dialog.open&&header.dataset.menuOpen!=='true'){projectPinned=false;updateScroll();}};
  addEventListener('wheel',releaseProject,{passive:true});addEventListener('touchmove',releaseProject,{passive:true});
  addEventListener('keydown',e=>{if(['PageDown','PageUp','Home','End','ArrowDown','ArrowUp',' '].includes(e.key)&&!e.target.closest?.('button,input,select,textarea,a,[contenteditable=true]'))releaseProject();});
  main.addEventListener('click',e=>{if(e.target.closest('a[href^="#"]'))releaseProject();});
  addEventListener('scroll',()=>{if(!frameRequest)frameRequest=requestAnimationFrame(()=>updateScroll());},{passive:true});addEventListener('resize',()=>updateScroll(false));
  new MutationObserver(()=>{const menu=header.dataset.menuOpen==='true';host.inert=menu;modeButton.inert=menu;if(state.mode==='adventure')refreshPause();}).observe(header,{attributes:true,attributeFilter:['data-menu-open']});
  addEventListener('popstate',async()=>{
    story.close();
    const next=readAtlasRoute(location.href),previousProject=state.activeProject;projectPinned=Boolean(next.activeProject);state.activeProject=next.activeProject;highlight();
    if(next.mode!==state.mode){if(next.mode==='adventure')await enterAdventure(next.activeProject,false);else exitEditorial(false);}else if(state.mode==='adventure'&&next.activeProject!==previousProject)await enterAdventure(next.activeProject,false);else if(state.mode==='editorial'&&next.activeProject)scrollProject(next.activeProject);
    if(next.panelOpen&&next.activeProject){state.panelOpen=true;world?.setPaused(true);panel.show(next.activeProject);}else closePanel();
    sync(true);
    if(next.mode==='editorial'&&!next.activeProject){scrollTo({top:0,behavior:'instant'});updateScroll(false);}
  });
  addEventListener('pagehide',()=>{world?.stop();persist();});addEventListener('pageshow',event=>{if(event.persisted)world?.start();});
  const compactMenu=matchMedia('(max-width:699px)');
  function placeModeButton(){if(compactMenu.matches)header.insertBefore(modeButton,header.querySelector('[data-nav-toggle]'));else header.querySelector('[data-site-nav]').insertBefore(modeButton,header.querySelector('[data-theme-toggle]'));}
  placeModeButton();compactMenu.addEventListener('change',placeModeButton);
  modeButton.hidden=false;document.querySelectorAll('[data-take-control]').forEach(b=>b.hidden=false);applyMode();highlight();
  if(route.activeProject)scrollProject(route.activeProject);
  if(!navigator.connection?.saveData||route.mode==='adventure')ensureWorld().then(()=>{if(route.mode==='adventure')enterAdventure(route.activeProject,false);if(route.panelOpen&&route.activeProject)select(route.activeProject,{push:false});}).catch(()=>{});
  else setStatus('Data Saver is on. Take control to load the live atlas; research is ready below.');
}
