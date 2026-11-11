import{routes as naturalTrails}from'./plan.js?v=73';
export function mountCirculationPlan(host,town){
 const box=document.createElement('div');box.style.cssText='position:absolute;inset:0;z-index:1001;pointer-events:none;display:none';host.append(box);let plan=null,error=null;
 fetch(new URL('../../../validation/circulation-c1c/circulation-plan.json',import.meta.url)).then(r=>{if(!r.ok)throw Error('Circulation plan '+r.status);return r.json();}).then(p=>plan=p).catch(e=>error=String(e));
 const centre=[20,27],span=80;
 function draw(visible){box.style.display=visible?'block':'none';if(!visible)return;const w=host.clientWidth,h=host.clientHeight,scale=h/span,x=X=>w/2+(X-centre[0])*scale,y=Z=>h/2+(Z-centre[1])*scale;
  if(!plan){box.textContent=error||'Preparing measured plan…';return;}
  const on=town.circulationEnabled,paths=on?plan.afterRoutes:plan.beforeRoutes;let body='';
  const line=(p,color,width=2,dash='')=>'<polyline points="'+p.map(v=>x(v[0])+','+y(v[1])).join(' ')+'" fill="none" stroke="'+color+'" stroke-width="'+width+'" '+(dash?'stroke-dasharray="'+dash+'"':'')+'/>';
  const label=(p,text,color='#173c35')=>'<g><rect x="'+(x(p[0])+6)+'" y="'+(y(p[1])-24)+'" width="'+(text.length*6.9+16)+'" height="24" rx="3" fill="#fff7e5" fill-opacity=".94"/><text x="'+(x(p[0])+14)+'" y="'+(y(p[1])-8)+'" fill="'+color+'" font-size="13" font-weight="600">'+text+'</text></g>';
  for(const r of naturalTrails)body+=line(r.points,'#ead6aa',1.1,'4 4');
  const gone=plan.removed_names.map(n=>n.split('.')[0]);
  for(const item of plan.before){const[a,b,c,d]=item.bounds,removed=gone.includes(item.name.split('.')[0]);body+='<rect x="'+x(a)+'" y="'+y(c)+'" width="'+Math.max(.6,(b-a)*scale)+'" height="'+Math.max(.6,(d-c)*scale)+'" fill="none" stroke="'+(on&&removed?'#d45137':'#304c49')+'" stroke-opacity="'+(on&&removed?.55:.38)+'" stroke-width=".75" '+(on&&removed?'stroke-dasharray="3 2"':'')+'/>';}
  if(on){for(const item of plan.after.filter(i=>i.status==='added')){const[a,b,c,d]=item.bounds;body+='<rect x="'+x(a)+'" y="'+y(c)+'" width="'+Math.max(1,(b-a)*scale)+'" height="'+Math.max(1,(d-c)*scale)+'" fill="none" stroke="#0e8a62" stroke-width="1"/>';}body+=line(plan.beforeRoutes.court,'#ce5337',2,'5 4');body+=line([[33,9],[32.3,7.9],[30.5,5.5],[31,1.2],[36,0]],'#ce5337',2,'5 4');body+=line(plan.beforeRoutes.arrival.slice(1),'#ce5337',2,'5 4');body+=line([[29.2,12.8],[42.2,11]],'#d3932d',2,'4 4');}
  if(on)body+=line([[30.4,10.9],[40.5,10.5]],'#d3932d',2,'4 4');
  for(const key of['arrival','market','court','guild'])if(paths[key])body+=line(paths[key],'#f8f2d4',6)+line(paths[key],'#126a9b',3.5);
  if(paths.highland)body+=line(paths.highland,'#16775a',3,'6 3');if(paths.optionalReturn)body+=line(paths.optionalReturn,'#16775a',2,'5 4');
  for(const[p,text]of[[[27,57],'1 Arrival / natural ground'],[[36,30],'2 Market Street'],[[35,12.6],'3 Upper forecourt'],[[21,9],'4 Telaga Awan'],[[-5,5],'Highland junction'],[[22,-8],'5 Guild boundary → / unbuilt']])body+=label(p,text);
  body+=label([10,18],on?'Direct: 5 × 0.163 m':'No direct entrance',on?'#126a9b':'#b34e32');
  const bar=10*scale;body+='<rect x="18" y="'+(h-64)+'" width="'+(bar+30)+'" height="50" fill="#fff7e5" fill-opacity=".94"/><path d="M30 '+(h-38)+'h'+bar+'m0 -4v8M30 '+(h-42)+'v8" stroke="#173c35" stroke-width="2"/><text x="30" y="'+(h-48)+'" font-size="12" fill="#173c35">10 m · north ↑</text>';
  body+='<rect x="'+(w-306)+'" y="18" width="288" height="174" rx="5" fill="#fff7e5" fill-opacity=".96"/><g fill="#173c35" font-family="system-ui" font-size="13"><text x="'+(w-290)+'" y="42" font-weight="700">'+(on?'C1C / one circulation proposal':'C1B / rejected circulation baseline')+'</text><text x="'+(w-290)+'" y="67">Blue: primary arrival → square → Guild</text><text x="'+(w-290)+'" y="91">Green dashed: optional highland / return</text><text x="'+(w-290)+'" y="115">Red dashed: removed path / hardware</text><text x="'+(w-290)+'" y="139">Green outlines: added interfaces</text><text x="'+(w-290)+'" y="163">Amber: relocated bench / tree planter</text><text x="'+(w-290)+'" y="182">Thin outlines: public stairs / rails / decks</text></g>';
  box.innerHTML='<svg width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'" xmlns="http://www.w3.org/2000/svg" style="font-family:system-ui">'+body+'</svg>';
 }
 return{centre,span,draw,summary:()=>({ready:!!plan,error,spanZMetres:span,metresPerPixel:span/host.clientHeight,source:'validation/circulation-c1c/circulation-plan.json',beforeObjects:plan?.before.length,afterObjects:plan?.after.length}),dispose(){box.remove();}};
}
