import{groundHeight,terrainSample}from'./terrain.js?v=56';
export const decks=Object.freeze([
 {id:'skyport',x:12,z:47,w:18,d:16,cut:2,top:10.015},
 {id:'station',x:-8,z:-14,w:31,d:25,cut:1.8,top:16.015},
 {id:'pavilion',x:-29,z:-35,w:13,d:12,cut:1,top:28.015},
 {id:'overlook',x:-51,z:-2,w:13,d:11,cut:1.2,top:22.015},
]);
export const onDeck=(x,z,d)=>{const a=Math.abs(x-d.x),b=Math.abs(z-d.z);return a<=d.w/2&&b<=d.d/2&&a+b<=(d.w+d.d)/2-d.cut;};
export function worldHeight(x,z){let y=groundHeight(x,z);for(const d of decks)if(onDeck(x,z,d))y=Math.max(y,d.top);return y;}
export function safePosition(x,z){const t=terrainSample(x,z);return decks.some(d=>onDeck(x,z,d))||(t.height>0&&t.fraction<.93);}
