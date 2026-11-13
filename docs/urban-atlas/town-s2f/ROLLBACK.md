# S2-F rollback

The default and every public origin exclude the town. This is a localhost-only opt-in; nothing was deployed.

- Review: `http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&town-review=1`
- Normal game: remove `dev-town` and `town-review` from the URL and reload. Its original session store is separate.
- Immediate in-place rollback: open the S2-F review controls and choose **Town off**. This detaches all town visuals, restores the exact original obstacle array, restores the four showcase planting transforms, and switches the existing explorer back to original terrain support. Loaded files remain cached; **Town on** reuses them.
- **Default experience** removes both development parameters and reloads the original experience without requesting the town GLBs.

Local version-control checkpoint: `codex/checkpoint-s2e-before-s2f`, commit `3f9e479fb0e656ee563fd9ec66ed2bfbac73c1aa`. It snapshots the complete pre-integration non-ignored working tree. The active branch, HEAD and original staged changes were preserved.

To remove the integration code, restore only these two existing files from that checkpoint, then remove the three newly added `town-*.js` modules:

```sh
git restore --source=codex/checkpoint-s2e-before-s2f --worktree -- assets/js/floating-atlas/entry.js assets/js/living-atlas-controller.js
```

Do not reset to the old HEAD or restore the entire repository: approved earlier phases were uncommitted before this checkpoint. Keep the evidence, manifests and approved source archives. The updated preservation tests have explicit before/after hashes for the two authorized seams; when removing the code, also restore the two modified preservation tests from the checkpoint. The new S2-F test and `tests/helpers/production-preservation.mjs` can then be removed with the integration.

The local preview compresses text at startup. Restart `node scripts/serve-pages-preview.mjs --root . --port 4173` after source changes, otherwise it may serve stale compressed scripts.
