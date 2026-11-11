import * as T from'../vendor/three-atlas.module.js?v=16';
import{createBuilder,extrudedPlan,archFrame,gableRoof}from'../urban-atlas/geometry.js?v=22';
import{createArchitectureDesignSystem}from'../urban-atlas/architecture-design-system.js?v=34';
import{modelMetrics}from'../urban-atlas/model-library.js?v=15';
import{createDistrictArtwork}from'../urban-atlas/district-artwork.js?v=40';
import{groundHeight}from'./terrain.js?v=56';
import{settlementBuildings}from'./plan.js?v=56';
const color={stone:'#c9bea0',edge:'#9eaa98',timber:'#75563f',copper:'#73978b',clay:'#ac7154',dark:'#314f4a',grass:'#8eab68',gold:'#c5a468'};
export function petalRoof(width,depth,rise){
 const p=[],c=[],idx=[],nx=24,nz=16,row=nx+1,layer=row*(nz+1);
 for(let side=0;side<2;side++)for(let j=0;j<=nz;j++)for(let i=0;i<=nx;i++){const u=i/nx*2-1,v=j/nz*2-1,x=u*width/2*(.78+.22*(1-v*v)),z=v*depth/2,y=rise*(.8*(1-u*u)+.2*Math.sin(v*Math.PI/2))+.85*Math.pow(Math.abs(v),6)+.3*Math.pow(Math.abs(u),6)-side*.19,co=new T.Color(side?'#ab9974':'#6e978d').multiplyScalar(.94+.07*(u+1)/2);p.push(x,y,z);c.push(co.r,co.g,co.b);}
 for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){const a=j*row+i,b=a+1,d=a+row,e=d+1;idx.push(a,d,b,b,d,e);idx.push(a+layer,b+layer,d+layer,b+layer,e+layer,d+layer);}
 for(let j=0;j<nz;j++)for(const i of[0,nx]){const a=j*row+i,b=a+row;idx.push(a,a+layer,b,a+layer,b+layer,b);}
 for(let i=0;i<nx;i++)for(const j of[0,nz]){const a=j*row+i,b=a+1;idx.push(a,b,a+layer,b,b+layer,a+layer);}
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('color',new T.Float32BufferAttribute(c,3));g.setIndex(idx);g.computeVertexNormals();return g;
}
function hipRoof(w,d,rise){const p=[-w/2,0,-d/2,w/2,0,-d/2,w/2,0,d/2,-w/2,0,d/2,-w*.12,rise,0,w*.12,rise,0],g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setIndex([0,4,1,1,4,5,1,5,2,2,5,3,3,5,4,3,4,0]);g.computeVertexNormals();return g;}
export async function buildSettlement(world,{artwork=createDistrictArtwork(),signal}={}){
 const{scene,library,materials,obstacles}=world,b=createBuilder(scene,materials),system=createArchitectureDesignSystem(library,{signTexture:(a,s)=>artwork.sign(a,s)}),extra=new Set(),authoredGeometry=new Set(),roots=[],stats={buildings:[],landmarks:['Stasiun Antara','Balai Angin'],imported:{},signs:[]};let disposed=false;
 const mat=(hex,options={})=>{const m=new T.MeshStandardMaterial({color:hex,roughness:.92,...options});extra.add(m);return m;},roofMaterial=mat('#ffffff',{vertexColors:true,side:T.DoubleSide,emissive:'#80785d',emissiveIntensity:.08}),glass=system.palette.glass;
 function solid(x,y,z,w,h,d,hex,tag){b.box(x,y,z,w,h,d,hex);if(tag)obstacles.push({x,z,w,d,minY:y-h/2,h:y+h/2,...(tag==='overhead'?{cameraOnly:true}:{building:tag})});}
 function sign(text,sub,x,y,z,w,h,rotation=0){const map=artwork.sign(text,sub,w,h),m=new T.MeshBasicMaterial({map,toneMapped:false});extra.add(m);b.box(x-Math.sin(rotation)*.085,y,z-Math.cos(rotation)*.085,w+.16,h+.16,.11,color.dark,rotation);const face=b.mesh(new T.PlaneGeometry(w,h),m,x,y,z,rotation);face.castShadow=false;face.name='Physical sign: '+text;stats.signs.push({text,position:[x,y,z],rotation,size:[map.image.width,map.image.height],world:[w,h],anisotropy:map.anisotropy,mipmaps:map.generateMipmaps});}
 function foundation(x,z,w,d,y,rotation=0,cut=.6){let low=y;for(const dx of[-w/2,w/2])for(const dz of[-d/2,d/2]){const c=Math.cos(rotation),s=Math.sin(rotation),support=groundHeight(x+dx*c+dz*s,z-dx*s+dz*c);if(support>0)low=Math.min(low,support);}const h=Math.max(.3,Math.min(7,y-low+.24));b.mesh(extrudedPlan(w,d,h,cut),color.edge,x,y-h,z,rotation);}
 function railing(a,c,y){const dx=c[0]-a[0],dz=c[1]-a[1],len=Math.hypot(dx,dz),n=Math.ceil(len/2.4),angle=Math.atan2(dx,dz);for(let i=0;i<=n;i++){const x=a[0]+dx*i/n,z=a[1]+dz*i/n;b.column(x,y+.55,z,.065,1.1,color.dark);}for(const h of[.32,1.08])b.box((a[0]+c[0])/2,y+h,(a[1]+c[1])/2,.09,.08,len,color.dark,angle);obstacles.push({x:(a[0]+c[0])/2,z:(a[1]+c[1])/2,w:Math.max(.12,Math.abs(dx)),d:Math.max(.12,Math.abs(dz)),h:y+1.2});}
 try{
 await library.get('architecture');
 // A gateway and railed landing terrace face the settlement rather than a wall.
 foundation(12,47,18,16,10,0,2);b.mesh(extrudedPlan(18,16,.22,2),color.stone,12,9.795,47);
 const landingRing=b.mesh(new T.TorusGeometry(4.3,.027,5,64),'#a7a182',12,10.035,45.5);landingRing.rotation.x=-Math.PI/2;landingRing.castShadow=false;landingRing.name='Future landing zone / no flight implemented';
 const gateway=b.mesh(archFrame(7.4,8.4,.6,1.2),color.edge,12,10,51.5);gateway.name='Pelabuhan Awan / original gateway';for(const x of[7.7,16.3])obstacles.push({x,z:52.1,w:1.2,d:1.4,h:18.5});obstacles.push({x:12,z:52.1,w:9,d:1.4,minY:16.2,h:19,cameraOnly:true});b.mesh(petalRoof(12,4.5,1.4),roofMaterial,12,18.3,52.1);sign('PELABUHAN AWAN','TRANSIT KINGDOM · ISLAND 01',12,16.45,53,6.4,.75);
 railing([3.5,54.5],[20.5,54.5],10);railing([3.5,47],[3.5,54.5],10);railing([20.5,47],[20.5,54.5],10);
 for(const[x,z]of[[5.6,43.8],[18.4,43.8]]){b.column(x,10.55,z,.55,1.1,color.stone);b.ball(x,11.4,z,.8,.7,.8,color.grass);obstacles.push({x,z,w:1.3,d:1.3,h:12});}
 // Twin sculpted leaf canopies, open arches, an elevated rear platform and beacon.
 foundation(-8,-14,31,25,16,0,1.8);b.mesh(extrudedPlan(31,25,.36,1.8),color.stone,-8,15.655,-14);
 const canopies=[b.mesh(petalRoof(18,24,3.2),roofMaterial,-15,23,-15,-.12),b.mesh(petalRoof(15,24,3.8),roofMaterial,-.5,23.7,-16,.14)];canopies.forEach(m=>m.updateMatrixWorld(true));
 function canopySupport(x,z,hex){const ray=new T.Raycaster(new T.Vector3(x,60,z),new T.Vector3(0,-1,0)),hit=ray.intersectObjects(canopies)[0];if(!hit)throw Error('Station support misses canopy: '+x+','+z);const base=groundHeight(x,z),h=hit.point.y-.2-base;solid(x,base+h/2,z,.32,h,.4,hex,'station-support');}
 for(const x of[-16,.2]){b.mesh(archFrame(9.2,7.2,.28,.45),color.stone,x,16,-5.5);for(const dx of[-4.9,4.9])canopySupport(x+dx,-5.3,color.stone);}
 for(const x of[-21,-11,-4.7,5.1])canopySupport(x,-23,color.timber);
 for(let i=0;i<11;i++){const x=-21+i*2.3,z=-24,y=groundHeight(x,z),root=await library.instantiate('architecture',{model:'glazing',x,y,z,height:3.9,rotation:Math.PI});root.traverse(o=>{if(o.isMesh&&/Glass|FakeInterior/.test(o.material.name))o.material=glass;});scene.add(root);roots.push(root);obstacles.push({...root.userData.collider,building:'station-glazing'});stats.imported.glazing=(stats.imported.glazing||0)+1;}
 for(const x of[-20.5,4.5])solid(x,18.2,-15,.22,4.4,15,color.dark,'station-side');
 for(const x of[-19.4,3.4])solid(x,19.8,-15,.12,.14,15,color.gold);
 sign('STASIUN ANTARA','AKSES KOTA · JAKARTA TRANSIT RESEARCH',-8,20.65,-4.8,11.4,1.05);
 // Original slotted transit beacon; the openings and cap create a distant silhouette.
 for(const dx of[-.85,.85])solid(8+dx,26,-18,.38,20,.7,color.stone,'transit-beacon');for(const y of[18,29,35.5])solid(8,y,-18,2.2,.3,1.1,color.stone,'transit-beacon');b.mesh(archFrame(1.25,3.7,.25,.6),color.stone,8,32,-18.3);b.mesh(hipRoof(4.2,3.4,2.8),color.copper,8,36,-18);sign('01','TRANSIT',8,30,-17.56,1.6,1.8);
 // Three selectively reused buildings form a bent cluster, never a repeated row.
 for(const p of settlementBuildings){const root=await system.create(p.variant),front=3.96315,x=p.front[0]-Math.sin(p.rotation)*front,z=p.front[1]-Math.cos(p.rotation)*front;root.position.set(x,p.y,z);root.rotation.y=p.rotation;root.updateMatrixWorld(true);
  root.traverse(o=>{if(!o.isMesh)return;if(o.material.name==='Project: original architectural lettering'){const gp=o.geometry.parameters,m=new T.MeshBasicMaterial({map:artwork.sign(p.title,p.subtitle,gp.width,gp.height),toneMapped:false});extra.add(m);o.material=m;}if(p.id==='kedai-daun'&&o.material===system.palette.roof){const m=o.material.clone();m.color.set('#879c80');extra.add(m);o.material=m;}});
  const displayMaterial=mat('#ffffff',{map:artwork.display(p.display)}),shelf=mat(color.timber),window=system.palette.glass.clone();window.transparent=true;window.opacity=.38;window.depthWrite=false;extra.add(window);root.traverse(o=>{if(o.isMesh&&o.material===system.palette.glass)o.material=window;});
  const xs=p.variant==='commercial'?[-2.5,2.5]:[0];for(const sx of xs){const plane=new T.Mesh(new T.PlaneGeometry(p.variant==='commercial'?4:3.72,2.05),displayMaterial);authoredGeometry.add(plane.geometry);plane.position.set(sx,1.23,front+.065);root.add(plane);for(const sy of[.78,1.5])for(let j=0;j<5;j++){const book=new T.Mesh(new T.BoxGeometry(.13,.22+j%3*.05,.13),j%2?system.palette.clay:shelf);authoredGeometry.add(book.geometry);book.position.set(sx-.6+j*.24,sy,front+.16);root.add(book);}}
  foundation(x,z,p.variant==='commercial'?11.2:6.4,12.8,p.y,p.rotation);scene.add(root);roots.push(root);const bodies=system.collisionBodies(root);obstacles.push(...bodies.map((c,i)=>({...c,oriented:{w:root.userData.localColliders[i].w,d:root.userData.localColliders[i].d,rotation:p.rotation},building:p.id})));stats.buildings.push({id:p.id,variant:p.variant,position:root.position.toArray(),rotation:p.rotation,metrics:modelMetrics(root),colliders:bodies});stats.imported[p.variant]=(stats.imported[p.variant]||0)+1;
 }
 // Open market timberwork shelters seating without blocking the main path.
 const marketRoof=b.mesh(gableRoof(11,7,2.2),color.clay,15.5,15.3,22);marketRoof.name='Pasar Angin / original open market';for(const x of[10.4,20.6])for(const z of[19,25]){solid(x,13.65,z,.2,3.3,.2,color.timber,'market-post');b.box(x+(x<15?1:-1)*.38,14.86,z,1.05,.09,.12,color.timber,0,x<15?.7:-.7);}for(let z=18.6;z<25.5;z+=.45)for(const side of[-1,1])b.box(15.5+side*2.75,16.42,z,5.92,.025,.025,'#9f7959',0,-side*Math.atan2(2.2,5.5));b.box(15.5,17.54,22,.13,.13,7.2,color.timber);sign('PASAR ANGIN','TERAS · KRIYA · PETA',15.5,14.7,25.7,7.5,.65);
 for(const x of[12.5,17.5]){solid(x,12.85,23.8,3,.12,.7,color.timber,'market-counter');for(let i=0;i<5;i++)b.mesh(new T.CylinderGeometry(.12,.15,.26,8),i%2?color.clay:color.edge,x-1+i*.45,13.04,23.8);}
 // A stepped tropical pavilion crowns the highlands; it is open, not a tower clone.
 foundation(-29,-35,13,12,28,0,1);b.mesh(extrudedPlan(13,12,.3,1),color.stone,-29,27.715,-35);
 for(const x of[-33.6,-24.4])for(const z of[-39,-31])solid(x,30.9,z,.28,5.8,.28,color.timber,'pavilion-post');
 b.mesh(hipRoof(15,13,3.2),color.copper,-29,33.4,-35);b.mesh(hipRoof(9.2,7.5,3),color.clay,-29,36.3,-35);b.mesh(hipRoof(4.3,3.5,2),color.copper,-29,39.05,-35);sign('BALAI ANGIN','BUKIT LESTARI · PANORAMA',-29,32.7,-28.8,7.5,.65);
 for(const[w,d,base,top]of[[7,5,34.7,36.3],[3.2,2.4,37.8,39.05]]){for(const side of[-1,1]){for(let x=-w/2;x<=w/2;x+=.55)b.box(-29+x,(base+top)/2,-35+side*d/2,.07,top-base,.08,color.timber);for(let z=-d/2;z<=d/2;z+=.55)b.box(-29+side*w/2,(base+top)/2,-35+z,.08,top-base,.07,color.timber);b.box(-29,top-.06,-35+side*d/2,w,.12,.12,color.timber);}}
 for(const z of[-38.8,-31.2])for(let x=-32.7;x<=-25.3;x+=.6)solid(x,31.1,z,.06,2.5,.075,color.timber);
 // The overlook has a visible balustrade and a clear approach from both routes.
 foundation(-51,-2,13,11,22,0,1.2);b.mesh(extrudedPlan(13,11,.25,1.2),color.stone,-51,21.765,-2);railing([-57,-7],[-57,3],22);railing([-57,3],[-49,3],22);railing([-57,-7],[-53,-7],22);sign('TERAS LANGIT','LIHAT KOTA · BACA BUKTI',-53.2,23.15,2.8,4.7,.55);
 // Path furnishings define rests and route choices, rather than random scatter.
 for(const[x,z]of[[8,39],[15,30],[-15,5],[-31,-18],[-45,-24],[-47,1]]){const y=groundHeight(x,z);solid(x,y+.46,z,2.2,.1,.65,color.timber,'bench');solid(x,y+.8,z+.3,2.2,.55,.07,color.timber);for(const dx of[-.8,.8])solid(x+dx,y+.23,z,.09,.46,.5,color.dark);}
 for(const[x,z,title,sub]of[[9,36,'STASIUN ANTARA','VIA PASAR ANGIN'],[-18,7,'BUKIT LESTARI','BALAI ANGIN · TERAS LANGIT'],[26,18,'PASAR ANGIN','KEDAI · PUSTAKA']]){const y=groundHeight(x,z);solid(x,y+1.25,z,.12,2.5,.12,color.timber,'wayfinding');sign(title,sub,x,y+2,z+.08,3.4,.52);}
 for(const[x,z]of[[8,32],[29,16],[-18,-1],[-26,-4],[-33,-14],[-44,-23]]){const y=groundHeight(x,z);b.column(x,y+1.1,z,.055,2.2,color.dark);b.mesh(gableRoof(.65,.65,.25),color.copper,x,y+2.2,z);b.box(x,y+2.02,z,.25,.3,.25,'#e6c787');obstacles.push({x,z,w:.24,d:.24,h:y+2.5});}
 b.flush();scene.updateMatrixWorld(true);stats.prototypes=system.stats().templates;stats.metrics=modelMetrics(scene);if(signal?.aborted)throw Error('Settlement cancelled');
 return{stats,dispose(){if(disposed)return;disposed=true;roots.forEach(r=>r.removeFromParent());system.dispose();extra.forEach(m=>m.dispose());authoredGeometry.forEach(g=>g.dispose());b.owned.forEach(g=>g.dispose());}};
 }catch(error){roots.forEach(r=>r.removeFromParent());system.dispose();extra.forEach(m=>m.dispose());authoredGeometry.forEach(g=>g.dispose());b.owned.forEach(g=>g.dispose());throw error;}
}
