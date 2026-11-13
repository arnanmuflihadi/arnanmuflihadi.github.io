# S2-E — Terrain and pedestrian interfaces

**Recommended concept: the hybrid. Human design approval is pending. Nothing is deployed.** The four buildings, their floors and the approved 10,007,904-byte GLB are unchanged. The actual R0-A3 terrain, original island vegetation, lighting, portfolio and player systems remain intact.

[Isolated browser overlay](../../../validation/market-street-s2e/index.html) · [Native Blender master](../../../validation/market-street-s2e/site-interface.blend) · [Visual gallery](index.html) · [Validation record](../../../validation/market-street-s2e/validation.json)

## Alternatives and recommendation

All options use the actual terrain, the same buildings, common pedestrian geometry, materials, lighting and comparison cameras. Native Blender and browser comparisons are real captures, not generated illustrations.

| Foundation | Added foundation geometry / bytes | Site and visual implications |
|---|---:|---|
| A — terraced stone bases | 2,448 triangles / 134,276 B | Continuous retaining tiers support the buildings but dominate the slope. A 16×16 sample integration estimates about **920 m³ of fill inside the four body footprints alone**; outer tiers add more. This is a game-design estimate, not an engineering quantity. Broad stone bases leave less natural ground and flexibility. |
| B — braced supports | 1,956 triangles / 107,748 B | Stone footings, timber columns, floor bearers and metal cross-bracing preserve the landform. Lowest geometry cost and flexible future height adaptation; its exposed structural rhythm is comparatively utilitarian. |
| **Hybrid — selected** | **7,248 triangles / 543,452 B** | Uses B's open structure on the steep slopes, short stone infill at shallow gaps, planted retaining toes and sixteen reused ferns. Better transition into the approved timber/plaster architecture while retaining the natural slope. |

The shared arrivals, stairs, ramp, guards, bearers and planting interfaces add **8,404 triangles / 527,172 B**. Selected visible total: **15,652 triangles, 13 GLB primitives, 1,070,624 bytes**. A separate **100-triangle / 6,164-byte** collision-support reference is invisible. The 26,416-triangle terrain-reference GLB is used for Blender authoring only; the browser reuses the existing world instead of drawing another island surface.

Geometry files: [shared interfaces](../../../validation/market-street-s2e/common-interface.glb), [selected hybrid foundations](../../../validation/market-street-s2e/foundation-hybrid.glb), [collision support reference](../../../validation/market-street-s2e/support-reference.glb). These remain isolated S2-E deliverables.

The original 5.95 / 4.31 / 7.38 / 6.35 m floor-to-ground requirements remain numerically unchanged. The proposal spans them with visible grounded structure instead of flattening terrain or pretending the floors moved. Bearing grids adapt to the slope; high ground may meet the base directly. All **113 selected footing records** have terrain-scribed corners embedded at least 0.20 m in the sampled surface. Beams connect to the existing floor undersides, with bracing on tall bays. Low retaining edges are localized; there is no island-wide platform.

## Coherent pedestrian connection

Natural ground `(24,66)` → shallow arrival stairs → small provisional skyport threshold → bridge/garden path → existing Market Street stairs → square threshold stairs → natural ground `(36,0)`.

- The **3.6×3.6 m landing** is an interface test, not skyport architecture. Access starts on actual natural ground. Thirteen approach risers are about **0.1672 m**, terminating at the landing edge `(27,61.8)` before continuing to the reserved deck centre `(27,60)` at Y=17.15.
- The verified connector is extended with an overlap at the garden-path seam: drawn bridge length about **8.78 m**, rise 0.292 m, roughly **3.32%**. The original 8.54 m connector remains the alignment reference. The existing garden path receives a visible bearing deck and a continuous support collar.
- Market Street's approved 36 m / 4 m-rise architecture and paving remain. Its risers reach **0.1743 m**; a dedicated support reference follows the actual step profile and fills tiny contact-sampling seams within the existing physical paving.
- **Eleven new 0.1690 m risers** replace the former 0.89 m square-edge drop, followed by a small terrain-matched landing. No full Town Square is constructed.
- A **2.4 m nominal-width garden ramp** provides a second square connection. It is a steep controller-compatible game route, with an approximately 18.8% maximum designed segment and a small threshold; it is not presented as a wheelchair-access route. It bypasses the square stairs, not all market stairs.
- Rails protect exposed arrival/stair edges and gaps between storefronts. Junction rails stop before the shared landing so they do not block return movement. The original shopfront geometry stays open to the public realm; interior gameplay is outside this study.

Nominal deck widths: approach stairs 3.2 m, bridge 3.0 m, garden path 2.8 m, square stair 4.4 m and ramp 2.4 m. Between the modeled guard proxies these provide roughly 2.92 / 2.72 / 2.52 / 4.12 / 2.12 m physical clear width respectively. The capsule is 0.68 m wide and 1.9 m high; snap limit is 0.42 m. The existing controller is used unchanged.

Four **standalone showcase canopy instances** receive vertical terrain alignment in the S2-E proposal. This removes the tall tree-pedestal artifacts inherited from flat-showcase grading. Original GLB bytes and all four building transforms stay unchanged; the overlay adjusts only those four instance transforms. The original island's trees are untouched. The raised plaza focal tree and integrated planters retain their intended supports. This alignment is recorded in `site-manifest.json` and in the preview's visible diagnostics.

## Actual route and movement results

| Test | Fresh result |
|---|---|
| Ground → landing → market → square | **PASS:** 69.36 m, 33.11 s, no large foot/support discontinuities |
| Complete return to natural arrival | **PASS:** 69.35 m, 33.11 s, no large discontinuities |
| Square ramp out / return | **PASS:** 16.75 / 16.76 m including the apron approach, about 8.09 s each |
| Running return | **PASS:** 15.18 s |
| Jump on the street | **PASS:** one actual jump and landing, 1.164 m peak foot clearance |
| Walking against exposed-edge guard | **PASS:** stops at X≈40.650, Z=39 while remaining on paving |
| Fixed-step route/seam tests | **12/12 PASS:** main and ramp, both directions, at 20/30/60 Hz |

The fixed-step results are simulations using the real controller, not frame-performance timings. Animated walks use the original explorer, movement, animation and follow camera with real frame delta. Supports are exported surface triangles, exact stair references and actual terrain; guard/obstacle proxies match the visible geometry. Success was not inferred from AABB clearance alone. The public routes are tested; arbitrary travel under buildings and full production collider coverage are not certified by these tests.

First-pass failures are retained in the validation directory. Corrections moved the approach stair to the landing edge and opened the stair/ramp merge, resolving both blocked directions. The original below-terrain inspection camera was replaced with a terrain-verified camera; every before/after pair uses identical settings. Final evidence has no critical asset/render errors.

## Visual and rendering evidence

Five paired browser views cover arrival, foundations, market, square connection and full site. Each PNG has a JSON camera/settings record. Drawing buffer **1800×1200, DPR 1, antialiasing, ACES exposure 1, PCFSoft 2048 shadows, near/far 0.12/1000 m**; lights and reflection environment match S2-D. No glass change or new postprocessing was made. Native A/B renders share the same Blender camera/daylight at 1800×1200; the native site view shows the selected composition. Blender uses the exact terrain top mesh and showcase plants; the browser also contains the original complete island landscape.

Matched foundation view, all rendering passes: baseline **441 calls / 3,998,471 triangles**; A **468 / 4,031,027**; B **468 / 4,029,551**; hybrid **480 / 4,045,427**. Matched market view: baseline **455 / 4,031,415**, hybrid **494 / 4,078,371**. These are measured view-dependent counters, not model inventory totals.

The complete-route timing is saved in [performance-full-route.json](../../../validation/market-street-s2e/performance-full-route.json). It covers **4,438 moving frames**, the completed route, authored glass and unchanged quality on Apple M4 Pro / ANGLE Metal: **5.6 ms median, 12.0 ms p95** rAF interval; render CPU submission **0.7 / 2.3 ms**. Calls vary **229–569** with the real follow camera; submitted triangles vary **2.49–4.15 million** across all passes. GPU timing and other devices were not measured. The browser JS heap snapshot was about 109.7 MB, excluding GPU/Blender memory. These timings are not a controlled FPS comparison with S2-D's different route.

## Verification and stop gate

**43 existing regression tests pass. All 1,430 protected files remain unchanged**, including every approved S2-A/B/C/D input, source archive/license, production game file and the original GLB. Native Blender save/reopen succeeded through live MCP. All selected models load and render without missing textures. [Regression output](../../../validation/market-street-s2e/regression-results.txt), [artifact/contact checks](../../../validation/market-street-s2e/validation.json), [site manifest](../../../validation/market-street-s2e/site-manifest.json).

No unresolved controller blocker remains on the tested public routes. Remaining gates/limitations, at most three:

1. **Owner design approval is pending** for the hybrid and the four planting-alignment adjustments.
2. Collisions outside the studied public routes and production wiring remain unimplemented/untested; this is an isolated design proof.
3. Full skyport, square and Guild architecture remain unbuilt by scope. The existing forest still partly closes the future Guild vista; this phase does not claim to resolve that future composition.

The foundations are visual/game-environment proposals, not certified structural engineering. Stop at S2-E; production integration is not authorized.
