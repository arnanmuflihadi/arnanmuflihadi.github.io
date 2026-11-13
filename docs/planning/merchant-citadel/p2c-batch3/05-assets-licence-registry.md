# 05 — Assets, licence evidence and registry

## 1. Syntaxes of Play: the open licence item is closed as far as the page allows

The P1.2 and P2-B registers carried one open item: the CC0 statement for the Syntaxes of Play "Medieval Cafe Asset Pack" came from the creator's page and no dated copy was kept; the archive has no licence file. The page was reachable and is now captured: [evidence/licence/README.md](evidence/licence/README.md), the saved page `sop-itch-page.html` (27,808 bytes, SHA-256 `5523da04...c46978`), retrieved 2026-11-12T08:52:38Z. It states "This asset pack is released under the CC0 1.0 Universal license ... free for both personal and commercial use. Attribution is not required", and that no generative AI was used. **What it does not do:** it is a web page, not a licence file inside the download, and it cannot prove that this archive is byte-identical to the page's current download. 25 of the 158 downloaded assets in the kit are from this pack.

## 2. Source and licence register

| | Count |
|---|---|
| Downloaded models instantiated by the kit, resolved to a file in an extracted archive with its SHA-256 | **158 of 158, none unresolved** |
| Of them new in this batch | **25** (list below) |
| By pack | Quaternius Medieval Village 61, Quaternius Fantasy Props 42, Avramania 30, Syntaxes of Play 25 |
| Custom (authored for this project, no third-party geometry) | 16: awnings in blue, burgundy, cream and **gold (new)**, seven-pictogram trade signs, guild seal, paving seal, bunting |
| Licence files shipped inside the archives (hash recorded) | Quaternius x2 (CC0), Avramania (CC0, `License.txt`) |

Files: [asset-provenance.csv](asset-provenance.csv) / [.json](asset-provenance.json) (column `new_in_batch3`), [asset-registry.csv](asset-registry.csv) / [.json](asset-registry.json). The earlier provenance (batch 2: 134 assets) is preserved unchanged in `../p2b-batch2/`. **No pack was added**; the new assets come from packs already in the register. The Avramania note from batch 2 stands: its ReadMe says some meshes were built by script with an AI coding assistant; the packs whose ReadMe admits unidentified AI meshes remain rejected.

### New downloaded assets in batch 3

| Asset | Pack | Placements | Source SHA-256 (first 12) |
|---|---|---|---|
| `AV-mdvl_dungeon_chest_01` | Avramania | 1 | `b82402c65c8a` |
| `AV-mdvl_interiors_anvil_01` | Avramania | 1 | `b1ffaf5f4a0d` |
| `AV-mdvl_interiors_pot_01` | Avramania | 1 | `ea323f3630bb` |
| `AV-mdvl_interiors_woodpile_01` | Avramania | 3 | `ff7104c618c8` |
| `AV-mdvl_nature_stump_01` | Avramania | 1 | `34a48815a1e7` |
| `AV-mdvl_props_axe_01` | Avramania | 1 | `d711d1c005de` |
| `AV-mdvl_props_barrel_01` | Avramania | 2 | `81a0d98865e2` |
| `AV-mdvl_props_basket_01` | Avramania | 1 | `d7208a8435f8` |
| `AV-mdvl_props_cart_wheel_01` | Avramania | 1 | `1b981e5c5b29` |
| `AV-mdvl_props_hammer_01` | Avramania | 2 | `c0e546fcae94` |
| `AV-mdvl_props_pot_01` | Avramania | 1 | `fa169cb32919` |
| `AV-mdvl_props_rope_coil_01` | Avramania | 1 | `36c713f2c804` |
| `AV-mdvl_props_signpost_01` | Avramania | 1 | `dba6d7f4c5d0` |
| `AV-mdvl_props_water_trough_01` | Avramania | 2 | `b0d6f77f68db` |
| `AV-mdvl_village_ladder_01` | Avramania | 1 | `f09bcd461872` |
| `FP-Anvil_Log` | Quaternius | 1 | `878f803a0d8d` |
| `FP-Banner_1@cream` | Quaternius | 1 | `a00162c8ef35` |
| `FP-Peg_Rack` | Quaternius | 2 | `7fa0747b6225` |
| `FP-Pickaxe_Bronze` | Quaternius | 1 | `2a934389f826` |
| `FP-Rope_1` | Quaternius | 1 | `b4722ec5baf1` |
| `FP-WeaponStand` | Quaternius | 1 | `039675f0ea79` |
| `FP-Whetstone` | Quaternius | 1 | `ec0f5173ac53` |
| `FP-Workbench` | Quaternius | 2 | `518fc5c955de` |
| `MV-Roof_RoundTiles_4x8` | Quaternius | 1 | `a33d41c743c8` |
| `SY-basket-of-jars` | Syntaxes of Play | 1 | `9fde82d27cd8` |

`MV-Roof_RoundTiles_4x8` is the shallow carrier's-office roof (A03c, E02), a P1.4 module first instantiated by this kit; `FP-Banner_1@cream` is the lane-entrance banner of the P1.4 dressing, now inside D6.

## 3. Custom vs downloaded (disclosure)

* **Custom:** the gold awning colour, the guild seal on the hall's inner gables (the seal is the same object as outside), trade signs, bunting, cloth awnings. Authored in `citadel_lib.py` (P1.4).
* **Composed from downloaded modules, not downloaded as such:** the potter's kiln (three scaled `MV-Wall_UnevenBrick_Straight`, a `MV-Floor_UnevenBrick` cap, `MV-Prop_Chimney`), the three lean-to bays (`MV-Roof_Wooden_2x1` modules on `MV-Corner_Exterior_Wood` posts), all arrangements of goods.
* **Graded or altered:** paving textures warmed (1.03, 0.96, 0.84 and 1.31, 1.00, 0.80 linear multipliers) at export; module LOD on eight props (collapse decimation to 600-1,400 triangles); cloth colour variants as before.

## 4. Registry

44 kit nodes: 16 P2-A, 5 P2-B batch 1, 16 P2-B batch 2, 7 P2-B batch 3. Kit triangles 420,575 (batch 2: 336,528); the five district nodes account for 78,137 of the +84,047, the Western Hall for -1,424, and the district dressing (D1, D6), signs and a smaller D3 dressing for the rest. Registry columns: node, archetype, purpose, status, instances, triangles, vertices, primitives, materials, baked AO, sources, licence notes, P1.4 readiness, collision groups.
