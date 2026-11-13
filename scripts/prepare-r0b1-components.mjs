import{readFile,writeFile,mkdir,readdir}from'node:fs/promises';
import{resolve}from'node:path';
import{pathToFileURL}from'node:url';
import{createHash}from'node:crypto';
const deps=process.argv[process.argv.indexOf('--deps')+1];if(!deps||!process.argv.includes('--deps'))throw Error('Pass --deps temporary/node_modules');
const{NodeIO,Document,getBounds}=await import(pathToFileURL(resolve(deps,'@gltf-transform/core/dist/index.modern.js'))),{ALL_EXTENSIONS}=await import(pathToFileURL(resolve(deps,'@gltf-transform/extensions/dist/index.js'))),{mergeDocuments,dedup,prune}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const{unpartition}=await import(pathToFileURL(resolve(deps,'@gltf-transform/functions/dist/functions.modern.js')));
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS),doc=new Document(),scene=doc.createScene('R0B1 verified source components'),sha=b=>createHash('sha256').update(b).digest('hex');
const selected=[
 ['modular-buildings','window-white-detailed','A-window',6,0],
 ['modular-buildings','window-white-tall','A-window-tall',6,0],
 ['modular-buildings','door-white-glass','A-door',4.8,0],
 ['building-kit','wall-window-wide-square-detailed','B-window-wall',1,-Math.PI/2],
 ['building-kit','wall-doorway-wide-square','B-portal',1,-Math.PI/2],
 ['building-kit','door-rotate-square-a','B-door',1,-Math.PI/2],
 ['building-kit','column-thin','B-column',4/3,0],
 ['building-kit','stairs-open-short','B-stair',1,-Math.PI/2],
 ['building-kit','border-high-corner-round','B-parapet',1,0]
];
const packs=[],models=[];for(const[pack,version]of[['modular-buildings','2.1'],['building-kit','1.0']]){const base='source-assets/r0b1/'+pack,license=await readFile(base+'/License.txt'),archive='source-assets/r0b1/kenney_'+pack+'.zip';if(!license.toString().includes('CC0'))throw Error('Missing CC0 notice');packs.push({id:pack,version,author:'Kenney',page:'https://kenney-assets.itch.io/'+pack,archive,archiveBytes:(await readFile(archive)).length,archiveSha256:sha(await readFile(archive)),license:'CC0-1.0',licenseFile:base+'/License.txt',licenseSha256:sha(license),attribution:'Not required; credited in manifest',glbFiles:(await readdir(base+'/Models/GLB format')).filter(n=>n.endsWith('.glb')).length});}
for(const[pack,name,id,scale,rotation]of selected){
 const file='source-assets/r0b1/'+pack+'/Models/GLB format/'+name+'.glb',bytes=await readFile(file),source=await io.read(file),root=source.getRoot(),original=root.getDefaultScene()||root.listScenes()[0],group=source.createNode(id);
 for(const child of original.listChildren())group.addChild(child);original.addChild(group);group.setScale([scale,scale,scale]).setRotation([0,Math.sin(rotation/2),0,Math.cos(rotation/2)]);const bounds=getBounds(group);group.setTranslation([-(bounds.min[0]+bounds.max[0])/2,-bounds.min[1],-(bounds.min[2]+bounds.max[2])/2]);group.setExtras({sourcePack:pack,sourceModel:name+'.glb',sourceSha256:sha(bytes),license:'CC0-1.0',uniformScale:scale});
 const record={id,pack,file,sourceSha256:sha(bytes),sourceBytes:bytes.length,sourceBounds:bounds,normalizedBounds:getBounds(group),uniformScale:scale,rotation,triangles:root.listMeshes().reduce((n,m)=>n+m.listPrimitives().reduce((v,p)=>v+(p.getIndices()?.getCount()||p.getAttribute('POSITION').getCount())/3,0),0),materials:root.listMaterials().map(m=>({name:m.getName(),alphaMode:m.getAlphaMode(),roughness:m.getRoughnessFactor(),color:m.getBaseColorFactor()})),textures:root.listTextures().map(t=>({name:t.getName(),size:t.getSize(),bytes:t.getImage()?.length,mimeType:t.getMimeType()}))};models.push(record);const mapping=mergeDocuments(doc,source);scene.addChild(mapping.get(group));
}
for(const s of doc.getRoot().listScenes())if(s!==scene)s.dispose();doc.getRoot().setDefaultScene(scene);await doc.transform(dedup(),prune(),unpartition());await mkdir('assets/game/architecture-r0b1',{recursive:true});const output='assets/game/architecture-r0b1/components.glb';await io.write(output,doc);await writeFile('assets/game/architecture-r0b1/components-source.json',JSON.stringify({phase:'R0-B1',date:'2026-11-02',packs,models,output,bytes:(await readFile(output)).length,sha256:sha(await readFile(output)),changes:['Select individual square modern components only; exclude sample buildings','Preserve source geometry, UVs, textures and material identities','Uniform metric normalization, ground-centered origins, front +Z orientation','Embed dependencies and deduplicate identical resources'],tooling:{core:'4.2.1',functions:'4.2.1',extensions:'4.5.1'}},null,2)+'\n');console.log({output,bytes:(await readFile(output)).length,models:models.map(m=>({id:m.id,bounds:m.normalizedBounds,triangles:m.triangles,textures:m.textures}))});
