# 02 — Validation (scripted, real preview; not a human playtest)

Data: `evidence/validation/` (`p3b3-*.json`, `autotest-network-p3b3.json`). Production modules (controller, camera, character, input, collision, vendored three) untouched.

| Check | Result |
|---|---|
| 17 landscape routes | 17/17: 0 stuck, end error 0.466-0.500 m (limit 0.6); minimum camera: tea_house_to_overlook 1.49 m, hall_doors_and_forecourt 1.71 m, crag_descent 2.96 m, others >= 5.1 m (identical to batch 2) |
| Reachability pairs | 11/11 found |
| Town pedestrian network | 65 edges tested, 0 failed, minimum node clearance 0.409 m |
| Rim / edge walks, fall recovery, jump at prow | 11 edge walks on the island, 0 recoveries |
| Camera spots (24) | minimum 2.789 m (crag upper), 2.793 (podium edge), 2.92 (summit); alpha >= 0.75; nothing collapses |
| Wildlife simulation 600 s | zero violations (not walkable, solids, keep-outs, step, slope, ground error, outside habitat); largest height step 0.096 m; relocations 0 |
| Wildlife spawn | 27/27 ground agents legal, min solid clearance 0.97 m, 0 in keep-outs, 20 birds / 18 butterflies |
| Reactions | alert 2.98-13.9 m, flee 1.7-9.9 m; pug and dog calm; all end positions legal |
| Songbird cycle | perch > takeoff > fly > land > perch, 0 m landing error, 4 habitats |
| `dragonNear` stub | 6 animals within 12 m of a horse switched to FLEE (hook only; no dragon exists) |
| Console | no errors or warnings in the final build |

## Foot slide (`p3b3-foot-slide.json`)

Method: a clone moves at the species walk (or flee) speed with the clip rate swept 0.4-3.0; the four low bones with the largest fore-aft travel are the feet (named `FrontFootR` etc. on the farm rigs and the pug; generic bone numbers on cat, dog, fox, chick, where the choice is a guess); slide = mean horizontal speed of a foot while it is within 4 % of body height of its floor, as a fraction of the body speed (0 = planted).

| Species | walk: current rate / best possible | run: current / best |
|---|---|---|
| Sheep, Lamb, Cow, Horse, Llama, Pig | 0.75-0.79 / 0.75-0.77 | 0.50-0.60 / 0.47-0.56 |
| Pug | 0.89 / 0.75 | 0.76 / 0.47 |
| Dog, Cat, Red fox, Chick | 1.0-1.09 / 1.0 | 1.0-1.05 / 1.0 |

**Finding:** the farm clips swing the leg forward and then hold the foot still relative to the body (no backward stance sweep), so a stance foot slides at about the body speed whatever the clip rate: the best achievable value is 0.47-0.77, far above the target of 0.15. Cat, dog, fox and chick measure about 1.0 (feet not identified reliably or clips without any foot travel). The clip-rate estimates (`cs`, `csr`) were therefore **not** changed. Real fixes: IK foot planting or root-motion-aware clips (backlog).
