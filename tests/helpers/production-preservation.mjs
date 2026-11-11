import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha=b=>createHash('sha256').update(b).digest('hex');
// Earlier isolated phases froze all entry code. S2-F explicitly authorizes two integration seams.
// Keep their historical bytes and require the exact reviewed successor; all other paths stay frozen.
export function assertProductionPreserved(){
 const changes=JSON.parse(readFileSync('validation/town-s2f/integration-authorization.json'));
 const allowed=new Set(['assets/js/floating-atlas/entry.js','assets/js/living-atlas-controller.js']);
 assert.equal(changes.files.length,2);
 for(const f of changes.files){assert.ok(allowed.has(f.file));assert.equal(sha(readFileSync(f.before_file)),f.before_sha256);assert.equal(sha(readFileSync(f.file)),f.after_sha256);}
 for(const f of JSON.parse(readFileSync('docs/architecture-r0b1-review/production-baseline.json')).files){const changed=changes.files.find(c=>c.file===f.file);assert.equal(changed?.before_sha256||sha(readFileSync(f.file)),f.sha256,f.file);}
}
