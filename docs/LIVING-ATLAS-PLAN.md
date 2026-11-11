# Living Urban Atlas — Phase 0 audit and Phase 1–2 plan

The working branch is `codex/jakarta-experience`. Existing uncommitted work is
retained. The site is a static multipage GitHub Pages portfolio; no framework or
publishing changes are needed. Six research routes and their map assets exist.

## Findings

- Home/Work currently invoke an early isolated RPG through experience-controller.
  Its renderer and project panels are separate from the newer Urban Atlas preview.
- Urban Atlas already has an authored ten-building Jakarta district, original
  parametric shell/arcade architecture, a genuine CC0 Quaternius skinned explorer,
  displacement-matched animations, collision, floor support and follow camera.
- The current mount eagerly loads the character before displaying the district.
  It has no cinematic/editorial camera owner, and cannot progressively present the
  same scene before control is requested.
- GSAP/Lenis and old decorative Three.js renderers own Home's previous hero.
  The pinned work rail is incompatible with a new shared scroll-camera owner.
- The shared registry is usable but the old toggle creates a disconnected canvas
  and duplicate header. The native project drawer can be reused after extracting
  it from game-specific mission/progress code.
- Existing static audit has 58 inherited failures, documented previously. Any new
  differences must be identified rather than reporting that audit as passing.

## Implementation order

1. Verify the suggested city/nature/road assets and import a small, suitable free
   subset with provenance. Keep designed Indonesian landmarks and the existing
   licensed character. Do not add combat animations or later-phase systems.
2. Refactor the Atlas mount into one persistent scene/renderer with editorial and
   adventure camera owners. Present the city before loading the character. Only
   first control activation downloads the character GLB. Retain/resume its state.
3. Add authored cinematic presets and registry-linked scroll chapters to Home and
   Work, using the existing semantic project content and ordinary links. Keep a
   static poster and all professional content usable without WebGL or JavaScript.
4. Replace the early integration controller with one shared mode/project/history
   controller. Keep the existing site header in both modes. Use the same drawer,
   same district and same renderer; no separate game screen or cover/load page.
5. Add compact gameplay minimap, landmark prompts, controls and safe focus/scroll
   ownership. No NPCs, quests, monsters, travel, other regions or gliding.
6. Validate actual scene identity across camera handoffs, lazy character loading,
   deep links/history, project context, resume position, collision, mobile layout,
   reduced-motion/error paths and source-backed research. Capture editorial and
   gameplay views of the same environment and inspect them.

## First-gate limits

Jakarta is the only constructed region. Other projects remain fully readable and
use a clearly labeled research-pavilion camera composition, not invented regional
scenes or geographic results. Phase 3 onward remains unimplemented pending review.

## Execution record

Phase 1–2 implementation and local validation completed on 31 October 2026.
See [current architecture and assets](LIVING-ATLAS.md) and the
[executed QA record and screenshots](LIVING-ATLAS-QA.md). Visual acceptance by the
user remains the gate before any later phase. No deployment was performed.
