import{realmSpecs,reviewViews}from'./plan.js?v=63';
export const presentations=Object.freeze({
 arrival:{position:[108,76,136],target:[-7,10,-4],label:'Transit Kingdom / The living landscape'},
 transit:{position:[46,48,57],target:[-25,32,-27],label:'Transit research / Settlement not constructed'},
 cbd:{position:[92,49,90],target:[15,21,8],label:'Business centres / Research available'},
 mbr:{position:[-124,60,103],target:[-12,10,8],label:'Urban morphology / Research available'},
 pangan:{position:[92,57,117],target:[-28,15,30],label:'Rice logistics / Research available'},
 'alphaearth-food':{position:[-118,67,89],target:[-35,24,-20],label:'Historical paddy / Research available'},
 'bandung-cafe':{position:[-96,63,6],target:[-39,39,-35],label:'Bandung locations / Research available'},
});
export const presentationFor=id=>presentations[id]||presentations.arrival;
export const landmarks=[];
export function mixComposition(a,b,t){const v=Math.max(0,Math.min(1,t)),s=v*v*(3-2*v);return{position:a.position.map((x,i)=>x+(b.position[i]-x)*s),target:a.target.map((x,i)=>x+(b.target[i]-x)*s)};}
export {realmSpecs,reviewViews};
