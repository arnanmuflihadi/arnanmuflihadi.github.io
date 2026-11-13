export const radius = 0.42;
export function blocked(x,z,obstacles,padding=radius) {
  return Math.abs(x)>31-padding || Math.abs(z)>31-padding || obstacles.some(b=>x>b.x-b.w/2-padding && x<b.x+b.w/2+padding && z>b.z-b.d/2-padding && z<b.z+b.d/2+padding);
}
export function move(position,dx,dz,obstacles) {
  // Axis separation and bounded substeps prevent tunnelling and allow wall sliding.
  const steps=Math.max(1,Math.ceil(Math.max(Math.abs(dx),Math.abs(dz))/.18));
  for(let i=0;i<steps;i++) {
    if(!blocked(position.x+dx/steps,position.z,obstacles)) position.x+=dx/steps;
    if(!blocked(position.x,position.z+dz/steps,obstacles)) position.z+=dz/steps;
  }
  return position;
}
