import{realmSpecs,reviewViews}from'./plan.js?v=56';
export const presentations=Object.freeze({
 arrival:{position:[87,65,116],target:[-7,6,-5],label:'Transit Kingdom / The Floating Urban Atlas'},
 transit:{position:[24,37,27],target:[-8,22,-12],focus:{x:-8,z:3},label:'Transit Kingdom / Stasiun Antara'},
 cbd:{position:[64,37,65],target:[20,16,16],label:'Merchant Citadel / Research available · realm planned'},
 mbr:{position:[-93,44,87],target:[-5,7,4],label:'Mosaic District / Research available · realm planned'},
 pangan:{position:[89,52,94],target:[-26,11,23],label:'Harvest Valley / Research available · realm planned'},
 'alphaearth-food':{position:[-88,57,72],target:[-25,16,-12],label:'Terra Observatory / Research available · realm planned'},
 'bandung-cafe':{position:[-79,57,15],target:[-20,23,-25],label:'Bandung Highlands / Research available · realm planned'},
});
export const presentationFor=id=>presentations[id]||presentations.arrival;
export const landmarks=[{projectId:'transit',x:-8,z:3,radius:8}];
export function mixComposition(a,b,t){const v=Math.max(0,Math.min(1,t)),s=v*v*(3-2*v);return{position:a.position.map((x,i)=>x+(b.position[i]-x)*s),target:a.target.map((x,i)=>x+(b.target[i]-x)*s)};}
export {realmSpecs,reviewViews};
