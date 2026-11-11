// One scene, authored camera compositions; positions are conceptual, not GIS coordinates.
export const presentations=Object.freeze({
  arrival:{position:[-2,21,40],target:[1,3,5],label:'Jakarta / The Urban Atlas'},
  transit:{position:[-6,16,26],target:[-23,3,1],focus:{x:-23,z:11},label:'Jakarta / Stasiun Taman'},
  cbd:{position:[36,21,30],target:[21,8,0],focus:{x:21,z:11},label:'Jakarta / Menara Teras'},
  mbr:{position:[-10,14,6],target:[0,4,-20],focus:{x:0,z:-16.8},label:'Jakarta / Neighbourhood observatory'},
  pangan:{position:[7,15,35],target:[28,3,20],label:'West Java research / Atlas pavilion'},
  'alphaearth-food':{position:[16,20,37],target:[29,3,21],label:'Earth observation / Atlas pavilion'},
  'bandung-cafe':{position:[-13,14,6],target:[-6,4,-20],label:'Bandung research / Atlas pavilion'},
});
export const presentationFor=id=>presentations[id]||presentations.arrival;
// Interaction zones cover the public approach, independently of safe spawn points.
export const landmarks=Object.freeze([
  {projectId:'transit',x:-23,z:9,radius:10},
  {projectId:'cbd',x:21,z:7,radius:9},
  {projectId:'mbr',x:0,z:-16,radius:7},
]);
export function mixComposition(a,b,t){
  const clamp=Math.max(0,Math.min(1,t)),smooth=clamp*clamp*(3-2*clamp);
  return {position:a.position.map((v,i)=>v+(b.position[i]-v)*smooth),target:a.target.map((v,i)=>v+(b.target[i]-v)*smooth)};
}
