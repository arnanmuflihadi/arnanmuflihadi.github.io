import * as T from '../vendor/three-atlas.module.js?v=16';
import {createModelLibrary,modelMetrics} from './model-library.js?v=4';
import {showcasePlan} from './showcase-plan.js?v=2';

const canvas=document.querySelector('canvas'),status=document.querySelector('[data-status]'),summary=document.querySelector('[data-summary]'),diagnostics=document.querySelector('[data-diagnostics]');
const scene=new T.Scene();scene.background=new T.Color('#cbd7c3');
const camera=new T.PerspectiveCamera(42,1,.1,250),models=new T.Group(),comparison=new T.Group(),collisionLines=new T.Group();
scene.add(models,comparison,collisionLines);comparison.visible=false;collisionLines.visible=false;
const instances=[],colliders=[],views={};let library=createModelLibrary(),renderer,view='street',reverse=false,ready=false;
const mat=color=>new T.MeshStandardMaterial({color,roughness:.92,metalness:0});
const concrete=mat('#ddd2b7'),asphalt=mat('#777f73'),soil=mat('#7d8660'),grass=mat('#99ab79');
function block(x,y,z,w,h,d,material,parent=scene){const mesh=new T.Mesh(new T.BoxGeometry(w,h,d),material);mesh.position.set(x,y+h/2,z);mesh.receiveShadow=true;parent.add(mesh);return mesh;}
block(0,-.2,0,48,.16,40,grass);
block(0,-.04,4.5,33,.2,6,concrete);
block(0,-.04,10.5,44,.04,6,asphalt);
block(0,.02,7.45,33,.14,.12,concrete);
for(const x of[-19,-14,-9,-4,1,6,11,16])block(x,.003,10.5,2.2,.008,.08,concrete);
block(-17.3,.16,3,2.8,.025,2.8,soil);
scene.add(new T.HemisphereLight('#fff4de','#7a967d',2));
const sun=new T.DirectionalLight('#fff0d3',2.6);sun.position.set(-18,32,25);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);
Object.assign(sun.shadow.camera,{left:-25,right:25,top:25,bottom:-25,near:1,far:90});sun.shadow.normalBias=.035;sun.shadow.bias=-.0002;sun.shadow.radius=3;scene.add(sun);

function frame(){
  if(!ready||!renderer)return;
  const targets=views[view].objects,box=new T.Box3();targets.forEach(o=>box.expandByObject(o));
  const center=box.getCenter(new T.Vector3());
  const direction=new T.Vector3(reverse?-1:.9,.62,1.4).normalize();
  const vertical=T.MathUtils.degToRad(camera.fov),horizontal=2*Math.atan(Math.tan(vertical/2)*camera.aspect);
  const right=new T.Vector3().crossVectors(new T.Vector3(0,1,0),direction).normalize(),up=new T.Vector3().crossVectors(direction,right);let distance=8;
  for(const object of targets){const b=new T.Box3().setFromObject(object);for(const x of[b.min.x,b.max.x])for(const y of[b.min.y,b.max.y])for(const z of[b.min.z,b.max.z]){
    const corner=new T.Vector3(x,y,z).sub(center),depth=corner.dot(direction);
    distance=Math.max(distance,depth+Math.abs(corner.dot(right))/Math.tan(horizontal/2)*1.12,depth+Math.abs(corner.dot(up))/Math.tan(vertical/2)*1.12);
  }}
  camera.position.copy(center).addScaledVector(direction,distance);camera.lookAt(center);camera.updateMatrixWorld();
  const bounds=targets.map(object=>{const b=new T.Box3().setFromObject(object),points=[];for(const x of[b.min.x,b.max.x])for(const y of[b.min.y,b.max.y])for(const z of[b.min.z,b.max.z])points.push(new T.Vector3(x,y,z).project(camera));return {name:object.name,minX:Math.min(...points.map(p=>p.x)),maxX:Math.max(...points.map(p=>p.x)),minY:Math.min(...points.map(p=>p.y)),maxY:Math.max(...points.map(p=>p.y))};});
  canvas.dataset.frameEvidence=JSON.stringify({view,comparison:comparison.visible,reverse,bounds});
  document.querySelector('[data-view-title]').textContent=comparison.visible?'Primitive blockout':views[view].title;
  document.querySelector('[data-view-description]').textContent=comparison.visible?'Matching asset bounds, same camera and lighting.':views[view].description;
  document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));document.querySelector('[data-orbit]').setAttribute('aria-pressed',String(reverse));
  render();
}
function render(){if(renderer)renderer.render(scene,camera);}
function controls(enabled){document.querySelectorAll('button:not([data-retry])').forEach(b=>b.disabled=!enabled);}
function resize(){if(!renderer)return;const rect=canvas.getBoundingClientRect();renderer.setSize(rect.width,rect.height,false);camera.aspect=rect.width/rect.height;camera.updateProjectionMatrix();frame();}
function record(){
  const metrics=modelMetrics(models),counts={};instances.forEach(root=>{const a=root.userData.imported,key=a.model||a.asset;counts[key]=(counts[key]||0)+1;});
  const evidence={scene:'AR(N)AN Phase 1 asset showcase',state:'ready',...library.stats(),importedInstances:instances.length,distinctTypes:Object.keys(counts).length,counts,...metrics,
    collisionBodies:colliders.length,groundAlignmentMaxError:Math.max(...instances.map(root=>Math.abs(new T.Box3().setFromObject(root).min.y-root.position.y))),
    models:instances.map(root=>({name:root.name,...root.userData.imported,collider:root.userData.collider,triangles:modelMetrics(root).triangles})),
    renderer:{triangles:renderer.info.render.triangles,drawCalls:renderer.info.render.calls},comparison:'Primitive blockout is optional and hidden by default'};
  diagnostics.textContent=JSON.stringify(evidence,null,2);canvas.dataset.assetEvidence=JSON.stringify(evidence);
  summary.textContent=`${evidence.importedInstances} imported instances · ${evidence.distinctTypes} distinct types · ${evidence.loadedFiles} local GLB files · ${metrics.missingTextures.length} missing textures.`;
  if(metrics.missingTextures.length)throw Error('One or more embedded textures did not decode');
}
async function mount(){
  controls(false);canvas.dataset.assetEvidence=JSON.stringify({state:'loading'});
  document.querySelector('[data-retry]').hidden=true;status.hidden=false;status.textContent='Loading verified local models…';
  try{
    renderer ||=new T.WebGLRenderer({canvas,antialias:true,alpha:false});renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.1;renderer.outputColorSpace=T.SRGBColorSpace;
    // The four requests are shared; repeated bollards, plants and pavers reuse their geometry and maps.
    await Promise.all(['architecture','tree','fern','planter'].map(id=>library.get(id)));
    const place=async(id,options)=>{const root=await library.instantiate(id,options);models.add(root);instances.push(root);if(root.userData.collider)colliders.push(root.userData.collider);return root;};
    for(const {asset,...options} of showcasePlan)await place(asset,options);
    const building=instances.find(o=>o.name==='office'),shop=instances.find(o=>o.name==='shop'),tree=instances.find(o=>o.name==='tree');
    const furniture=instances.filter(o=>!['office','shop','tree','paving'].includes(o.name));
    for(const object of[building,shop]){
      const b=new T.Box3().setFromObject(object),s=b.getSize(new T.Vector3()),c=b.getCenter(new T.Vector3());
      block(c.x,b.min.y,c.z,s.x,s.y,s.z,concrete,comparison).castShadow=true;
      block(c.x,b.max.y,c.z,s.x+.25,.25,s.z+.25,concrete,comparison).castShadow=true;
    }
    for(const root of instances.filter(o=>o.userData.collider)){
      const c=root.userData.collider;
      const wire=new T.Mesh(new T.BoxGeometry(c.w,c.h-c.minY,c.d),new T.MeshBasicMaterial({color:'#925d19',wireframe:true}));wire.position.set(c.x,(c.h+c.minY)/2,c.z);collisionLines.add(wire);
    }
    views.street={objects:[building,shop,tree,...furniture],title:'Streetscape',description:'Complete imported buildings, planting and a clear pedestrian strip.'};
    views.building={objects:[building],title:'Complete multi-story building',description:'Building_Large_2.gltf · 45,122 source triangles · uniform scale.'};
    views.shop={objects:[shop],title:'Shopfront',description:'Building_Small_1.gltf · recessed doors, windows, cornices and roof detail.'};
    views.planting={objects:[tree,...furniture.filter(o=>o.name==='fern'&&o.position.x<0)],title:'Urban shade tree',description:'CommonTree_1.gltf and Fern_1.gltf · real foliage meshes and a trunk collision proxy.'};
    views.furniture={objects:furniture.filter(o=>o.position.x>0&&!['aircon'].includes(o.name)),title:'Street furniture',description:'Imported planter, ferns, bollards and a flush drain beside the pedestrian strip.'};
    ready=true;resize();record();status.hidden=true;controls(true);
  }catch(error){ready=false;controls(false);models.clear();instances.length=0;colliders.length=0;comparison.clear();collisionLines.clear();library.dispose();library=createModelLibrary();status.textContent=`Asset review could not load. ${error.message}`;summary.textContent='Loading did not complete. No success counts reported.';diagnostics.textContent=JSON.stringify({state:'error',message:error.message},null,2);canvas.dataset.assetEvidence=diagnostics.textContent;document.querySelector('[data-retry]').hidden=false;render();}
}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{view=b.dataset.view;reverse=false;frame();}));
document.querySelector('[data-compare]').addEventListener('click',event=>{comparison.visible=!comparison.visible;instances.filter(o=>['office','shop'].includes(o.name)).forEach(o=>o.visible=!comparison.visible);event.currentTarget.setAttribute('aria-pressed',String(comparison.visible));frame();});
document.querySelector('[data-collisions]').addEventListener('click',event=>{collisionLines.visible=!collisionLines.visible;event.currentTarget.setAttribute('aria-pressed',String(collisionLines.visible));render();});
document.querySelector('[data-orbit]').addEventListener('click',()=>{reverse=!reverse;frame();});
document.querySelector('[data-retry]').addEventListener('click',mount);
new ResizeObserver(resize).observe(canvas.parentElement);
canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();ready=false;controls(false);status.hidden=false;status.textContent='The graphics context was lost. Reload this review to restore it.';summary.textContent='Scene unavailable until the graphics context is restored.';diagnostics.textContent=JSON.stringify({state:'error',message:'WebGL context lost'},null,2);canvas.dataset.assetEvidence=diagnostics.textContent;});
addEventListener('pagehide',event=>{if(!event.persisted){library.dispose();renderer?.dispose();}});
mount();
