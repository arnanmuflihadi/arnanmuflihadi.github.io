export const worldId='transit-kingdom-r0';
export const spawn=Object.freeze({x:12,z:47});
export const outlineControls=[[-4,-73],[12,-69],[23,-57],[43,-52],[51,-35],[61,-24],[57,-6],[66,10],[57,27],[49,37],[49,50],[32,55],[22,69],[5,65],[-7,58],[-25,62],[-38,50],[-43,34],[-59,28],[-62,11],[-56,-1],[-65,-18],[-57,-33],[-42,-40],[-37,-58],[-20,-63]];
export const areas=Object.freeze({
 arrival:{x:12,z:47,y:10,rx:13,rz:12,name:'Pelabuhan Awan'},
 merchant:{x:24,z:18,y:12,rx:18,rz:16,name:'Pasar Angin'},
 transit:{x:-8,z:-10,y:16,rx:18,rz:17,name:'Stasiun Antara'},
 highlands:{x:-32,z:-32,y:28,rx:10,rz:10,name:'Bukit Lestari'},
 overlook:{x:-49,z:-2,y:22,rx:8,rz:7,name:'Teras Langit'},
});
export const routes=Object.freeze([
 {id:'arrival',width:4.6,points:[[12,47,10],[14,38,10],[15,36,10.5],[21,28,11.5],[24,18,12]]},
 {id:'city',width:5.4,points:[[24,18,12],[10,18,12],[2,8,14],[-8,3,16],[-8,-10,16]]},
 {id:'highlands',width:3.3,points:[[-8,3,16],[-21,3,17],[-30,-9,21],[-35,-20,25],[-33,-28,28],[-32,-32,28]]},
 {id:'overlook',width:3.1,points:[[-32,-32,28],[-32,-28,28],[-39,-26,27.3],[-44,-26,26],[-51,-15,23],[-50,-8.5,22],[-49,-2,22]]},
 {id:'return',width:3.4,points:[[-49,-2,22],[-43,2,22],[-38,6,19],[-21,3,17]]},
 {id:'market-east',width:3.2,points:[[24,18,12],[32,20,12],[35,22,12]]},
 {id:'market-north',width:3.2,points:[[24,18,12],[27.5,11,12],[28,8.5,12],[27.4,7.8,12]]},
 {id:'market-south',width:3.2,points:[[24,18,12],[22,23,12],[24,34,12],[31,33,12]]},
]);
export const settlementBuildings=[
 {id:'rumah-karya',variant:'commercial',front:[27,6],rotation:-.6,y:12,title:'RUMAH KARYA',subtitle:'KRIYA · KOPI · TERAS',display:'gallery'},
 {id:'kedai-daun',variant:'neighborhood',front:[36,22],rotation:-Math.PI/2,y:12,title:'KEDAI DAUN',subtitle:'TEH · ROTI · TANAMAN',display:'cafe'},
 {id:'pustaka-angin',variant:'neighborhood',front:[30,31],rotation:-.8,y:12,title:'PUSTAKA ANGIN',subtitle:'BUKU · PETA · CERITA',display:'books'},
];
export const pads=[{x:12,z:47,w:18,d:16,y:10,rotation:0},{x:-8,z:-14,w:31,d:25,y:16,rotation:0},{x:-8,z:-23,w:25,d:10,y:17.2,rotation:0},{x:-29,z:-35,w:13,d:12,y:28,rotation:0},{x:-51,z:-2,w:14,d:11,y:22,rotation:0},...settlementBuildings.map(p=>({x:p.front[0]-Math.sin(p.rotation)*4,z:p.front[1]-Math.cos(p.rotation)*4,w:p.variant==='commercial'?12.4:7,d:13.5,y:p.y,rotation:p.rotation}))];
export const realmSpecs=Object.freeze([
 {id:'transit',name:'Transit Kingdom',constructed:true,arrival:spawn,landing:[12,10,47]},
 {id:'cbd',name:'Merchant Citadel',constructed:false},
 {id:'mbr',name:'Mosaic District',constructed:false},
 {id:'bandung-cafe',name:'Bandung Highlands',constructed:false},
 {id:'pangan',name:'Harvest Valley',constructed:false},
 {id:'alphaearth-food',name:'Terra Observatory',constructed:false},
]);
export const isConstructed=id=>realmSpecs.some(r=>r.id===id&&r.constructed);
export const travelConfig=Object.freeze({state:'explore',implemented:false,worldId,skyport:{spawn,takeoff:{x:12,y:10.015,z:45.5,radius:4.3},landing:{x:12,y:10.015,z:45.5,radius:4.3}},airspace:{minY:-90,maxY:240,radius:800},futureSequence:['explore','mount','takeoff','fly','load-destination','land','explore'],routes:realmSpecs.filter(r=>!r.constructed).map(r=>({destination:r.id,enabled:false}))});
export const treeSites=[[-5,46,7],[22,43,8],[29,38,6.7],[0,34,8],[-9,30,8.5],[6,24,7],[-10,19,8],[-20,17,9],[-28,17,7.2],[-37,15,7],[-43,23,6.5],[-38,34,7.5],[40,31,8],[43,19,7.5],[39,8,7],[31,-8,7],[-23,-8,7],[-24,-19,6.5],[-22,-30,7],[-29,-45,6],[-40,-43,6.7],[-46,-32,7],[-56,-23,5],[-57,5,5.8],[-18,-47,6.8],[-3,-38,7],[14,-30,8],[30,-27,7.5],[8,-54,7.2],[22,-48,6],[-7,57,6.8],[-28,48,7]];
export const streamPoints=[[-24,20,12],[-32,24,11],[-40,24,10],[-48,29,8.5],[-57,27,7.6]];
export const reviewViews={
 aerial:{position:[110,82,135],target:[0,-3,0],player:[12,47],fov:43,label:'Transit Kingdom / Full island'},
 underside:{position:[-113,-13,132],target:[-2,-9,2],player:[12,47],fov:49,label:'Geology / Floating underside'},
 arrival:{position:[27,21,61],target:[-7,18,-5],player:[12,47],fov:55,label:'Arrival / Pelabuhan Awan'},
 station:{position:[10,23,14],target:[-8,22,-12],player:[-8,3],fov:53,label:'Transit / Stasiun Antara'},
 merchant:{position:[22,16,38],target:[31,16,17],player:[24,25],fov:58,label:'Merchant quarter / Pasar Angin'},
 route:{position:[-14,25,12],target:[-31,28,-18],player:[-21,3],fov:55,label:'Highland path'},
 overlook:{position:[-62,32,13],target:[0,13,12],player:[-49,-2],fov:57,label:'Overlook / Teras Langit'},
 exploration:{position:[17,17,44],target:[13,13,29],player:[15,36],fov:60,label:'Third-person exploration'},
 terrain:{position:[125,83,155],target:[-4,-6,0],player:[12,47],fov:49,label:'R0-B / Terrain before settlement'},
};
