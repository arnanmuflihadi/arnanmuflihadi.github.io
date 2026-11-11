export const worldId='transit-landscape-r0a';
export const spawn=Object.freeze({x:27,z:57});
export const outlineControls=[[0,-94],[21,-83],[30,-61],[58,-63],[68,-37],[60,-18],[83,-6],[74,15],[87,37],[65,47],[51,73],[34,83],[14,79],[-2,89],[-20,76],[-34,54],[-56,55],[-72,38],[-65,22],[-90,6],[-82,-14],[-68,-27],[-73,-49],[-47,-58],[-36,-81],[-18,-87]];
export const areas=Object.freeze({
 arrival:{x:27,z:57,y:16,rx:10,rz:10,name:'Arrival meadow'},
 merchant:{x:32,z:12,y:22,rx:12,rz:11,name:'Eastern clearing'},
 transit:{x:-5,z:5,y:21,rx:10,rz:9,name:'Valley clearing'},
 highlands:{x:-45,z:-49,y:49,rx:6,rz:7,name:'Crown ridge'},
 overlook:{x:-80,z:5,y:32,rx:7,rz:6,name:'Cloudbreak overlook'},
});
const trail=(id,width,points)=>({id,width,points});
export const routes=Object.freeze([
 trail('arrival',3.1,[[27,57,16],[26,49,16.8],[22,42,17.6],[16,36,18],[12,29,18.5],[11,22,19],[6,15,20],[-5,5,21]]),
 trail('ridge',2.6,[[-5,5,21],[-20,8,24],[-32,-3,28],[-39,-14,32],[-28,-22,36],[-35,-32,41],[-38,-41,46],[-45,-49,49]]),
 trail('overlook',2.5,[[-45,-49,49],[-53,-39,46],[-58,-30,41],[-62,-15,36],[-67,-4,33],[-75,0,32.4],[-80,5,32]]),
 trail('return',2.8,[[-80,5,32],[-71,11,31],[-57,8,30],[-46,15,27],[-31,19,24],[-17,17,22],[-5,5,21]]),
 trail('clearing',3.0,[[-5,5,21],[3,12,20.5],[18,12,20.5],[32,12,22]]),
 trail('meadow',2.6,[[32,12,22],[40,24,21],[39,36,19],[32,44,17.5],[26,49,16.8]]),
]);
export const settlementBuildings=[];
export const pads=[];
export const reservations=Object.freeze({
 skyport:{x:27,z:57,y:16,radius:9,constructed:false},
 station:{x:-5,z:5,y:21,radius:8,constructed:false},
 settlement:{x:32,z:12,y:22,radius:11,constructed:false},
 overlook:{x:-80,z:5,y:32,radius:5,constructed:false,natural:true},
 dragon:{x:27,z:57,y:16,radius:6.5,constructed:false},
});
export const realmSpecs=Object.freeze([
 {id:'transit',name:'Transit Kingdom',constructed:false,landscapeAvailable:true},
 {id:'cbd',name:'Merchant Citadel',constructed:false},
 {id:'mbr',name:'Mosaic District',constructed:false},
 {id:'bandung-cafe',name:'Bandung Highlands',constructed:false},
 {id:'pangan',name:'Harvest Valley',constructed:false},
 {id:'alphaearth-food',name:'Terra Observatory',constructed:false},
]);
export const isConstructed=id=>realmSpecs.some(r=>r.id===id&&r.constructed);
export const travelConfig=Object.freeze({state:'explore',implemented:false,worldId,skyport:{spawn,takeoff:{...reservations.dragon},landing:{...reservations.dragon}},airspace:{minY:-120,maxY:260,radius:800},routes:realmSpecs.filter(r=>r.id!=='transit').map(r=>({destination:r.id,enabled:false}))});
export const treeGroves=[[-19,46,14,18],[-39,40,13,17],[-55,21,9,10],[-15,31,9,10],[12,55,11,12],[46,48,12,13],[55,28,12,14],[51,2,12,13],[31,-21,15,17],[6,-34,12,13],[-13,-57,11,10],[-53,-60,8,7],[-67,-37,7,6]];
export const streamPoints=[[-22,25,23],[-34,28,21],[-46,33,18],[-58,37,14],[-68,35,11],[-72,38,10.5]];
export const reviewViews={
 waterfall:{position:[-115,32,79],target:[-73,-18,38],player:[-80,5],fov:55,label:'Cloudbreak waterfall / Fixed close-up'},
 editorial:{position:[108,76,136],target:[-7,10,-4],player:[27,57],fov:48,label:'Editorial fixed-camera comparison'},
 forest:{position:[24,22,45],target:[4,25,0],player:[21,40],fov:60,label:'Forest trail'},
 ridge:{position:[-51,53,-30],target:[-35,44,-53],player:[-38,-41],fov:55,label:'Crown ridge'},
 aerial:{position:[135,105,175],target:[-2,-8,0],player:[27,57],fov:43,label:'R0-A / Full floating landscape'},
 comparison:{position:[110,82,135],target:[0,-3,0],player:[27,57],fov:43,label:'R0-A / Matched pre-correction camera'},
 side:{position:[-145,5,155],target:[-4,-15,0],player:[27,57],fov:53,label:'Layered geology / Side profile'},
 cliff:{position:[-104,-15,57],target:[-58,12,16],player:[-80,5],fov:57,label:'Low-angle cloudbreak cliffs'},
 spawn:{position:[29,19.2,65],target:[1,27,-17],player:[27,57],fov:60,label:'Third-person arrival meadow'},
 route:{position:[-26,34,9],target:[-29,29,-.25],player:[-29,-.25],fov:60,label:'Ridge switchback / Walking trail'},
 overlook:{position:[-96,48,23],target:[-25,15,23],player:[-80,5],fov:60,label:'Cloudbreak overlook'},
 exploration:{position:[24,22,45],target:[4,25,0],player:[21,40],fov:60,label:'Third-person valley trail'},
 underside:{position:[-145,5,155],target:[-4,-15,0],player:[27,57],fov:53,label:'Layered geology / Side profile'},
 arrival:{position:[29,19.2,65],target:[1,27,-17],player:[27,57],fov:60,label:'Arrival meadow'},
};
