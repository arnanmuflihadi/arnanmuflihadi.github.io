# R0-E1B review

E1B extends the local `town-story=r0e1` field note with Telaga Awan interpretation and Guild filing. Nadia, both scenarios, the 1/3 and 2/3 journals, incorrect-answer retry, Guild study and 3/3 completion were exercised in a real browser using the explorer. The final answer gate was tightened and retested from the saved first observation through the Guild. The original Guild study also remained available from Professional Mode without a file action. A browser reload preserved 3/3; the full case study opened and browser Back returned to the local review URL.

[Square interpretation](evidence/square-interpretation.jpg) · [Guild completion](evidence/guild-completion.jpg)

The full first run walked from spawn to Nadia, Lembaran, square and the Guild entrance before a cache refresh was needed for the new Guild panel; the final Guild submission was subsequently checked using the existing controller review walk. This is not an uninterrupted final-version completion-and-return recording. The E1A canopy occlusion near Nadia remains. Full six-link browser checks, mobile/touch, repeated-resource leak checks and a fresh matched off/on performance comparison were not completed. Owner visual approval remains pending.

Tests: `node --test tests/transit-quest.test.mjs tests/living-atlas.test.mjs tests/floating-atlas.test.mjs tests/atlas-guild.test.mjs tests/experience.test.mjs`: 25 passed. A real local 1280×656 DPR 1 Glass B camera rail, 2 s warmup / 12 s sample, measured 5.6 ms median, 11.2 ms p95, 338–417 all-pass calls, 2,545,684–2,624,244 triangles. It is not a controlled comparison with story off; CPU frame intervals are not GPU timings. No new binary assets were added.

Changed: `assets/js/floating-atlas/transit-quest.js`, `assets/js/floating-atlas/entry.js`, `assets/js/floating-atlas/minimap.js`, `assets/js/adventure-ui.js`, `assets/js/living-atlas-controller.js`, `assets/js/project-panel.js`, `tests/transit-quest.test.mjs`. Added this validation directory. The approved town and research data were not changed.

For runtime rollback, remove `town-story=r0e1`. Exact E1A copies of the files potentially touched by E1B are in `baseline/`; validate with `shasum -a 256 -c validation/transit-e1b/baseline/SHA256SUMS` and restore only those files to undo this phase. Preserve unrelated work. No deployment.
