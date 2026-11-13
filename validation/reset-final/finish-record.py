from pathlib import Path
import json,re
from PIL import Image
root=Path.cwd();v=root/'validation/reset-final';d=root/'docs/urban-atlas/reset-final'
read=lambda n:json.loads((v/n).read_text())
s=read('site-validation.json');r=read('controller-routes.json');live=read('live-traversal.json');perf=read('live-performance.json');layout=read('layout.json')
assert len(live['traversal'])==11 and all(x['success']for x in live['traversal'])
assert all(x['success']for x in r['rows']) and r['maxTerrainError']<1e-5 and r['maxSupportError']<1e-4
assert live['scene']==perf['scene'] and perf['rendererCount']=='1'
assert not perf['errors'] and not perf['warnings'] and not perf['town']['assets']['missingTextures']
assert 'pass 35' in (v/'regression.log').read_text()
on=next(x for x in reversed(perf['benchmarks'])if x['on']);off=next(x for x in reversed(perf['benchmarks'])if not x['on'])
captures=[]
views=[('01-island','Whole island'),('02-arrival','Arrival into Market Street'),('03-market','Market Street toward Telaga Awan'),('04-fountain-guild','Fountain toward the Guild reservation'),('05-oblique','Town, terrain and forest'),('06-plan','Measured circulation plan')]
for name,title in views:
 with Image.open(v/(name+'.png'))as im:im.load();assert im.size==(1440,836)
 meta=read(name+'.json');assert meta['scene']==perf['scene'] and meta['enabled'] and meta['settings']['glass']=='B'
 captures.append({'file':name+'.png','title':title,'camera':meta['camera'],'settings':meta['settings'],'scene':meta['scene'],'annotated':name=='06-plan'})
(v/'captures.json').write_text(json.dumps(captures,indent=2)+'\n')
nav=read('navigation-checks.json');assert nav['defaultNoTownRequests'] and nav['sixStudies'] and nav['mbr'] and nav['oldTownAvailable'] and nav['editorialAdventure']
asset=perf['town']['assets'];terrain=s['terrain'];veg=s['vegetation'];maxgap=max(x['maxBaseToGround']for x in s['foundations']);p=s['primaryRoute'];total=sum(x['bytes']for x in s['files'])
text=f'''# R0-RESET-FINAL owner review

Complete local development alternative. **Human visual approval is pending. No public deployment.**

The four unchanged storefront groups now face one civic promenade and a 210 m² Telaga Awan court. Arrival, market, fountain and the 10 × 8 m Guild reservation form one sequence. The old stairs, bridge system and detached forecourt are absent from this version. The Guild has a physical reservation noticeboard, not a building proxy. The arrival is a guarded paved threshold, not finished skyport architecture.

[Six review images](index.html) · [Actual explorer frame](../../../validation/reset-final/walking-forward.png) · [Coordinates](../../../validation/reset-final/layout.json) · [Provenance](../../../validation/reset-final/provenance.json)

| Measurement | Final result |
|---|---|
| Primary walk | {p['lengthMetres']:.2f} m; {p['directMetres']:.2f} m direct; {p['turns']} gentle changes of direction |
| Primary elevation / grade | {p['minElevation']:.3f}–{p['maxElevation']:.3f} m; {p['maxGradePercent']:.2f}% maximum, no civic stairs |
| Clear street / square | 6 m spine; 15 × 14 m court |
| Building lower-shell gap | Maximum {maxgap*100:.2f} cm at sampled plot perimeters; retained visible thresholds support door approaches |
| Terrain | {terrain['changedTriangleFootprintM2']:.1f} m² affected triangles; {terrain['changedVertices']} vertices; {terrain['minDelta']:.2f} to +{terrain['maxDelta']:.2f} m |
| Earth-volume estimate | {terrain['fillEstimateM3']:.1f} m³ fill / {terrain['cutEstimateM3']:.1f} m³ cut, integrated from triangle deltas; environment design only |
| Vegetation | {veg['treeMoves']} trees relocated, {veg['treeRemovals']} removed; {veg['palmChanges']} palm adjustments; {veg['understoryCleared']} understory instances cleared; {veg['grassChunksAdjusted']} grass chunks regrounded |
| Active town geometry | {asset['triangles']:,} triangles; {asset['meshes']} render meshes; {asset['materials']} materials; {asset['textures']} texture objects; no missing textures |
| Source payload | {total:,} bytes across the unchanged market GLB and four civic exports; original market remains 10,007,904 bytes |

The largest +{terrain['maxDelta']:.2f} m fill is in the locally blended forest connector, removing its former deep dip. The island rim, cliffs, waterfall and highland ridge are unchanged. Rendered terrain and the existing height/collision sampler use the same modified triangles. Full ledger: [site validation](../../../validation/reset-final/site-validation.json), [vegetation changes](../../../validation/reset-final/vegetation-ledger.json).

Implementation: `assets/js/floating-atlas/entry.js` selects the version; `town-reconstruction.js` loads the assets; `reconstruction-plan.js`, `reconstruction-terrain.js`, `reconstruction-geometry.js`, `reconstruction-landscape.js` and `reconstruction-review.js` contain the isolated layout, shelf, paving, vegetation and evidence controls. Exact hashes are in `validation/reset-final/implementation-hashes.json`.

The three principal composition fixes are the continuous street-to-square alignment, continuous shopfront thresholds, and coordinated terrain/forest clearance. A detached source caption was omitted beside the fountain; the original export, sculpture and basin remain unchanged. Compatible guard fittings are batched by material. No approved building geometry was altered.

## Actual gameplay and regression evidence

- **11/11 real-game checks pass:** uninterrupted arrival-to-Guild-reservation and reverse; four door approaches; jump/landing; guard; fountain; optional forest branch both ways. [Live traces](../../../validation/reset-final/live-traversal.json).
- **13/13 CPU controller cases pass**, including both 20 Hz and 60 Hz civic traversals, actual terrain and visible imported floor support. Maximum terrain/raycast error {r['maxTerrainError']:.3g} m; pavement/support error {r['maxSupportError']:.3g} m away from the original raised building thresholds. [Results](../../../validation/reset-final/controller-routes.json).
- **35 existing scoped tests pass**, covering landscape, character, experience, S2-F/G, square and circulation preservation. [Log](../../../validation/reset-final/regression.log).
- Static material batching retains all single-material and repeated-material face groups and world bounds. [Regression](../../../validation/reset-final/batch-regression.log).
- **Two exact restoration round trips pass:** every original terrain attribute, instance matrix, collider and scene-child identity. All {s['preservation']['filesChecked']} baseline files were checked; only the entry integration and asset-manifest history changed. Approved native masters, GLBs, archives and research pages retain their hashes.
- Fresh default page requests no town assets; Home/editorial/adventure, Work's six studies, `project=mbr` and the old accepted town were checked in the browser. [Navigation record](../../../validation/reset-final/navigation-checks.json).

## Measured rendering cost

Same scene and renderer, Apple M4 Pro / ANGLE Metal, 1440 × 836 drawing buffer, DPR 1, standard shadows, antialiasing, exposure 0.96, Glass B. Each matched camera rail has 2 s warmup and 12 s sampling. rAF intervals are measured frame intervals, **not GPU timing or a device-independent FPS promise**.

| Setting | Median / p95 frame ms | Draw calls, all passes | Submitted triangles, all passes |
|---|---:|---:|---:|
| Original landscape / town OFF | {off['medianMs']:.2f} / {off['p95Ms']:.2f} | {off['drawCalls'][0]}–{off['drawCalls'][1]} | {off['triangles'][0]:,}–{off['triangles'][1]:,} |
| Rebuilt town ON | {on['medianMs']:.2f} / {on['p95Ms']:.2f} | {on['drawCalls'][0]}–{on['drawCalls'][1]} | {on['triangles'][0]:,}–{on['triangles'][1]:,} |

CPU render submission ON: {on['cpuMedianMs']:.2f}/{on['cpuP95Ms']:.2f} ms median/p95. Loading cache holds {perf['town']['cache']['loadedFiles']} files, with no added requests when toggled off/on. Browser memory counters and observed resource-transfer/cache entries are retained in [performance evidence](../../../validation/reset-final/live-performance.json); source file bytes are distinct from observed transfer bytes. No browser warnings/errors were reported. Authored Glass A remains reversible; B is the measured default.

## Review limits (maximum three)

1. The optional forest branch is traversable but retains short {layout['optionalTrail']['maxGradePercent']:.1f}% pitches. It is an exploration branch, separate from the 2.03% civic route.
2. Approved Glass B remains darker and less reflective than the Blender transmission reference; lighting and architecture were preserved.
3. Guild and skyport architecture remain deliberately unbuilt. Their reservation/threshold does not establish a future building entrance or dragon landing system.

## Open and roll back

Local preview: `http://127.0.0.1:4175/index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-review=1&build=reset-final`.

- Immediate original landscape: **Town off**, or remove `dev-town=s2f` and `town-layout=reset-final` from the URL.
- Previous accepted town: remove `town-layout=reset-final` and use `dev-town=s2f&terrain-study=c1a5&town-square=c1b&circulation=c1c&town-review=1`. The two towns are mutually exclusive.
- Code checkpoint: `codex/reset-final-checkpoint` (`ff8b545ebd7c13894bf4af59fc5406ee8e1a6ada`). Restore only the entry file if code rollback is wanted; do not reset unrelated working-tree changes. Its direct backup is `validation/reset-final/entry.js.before`. Native sources are additionally preserved by SHA256.

Reproduce: run `node validation/reset-final/test-routes.mjs`, `node validation/reset-final/site-validation.mjs`, and `node validation/reset-final/batch-regression.mjs`. Use the visible review controls for the real explorer, camera presets and camera-rail measurements. `captures.json` records every final camera/settings tuple. The isolated civic derivative is `validation/reset-final/civic-reuse.blend`; it is not a new town master.

Anti-slop delivery check: **Hard gate PASS** (authorized real scene assets, native review buttons, no fabricated claims or production UI change); **Purpose PASS** (forest/stone palette retained, gold only identifies the technical primary route); **Liveliness PASS** (ENERGY 2 / RHYTHM 2 / MOTION 1, fountain focal point and varied approved roofs); **Craftsmanship PASS** (actual captures, controller tests, restoration and measured costs). This internal check does not grant owner artistic approval.
'''
d.mkdir(exist_ok=True,parents=True);(d/'REVIEW.md').write_text(text)
figs='\n'.join(f'<figure><a href="../../../validation/reset-final/{n}.png"><img src="../../../validation/reset-final/{n}.png" width="1440" height="836" alt="{title}" loading="'+('eager'if i==0 else'lazy')+'"></a><figcaption>'+str(i+1)+'. '+title+'</figcaption></figure>'for i,(n,title)in enumerate(views))
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Transit Kingdom | RESET-FINAL owner review</title><style>body{margin:0;background:#eee7d7;color:#173d36;font:16px/1.6 system-ui}main{max-width:1280px;margin:auto;padding:30px 24px 60px}h1{font:36px/1.2 Georgia,serif;margin:12px 0}p{max-width:900px}a{color:#72511f;text-underline-offset:3px}figure{margin:40px 0}img{display:block;width:100%;height:auto;background:#c9c9b0}figcaption{padding-top:10px;font-weight:600}a:focus-visible{outline:3px solid #9c7028;outline-offset:4px}</style><main><p>AR(N)AN Urban Atlas / R0-RESET-FINAL</p><h1>One street, one civic court.</h1><p>Actual local-game captures. Four approved buildings on a coordinated terrain shelf. Human visual approval is pending. No public deployment.</p><p><a href="REVIEW.md">Measurements, tests and rollback</a> · <a href="../../../validation/reset-final/captures.json">Reproducible cameras</a> · <a href="../../../validation/reset-final/walking-forward.png">Original explorer walking</a></p>'''+figs+'</main></html>'
html=html.replace('loading="eager"','loading="eager" fetchpriority="high"')
(d/'index.html').write_text(html)
print('PASS: final report, gallery and six validated image/camera records written')
