# Merchant Citadel P3-B batch 2 — living floating island: third-party flora, wildlife, landscape art direction

**Status: ready for human visual review. Nothing committed or deployed. Not approved.** Executor: Claude Sonnet 5.5. Baseline: P3-B batch 1 island, P2-B batch 5 town (24 buildings unchanged), P3-A concept.

## Try it

```bash
node merchant-citadel-p2a/server.mjs --port 4180
```
`http://127.0.0.1:4180/merchant-citadel-p2a/index.html` — island, corrections, flora and wildlife on. Flags: `?flora=0` (batch 1 procedural scenery), `?wild=0` (no animals), `?wscale=1.3` (animals 30 % larger, review knob), `?island=0`, `?fixes=0`. WASD, Shift, Space, Q/R. Walk up to animals: they notice, flee and come back.

## What changed

* **Real flora**: Quaternius Stylized Nature MegaKit (free Standard tier, CC0, 68 of 116 models): 33 models adapted (textures 2048 -> 512-1024, normal maps dropped, tree L1 decimation) into a 10.9 MB library; 1,651 instances placed by a seeded scatter with groves, understory, meadow flowers, boulder fields, 121 ledge outcrops, path pebbles, stream-bank plants; tea terraces replanted as contour rows; Cloudfall mist and foam; clouds from Gobkit.
* **Wildlife (Quaternius-only after owner decision D1, see [08](08-animal-source-change.md))**: Quaternius farm / animal packs (CC0, rigged, real Idle/Walk/Run/Flying/flap clips) at natural size: cow, horse, llama, pig, pug, sheep + lamb, dog, cat, red fox, chick, songbird, eagle; 65 agents in 7 habitats (settlement, Caravan Green, Counting Crag, tea terraces, Cloudfall, lookout/stack, Sky Quay) with state machines, player reactions, terrain/obstacle/slope validation, per-animal wall margins, dragon-landing keep-outs, perch-to-perch songbird flight and eagle soaring with the real clips; the Gobkit swallowtail is the only butterfly (kept). The first Gobkit version (27 species, 83 agents) is archived under `superseded-gobkit/`.
* **Not touched**: terrain, collision data, buildings, kit, `scene.json`, the six production files (SHA-256 verified).

## Results (scripted, real preview)

* Town/landscape regression (run in the Gobkit stage, **not re-run for the animal swap**: terrain, collision, town and flora data unchanged and animals are not obstacles): 17/17 routes, 11/11 reachability, **65/65 town edges** (clearance 0.409 m as before), rim and fall tests as batch 1, camera spots >= 2.79 m.
* Wildlife (**re-run on the final Quaternius code**): 600 s full-rate simulation with **zero** violations (walkability, solids, keep-outs, slope, habitat); spawn validity 27/27 ground agents (min clearance 0.49 m); reactions per species (alert 2.9-13.9 m, flee 1.8-9.9 m; pug and dog calm), 0 trapped, relocation fallback 0; songbird PERCHED > TAKEOFF > FLY > LAND > PERCHED landing exactly on target in 4 habitats; eagles circle at 35-40 m.
* Performance (1280 x 720, GPU-complete, load about 5.6, re-measured): 3.3-11.7 ms p50 across the 9 cameras (all layers on: 6.0-11.7); 0.5-1.3 M triangles; wildlife 0.19 ms CPU per frame (65 agents); flora textures about 35 MB; animals 2.7 MB on disk.
* Bugs found and fixed while doing the swap: wrong grazing pitch sign on these rigs, a fixed 0.28 m wall margin too small for large animals, a single shared perch for the tea-terrace and Cloudfall birds, a demo helper that deleted a real agent. Earlier: animals spawned inside boulders; a bird perched in the landing zone; leaves rendered white because the twisted-tree leaf texture is a mask.

## Read

| | |
|---|---|
| [01](01-assets-research-and-licences.md) | sources, what could and could not be fetched, licences, verification findings |
| [02](02-landscape-and-flora.md) | pipeline, placement rules, tea terraces, crag, Cloudfall |
| [03](03-wildlife-system.md) | habitats, species, clip aliases, state machines, dragon coexistence |
| [04](04-validation.md) | tests and results |
| [05](05-performance.md) | measurements and limits |
| [06](06-defects-risks-roadmap.md) | defects, risks, roadmap for further islands |
| [07](07-polish-plan-batch3.md) | proposed polish batch (plan only, not started; D1 is resolved, D2 and D3 still open) |
| [08](08-animal-source-change.md) | animal source change to Quaternius-only: sources, what changed, limits |

`evidence/asset-register-batch2.csv` (145 rows), `evidence/inspect-*.json`, `evidence/validation/`, `evidence/scatter-report.json`. Visuals: `visuals/compare/` (batch 1 browser | batch 2 Blender | batch 2 browser, 8 views), `visuals/quaternius/wildlife/` (16 stills + contact sheet), `visuals/quaternius/gameplay/` (follow-camera encounters, standard and close), `visuals/quaternius/gifs/` (5 behaviour GIFs + strips: horse flee, fox flee, sheep graze, songbird flight, eagle circle), `visuals/quaternius/animation-sheets/` (clip phases, graze pose check), `visuals/superseded-gobkit/` (first version's stills, encounters, GIFs and sheets), `visuals/animation-sheets/` (none left at top level) and `visuals/inspection/` (animal and flora sheets), `visuals/browser/`, `visuals/blender/`.

## The brief's 12 required views

1 whole island: `compare-aerial` · 2 town with vegetation: `compare-town-vegetation` · 3 Caravan Green with grazing animals: `compare-caravan-green`, `quaternius/wildlife/p3b-q-wild-sheep.jpg`, `quaternius/gameplay/p3b-q-encounter-green-*.jpg` · 4 Counting Crag: `compare-crag`, `quaternius/wildlife/p3b-q-wild-redfox.jpg`, `quaternius/gifs/strip-eagle-circle.jpg` · 5 tea terraces: `compare-tea-terraces`, `quaternius/gameplay/p3b-q-encounter-terrace-llama.jpg` · 6 Cloudfall: `compare-cloudfall` · 7 Tea Lookout: `browser/p3b-b2-v5-tea-lookout.jpg` · 8 Sky Quay: `compare-sky-quay` · 9 animal contact sheets: `quaternius/wildlife/wildlife-contact-sheet.jpg`, `quaternius/animation-sheets/` · 10 player-height encounters: `quaternius/gameplay/` · 11 behaviour demonstration: `quaternius/gifs/wildlife-*.gif` · 12 distant aerial: `browser/p3b-b2-v6-dragon-approach.jpg`, `...v6b...`.

## Files (isolated preview; production modules untouched)

New: `merchant-citadel-p2a/flora.js`, `wildlife.js`, `p3b2-tests.js`, `assets-p3b2/{flora.glb, fauna-q/ (13 Quaternius animals), fauna/ (Swallowtail only), env/}`, `data/island-flora.json`. Edited: `island.js` (flora hook, clouds, Cloudfall effects), `p2a.js` (wildlife hook), `p3b-tests.js` unchanged. Batch 1 baseline copies remain in `baseline-p3b-batch1/`.

## Not verified / limits

The 8 `visuals/compare/` sheets were taken in the Gobkit stage (animals are barely visible at those cameras) and were **not recaptured**. Small animals are specks at the follow camera (see 06 #1). No human playtest. No lower-end device, phone or other browser. Foot sliding unmeasured. The dragon controller does not exist, so dragon coexistence is by keep-outs only. Blender renders show the same GLBs and placement but not the browser's detail shader or animals. Quality statements are provisional internal observations; **owner approval pending**.

Rebuild: `bash docs/planning/merchant-citadel/p3b-batch2/source/build_all.sh` (needs the free Standard pack unzipped at `$NATURE`).
