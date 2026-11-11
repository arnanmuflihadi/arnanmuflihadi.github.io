import{readFileSync}from'node:fs';
import * as T from'../../assets/js/vendor/three-atlas.module.js?v=16';
import{createModelLibrary}from'../../assets/js/urban-atlas/model-library.js';
export function fixtureLibrary(){globalThis.ProgressEvent||=class{constructor(type,data){Object.assign(this,data);}};return createModelLibrary({load:async url=>{const path=new URL(url);path.search='';const b=readFileSync(path),n=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+n));delete j.images;delete j.textures;delete j.samplers;j.materials=j.materials.map(m=>({name:m.name}));j.buffers[0].uri='data:application/octet-stream;base64,'+b.subarray(28+n).toString('base64');return new T.GLTFLoader().parseAsync(JSON.stringify(j),'');}});}
export function fixtureArtwork(){const maps=[],map=()=>{const t=new T.DataTexture(new Uint8Array([255,255,255,255]),1,1);maps.push(t);return t;};return{sign:map,display:map,dispose(){maps.forEach(t=>t.dispose());}};}
