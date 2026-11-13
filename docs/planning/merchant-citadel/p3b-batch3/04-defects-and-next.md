# 04 — Closure of the batch 2 defect list and what is left

Numbers refer to [batch 2 doc 06](../p3b-batch2/06-defects-risks-roadmap.md).

| # | Defect | Status after batch 3 |
|---|---|---|
| 5 | Clouds read as ice shards; Cloudfall one thin sheet | **Improved**: soft puffs; layered fall with spray; bank planting and lip stones. Open: carved lip pool/ledge (terrain change), fall volume from below is still thin |
| 6 | Soft paths, smeared tea soil | **Closed** (ground map) |
| 7 | Tea rows are `Bush_Common` | open (no tea plant model) |
| 8 | Cliff and underside procedural shell; smooth crag dome | **Improved** (74 rock masses; crag: shader strata, 23 outcrops, 9 dead trees, scree); cliff-top strata geometry open |
| 9 | Tea-house veranda camera 1.49 m | **Open**, cause `UNVERIFIED`; recovers within 3.6 s |
| 10 | Leaf cards faceted, tint multipliers | **Improved**: table removed (global grade + variation + wind); one mask-texture fix remains; cost 0-1 ms |
| 1 (animals) | small animals read as specks | **Partly**: soft lift and contact blobs; still small at the 11.8 m camera |
| 4 (animals) | foot sliding unmeasured | **Measured**: 0.47-1.0 of body speed, not fixable by rate (needs IK) |
| 11 | Sky Quay lightly dressed | open |

## Next steps that this batch does not authorise

WP6 (flora spatial cells, second shadow cascade near the player, WebP/KTX2 test, throttled-profile timing) and WP8 (production proposals and patch files for collision/bounds, the town corrections and the asset register). Candidates for a further visual pass: a carved Cloudfall pool (terrain edit with route re-test), IK for animals, a cheaper wind (vertex wind only within 36 m), `?tm=aces` check of the foliage grade.
