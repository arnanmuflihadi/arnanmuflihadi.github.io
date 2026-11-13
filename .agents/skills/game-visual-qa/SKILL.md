---
name: game-visual-qa
description: "Review actual browser-based 3D game visuals for AR(N)AN: Three.js environments, architecture, street-level experience, matched screenshots, rendering quality, performance and phase acceptance. Use before submitting environment or architectural phases; not for ordinary text-only website changes."
---

# Game visual QA

Inspect what the real browser renders. Keep technical validation, provisional internal visual observations and owner acceptance separate.

Read the latest phase scope and `AGENTS.md`. Use [references/browser-evidence.md](references/browser-evidence.md) for the existing preview, camera, capture, regression and performance workflows. Reuse relevant installed frontend-testing and anti-slop guidance; this skill adds game/environment judgment rather than another browser automation framework.

## Workflow

1. Verify the actual local website and origin. Reuse a healthy preview server; otherwise start the documented repository preview. Confirm the intended build, active scene and approved baseline.
2. Capture real browser screenshots. Record URL/build, camera tuple, FOV, eye/support height, viewport, drawing buffer/DPR, quality and lighting. Default to at least 1280 × 720 review captures unless the task specifies another size. Keep generated mockups separate from implementation evidence.
3. Inspect full-world aerial, side/underside and actual third-person views. Include player-eye-height inspections at approximately 1.65 m above the relevant support, using the actual character for scale.
4. Check silhouettes, massing, facade rhythm, material hierarchy, window recesses, door dimensions, canopy clearance and roof detailing. Confirm visible geometry instead of relying on labels or source metadata alone.
5. Inspect road/paving continuity, street/plaza enclosure, frontage orientation and transitions to natural paths. Judge whether architecture and ground treatment read as one intentional place.
6. Inspect landmark hierarchy, vegetation variety and placement, lighting, contact shadows, sky and atmosphere. Keep approved environmental strengths visible in the review.
7. Detect missing textures, loading/console errors, clipping, floating geometry, blocked routes and inaccessible entrances. Verify support/collision with real controller movement; use existing diagnostics when relevant.
8. Compare before/after images with matched fixed cameras, scale, resolution, quality and lighting. Preserve approved evidence; use new run paths for new captures. Do not improve apparent quality by hiding defects through framing or postprocessing.
9. Run the relevant existing gameplay, architecture, asset and integration regressions. Preserve working movement/jumping/camera, renderer lifecycle, source licenses, research registry, Home/Work and `project=mbr`. Report actual commands/results and inherited failures separately; do not delete or skip failures to claim success.
10. Record actual GLB bytes, loaded instances, decoded textures, draw calls, triangles, resource inventory and active-walking frame timing. Distinguish file/potential totals from view-specific renderer counters and CPU submission from GPU cost. Keep viewport, quality, route and cache conditions explicit.

## Visual rubric and correction

Assess these eight criteria against the requested phase:

- World composition.
- Architectural coherence.
- Streetscape richness.
- Gameplay navigation clarity.
- Material and lighting quality.
- Environmental atmosphere.
- Visual identity and originality.
- Character-scale experience.

Any 1–5 score is a **provisional internal observation**, supported by specific images and defects. Mark unobserved criteria unverified; do not infer quality from passing tests. Owner acceptance targets an average of at least 4/5 with no criterion below 3/5. Never label internal scores as independent human review or award owner approval automatically.

After each inspection pass, identify the three highest-impact visible issues (or all if fewer). When correction is authorized, fix the underlying issue within that phase and recapture affected matched views. Repeat until addressed or a concrete blocker is recorded. For a final environment phase, use at least a massing/context pass and a separate pedestrian pass; add a targeted pass for remaining material, circulation or clipping defects. Do not turn a scoped audit into a rebuild.

For an explicitly read-only review or skill-installation dry-run, use existing actual browser captures, label them as prior evidence and report proposed corrections without editing the game or recapturing over approved files. Distinguish an asset showcase's settlement-readiness gap from a failure of previously approved natural terrain.

## Delivery and gate

Deliver linked screenshots and camera references, specific visual defects/corrections, test results, measured rendering costs and limitations. State separately what was freshly executed, what is historical evidence and what remains unverified. Preserve the prior evidence and report owner approval as pending unless the owner explicitly provides it. Stop at the requested phase boundary; a technical pass does not authorize the next phase.
