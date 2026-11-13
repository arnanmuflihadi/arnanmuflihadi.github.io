import * as T from '../vendor/three-rpg.module.js';
import {district} from './district.js';
export function createWorld() {
  const scene=new T.Scene();scene.background=new T.Color('#d8e2df');scene.fog=new T.Fog('#d8e2df',48,115);
  scene.add(new T.HemisphereLight('#fff6df','#819d93',2.7));
  const sun=new T.DirectionalLight('#fff0d3',3.2);sun.position.set(-25,45,20);sun.castShadow=true;
  sun.shadow.mapSize.set(1024,1024);Object.assign(sun.shadow.camera,{left:-38,right:38,top:38,bottom:-38,near:1,far:95});sun.shadow.bias=-.001;scene.add(sun);
  const materials=new Map(),cube=new T.BoxGeometry(1,1,1),obstacles=[...district.buildings],cameraObjects=[];
  const mat=color=>{if(!materials.has(color))materials.set(color,new T.MeshStandardMaterial({color,roughness:.9}));return materials.get(color);};
  function box(x,y,z,w,h,d,color,solid=false){const mesh=new T.Mesh(cube,mat(color));mesh.position.set(x,y,z);mesh.scale.set(w,h,d);mesh.castShadow=h>.5;mesh.receiveShadow=true;scene.add(mesh);if(solid)cameraObjects.push(mesh);return mesh;}
  box(0,-.35,0,66,.6,66,'#a5b5a3');
  box(0,.015,0,8,.08,62,'#63716d');box(0,.02,0,62,.08,7,'#63716d');
  for(const x of [-5,5])box(x,.12,0,1.8,.24,62,'#e5ddc9');
  for(const z of [-4.6,4.6])box(0,.12,z,62,.24,1.8,'#e5ddc9');
  for(let i=-28;i<=28;i+=4){if(Math.abs(i)>5){box(0,.07,i,.12,.02,1.6,'#efe6c8');box(i,.075,0,1.6,.02,.12,'#efe6c8');}}
  for(let i=-3;i<=3;i++){box(i*.85,.08,5,.45,.025,2,'#f5edda');box(-5,.08,i*.75,2,.025,.35,'#f5edda');}
  function sign(text,x,y,z,width) {
    const canvas=document.createElement('canvas');canvas.width=768;canvas.height=128;
    const c=canvas.getContext('2d');c.fillStyle='#264d48';c.fillRect(0,0,768,128);c.fillStyle='#fff4d9';c.font='600 43px sans-serif';c.textAlign='center';c.textBaseline='middle';c.fillText(text,384,64);
    const texture=new T.CanvasTexture(canvas);texture.colorSpace=T.SRGBColorSpace;
    const mesh=new T.Mesh(new T.PlaneGeometry(width,width/6),new T.MeshBasicMaterial({map:texture}));mesh.position.set(x,y,z);scene.add(mesh);
  }
  district.buildings.forEach((b,i)=>{

    box(b.x,.16,b.z,b.w+1.6,.32,b.d+1.6,'#d8d3c2');
    const color=b.type==='tower'?'#4d7777':b.type==='station'?'#ede3c9':['#cbb998','#e5d7be','#b3b8aa'][i%3];
    box(b.x,b.h/2+.3,b.z,b.w,b.h,b.d,color,true);
    box(b.x,b.h+.45,b.z,b.w+.35,.3,b.d+.35,'#f4e8ce');
    if(b.type==='station') {
      sign('01 / TRANSIT JAKARTA',b.x,2.2,b.z+3.66,9);
      box(b.x,2,b.z+3.57,10,1.3,.13,'#315859');box(b.x,3.5,b.z+4.2,13,.3,2.3,'#b9345e');
      for(const x of [-5,5])box(b.x+x,1.7,b.z+4.6,.16,3.4,.16,'#496c64');
      for(let i=0;i<4;i++)box(b.x, .08+i*.05,b.z+4.8+i*.38,7,.16,.5,'#ede3c9');
    } else {
      if(b.type==='tower')sign('02 / PUSAT USAHA',b.x,1.6,b.z+b.d/2+.08,6);
      for(let y=2;y<b.h;y+=2.1)for(let x=-b.w/2+1;x<b.w/2;x+=1.5)box(b.x+x,y,b.z+b.d/2+.02,.75,.95,.04,b.type==='tower'?'#a4c7bd':'#566e69');
    }
  });
  // Shared geometry + instancing for repeated trees.
  const treePositions=[];
  for(let z=-27;z<30;z+=8)for(const x of [-6.8,6.8])if(Math.abs(z)>7)treePositions.push([x,z]);
  treePositions.push([-20,0],[-20,14],[21,13],[22,-23],[-25,20]);
  const trunks=new T.InstancedMesh(new T.CylinderGeometry(.15,.22,2.4,7),mat('#876c4b'),treePositions.length);
  const crowns=new T.InstancedMesh(new T.SphereGeometry(1.25,8,6),mat('#638d70'),treePositions.length),dummy=new T.Object3D();
  treePositions.forEach(([x,z],i)=>{dummy.position.set(x,1.2,z);dummy.updateMatrix();trunks.setMatrixAt(i,dummy.matrix);dummy.position.y=3.1;dummy.scale.set(1,1.25,1);dummy.updateMatrix();crowns.setMatrixAt(i,dummy.matrix);dummy.scale.set(1,1,1);obstacles.push({x,z,w:.45,d:.45});});
  trunks.castShadow=crowns.castShadow=true;scene.add(trunks,crowns);
  for(const [x,z] of [[-20,13],[21,14],[-20,-18],[19,-26]]){
    box(x,.6,z,2.5,.2,.7,'#937653');box(x,.95,z+.3,2.5,.6,.12,'#937653');
    for(const dx of [-.9,.9])box(x+dx,.3,z,.15,.6,.65,'#456058');
    obstacles.push({x,z,w:2.5,d:.85});
  }
  // District edges are an explicit, continuous visual boundary.
  for(const x of [-32,32])box(x,.5,0,.4,1,64,'#7c927d');
  for(const z of [-32,32])box(0,.5,z,64,1,.4,'#7c927d');
  const markers=district.landmarks.map(l=>{const mesh=new T.Mesh(new T.CylinderGeometry(.4,0,1,5),new T.MeshBasicMaterial({color:'#be365d'}));mesh.position.set(l.focus.x,3.1,l.focus.z);scene.add(mesh);return mesh;});
  scene.updateMatrixWorld(true);
  return {scene,obstacles,cameraObjects,markers,dispose(){const geometries=new Set(),mats=new Set();scene.traverse(o=>{if(o.geometry)geometries.add(o.geometry);if(o.material)mats.add(o.material);if(o.isInstancedMesh)o.dispose();});geometries.forEach(g=>g.dispose());mats.forEach(m=>{m.map?.dispose();m.dispose();});sun.shadow.dispose();}};
}
