# R0-D2 — precision mount search

Research checked 10 November 2026. **NO SUITABLE VERIFIED ASSET. No purchase or integration recommended yet.** Sol selected and judged candidates; Terra inspected listing metadata and reproducible GLB checks. D1A/B/C were read, not repeated. Stan’s dragon remains excluded as the primary mount.

**Best next verification candidate:** Dragon Pack by DZTFIX Dreakow, because its reference shows four legs and separate wings and its listing expressly offers Blender actions/FBX beyond Unreal. **Fallback investigation:** Ashwing Full, using the free Lite as a technical sample. Neither is an approved mount. European Dragon is the best legally open option examined, but fails the supplied-animation requirement.

## Three finalists

| Candidate / exact source | Creator, price and formats | License / present status |
|---|---|---|
| [Dragon Pack — Fantasy Rigged & Animated Creature](https://www.fab.com/listings/0a8edefe-51c5-47c5-b324-d40104ac351a) | DZTFIX Dreakow. Browser shows Personal **Rp902,965 including VAT**, Professional Rp1,806,131; eligibility not selected. Blender/FBX/Unreal listed. | Fab Standard; listing allows AI usage. Raw public-repository permission not established. **UNVERIFIED** technical suitability; legal clearance required. |
| [Ashwing Drake Full](https://literock-studios.itch.io/ashwing-drake) | Literock Studios. **US$29+**, 432 MB listed archive. FBX/GLB/Blend claimed. Paid files **not acquired**. | Custom commercial end-product license; no raw asset redistribution. Full terms inaccessible without its archive. **UNVERIFIED** full model; Lite findings below are not proof of Full. |
| [European Dragon](https://sketchfab.com/3d-models/european-dragon-82f393a2e6c048ad80c171ce3b3a7b87) | Regina Cachoa / embedded credit Nonexistent 101. **Free**. Original FBX and converted GLB/glTF offered; 1K GLB actually downloaded. | **CC BY 4.0**, including commercial adaptation/redistribution with credit. **REJECT for this ready-mount brief:** both takeoff and landing absent; rider/landing fit unverified. |

Prices are observations, not purchase approval. No payment details entered. [Visual comparison](evidence/candidate-comparison.png): two actual Blender previews and one seller image, explicitly labeled; framing/scales differ and do not establish fit.

## Animation and geometry: claimed versus inspected

**Dragon Pack — listing only.** Seller claims 62 actions in Blend and separate animation FBXs, 111 deform bones, 19 morphs, and 56k/28k/14k/6.7k LODs. Ground/flight/transitions are advertised; actual clip names, durations, folding, foot contact and export preservation are **unverified**. Separate source formats could avoid Blueprint/Niagara dependency; this has not been tested. Four-legged silhouette is promising, but dorsal spines/wing roots may obstruct a rider. No measured dimensions, materials, texture memory, file bytes or rider envelope. This is a verification lead, not a numerical quality endorsement. [Seller listing](https://www.fab.com/listings/0a8edefe-51c5-47c5-b324-d40104ac351a).

**Ashwing family.** Full claims 33 clips including landing, 61 bones and 38,758/11,993/3,997/1,499-triangle LODs. Seller discloses Meshy-generated base mesh/textures with studio-made rigging/animation. Full’s file contents and rights chain were not independently verified. [Full listing](https://literock-studios.itch.io/ashwing-drake).

The official **free Lite** was acquired for private evaluation, outside the repository. Actual GLB: **11,407,532 bytes, 11,992 triangles, 61 joints, one mesh/material, three embedded 2048² textures**, two fold-corrective morphs, four influences maximum. Actual clips:

| Lite clip | Duration |
|---|---:|
| idle_loop | 3.000 s |
| walk_loop | 1.067 s |
| roar | 2.000 s |
| bite | 1.200 s |
| takeoff | 2.400 s |
| fly_loop | 0.800 s |

All six contain morph-weight tracks; takeoff changes both corrections from 1 to 0. **No landing clip.** Blender static inspection confirms folded and airborne configurations, not convincing continuous ground contact or riding. In the sampled idle, hand-weighted regions remain ~0.60/0.62 m above Z=0, while foot-weighted minima are +0.059/−0.004 m. These regions are not complete soles/knuckles: contact remains unresolved rather than declared proven. Wyvern anatomy requires particular scrutiny around wing-hand support and the rider’s knees. [Metadata](ashwing-lite-metadata.json), [pose samples](ashwing-pose-samples.json).

**European Dragon — actual GLB.** **8,997,240 bytes, 42,338 triangles, five skinned meshes, 169 joints, four materials, six embedded 1024² textures**, no morphs. Actual clips: `Fly` **3.292 s**, `Walk` **0.625 s**, `Run` **0.625 s**, `Idle Stand` **6.625 s**, `Idle Sit` **2.458 s**. Blender shows four legs and tall folded membranes in the standing clip. Flight start/middle/end remain airborne, not a hidden takeoff/landing sequence. Two missing transitions exceed the allowed one-transition conditional case. No seated rider or certified ground-contact result. [Metadata](european-metadata.json).

Source and corrected Stan files were not altered. These are new-candidate checks, not repeated Stan fidelity experiments.

## Conversion and cost checks

Terra’s existing Three.js GLTFLoader/AnimationMixer approach parsed both evaluation GLBs and checked finite bone matrices at start/middle/end of every clip. Texture handling was stripped **in memory only** for these CPU checks; Blender separately rendered actual textures.

Lite’s isolated Blender roundtrip initially used inherited **24 fps**, shortening four clips and producing sampled bone differences up to 0.32144 units. One justified correction—reimport/export at the source **30 fps**—preserved six durations, 61 bone names/parent relationships and both morphs; maximum sampled bone-position difference **0.0000062 units**. Vertex-by-index comparison is unavailable because export changes 9,152 vertices to 9,215. This is three-phase skeletal/morph evidence, not full deformation equivalence or texture/export appearance approval. Exporter also emitted a multiple-image sampler warning. [24 fps finding](roundtrip-check.json), [30 fps result](roundtrip-30fps-check.json). Restricted derivatives remain outside the repository.

European’s roundtrip was not pursued after its two missing transitions eliminated it. Actual compatible GLB parsing is verified; Blender re-export preservation is **NOT TESTED**.

Decoded RGBA8 texture **estimates**, before/with mipmaps: European ~24/32 MiB; Lite ~48/64 MiB. Source mesh primitives suggest five/one base draws respectively, **not measured runtime draw calls**. No browser scene, GPU-memory test or performance benchmark was created. Paid assets’ counts remain seller claims; their rendering costs are unmeasured.

## Skyport and rider feasibility

Use the accepted **1.9 m explorer, 13 m deck, 9.2 × 4.1 m canopy, 2.595 m fascia**, closed guards/pylons/standard and candidate **4 × 4 m** standing area. No candidate has passed a full body/rider/wing/tail swept-volume test there.

| Candidate | Grounded fit | Dynamic fit | Boarding fit |
|---|---|---|---|
| European | Sampled native standing bounds 1.169 × 1.472 × 1.370 m. At illustrative 3×: **3.507 × 4.415 × 4.111 m**. Scale is calculated, not an approved rider scale. | Three sampled flight poses at that scale reach ~6.48 m width; **not** a maximum sweep. No landing motion. | Four legs and a dorsal torso exist; tall folded wings may mask/clash with the rider. Actual pelvis/boot clearance unknown. |
| Ashwing Lite / Full | Lite sampled folded idle **3.503 × 9.309 × 3.231 m**. Cannot fit the 4 × 4 m zone. Full bounds not measured. | Lite sampled flight width ~7.985 m; advertised family span 12 m is not an independently verified maximum. Tail/roof/guard clearance unknown. | Mid-spine weighted width ~0.856 m is only a regional bound, not a clear seat. Wing roots, membranes, tail and rider legs need joint inspection. |
| Dragon Pack | No trustworthy physical dimensions in available evidence. | No measured sweep or stopping envelope. | Four-leg arrangement is promising; no rider dimensions or unoccluded dorsal seat proven. |

No candidate should be scaled down merely to force the deck fit. A mounted creature must stay outside the low canopy. If the chosen full-size candidate cannot clear the closed platform, a **separate minimal landing pad** is the preferred future site question; no modification or site search is authorized/performed here. Current evidence cannot specify its dimensions or declare every candidate impossible on the whole 13 m deck.

## License and authenticity gate

- European listing and GLB identify CC BY 4.0. Current [ReginaCachoa profile](https://sketchfab.com/ReginaCachoa) explicitly links Nonexistent_101 social accounts, supporting its older embedded attribution. Preserve both names, source, license and modification notice. No separate NoAI restriction was observed. [Attribution](acquired/ATTRIBUTION.md), [profile evidence](evidence/european-creator-profile.png). CC BY permits commercial sharing/adaptation; it does not warrant third-party rights. [License/legal code](https://creativecommons.org/licenses/by/4.0/legalcode).
- Lite’s actual `LICENSE.txt` permits commercial end products and modification, prohibits raw/modified asset re-upload and ML training, and permits compiled/packaged end products. It does **not expressly clear a raw GLB committed to public GitHub**. README mentions web use; that is not a blanket source-redistribution grant. Credit is appreciated, not required. Full’s complete license has not been inspected; do not transfer Lite permission automatically. [Lite listing](https://literock-studios.itch.io/ashwing-drake-lite).
- Dragon Pack’s selected listing points to **Fab Standard** and says AI usage allowed. Standard permits commercial incorporated projects/modification and private collaborator sharing, not standalone free asset redistribution. This does not clear putting source Blend/FBX/GLB in a public repository. Written clarification/additional permission is needed for this delivery model. Default attribution is not required under Standard; retain provenance anyway. The seller presents it as their work, without obvious proprietary-character branding; independent authorship is unverified. [Fab license summary](https://www.fab.com/eula).

No marketplace license was assumed to cover all assets. No restricted source files or model-containing Blend derivatives were copied into the public repository; Lite source/exports are under `/private/tmp/arnan-dragon-d2/` and the official downloaded zip is in Downloads. Research images are reference evidence, not acquired production art. No seller messages sent.

## Gates and scores

**P** = verified narrow requirement; **U** = insufficient evidence; **C** = explicit clearance/test prerequisite; **F** = fails this brief. A clip existing is not proof of rider fit.

| Finalist | G1 legal/public raw files | G2 grounded | G3 skeletal flight | G4 rider | G5 fold/landing | G6 compatible/cost | Overall / weighted score |
|---|---|---|---|---|---|---|---|
| Dragon Pack | C: extra permission | U | U | U | U | U: source formats/LODs claimed | **UNVERIFIED / N/A** |
| Ashwing Full | C: full terms + extra permission | U: Lite contact unresolved | U for Full; P for Lite clip | U | U: Full landing unseen | U for Full; Lite conversion sampled | **UNVERIFIED / N/A** |
| European | P with attribution | P: existing standing/sitting clips | P: actual flight data | U | F: no takeoff/landing; geometry unproven | P: actual manageable GLB | **REJECT / N/A** |

Lite alone is **UNVERIFIED**, not a ready free fallback: missing landing, unresolved contact/rider fit and raw-public-hosting permission. Reversing takeoff is not established as a low-risk landing solution.

Apply the requested weights only after essential gates pass: rider/anatomy 25%, animation 25%, fold/landing 20%, style 15%, Three.js cost 10%, effort 5%. **No asset qualifies for a defensible numerical score.** No human visual approval is assigned.

## Bounded search log and exact next action

Seven distinct listings inspected; only the three finalists above received detailed evaluation. Lite is a sample of Ashwing, not a separate ranked color/model variant. Other screens:

- [Dexsoft Dragon Animated Character](https://www.fab.com/listings/42d1d0d9-9de8-46be-9c6e-9a842f6b5835): only Unreal format exposed; AI-usage flag No. Not shortlisted; compatible animated sources and workflow permission unresolved. Its advertised 18 clips are not file-verified.
- [3DDisco Realistic Gold Dragon](https://www.fab.com/listings/0f06d67c-aa51-4f96-981a-0ff07f228669): compatible formats advertised, but AI-usage flag No and raw-repository rights unresolved. Not acquired or advanced; no color variants counted separately.
- [Glacivern](https://www.fab.com/listings/5b833abe-1311-45fb-a3ea-ea063fe17e14): advertised 67,370 triangles, icy/crystal styling and 4 m height create greater art/clearance risk. Not shortlisted; not downloaded. Seller disclosures about generated base geometry and marketplace AI metadata differ, requiring clarification if reconsidered.

**First next action, only after owner decision:** seek Dragon Pack seller confirmation of (1) permission for a publicly downloadable game GLB **and** raw source in this public GitHub project, (2) actual Blend/FBX ground-idle, folded-wing, takeoff, flight and landing actions, and (3) an uncut side/front preview with a 1.9 m rider reference, clear back/leg space and physical dimensions. No purchase until those gates are resolved. Ask the same license/contact questions for Ashwing Full only as fallback; use existing Lite measurements rather than repeat its audit. If neither supplier clears public distribution and mount geometry, retain **NO SUITABLE VERIFIED ASSET** rather than force a selection.

All implementation, saddles, new clips, skyport changes, gameplay and deployment remain untouched. Stop for owner approval.
