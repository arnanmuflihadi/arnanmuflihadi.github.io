import * as T from'../vendor/three-atlas.module.js?v=16';

export function trailPlantGeometry(flower=false){
 const p=[],c=[],idx=[],leafBase=new T.Color('#345f4c'),leafTip=new T.Color('#85a26b'),petal=new T.Color(flower?'#c89172':'#b5bd7b');
 for(let j=0;j<8;j++){
  const a=j*2.399,base=.12+j%3*.18,length=.52+(j%3)*.17,vi=p.length/3;
  for(let r=0;r<7;r++)for(const s of[-1,1]){const t=r/6,w=Math.sin(Math.PI*t)*(.15+j%2*.045),out=t*length,y=base+Math.sin(t*Math.PI*.8)*.48-t*t*.15;p.push(Math.cos(a)*out-Math.sin(a)*w*s,y,Math.sin(a)*out+Math.cos(a)*w*s);const col=leafBase.clone().lerp(leafTip,t*.65);c.push(col.r,col.g,col.b);}
  for(let r=0;r<6;r++){const k=vi+r*2;idx.push(k,k+2,k+1,k+1,k+2,k+3);}
 }
 if(flower){
  const start=p.length/3;for(let r=0;r<2;r++)for(let i=0;i<6;i++){const a=i/6*Math.PI*2;p.push(Math.cos(a)*.026,r*1.08,Math.sin(a)*.026);c.push(leafBase.r,leafBase.g,leafBase.b);if(r===0){const j=(i+1)%6;idx.push(start+i,start+i+6,start+j,start+j,start+i+6,start+j+6);}}
  for(let ring=0;ring<4;ring++)for(let j=0;j<5;j++){
   const a=j/5*Math.PI*2+ring*.8,y=.72+ring*.12,radius=.17-ring*.025,k=p.length/3;
   p.push(0,y-.08,0,Math.cos(a-.42)*radius,y,Math.sin(a-.42)*radius,Math.cos(a)*radius*.7,y+.13,Math.sin(a)*radius*.7,Math.cos(a+.42)*radius,y,Math.sin(a+.42)*radius);
   for(let i=0;i<4;i++){const color=petal.clone().multiplyScalar(.82+ring*.06);c.push(color.r,color.g,color.b);}idx.push(k,k+1,k+2,k,k+2,k+3);
  }
 }
 const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('color',new T.Float32BufferAttribute(c,3));g.setIndex(idx);g.computeVertexNormals();g.computeBoundingBox();return g;
}
