#!/usr/bin/env node
// Convert only reviewed CC0 kit models. Source archives remain outside the site.
import{resolve}from'node:path';import{pathToFileURL}from'node:url';import{readFile,writeFile,copyFile}from'node:fs/promises';import{createHash}from'node:crypto';
const arg=n=>{const i=process.argv.indexOf(n);if(i<0)throw Error(`Required ${n}`);return resolve(process.argv[i+1]);};
const deps=arg('--deps'),source=arg('--source');
const{NodeIO}=await import(pathToFileURL(resolve(deps,'@gltf-transform/core/dist/index.modern.js')));
const{dedup,prune,textureCompress}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const{default:sharp}=await import(pathToFileURL(resolve(deps,'sharp/lib/index.js')));
const models=[['city-building','downtown-city-megakit','Exports/glTF (Godot)/Building_Small_1.gltf'],['city-planter','downtown-city-megakit','Exports/glTF (Godot)/Prop_Planter_Single.gltf'],['canopy-tree','stylized-nature-megakit','glTF/CommonTree_1.gltf'],['fern','stylized-nature-megakit','glTF/Fern_1.gltf']];
const sha=b=>createHash('sha256').update(b).digest('hex'),manifest=[];
for(const[id,pack,file]of models){
 const path=resolve(source,pack,file),io=new NodeIO(),doc=await io.read(path);
 await doc.transform(prune(),dedup(),textureCompress({encoder:sharp,targetFormat:'png',resize:[256,256]}));
 for(const m of doc.getRoot().listMaterials())m.setMetallicFactor(0).setRoughnessFactor(.95);
 const output=`assets/game/scenery/${id}.glb`;await io.write(output,doc);
 manifest.push({id,pack,sourceFile:file,sourceSha256:sha(await readFile(path)),outputSha256:sha(await readFile(output)),bytes:(await readFile(output)).length,license:'CC0-1.0',changes:['Keep the actual mesh/UVs/normals/material textures','Downsize texture maps to at most 256px as PNG','Nonmetallic matte finish; prune and deduplicate']});
}
for(const pack of ['downtown-city-megakit','stylized-nature-megakit'])await copyFile(resolve(source,pack,'License_Standard.txt'),`assets/game/scenery/${pack}-LICENSE.txt`);
await writeFile('assets/game/scenery/source.json',JSON.stringify({author:'Quaternius',pages:['https://quaternius.com/packs/downtowncitymegakit.html','https://quaternius.com/packs/stylizednaturemegakit.html'],models:manifest},null,2)+'\n');console.log(manifest.map(m=>({id:m.id,bytes:m.bytes})));
