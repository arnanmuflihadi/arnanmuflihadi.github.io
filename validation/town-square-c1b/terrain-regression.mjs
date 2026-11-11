// Preserve approved C1A.5 evidence while running its existing assertions unchanged.
import fs from'node:fs';import{syncBuiltinESMExports}from'node:module';
const write=fs.writeFileSync;
fs.writeFileSync=(path,...args)=>write(typeof path==='string'&&path.startsWith('validation/terrain-c1a5/')?path.replace('validation/terrain-c1a5/','validation/town-square-c1b/inherited-'):path,...args);
syncBuiltinESMExports();
await import('../../tests/terrain-c1a5.test.mjs');
