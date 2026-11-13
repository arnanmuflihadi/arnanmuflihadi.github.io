export function createInput(canvas, root, action) {
  const keys=new Set(),touch=new Set(),abort=new AbortController(),opt={signal:abort.signal};
  const input={keys,touch,yaw:0,pitch:.48,clear(){keys.clear();touch.clear();},destroy(){abort.abort();input.clear();}};
  addEventListener('keydown',e=>{
    if(root.hidden || document.querySelector('.experience-panel[open]') || /INPUT|SELECT|TEXTAREA/.test(e.target.tagName)) return;
    const key=e.key.toLowerCase();
    if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','shift','e','m','escape'].includes(key)) {e.preventDefault();keys.add(key);if(!e.repeat) action(key);}
  },opt);
  addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()),opt);
  addEventListener('blur',()=>input.clear(),opt);
  let pointer=null;
  canvas.addEventListener('pointerdown',e=>{pointer={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);canvas.focus();},opt);
  canvas.addEventListener('pointermove',e=>{if(pointer?.id!==e.pointerId)return;input.yaw-=(e.clientX-pointer.x)*.006;input.pitch=Math.max(.2,Math.min(.95,input.pitch+(e.clientY-pointer.y)*.004));pointer={id:e.pointerId,x:e.clientX,y:e.clientY};},opt);
  for(const type of ['pointerup','pointercancel','lostpointercapture']) canvas.addEventListener(type,()=>pointer=null,opt);
  root.querySelectorAll('[data-move]').forEach(button=>{
    button.addEventListener('pointerdown',e=>{e.preventDefault();button.setPointerCapture(e.pointerId);touch.add(button.dataset.move);},opt);
    for(const type of ['pointerup','pointercancel','lostpointercapture'])button.addEventListener(type,()=>touch.delete(button.dataset.move),opt);
  });
  return input;
}
