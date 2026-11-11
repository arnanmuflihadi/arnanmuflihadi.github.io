const host=document.querySelector('[data-atlas]'),cover=document.querySelector('[data-cover]'),enter=document.querySelector('[data-enter]'),status=document.querySelector('[data-status]'),pause=document.querySelector('dialog');
let world=null,failed=false;
function error(message){failed=true;world?.stop();cover.hidden=false;enter.hidden=true;status.textContent=message;}
enter.addEventListener('click',async()=>{
  enter.disabled=true;status.textContent='Preparing the district…';
  try{const {mountUrbanAtlas}=await import('./entry.js?v=22');world=await mountUrbanAtlas(host,{onError:error});cover.hidden=true;world.start();host.querySelector('canvas').focus();}
  catch(e){console.error(e);error('This device could not start the 3D preview. Your professional portfolio is still available through the link above.');}
});
function showPause(){if(!world||failed)return;world.setPaused(true);pause.showModal();}
host.addEventListener('atlas:pause',showPause);document.querySelector('[data-pause]').onclick=showPause;
pause.querySelector('button').onclick=()=>pause.close();pause.addEventListener('close',()=>world?.setPaused(false));
document.querySelector('[data-quality]').onchange=e=>world?.setQuality(e.target.value==='eco');
document.querySelectorAll('[data-view]').forEach(button=>button.onclick=()=>{if(!world||failed)return;world.goToViewpoint(button.dataset.view);document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelector('[data-place]').textContent=button.dataset.place;host.querySelector('canvas').focus();});
addEventListener('pagehide',()=>world?.stop());addEventListener('pageshow',e=>{if(e.persisted&&world&&!failed)world.start();});
