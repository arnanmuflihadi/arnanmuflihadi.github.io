# Current-build repair audit

The latest street-layout and adventure-UI follow-up is recorded at the end of this document. Earlier asset sizes, positions and screenshots describe the preceding repair rather than the latest street plan.

Audited 31 October 2026 against the running localhost Home page, including the supplied adventure/MBR URL. This is an improvement pass on the existing shared world, not a claim that the game roadmap is complete.

## Before implementation

| Problem | Observed evidence and root cause | Correction | Module | Priority |
| --- | --- | --- | --- | --- |
| Main street and landmarks look unfinished | MBR before screenshot shows flat generated façades dominating the camera. Browser resource inventory confirms only `city-building.glb`, planter, tree, fern, resident and explorer requests. `licensed-scenery.js` places the sole imported building at (-34,-31), behind the principal streets; `architecture.js` generates every main landmark. | Replace camera-visible building shells with selected licensed prefabs; retain the road layout and tropical additions. | `architecture.js`, `licensed-scenery.js`, asset pipeline | P1 |
| NPC identity is weak | Five same-model residents, only shirt colors vary. MBR interaction offers Ayu, not Damar; no nameplates. Names/roles are hardcoded inside the renderer module. | Add a project-aware NPC registry, nearby labels, distinct appearances and research/limitations conversations. | `city-life.js`, `rigged-actor.js`, `adventure.js`, `adventure-ui.js` | P1 |
| Space cannot jump | Real key test leaves root Y at the support height. Input maps Space to dodge; controller overwrites Y with `groundHeight` each frame. Current explorer contains Idle/Walk/Run, no jump animation. | Add grounded vertical integration and compatible jump poses; move dodge to C. | `input.js`, `player-controller.js`, `character.js`, camera | P1 |
| Explicit project can lose ownership | Fresh MBR URL initially selects MBR and starts at (0,-25). However saved position can override an explicit deep link. Editorial scroll tracking can overwrite a project absent from Home's three featured chapters after returning/closing its panel. | Give explicit URL/project choices ownership until deliberate editorial navigation; explicit adventure links focus the relevant safe start; test history. | `living-atlas-controller.js`, state | P1 |
| Jump needs collision/camera integration | Horizontal collision successfully stops a run at the north shop wall (Z=-28.16). It has no vertical capsule/support state; camera follows instantaneous root height. | Preserve horizontal walls, add bounded step/support/ceiling behavior and damped vertical following. | movement, collision, camera | P1 |
| Asset presence is insufficient proof | Actual loaded asset inventory and screenshot disagree with the impression of a fully imported city. | Record source/license, optimized footprints, actual runtime prefab counts, and before/after views. | this document, asset manifests | P1 |

Existing strengths preserved: one renderer and scene across modes; real rigged explorer and residents; existing research case study links and factual caveats; optional service-yard quest/combat; warm directional/hemisphere lighting; walkable station ramp and original road network. Browser warning/error log was empty during the before audit.

Before screenshots are stored outside the repository in the task's visualization directory: `atlas-before-home.jpg`, `atlas-before-editorial.jpg`, `atlas-before-mbr.jpg`, `atlas-before-adventure.jpg`.

## Implemented repair, 1 November 2026

The existing Home/Work scene, research registry, HTML case studies and optional encounter remain in place. This pass replaces the dominant building shells, adds research guides, repairs explicit project selection, and adds a physical jump. It does not complete the broader game roadmap.

### Direction and Anti-Slop

Reading this as: a GIS research portfolio for planners and employers, in an Indonesian urban field-guide style, dial ENERGY 2 / RHYTHM 3 / MOTION 2. Direction comes from the supplied Living Urban Atlas and repair briefs, rather than a new visual identity.

| Decision | Purpose |
| --- | --- |
| Warm plaster, forest/teal, terracotta and a restrained research accent | Tie the imported city meshes to the brief's tropical modernist setting and the existing portfolio palette. The 3D material palette represents buildings and vegetation; interface signal colors remain limited. |
| Existing Archivo headings, Public Sans reading text and IBM Plex Mono metadata | Keep the established editorial hierarchy; use mono for short map/control metadata, rather than body copy. |
| Stable research boards over distinct landmark compositions | Keep evidence readable while transit, morphology and business studies occupy different visual settings. |
| Solid paper HUD panels and dark nameplates | Maintain measured contrast over moving scenery. Nearby actors get at most two labels, with occlusion and overlap checks. |
| Small radii and selective shadows | Separate controls and labels from the world without turning the interface into a stack of floating cards. |
| Amber optional-story marker and selected researcher outline | Identify actual quest/selection state; fictional gameplay remains separate from scientific findings. |
| User-driven camera transitions, authored movement and quiet vegetation | Provide exploration feedback. Reduced motion and an editorial background-pause button stop nonessential motion. |

Anti-Slop 3.2.24 was installed through the requested Codex marketplace commands. The user's session choice is `during`; no global mode preference or repository agent instructions were changed. The core, UI, human, mobile-layout, copywriting and comment skills were read. This pass adds solid contrast surfaces, 44-pixel controls, visible pressed/focus feedback, keyboard camera turning, keyboard operation of direction buttons, and an editorial pause action. The Space-in-dialogue exception follows the user's explicit control requirement; Enter activates conversation choices.

### Imported architecture: actual runtime use

All architectural rows below come from the **Downtown City MegaKit Standard** edition by Quaternius, under **CC0-1.0**. The archive's `License_Standard.txt` and actual glTF contents were checked. The delivered library is `assets/game/scenery/architecture-library.glb`, with source/output SHA-256 records in `architecture-source.json` and the original notice in `downtown-city-megakit-LICENSE.txt`.

`licensed-scenery.js` loads the library with GLTFLoader; `architectural-prefabs.js` instantiates its named templates and batches repeated primitives. Generated fallback shells are hidden only after successful loading. The original roads, collision footprints, canopies, signs, station vaults, pavilion roof and tropical planting composition are retained. These original structural details are not described as downloaded models.

| Category / source glTF inside the library | Instances | Geometry per template, approximate | Screenshot evidence |
| --- | --- | --- | --- |
| Shopfront / `Building_Small_1.gltf` (`shop`) | 3 | 18,344 triangles; 763 KB vertex/index data | `atlas-after-mbr.jpg`, Kopi Sore and Toko Taman |
| Mixed-use / `Building_Medium_2_001.gltf` (`mixed`) | 4 | 25,612 triangles; 1.13 MB geometry | `atlas-after-mbr.jpg`, Ruang Baca; `atlas-after-offices.jpg`, rear apartment block |
| Office tower / `Building_Large_2.gltf` (`office`) | 1 | 45,122 triangles; 1.70 MB geometry | `atlas-after-offices.jpg`, Menara Teras |
| Station and shop entrance bays / `Metal_FirstFloor_Window.gltf` (`entrance`) | 13 | 156 triangles; 6.8 KB geometry | `atlas-after-station.jpg`; entrance bays in `atlas-after-mbr.jpg` |
| Hall and bus-shelter glazing / `Metal_FullWindow.gltf` (`glazing`) | 12 | 210 triangles; 7.9 KB geometry | Station glass band in `atlas-after-station.jpg`; shelter beside the hall in `atlas-after-home.jpg` |
| Research pavilion / `Trim_FirstFloor_Window_001.gltf` (`civic`) | 6 | 160 triangles; 6.2 KB geometry | `atlas-after-pavilion.jpg`, recessed rear window band under the retained roof |
| Façade equipment / `Prop_ACUnit.gltf` (`aircon`) | 4 | 136 triangles; 3.0 KB geometry | AC units in `atlas-after-mbr.jpg` and `atlas-after-offices.jpg` |
| Station street furniture / `Prop_Bollard.gltf` (`bollard`) | 4 | 190 triangles; 4.7 KB geometry | Forecourt in `atlas-after-station.jpg` |
| Paving / `Sidewalk_Straight_3m.gltf` (`paving`) | 16 | 60 triangles; 2.3 KB geometry | Station promenade and central approach in `atlas-after-home.jpg` |

The templates share **22 embedded texture images**. Color maps are at most 512 px, normal/ORM maps at most 256 px. They occupy approximately **18.18 MB of RGBA8 texture storage with mipmaps**; this is an estimate, not a GPU profiler measurement. Unique geometry totals **3,621,708 bytes**. Per-template geometry figures above overlap shared data and should not be added. The self-contained GLB is **5,525,512 bytes**. Quantized attributes require no external geometry decoder. Warm mineral recoloring, matte finishes, correctly scaled entrance bays, Indonesian signage and retained shaded corridors customize the kit.

| Other active scenery / filename | Source / license | Runtime footprint and placement |
| --- | --- | --- |
| `canopy-tree.glb` | Quaternius Stylized Nature MegaKit Standard, CC0 | 719,224 B; 6,265 triangles/template; three 256 px maps; fourteen instances. Visible throughout the station and plaza screenshots. |
| `fern.glb` | Same nature kit, CC0 | 104,876 B; 288 triangles/template; one 256 px map; eight planting clusters. Used by `licensed-scenery.js`. |
| `city-planter.glb` | Downtown City MegaKit Standard, CC0 | 454,776 B; 118 triangles/template; six 256 px maps; four desktop instances. Visible beside the north shops and office approach. Omitted by the compact initial profile. |

Source pages: [Downtown City MegaKit](https://quaternius.com/packs/downtowncitymegakit.html), [Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html). The earlier `city-building.glb` is retained as a historical asset but is no longer requested by the active scenery loader. Roads and intersections retain their authored layout.

### NPC registry and conversations

`npc-registry.js` owns IDs, names, roles, districts, research links, text, appearance, animation choices and routes. `city-life.js` owns live interaction state and movement. All guides are explicitly fictional.

| Guide | Project / actual case study | Current integration |
| --- | --- | --- |
| Damar, Urban Morphology Analyst | `mbr` / `project-mbr.html` | Jakarta, beside the safe morphology approach at (2.2,-25.2). Explorer outfit/backpack, warm shirt/hair variation, faces the visitor. |
| Nadia, Transit Planner | `transit` / `project-transit.html` | Jakarta station/ramp route, ochre clothing, dark hair, shorter stature and an interaction idle. |
| Bima, Spatial Data Scientist | `cbd` / `project-cbd.html` | Jakarta office promenade route, blue shirt, different hair/pants/height. Starts offset from the player's approach. |
| Raka, Food Logistics Analyst | `pangan` / `project-pangan.html` | Registered for West Java, not spawned. |
| Kirana, Earth Observation Scientist | `alphaearth-food` / `project-alphaearth-food.html` | Registered for West Java, not spawned. |
| Sinta, Location Intelligence Analyst | `bandung-cafe` / `project-bandung-cafe.html` | Registered for Bandung, not spawned. |
| Sari, optional field-story researcher | Existing story / MBR research link | Existing south-plaza quest retained, with the resident model and its own appearance. |

Damar, Nadia and Bima offer research, project, limitations and goodbye choices. Text uses the existing case study evidence. Damar distinguishes morphology fit from income and welfare claims; Nadia distinguishes modeled access from observed trips; Bima distinguishes density clusters from official CBD designations. Future-region entries retain evidence boundaries without constructing those regions. Nameplates use camera projection, distance limits, collision occlusion, viewport bounds and a two-label cap.

A playtest exposed resident overlap trapping the player. Stronger avoidance and static-wall-aware overlap recovery fix the trap; the regression is tested.

### Jump physics and animation

Space queues one jump; held/repeated airborne presses cannot relaunch. C now dodges, J attacks and K guards. Jump and camera input ignore dialogs, fields, editable content and browser modifier shortcuts. Direction controls support held Enter/Space when focused. Q/R provides a keyboard alternative to camera dragging.

The stable movement root integrates vertical velocity using delta time, with **6.2 m/s launch velocity**, **16.5 m/s² gravity**, a short takeoff and landing phase, support detection, bounded steps, overhead collision and invalid-position recovery. The predicted apex is about **1.16 m above support**, appropriate to the 1.9 m explorer. Horizontal collision remains swept and independent of pose. Camera height follows a damped vertical target with existing obstruction protection.

The source explorer has no jump clips. The CC0 [Universal Animation Library Standard](https://quaternius.com/packs/universalanimationlibrary.html) contains authored `Jump_Start`, `Jump_Loop` and `Jump_Land`. `prepare-atlas-jump.mjs` retargets world-space bind-pose rotation deltas onto the original explorer, preserves bone lengths/scales, reconstructs the legacy sibling foot targets, and keeps root travel under physics control. The shipped `jump-animations.glb` is **267,260 bytes**, animation-only, with `JumpStart`, `JumpAir`, `JumpLand`; the library mannequin is not shipped. Original license and source/target/output hashes accompany it. Transitions are locomotion → takeoff → air → landing → locomotion, with a bounded visual floor correction at takeoff/landing.

Supports match pavement, shop thresholds, the station ramp/platform and the pavilion's chamfered floor. The pavilion now has a matching short approach ramp. Browser playtesting measured a jump there followed by a grounded return to Y=0.570. Mode changes settle vertical state; safe saved state contains X/Z rather than an airborne Y.

### Project synchronization

Explicit adventure links focus the chosen safe approach even if session storage contains a different prior position. Explicit selection owns the editorial camera until deliberate editorial navigation releases it; menu restoration and resize cannot silently select Transit or CBD. The supplied MBR link starts beside Damar, opens the real study, and keeps `project=mbr` when returning to reading. Work navigation also carries the selected project. Back/Forward uses the URL state while retaining one in-document scene/renderer.

### Performance and reproducibility

The sum of distinct basic desktop-adventure GLBs is **9,839,516 bytes**, excluding vendor JS, HTML, fonts and portfolio imagery. The compact profile omits the 454,776 B planter. Architecture/scenery load progressively; resident/explorer/jump assets wait for Take control. The optional encounter adds **1,122,992 bytes** only on acceptance or unfinished-story resume. Four scenery GLB fetches were observed in editorial mode; the adventure resource inventory adds the resident, explorer and jump files. Runtime prefab counts and actual fetch inventory are saved with the screenshots.

Repeated primitives use instances and shared geometry/materials. Distant NPC mixers run less often. Hidden pages, dialogs and menus pause simulation. Cancellation and disposal cover textures, instance buffers, skeletons, mixers and labels. This pass adds geometry and texture cost; it does not claim a device-wide frame-rate improvement. Lighthouse, Web Vitals, physical-phone performance and GPU memory were not measured.

Reproduce selected architecture with `scripts/prepare-atlas-architecture.mjs --source <extracted Downtown Standard> --deps <temporary node_modules>`. It uses glTF-Transform core/functions 4.2.1, extensions 4.5.1 and Sharp 0.34.5. Retarget with `scripts/prepare-atlas-jump.mjs --source <extracted Standard GLB/license folder> --deps <temporary node_modules> --three <temporary node_modules>`, using Three.js 0.180.0. These are authoring tools, not deployment dependencies. The site still runs from a plain static server.

### Verification

Automated suite: `node --test tests/*.test.mjs`, **46 passing**. Tests cover frame-rate-independent jump arcs, walking/running, repeat rejection, ceilings/walls, support drops, recovery, retargeted skeleton deformation, source hashes, NPC registry/routes, resident overlap recovery, pavilion support and keyboard input isolation, plus the existing scene/quest/combat/state checks.

The original static audit still exits 1 with **58 inherited findings**. Its complete output was compared with the untouched source checkout and is byte-identical. It is not a passing check and was not weakened. Local HTML href/src target inspection found no missing targets.

Final source checks: 40 authored Atlas modules, scripts and test files pass `node --check`; `git diff --check` passes. All 13 top-level HTML files have existing local href/src targets. The final static-audit comparison still matches the untouched checkout byte for byte.

### Browser click-through evidence

Verified in the in-app Chromium browser on 1 November 2026. The final runtime uses module revision 16 and Atlas CSS revision 18. A fresh `build=18` query avoids an older cached HTML response during preview. Browser viewport overrides were reset after testing. These checks do not establish physical-device or cross-browser compatibility.

| Element / action | Observed result |
| --- | --- |
| Explicit `index.html?experience=adventure&project=mbr&build=18` | MBR selected; explorer starts at (0,-25), grounded at Y=0.240; Damar is nearby and the interaction names him. |
| E near Damar | Opens the named fictional-guide conversation. Research, limitations, project and goodbye choices work; Space leaves the conversation open without jumping. |
| Damar → Show me the project → Read complete case study | Opens the MBR research panel, then navigates to `project-mbr.html` with the actual study heading and evidence. Browser Back returns to the selected MBR panel. |
| Nadia and Bima conversations | Research/limitations choices show their evidence boundaries; study choices open Transit and CBD panels with their actual case-study links. |
| Close study / Close conversation / Goodbye | Closes the relevant dialog and restores exploration or reading. |
| Read the atlas / Take control | Preserves MBR selection. On Home, MBR opens its panel because it is outside the three featured chapters; Work has the full MBR chapter. |
| Header Work | Navigates to `portfolio.html?project=mbr`; the morphology chapter remains selected. |
| Work Take control → Back → Forward | Adventure → editorial → adventure, all with MBR and scene UUID `02159ba1-b0d6-4f93-8931-346f4bed7482`. One renderer remains active. A full document navigation creates a new scene as expected. |
| Inspect study / Walk here | Opens the selected study or takes control at its research approach. Future-region entries show that their regions are not constructed. |
| Standing, walking and running Space jumps | Actual player Y rises and returns to support; held Space launches once. Wall, ramp and pavilion landings remain grounded. Station return Y=0.409; pavilion return Y=0.570. |
| Touch Jump / focused direction control | Touch launches a jump. Holding Enter on Walk forward moves Z from -25 to -26.161; releasing or blurring stops movement. |
| Native WASD / Shift / drag / Q and R | Walking, running and camera changes are visible. Browser modifier shortcuts are excluded by the input regression test. |
| Controls / pause / Escape / Close guide | Opens the controls dialog and pauses; Escape or Close guide restores play. |
| Reduce camera and environmental motion | Checkbox and world `reducedMotion` state change together; restored to the original false value after the check. |
| Quality | Eco and Standard both update the selected option and renderer quality setting. |
| Pause background / Resume background | Changes pressed state and actual world pause state in editorial mode. Taking control restores gameplay input. |
| Theme toggle / mobile menu | Light and dark render legibly; menu opens/closes and pauses the world. Original dark theme restored. |
| Optional story / Journal / acceptance | Existing Sari story opens; accepting enters the searching phase and loads encounter assets. Journal retains the active objective. |
| Optional J attack / C dodge | Native presses produce Attack1 and Dodge states; dodge moves the player. Guard, damage, defeat and retry behavior are covered by the retained combat tests. |

Layout checks covered 320×844, 390×844, 390×600, 768×1024, 844×390, 1024×768 and 1280×720. No horizontal document overflow was observed. New action targets are at least 44 px tall. At 390×600 the story panel ends at Y=165.78 and encounter health starts at Y=176, leaving a 10.22 px gap. Short landscape screens suppress the mini-map and extra objective text while retaining combat, journal and movement controls. At intermediate widths, resizing retains MBR selection. The final Work adventure console contains no warnings or errors.

The final browser asset inventory records seven real GLB fetches: architecture library, tree, fern, planter, resident, explorer and jump clips. At 1024×768 the observed MBR frame reports 149 draw calls and 289,774 triangles, with one renderer and all nine prefab categories present. These are one-view diagnostics, not a frame-rate benchmark or a measured GPU-memory budget.

### Contrast and screenshots

Ratios calculated with the installed Anti-Slop contrast checker from the actual foreground/background colors used by the repaired interface:

| Pair | Ratio | Result |
| --- | --- | --- |
| HUD text `#304b3d` / paper `#f8efd8` | 8.33:1 | AA normal text |
| Secondary text `#58634d` / paper | 5.54:1 | AA normal text; replaces the previous 4.29:1 pair |
| Story label `#725e39` / paper | 5.43:1 | AA normal text |
| Interaction intent `#835c35` / paper | 5.17:1 | AA normal text |
| Caption `#53624e` / paper | 5.68:1 | AA normal text |
| Nameplate role `#e0dfc7` / forest `#1b342e` | 9.86:1 | AA normal text |
| Pressed guard `#e9dec1` / `#315347` | 6.38:1 | AA normal text |
| Light dialog text `#1b1a16` / `#f8f4ec` | 15.87:1 | AA normal text |
| Light research accent `#c2295b` / `#f8f4ec` | 5.09:1 | AA normal text |
| Dark dialog text `#f3ede0` / `#15130f` | 15.90:1 | AA normal text |
| Dark research accent `#ff6fa0` / `#15130f` | 7.10:1 | AA normal text |
| Light muted text `#706a5e` / `#f8f4ec` | 4.89:1 | AA normal text |
| Control border `#68715b` / paper | 4.47:1 | Passes 3:1 non-text control boundary requirement |

Evidence directory: `/Users/arnanmuflihadi/.codex/visualizations/2026/10/31/01a18f7a-21b9-7172-b87f-9838b59bf748/`.

- Before: `atlas-before-home.jpg`, `atlas-before-editorial.jpg`, `atlas-before-mbr.jpg`, `atlas-before-adventure.jpg`.
- After: `atlas-after-mbr.jpg`, `atlas-after-jump.jpg`, `atlas-after-station.jpg`, `atlas-after-offices.jpg`, `atlas-after-pavilion.jpg`, `atlas-after-home.jpg`.
- Responsive and dialogue: `atlas-after-mobile.jpg`, `atlas-after-compact-encounter.jpg`, `atlas-after-mobile-dialogue.jpg`, `atlas-damar-limitations.jpg`.
- Actual resource requests and runtime counts: `atlas-network-assets.json`.

### Anti-Slop delivery gate

Scope: interface, copy and behavior added or repaired in this pass. Existing research titles, statistics and case-study content remain owner-supplied evidence, not newly invented promotional claims. This gate is not a certification of every historical portfolio page, and does not turn the 58 baseline static-audit findings into a passing result.

**Block 1: Hard Gate**

| Item | Status / evidence |
| --- | --- |
| R-02, punctuation | PASS: no em dash in the repaired dialogue, controls or project-panel source text. Existing owner titles are preserved. |
| R-03, mobile layout | PASS: tested widths 320, 390, 768, 844, 1024 and 1280; no document overflow; compact encounter panels have a measured gap. |
| R-17, statistics | PASS: research statements point to existing cases; byte counts come from files and render counts from the running renderer. |
| R-18, testimonials | PASS: none added. NPCs are explicitly fictional game guides, as requested. |
| R-23, asset authorization | PASS: imported scenery, differentiated NPCs and jump animations are explicitly requested in the repair brief; CC0 notices and provenance are retained. |
| R-24, navigation | PASS: 13-page local href/src inspection found no missing targets; native Work and MBR case navigation succeeded. |
| R-25, contrast | PASS: repaired text pairs exceed 4.5:1, recorded above; solid panels isolate text from moving scenery. |
| R-26, controls | PASS: element-by-element behavior is recorded in the click-through table; native controls invoke real actions. |
| R-27, loading/empty/error states | PASS: live-world preparation and failure status, unavailable explorer state, distant interaction guidance and no-nearby-nameplate state exist in the controller and renderer. |
| R-28, FAQ | PASS: no FAQ added; the guide contains actual controls and geographic limits. |
| R-32, keyboard | PASS: Tab/Enter direction control, E dialogue, Q/R camera, Escape dismissal and visible two-tone focus; input tests include repeat and modifier isolation. |
| R-33, source editing | PASS: this Anti-Slop pass uses source patches; authoring scripts process GLBs rather than rewriting UI source at runtime. |
| R-34, themes | PASS: native light/dark toggle tested; both dialog palettes have measured contrast. |
| R-35, executed interface | PASS: live static server, actual GLB resource inventory, browser click-through table, 46 passing tests and 40 syntax checks. |
| R-36, claims | PASS: no unmeasured speed or compliance claim; diagnostic counts and unmeasured device limits are explicit. |
| R-37, direction | PASS: existing Indonesian field-guide brief recorded as ENERGY 2 / RHYTHM 3 / MOTION 2 before this pass. |
| R-38, realistic content | PASS: research is linked to actual case studies; fictional guide roles are identified in the conversation. |
| R-39, interaction semantics and motion | PASS: named native buttons/select/checkbox, visible focus and pressed/disabled feedback, 44 px action targets, reduced-motion setting and a background-pause control. Existing document landmarks/language and zoom remain available. |
| R-40, loading stability | PASS: fixed world canvas and reserved panels; poster dimensions and high fetch priority are explicit on Home/Work. No third-party blocking script or invented Web Vitals score added. |

**Block 2: Purpose-Gate**

| Item | Status / evidence |
| --- | --- |
| R-01, gradients | PASS: existing atmospheric world shading expresses daylight/depth; readable interface panels use solid colors. |
| R-04, icon relevance | PASS: movement arrows indicate directions; the mini-map and optional-story marker represent actual spatial/quest state. No generic icon set added. |
| R-06, typography | PASS: Archivo/Public Sans preserve the portfolio hierarchy; mono is confined to compact map/control metadata. |
| R-07, grids | PASS: the map depicts this conceptual district; no decorative blueprint background added. |
| R-08, arrows | PASS: the case-study link uses a directional cue for navigation; no arrow added to every control. |
| R-09, badges | PASS: metadata identifies place, research and fictional story state; no promotional badge added. |
| R-10, glass | PASS: repaired HUD and nameplates use opaque surfaces; no stack of translucent overlays added. |
| R-12, shadows | PASS: selective label/panel separation supports legibility over the world; no universal large floating shadow. |
| R-13, glow | PASS: no decorative glow added. |
| R-14, repeated cards | PASS: imported transit, neighbourhood and office compositions differ; study boards share a readable evidence hierarchy. |
| R-19, motion | PASS: authored locomotion/jump and user-triggered camera transitions support exploration; reduced motion and pause limit ambient animation. |
| R-22, illustration | PASS: licensed architecture and nature are requested world content with per-category runtime evidence. |

**Block 3: Liveliness**

| Item | Status / evidence |
| --- | --- |
| Explicit dials | PASS: ENERGY 2 / RHYTHM 3 / MOTION 2 recorded in Design Read. |
| Consistent execution | PASS: restrained paper controls frame distinct station, shop, office and pavilion views; movement responds to the visitor. |
| Focal point | PASS: the explorer/nearby guide anchors adventure; selected study text anchors reading and dialogs. |
| Structural whitespace | PASS: HUD keeps the central traversal corridor clear; compact panels are separated from combat and movement controls. |
| Deliberate accent | PASS: research accent identifies study hierarchy; amber is reserved for the separate gameplay warning/quest state. |
| Identity motif | PASS: paper field notes, short map metadata, Indonesian signage and shaded tropical landmarks repeat across views. |
| Design Read | PASS: the user brief, audience, visual direction and rationale table precede the documented Anti-Slop interface changes. |

**Block 4: Craftsmanship and quality locks**

| Item | Status / evidence |
| --- | --- |
| C-1, intentionality | PASS: the visual-purpose table records color, type, composition, surface, spacing and motion decisions. |
| C-2, functional completeness | PASS: click-through results cover repaired controls, dialogs, navigation, choices, movement and quality settings. |
| C-3, content-driven composition | PASS: research, limitations, navigation and optional play serve the requested portfolio; no filler sections added. |
| C-4, resilience | PASS: tested themes, keyboard, short portrait/landscape and intermediate widths; safe recovery and failure states remain. Broader browser/device testing is still listed below. |
| C-5, evidence | PASS: source licenses, local study links, manifests, test output and actual browser resource inventory support the repair claims. |
| R-05, layout rhythm | PASS: full world, evidence boards, conversation and compact controls have different roles and proportions. |
| R-11, radii | PASS: modest rectangular field-note controls coexist with the existing primary mode switch; no universal pill treatment. |
| R-15, action copy | PASS: Talk to Damar, Inspect study, Walk here, Jump, Read the atlas and Pause background describe their effects. |
| R-16, buzzwords | PASS: repaired UI uses factual research/control copy; no generic AI marketing language. |
| R-20, identity | PASS: ruko signage, shaded station, pavilion, Indonesian research and named fictional guides give the work a specific setting. |
| R-21, themes | PASS: existing owner theme preference is respected; the light/dark toggle was exercised and restored. |
| R-29, palette | PASS: paper/forest surfaces and a research accent form the interface system; world materials use the documented tropical architectural palette. |
| R-30, originality | PASS: no borrowed SaaS template or product-clone layout introduced. |
| R-31, rationale | PASS: every major new visual treatment has a one-line purpose in the Design Read table. |

### Remaining development

West Java and Bandung, their three prepared guides, intercity travel, open interiors and rooftop traversal remain unimplemented. Grounding uses the designed support surfaces rather than arbitrary imported mesh traversal. There is one existing optional encounter. Automatic WebGL context rebuilding, physical-device performance testing and Safari/Firefox testing are not included. The 58 baseline static-audit findings remain separate work. No deployment was performed.

## Street and adventure UI follow-up, 1 November 2026

The requested follow-up fixes streetscape placement and applies the owner's Breath of the Wild UI reference to the existing urban portfolio. ENERGY 2 / RHYTHM 3 / MOTION 2 remain the direction: quiet exploration, distinct landmarks and user-controlled movement. The interface is original, with no Nintendo assets, copied glyphs or game fonts.

### Review findings and implemented corrections

| Finding | Correction and verification |
| --- | --- |
| Tree at (15,-24) and decorative planters occupy the north road | All 14 tree sites and four imported planters now occupy planting pockets; tree pits remain visible when imported trees replace fallback crowns. Tests reject any tree pit, palm or planter overlapping a road. |
| Shop steps extend into the carriageway; posts constrict the footway | Shortened thresholds and repositioned shade supports. A continuous walk along the north footway passes the full block. |
| Office podium/collision extends into the road and obstructs the south sidewalk | Set the actual office back to (21,-11), align its collision to its 13.8×12.8 m imported footprint, and move its arcade/sign to the new frontage. The rear west block and Warung Rindang also move clear of the inner sidewalk. |
| Curbs cut across junctions; separate paving aprons overlap | Shared street and sidewalk rectangles leave both junctions open. A single plaza/walk outline replaces overlapping slabs. The north spine stops before the carriageway; two physical curb ramps meet the marked crossing. Raycasts compare actual surface heights with player support, including road/crossing samples. |
| Mini-map roads disagree with the world | The circular map consumes the same roads, sidewalks, public-space outline and tree coordinates as the rendered district. It remains a conceptual map, with actual player and guide markers. |
| Damar stands in the road | Damar now stands at (2.2,-27.8); the MBR approach is (0,-27.8), on the north sidewalk. Native E opens his dialogue, limitations and the real MBR project panel. |
| Broad blank frontage lacks street detail | Add pitched terracotta roofs, deep eaves, balcony rails, rain pipes, grounded café tables/chairs, cycle stands, eight imported drain grates and four manhole covers. Flat imported paving replaces curb-shaped tiles inside pedestrian walks. |

`architecture-library.glb` now contains **eleven** Quaternius Downtown City MegaKit Standard CC0 templates. The two new files are `Prop_Drain.gltf` (10 source triangles) and `Prop_ManholeCover.gltf` (118); flat paving is `Sidewalk_NoCurb_3m.gltf` (42). The library is **5,529,408 B**, only **3,896 B** larger than the preceding repair. Unique geometry is **3,623,740 B**, and the same 22 embedded texture images are reused. Source/output hashes and original license remain adjacent to the GLB. Runtime instance counts are shop 3, mixed-use 4, entrance 13, office 1, glazing 12, civic 6, AC 4, bollard 4, paving 14, drain 8 and manhole 4. No extra model request is needed for the two props.

### Adventure interface and fidelity

The concept was generated with the built-in image tool from the real before screenshot. Reference file: `/Users/arnanmuflihadi/.codex/generated_images/01a18f7a-21b9-7172-b87f-9838b59bf748/exec-59c2cc77-c549-4e36-8f52-401037ab064a.png`. HUD text, controls and the map remain live HTML/CSS/Canvas; the concept is not shipped as UI artwork.

| Comparison point | Implemented result / deliberate boundary |
| --- | --- |
| Layout | Slim forest header, restrained location note, upper-right optional-story strip, lower-right circular map and small bottom actions. The center stays open for traversal. |
| Typography | Georgia serif location/dialogue headings and readable Public Sans controls/body text. Existing owner name, project titles and factual caveats are preserved. |
| Palette and surfaces | Ivory, forest and brass. Solid forest control/dialogue surfaces and a small paper location note keep measured contrast over arbitrary scenery. |
| Map and controls | Brass compass ring, north marker and the real shared street plan. Native keycaps, 44 px controls and round touch directions replace the earlier rectangular control cluster. |
| Dialogue | Lower dark band with research text on the left and actual topic choices on the right; one column with scrolling on phones. The concept's invented illustrated portrait is omitted in favor of the existing licensed 3D actors. |
| Responsive behavior | The narrow quality row and combat captions were repaired after browser inspection. Short screens hide the mini-map, retain movement/combat controls, and keep health/story/action panels apart. |
| Copy | Existing research and story copy retained. Only controls are condensed into real keycap/label pairs and the empty interaction prompt becomes “Find a guide or landmark.” No invented weather, currency, stamina or promotional numbers. |

The concept and final browser screenshots were inspected with `view_image` in the same verification pass. Desktop was checked at 1280×720, with phone/tablet checks at 320×844, 390×600, 390×844, 768×1024, 844×390 and 1024×768. The listed boundaries preserve real content and legibility rather than reproducing invented concept content.

Measured contrast: ivory on forest **13.52:1**, brass on forest **9.01:1**, disabled prompt **8.43:1**, forest on paper **12.68:1**, secondary paper text **6.01:1**, research label **6.02:1**, selected dialogue choice **8.84:1**, hover **7.79:1**, active **6.22:1**, paper research link **6.53:1**. The quality select itself is 44 px tall. At 390×844 the wrapped MBR location note ends at Y=154.375 and the story starts at Y=160; the document has no horizontal overflow.

### Follow-up verification and gate

**49 tests pass.** Three new meaningful tests reject carriageway obstructions, traverse the north/side/south footways and curb ramps, and raycast rendered paving against support heights. Existing quest approach, rig, jump, collision, camera, NPC, research-route and combat tests remain passing. Fractional MBR coordinates are checked with a real swept move from the reachable grid. Asset count assertions now validate the eleven-template library and its hash. Syntax checking covers 41 authored modules/scripts/test files. `git diff --check` and local HTML target checks pass. The original static audit still exits 1 with the same **58 findings**, byte-identical to its untouched baseline.

Native browser click-through: plaza walking → north crossing → Damar conversation; limitations → real MBR panel; touch Jump → airborne state; reading/adventure/Back retains MBR and one scene UUID; mobile menu opens/closes; light/dark theme switches and restores; reduced motion switches and restores; Eco/Standard changes quality; Sari accepts the quest; entering the yard shows actual health/actions; defeat recovery restores health 100 at the clear entrance (-9.5,37). At 844×390, story ends Y=133.19, health begins Y=154, combat occupies Y=263–315 and bottom controls begin Y=330. The final browser warning/error log is empty. Authored modules use revision 22, unchanged Three.js uses revision 16, and adventure CSS uses revision 5.

The earlier per-item Anti-Slop gate was rechecked within this follow-up's scope:

- **Hard Gate PASS:** authorized original/CC0 content, real controls and links, measured text contrast, visible keyboard focus, 44 px targets, responsive layouts and actual browser execution. Loading/failure states and reduced-motion/pause behavior remain available. The baseline static audit is explicitly separate and still failing.
- **Purpose-Gate PASS:** map grid communicates the actual conceptual district; brass identifies compass, selection and key prompts; serif headings give the adventure reference; solid surfaces maintain contrast. Roof/paving/planting changes serve the streetscape rather than generic decoration.
- **Liveliness PASS:** ENERGY 2 / RHYTHM 3 / MOTION 2, a clear explorer/guide focal point, shaded Indonesian landmarks, structural space around the HUD and restrained user-driven motion.
- **Craftsmanship PASS:** shared placement data, traversable footways, source-verified assets, functional dialogs/settings/history, theme/keyboard/viewport checks and the recorded fidelity ledger. No whole-roadmap, cross-browser, physical-phone or performance-improvement claim.

Evidence in the same visualization directory as the earlier repair: `city-layout-before.jpg`, `city-layout-after-plaza.jpg`, `city-layout-after-crossing.jpg`, `city-layout-after-dialogue.jpg`, `city-layout-mobile.jpg`, `city-layout-mobile-dialogue.jpg`, `city-layout-mobile-encounter.jpg`, `city-layout-landscape-encounter.jpg`, and `city-layout-network.json`. No deployment or commit was performed.
