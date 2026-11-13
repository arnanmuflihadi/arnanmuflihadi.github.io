import * as T from '../vendor/three-atlas.module.js?v=16';
import{treeSites,palmSites,planterSites,streets,groundHeight,curbRamps,inRoad}from'./layout.js?v=40';
import{palette as P}from'./materials.js?v=22';
import{leafRibbon,accessRamp}from'./geometry.js?v=22';
import{createDistrictPaving}from'./district-ground.js?v=40';
import{parkPond,serviceCourt,cafeSites,benchSites,lampSites}from'./district-plan.js?v=40';
export function buildEnvironment(scene,b,materials,obstacles){
  const animated=[];
  const skyMaterial=new T.ShaderMaterial({side:T.BackSide,depthWrite:false,toneMapped:false,vertexShader:'varying vec3 direction; void main(){direction=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',fragmentShader:'varying vec3 direction; void main(){float h=pow(max(normalize(direction).y,0.0),.45); vec3 col=mix(vec3(.80,.86,.80),vec3(.24,.47,.64),h); gl_FragColor=vec4(col,1.0); #include <colorspace_fragment> }'.replace('#include <colorspace_fragment>','\n#include <colorspace_fragment>\n')});
  const sky=new T.Mesh(new T.SphereGeometry(260,32,20),skyMaterial);scene.add(sky);
  const cloudGeometry=new T.SphereGeometry(1,12,8),cloudMaterial=new T.MeshBasicMaterial({color:'#f5efe0',fog:false}),clouds=new T.Group();
  for(const[cx,cy,cz,size]of[[-90,47,-135,1.3],[30,53,-155,1.7],[117,44,-123,1.1]])for(let i=0;i<6;i++){const m=new T.Mesh(cloudGeometry,cloudMaterial);m.position.set(cx+(i-2.5)*7*size,cy+Math.sin(i*1.4)*3,cz);m.scale.set((8+i%3)*size,3.5*size,5*size);clouds.add(m);}scene.add(clouds);
  b.box(0,-.42,0,220,.8,220,'#8b9e79');
  for(const r of streets)b.box(r.x,.015,r.z,r.w,.08,r.d,'#697773');
  b.box(serviceCourt.x,.02,serviceCourt.z,serviceCourt.w,.08,serviceCourt.d,'#aeb8a0');
  const paving=createDistrictPaving(),colors=[],p=paving.attributes.position;
  for(let i=0;i<p.count;i++){const x=p.getX(i),z=p.getZ(i),tone=z<-14?'#c8cdbf':x<-8&&z>16?'#d0c3a8':'#d8ceba',c=new T.Color(tone).multiplyScalar(.97+Math.sin(x*.31+z*.19)*.018);colors.push(c.r,c.g,c.b);}paving.setAttribute('color',new T.Float32BufferAttribute(colors,3));
  const pavingMaterial=new T.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.96});const pavingMesh=b.mesh(paving,pavingMaterial);pavingMesh.name='Shared union paving and collision supports';pavingMesh.castShadow=false;
  for(const r of curbRamps)b.mesh(accessRamp(r.axis==='x'?r.d:r.w,r.axis==='x'?r.w:r.d,r.rise),P.stone,r.axis==='x'?r.front:r.x,r.base,r.axis==='x'?r.z:r.front,r.rotation).castShadow=false;
  // Joints occupy only surveyed paving cells, rather than a sheet over the road.
  for(let x=-34.5;x<35;x+=3)for(let z=-41;z<40;z+=1.5){if([[-.65,0],[.65,0],[0,-.1],[0,.1]].every(([dx,dz])=>groundHeight(x+dx,z+dz)===.24)&&!inRoad(x,z))b.box(x,.244,z,1.35,.006,.012,'#b3b5a6');}
  for(const z of[-12,-36]){for(let x=-34;x<35;x+=4.5)if(Math.abs(x)>5)b.box(x,.062,z,1.8,.012,.09,'#dce0ce');for(const x of[-2.1,-1.05,0,1.05,2.1])b.box(x,.063,z,.55,.016,5.3,'#f0ead7');}
  for(const x of[-40,40])for(let z=-41;z<43;z+=4.5)if(![-12,-36].some(c=>Math.abs(z-c)<5))b.box(x,.062,z,.09,.012,1.8,'#dce0ce');
  for(const z of[27.1,27.7,28.3,28.9])b.box(-14,.063,z,3.9,.016,.34,'#f0ead7');
  for(const r of curbRamps)for(let t=-(r.axis==='x'?1.1:2.1);t<=(r.axis==='x'?1.1:2.1);t+=.6){const x=r.axis==='x'?r.front+(r.rotation>0?-1:1)*1.3:t,z=r.axis==='x'?r.z+t:r.front+(r.rotation===0?-1:1)*1.3;b.box(x,groundHeight(x,z)+.012,z,.32,.024,.25,'#c6a25b');}
  // A civic water basin anchors arrival while its perimeter stays walkable.
  b.mesh(new T.CylinderGeometry(2.9,3.2,.52,48),P.ivory,0,.54,10);b.mesh(new T.CylinderGeometry(2.62,2.62,.04,48),'#679b92',0,.78,10);
  b.column(0,1.5,10,.26,1.4,P.terra);for(let i=0;i<5;i++){const a=i/5*Math.PI*2,m=b.mesh(new T.SphereGeometry(1,12,8),i%2?P.terra:P.ivory,Math.sin(a)*.5,2.25,10+Math.cos(a)*.5);m.scale.set(.16,.9,.45);m.rotation.set(.4,a,.3);}obstacles.push({x:0,z:10,w:5.9,d:5.9,h:3});
  const pond=b.mesh(new T.PlaneGeometry(parkPond.w,parkPond.d),'#5e8e84',parkPond.x,.035,parkPond.z);pond.rotation.x=-Math.PI/2;pond.castShadow=false;
  for(const s of[-1,1]){b.box(parkPond.x+s*(parkPond.w/2+.1),.33,parkPond.z,.2,.18,parkPond.d+.4,P.stone);b.box(parkPond.x,.33,parkPond.z+s*(parkPond.d/2+.1),parkPond.w,.18,.2,P.stone);}obstacles.push({...parkPond,w:parkPond.w+.4,d:parkPond.d+.4,h:.5});
  for(const[x,z,s]of treeSites){const y=groundHeight(x,z);obstacles.push({x,z,w:1.05*s,d:1.05*s,minY:y,h:y+6.8*s,tree:true});b.mesh(new T.CylinderGeometry(.85*s,.92*s,.08,20),'#617950',x,y+.015,z);const rim=b.mesh(new T.TorusGeometry(.93*s,.045,5,24),P.stone,x,y+.045,z);rim.rotation.x=Math.PI/2;}
  const frond=leafRibbon(4.5);b.owned.add(frond);
  for(const[x,z,height]of palmSites){const floor=groundHeight(x,z);b.column(x,floor+height/2,z,.22,height,P.timber);const crown=new T.Group();crown.position.set(x,floor+height,z);scene.add(crown);for(let i=0;i<9;i++){const m=new T.Mesh(frond,materials.toon(i%3?P.leaf:P.leafLight,{side:T.DoubleSide}));m.rotation.y=i/9*Math.PI*2;m.rotation.x=-.1+(i%2)*.12;m.castShadow=true;crown.add(m);}animated.push({object:crown,phase:x*.4+z*.2});obstacles.push({x,z,w:.6,d:.6,h:floor+height});}
  for(const[x,z]of planterSites)obstacles.push({x,z,w:2.5,d:2.5,h:groundHeight(x,z)+.75,planter:true});
  // Low planted pockets sit outside the movement spine and station ramp.
  for(const[x,z,w,d]of[[-6,1,2,3],[6,1,2,3],[-33.5,15,2,2],[-26,14.5,1.8,2],[-7,19,2,2],[16,17,2,3]]){const floor=groundHeight(x,z);b.box(x,floor+.18,z,w,.36,d,P.stone);b.box(x,floor+.37,z,w-.15,.03,d-.15,'#627950');obstacles.push({x,z,w,d,h:floor+.65});for(let i=0;i<5;i++)b.ball(x+Math.sin(i*2.4)*w*.3,floor+.55,z+Math.cos(i*2.4)*d*.3,.35,.2,.35,i%2?P.leaf:P.leafLight);}
  function bench(x,z){const y=groundHeight(x,z);for(let i=0;i<4;i++)b.box(x,y+.44,z+(i-1.5)*.12,2.4,.09,.1,P.timber);b.box(x,y+.8,z+.3,2.4,.55,.085,P.timber);for(const dx of[-.85,.85])b.box(x+dx,y+.2,z,.11,.4,.55,P.dark);obstacles.push({x,z,w:2.5,d:.85,h:y+1.1});}
  for(const point of benchSites)bench(...point);
  for(const[x,z]of lampSites){const y=groundHeight(x,z);b.column(x,y+2.35,z,.055,4.7,P.dark);b.box(x+.35,y+4.65,z,.75,.09,.25,P.dark);b.ball(x+.58,y+4.58,z,.16,.06,.14,'#f4dfab');obstacles.push({x,z,w:.18,d:.18,h:y+4.8});}
  // Café furnishings stay in frontage pockets; no commerce mechanic is added.
  for(const[x,z]of cafeSites){const y=groundHeight(x,z);b.mesh(new T.CylinderGeometry(.48,.48,.07,16),P.timber,x,y+.76,z);b.column(x,y+.38,z,.065,.72,P.dark);for(const dx of[-.75,.75]){b.box(x+dx,y+.43,z,.44,.07,.46,P.timber);b.box(x+dx,y+.7,z+.22,.44,.5,.05,P.timber);for(const lx of[-.16,.16])for(const lz of[-.16,.16])b.box(x+dx+lx,y+.21,z+lz,.045,.42,.045,P.dark);obstacles.push({x:x+dx,z,w:.5,d:.55,h:y+1});}obstacles.push({x,z,w:1,d:1,h:y+.85});}
  for(const x of[-33,-31,-29]){const z=7,y=groundHeight(x,z);b.mesh(new T.TorusGeometry(.42,.04,6,16,Math.PI),P.dark,x,y+.04,z);obstacles.push({x,z,w:.95,d:.22,h:y+.9});}
  const bikeX=-29.9,bikeZ=7.25,bikeY=groundHeight(bikeX,bikeZ);
  for(const dx of[-.5,.5])b.mesh(new T.TorusGeometry(.33,.035,6,20),P.dark,bikeX+dx,bikeY+.35,bikeZ);
  const framePoints=[[-.5,.35],[-.18,.78],[.1,.38],[.5,.35],[.22,.85]];
  for(const[a,c]of[[0,1],[1,2],[2,0],[2,4],[4,3],[1,4]]){const p=framePoints[a],q=framePoints[c],dx=q[0]-p[0],dy=q[1]-p[1];b.box(bikeX+(p[0]+q[0])/2,bikeY+(p[1]+q[1])/2,bikeZ,Math.hypot(dx,dy),.045,.045,'#69847b',0,Math.atan2(dy,dx));}
  b.box(bikeX-.18,bikeY+.83,bikeZ,.28,.06,.15,P.timber);b.box(bikeX+.25,bikeY+.98,bikeZ,.08,.045,.4,P.dark);obstacles.push({x:bikeX,z:bikeZ,w:1.75,d:.45,h:bikeY+1.05});
  for(const[x,z]of[[-8,16],[-33,20],[32,12],[-5,-31.5]]){const y=groundHeight(x,z);b.mesh(new T.CylinderGeometry(.25,.28,.75,10),'#536b60',x,y+.375,z);b.mesh(new T.CylinderGeometry(.3,.3,.07,10),P.dark,x,y+.76,z);obstacles.push({x,z,w:.6,d:.6,h:y+.82});}
  // Low planted district edges guide the player before the collision boundary.
  for(const x of[-44,44])b.box(x,.45,0,.45,.9,88,'#6b855d');for(const z of[-44,44])b.box(0,.45,z,88,.9,.45,'#6b855d');
  return{sky,skyMaterial,clouds,animated,update(time,reduced){if(reduced)return;for(const item of animated)item.object.rotation.z=Math.sin(time*.4+item.phase)*.012;clouds.position.x=Math.sin(time*.008)*2;}};
}
