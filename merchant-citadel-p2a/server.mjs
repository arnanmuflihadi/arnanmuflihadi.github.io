#!/usr/bin/env node
/**
 * Dependency-free preview server for the Merchant Citadel P2-A slice.
 * Serves the repository root read-only (so the preview can import the game's real controller and camera modules unchanged)
 * and accepts POST /__save?name=<file> to write test evidence (screenshots, JSON) into merchant-citadel-p2a/evidence/ only.
 * Usage: node merchant-citadel-p2a/server.mjs [--port 4180]
 */
import { createServer } from 'node:http';
import { createReadStream } from 'node:fs';
import { mkdir, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const evidence = join(here, 'evidence');
const args = process.argv.slice(2);
const port = Number(args[args.indexOf('--port') + 1]) || 4180;
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.glb': 'model/gltf-binary', '.bin': 'application/octet-stream', '.png': 'image/png', '.jpg': 'image/jpeg', '.css': 'text/css; charset=utf-8', '.md': 'text/plain; charset=utf-8' };

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (req.method === 'POST' && url.pathname === '/__save') {
      const name = (url.searchParams.get('name') || '').replace(/[^A-Za-z0-9._-]/g, '_');
      if (!name || name.startsWith('.')) { res.writeHead(400); return res.end('bad name'); }
      const chunks = []; for await (const c of req) chunks.push(c);
      await mkdir(evidence, { recursive: true }); await writeFile(join(evidence, name), Buffer.concat(chunks));
      res.writeHead(200, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ saved: name, bytes: Buffer.concat(chunks).length }));
    }
    let path = resolve(root, '.' + decodeURIComponent(url.pathname));
    if (!(path === root || path.startsWith(root + sep))) { res.writeHead(403); return res.end('forbidden'); }
    if (path.split(sep).includes('.git')) { res.writeHead(403); return res.end('forbidden'); }
    let info = await stat(path).catch(() => null);
    if (info?.isDirectory()) { path = join(path, 'index.html'); info = await stat(path).catch(() => null); }
    if (!info) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': types[extname(path).toLowerCase()] || 'application/octet-stream', 'content-length': info.size, 'cache-control': 'no-store' });
    createReadStream(path).pipe(res);
  } catch (e) { res.writeHead(500); res.end(String(e)); }
}).listen(port, '127.0.0.1', () => console.log(`P2-A preview: http://127.0.0.1:${port}/merchant-citadel-p2a/index.html  (evidence -> ${evidence})`));
