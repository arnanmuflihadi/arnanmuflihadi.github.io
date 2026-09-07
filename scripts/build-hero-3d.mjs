#!/usr/bin/env node
/** One-time vendor build; the deployed static site needs no npm/runtime build.
 * npm install --prefix <temporary directory> --ignore-scripts three@0.180.0 esbuild@0.25.10
 * node scripts/build-hero-3d.mjs --deps <temporary directory>/node_modules
 */
import { readFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const index = process.argv.indexOf('--deps');
if (index < 0 || !process.argv[index + 1]) throw new Error('Pass --deps <temporary node_modules>');
const deps = resolve(process.argv[index + 1]);
for (const [name, version] of [['three', '0.180.0'], ['esbuild', '0.25.10']]) {
  const pkg = JSON.parse(await readFile(resolve(deps, name, 'package.json'), 'utf8'));
  if (pkg.version !== version) throw new Error(`Expected ${name}@${version}`);
}
const { build } = await import(pathToFileURL(resolve(deps, 'esbuild/lib/main.js')));
await build({
  entryPoints: [resolve(root, 'scripts/hero-3d-primitives.mjs')],
  outfile: resolve(root, 'assets/js/vendor/three-hero.min.js'),
  nodePaths: [deps], bundle: true, minify: true, treeShaking: true,
  format: 'iife', globalName: 'Hero3DPrimitives', target: 'es2020',
  legalComments: 'eof',
  banner: { js: '/*! Three.js r180 (MIT). Curated hero renderer; see THREE-LICENSE.txt. */' }
});
