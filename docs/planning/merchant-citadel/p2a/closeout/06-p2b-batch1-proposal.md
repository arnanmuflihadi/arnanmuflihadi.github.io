# First P2-B construction batch: what is built, what is proposed

Nothing here authorises P2-B. Part A is **built in the preview for approval**; Part B is a **proposal** for the next controlled batch. The remaining Merchant Citadel buildings are not constructed.

## A. Batch 1 — Exchange Hall and civic court (built, pending approval)

### A1. The Exchange Hall as a modular landmark

The P1.4 archetype A01 (28 x 16 m footprint on the terrace, 25.8 m to the tower finial) is exported as **five reusable modules**, all sharing the hall's origin so they assemble by placing each at one transform. The podium deck and the 12 m flight of steps are the existing `PODIUM` module; the terrace is `TERRACE`.

| Module (`A01_…`) | Contents | Triangles (final kit) | Primitives | Notes |
|---|---|---|---|---|
| `main` | 14 x 8 m two-storey body, stone ground floor, jettied arcade facade, roof 8x14 (ridge along x), two round-tile dormers, four burgundy banners, two wall lanterns | 22,450 | 15 | the hall's mass and front |
| `wing_w`, `wing_e` | 6 x 6 m two-storey wings with gables (mirror of each other) | 8,654 each | 9 each | pure mirror: one module could be instanced with a flip in P2-B |
| `porch` | gabled entrance porch on four posts, three round-arched doors behind, seal on the gable | 5,792 | 7 | the entrance threshold |
| `tower` | 4 x 4 m tower from level 4 to 6, seal on each of four faces, round windows, pyramid roof with finial | 13,420 | 12 | landmark; custom seal (`CUS-Seal_NiagaAwan`) x 4 |

Total 58,970 triangles (90,234 before module LOD), vertices with baked AO. Provenance: downloaded CC0 Quaternius Medieval Village and Fantasy Props modules plus the custom seal (`04`, registry `asset-registry.csv`); nothing from the first island, no AI generation.
Source: `p2a_hall.py` splits the P1.4 `A01` parts; `p2a_kit_export.py` builds, bakes and exports; the Blender source assemblies are the two `.blend` files in `.asset-inspection/merchant-citadel-p1/p2a/` (not in the zip).

### A2. Court integration

The hall stands on the 1 m civic terrace (N07, y 1.0) and its own 1 m podium (N08, y 2.0). The court already had two flag posts with burgundy banners, benches, lamp posts and the paving seal (P2-A dressing); they now frame a real facade instead of a box. The 12 m flight reaches the porch landing at n 75–77.4. The terrace balustrade, steps and skirt are unchanged.

### A3. Collision and camera

* 23 proxies, all derived from the part definitions: walls (hall body, wings, tower core), 15 stepped roof bands (`cameraOnly`), 4 porch posts. The porch posts and the roof bands follow the P2-A rules (03, 04 of P2-A).
* Walk-through width in front of the porch: 5.3 m between the posts' inner faces; stairs top (N08) 3.6 m clear to the nearest solid.
* Camera: stairs up 12.9 m with no pops; stairs down 2.97 m minimum for about a second (starts against the facade) then recovers; on the porch landing facing out the camera is 0.94 m away and the **character fade** removes the back-on-the-lens view (03).
* Pedestrian access verified: N06→N07→N08 up and down, walking and running, 0.22 m risers, jump on a riser, 1 m drop landed; porch landing route; edges N07–N21/N22 to the court benches (02).
* **Doors are decorative.** There is no interior; the hall cannot be entered in this batch (P1.4 has none either).

### A4. Evidence

Matched Blender/browser views of the hall: [court at eye height](visuals/comparison/cmp-view-d-exchange-court.jpg), [porch](visuals/comparison/cmp-p2b-hall-porch.jpg), [tower](visuals/comparison/cmp-p2b-hall-tower.jpg), [aerial](visuals/comparison/cmp-p2b-hall-aerial.jpg); Blender renders in `visuals/blender/`; browser stills in `visuals/browser/`; scale test (9 buildings within 0.5 cm of the P1.4 envelopes including the hall's 0.40 cm); performance in 05.

### A5. Artistic corrections

Supported by evidence and made: (1) the hall's front looked dull in the browser because the preview light was mirrored; corrected (04). (2) The recess and porch darkness the Blender render has is now reproduced by baked AO (04).
Considered and **not** made: the Blender render shows slightly more roof weathering and a thin grey line along the main roof's eave that I did not identify in the kit modules; the browser roof (1024 px texture) is flatter. If the owner wants either, the options are a roof-texture variant and a small custom eave trim; neither is needed for the architecture to read.
The hall is faithful to the approved P1.4 design; I made no change of form, proportion or materials.

## B. Proposed batch 2 — complete the representative commercial district (D3 Pasar Awan)

D2 Koridor Niaga is already complete in the slice (B04–B09). D3 Pasar Awan holds the market and the inn (E03) and four awning rows with the cross (built); what it lacks is its **two market halls and three small shops**. Building them makes D3 a complete, walkable, representative commercial district.

| Item | Archetype | P1.4 triangles (est. after module LOD) | P1.4 readiness | Work |
|---|---|---|---|---|
| B02 Market Hall West (provisions) | A02 | 42,176 (≈ 30k) | CONDITIONAL | covered hall 8 x 12 m, two dressing kits, cafe-pack counters, Avramania goods |
| B03 Market Hall East (crafts) | A02 | 42,176 (≈ 30k) | CONDITIONAL | same shell, different kit |
| B14, E06 | A04 | 7,980 (5.9k) | CONDITIONAL | shops with the custom cloth awning (module exists) |
| E07 | A04b | 8,278 (6.2k) | CONDITIONAL | shop, eaves to street |
| Nodes N18/N31, N19/N32 | | | | arch entrances and interiors become real network nodes |
| Estimated addition | | **≈ 78k triangles** | | whole-slice view ≈ 387k triangles; frame cost expected to stay in single-digit milliseconds on machine A (estimate, not measured) |

Why this batch and not another: it reuses the awning, cloth, cross and inn modules already proven, adds the two conditional asset families (cafe pack, Avramania goods) so their risks surface early, and finishes a district the owner can walk end to end.

Entry criteria for batch 2 (all must hold): owner approval of this closeout; decision on AO bake strength (0.6 suggested in `production-config.json`); a measurement on a lower-end GPU or an agreed target minimum spec; the loader material cache and shader pre-warm in place.
Acceptance for batch 2 (same as batch 1): reproducible Blender source and GLB; scale/placement within 5 cm; collision proxies; every edge walked both ways; camera cases; matched views; performance counts and times with the read-back method; provenance rows in the registry.

## C. Reusable configuration and registry

* [`production-config.json`](production-config.json): texture tiers, module LOD targets, AO parameters, metal constants, lighting, collision/camera rules, network rules, loader to-do.
* [`asset-registry.csv`](asset-registry.csv) / `.json`: one row per production GLB node (22): archetype, purpose, status (P2-A / P2-B batch 1), instances, triangles, vertices, primitives, materials, baked AO, sources, licence notes, P1.4 readiness, collision groups. Regenerate with `blender/p2a_registry.py`.
* Scripts: `blender/p2a_data.py` (slice, collisions, network), `p2a_hall.py`, `p2a_kit_export.py`, `p2a_world_scene.py`, `p2a_compare.py`, `p2a_registry.py`.

## D. Not in batch 1 or 2

D1 Gerbang Niaga, D4 Pelataran Bursa (B15/B16 corner houses), D6 Lorong Lentera, D7 Jalur Gudang (warehouse, E04), the lookout's second shop (E05), the floating island, NPCs, quests, vegetation, the first-island integration, any deploy or commit.
