# S2-G rollback and review

Nothing was deployed. `dev-town=s2f` remains localhost-only and off by default. A public host cannot enable it.

- Open the local comparison at `http://127.0.0.1:4173/index.html?experience=adventure&dev-town=s2f&town-review=1`.
- **Glass A** restores the exact approved transmission material. Glass B/C are temporary review choices; they are not saved and a fresh page starts with A.
- **Clearance before** restores the S2-F vegetation placements and stone shadow materials while retaining the approved town. **Clearance after** restores the S2-G clearance corrections.
- **Town off** restores the original island instances, palm position, grass LODs, tree collision proxies, material references and original obstacle array. Assets remain cached for a reversible on switch.
- **Default experience**, or removing `dev-town` and `town-review` and reloading, starts the original game without requesting any town models or stabilization modules.

Pre-change checkpoint: `codex/checkpoint-s2f-before-s2g`, commit `05c9912153bdc80b85c1bd0ead9a5534fe2dc5ed`. Current branch, HEAD, working files and original staged changes were preserved during checkpoint creation.

For a code rollback to approved S2-F, restore only the modified existing files:

```sh
git restore --source=codex/checkpoint-s2f-before-s2g --worktree -- assets/js/floating-atlas/town-integration.js assets/js/floating-atlas/town-review.js tests/town-s2f.test.mjs
```

The new `assets/js/floating-atlas/town-stabilization.js` and `tests/town-s2g.test.mjs` may then be removed. Retain the review evidence. Do not reset the repository to its old HEAD: the approved earlier phases were uncommitted and are preserved in the checkpoint.

The existing local preview precompresses scripts at startup. After code rollback or editing, restart the documented local preview to refresh its script cache:

```sh
node scripts/serve-pages-preview.mjs --root . --port 4173
```
