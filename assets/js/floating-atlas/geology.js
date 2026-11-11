import * as T from'../vendor/three-atlas.module.js?v=16';

export function fracturedRock(seed=0){
 const p=[],colors=[],idx=[],n=6,rings=[[-.88,.8],[-.5,1],[.65,1],[.94,.68]],outline=[[-.86,-.53],[.48,-.78],[1,-.19],[.72,.59],[-.42,.8],[-1,.12]],warm=new T.Color('#9c9787'),cool=new T.Color('#687a77');
 for(let r=0;r<4;r++)for(let i=0;i<n;i++){
  const rr=rings[r][1],y=rings[r][0]+.08*Math.sin(i*1.9+seed),[x,z]=outline[i];
  p.push(x*rr*(1+.07*seed)+.32*y,y,z*rr-.23*y);const c=cool.clone().lerp(warm,.3+r*.14+.08*Math.sin(i+seed));colors.push(c.r,c.g,c.b);
  if(r<3){const k=r*n+i,j=r*n+(i+1)%n;idx.push(k,k+n,j,j,k+n,j+n);}
 }
 const top=p.length/3;p.push(.15,.84,-.12);colors.push(warm.r,warm.g,warm.b);const bottom=p.length/3;p.push(-.1,-.86,.1);colors.push(cool.r,cool.g,cool.b);
 for(let i=0;i<n;i++)idx.push(top,3*n+(i+1)%n,3*n+i,bottom,i,(i+1)%n);
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.setIndex(idx);g.computeVertexNormals();g.computeBoundingBox();return g;
}

export function dressCliff({cliffs,b,standard,stats}){
 const rocks=[0,1,2].map(fracturedRock),material=standard('#ffffff',{vertexColors:true,flatShading:true});for(const g of rocks)b.owned.add(g);
 const p=cliffs.geometry.attributes.position,clusters=[[79,5,1],[88,7,1.25],[98,10,.9],[125,6,.9],[139,12,1.1],[24,8,.85],[36,12,1]],n=208;let pieces=0;
 for(const[c,[sector,ring,size]]of clusters.entries()){
  for(let j=0;j<4;j++){
   const v=new T.Vector3().fromBufferAttribute(p,ring*n+sector+Math.round((j-1.5)*2)),normal=new T.Vector3(v.x,0,v.z).normalize(),angle=Math.atan2(normal.x,normal.z),point=v.addScaledVector(normal,-1.4+(j%2)*.3);point.y+=(j%2?1:-1)*size;
   b.instance(rocks[(c+j)%3],material,point.x,point.y,point.z,(3.5+j%2)*size,(5.2+(j+c)%3*1.6)*size,3.1*size,angle,.11*(j-1),.08*(c%3-1));pieces++;
  }
 }
 stats.geology={clusters:clusters.length,rockPieces:pieces,sharedRockGeometries:rocks.length};return{rocks,material};
}
