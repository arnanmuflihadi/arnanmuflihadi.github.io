# 06 — Assets, provenance, licences and the registry

## 1. Provenance register (preserved and extended)

[asset-provenance.csv](asset-provenance.csv) / [.json](asset-provenance.json) resolve **every downloaded model the kit instantiates** to its exact source file in the extracted pack, its size and SHA-256, the licence file that ships with the pack and its hash, and the licence condition. Rebuilt for the final kit by `p2a_provenance.py` from `kit-report.json`.

| | Batch 3 | Batch 4 |
|---|---|---|
| Downloaded assets resolved to a source file | 158 | **164** (all 164 source files found, none unresolved) |
| — Quaternius Medieval Village MegaKit [Standard] | | 63 |
| — Quaternius Fantasy Props MegaKit [Standard] | | 43 |
| — Avramania Free Low-Poly Medieval Collection | | 32 |
| — Syntaxes of Play Medieval Cafe Asset Pack | | 26 |
| Custom items (authored for this project) | 16 | **20** |
| New third-party packs | — | **none** |

**New in batch 4 (6, all from packs already in the register):** `AV-mdvl_interiors_chest_01` and `AV-mdvl_interiors_pottedplant_01` (Avramania Free Collection), `FP-Book_Stack_1` (Quaternius Fantasy Props), `SY-menu-stand01` (Syntaxes of Play), and two **colour variants** of Quaternius roof geometry, `MV-Roof_RoundTiles_4x6@dark` and `_8x8@dark` (the dark civic tile grade of batch 1 applied to two more roof sizes; the geometry is the downloaded model, only the material differs).

**Custom, authored here (20; 4 new):** `CUS-Hoist` (B13's loading jib), `CUS-Awning_tea` (sage-green awning), `CUS-Sign_Leaf_wood` (tea-sprig pictogram), `CUS-Sign_Crate_burgundy` (an existing glyph on a new field), plus the 16 of earlier batches (awnings, signs, bunting, seal, paving seal). They are flat-colour geometry with no third-party licence. The lean-to roofs, loggia, gallery and strongroom wing are **assemblies of downloaded modules**, not custom geometry.

**No new asset was downloaded in this batch, and no asset search was made;** the existing library covered every function, and the two details it could not provide (the jib, the sprig sign) were built as custom geometry.

## 2. Licence evidence

| Pack | Licence | Evidence |
|---|---|---|
| Quaternius Medieval Village MegaKit [Standard] | CC0 1.0 | `License_Standard.txt` in the archive, SHA-256 `ec6fd500…2de` |
| Quaternius Fantasy Props MegaKit [Standard] | CC0 1.0 | `License_Standard.txt`, SHA-256 `edad1224…bda` |
| Avramania Free Low-Poly Medieval Collection | CC0 1.0 | `License.txt`, SHA-256 `f84a514e…d3d`; the ReadMe states the models were built by scripts written with an AI coding assistant (not AI 3D generation); the packs whose ReadMe admits unidentified Tripo-AI meshes were rejected in P1.2 |
| Syntaxes of Play Medieval Cafe | CC0 1.0 **stated on the creator's page only** (no licence file in the archive) | the page copy captured in batch 3: `docs/planning/merchant-citadel/p2c-batch3/evidence/licence/sop-itch-page.html` (SHA-256 `5523da04…c46978`, retrieved 2026-11-12T08:52:38Z); the new SoP asset of this batch is from the same pack. **A page copy is evidence of a statement, not a licence file**; if the owner wants more than that, the creator can be asked for a licence text. |

Nothing was re-downloaded; the batch 3 capture stands and was not touched.

## 3. Palette

The P1.2 palette (burgundy, blue, gold, terracotta, cream) gained **one accent, tea green `#6F7F55`**, used only on E05's awnings (`CUS-Awning_tea`). It extends the approved palette and is the owner's to accept or remove (one line in `p2a_bazaar.py`).

## 4. Registry

[asset-registry.csv](asset-registry.csv) / [.json](asset-registry.json): **51 kit nodes** (44 in batch 3, plus the three building nodes A07w, A05c, A03cT, the new DRESSING_D7 and sign nodes for the new signs; DRESSING_D8 grew), triangles, vertices, primitives, materials, baked AO, sources, licence notes, collision groups, status "P2-B batch 4" for the new nodes. Kit total 516,528 unique triangles (batch 3: 420,575 for 44 nodes). Per node: B13 `A07w` 37,194; E04 `A05c` 31,628; E05 `A03cT` 24,606; `DRESSING_D7` 5,773. Against the P1.4 contract: B13 −12 %, E04 −15 %, E05 +197 % (two floors instead of one: 01).

## 5. Open points about sources

The same ones as before, unchanged: the Syntaxes of Play licence is a page statement; Avramania's pack was built with an AI coding assistant (disclosed, not AI 3D generation); Quaternius CC0 means no attribution is required, which the project nevertheless records. No new risk was introduced in this batch.
