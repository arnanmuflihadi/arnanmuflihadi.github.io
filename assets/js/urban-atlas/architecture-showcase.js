import * as T from '../vendor/three-atlas.module.js?v=16';
import {createModelLibrary,modelMetrics} from './model-library.js?v=15';
import {createArchitectureDesignSystem} from './architecture-design-system.js?v=34';
import {createShowcaseDaylight,daylightPreset} from './showcase-daylight.js?v=30';

const canvas=document.querySelector('canvas'),status=document.querySelector('[data-status]'),summary=document.querySelector('[data-summary]'),diagnostics=document.querySelector('[data-diagnostics]');
if(new URLSearchParams(location.search).has('capture'))document.documentElement.dataset.architectureCapture='true';
const scene=new T.Scene(),lighting=createShowcaseDaylight(scene),contextFinishes=new Map(),contextGeometry=new Set(),contextMaterials=new Set();
const camera=new T.PerspectiveCamera(40,1,.1,240),context=new T.Group(),collisionLines=new T.Group();scene.add(context,collisionLines);collisionLines.visible=false;
let renderer,library,system,ready=false,view='variants';const roots={},views={},pairs={};
const material=color=>{const m=new T.MeshStandardMaterial({color,roughness:.94});contextMaterials.add(m);return m;};
const earth=material('#90a381'),curb=material('#c1c7c1'),road=material('#69767a');
function block(x,y,z,w,h,d,mat,parent=context){const geometry=new T.BoxGeometry(w,h,d),mesh=new T.Mesh(geometry,mat);contextGeometry.add(geometry);mesh.position.set(x,y+h/2,z);mesh.receiveShadow=true;parent.add(mesh);return mesh;}
block(0,-.23,-4,60,.23,40,earth);block(0,-.04,3.6,55,.185,7.2,curb);block(0,-.04,10.4,60,.04,6,road);block(0,.03,7.14,55,.13,.13,curb);
const foundationGeometry=new T.BoxGeometry(1,1,1),foundations=new T.InstancedMesh(foundationGeometry,curb,3);contextGeometry.add(foundationGeometry);foundations.name='Continuous building foundation supports';foundations.receiveShadow=true;context.add(foundations);

function lettering(title,subtitle){
  const c=document.createElement('canvas');c.width=1024;c.height=192;const p=c.getContext('2d');p.fillStyle='#29413d';p.fillRect(0,0,c.width,c.height);p.textAlign='center';p.fillStyle='#f0dfb5';p.font='600 66px Georgia';p.fillText(title,512,91);p.font='24px Arial';p.fillStyle='#d0cbb5';p.fillText(subtitle,512,146);const t=new T.CanvasTexture(c);t.name='Project-authored fictional architectural signage';t.colorSpace=T.SRGBColorSpace;return t;
}
function setControls(enabled){document.querySelectorAll('button:not([data-retry])').forEach(b=>b.disabled=!enabled);}
function visibleRoots(){return Object.values(roots).filter(r=>r.visible);}
function alignFoundations(){
  const visible=visibleRoots();foundations.count=visible.length;
  visible.forEach((root,i)=>{const c=root.userData.collider,box=new T.Box3(new T.Vector3(c.x-c.w/2,0,c.z-c.d/2),new T.Vector3(c.x+c.w/2,0,c.z+c.d/2)).applyMatrix4(root.matrixWorld),size=box.getSize(new T.Vector3()),center=box.getCenter(new T.Vector3()),o=new T.Object3D();o.position.set(center.x,.08,center.z);o.scale.set(size.x,.16,size.z);o.updateMatrix();foundations.setMatrixAt(i,o.matrix);});
  foundations.instanceMatrix.needsUpdate=true;foundations.computeBoundingSphere();
}
function localBounds(objects){const box=new T.Box3();objects.forEach(o=>box.expandByObject(o));return box;}
function fit(box){
  const target=box.getCenter(new T.Vector3()),direction=new T.Vector3(.83,.55,1.6).normalize(),right=new T.Vector3().crossVectors(new T.Vector3(0,1,0),direction).normalize(),up=new T.Vector3().crossVectors(direction,right);
  const vertical=T.MathUtils.degToRad(camera.fov),horizontal=2*Math.atan(Math.tan(vertical/2)*camera.aspect);let distance=12;
  for(const x of[box.min.x,box.max.x])for(const y of[box.min.y,box.max.y])for(const z of[box.min.z,box.max.z]){
    const corner=new T.Vector3(x,y,z).sub(target),depth=corner.dot(direction);
    distance=Math.max(distance,depth+Math.abs(corner.dot(right))/Math.tan(horizontal/2)*1.12,depth+Math.abs(corner.dot(up))/Math.tan(vertical/2)*1.12);
  }
  camera.position.copy(target).addScaledVector(direction,distance);camera.lookAt(target);
}
function render(){renderer?.render(scene,camera);}
function cameraEvidence(){return {position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),fov:camera.fov,aspect:camera.aspect,eyeHeight:views[view]?.pedestrian||view==='street-level'?camera.position.y-.16:null};}
function updateEvidence(){
  const groups=visibleRoots(),counts={};let authoredInstances=0,authoredTriangles=0,importedTriangles=0,renderedMeshes=0;
  for(const root of groups){root.traverse(o=>{if(!o.isMesh)return;renderedMeshes++;const tris=(o.geometry.index?.count||o.geometry.attributes.position.count)/3*(o.isInstancedMesh?o.count:1);if(o.userData.projectAuthored){authoredInstances+=o.isInstancedMesh?o.count:1;authoredTriangles+=tris;}else importedTriangles+=tris;});root.traverse(o=>{if(o.userData.imported){const id=o.userData.imported.model||o.userData.imported.asset;counts[id]=(counts[id]||0)+1;}});}
  const textureSet=new Set();for(const root of[context,...groups])root.traverse(o=>{for(const m of o.material?(Array.isArray(o.material)?o.material:[o.material]):[])for(const value of Object.values(m))if(value?.isTexture)textureSet.add(value);});
  const missing=[...textureSet].filter(t=>!(t.image?.width>0&&t.image?.height>0)).map(t=>t.name||t.uuid);
  const bodies=groups.flatMap(root=>root.userData.variantId?system.collisionBodies(root):root.userData.collider?[root.userData.collider]:[]);
  const evidence={scene:'AR(N)AN Phase 1.5 architectural study',state:'ready',iteration:'Focused final visual correction',view,...library.stats(),architectureCache:system.stats(),counts,renderedArchitectureRoots:groups.length,renderedMeshes,importedTriangles,authoredInstances,authoredTriangles,referencedTextures:textureSet.size,missingTextures:missing,camera:cameraEvidence(),lighting:daylightPreset,groundAlignment:{terrainTop:0,sidewalkTop:.16,foundationTop:.16,foundationInstances:foundations.count},variants:groups.filter(r=>r.userData.architecture).map(r=>({...r.userData.architecture,bounds:boundsRecord(r),colliders:system.collisionBodies(r)})),collisionBodies:bodies.length,renderer:{drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles},humanReview:{targetAverage:4,maximum:5,status:'Awaiting human review of visual correction',score:null},comparisonMethod:'Before/after pairs use the same precomputed union bounds, camera,scale and lighting'};
  diagnostics.textContent=JSON.stringify(evidence,null,2);canvas.dataset.assetEvidence=JSON.stringify(evidence);summary.textContent=`${groups.length} architectural composition${groups.length===1?'':'s'} visible · ${renderedMeshes} mesh batches · ${library.stats().loadedFiles} cached GLBs · ${missing.length} missing textures.`;
  if(missing.length)throw Error('An architectural texture did not decode');
}
function boundsRecord(root){const b=new T.Box3().setFromObject(root);return {min:b.min.toArray(),max:b.max.toArray()};}
function frame(){
  if(!ready||!renderer)return;
  Object.values(roots).forEach(r=>r.visible=false);const selected=views[view];selected.roots.forEach(id=>roots[id].visible=true);
  if(selected.camera){camera.position.fromArray(selected.camera.position);camera.lookAt(new T.Vector3(...selected.camera.target));}else fit(selected.bounds);
  camera.updateMatrixWorld(true);alignFoundations();document.querySelector('[data-view-title]').textContent=selected.title;document.querySelector('[data-view-description]').textContent=selected.description;
  document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));updateCollisionLines();render();updateEvidence();
  canvas.dataset.frameEvidence=JSON.stringify({view,camera:cameraEvidence(),bounds:boundsRecordGroup(selected.roots.map(id=>roots[id]))});
}
function boundsRecordGroup(objects){const b=localBounds(objects);return {min:b.min.toArray(),max:b.max.toArray()};}
function updateCollisionLines(){
  for(const mesh of collisionLines.children){mesh.geometry.dispose();mesh.material.dispose();}collisionLines.clear();if(!collisionLines.visible)return;
  for(const root of visibleRoots())for(const c of root.userData.variantId?system.collisionBodies(root):[]){const m=new T.Mesh(new T.BoxGeometry(c.w,c.h-c.minY,c.d),new T.MeshBasicMaterial({color:'#ad682b',wireframe:true}));m.position.set(c.x,(c.h+c.minY)/2,c.z);collisionLines.add(m);}
}
function resize(){if(!renderer)return;const b=canvas.getBoundingClientRect();renderer.setSize(b.width,b.height,false);camera.aspect=b.width/b.height;camera.updateProjectionMatrix();frame();}
async function mount(){
  setControls(false);document.querySelector('[data-retry]').hidden=true;status.hidden=false;status.textContent='Loading the verified source meshes and architectural layers…';library=createModelLibrary();system=createArchitectureDesignSystem(library,{signTexture:lettering});
  try{
    renderer ||=new T.WebGLRenderer({canvas,antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=daylightPreset.exposure;renderer.outputColorSpace=T.SRGBColorSpace;
    await Promise.all(['architecture','tree','fern','planter'].map(id=>library.get(id)));
    roots['office-before']=await library.instantiate('architecture',{model:'office',height:22.4});roots['office-after']=await system.create('office');
    roots['shop-before']=await library.instantiate('architecture',{model:'shop',height:13.6});roots['shop-after']=await system.create('commercial');const small=await system.create('neighborhood');
    for(const [id,root]of Object.entries(roots)){root.position.set(0,.16,id.startsWith('office')?-6.399991:-3.96315);scene.add(root);root.updateMatrixWorld(true);}
    roots['gallery-office']=roots['office-after'].clone(true);roots['gallery-commercial']=roots['shop-after'].clone(true);roots['gallery-neighborhood']=small;
    for(const [key,x]of[['gallery-office',-13.5],['gallery-commercial',4],['gallery-neighborhood',14]]){const root=roots[key];root.position.set(x,.16,-root.userData.architecture.front);scene.add(root);root.updateMatrixWorld(true);}
    pairs.office=localBounds([roots['office-before'],roots['office-after']]);pairs.shop=localBounds([roots['shop-before'],roots['shop-after']]);
    const gallery=['gallery-office','gallery-commercial','gallery-neighborhood'],galleryBounds=localBounds(gallery.map(id=>roots[id]));
    views['office-before']={roots:['office-before'],bounds:pairs.office,title:'01 / Original imported office',description:'Phase 1 imported baseline. Same camera, light and source scale as the enhanced office.'};
    views['office-after']={roots:['office-after'],bounds:pairs.office,title:'02 / Contemporary Tropical Office',description:'Deep shading fins, recessed glazing, a planted terrace and a sheltered stone lobby.'};
    views['shop-before']={roots:['shop-before'],bounds:pairs.shop,title:'03 / Original imported shop',description:'Phase 1 imported baseline. Same camera, light and source scale as the enhanced mixed-use building.'};
    views['shop-after']={roots:['shop-after'],bounds:pairs.shop,title:'04 / Urban Mixed-Use Commercial Building',description:'Terracotta plaster, a shaded arcade, roster screen, timber shutters and a roof-access pavilion.'};
    views.variants={roots:gallery,bounds:galleryBounds,title:'05 / Three architectural variants',description:'Tropical office · mixed-use commercial · neighborhood shopfront. Original conceptual designs.'};
    views.detail={roots:['office-after'],camera:{position:[10.6,10.8,10.5],target:[2.8,10.5,.2]},title:'06 / Façade depth and material study',description:'Actual recessed source glass, cast-concrete fins, darker seams and imported terrace planting.'};
    views['street-level']={roots:gallery,camera:{position:[14,1.81,12],target:[6.8,2.3,.7]},title:'07 / Street level at character scale',description:'Camera eye height 1.65 m above the sidewalk. Clearances above the porches are at least 2.8 m.'};
    views.neighborhood={roots:['gallery-neighborhood'],bounds:localBounds([roots['gallery-neighborhood']]),title:'08 / Human-Scale Neighborhood Shopfront',description:'A cropped two-story imported body, timber frontage, vented gable and deep clay eaves. Source door scale is retained.'};
    views['office-entrance']={roots:gallery,pedestrian:true,camera:{position:[-10.8,1.81,10.8],target:[-13.5,1.65,.35]},title:'09 / Office entrance',description:'Eye height 1.65 m. Double doors, transom, shaded lobby and a 20 mm porch transition.'};
    views['commercial-arcade']={roots:gallery,pedestrian:true,camera:{position:[6.6,1.81,11],target:[4,1.65,.7]},title:'10 / Commercial arcade',description:'Eye height 1.65 m. Glazed doors, display bays, stone thresholds and satin metal frames.'};
    views['neighborhood-frontage']={roots:gallery,pedestrian:true,camera:{position:[16.2,1.81,12],target:[14,3.4,.6]},title:'11 / Neighborhood frontage',description:'Eye height 1.65 m. Timber framing, fired-clay eaves and a separate entrance leaf.'};
    views['sidewalk-interface']={roots:gallery,pedestrian:true,camera:{position:[.4,1.81,7.8],target:[1,.48,.7]},title:'12 / Sidewalk interfaces',description:'Eye height 1.65 m. Porch surfaces rise 20 mm above the continuous sidewalk.'};
    views['pedestrian-composition']={roots:gallery,pedestrian:true,camera:{position:[4,1.81,43],target:[-3,10.5,-.5]},title:'13 / Three buildings from the street',description:'Eye height 1.65 m. Same 40° lens and daytime lighting as the four close inspections.'};
    for(let x=-24;x<=24;x+=3)for(const z of[2.4,5.4]){
      const paver=await library.instantiate('architecture',{model:'paving',height:.15,x,y:.01,z,collidable:false});paver.traverse(o=>{if(!o.isMesh)return;o.castShadow=false;const previous=o.material;if(!contextFinishes.has(previous.uuid)){const m=previous.clone();m.color.set('#d5d9d2');m.roughness=.98;m.map=null;m.normalMap=null;m.roughnessMap=null;m.metalnessMap=null;m.aoMap=null;contextFinishes.set(previous.uuid,m);}o.material=contextFinishes.get(previous.uuid);});context.add(paver);
    }
    const jointGeometry=new T.BoxGeometry(1,1,1),jointMaterial=material('#b5beb6'),jointMatrices=[];contextGeometry.add(jointGeometry);
    for(let x=-25.5;x<=25.5;x+=3){const o=new T.Object3D();o.position.set(x,.161,3.9);o.scale.set(.012,.002,6);o.updateMatrix();jointMatrices.push(o.matrix.clone());}
    for(const z of[.9,3.9,6.9]){const o=new T.Object3D();o.position.set(0,.161,z);o.scale.set(51,.002,.012);o.updateMatrix();jointMatrices.push(o.matrix.clone());}
    const joints=new T.InstancedMesh(jointGeometry,jointMaterial,jointMatrices.length);jointMatrices.forEach((m,i)=>joints.setMatrixAt(i,m));joints.name='Sidewalk module joints';context.add(joints);
    for(const[x,z,height]of[[-25,-2,7.5],[24,-6,8]])context.add(system.finishVegetation(await library.instantiate('tree',{height,x,y:0,z,collision:'trunk'}),{tree:true}));
    for(const x of[-24,22]){context.add(await library.instantiate('planter',{height:.65,x,y:.16,z:3.8}));context.add(system.finishVegetation(await library.instantiate('fern',{height:.8,x,y:.76,z:3.8,collidable:false})));}
    ready=true;resize();status.hidden=true;setControls(true);
    const hash=location.hash.slice(1);if(Object.hasOwn(views,hash)){view=hash;frame();}
  }catch(error){ready=false;setControls(false);status.hidden=false;status.textContent=`Architectural review could not load. ${error.message}`;canvas.dataset.assetEvidence=JSON.stringify({state:'error',message:error.message});diagnostics.textContent=canvas.dataset.assetEvidence;summary.textContent='No successful model counts reported.';document.querySelector('[data-retry]').hidden=false;}
}
document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{view=button.dataset.view;history.replaceState(null,'','#'+view);frame();}));
addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(ready&&Object.hasOwn(views,id)){view=id;frame();}});
document.querySelectorAll('[data-gallery-view]').forEach(link=>link.addEventListener('click',event=>{if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;event.preventDefault();view=link.dataset.galleryView;history.replaceState(null,'','#'+view);frame();document.querySelector('.review-stage').scrollIntoView({block:'start',behavior:'instant'});}));
document.querySelector('[data-collisions]').addEventListener('click',event=>{collisionLines.visible=!collisionLines.visible;event.currentTarget.setAttribute('aria-pressed',String(collisionLines.visible));frame();});
document.querySelector('[data-retry]').addEventListener('click',()=>location.reload());
new ResizeObserver(resize).observe(canvas.parentElement);canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();ready=false;setControls(false);status.hidden=false;status.textContent='Graphics context lost. Reload the review to restore it.';canvas.dataset.assetEvidence=JSON.stringify({state:'error',message:'WebGL context lost'});});
addEventListener('pagehide',event=>{if(!event.persisted){system?.dispose();library?.dispose();lighting.dispose();contextFinishes.forEach(m=>m.dispose());contextGeometry.forEach(g=>g.dispose());contextMaterials.forEach(m=>m.dispose());renderer?.dispose();}});
mount();
