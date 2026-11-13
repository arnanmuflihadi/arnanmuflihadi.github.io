// Frontage coordinates, not model centers. All variants retain approved human scale.
export const districtBuildings=Object.freeze([
  {id:'menara',variant:'office',x:23,z:8.5,rotation:0,title:'MENARA TERAS',subtitle:'RUANG KERJA · TAMAN KOTA',display:'lobby'},
  {id:'kopi',variant:'commercial',x:-24,z:-20,rotation:0,title:'KOPI SORE',subtitle:'KOPI · ROTI · TERAS',display:'cafe'},
  {id:'baca',variant:'commercial',x:-12,z:-20,rotation:0,title:'RUANG BACA',subtitle:'BUKU · KERTAS · CERITA',display:'books'},
  {id:'karya',variant:'commercial',x:12,z:-20,rotation:0,title:'KARYA KOTA',subtitle:'STUDIO · GALERI · RUPA',display:'gallery'},
  {id:'pasar',variant:'commercial',x:24,z:-20,rotation:0,title:'PASAR RUPA',subtitle:'KRIYA · TANAMAN · RUMAH',display:'gallery'},
  {id:'jiran',variant:'neighborhood',x:-20,z:21,rotation:Math.PI/2,title:'RUANG JIRAN',subtitle:'ALAT TULIS · BUKU',display:'books'},
  {id:'roti',variant:'neighborhood',x:-20,z:28,rotation:Math.PI/2,title:'ROTI PAGI',subtitle:'ROTI · KOPI',display:'cafe'},
  {id:'kebun',variant:'neighborhood',x:-20,z:35,rotation:Math.PI/2,title:'KEBUN KECIL',subtitle:'TANAMAN · POT',display:'gallery'},
]);
export const skylineBuildings=Object.freeze([
  {id:'sky-west',variant:'office',x:-56,z:-53,rotation:.12},
  {id:'sky-center',variant:'office',x:8,z:-65,rotation:-.16},
  {id:'sky-east',variant:'office',x:54,z:-47,rotation:-.3},
  {id:'sky-east-low',variant:'commercial',x:58,z:-22,rotation:-Math.PI/2},
  ...[-34,-19,-4,11,26].map((z,i)=>({id:'west-streetwall-'+i,variant:'commercial',x:-48,z,rotation:Math.PI/2,backgroundSign:['TERAS NIAGA','RUMAH KARYA','GALERI KOTA'][i%3]})),
  ...[-24,24].map((x,i)=>({id:'north-streetwall-'+i,variant:'commercial',x,z:-46.5,rotation:0,backgroundSign:'TERAS UTARA'})),
  ...[12,34].map((z,i)=>({id:'east-streetwall-'+i,variant:'commercial',x:48,z,rotation:-Math.PI/2,backgroundSign:'RUANG TIMUR'})),
]);
export const variantFront=Object.freeze({office:6.399991,commercial:3.96315,neighborhood:3.96315});
export function buildingTransform(p){const front=variantFront[p.variant];return{x:p.x-Math.sin(p.rotation)*front,y:.24,z:p.z-Math.cos(p.rotation)*front,rotation:p.rotation};}
export const buildingPorches=districtBuildings.map(p=>{const[w,d,offset]=p.variant==='office'?[7.35,3.2,1.1]:p.variant==='commercial'?[10.3,3.4,1.35]:[4.3,2.2,.6],c=Math.abs(Math.cos(p.rotation)),s=Math.abs(Math.sin(p.rotation));return{x:p.x+Math.sin(p.rotation)*offset,z:p.z+Math.cos(p.rotation)*offset,w:c*w+s*d,d:s*w+c*d,height:.26};});

// Approved factory proxy dimensions. Integration tests compare every exported
// shape against real generated GLB instances, including their rotated envelopes.
const proxy=(x,z,w,d,minY,h,cameraOnly=false)=>({x,z,w,d,minY,h,...(cameraOnly?{cameraOnly:true}:{})});
const localProxies={
  office:[proxy(0,0,16.514761803,13.315445418,0,22.4),proxy(0,7.629991,7.4,3.2,3.08,3.43,true),proxy(0,7.049991,16.6,1.8,11.95,12.55,true),proxy(0,7.049991,16.6,1.8,21.6,22.2,true),proxy(.165000096,1.359134146,17.129999429,16.033713709,4.4,23.789999314,true)],
  commercial:[proxy(0,-.746193,9.95212,10.118686,0,13.6),...[-4.8,0,4.8].map(x=>proxy(x,6.76315,.22,.22,0,2.95)),proxy(0,5.41315,10.9,3.5,2.88,3.2,true),proxy(0,.756806865,10.899999619,13.12468627,4.25,16.20999939,true)],
  neighborhood:[proxy(0,.23815,4.3,8.15,0,6.35),...[-2.45,2.45].map(x=>proxy(x,6.86315,.19,.19,0,2.85)),proxy(0,5.46315,5.6,3.35,2.82,3.32,true),proxy(0,1.376149998,6.105338664,11.766000004,6.2,8.18000038,true)],
};
export function buildingObstacles(p){const t=buildingTransform(p),c=Math.cos(p.rotation),s=Math.sin(p.rotation);return localProxies[p.variant].map(o=>({...o,x:t.x+c*o.x+s*o.z,z:t.z-s*o.x+c*o.z,w:Math.abs(c)*o.w+Math.abs(s)*o.d,d:Math.abs(s)*o.w+Math.abs(c)*o.d,minY:o.minY+t.y,h:o.h+t.y,building:p.id}));}

export const parkPond=Object.freeze({x:-31,z:10.8,w:4.2,d:4});
export const serviceCourt=Object.freeze({x:-22.5,z:40.95,w:11,d:5.1});
export const cafeSites=Object.freeze([[-27.5,-19.1],[-20.5,-19.1],[-17.6,31.5]]);
export const benchSites=Object.freeze([[-7,16],[7,16],[-21,10],[-28,14.5],[-34,14.5],[15,13],[32,12],[2,-31.5],[10,34],[17,34]]);
export const lampSites=Object.freeze([[-7,24],[7,24],[-18,12],[13,12],[-4,-7],[4,-7],[-30,-16.4],[-6,-16.4],[6,-16.4],[30,-16.4],[-10.3,21],[-10.3,34],[33,-31.5],[-33,-31.5],[6.25,24],[19.75,33]]);
