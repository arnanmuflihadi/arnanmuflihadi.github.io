# 02 — Gameplay validation with the real controller and camera

All figures from `evidence/` (scripted input at 60 Hz through the game's unmodified `player-controller.js` and `camera.js`; the preview supplies its own terrain collision). **Scripted tests, not a human playtest.**

## Routes walked (17)

| Route | Time (s) | Stuck | End error (m) | Max step up (m) | Min camera (m) | Share of samples with camera < 3 m |
|---|---|---|---|---|---|---|
| quay_to_arrival_court | 20.8 | 0 | 0.50 | 0.009 | 12.93 | 0 % |
| arrival_court_to_quay | 20.8 | 0 | 0.50 | 0.000 | 12.93 | 0 % |
| arrival_court_to_merchant_street | 25.3 | 0 | 0.48 | 0.030 | 12.93 | 0 % |
| street_to_civic_terrace | 18.7 | 0 | 0.47 | 0.220 | 12.52 | 0 % |
| hall_doors_and_forecourt | 6.1 | 0 | 0.50 | 0.000 | 1.71 | 13 % |
| hall_to_crag_stair_foot | 9.9 | 0 | 0.47 | 0.006 | 12.90 | 0 % |
| crag_ascent | 40.4 | 0 | 0.47 | 0.019 | 5.17 | 0 % |
| crag_descent | 40.4 | 0 | 0.47 | 0.002 | 2.96 | 0 % |
| hall_to_shoulder_table | 20.3 | 0 | 0.49 | 0.024 | 8.63 | 0 % |
| tea_house_to_overlook | 23.8 | 0 | 0.47 | 0.000 | 1.49 | 5 % |
| overlook_back_to_lookout | 21.1 | 0 | 0.48 | 0.110 | 12.93 | 0 % |
| service_court_to_lower_benches | 24.9 | 0 | 0.47 | 0.003 | 11.78 | 0 % |
| benches_back_to_court | 24.9 | 0 | 0.50 | 0.010 | 12.82 | 0 % |
| arrival_court_to_caravan_green | 28.9 | 0 | 0.47 | 0.000 | 11.91 | 0 % |
| caravan_green_to_arrival_court | 28.9 | 0 | 0.47 | 0.000 | 5.84 | 0 % |
| bridge_to_tea_stack | 11.8 | 0 | 0.47 | 0.020 | 12.93 | 0 % |
| bridge_back | 11.8 | 0 | 0.47 | 0.019 | 12.93 | 0 % |

Pass rule: no stuck waypoint and end within 0.6 m. **17/17 pass.** `tea_house_to_overlook` (min camera 1.49 m) and `hall_doors_and_forecourt` (1.7 m) are the tight ones: the tea-house veranda is the unsolved item of P3-A and the doors are against the hall wall, as at every door of the town.

## Reachability (A* over the real `blocked()` and support heights)

| From → to | Length (m) | Walk (s) | Run (s) |
|---|---|---|---|
| arrival court -> Exchange Hall podium | 154.213 | 73.435 | 33.524 |
| arrival court -> Caravan Green | 64.457 | 30.694 | 14.012 |
| Exchange Hall -> crag stair foot | 21.935 | 10.445 | 4.768 |
| quay -> arrival court | 38.215 | 18.198 | 8.308 |
| Exchange Hall -> crag summit (beside the Counting Stone) | 83.341 | 39.686 | 18.118 |
| Exchange Hall -> Shoulder Table | 57.121 | 27.2 | 12.418 |
| tea house veranda -> Cloudfall overlook | 47.458 | 22.599 | 10.317 |
| service court -> lower benches | 45.391 | 21.615 | 9.868 |
| overlook -> Tea Stack (bridge) | 34.8 | 16.571 | 7.565 |
| tea lookout -> Caravan Green (whole town) | 105.42 | 50.2 | 22.917 |
| quay -> Tea Stack | 158.937 | 75.684 | 34.552 |

The Caravan Green is reached **from the arrival court round the south-west of the artisan block** (64 m), not through the lane: the lane's west end is closed by B11's yard. The authored *Green road* follows that route. The Tea Stack is reached over the bridge only (the route test used 0.25 m cells because the deck's free corridor is 1.4 m wide).

## Edges, steep ground, falls

| Test | Result |
|---|---|
| Sprint at the rim from 11 starts (quay prow, Green, crag, shoulder table, benches, stack, west meadow) | all stop on the island; none left it; fall recovery was never needed |
| Walk into: tea riser, outward | ends (61.52, 46) y -4.249, stuck 0 |
| Walk into: crag face, northward | ends (30, 100.725) y 4.811, stuck 1 |
| Walk into: quay retaining wall, southward from the court | ends (-14, -26.72) y -0.365, stuck 1 |
| Walk into: hall shelf bank, northward (west of the terrace) | ends (-30, 81.51) y 2, stuck 0 |
| Placed in the void: void south of the quay | recovered in 1 step to the last safe ground [5, -52], back on support: True |
| Placed in the void: void east of the stack | recovered in 1 step to the last safe ground [5, -52], back on support: True |
| Placed in the void: void under the crag | recovered in 1 step to the last safe ground [5, -52], back on support: True |
| Placed in the void: inside the rim lip (blocked cell) | recovered in 1 step to the last safe ground [5, -52], back on support: True |
| Sprint + repeated jumps at the quay prow | left the island: False |

Method: walkability comes from `island-mask.bin` (supported, ≥ 1.2 m inside the rim, slope ≤ 0.9; or authored by the town grid). Steep ground and the rim are therefore blocked for the body even in the air, so the player cannot fall off by walking; the controller's own recovery (minY −30 m) is exercised by placing the character in the void.

## Existing town network

Batch 5's 65-edge pedestrian regression (`P.autotest('network')`, both directions): **65 edges, 0 failed, 51 nodes standable, minimum node clearance 0.409 m** — identical to the batch 5 record. Evidence `p3b-network.json` (the batch 5 `network.json` was not overwritten).

## Camera against landscape (24-yaw sweeps at 24 spots)

| Spot | Min camera (m) | Yaws < 3 m | Min character opacity |
|---|---|---|---|
| quay centre | 5.70 | 0 % | 1.00 |
| ramp head | 12.92 | 0 % | 1.00 |
| ramp middle | 12.92 | 0 % | 1.00 |
| ramp foot | 12.89 | 0 % | 1.00 |
| crag stair foot | 5.00 | 0 % | 1.00 |
| crag stair, first switchback | 12.92 | 0 % | 1.00 |
| crag mid | 6.69 | 0 % | 1.00 |
| crag upper | 2.79 | 17 % | 0.75 |
| crag summit stone | 2.92 | 4 % | 0.82 |
| shoulder table | 12.92 | 0 % | 1.00 |
| hall lawn west | 12.92 | 0 % | 1.00 |
| east of hall (shelf) | 7.24 | 0 % | 1.00 |
| behind hall (shelf) | 5.00 | 0 % | 1.00 |
| tea promenade start | 3.97 | 0 % | 1.00 |
| tea promenade middle | 12.92 | 0 % | 1.00 |
| cloudfall overlook | 12.92 | 0 % | 1.00 |
| porters loop bend | 12.92 | 0 % | 1.00 |
| lower benches | 12.92 | 0 % | 1.00 |
| caravan green | 12.92 | 0 % | 1.00 |
| artisan gate path | 12.92 | 0 % | 1.00 |
| bridge middle | 11.85 | 0 % | 1.00 |
| tea stack top | 12.92 | 0 % | 1.00 |
| east of the hall podium edge | 2.79 | 17 % | 0.75 |
| bank behind tea house | 3.01 | 0 % | 0.84 |

Tight spots: crag upper (2.79 m), crag summit by the stone (2.9 m), east edge of the podium shelf (2.79 m, a retaining bank behind the camera). All stay ≥ 2.7 m; none collapses onto the character. `VISUAL-DEFECT` candidates, not blockers.
