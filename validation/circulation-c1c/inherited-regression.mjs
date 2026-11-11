// Run existing assertions unchanged while preserving their approved output records.
import fs from'node:fs';import{syncBuiltinESMExports}from'node:module';const write=fs.writeFileSync;
fs.writeFileSync=(path,...args)=>write(typeof path==='string'?path.replace(/^validation\/town-square-c1b\//,'validation/circulation-c1c/inherited-c1b-').replace(/^validation\/terrain-c1a5\//,'validation/circulation-c1c/inherited-terrain-'):path,...args);syncBuiltinESMExports();
await import('../../tests/town-s2f.test.mjs');await import('../../tests/town-s2g.test.mjs');await import('../../tests/town-square-c1b.test.mjs');await import('../../tests/terrain-c1a5.test.mjs');
