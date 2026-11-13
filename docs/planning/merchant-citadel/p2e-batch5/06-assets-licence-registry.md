# 06 — Assets, provenance, licences and the registry (batch 5)

## 1. Provenance

[asset-provenance.csv](asset-provenance.csv) / [.json](asset-provenance.json), regenerated for the final kit by `p2a_provenance.py` from `kit-report.json`: every downloaded model the kit instantiates resolved to its source file, size, SHA-256 and the licence file in the pack.

| | Batch 4 | Batch 5 |
|---|---|---|
| Downloaded assets resolved to a source file | 164 | **170** (170 of 170 found, none unresolved) |
| — Quaternius Medieval Village MegaKit [Standard] | 63 | 67 |
| — Quaternius Fantasy Props MegaKit [Standard] | 43 | 43 |
| — Avramania Free Low-Poly Medieval Collection | 32 | 34 |
| — Syntaxes of Play Medieval Cafe Asset Pack | 26 | 26 |
| Custom items (authored for this project) | 20 | **23** |
| New third-party packs | — | **none** |

**New in batch 5 (downloaded, all from packs already registered):** `AV-mdvl_food_coin_stack_01`, `AV-mdvl_interiors_workbench_01` (Avramania), `MV-Prop_Vine5` (Quaternius), and three roof geometries in the new **weathered** colour grade (`MV-Roof_RoundTiles_4x6@weathered`, `_4x8@`, `_6x6@`): Quaternius geometry, only the material grade differs.
**New custom, authored here (flat-colour geometry, no third-party licence):** `CUS-AssayBalance`, `CUS-MapBoard`, `CUS-Sign_Compass_wood`.
The leaf sign (`CUS-Sign_Leaf_*`) was redrawn; the glyph shapes are mine.
Disclosure: custom geometry is 23 of the kit's items; the building shells and almost all dressing are assemblies of downloaded modules.

**No asset was downloaded in batch 5, no asset search was made, no paid or AI-generated asset was used** (the Blender MCP's `generate_3d` and `import_asset` were not called).

## 2. Licence evidence

Unchanged from batch 4 and not re-fetched: Quaternius Medieval Village and Fantasy Props MegaKits [Standard] CC0 1.0 (licence files hashed `ec6fd500…` and `edad1224…`); Avramania Free Low-Poly Medieval Collection CC0 1.0 (`f84a514e…`; the ReadMe says the models were built by scripts written with an AI coding assistant, which is not AI 3D generation; packs with unidentified AI meshes were rejected in P1.2); Syntaxes of Play Medieval Cafe CC0 1.0 **stated on the creator's page only** (no licence file in the archive; the batch 3 page copy `p2c-batch3/evidence/licence/sop-itch-page.html` is evidence of a statement, not a licence file).

## 3. Registry

[asset-registry.csv](asset-registry.csv) / [.json](asset-registry.json): **54 nodes**, 602 primitives, **588,064 unique triangles**. Revision label "P2-B batch 5"; statuses A11a (31,804 triangles), A11c (34,578) and the compass sign node are "P2-B batch 5". Nodes modified in batch 5 but created earlier (A07w, A05c, A03cT, the terrace and warehouse dressing, roof grades) keep the status of the batch that created them; the per-node change is in `01`. **Known registry blemishes:** the provenance flag column is still named `new_in_batch4` (in this file it is `True` for the six assets new in batch 5 and `False` for batch 4's; the name was kept to keep the CSV schema stable).

## 4. Palette

P1.2 palette plus the tea-green accent `#6F7F55` introduced in batch 4 (E05 awnings), still the owner's to accept or remove. Batch 5 adds no new palette colour; the weathered roof grade is a muted variant of the existing terracotta.
