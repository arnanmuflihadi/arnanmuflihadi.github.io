import * as T from'../vendor/three-atlas.module.js?v=16';
import{createBuilder}from'../urban-atlas/geometry.js?v=22';
import{groundHeight,safeGround}from'../floating-atlas/terrain.js?v=73';
import{blocked,clearDistance}from'../floating-atlas/collision.js?v=73';
import{createSupportIndex}from'../architecture-r0b1/preview.js?v=b1-6';
import{modelMetrics}from'../urban-atlas/model-library.js?v=74';
import{selected,densify,entryOf,thresholdLinks,surveyPlot,streetLevel}from'./plan.js?v=composition-3';
export{entryOf}from'./plan.js?v=composition-3';

const project=(x,z,a,b)=>{const dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));return{distance:Math.hypot(x-a[0]-dx*t,z-a[1]-dz*t),height:a[2]+(b[2]-a[2])*t};};
export function footprintMask(x,z,pad=0){
 const p=selected,s=p.square;
 if(Math.abs(x-s.x)<s.w/2+pad&&Math.abs(z-s.z)<s.d/2+pad||Math.hypot(x-p.skyport.x,z-p.skyport.z)<p.skyport.r+pad)return true;
 if(p.lots.some(l=>Math.abs(x-l.x)<l.w/2+pad&&Math.abs(z-l.z)<l.d/2+pad))return true;
 return p.streets.some(r=>r.kind!=='trail'&&r.points.slice(1).some((b,i)=>project(x,z,r.points[i],b).distance<r.width/2+pad));
}
export function mountBlockout(world){
 const group=new T.Group(),owned=new Set(),materials=new Set(),textures=new Set(),solids=[],labels=[],b=createBuilder(group,{toon:color=>{if(typeof color!=='string')return color;if(!palette.has(color)){const m=new T.MeshStandardMaterial({color,roughness:.94});palette.set(color,m);materials.add(m);}return palette.get(color);}}),palette=new Map();let enabled=true,disposed=false;
 group.name='R0-B1.5 / temporary planning geometry';
 const material=(color,name)=>{const m=new T.MeshStandardMaterial({color,roughness:.96,name});materials.add(m);return m;};
 const stone=material('#7d8c85','Planning / retaining stone'),paving=material('#c7bda4','Planning / primary mineral paving'),soil=material('#ae9166','Planning / natural trail transition'),gravel=material('#969b7b','Planning / secondary meadow gravel');
 const routePaving=material('#c7bda4','Planning / paving junctions');routePaving.polygonOffset=true;routePaving.polygonOffsetFactor=-1;routePaving.polygonOffsetUnits=-1;
 const add=(g,m,walkable=false)=>{owned.add(g);const mesh=new T.Mesh(g,m);mesh.castShadow=!walkable;mesh.receiveShadow=true;mesh.userData.walkable=walkable;group.add(mesh);return mesh;};
 const geometry=(positions,indices)=>{const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setIndex(indices);g.computeVertexNormals();return g;};
 const side=(a,b)=>{const ga=groundHeight(a[0],a[2])-.06,gb=groundHeight(b[0],b[2])-.06;return{p:[...a,...b,a[0],ga,a[2],b[0],gb,b[2]],i:[0,2,1,1,2,3]};};
 const sides=[];
 function polygon(points,y){const cx=points.reduce((n,p)=>n+p[0]/points.length,0),cz=points.reduce((n,p)=>n+p[1]/points.length,0),height=typeof y==='function'?y:()=>y,positions=[cx,height(cx,cz),cz],idx=[];points.forEach(([x,z])=>positions.push(x,height(x,z),z));for(let i=0;i<points.length;i++){idx.push(0,i+1,(i+1)%points.length+1);const a=points[i],b=points[(i+1)%points.length];sides.push(side([a[0],height(...a),a[1]],[b[0],height(...b),b[1]]));}add(geometry(positions,idx),paving,true);}
 // The plaza is a raised, reversible terrace. The terrain's vertices are untouched.
 const s=selected.square,x=s.x,z=s.z,w=s.w/2,d=s.d/2,c=2;
 polygon([[x-w+c,z-d],[x-w,z-d+c],[x-w,z+d-c],[x-w+c,z+d],[x+w-c,z+d],[x+w,z+d-c],[x+w,z-d+c],[x+w-c,z-d]],s.y);
 const port=selected.skyport;polygon(Array.from({length:48},(_,i)=>[port.x+Math.cos(-i/48*Math.PI*2)*port.r,port.z+Math.sin(-i/48*Math.PI*2)*port.r]),port.y);
 const streetMeshes=[];
 const guildLevel=z=>z>=14?22.6:z>=9?22.6+(14-z)*.15:z>=5?23.35+(9-z)*.2125:Math.min(25.2,24.2+(5-z)/4.2);
 function ribbon(r){
  const pts=densify(r.points,.45),positions=[],idx=[],cross=10,edges=[[],[]];
  for(let i=0;i<pts.length;i++){
   const a=pts[Math.max(0,i-1)],q=pts[Math.min(pts.length-1,i+1)],len=Math.hypot(q[0]-a[0],q[1]-a[1])||1;let nx=-(q[1]-a[1])/len,nz=(q[0]-a[0])/len;
   if(r.id==='arrival'&&pts[i][1]<46){const t=Math.min(1,(46-pts[i][1])/3);nx+=(1-nx)*t;nz*=1-t;const n=Math.hypot(nx,nz);nx/=n;nz/=n;}
   for(let j=0;j<=cross;j++){const offset=(j/cross-.5)*r.width,xx=pts[i][0]+nx*offset,zz=pts[i][1]+nz*offset;const shared=r.id==='guild'?22.6+(guildLevel(zz)-22.6)*Math.max(0,Math.min(1,(xx-37.25)/.75)):['market','east-frontage','west-frontage','arrival'].includes(r.id)?streetLevel(zz):pts[i][2];const yy=Math.max(shared,groundHeight(xx,zz)+.075);positions.push(xx,yy,zz);if(j===0||j===cross)edges[j===0?0:1].push([xx,yy,zz]);}
   if(i)for(let j=0;j<cross;j++){const a=(i-1)*(cross+1)+j,k=i*(cross+1)+j;idx.push(a,a+1,k,a+1,k+1,k);}
  }
  const mesh=add(geometry(positions,idx),r.kind==='trail'?soil:r.kind==='secondary'?gravel:routePaving,true);mesh.name='Planning support / '+r.id;mesh.userData.routeId=r.id;streetMeshes.push(mesh);
  if(r.kind!=='trail')for(const es of edges)for(let i=1;i<es.length;i++)sides.push(side(es[i-1],es[i]));
 }
 for(const r of selected.streets.filter(r=>!['highland','scenic-return','east-frontage','west-frontage'].includes(r.id)))ribbon(r.id==='market'?{...r,width:9.6,points:[[36,43,18.8],...r.points,[36,16,22.6]].sort((a,b)=>b[1]-a[1])}:r.id==='arrival'?{...r,points:r.points.slice(0,-1)}:['ridge-connector','guild'].includes(r.id)?{...r,points:r.points.slice(1)}:r.id==='garden-loop'?{...r,points:r.points.slice(0,8)}:r);
 ribbon({...selected.streets[5],id:'town-gate',kind:'paved',points:selected.streets[5].points.slice(0,2)});
 // Short threshold links connect every envelope to its public frontage.
 const links=thresholdLinks;links.forEach(r=>{const l=selected.lots.find(l=>r.id==='threshold-'+l.id);if(Number(l.id.slice(1))<=8){const e=entryOf(l),xx=l.face==='east'?31.25:40.75;ribbon({...r,points:[[xx,l.z,l.y],[...e,l.y]]});}else ribbon(r);});
 const sp=[],si=[];for(const v of sides){const k=sp.length/3;sp.push(...v.p);si.push(...v.i.map(i=>i+k));}add(geometry(sp,si),stone);
 // Low contrast joint lines establish paving scale without an expensive texture.
 const[cx0,cz0,cx1,cz1]=s.clear;
 for(let xx=cx0+1;xx<cx1;xx+=2)b.box(xx,s.y+.008,(cz0+cz1)/2,.018,.012,cz1-cz0,'#b0a78f');
 for(let zz=cz0+1;zz<cz1;zz+=2)b.box((cx0+cx1)/2,s.y+.009,zz,cx1-cx0,.012,.018,'#b0a78f');
 // A flush circle reserves a future gathering focal point without obstructing the square.
 const[fx,fz]=s.focal,ring=[];for(let i=0;i<=48;i++){const a=i/48*Math.PI*2;ring.push([fx+Math.cos(a)*2.1,s.y+.018,fz+Math.sin(a)*2.1]);}const rp=[],ri=[];for(let i=1;i<ring.length;i++){const a=ring[i-1],q=ring[i],k=rp.length/3;rp.push(a[0],a[1],a[2],q[0],q[1],q[2],fx+(a[0]-fx)*.95,a[1],fz+(a[2]-fz)*.95,fx+(q[0]-fx)*.95,q[1],fz+(q[2]-fz)*.95);ri.push(k,k+2,k+1,k+1,k+2,k+3);}add(geometry(rp,ri),stone);
 const landingPositions=[],landingIndices=[],landingMaterial=material('#8c9e92','Planning / supported flush thresholds');
 landingMaterial.polygonOffset=true;landingMaterial.polygonOffsetFactor=-2;landingMaterial.polygonOffsetUnits=-2;
 for(const l of selected.lots){
  const top=l.y+l.h,body=l.id==='G'?'#95b4ae':Number(l.id.slice(1))%3===0?'#b4bdb4':Number(l.id.slice(1))%2?'#c5bdac':'#d3cdc0',roof=l.id==='G'?'#496e6c':'#8e8778',bottom=surveyPlot(l).foundationBottom;
  const mass=(x,y,z,w,h,d,color,minY=y-h/2)=>{b.box(x,y,z,w,h,d,color);solids.push({x,z,w,d,minY,h:y+h/2,planning:l.id});};
  if(l.id==='G'){
   // Open civic porch, two lower wings and a rear observatory establish landmark hierarchy.
   mass(l.x-3.7,l.y+2.9,l.z,2.6,5.8,l.d,body);mass(l.x+3.7,l.y+2.9,l.z,2.6,5.8,l.d,body);
   mass(l.x,l.y+3,l.z-2.8,4.8,6,2.4,body);
   b.box(l.x,l.y+6.1,l.z+1,5.1,.3,6,roof);
   gable(l.x,l.y+6.25,l.z,5.8,8.6,2.2,roof);
   mass(l.x+1,l.y+9.2,l.z-1.8,3.4,6.2,3.4,body);
   b.column(l.x+1,l.y+12.6,l.z-1.8,2.15,.6,roof);
   const peak=new T.ConeGeometry(2.15,3.4,4);peak.rotateY(Math.PI/4);peak.translate(l.x+1,l.y+14.6,l.z-1.8);add(peak,material(roof,'Planning / observatory roof'));
   solids.push({x:l.x+1,z:l.z-1.8,w:4.3,d:4.3,minY:l.y+12.3,h:l.y+16.3,cameraOnly:true});
   b.box(l.x-3.7,l.y+5.9,l.z,2.9,.25,l.d+.35,roof);b.box(l.x+3.7,l.y+5.9,l.z,2.9,.25,l.d+.35,roof);
   polygon([[l.x-2.4,l.z+4],[l.x-2.4,l.z-1.6],[l.x+2.4,l.z-1.6],[l.x+2.4,l.z+4]],l.y);
  }else{
   const east=l.face==='east',south=l.face==='south',nx=south?0:east?1:-1,nz=south?1:0;
   // Recessed ground-floor volume and two piers describe an arcade, not a finished facade.
   mass(l.x-nx*.55,l.y+1.55,l.z-nz*.55,l.w-(south?0:1.1),3.1,l.d-(south?1.1:0),body);
   mass(l.x,l.y+3.2+(l.h-3.2)/2,l.z,l.w,l.h-3.2,l.d,body);
   for(const sign of[-1,1])mass(l.x+nx*(l.w/2-.2)+(south?sign*(l.w/2-.25):0),l.y+1.55,l.z+nz*(l.d/2-.2)+(south?0:sign*(l.d/2-.25)),.35,3.1,.35,roof);
   if(l.roof==='gable')gable(l.x,top,l.z,l.w+.45,l.d+.45,1.5,roof);else{b.box(l.x,top+.13,l.z,l.w+.35,.26,l.d+.35,roof);b.box(l.x-(south?0:.8),top+.65,l.z-(south?.8:0),l.w*.65,1,l.d*.65,body);}
   b.box(l.x,l.y+3.18,l.z,l.w+.16,.16,l.d+.16,roof);
   for(let y=l.y+6.4;y<top;y+=3.2)b.box(l.x,y,l.z,l.w+.06,.09,l.d+.06,'#9b9e93');
  }
  const e=entryOf(l),rot=l.face==='south'?0:Math.PI/2;
  const normal=l.face==='south'?[0,1]:l.face==='east'?[1,0]:[-1,0],landing=new T.BoxGeometry(l.face==='south'?3.4:.8,.2,l.face==='south'?.8:3.4);landing.translate(e[0]-normal[0]*.4,l.y-.1,e[1]-normal[1]*.4);const base=landingPositions.length/3;landingPositions.push(...landing.attributes.position.array);landingIndices.push(...Array.from(landing.index.array,i=>i+base));landing.dispose();
  const doorX=l.face==='south'?l.x:l.x+(l.face==='east'?1:-1)*(l.w/2-1.085),doorZ=l.id==='G'?l.z-1.58:l.face==='south'?l.z+l.d/2-1.085:l.z;
  b.box(doorX,l.y+(l.id==='G'?2.75:1.45),doorZ,l.id==='G'?3.6:2.4,l.id==='G'?5.5:2.9,.035,'#405c57',rot);
  const canopy=l.id==='G'?5.9:3.2,canopyWidth=l.id==='G'?5.4:l.face==='south'?3.8:2,canopyDepth=l.id==='G'?2.4:l.face==='south'?2:3.8;
  b.box(e[0],l.y+canopy,e[1],canopyWidth,.18,canopyDepth,roof);
  solids.push({x:e[0],z:e[1],w:canopyWidth,d:canopyDepth,minY:l.y+canopy-.09,h:l.y+canopy+.09,cameraOnly:true,planningCanopy:l.id});
  // These are split-level lower building volumes, rather than independent podium slabs.
  b.box(l.x,(l.y+bottom)/2,l.z,l.w,l.y-bottom,l.d,body);
  solids.push({x:l.x,z:l.z,w:l.w,d:l.d,minY:bottom,h:l.y-.02,planning:l.id});
  labels.push({id:l.id,text:l.id==='G'?'ATLAS GUILD':l.id,position:[l.x,top+1,l.z],entry:e,floor:l.y});
 }
 add(geometry(landingPositions,landingIndices),landingMaterial,true).name='Planning support / flush doorway landings';
 // Arrival edge is legible, with a north gap opening onto the main route.
 for(let i=0;i<32;i++){const a=i/32*Math.PI*2,xx=port.x+Math.sin(a)*8.65,zz=port.z+Math.cos(a)*8.65,exitA=selected.streets[0].points[0],exitB=selected.streets[0].points[1];if(project(xx,zz,exitA,exitB).distance<4.8&&zz<port.z)continue;b.column(xx,port.y+.55,zz,.065,1.1,'#6c7c73');b.box(xx,port.y+1.0,zz,1.75,.09,.09,'#6c7c73',a);solids.push({x:xx,z:zz,w:.15,d:.15,minY:port.y,h:port.y+1.1});}
 b.flush();b.owned.forEach(g=>owned.add(g));
 const vegetation=maskVegetation(world,owned),originalObstacles=world.obstacles,filtered=originalObstacles.filter(o=>!footprintMask(o.x,o.z,1));
 world.scene.add(group);const support=createSupportIndex(group),surface=createSupportIndex(group,()=>-500);
 const active=y=>world.obstacles.filter(o=>!Number.isFinite(o.minY)||(y+1.7>o.minY&&y<o.h-.06));
 const api={group,labels,solids,streetMeshes,links,plots:selected.lots.map(l=>surveyPlot(l)),surfaceAt:(x,z,reference=Infinity)=>enabled?surface(x,z,reference):-500,metrics:modelMetrics(group),get enabled(){return enabled;},heightAt:(x,z,reference=Infinity)=>enabled?support(x,z,reference):groundHeight(x,z),clearDistance,
  movementOptions(getY){return{bounds:105,minY:-100,maxY:130,recoveryPoint:{x:27,z:60},isSafe:safeGround,collision:{blocked:(x,z,_solids,r)=>blocked(x,z,active(getY()),r),slide(p,dx,dz){const obstacles=active(p.y),n=Math.max(1,Math.ceil(Math.max(Math.abs(dx),Math.abs(dz))/.1));for(let i=0;i<n;i++){if(!blocked(p.x+dx/n,p.z,obstacles))p.x+=dx/n;if(!blocked(p.x,p.z+dz/n,obstacles))p.z+=dz/n;}}}};},
  setEnabled(value){enabled=value;group.visible=value;vegetation(value);world.obstacles=value?[...filtered,...solids]:originalObstacles;},
  dispose(){if(disposed)return;api.setEnabled(false);disposed=true;group.removeFromParent();group.traverse(o=>{if(o.isInstancedMesh)o.dispose();});owned.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());}
 };api.setEnabled(true);return api;
 function gable(x,y,z,w,d,h,color){const p=[x-w/2,y,z-d/2,x+w/2,y,z-d/2,x,y+h,z-d/2,x-w/2,y,z+d/2,x+w/2,y,z+d/2,x,y+h,z+d/2],i=[0,2,1,3,4,5,0,3,5,0,5,2,1,2,5,1,5,4,0,1,4,0,4,3];add(geometry(p,i),palette.get(color)||material(color,'Planning / roof mass'));solids.push({x,z,w,d,minY:y,h:y+h,cameraOnly:true});}
}

function maskVegetation(world,owned){
 const instances=[],grass=[],palms=[],removed=[];
 world.scene.traverse(o=>{if(!o.isMesh||o.isInstancedMesh||o.name||o.geometry?.attributes.position.count!==91)return;o.geometry.computeBoundingBox();const size=o.geometry.boundingBox.getSize(new T.Vector3());if(size.y<8||size.x>2||size.z>2)return;const p=o.geometry.attributes.position;let x=0,z=0,cx=0,cz=0;for(let i=0;i<7;i++){x+=p.getX(i)/7;z+=p.getZ(i)/7;cx+=p.getX(p.count-7+i)/7;cz+=p.getZ(p.count-7+i)/7;}const hide=footprintMask(x,z,4);palms.push({mesh:o,visible:o.visible,hide});if(hide)removed.push([cx,cz]);});
 world.scene.traverse(o=>{
  if(o.isInstancedMesh&&(o.name.startsWith('Living landscape /')||!o.name)){o.geometry.computeBoundingBox();const frond=!o.name&&o.geometry.attributes.position.count===26&&o.geometry.boundingBox.max.z-o.geometry.boundingBox.min.z>4,tree=/tree|canopy|crown/i.test(o.name),before=o.instanceMatrix.array.slice(),count=o.count,dummy=new T.Object3D(),kept=[];for(let i=0;i<count;i++){o.getMatrixAt(i,dummy.matrix);const e=dummy.matrix.elements,hide=frond?removed.some(([x,z])=>Math.hypot(e[12]-x,e[14]-z)<.05):e[13]>groundHeight(e[12],e[14])-1&&footprintMask(e[12],e[14],tree?4:1);if(!hide)kept.push(dummy.matrix.clone());}instances.push({mesh:o,before,count,kept});}
  if(o.name==='Zone grass / curved blades'){const original=o.userData.detailLevels,replacement={},indices={};for(const key of['near','far']){const g=original[key],p=g.attributes.position,idx=g.index,kept=[];indices[key]=idx;for(let i=0;i<idx.count;i+=3){const ids=[idx.getX(i),idx.getX(i+1),idx.getX(i+2)],x=ids.reduce((n,j)=>n+p.getX(j)/3,0),z=ids.reduce((n,j)=>n+p.getZ(j)/3,0);if(!footprintMask(x,z,.2))kept.push(...ids);}replacement[key]=g.clone();replacement[key].setIndex(kept);owned.add(replacement[key]);}grass.push({mesh:o,original,replacement,indices});}
 });
 return enabled=>{for(const v of instances){v.mesh.instanceMatrix.array.set(v.before);if(enabled){v.kept.forEach((m,i)=>v.mesh.setMatrixAt(i,m));v.mesh.count=v.kept.length;}else v.mesh.count=v.count;v.mesh.instanceMatrix.needsUpdate=true;v.mesh.computeBoundingSphere();}for(const p of palms)p.mesh.visible=enabled&&p.hide?false:p.visible;for(const g of grass){for(const key of['near','far'])g.original[key].setIndex(enabled?g.replacement[key].index:g.indices[key]);g.mesh.geometry=g.original.near;}};
}
