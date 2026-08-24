#!/usr/bin/env node
/**
 * Dependency-free server for a GitHub Pages-equivalent preview directory.
 *
 * Before listening, it streams deterministic gzip level-9 representations for
 * eligible text assets into an OS-temporary cache. The served root is never
 * modified, and the cache is removed on a clean SIGINT/SIGTERM shutdown.
 *
 * Usage: node scripts/serve-pages-preview.mjs --root /path/to/_site --port 4173
 */
import { createServer } from 'node:http';
import { createReadStream, createWriteStream } from 'node:fs';
import { lstat, mkdir, mkdtemp, readdir, realpath, rm, stat } from 'node:fs/promises';
import { pipeline } from 'node:stream/promises';
import { createGzip } from 'node:zlib';
import { tmpdir } from 'node:os';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';

const args = process.argv.slice(2);
const valueFor = (name, fallback) => {
  const index = args.indexOf(name);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
};
const requestedRoot = resolve(valueFor('--root', process.cwd()));
const port = Number(valueFor('--port', '4173'));
const maxGzipSourceBytes = 8 * 1024 * 1024;
const compressibleExtensions = new Set(['.css', '.geojson', '.html', '.js', '.json', '.mjs', '.svg']);
const privatePathSegments = new Set(['.git', '.github']);
const contentTypes = {
  '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.pdf': 'application/pdf', '.geojson': 'application/geo+json; charset=utf-8',
  '.woff2': 'font/woff2', '.ico': 'image/x-icon'
};

let root = '';
let gzipCacheRoot = '';
let server = null;
let shutdownPromise = null;
const gzipCache = new Map();

const insideRoot = (candidate) => candidate === root || candidate.startsWith(root + sep);
const pathSegments = (source) => relative(root, source).split(sep).filter(Boolean);
const isDki3d = (source) => pathSegments(source)[0] === 'dki-3d';
const isPrivatePath = (source) => pathSegments(source).some((segment) => privatePathSegments.has(segment));
const contentTypeFor = (source) => contentTypes[extname(source).toLowerCase()] || 'application/octet-stream';
const isGzipEligible = (source, info) => (
  info.isFile() &&
  info.size < maxGzipSourceBytes &&
  !isDki3d(source) &&
  !isPrivatePath(source) &&
  compressibleExtensions.has(extname(source).toLowerCase())
);

function acceptsGzip(value) {
  if (!value) return false;
  let wildcard = null;
  for (const item of value.split(',')) {
    const parts = item.trim().toLowerCase().split(';').map((part) => part.trim());
    if (parts[0] !== 'gzip' && parts[0] !== '*') continue;
    const quality = parts.find((part) => part.startsWith('q='));
    const allowed = !quality || Number(quality.slice(2)) > 0;
    if (parts[0] === 'gzip') return allowed;
    wildcard = allowed;
  }
  return Boolean(wildcard);
}

function respond(req, res, status, body) {
  const bytes = Buffer.byteLength(body);
  res.writeHead(status, {
    'Content-Type': 'text/plain; charset=utf-8',
    'Cache-Control': 'no-store',
    'Content-Length': String(bytes),
    'X-Content-Type-Options': 'nosniff'
  });
  if (req.method === 'HEAD') return res.end();
  return res.end(body);
}

async function buildGzipCache(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    const lexicalSource = join(directory, entry.name);
    if (entry.isSymbolicLink()) continue;
    if (entry.isDirectory()) {
      if (!isDki3d(lexicalSource) && !isPrivatePath(lexicalSource)) await buildGzipCache(lexicalSource);
      continue;
    }
    if (!entry.isFile()) continue;
    const source = await realpath(lexicalSource);
    if (!insideRoot(source) || isPrivatePath(source)) continue;
    const info = await stat(source);
    if (!isGzipEligible(source, info)) continue;

    const compressed = join(gzipCacheRoot, `${relative(root, source)}.gz`);
    await mkdir(dirname(compressed), { recursive: true });
    await pipeline(
      createReadStream(source),
      createGzip({ level: 9, mtime: 0 }),
      createWriteStream(compressed, { flags: 'w' })
    );
    const compressedInfo = await stat(compressed);
    gzipCache.set(source, {
      path: compressed,
      bytes: compressedInfo.size,
      sourceBytes: info.size,
      contentType: contentTypeFor(source)
    });
  }
}

async function resolveFile(relativePath) {
  let candidate = resolve(root, relativePath);
  if (!insideRoot(candidate) || isPrivatePath(candidate)) return { forbidden: true };
  let target;
  try {
    target = await realpath(candidate);
  } catch {
    return { missing: true };
  }
  if (!insideRoot(target) || isPrivatePath(target)) return { forbidden: true };

  let info = await lstat(target);
  if (info.isDirectory()) {
    candidate = join(target, 'index.html');
    try {
      target = await realpath(candidate);
    } catch {
      return { missing: true };
    }
    if (!insideRoot(target) || isPrivatePath(target)) return { forbidden: true };
    info = await lstat(target);
  }
  return info.isFile() ? { target, info } : { missing: true };
}

async function sendFile(req, res, source, info, status = 200) {
  const compressed = gzipCache.get(source);
  const useGzip = Boolean(compressed && acceptsGzip(req.headers['accept-encoding']));
  const target = useGzip ? compressed.path : source;
  const headers = {
    'Content-Type': compressed?.contentType || contentTypeFor(source),
    'Cache-Control': 'no-store',
    'Content-Length': String(useGzip ? compressed.bytes : info.size),
    'X-Content-Type-Options': 'nosniff'
  };
  if (compressed) headers.Vary = 'Accept-Encoding';
  if (useGzip) headers['Content-Encoding'] = 'gzip';

  res.writeHead(status, headers);
  if (req.method === 'HEAD') return res.end();
  const stream = createReadStream(target);
  stream.on('error', (error) => {
    if (!res.headersSent) respond(req, res, 500, `Preview server error: ${error.message}`);
    else res.destroy(error);
  });
  stream.pipe(res);
}

async function handleRequest(request, response) {
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    response.writeHead(405, { Allow: 'GET, HEAD', 'Cache-Control': 'no-store', 'Content-Length': '0' });
    response.end();
    return;
  }
  const rawPathname = (request.url || '/').split(/[?#]/, 1)[0];
  let decodedPathname;
  try {
    decodedPathname = decodeURIComponent(rawPathname);
  } catch {
    respond(request, response, 400, 'Malformed request path');
    return;
  }
  if (decodedPathname.includes('\0')) {
    respond(request, response, 400, 'Malformed request path');
    return;
  }
  if (decodedPathname.split('/').includes('..')) {
    respond(request, response, 403, 'Forbidden');
    return;
  }

  let relativePath = decodedPathname.replace(/^\/+/, '');
  if (!relativePath || relativePath.endsWith('/')) relativePath = join(relativePath, 'index.html');
  const resolved = await resolveFile(relativePath);
  if (resolved.forbidden) {
    respond(request, response, 403, 'Forbidden');
    return;
  }
  if (resolved.missing) {
    const fallback = await resolveFile('404.html');
    if (fallback.target) return sendFile(request, response, fallback.target, fallback.info, 404);
    respond(request, response, 404, 'Not found');
    return;
  }
  return sendFile(request, response, resolved.target, resolved.info);
}

async function shutdown(exitCode = 0) {
  if (shutdownPromise) return shutdownPromise;
  shutdownPromise = (async () => {
    if (server?.listening) await new Promise((done) => server.close(done));
    if (gzipCacheRoot) await rm(gzipCacheRoot, { recursive: true, force: true });
    process.exitCode = exitCode;
  })();
  return shutdownPromise;
}

async function start() {
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('--port must be an integer from 1 through 65535');
  const rootInfo = await stat(requestedRoot);
  if (!rootInfo.isDirectory()) throw new Error(`--root is not a directory: ${requestedRoot}`);
  root = await realpath(requestedRoot);
  gzipCacheRoot = await mkdtemp(join(tmpdir(), 'pages-preview-gzip-'));
  await buildGzipCache(root);

  server = createServer((request, response) => {
    handleRequest(request, response).catch((error) => respond(request, response, 500, `Preview server error: ${error.message}`));
  });
  await new Promise((resolveListening, rejectListening) => {
    server.once('error', rejectListening);
    server.listen(port, '127.0.0.1', resolveListening);
  });
  console.log(`Pages preview: http://127.0.0.1:${port}/ (root: ${root}; gzip cache: ${gzipCache.size} files at ${gzipCacheRoot})`);
}

process.once('SIGINT', () => shutdown().then(() => process.exit(0)));
process.once('SIGTERM', () => shutdown().then(() => process.exit(0)));

try {
  await start();
} catch (error) {
  await shutdown(1);
  console.error(`Pages preview failed: ${error.message}`);
}
