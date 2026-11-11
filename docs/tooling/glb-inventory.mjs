#!/usr/bin/env node
// Read-only GLB/glTF inventory: bytes, meshes, triangles, materials, textures, animation clips.
// Usage: node glb-inventory.mjs [rootDir=assets/game] [--json]
// Never writes files. Triangles = indexed count/3 (or position count/3) per TRIANGLES primitive,
// counted once per mesh definition (instancing via nodes is reported separately as nodeRefs).
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname, relative } from 'node:path';

const args = process.argv.slice(2);
const root = args.find(a => !a.startsWith('--')) || 'assets/game';
const asJson = args.includes('--json');

const walk = d => readdirSync(d).flatMap(n => {
  const p = join(d, n);
  return statSync(p).isDirectory() ? walk(p) : [p];
});

function readGltf(file) {
  const buf = readFileSync(file);
  if (extname(file).toLowerCase() === '.glb') {
    if (buf.readUInt32LE(0) !== 0x46546c67) throw new Error('not a GLB');
    const len = buf.readUInt32LE(12);
    return JSON.parse(buf.subarray(20, 20 + len).toString('utf8'));
  }
  return JSON.parse(buf.toString('utf8'));
}

function summarize(file) {
  const g = readGltf(file);
  let triangles = 0;
  for (const m of g.meshes || []) for (const p of m.primitives || []) {
    if ((p.mode ?? 4) !== 4) continue;
    const acc = p.indices !== undefined ? g.accessors[p.indices] : g.accessors[p.attributes.POSITION];
    triangles += Math.floor((acc?.count || 0) / 3);
  }
  const nodeRefs = (g.nodes || []).filter(n => n.mesh !== undefined).length;
  const extBytes = (g.buffers || []).filter(b => b.uri && !b.uri.startsWith('data:'))
    .reduce((s, b) => { try { return s + statSync(join(file, '..', b.uri)).size; } catch { return s; } }, 0);
  return {
    file,
    bytes: statSync(file).size + extBytes,
    meshes: (g.meshes || []).length,
    nodeRefs,
    triangles,
    materials: (g.materials || []).length,
    textures: (g.textures || []).length,
    images: (g.images || []).length,
    skins: (g.skins || []).length,
    clips: (g.animations || []).map(a => a.name || '(unnamed)'),
  };
}

const files = walk(root).filter(f => /\.(glb|gltf)$/i.test(f)).sort();
const rows = files.map(f => { try { return summarize(f); } catch (e) { return { file: f, error: e.message }; } });
if (asJson) { console.log(JSON.stringify(rows, null, 2)); process.exit(0); }
const kb = b => (b / 1024).toFixed(0) + ' KB';
console.log('| File | Bytes | Meshes (node refs) | Triangles | Mat / Tex | Skins | Clips |');
console.log('| --- | ---: | ---: | ---: | ---: | ---: | --- |');
for (const r of rows) {
  if (r.error) { console.log(`| \`${relative('.', r.file)}\` | ERROR: ${r.error} |||||| `); continue; }
  const clips = r.clips.length ? r.clips.slice(0, 8).join(', ') + (r.clips.length > 8 ? ` (+${r.clips.length - 8})` : '') : '—';
  console.log(`| \`${relative('.', r.file)}\` | ${kb(r.bytes)} | ${r.meshes} (${r.nodeRefs}) | ${r.triangles.toLocaleString('en')} | ${r.materials} / ${r.textures} | ${r.skins} | ${clips} |`);
}
