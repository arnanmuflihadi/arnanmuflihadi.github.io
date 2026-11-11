import { layout } from './layout.js?v=40';
export const playerRadius = .34;
export function blocked(x, z, obstacles, radius = playerRadius) {
  return Math.abs(x) > layout.bounds - radius || Math.abs(z) > layout.bounds - radius || obstacles.some(o => !o.cameraOnly && x > o.x - o.w / 2 - radius && x < o.x + o.w / 2 + radius && z > o.z - o.d / 2 - radius && z < o.z + o.d / 2 + radius);
}
export function slide(position, dx, dz, obstacles) {
  const steps = Math.max(1, Math.ceil(Math.max(Math.abs(dx), Math.abs(dz)) / .12));
  for (let i = 0; i < steps; i++) {
    if (!blocked(position.x + dx / steps, position.z, obstacles)) position.x += dx / steps;
    if (!blocked(position.x, position.z + dz / steps, obstacles)) position.z += dz / steps;
  }
}
// Swept line against expanded world-space solids; independent of render batches.
export function clearDistance(origin, destination, obstacles, padding = .28) {
  const delta = { x: destination.x - origin.x, y: destination.y - origin.y, z: destination.z - origin.z };
  let nearest = 1;
  for (const o of obstacles) {
    let enter = 0, leave = 1;
    const bounds = { x: [o.x - o.w / 2 - padding, o.x + o.w / 2 + padding], y: [o.minY ?? -.2, o.h + padding], z: [o.z - o.d / 2 - padding, o.z + o.d / 2 + padding] };
    for (const axis of ['x', 'y', 'z']) {
      if (Math.abs(delta[axis]) < 1e-7) { if (origin[axis] < bounds[axis][0] || origin[axis] > bounds[axis][1]) { enter = 2; break; } }
      else { let a = (bounds[axis][0] - origin[axis]) / delta[axis], b = (bounds[axis][1] - origin[axis]) / delta[axis]; if (a > b) [a, b] = [b, a]; enter = Math.max(enter, a); leave = Math.min(leave, b); }
    }
    if (enter <= leave && enter >= 0 && enter <= 1) nearest = Math.min(nearest, enter);
  }
  return Math.hypot(delta.x, delta.y, delta.z) * nearest;
}
// A moving resident must not embed the player in an expanded footprint. Resolve
// only the overlap, against static solids, before normal swept movement resumes.
export function separateFromPeople(position,people,obstacles){
 for(const p of people){
  const dx=position.x-p.x,dz=position.z-p.z;
  if(Math.abs(dx)>=.65||Math.abs(dz)>=.65)continue;
  const options=[{x:p.x+Math.sign(dx||1)*.66,z:position.z},{x:position.x,z:p.z+Math.sign(dz||1)*.66}].sort((a,b)=>Math.hypot(a.x-position.x,a.z-position.z)-Math.hypot(b.x-position.x,b.z-position.z));
  const free=options.find(q=>!blocked(q.x,q.z,obstacles));if(free){position.x=free.x;position.z=free.z;}
 }
}
