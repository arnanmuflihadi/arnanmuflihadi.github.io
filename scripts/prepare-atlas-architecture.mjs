#!/usr/bin/env node
// Selected Standard-edition CC0 meshes only. Original archives stay outside the site.
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const option=n=>{const i=process.argv.indexOf(n);if(i<0)throw Error(`Required ${n}`);return resolve(process.argv[i+1]);};
const deps=option('--deps'),source=option('--source');
const {NodeIO,Document,getBounds}=await import(pathToFileURL(resolve(deps,'@gltf-transform/core/dist/index.modern.js')));
const {mergeDocuments,dedup,prune,weld,unpartition,quantize,textureCompress}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const {ALL_EXTENSIONS}=await import(pathToFileURL(resolve(deps,'@gltf-transform/extensions/dist/index.js')));
const {default:sharp}=await import(pathToFileURL(resolve(deps,'sharp/lib/index.js')));
const selected={shop:'Building_Small_1',mixed:'Building_Medium_2_001',office:'Building_Large_2',entrance:'Metal_FirstFloor_Window',glazing:'Metal_FullWindow',civic:'Trim_FirstFloor_Window_001',aircon:'Prop_ACUnit',bollard:'Prop_Bollard',paving:'Sidewalk_NoCurb_3m',drain:'Prop_Drain',manhole:'Prop_ManholeCover'};
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS),library=new Document(),scene=library.createScene('Jakarta prefab library'),records=[];
const sha=b=>createHash('sha256').update(b).digest('hex');
const approved=JSON.parse(await readFile('assets/game/scenery/architecture-source.json','utf8'));
const license=await readFile(resolve(source,'License_Standard.txt'));
if(!license.equals(await readFile('assets/game/scenery/downtown-city-megakit-LICENSE.txt')))throw Error('Source license differs from the reviewed Standard license');
for(const[id,file]of Object.entries(selected)){
 const path=resolve(source,'Exports/glTF (Godot)',file+'.gltf'),sourceBytes=await readFile(path);
 if(sha(sourceBytes)!==approved.models.find(m=>m.id===id)?.sourceSha256)throw Error(`Source differs from reviewed ${file}.gltf`);
 const doc=await io.read(path),original=doc.getRoot().getDefaultScene()||doc.getRoot().listScenes()[0];
 const group=doc.createNode(id);for(const node of original.listChildren())group.addChild(node);original.addChild(group);
 records.push({id,sourceFile:file+'.gltf',sourceSha256:sha(await readFile(path)),bounds:getBounds(original),triangles:doc.getRoot().listMeshes().reduce((n,m)=>n+m.listPrimitives().reduce((v,p)=>v+(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3,0),0)});
 const mapping=mergeDocuments(library,doc);scene.addChild(mapping.get(group));
}
for(const s of library.getRoot().listScenes())if(s!==scene)s.dispose();library.getRoot().setDefaultScene(scene);
await library.transform(weld(),dedup(),prune(),unpartition(),quantize({quantizePosition:14,quantizeNormal:10,quantizeTexcoord:12}),textureCompress({encoder:sharp,slots:/baseColorTexture|emissiveTexture/,targetFormat:'jpeg',quality:82,resize:[512,512]}),textureCompress({encoder:sharp,slots:/normalTexture|occlusionTexture|metallicRoughnessTexture/,targetFormat:'png',resize:[256,256]}));
// Matte, warm mineral palette. The original mapped UVs, normals and façade detail remain.
for(const m of library.getRoot().listMaterials()){
 m.setMetallicFactor(0).setRoughnessFactor(.88);
 const name=m.getName();
 if(name.includes('RedBrick')){m.setBaseColorFactor([1,1,1,1]);const map=m.getBaseColorTexture();if(map&&!map.getExtras().mineralWash){map.setImage(await sharp(map.getImage()).grayscale().linear(.24,166).png().toBuffer()).setMimeType('image/png').setExtras({mineralWash:true});}}
 if(name.includes('Trim')){m.setBaseColorFactor([1,.98,.9,1]);const map=m.getBaseColorTexture();if(map&&!map.getExtras().mineralWash){map.setImage(await sharp(map.getImage()).grayscale().linear(.2,185).png().toBuffer()).setMimeType('image/png').setExtras({mineralWash:true});}}
 if(name.includes('FakeInterior'))m.setBaseColorTexture(null).setBaseColorFactor([.13,.28,.25,1]);
 if(name==='MI_Concrete')m.setBaseColorFactor([.92,.86,.72,1]);
 if(name.includes('Glass')){m.setAlphaMode('OPAQUE').setBaseColorFactor([.19,.39,.36,1]);}
}
await library.transform(prune());
const output='assets/game/scenery/architecture-library.glb';await io.write(output,library);
const geometryBytes=library.getRoot().listAccessors().reduce((n,a)=>n+a.getByteLength(),0);
const textures=library.getRoot().listTextures().map(t=>({name:t.getName(),size:t.getSize(),bytes:t.getImage()?.byteLength||0}));
await writeFile('assets/game/scenery/architecture-source.json',JSON.stringify({author:'Quaternius',edition:'Downtown City MegaKit Standard (free)',source:'https://quaternius.com/packs/downtowncitymegakit.html',license:'CC0-1.0',licenseFile:'downtown-city-megakit-LICENSE.txt',output,bytes:(await readFile(output)).length,outputSha256:sha(await readFile(output)),geometryBytes,textures,models:records,changes:['Select eleven current-district meshes only, including flat paving, drainage and manhole covers','Share duplicated geometry/materials/textures across prefabs','512px JPEG color maps and 256px PNG normal/ORM maps; quantized vertex buffers','Neutral mineral washes for masonry and trim, matte finishes, opaque teal glazing','Replace photographic fake interiors with solid teal to match the stylized district','Keep source topology, UVs, authored façade detail and normals']},null,2)+'\n');
console.log({output,bytes:(await readFile(output)).length,geometryBytes,textures:textures.length,models:records.map(r=>({id:r.id,triangles:r.triangles}))});
