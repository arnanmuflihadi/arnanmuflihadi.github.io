# Corrected pedestrian-network specification (P2-A closeout)

Machine-readable: [pedestrian-network-p2a.json](pedestrian-network-p2a.json), [nodes.csv](pedestrian-network-p2a-nodes.csv), [edges.csv](pedestrian-network-p2a-edges.csv). Source of the numbers: `merchant-citadel-p2a/evidence/network.json` (test `?autotest=network`).

## Method

* Slice nodes = the P1.4 nodes inside the built area of the slice (28). Nodes inside buildings the slice does not contain (market halls N18/N19/N31/N32, workyard N40, service court N33, reservation N20) are excluded; they are P2-B work.
* **Every edge between two slice nodes (34) is walked in both directions** with the unmodified player controller and the real collision proxies: 60 Hz autopilot, W held, walking speed 2.1 m/s, body radius 0.34 m, straight node-to-node line or the listed via-points. An edge passes when no stuck state occurs (no progress for 2 s) and the player ends within 0.6 m of the target node.
* Each node is tested for standability (not blocked) and its clearance to the nearest solid proxy (distance minus body radius).
* The 0.42 m arrival-error figures in the CSV are the autopilot's stop radius (0.45 m), not a position error.

## Result

**28 / 28 nodes standable, 34 / 34 edges pass in both directions, 0 stuck states.** Smallest node clearance 0.41 m (N17). Smallest edge side clearance 0.30 m (N16–N17, between two veranda posts).

## Corrections to the P1.4 network

| Item | P1.4 / P2-A | Closeout | Why (measured) |
|---|---|---|---|
| **N17** Tea house veranda | (37.6, 62.6) | **(36.16, 62.24)** | The old point is 0.55 m from the porch post at (37.06, 62.53): not standable for a 0.34 m body (P2-A: stuck on arrival and on leaving). The new point is the centre of the 1.49 m clear gap between the first two posts (35.26/37.06). The post layout was **not** changed: the gap is 1.49 m clear, 0.81 m of slack, and the posts come from the kit modules. Both directions, an in-place 360° turn (camera sweep) and oblique approaches from SSW (27° from north) and SSE (29°) pass. A much shallower approach (55° from north, aimed past post 1) slides into the post and stalls: the veranda is entered from the front, as designed |
| **B04–B05 cross street** (n ≈ 20) | wall gap 3.0 m at the turret, centre n 20.5; roof-eave gap 1.34 m | **B04 moved 1.2 m south**; wall gap **4.2 m** at the turret, centre **n 19.9** (N03 is at n 20), roof-eave gap 2.54 m | The P2-A statement "1.34 m alley" was the **roof-eave envelope** gap, not the walkable width (walls were 3.0 m apart). The real defects: the A11 turret projects to n 19, so the street centre was 0.5 m off N03's line and the route brushed the turret (stuck at (−8.4, 19.3)); and the eaves nearly touched overhead. The 4 m street of the masterplan is restored and kept open (permeable) rather than closed |
| **Market cross** (M01) | node pair N29/N30 at x = ±2.7, edges straight | cross **kept at (0, 49)**; **N29/N30 at x = ±2.9** with via-points | Clear width each side of the 2 m cross is **3.85 m** (cross edge x = ±1.0 to the awning-row posts at x = ±4.85); both passages exist in P1.4 already. A straight line along x = 0 is blocked by design (test `street_axis_straight_through_cross` documents it). The straight N05→N29 chord passed 0.485 m from the cross corner, so the edges are now polylines through (±2.9, 46.4) and (±2.9, 51.6): clearance ≥ 1.56 m |
| **N23–N06, N24–N06** | straight | via (∓7.5, 60.3) | The straight line passed 0.18 m from an awning-row post; the via-point gives 1.03 m |
| Spawn of the preview | z = +4 (n = −4) | z = −4 (n = +4) | A sign error in the preview, unrelated to the plan |

## Tightest places remaining (all pass; recorded so P2-B does not narrow them)

| Edge / node | Side clearance m | Against |
|---|---|---|
| N16 ↔ N17 (veranda gap) | 0.30 | B17 posts |
| N05/N30 ↔ N29/N27 (round the cross) | ≥ 1.56 (was 0.485) | M01 |
| N38 ↔ N23 (inn lane) | 0.86 | E03 posts |
| N04 ↔ N14 | 0.87 | B09 wall |
| N11 ↔ N04 | 1.07 | dressing |

## Rules the network now follows (carry to P2-B)

1. Walk-through width between solids ≥ 1.5 m clear (0.68 m body + margin); the tea-house veranda gap (1.49 m) is the only place just under it and is a threshold, not a street.
2. A node is placed at the **centre of the free span**, measured on the collision proxies, not on the plan footprint; footprints exclude eaves, turrets and posts.
3. An edge that passes within 0.5 m of a solid gets a via-point; the straight chord is not the route.
4. Centre-lines of streets agree with the junction nodes to within 0.1 m (N03 / B04 / B05).
5. Verify with the real controller, both directions, after every layout change.
