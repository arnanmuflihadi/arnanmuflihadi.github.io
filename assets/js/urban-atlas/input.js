export function createInput(canvas,host,onPause){
  const keys=new Set(),touch=new Set(),actions=new Set(),abort=new AbortController(),opts={signal:abort.signal};let drag=null;
  const input={keys,touch,yaw:0,pitch:.19,enabled:true,updateCamera(dt){if(input.enabled)input.yaw+=(Number(keys.has('q'))-Number(keys.has('r')))*1.7*dt;},consumeActions(){const result=new Set(actions);actions.clear();return result;},clear(){keys.clear();touch.clear();actions.clear();drag=null;host.querySelectorAll('[data-combat-action=guard]').forEach(b=>b.setAttribute('aria-pressed','false'));},destroy(){abort.abort();input.clear();}};
  addEventListener('keydown',e=>{if(e.defaultPrevented||e.metaKey||e.ctrlKey||e.altKey||e.target.isContentEditable||document.querySelector('[data-site-header][data-menu-open="true"]')||!input.enabled||host.hidden||document.querySelector('dialog[open]')||e.target.closest?.('button,a,input,select,textarea,[contenteditable=true]'))return;
    const key=e.key.toLowerCase();if(['j','c',' '].includes(key)){e.preventDefault();if(!e.repeat)actions.add(key==='j'?'attack':key==='c'?'dodge':'jump');return;}if(['w','a','s','d','q','r','k','shift','arrowup','arrowdown','arrowleft','arrowright','escape'].includes(key)){e.preventDefault();if(key==='escape'&&!e.repeat)onPause();else keys.add(key);}},opts);
  addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()),opts);addEventListener('blur',()=>input.clear(),opts);
  canvas.addEventListener('pointerdown',e=>{if(!input.enabled)return;drag={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);canvas.focus({preventScroll:true});},opts);
  canvas.addEventListener('pointermove',e=>{if(drag?.id!==e.pointerId)return;input.yaw-=(e.clientX-drag.x)*.004;input.pitch=Math.max(-.2,Math.min(.9,input.pitch+(e.clientY-drag.y)*.004));drag={id:e.pointerId,x:e.clientX,y:e.clientY};},opts);
  for(const type of['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,()=>drag=null,opts);
  host.querySelectorAll('[data-move]').forEach(button=>{button.addEventListener('pointerdown',e=>{if(!input.enabled)return;e.preventDefault();button.setPointerCapture(e.pointerId);touch.add(button.dataset.move);},opts);button.addEventListener('keydown',e=>{if(input.enabled&&['Enter',' '].includes(e.key)){e.preventDefault();touch.add(button.dataset.move);}},opts);button.addEventListener('keyup',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();touch.delete(button.dataset.move);}},opts);for(const type of['pointerup','pointercancel','lostpointercapture','blur'])button.addEventListener(type,()=>touch.delete(button.dataset.move),opts);});
  host.querySelectorAll('[data-combat-action]').forEach(button=>{
    const action=button.dataset.combatAction;
    button.addEventListener('pointerdown',e=>{if(!input.enabled)return;e.preventDefault();button.setPointerCapture(e.pointerId);if(action==='guard'){touch.add('k');button.setAttribute('aria-pressed','true');}else actions.add(action);},opts);
    for(const type of['pointerup','pointercancel','lostpointercapture'])button.addEventListener(type,()=>{touch.delete('k');if(action==='guard')button.setAttribute('aria-pressed','false');},opts);
    button.addEventListener('click',e=>{if(e.detail===0&&input.enabled){if(action==='guard'){const active=touch.has('k');if(active)touch.delete('k');else touch.add('k');button.setAttribute('aria-pressed',String(!active));}else actions.add(action);}},opts);
  });
  return input;
}
