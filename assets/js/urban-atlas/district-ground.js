import * as T from '../vendor/three-atlas.module.js?v=16';
import{sidewalks,walks,frontageWalks,publicRealmOutline,streets,curbRamps}from'./layout.js?v=40';
import{parkPond,serviceCourt}from'./district-plan.js?v=40';

const rectangle=r=>[[r.x-r.w/2,r.z-r.d/2],[r.x+r.w/2,r.z-r.d/2],[r.x+r.w/2,r.z+r.d/2],[r.x-r.w/2,r.z+r.d/2]];
function clip(poly,a,b,inside){const result=[],distance=p=>(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);for(let i=0;i<poly.length;i++){const p=poly[i],q=poly[(i+1)%poly.length],dp=distance(p),dq=distance(q),keep=inside?dp>=-1e-8:dp<=1e-8;if(keep)result.push(p);if(dp*dq< -1e-12){const t=dp/(dp-dq);result.push([p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t]);}}return result;}
function subtract(poly,cut){let inside=poly;const pieces=[];for(let i=0;i<cut.length&&inside.length>=3;i++){const a=cut[i],b=cut[(i+1)%cut.length],outside=clip(inside,a,b,false);if(outside.length>=3)pieces.push(outside);inside=clip(inside,a,b,true);}return pieces;}
const overlaps=(a,b)=>Math.max(...a.map(p=>p[0]))>Math.min(...b.map(p=>p[0]))+1e-7&&Math.min(...a.map(p=>p[0]))<Math.max(...b.map(p=>p[0]))-1e-7&&Math.max(...a.map(p=>p[1]))>Math.min(...b.map(p=>p[1]))+1e-7&&Math.min(...a.map(p=>p[1]))<Math.max(...b.map(p=>p[1]))-1e-7;

// A geometric union prevents coplanar slabs and keeps paving out of roads/ramps.
export function createDistrictPaving(){
  const contour=publicRealmOutline.map(p=>new T.Vector2(...p)),triangulated=new T.ExtrudeGeometry(new T.Shape(contour),{depth:.1,bevelEnabled:false,steps:1}),p=triangulated.attributes.position,n=triangulated.attributes.normal,base=[];
  for(let i=0;i<p.count;i+=3)if(n.getZ(i)>.5){const triangle=[0,1,2].map(j=>[p.getX(i+j),p.getY(i+j)]);if((triangle[1][0]-triangle[0][0])*(triangle[2][1]-triangle[0][1])-(triangle[1][1]-triangle[0][1])*(triangle[2][0]-triangle[0][0])<0)triangle.reverse();base.push(triangle);}triangulated.dispose();
  const accepted=[...base],cutouts=[...streets.map(rectangle),...curbRamps.map(rectangle),rectangle(parkPond),rectangle(serviceCourt)];
  for(const r of[...sidewalks,...walks,...frontageWalks]){const rect=rectangle(r);let pieces=[rect];for(const prior of accepted){if(!overlaps(rect,prior))continue;pieces=pieces.flatMap(p=>overlaps(p,prior)?subtract(p,prior):[p]);if(!pieces.length)break;}accepted.push(...pieces);}
  let polygons=accepted;for(const cut of cutouts)polygons=polygons.flatMap(p=>overlaps(p,cut)?subtract(p,cut):[p]);
  const positions=[];
  function tri(a,b,c){positions.push(...a,...b,...c);}
  for(const p of polygons){for(let i=1;i<p.length-1;i++)tri([p[0][0],.24,p[0][1]],[p[i+1][0],.24,p[i+1][1]],[p[i][0],.24,p[i][1]]);for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length];tri([a[0],-.02,a[1]],[b[0],.24,b[1]],[a[0],.24,a[1]]);tri([a[0],-.02,a[1]],[b[0],-.02,b[1]],[b[0],.24,b[1]]);}}
  const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(positions,3));geometry.computeVertexNormals();geometry.computeBoundingBox();geometry.computeBoundingSphere();return geometry;
}
