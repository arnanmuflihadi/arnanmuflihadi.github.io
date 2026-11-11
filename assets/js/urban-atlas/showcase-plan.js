const items=[
  {asset:'architecture',model:'office',height:22.4,x:-7,y:.16,z:-5.86},
  {asset:'architecture',model:'shop',height:13.6,x:7,y:.16,z:-5.01},
  {asset:'tree',height:6.5,x:-17.3,y:.185,z:3,collision:'trunk'},
  {asset:'planter',height:.8,x:10.8,y:.16,z:4.4},
  {asset:'fern',height:.65,x:10.8,y:.91,z:4.4,collidable:false},
  {asset:'fern',height:.65,x:-18,y:.21,z:3,collidable:false},
  {asset:'fern',height:.65,x:-16.6,y:.21,z:3,collidable:false},
  {asset:'architecture',model:'drain',height:.035,x:8,y:-.03,z:8.1,collidable:false},
  {asset:'architecture',model:'manhole',height:.035,x:-4,y:-.03,z:10.5,collidable:false},
  {asset:'architecture',model:'aircon',height:.6,x:10.8,y:3.7,z:.9,collidable:false}
];
for(const x of[-10,-8,7,9])items.push({asset:'architecture',model:'bollard',height:.8,x,y:.16,z:6.9});
for(let x=-15;x<=15;x+=3)for(const z of[3,6])items.push({asset:'architecture',model:'paving',height:.15,x,y:.01,z,collidable:false});
export const showcasePlan=Object.freeze(items.map(Object.freeze));
