# Transit Kingdom: curated prop population

**Locally playable; owner visual approval pending. No deployment.** [Before/after gallery](index.html) · [Play](../../../index.html?experience=adventure&dev-town=s2f&town-layout=reset-final&town-review=1&town-props=cc0&build=population-final).

The accepted settlement is unchanged. Added **17 imported CC0 model types, 42 placements**, including three reused Quaternius ferns. Nine selected Kenney furniture models and seven food models supply café tables/chairs, a book counter, stools, deliveries, ceramic pots, a bench and table settings. Existing lamps, fountain, pavilion and wayfinding remain. The Guild is still only its reservation noticeboard.

## Evidence and corrections

Five matched actual-game pairs: [street](../../../validation/town-population/01-market-after.png), [café](../../../validation/town-population/02-kopi-after.png), [square](../../../validation/town-population/03-square-after.png), [Guild approach](../../../validation/town-population/04-guild-after.png), [aerial](../../../validation/town-population/05-aerial-after.png). [Actual explorer](../../../validation/town-population/06-traversal.png). Each PNG has matching camera/settings JSON; [pair index](../../../validation/town-population/captures.json).

Pedestrian views use eye height **1.65 m above existing support**, FOV 60°. Aerial FOV 48°. Available game buffer **1280×656**, DPR 1, below the site header. Standard shadows, exposure 0.96, Glass B and the original daylight are identical. Existing clouds/foliage remain animated. No generated illustrations, relighting or concealed geometry.

Corrected the three main findings: moved furniture off existing planted strips onto the paving edge; moved square seating clear of Serambi's door; rejected indoor floor lamps. Internal review finds the café frontage richer and the civic axis still clear. These observations are not owner approval.

## Measured cost

| Measure | Props OFF | Props ON |
|---|---:|---:|
| Camera-rail rAF median / p95 | 5.70 / 11.20 ms | 5.70 / 11.20 ms |
| CPU render submission median / p95 | 0.90 / 1.20 ms | 1.00 / 1.20 ms |
| All-pass draw calls across rail | 259–311 | 296–365 |
| Submitted triangles across rail | 2,492,070–2,554,044 | 2,501,014–2,564,356 |
| Samples | 1,538 | 1,543 |

Same 12-second arrival-to-fountain camera rail after 2-second warmup, Apple M4 Pro / ANGLE Metal. Frame intervals are not GPU timings or a general FPS promise. [Raw live evidence](../../../validation/town-population/live-evidence.json).

At the exact Market Street capture: **+43 calls / +9,778 submitted triangles**; aerial **+54 / +10,312**. [Five view deltas](../../../validation/town-population/comparison-metrics.json). Added potential geometry **5,156 triangles**, 27 instanced geometry/material batches, nine materials including the reused fern material, and one new embedded food atlas. Whole warm scene: 239 GPU geometry records, 21 textures, 39 programs; GPU byte allocation unavailable.

New GLB **117,052 bytes**. Browser warm reload recorded **300 transfer bytes** (revalidation), with encoded/decoded body **117,052 bytes**; cold transfer was not captured. One cached props GLB, eight total model-library files versus seven without the flag. Original acquisition ZIPs total **9,736,999 bytes**, separate from game delivery.

## Gameplay and preservation

Original animated controller: **11/11 live cases pass**: forward/reverse civic spine (**44.30 / 44.31 m**, about 21.16 s each), four doors, jump/landing, guard, fountain and highland both ways. Main walk median/p95 **5.6 / 11.2 ms** forward and **5.6 / 11.1 ms** reverse. [Live traces](../../../validation/town-population/live-evidence.json).

**13/13 CPU route/collision cases** at 20/60 Hz and **13/13 scoped regression tests** pass. [Controller results](../../../validation/town-population/controller-routes.json), [regression output](../../../validation/town-population/regression.log). CPU geometry fixtures omit textures; actual browser loading confirms no missing textures or current errors/warnings.

**62 frozen checkpoint files and five approved GLBs remain identical.** Only the additive entry hook, optional library catalog, local review controls and appended asset manifest changed among baseline files. Terrain, vegetation composition, paving, source GLBs and building coordinates were not edited. [Preservation](../../../validation/town-population/preservation.json). One renderer/scene is retained. Disabling the town removes props/colliders and restores the original terrain; re-enabling restores both in the same scene. [Rollback evidence](../../../validation/town-population/rollback-live.json). A flagless fresh load requests no prop GLB. Editorial, Work, six studies and `project=mbr` were checked separately.

## Rollback

Remove **`town-props=cc0`** from the URL and reload to restore the accepted settlement without any prop request. “Props off” previews the same restoration while keeping loaded resources cached. Removing `dev-town` restores the public/default landscape. Public origins cannot activate this layer.

Exact source backups: `validation/town-population/baseline/{entry.js,town-reconstruction.js,reconstruction-review.js,ASSET_MANIFEST.md}`. Accepted rollback ref: `codex/accepted-settlement-baseline`, commit `ebdd7964aa1e981c4642b52307c18927e9b1c503`. Do not restore unrelated dirty working files.

## Remaining observations

No new critical blocker found. The existing camera tightens to about **1.57–1.60 m** near doors; existing grass at some outer paving edges remains untouched. Props are static scenery, with no new interactions or NPC behavior. Stop for owner visual review.

[Asset inventory](ASSET-INVENTORY.csv) · [Source licenses and hashes](ASSET-RECORD.md) · [Placement ledger](../../../validation/town-population/placement-ledger.json).
