import{fixture as base}from'../town-s2g/fixture.mjs';
import{integrateTown}from'../../assets/js/floating-atlas/town-integration.js';
import{squareAsset}from'../../assets/js/floating-atlas/town-square.js';
import{readFileSync}from'node:fs';
import * as T from'../../assets/js/vendor/three-atlas.module.js?v=16';
export async function fixture(){const f=await base();f.town.dispose();const b=readFileSync(new URL(squareAsset.url)),asset=await new T.GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'');const library=f.world.library,original=library.get;library.get=id=>id==='square'?Promise.resolve(asset):original(id);const town=await integrateTown(f.world,{terrainStudy:true,squareStudy:true});return{...f,town,dispose(){town.dispose();f.world.dispose();}};}
