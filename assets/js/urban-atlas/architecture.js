import * as T from '../vendor/three-atlas.module.js?v=16';
import{palette as P}from'./materials.js?v=22';
import{extrudedPlan,shellRoof,gableRoof,accessRamp}from'./geometry.js?v=22';
import{districtBuildings,skylineBuildings,buildingObstacles}from'./district-plan.js?v=40';
import{createDistrictArtwork}from'./district-artwork.js?v=40';
export function buildArchitecture(scene,b,materials,obstacles){
  const artwork=createDistrictArtwork(),signs=[];
  function sign(title,sub,x,y,z,width,height=.65,rotation=0){const map=artwork.sign(title,sub,width,height),material=new T.MeshBasicMaterial({map,toneMapped:false});const mesh=b.mesh(new T.PlaneGeometry(width,height),material,x,y,z,rotation);mesh.castShadow=false;signs.push({map,material});return mesh;}
  for(const p of[...districtBuildings,...skylineBuildings])obstacles.push(...buildingObstacles(p));
  for(const p of[...districtBuildings,...skylineBuildings]){const c=buildingObstacles(p)[0];b.box(c.x,.11,c.z,c.w,.26,c.d,P.stone);}
  // Original vaulted transit hall, with imported entrance/glazing modules loaded separately.
  b.mesh(extrudedPlan(25,12,.54,1.4),P.stone,-23,-.02,-1);
  b.mesh(accessRamp(8,2,.28),P.stone,-23,.24,7);
  obstacles.push({x:-23,z:-3,w:21,d:5.5,minY:.52,h:4.7,building:'station'});
  for(const z of[-4.5,2]){
    b.mesh(shellRoof(29,5.6,2.1),P.ivory,-23,5.2,z).receiveShadow=false;
    b.mesh(shellRoof(29.15,.22,2.1),P.terra,-23,5.17,z+2.85).receiveShadow=false;
    obstacles.push({x:-23,z,w:29,d:5.6,minY:5,h:7.5,cameraOnly:true});
    for(const x of[-34,-28.5,-17.5,-12]){b.column(x,2.9,z+1.6,.14,5.3,P.timber);obstacles.push({x,z:z+1.6,w:.35,d:.35,h:5.6});}
    for(let x=-35;x<=-11;x+=1.2)b.box(x,5.22+2.1*(1-((x+23)/14.5)**2),z,.06,.12,5.1,'#b4a78d');
  }
  b.box(-23,4.65,4.75,19,.3,.6,P.dark);b.box(-23,4.07,5.01,9.16,.85,.12,P.dark);sign('STASIUN TAMAN','MRT · JALUR KOTA',-23,4.07,5.08,9,.7);
  for(const x of[-25.35,-20.65])b.box(x,2.25,.05,.2,3.46,.32,P.ivory);b.box(-23,3.95,.05,4.9,.28,.4,P.ivory);sign('MASUK','',-23,3.55,.28,3,.35);
  for(const x of[-29,-17]){b.box(x,1.15,5.6,.45,1.25,.45,P.dark);b.box(x,1.7,5.86,.28,.16,.04,P.glassLight);obstacles.push({x,z:5.6,w:.5,d:.5,h:1.8});}
  for(let x=-34;x<=-12;x+=.7)b.box(x,.533,4.7,.36,.025,.32,'#d2ad61');
  b.column(-32,1.8,8,.08,3.1,P.dark);sign('M','TAMAN',-32,2.7,8.1,1.05,1.4);obstacles.push({x:-32,z:8,w:.2,d:.2,h:3.5});
  // A local transit shelter faces the promenade, clear of the through footway.
  b.box(-11.1,3.15,13.2,4.6,.2,2.1,P.terra);for(const x of[-13.2,-9]){b.column(x,1.65,13.9,.07,2.85,P.dark);obstacles.push({x,z:13.9,w:.2,d:.2,h:3.3});}
  obstacles.push({x:-11.1,z:14,w:4.4,d:.25,h:2.8},{x:-11.1,z:13.2,w:4.6,d:2.1,minY:3,h:3.4,cameraOnly:true});sign('HALTE TAMAN','PROMENADE',-11.1,2.9,14.28,3.5,.4);
  // Public research pavilion: a lightweight authored roof above imported panels.
  b.mesh(extrudedPlan(14,11,.33,.9),P.stone,29,.24,21);
  b.mesh(accessRamp(5,3,.33),P.stone,29,.24,12.5,Math.PI);
  b.mesh(gableRoof(16,13,3.3),P.terra,29,4.6,21).receiveShadow=false;
  b.mesh(gableRoof(13.5,10,2.6),P.ivory,29,4.45,21).receiveShadow=false;
  obstacles.push({x:29,z:21,w:16,d:13,minY:4.4,h:8,cameraOnly:true},{x:29,z:24.8,w:12,d:.4,h:4.2});
  for(const x of[23.5,34.5])for(const z of[17,21,25]){b.column(x,2.75,z,.15,4.8,P.timber);obstacles.push({x,z,w:.35,d:.35,h:5.2});}
  sign('BALE KOTA','ATLAS · RUANG PUBLIK',29,3.7,16.55,6,.6,Math.PI);
  sign('TAMAN ATLAS','STASIUN · KOTA · RUANG JIRAN',0,2.9,-5.6,4.5,.5);
  b.column(-2.6,1.7,-5.6,.065,3,P.dark);obstacles.push({x:-2.6,z:-5.6,w:.18,d:.18,h:3.3});
  b.box(10,1.65,20.65,3.2,.55,.12,P.dark);for(const[rotation,z]of[[0,20.72],[Math.PI,20.58]])sign('TAMAN TEDUH','RUANG HIJAU · TAMAN KOTA',10,1.65,z,3.1,.45,rotation);for(const x of[8.6,11.4])b.column(x,.93,20.65,.045,1.4,P.dark);obstacles.push({x:10,z:20.65,w:3.2,d:.15,h:1.95});
  return{signs,dispose:()=>artwork.dispose()};
}
