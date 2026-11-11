import * as T from '../vendor/three-atlas.module.js?v=16';

export const architecturalVariants=Object.freeze({
  office:{name:'Contemporary Tropical Office',source:'office',height:22.4,front:6.399991,sign:'TERAS ATLAS'},
  commercial:{name:'Urban Mixed-Use Commercial Building',source:'shop',height:13.6,front:3.96315,sign:'RUKO SENJA'},
  neighborhood:{name:'Human-Scale Neighborhood Shopfront',source:'shop',height:13.6,front:3.96315,sign:'RUANG JIRAN'}
});

function colorTexture(colors,width=16,height=64){
  const data=new Uint8Array(width*height*4),stops=colors.map(c=>new T.Color(c));
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){
    const t=y/(height-1)*(stops.length-1),a=Math.min(stops.length-2,Math.floor(t)),c=stops[a].clone().lerp(stops[a+1],t-a);
    const grain=Math.sin(x*.4+y*.08)*.0015,index=(y*width+x)*4;
    data[index]=Math.round(Math.min(1,c.r+grain)*255);data[index+1]=Math.round(Math.min(1,c.g+grain)*255);data[index+2]=Math.round(Math.min(1,c.b+grain)*255);data[index+3]=255;
  }
  const texture=new T.DataTexture(data,width,height);texture.name='Project-authored tonal wash';texture.magFilter=T.LinearFilter;texture.minFilter=T.LinearFilter;texture.needsUpdate=true;return texture;
}

function glazingTexture(){
  const width=64,height=128,data=new Uint8Array(width*height*4),low=new T.Color('#244651'),high=new T.Color('#8eb1ba'),reflection=new T.Color('#d4dfd8');
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){
    const u=x/(width-1),v=y/(height-1),band=Math.exp(-Math.pow((v-.56-u*.24)/.11,2))*.28,c=low.clone().lerp(high,v*.75+.12).lerp(reflection,band),i=(y*width+x)*4;
    data[i]=Math.round(c.r*255);data[i+1]=Math.round(c.g*255);data[i+2]=Math.round(c.b*255);data[i+3]=255;
  }
  const texture=new T.DataTexture(data,width,height);texture.name='Project-authored soft sky reflection';texture.magFilter=T.LinearFilter;texture.minFilter=T.LinearFilter;texture.needsUpdate=true;return texture;
}

function clearFrontageOpening(root,front,owned,{halfWidth=2.23,height=3.05,depth=.5}={}){
  root.updateMatrixWorld(true);const meshes=[];root.traverse(o=>{if(o.isMesh&&!/Glass|FakeInterior/.test(o.material.name))meshes.push(o);});
  const low=[-halfWidth,0,front-depth],high=[halfWidth,height,front+.45];
  const clip=(polygon,axis,value,sign)=>{const next=[];for(let i=0;i<polygon.length;i++){const a=polygon[i],b=polygon[(i+1)%polygon.length],da=(a.p.getComponent(axis)-value)*sign,db=(b.p.getComponent(axis)-value)*sign;if(da<=0)next.push(a);if(da*db<0){const t=da/(da-db);next.push({p:a.p.clone().lerp(b.p,t),n:a.n.clone().lerp(b.n,t).normalize(),u:a.u.clone().lerp(b.u,t)});}}return next;};
  for(const mesh of meshes){
    const source=mesh.geometry,index=source.index;if(!index)continue;const p=source.attributes.position,n=source.attributes.normal,uv=source.attributes.uv,keep=[],positions=[],normals=[],uvs=[];let changed=false;
    for(let i=0;i<index.count;i+=3){const ids=[index.getX(i),index.getX(i+1),index.getX(i+2)],triangle=ids.map(j=>({p:new T.Vector3().fromBufferAttribute(p,j).applyMatrix4(mesh.matrixWorld),n:new T.Vector3().fromBufferAttribute(n,j).transformDirection(mesh.matrixWorld),u:uv?new T.Vector2().fromBufferAttribute(uv,j):new T.Vector2()}));
      if([0,1,2].some(axis=>Math.max(...triangle.map(v=>v.p.getComponent(axis)))<low[axis]||Math.min(...triangle.map(v=>v.p.getComponent(axis)))>high[axis])){keep.push(...ids);continue;}
      changed=true;let inside=triangle;const outside=[];
      for(const axis of[0,1,2])for(const [value,sign]of[[high[axis],1],[low[axis],-1]]){if(!inside.length)break;outside.push(clip(inside,axis,value,-sign));inside=clip(inside,axis,value,sign);}
      for(const polygon of outside)for(let j=1;j<polygon.length-1;j++)for(const v of[polygon[0],polygon[j],polygon[j+1]]){positions.push(...v.p.toArray());normals.push(...v.n.toArray());uvs.push(v.u.x,v.u.y);}
    }
    if(!changed)continue;
    const retained=new T.BufferGeometry();for(const[name,attribute]of Object.entries(source.attributes))retained.setAttribute(name,attribute);retained.setIndex(keep);retained.boundingBox=source.boundingBox?.clone()||null;retained.boundingSphere=source.boundingSphere?.clone()||null;owned.add(retained);mesh.geometry=retained;
    if(positions.length){const cut=new T.BufferGeometry();cut.setAttribute('position',new T.Float32BufferAttribute(positions,3));cut.setAttribute('normal',new T.Float32BufferAttribute(normals,3));cut.setAttribute('uv',new T.Float32BufferAttribute(uvs,2));cut.computeBoundingBox();cut.computeBoundingSphere();owned.add(cut);const edge=new T.Mesh(cut,mesh.material);edge.name='Source-derived frontage opening edges';edge.castShadow=true;edge.receiveShadow=true;edge.userData.importedSource=true;root.add(edge);}
  }
}

// Cutting a cloned source mesh leaves the verified GLB and its shared buffers intact.
function editImported(root,{crop,inset=0,front=0,groundClip=false,glassOffset=0,owned}){
  root.updateMatrixWorld(true);const meshes=[];root.traverse(o=>{if(o.isMesh)meshes.push(o);});
  const planes=crop?[{axis:0,value:crop.halfWidth,sign:1},{axis:0,value:-crop.halfWidth,sign:-1},{axis:1,value:crop.height,sign:1},{axis:2,value:crop.rear,sign:-1}]:[];
  const mix=(a,b,t)=>({p:a.p.clone().lerp(b.p,t),n:a.n.clone().lerp(b.n,t).normalize(),u:a.u.clone().lerp(b.u,t)});
  function clip(polygon,plane){const next=[];for(let j=0;j<polygon.length;j++){
    const a=polygon[j],b=polygon[(j+1)%polygon.length],da=(a.p.getComponent(plane.axis)-plane.value)*plane.sign,db=(b.p.getComponent(plane.axis)-plane.value)*plane.sign;
    if(da<=.000001)next.push(a);if((da<0&&db>0)||(da>0&&db<0))next.push(mix(a,b,da/(da-db)));
  }return next;}
  for(const mesh of meshes){
    const glass=/Glass|FakeInterior/.test(mesh.material.name);if(!crop&&!glass&&!groundClip)continue;
    const source=mesh.geometry,position=source.attributes.position,normal=source.attributes.normal,uv=source.attributes.uv,indices=source.index;
    const positions=[],normals=[],uvs=[];
    const vertex=index=>({p:new T.Vector3().fromBufferAttribute(position,index).applyMatrix4(mesh.matrixWorld),n:normal?new T.Vector3().fromBufferAttribute(normal,index).transformDirection(mesh.matrixWorld):new T.Vector3(0,0,1),u:uv?new T.Vector2().fromBufferAttribute(uv,index):new T.Vector2()});
    for(let i=0;i<(indices?.count||position.count);i+=3){
      const triangle=[0,1,2].map(j=>vertex(indices?indices.getX(i+j):i+j));
      const polygons=groundClip?[clip(triangle,{axis:2,value:front+.15,sign:1}),clip(clip(triangle,{axis:2,value:front+.15,sign:-1}),{axis:1,value:2.9,sign:-1})]:[triangle];
      for(let polygon of polygons){for(const plane of planes){polygon=clip(polygon,plane);if(!polygon.length)break;}
      for(let j=1;j<polygon.length-1;j++)for(const v of[polygon[0],polygon[j],polygon[j+1]]){
        const point=v.p.clone();if(glass&&point.z>front-.45)point.z-=inset;
        positions.push(...point.toArray());normals.push(...v.n.toArray());
        // The source interior atlas UVs do not describe a pane-sized sky reflection.
        if(glass)uvs.push(((point.x/1.6)%1+1)%1,(((point.y-glassOffset)/2.4)%1+1)%1);else uvs.push(v.u.x,v.u.y);
      }}
    }
    mesh.removeFromParent();if(!positions.length)continue;
    const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(positions,3));geometry.setAttribute('normal',new T.Float32BufferAttribute(normals,3));geometry.setAttribute('uv',new T.Float32BufferAttribute(uvs,2));geometry.computeBoundingBox();geometry.computeBoundingSphere();owned.add(geometry);
    const replacement=new T.Mesh(geometry,mesh.material);replacement.name=mesh.name;replacement.castShadow=true;replacement.receiveShadow=true;replacement.userData.importedSource=true;root.add(replacement);
  }
}

export function createArchitectureDesignSystem(library,{signTexture}={}){
  const geometries=new Set(),materials=new Set(),textures=new Set(),sourceFinishes=new Map(),vegetationFinishes=new Map(),templates=new Map();let alive=true;
  const wash=colorTexture(['#f6f7f3','#e7eae5']),glassWash=glazingTexture(),woodWash=colorTexture(['#e1cbb3','#b8a18a','#d2bda3']),stoneWash=colorTexture(['#f0f2ef','#cbd1cc'],16,32);
  for(const t of[wash,glassWash,woodWash,stoneWash])textures.add(t);
  function material(name,color,roughness=.88,extra={}){const m=new T.MeshStandardMaterial({name,color,roughness,metalness:0,map:wash,...extra});materials.add(m);return m;}
  const palette={
    ivory:material('Project: pale cast concrete','#cbd0ca',.92),plaster:material('Project: warm lime plaster','#efe5d2',.96),clay:material('Project: terracotta plaster','#ce947b',.96),
    roof:material('Project: fired clay roof','#b15a40',.94),stone:material('Project: andesite base','#455451',.97,{map:stoneWash}),timber:material('Project: stained timber','#92704f',.86,{map:woodWash}),
    metal:material('Project: satin bronze frames','#60746f',.62,{metalness:.16,map:null}),dark:material('Project: recess shadow','#293b3d'),
    glass:material('Project: stylized sky glazing','#d8e6e7',.5,{map:glassWash,metalness:.04,emissive:'#476f79',emissiveIntensity:.1}),glassLight:material('Project: entrance glazing','#e5eeeb',.54,{map:glassWash,emissive:'#63858a',emissiveIntensity:.11}),
    soil:material('Project: terrace soil','#45533e'),sage:material('Project: painted sage','#a6b59c',.96),contact:material('Project: recessed contact seam','#63726b')
  };
  const box=new T.BoxGeometry(1,1,1),cylinder=new T.CylinderGeometry(1,1,1,8);geometries.add(box);geometries.add(cylinder);
  const roster=new T.Shape();roster.moveTo(-.22,-.22);roster.lineTo(.22,-.22);roster.lineTo(.22,.22);roster.lineTo(-.22,.22);roster.closePath();
  const hole=new T.Shape();hole.moveTo(-.145,-.145);hole.lineTo(-.145,.145);hole.lineTo(.145,.145);hole.lineTo(.145,-.145);hole.closePath();roster.holes.push(hole);
  const vent=new T.ExtrudeGeometry(roster,{depth:.14,bevelEnabled:true,bevelThickness:.012,bevelSize:.012,bevelSegments:1,steps:1});geometries.add(vent);
  function builder(parent){
    const batches=new Map(),solids=[];let details=0;
    function add(geometry,mat,x,y,z,w=1,h=1,d=1,rotation={}){
      const key=geometry.uuid+mat.uuid;if(!batches.has(key))batches.set(key,{geometry,material:mat,matrices:[]});
      const object=new T.Object3D();object.position.set(x,y,z);object.scale.set(w,h,d);object.rotation.set(rotation.x||0,rotation.y||0,rotation.z||0);object.updateMatrix();batches.get(key).matrices.push(object.matrix.clone());details++;
    }
    const block=(x,y,z,w,h,d,mat=palette.ivory,rotation)=>add(box,mat,x,y+h/2,z,w,h,d,rotation);
    function post(x,z,height,mat=palette.stone,radius=.09){add(cylinder,mat,x,height/2,z,radius,height,radius);solids.push({x,z,w:radius*2,d:radius*2,minY:0,h:height});}
    function screen(x,y,z,cols,rows,mat=palette.clay,rotation=0){for(let i=0;i<cols;i++)for(let j=0;j<rows;j++)add(vent,mat,x+(i-(cols-1)/2)*.48,y+j*.48,z,1,1,1,{y:rotation});}
    function commit(){for(const b of batches.values()){const mesh=new T.InstancedMesh(b.geometry,b.material,b.matrices.length);b.matrices.forEach((m,i)=>mesh.setMatrixAt(i,m));mesh.name=b.material.name;mesh.castShadow=true;mesh.receiveShadow=true;mesh.computeBoundingSphere();mesh.userData.projectAuthored=true;parent.add(mesh);}return {details,batches:batches.size,solids};}
    return {add,block,post,screen,commit};
  }
  function finishSource(root,id){root.traverse(o=>{if(!o.isMesh)return;const previous=o.material,key=id+previous.uuid;if(!sourceFinishes.has(key)){
    const m=previous.clone();m.roughness=.9;m.metalness=0;if(m.aoMap)m.aoMapIntensity=.42;
    if(/Glass|FakeInterior/.test(m.name)){m.map=glassWash;m.color.set('#d3e3e2');m.roughness=.52;m.emissive.set(m.name.includes('_2')?'#587b80':'#476f79');m.emissiveIntensity=.1;}
    else if(/RedBrick/.test(m.name)){m.color.set(id==='office'?'#e3e4da':id==='commercial'?'#d19a80':'#bac9af');if(id!=='office'){m.map=wash;m.normalMap=null;m.aoMap=null;m.roughnessMap=null;m.metalnessMap=null;}}
    else if(/Trim|Concrete/.test(m.name)){m.color.set(id==='commercial'?'#ddd6c6':'#d6dcd5');m.map=wash;if(m.normalScale)m.normalScale.set(.4,.4);}
    else if(/Asphalt/.test(m.name)){m.color.set('#65726e');}
    sourceFinishes.set(key,m);materials.add(m);
  }o.material=sourceFinishes.get(key);});}
  function finishVegetation(root,{tree=false}={}){
    root.traverse(o=>{if(!o.isMesh)return;const previous=o.material,key=previous.uuid+(tree?'tree':'plant');if(!vegetationFinishes.has(key)){
      const m=previous.clone(),leaf=!tree||/Leaves/i.test(m.name);m.roughness=.98;m.metalness=0;m.vertexColors=false;
      if(leaf){m.color.set('#b1cda2');m.emissive.set('#35583c');m.emissiveIntensity=.06;if(m.aoMap)m.aoMapIntensity=.2;}
      else{m.color.set('#92775c');m.emissiveIntensity=0;}vegetationFinishes.set(key,m);materials.add(m);
    }o.material=vegetationFinishes.get(key);});return root;
  }
  async function vegetation(root,x,y,z,width=1.2){
    const fern=finishVegetation(await library.instantiate('fern',{height:.58,x,y,z,collidable:false}));root.add(fern);fern.name='Imported terrace fern';fern.userData.terraceVegetation=true;return fern;
  }
  function doorLeaf(root,x,y,z,width,height){const geometry=new T.PlaneGeometry(width,height);geometries.add(geometry);const mesh=new T.Mesh(geometry,palette.glassLight);mesh.position.set(x,y+height/2,z);mesh.name='Project: glazed entrance leaf';mesh.userData.projectAuthored=true;root.add(mesh);}
  function pull(b,x,y,z){b.block(x,y,z,.025,.36,.035,palette.metal);for(const dy of[.025,.31])b.block(x,y+dy,z-.025,.025,.025,.06,palette.metal);}
  function sign(root,b,text,subtitle,x,y,z,width,height){
    b.block(x,y,z,width,height,.12,palette.stone);
    if(signTexture){const map=signTexture(text,subtitle);textures.add(map);const m=new T.MeshStandardMaterial({name:'Project: original architectural lettering',map,roughness:.88});materials.add(m);const geometry=new T.PlaneGeometry(width-.16,height-.1);geometries.add(geometry);const mesh=new T.Mesh(geometry,m);mesh.position.set(x,y+height/2,z+.066);mesh.userData.projectAuthored=true;root.add(mesh);}
  }
  function planter(b,x,y,z,w,d){b.block(x,y,z,w,.38,d,palette.stone);b.block(x,y+.38,z,w-.14,.025,d-.14,palette.soil);}
  async function build(id){
    const spec=architecturalVariants[id];if(!spec)throw Error(`Unknown architectural variant ${id}`);
    const root=await library.instantiate('architecture',{model:spec.source,height:spec.height}),front=spec.front;
    root.name=spec.name;root.userData.variantId=id;finishSource(root,id);
    if(id==='office')root.getObjectByName('Plane235_10')?.removeFromParent();
    clearFrontageOpening(root,front,geometries,id==='office'?{}:{halfWidth:id==='commercial'?4.62:1.98,height:id==='commercial'?2.72:2.7,depth:.6});
    editImported(root,{front,inset:id==='office'?.22:.16,groundClip:id!=='office',glassOffset:id==='office'?0:.8,crop:id==='neighborhood'?{halfWidth:2.1,height:6.2,rear:front-7.8}:null,owned:geometries});
    const b=builder(root),overheads=[];
    if(id==='office'){
      for(const x of[-4.6,4.6])b.block(x,0,front+.03,6.8,.28,.26,palette.stone);
      b.block(0,0,front+1.1,7.35,.02,3.2,palette.stone);
      for(const x of[-7.65,7.65])b.block(x,.28,front+.06,.7,3.5,.32,palette.stone);
      b.block(0,3.85,front+.2,16.2,.32,.8,palette.stone);
      for(const x of[-8,-4.8,-1.6,1.6,4.8,8])b.block(x,4.4,front+.35,.22,17.15,1.05);
      for(const x of[-6.4,-3.2,0,3.2,6.4])b.block(x,4.4,front+.16,.11,17.15,.64,palette.plaster);
      for(const y of[4.6,7.2,9.6,12,14.4,16.8,19.2,21.45])b.block(0,y,front+.24,16.35,.16,.92);
      b.block(0,3.15,front+1.23,7.4,.28,3.2);b.block(0,3.08,front+1.23,6.95,.06,2.9,palette.timber);
      overheads.push({x:0,z:front+1.23,w:7.4,d:3.2,minY:3.08,h:3.43,cameraOnly:true});
      b.block(0,.02,front-.18,4.4,2.9,.08,palette.glass);for(const x of[-2.2,-.95,0,.95,2.2])b.block(x,.02,front-.07,.065,2.88,.12,palette.metal);
      b.block(0,2.44,front-.07,4.4,.065,.12,palette.metal);b.block(0,.02,front-.07,4.4,.07,.12,palette.stone);
      b.block(0,2.89,front-.05,4.5,.16,.3,palette.ivory);
      for(const x of[-.475,.475])doorLeaf(root,x,.035,front-.13,.91,2.40);
      pull(b,-.13,1.02,front-.015);pull(b,.13,1.02,front-.015);
      for(const x of[-6.6,-6.2,-5.8,-5.4,-5])b.block(x,.3,front+.09,.13,3.15,.28,palette.timber);
      sign(root,b,spec.sign,'RUANG KERJA · TAMAN KOTA',0,3.2,front+2.91,6.8,.44);
      for(const y of[11.95,21.6]){
        b.block(0,y,front+.65,16.6,.2,1.8);overheads.push({x:0,z:front+.65,w:16.6,d:1.8,minY:y,h:y+.6,cameraOnly:true});
        for(const x of[-5.5,5.5]){planter(b,x,y+.2,front+1.1,4.8,.7);for(const dx of[-1.5,-.5,.5,1.5])await vegetation(root,x+dx,y+.6,front+1.1);}
      }
      // The blind party wall becomes a shaded side elevation with a service spine.
      for(const[index,y]of[5.4,7.8,10.2,12.6,15,17.4,19.8].entries()){
        b.block(8.28,y,front-6.4,.07,1.65,8.6,index%3===0?palette.glassLight:palette.glass);
        b.block(8.45,y-.15,front-6.4,.5,.15,9.1);b.block(8.45,y+1.65,front-6.4,.5,.14,9.1);
      }
      for(const z of[front-11,front-7.8,front-4.6,front-1.85])b.block(8.45,5.1,z,.56,16.5,.16);
      for(let y=4.7;y<21.5;y+=.44)b.block(8.4,y,front-12.1,.22,.14,1.3,palette.timber);
      b.block(0,22.25,front-6.4,16.8,.22,13.3);for(const x of[-8,8])b.block(x,22.4,front-6.4,.18,.64,12.9,palette.stone);
      b.block(0,22.4,front-12.9,16,.64,.18,palette.stone);
      for(const x of[-8,8])b.block(x,23.04,front-6.4,.22,.065,12.9,palette.metal);
      b.block(0,23.04,front-12.9,16.1,.065,.22,palette.metal);
      for(const x of[-6,-3,0]){const equipment=await library.instantiate('architecture',{model:'aircon',height:.72,x,y:22.5,z:front-10.5,collidable:false});root.add(equipment);}
      for(let y=22.55;y<23.5;y+=.25)b.block(-3,y,front-8.8,8,.1,.12,palette.metal);
      for(const x of[-6.9,-1.7])b.block(x,22.5,front-3.2,.12,1.25,.12,palette.metal);
      for(let x=-7.1;x<-1.4;x+=.7)b.block(x,23.65,front-3.2,.18,.14,4.4,palette.timber);
    }else if(id==='commercial'){
      b.block(0,0,front+1.35,10.3,.02,3.4,palette.stone);
      b.block(0,2.95,front+1.45,10.9,.25,3.5,palette.ivory);b.block(0,2.88,front+1.45,10.55,.06,3.15,palette.timber);
      for(const x of[-4.8,0,4.8])b.post(x,front+2.8,2.95,palette.stone,.11);
      overheads.push({x:0,z:front+1.45,w:10.9,d:3.5,minY:2.88,h:3.2,cameraOnly:true});
      for(const x of[-2.5,2.5]){b.block(x,.02,front+.22,4.25,2.58,.07,palette.glass);for(const dx of[-2,0,2])b.block(x+dx,.02,front+.32,.065,2.58,.1,palette.metal);b.block(x,2.28,front+.32,4.25,.06,.1,palette.metal);b.block(x,.02,front+.32,4.25,.085,.1,palette.stone);}
      for(const x of[-1.3,1.3]){for(const dx of[-.52,.52])b.block(x+dx,.02,front+.32,.055,2.26,.1,palette.metal);doorLeaf(root,x,.035,front+.263,.98,2.20);pull(b,x+(x<0?.37:-.37),1.0,front+.34);}
      b.block(0,0,front+.04,.62,2.95,.4,palette.ivory);b.block(0,2.6,front+.04,9.4,.28,.4,palette.ivory);
      sign(root,b,spec.sign,'TOKO · STUDIO · RUANG USAHA',0,2.88,front+3.29,9.4,.6);
      for(const y of[4.25,6.75,9.2,12.65])b.block(0,y,front+.26,10.1,.18,.78,palette.ivory);
      for(const x of[-4.8,1.65,4.8])b.block(x,4.25,front+.25,.19,8.45,.78,palette.ivory);
      b.screen(3.1,7.35,front+.65,6,9,palette.roof);
      b.block(-1.5,7.05,front+.65,5.9,.2,1.4,palette.ivory);planter(b,-1.5,7.25,front+1.1,5.45,.55);
      for(const x of[-3.5,-2.5,-1.5,-.5,.5])await vegetation(root,x,7.65,front+1.1);
      for(const x of[-4,-3.5,-3,-2.5,-2,-1.5,-1,-.5,0,.5,1])b.block(x,9.3,front+.55,.12,3.05,.27,palette.timber);
      b.block(0,13.5,front-4.75,10.3,.22,9.6,palette.ivory);
      b.block(0,13.72,front-.02,10.24,.065,.18,palette.metal);for(const x of[-5.04,5.04])b.block(x,13.72,front-4.75,.16,.065,9.4,palette.metal);
      b.block(-2.5,13.72,front-6,3.4,2.35,2.6,palette.sage);b.block(-2.5,16.07,front-6,3.85,.14,3,palette.metal);
      b.block(-2.5,13.82,front-4.65,.85,1.95,.035,palette.dark);
      for(let z=front-8;z<front-2;z+=.85)b.block(3.5,13.84,z,2.15,.1,.14,palette.timber);
      planter(b,2.6,13.72,front-1.2,3.8,.8);for(const x of[1.6,2.6,3.6])await vegetation(root,x,14.12,front-1.2);
    }else{
      b.block(0,0,front+.6,4.3,.02,2.2,palette.stone);
      b.block(-2.12,0,front-3.85,.12,6.15,7.8,palette.sage);b.block(2.12,0,front-3.85,.12,6.15,7.8,palette.sage);
      b.block(0,0,front-7.8,4.3,6.15,.12,palette.sage);
      b.block(0,2.85,front+1.5,5.6,.2,3.35,palette.timber);
      for(const x of[-2.45,2.45])b.post(x,front+2.9,2.85,palette.timber,.095);
      overheads.push({x:0,z:front+1.5,w:5.6,d:3.35,minY:2.82,h:3.32,cameraOnly:true});
      b.block(0,.02,front+.25,3.95,2.48,.08,palette.glass);for(const x of[-1.95,.7,1.95])b.block(x,.02,front+.33,.09,2.48,.14,palette.timber);
      b.block(0,2.22,front+.33,3.95,.07,.14,palette.timber);b.block(0,.02,front+.33,3.95,.075,.14,palette.stone);doorLeaf(root,1.27,.035,front+.296,.98,2.15);pull(b,.92,.99,front+.38);
      b.block(1.8,.02,front+.33,.06,2.2,.14,palette.timber);
      b.block(0,2.5,front+.05,4.05,.24,.4,palette.ivory);
      sign(root,b,spec.sign,'ALAT TULIS · BUKU · KERTAS',0,2.82,front+3.23,4.95,.5);
      for(const x of[-1.75,-1.5,1.5,1.75])b.block(x,4.1,front+.3,.14,1.65,.25,palette.timber);
      b.block(0,5.06,front+.34,2.9,.22,.32,palette.timber);for(const x of[-1.34,1.34])b.block(x,3.65,front+.34,.14,1.42,.32,palette.timber);
      b.block(0,6.15,front-3.5,4.5,.18,8.2,palette.ivory);
      const roofGeometry=new T.BufferGeometry(),v=[],n=[];const half=3.05,eave=6.4,peak=8.05,back=front-8.4,edge=front+.95;
      for(const side of[-1,1]){const p=[[0,peak,back],[side*half,eave,back],[side*half,eave,edge],[0,peak,edge]];for(const index of side>0?[0,2,1,0,3,2]:[0,1,2,0,2,3])v.push(...p[index]);}
      roofGeometry.setAttribute('position',new T.Float32BufferAttribute(v,3));roofGeometry.computeVertexNormals();geometries.add(roofGeometry);const roofMesh=new T.Mesh(roofGeometry,palette.roof);roofMesh.material.side=T.DoubleSide;roofMesh.castShadow=true;roofMesh.receiveShadow=true;roofMesh.userData.projectAuthored=true;root.add(roofMesh);
      b.block(0,8.02,front-3.72,.16,.16,9.5,palette.roof);
      for(const x of[-2.9,2.9])b.block(x,6.27,front-3.72,.13,.14,9.5,palette.timber);
      for(const x of[-3,3])b.block(x,6.3,front-3.72,.09,.14,9.4,palette.timber);
      for(let x=-2.7;x<2.8;x+=.45){const height=peak-Math.abs(x)/half*(peak-eave);b.block(x,6.34,front+.5,.075,Math.max(.1,height-6.34),.12,palette.timber);}
      for(let z=back+.25;z<edge;z+=.5)for(const side of[-1,1])b.block(side*1.52,7.23,z,3.47,.028,.025,palette.roof,{z:-side*Math.atan2(1.65,3.05)});
    }
    const authored=b.commit();root.userData.architecture={id,name:spec.name,source:spec.source,sourceHeight:spec.height,front,details:authored.details,batches:authored.batches,insetDepth:id==='office'?.22:.16,groundClearance:id==='office'?3.08:id==='commercial'?2.88:2.82,fictionalSignage:true};
    root.userData.architecture.entrance={nominalLeafWidth:id==='office'?.95:1,glazedLeafWidth:id==='office'?.91:.98,glazedLeafHeight:id==='office'?2.4:id==='commercial'?2.2:2.15,porchRise:.02,clearanceAbovePorch:root.userData.architecture.groundClearance-.02};
    const sourceBox=new T.Box3().setFromObject(root),body=id==='office'?root.userData.collider:id==='commercial'?{x:0,z:(-5.805536+front+.35)/2,w:9.95212,d:front+.35+5.805536,minY:0,h:13.6}:{x:0,z:front-3.725,w:4.3,d:8.15,minY:0,h:6.35};
    const extent=sourceBox.getSize(new T.Vector3()),center=sourceBox.getCenter(new T.Vector3());
    overheads.push({x:center.x,z:center.z,w:extent.x,d:extent.z,minY:id==='office'?4.4:id==='commercial'?4.25:6.2,h:sourceBox.max.y,cameraOnly:true});
    root.userData.collider=body;root.userData.localColliders=[body,...authored.solids,...overheads];
    root.userData.importedMeshesPreserved=true;return root;
  }
  function collisionBodies(root){
    root.updateMatrixWorld(true);return root.userData.localColliders.map(c=>{
      const b=new T.Box3(new T.Vector3(c.x-c.w/2,c.minY,c.z-c.d/2),new T.Vector3(c.x+c.w/2,c.h,c.z+c.d/2)).applyMatrix4(root.matrixWorld),s=b.getSize(new T.Vector3()),p=b.getCenter(new T.Vector3());
      return {...c,x:p.x,z:p.z,w:s.x,d:s.z,minY:b.min.y,h:b.max.y};
    });
  }
  async function create(id){
    if(!alive)throw Error('Architecture design system has been disposed');
    if(!templates.has(id))templates.set(id,build(id).catch(error=>{templates.delete(id);throw error;}));
    const template=await templates.get(id);if(!alive)throw Error('Architecture design system disposed during construction');return template.clone(true);
  }
  return {create,collisionBodies,finishVegetation,palette,stats:()=>({templates:templates.size,variants:[...templates.keys()]}),dispose(){if(!alive)return;alive=false;geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());templates.clear();}};
}
