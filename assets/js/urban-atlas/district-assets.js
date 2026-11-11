import * as T from '../vendor/three-atlas.module.js?v=16';
import{createModelLibrary,modelMetrics}from'./model-library.js?v=15';
import{createArchitectureDesignSystem}from'./architecture-design-system.js?v=34';
import{districtBuildings,skylineBuildings,buildingTransform,buildingObstacles,variantFront}from'./district-plan.js?v=40';
import{treeSites,planterSites,groundHeight}from'./layout.js?v=40';
import{createDistrictArtwork}from'./district-artwork.js?v=40';

export async function assembleDistrictAssets(scene,{library=createModelLibrary(),artwork=createDistrictArtwork(),signal,obstacles=[]}={}){
  const container=new T.Group();container.name='Phase 2 verified district assets';const system=createArchitectureDesignSystem(library,{signTexture:(a,b)=>artwork.sign(a,b)}),batches=new Map(),ownedGeometry=new Set(),ownedMaterials=new Set(),roots=[],trees=[],counts={};let alive=true;
  const unit=new T.BoxGeometry(1,1,1),potGeometry=new T.CylinderGeometry(.8,1,1,8);ownedGeometry.add(unit);ownedGeometry.add(potGeometry);
  const pigment=color=>{const m=new T.MeshStandardMaterial({color,roughness:.9});ownedMaterials.add(m);return m;},wood=pigment('#8b6949'),paper=pigment('#d6c59f'),red=pigment('#a45f49'),sage=pigment('#6e8877'),glassFinishes=new Map(),roomFinishes=new Map();
  const stats={buildings:[],importedInstances:counts,signage:[],propColliders:[]},moduleFinishes=new Map();
  function record(root){root.traverse(o=>{if(o.userData.imported){const k=o.userData.imported.model||o.userData.imported.asset;counts[k]=(counts[k]||0)+1;}});}
  function addBatch(root){root.updateMatrixWorld(true);record(root);root.traverse(o=>{if(!o.isMesh)return;const key=o.geometry.uuid+o.material.uuid;if(!batches.has(key))batches.set(key,{geometry:o.geometry,material:o.material,matrices:[],authored:!!o.userData.projectAuthored});const b=batches.get(key);if(o.isInstancedMesh){const m=new T.Object3D().matrix;for(let i=0;i<o.count;i++){o.getMatrixAt(i,m);b.matrices.push(o.matrixWorld.clone().multiply(m));}}else b.matrices.push(o.matrixWorld.clone());});}
  function detail(root,geometry,material,x,y,z,w,h,d){const mesh=new T.Mesh(geometry,material);mesh.position.set(x,y,z);mesh.scale.set(w,h,d);mesh.userData.projectAuthored=true;root.add(mesh);return mesh;}
  function occupy(root,p){
    if(p.variant==='office')return;
    if(!glassFinishes.has(p.display)){const m=system.palette.glass.clone();m.transparent=true;m.opacity=.36;m.depthWrite=false;m.roughness=.64;ownedMaterials.add(m);glassFinishes.set(p.display,m);const room=new T.MeshStandardMaterial({map:artwork.display(p.display),color:'#f3ead8',roughness:.96,emissive:'#a68b60',emissiveIntensity:.12});ownedMaterials.add(room);roomFinishes.set(p.display,room);}
    root.traverse(o=>{if(o.isMesh&&o.material===system.palette.glass)o.material=glassFinishes.get(p.display);});
    const front=variantFront[p.variant],centers=p.variant==='commercial'?[-2.5,2.5]:[0],width=p.variant==='commercial'?4:3.72;
    for(const x of centers){const plane=new T.PlaneGeometry(width,2.08);ownedGeometry.add(plane);detail(root,plane,roomFinishes.get(p.display),x,1.23,front+.06,1,1,1);const shelfX=p.variant==='commercial'?x+Math.sign(x)*.85:-.65;
      for(const y of[.8,1.58]){detail(root,unit,wood,shelfX,y,front+.13,1.25,.055,.15);for(let i=0;i<6;i++){const h=p.display==='cafe'?.11:.19+(i%3)*.055;detail(root,p.display==='books'?unit:potGeometry,p.display==='cafe'?paper:[paper,red,sage][i%3],shelfX-.5+i*.2,y+.03+h/2,front+.13,p.display==='books'?.13:.065,h,.1);}}
    }
  }
  function rename(root,p){root.traverse(o=>{if(o.isMesh&&o.material.name==='Project: original architectural lettering'){const size=o.geometry.parameters,map=artwork.sign(p.title,p.subtitle,size.width,size.height),mat=new T.MeshBasicMaterial({map,toneMapped:false});mat.name='District sign: '+p.title;ownedMaterials.add(mat);o.material=mat;stats.signage.push({title:p.title,worldSize:[size.width,size.height],textureSize:[map.image.width,map.image.height],mipmaps:map.generateMipmaps,minFilter:map.minFilter,anisotropy:map.anisotropy});}});}
  async function modular(model,options){const root=await library.instantiate('architecture',{model,collidable:false,...options});root.traverse(o=>{if(!o.isMesh||!/Glass|FakeInterior/.test(o.material.name))return;const previous=o.material;if(!moduleFinishes.has(previous.uuid)){const m=system.palette.glass.clone();m.name='District module sky glazing';ownedMaterials.add(m);moduleFinishes.set(previous.uuid,m);}o.material=moduleFinishes.get(previous.uuid);});addBatch(root);return root;}
  function dispose(){if(!alive)return;alive=false;container.removeFromParent();container.traverse(o=>{if(o.isInstancedMesh)o.dispose();});system.dispose();library.dispose();artwork.dispose();ownedGeometry.forEach(g=>g.dispose());ownedMaterials.forEach(m=>m.dispose());signal?.removeEventListener('abort',dispose);}
  try{
    await Promise.all(['architecture','tree','fern','planter'].map(id=>library.get(id)));if(signal?.aborted)throw Error('District asset assembly cancelled');
    for(const p of[...districtBuildings,...skylineBuildings]){
      const root=await system.create(p.variant),t=buildingTransform(p);root.position.set(t.x,t.y,t.z);root.rotation.y=t.rotation;root.updateMatrixWorld(true);
      if(p.backgroundSign)rename(root,{...p,title:p.backgroundSign,subtitle:'KAWASAN TAMAN'});
      if(p.title){rename(root,p);occupy(root,p);const expected=buildingObstacles(p),actual=system.collisionBodies(root);if(actual.length!==expected.length||actual.some((c,i)=>['x','z','w','d','minY','h'].some(k=>Math.abs(c[k]-expected[i][k])>.00001)))throw Error('Imported building collision does not match the district plan: '+p.id);const planned=obstacles.filter(o=>o.building===p.id);planned.forEach((o,i)=>Object.assign(o,actual[i]));}
      roots.push(root);stats.buildings.push({id:p.id,variant:p.variant,skyline:!p.title,transform:t,colliders:p.title?system.collisionBodies(root):[],metrics:modelMetrics(root)});addBatch(root);
    }
    // Imported façade modules, normalized uniformly, form the station and pavilion.
    for(let x=-32.5;x<=-13.5;x+=2.1){await modular('entrance',{x,y:.52,z:-.15,height:3.35});await modular('glazing',{x,y:.52,z:-5.75,height:3.35,rotation:Math.PI});}
    for(let x=24;x<=34;x+=2)await modular('civic',{x,y:.57,z:24.55,height:3.3,rotation:Math.PI});
    for(const x of[-12.1,-10.1])await modular('glazing',{x,y:.24,z:14,height:2.5,rotation:Math.PI});
    for(const x of[-33,-13]){const root=await modular('bollard',{x,y:.24,z:6.8,height:.75,collidable:true}),body={...root.userData.collider,importedProp:'bollard'};obstacles.push(body);stats.propColliders.push(body);}
    for(const[x,z]of[[-20,-12],[20,-12],[-40,13],[40,13],[0,-36]])await modular('manhole',{x,y:.056,z,height:.015});
    for(const x of[-31,-7,7,31])for(const z of[-14.7,-9.3])await modular('drain',{x,y:.056,z,height:.02});
    for(const[x,z,size]of treeSites){const tree=system.finishVegetation(await library.instantiate('tree',{x,y:groundHeight(x,z),z,height:6.8*size,rotation:(x+z)*.17,collision:'trunk'}),{tree:true});tree.userData.crownScale=size;const planned=obstacles.find(o=>o.tree&&o.x===x&&o.z===z);if(planned)Object.assign(planned,tree.userData.collider,{h:groundHeight(x,z)+6.8*size});trees.push(tree);record(tree);container.add(tree);}
    for(const[x,z]of planterSites){const planter=await library.instantiate('planter',{x,y:groundHeight(x,z),z,height:.75}),body=obstacles.find(o=>o.planter&&o.x===x&&o.z===z);if(body)Object.assign(body,planter.userData.collider);stats.propColliders.push({...planter.userData.collider,importedProp:'planter'});addBatch(planter);const fern=system.finishVegetation(await library.instantiate('fern',{x,y:groundHeight(x,z)+.6,z,height:.7,collidable:false}));addBatch(fern);}
    for(const[x,z]of[[-34,7],[-27,14],[-33,14],[-7,1],[7,1],[16,17],[29,18]])addBatch(system.finishVegetation(await library.instantiate('fern',{x,y:groundHeight(x,z)+.12,z,height:.85,collidable:false})));
    let triangles=0,authoredTriangles=0;
    for(const b of batches.values()){const mesh=new T.InstancedMesh(b.geometry,b.material,b.matrices.length);b.matrices.forEach((m,i)=>mesh.setMatrixAt(i,m));mesh.castShadow=true;mesh.receiveShadow=true;mesh.computeBoundingSphere();mesh.name='District batch: '+b.material.name;mesh.userData.importedDistrict=true;container.add(mesh);const n=(b.geometry.index?b.geometry.index.count:b.geometry.attributes.position.count)/3*b.matrices.length;triangles+=n;if(b.authored)authoredTriangles+=n;}
    scene.add(container);scene.updateMatrixWorld(true);const metrics=modelMetrics(container);Object.assign(stats,{loadedFiles:library.stats().loadedFiles,requests:library.stats().requests,prototypes:system.stats().templates,batches:batches.size,triangles:metrics.triangles,authoredTriangles,missingTextures:metrics.missingTextures,textures:metrics.textures});if(stats.missingTextures.length)throw Error('A district texture is missing');
    signal?.addEventListener('abort',dispose,{once:true});if(signal?.aborted){dispose();throw Error('District asset assembly cancelled');}
    return{stats,roots,prefabCounts:counts,dispose,update(){},frameCamera(camera,adventure){for(const tree of trees){const size=tree.userData.crownScale,limit=(tree.userData.cutCanopy?4.2:3.6)*size,d=Math.hypot(camera.position.x-tree.position.x,camera.position.z-tree.position.z),cut=adventure&&d<limit&&camera.position.y>tree.position.y+2*size&&camera.position.y<tree.position.y+8.5*size;tree.userData.cutCanopy=cut;tree.traverse(o=>{if(o.isMesh&&o.material.name.includes('Leaves'))o.visible=!cut;});}}};
  }catch(error){dispose();throw error;}
}
