# 04 — The selected island: measured masterplan, integration and gameplay

Design name: **Terraced Merchant Highlands with the Tea Stack**. All figures are from `evidence/island-measurements.json` (computed from the shape file and the real building envelopes) or from the shape file itself. Plan: `visuals/plans/plan-S.jpg`. Views: `visuals/selected/` (Blender massing). One spatial arrangement is used in every image. **No building is moved, rotated or changed.**

## 1. Identity

A tilted table of pale, banded rock (cream limestone with ochre and terracotta-red layers, echoing the town's plaster and roofs) that reads from afar as a laden merchant ship: a low **quay prow** to the south, the town amidships, a wooded **crag** as the stern castle behind the Exchange Hall, and a **keel** of dark rock beneath, deepest under the crag. Water rises at the crag, runs through the tea benches and leaves the island as the **Cloudfall**. It is not the first island's landscape: different silhouette, different rock, a planted working slope instead of wild highland.

## 2. Measured facts

| Item | Value |
|---|---|
| Size | 178 m east–west × 216 m north–south (rim x −81…97, n −80…136) |
| Top area | 26,203 m² with the stack; the town's built extent covers 27 % |
| Rim length | 678 m |
| Terrain top | −8.7 m (lowest tea bench) … +23.7 m (crag); town datum 0 |
| Cliff band, underside | 23 m of strata, then the keel: 48 m below the rim under the quay, 94 m under the crag |
| Overall height, crag top to keel | about 118 m |
| Closest building to the rim | 18.5 m (E01's south-west corner); the contract asks for ≥ 6 m |
| N20 (0, −16) | on the arrival court at datum, 61.6 m from the rim along the quay |
| Near-level ground (slope under ~7°) | 18,575 m² |

## 3. The parts (plan coordinates)

| Part | Where | Levels | Purpose |
|---|---|---|---|
| **Sky Quay** | prow, n −32…−80, about 45 m wide | −3.0 m | arrival, future transport berth, landing zone; a 14 m wide stair of ten 0.3 m risers on the town axis (n −31…−25) climbs to the arrival court. From the quay the hall tower is visible through the gateway gap (`v3`) |
| **Arrival court and N20** | n −24…−8 | 0 | unchanged town datum; N20 stays the transport interface at street level, 8 m north of the stair head |
| **Hall shelf** | beside and behind the hall, n ≥ 76, x ±50 | +2.0 m | removes the podium's three 2 m drops (02); the bank rises between n 73.2 and 76, clear of B15, B16 and the tea house (all end at n ≤ 72.3) |
| **Counting Crag** | north-east, peak near (40, 116) | to +23.7 m in 3.6 m rock benches | the hall's backdrop, **offset east so the tower keeps open sky** (`v4`: tower 26.8 m against sky, crag to its right); summit viewpoint over the whole town (`v8`); source of the stream |
| **Shoulder Table** | north-west, (−36, 112) | flat at +9.1 m | lower counterweight to the crag; a landing table |
| **Tea benches** | east, x 47…95, n 0…88 | five 6.5 m benches stepping 1.7 m each, to −8.5 m | the tea house's reason: rows follow the contours round the lookout; the east rim is 8 m lower than the town, so the lookout looks **over** it (`v5`) |
| **Stream and Cloudfall** | spring (36, 104) → (88, 64), 69 m | falls 30 m (massing value) off the east cliff | drainage feature, sound source, landmark from the east approach |
| **Tea Stack** | (111, 45), about 22 m across | −5.0 m, pavilion on top | focal point of the lookout panorama; optional rope-bridge reward |
| **Caravan Green** | west, centre (−50, 18) | 0 | open common west of the artisan lane: fairground, main dragon landing |
| **Fractures** | notches at bearings 12°, 154°, 238° | — | break the rim; floating debris; the 12° notch frames the Cloudfall |

## 4. Town–terrain integration (each built edge and what meets it)

| Built edge | Today | Selected design |
|---|---|---|
| South: E01/E02 gateway, arrival court | cobble field on a plane | quay stair and retaining bank; gateway seen from below with the tower on the axis |
| West: backs of B10–B12, E03, E07 | open plane | garden strip, then the Caravan Green; trail from the artisan lane gate (−24, 20) |
| North: hall podium | 2 m slab edges, sky | hall shelf at podium level, then crag and wood |
| North-east: tea house (B17) | fence, plane | bank behind, stream beyond, benches east |
| East: lookout terrace, E05, porters' path | fence, plane | the first bench drop is about 6 m beyond the paving (x 48); a porters' loop leaves the service court's east opening and climbs through the lower benches to the promenade |
| South-east: B13 warehouse south side | plane | lowest bench end and a small wood |

Clearances: all 28 building entries stand on the flat pad or the shelf and the paving is untouched. **One deliberate deviation from batch 5's contract** ("nothing rises within 6 m of a tower's walls"): the 2 m shelf bank begins 1.1 m north of B15 and B16 and 0.9 m north of the tea house. It is a low bank (or a retaining wall, P3-B's choice), not a cliff; if that is too close, the bank can start at n 76 only east and west of x ±26. Otherwise the lookout's sightline to the terrace is unaffected (terrain there stays at datum).

## 5. Routes and viewpoints

| Trail | Length | Walk / run |
|---|---|---|
| Gateway to the quay centre | 50 m | 24 s / 11 s |
| Tea lookout to the Cloudfall overlook (80, 54) | 39 m | 18 s / 8 s |
| Hall (east side) up the crag stair to the Counting Stone | 39 m (about 22 m of climb) | 18 s / 8 s on the flat; the climb will be slower |
| Service court through the lower benches to the promenade | 53 m | 25 s / 11 s |
| Hall (west side) to the Shoulder Table | 20 m | 9 s / 4 s |
| Artisan gate to the Caravan Green | 12 m | 6 s / 3 s |

Loops this creates: quay → street → hall → crag → stream → Cloudfall → lookout → bazaar; and court → benches → promenade → lookout. Each optional branch ends in a reward (view, pavilion, summit). From every fork the next destination is in view in the massing images; that is `UNVERIFIED` from the gameplay camera.

Viewpoints: Tea lookout (36, 57), Cloudfall overlook (80, 54), Counting Stone (40, 116), Sky Quay prow (0, −70), Tea Stack (111, 45).

## 6. Edge safety, collision and camera

* The town's streets and buildings stay at least 18 m from the rim; the player reaches an edge only by design, at the quay, the overlook and the stack bridge. Rim treatment: a 0.6 m rock lip everywhere (in the massing), rails at the quay edge, the overlook and the stack bridge, hedges along the bench ends. Optional risky edges (bench ends, the crag's north side) stay optional.
* Bench risers are 1.7 m (not jumpable, apex 1.17 m): descents are by the promenade and the porters' loop only, so benches cannot be used to skip to the rim.
* The stair on the axis is 0.3 m per riser (max step 0.42 m).
* Camera: the crag, the bank behind the tea house and the bench risers will collide with the follow camera through `heightAt`; expected tight spots are the foot of the crag stair and the promenade under the first riser. **Not tested: terrain is not in the browser.**

## 7. Dragon flight and landing (design intent only; no dragon code touched)

Landing is not one platform. Four open surfaces pass the concept criteria (flat within 0.6 m, at least 8 m from the disc to the rim and to any building; trees excluded by the generator):

| Zone | Centre | Radius | Level | Height range | To rim | To building |
|---|---|---|---|---|---|---|
| Caravan Green | (−50, 18) | 14 m | 0 | 0.36 m | 11.9 m | 10.2 m |
| Sky Quay | (5, −52) | 11 m | −3.0 | 0.0 m | 17.2 m | 34.2 m |
| Shoulder Table | (−36, 112) | 6 m | +9.1 | 0.19 m | 12.0 m | 30.3 m |
| Hall lawn (west) | (−32.5, 85) | 7.5 m | +1.9 | 0.20 m | 34.3 m | 8.3 m |

Not landing zones by design: roofs, the tea benches (1.7 m steps), the crag's benches, the stack, cliffs, streets. Approaches: from the south-west the quay and green are open with the hall tower as the aiming mark (`v6`); from the east the Cloudfall and stack mark the island (`v6b`). **These criteria are mine.** The game's dynamic landing system has its own rules, which I did not evaluate; the surfaces are sized to give it room.

## 8. Provisional rubric for the concept (Blender massing; browser `UNVERIFIED`)

| Domain | Score | Evidence |
|---|---|---|
| World composition | 4 | distinct silhouette from four directions (`v1`, `v2`, `v6`, `v6b`); hall + crag hierarchy (`v4`) |
| Environment | 3 (massing) | parts are right; rock, foliage and water quality do not exist yet |
| Town integration | 4 | every built edge has an answer (section 4) |
| Character and camera, rendering, gameplay readability | `UNVERIFIED` | nothing is in the browser |

Three largest weaknesses of the concept as drawn: (1) the Sky Quay is a large blank apron and needs cranes, cargo and berths to read as a harbour (`v3b`); (2) the Caravan Green is a big empty lawn without edges at player height (`v9`); (3) the underside is smooth and bulbous in the middle and needs faceted rock work (`v2`).
