# 03 - External asset inventory update (P1.4)

The P1.2 inventory (918 inspected models, hashes and licences in `../p1/02`, `../p1/03`, `../p1/04`) remains the base. P1.4 changes it as follows.
Evidence: [new-asset-evidence-sheet.png](visuals/new-asset-evidence-sheet.png); list: [03b-asset-inventory-additions.csv](03b-asset-inventory-additions.csv).

## Sources examined in P1.4

| Source | What was done | Result |
|---|---|---|
| Alefran - Medieval Stylized Assets pack (free), alefrandev.itch.io | Downloaded from the creator's free path (358,158,805 bytes, SHA-256 `b225ad59d154a265...`), 33 glTF models extracted, licence file read, five models imported and measured | **Not adopted.** Textured and close in style, with a street lamp, a stall and a sign that the town lacks. But `Free version license.txt` allows commercial use while limiting modification to personal use and forbidding redistribution "even if modified". A public browser game serves its model files and P2 must optimise them, so the terms do not fit. The street lamp alone is a 34 MB file |
| WizP - Stylized Medieval Village, itch.io | Page read (CC0 stated, with a contradictory "can't be resold" line; three palette materials); download attempted | **Not obtained.** The free path listed no upload. Flat palette style, so it would not have suited the architecture |
| skfod - Stylized Medieval Market, itch.io | Page read | **Rejected unseen:** CC BY-ND and a minimum price |
| KayKit Medieval Hexagon | Page read | **Rejected unseen:** hex-tile strategy miniatures, the same family as the Medieval Builder Pack measured in P1.2 (buildings about 1 m tall) |
| Louis J. Sullivan - Stylised Street Market (UE4 project), itch.io | Page read (it is reference R04) | **Not usable as assets:** no licence stated; Unreal project format |
| Quaternius, other packs | Site listing checked | No further fantasy-town pack; the three MegaKits already in use are the relevant ones |

**Conclusion of the search:** no free, clearly licensed pack offers architecture or street furniture in a style that sits beside the Quaternius kit. The gain in P1.4 comes from the kit's own unused modules and from five small custom elements.

## Downloaded models first used in P1.4 (2)

`MV-Balcony_Cross_Straight`, `MV-Roof_RoundTiles_8x10`

All are from packs already verified (CC0). The roof `8x10`, the cross-braced balustrade and the plinth use of the stair skirt are the notable ones.

## Custom geometry (authored for this project, not downloaded)

| Item | What it is | Triangles each | Placed |
|---|---|---|---|
| `CUS-Awning_blue` | striped cloth awning bay, 2 m | 48 | 23 |
| `CUS-Awning_burgundy` | striped cloth awning bay, 2 m | 48 | 14 |
| `CUS-Bunting_10` | line of pennants | 42 | 1 |
| `CUS-Bunting_18` | line of pennants | 75 | 2 |
| `CUS-PavingSeal` | guild seal inlaid in the paving, 3.2 m | 266 | 2 |
| `CUS-Seal_NiagaAwan` | guild seal | 440 | 16 |
| `CUS-Sign_Coin_burgundy` | hanging trade sign | 164 | 3 |
| `CUS-Sign_Coin_wood` | hanging trade sign | 164 | 1 |
| `CUS-Sign_Crate_wood` | hanging trade sign | 92 | 3 |
| `CUS-Sign_Cup_wood` | hanging trade sign | 116 | 3 |
| `CUS-Sign_Hammer_wood` | hanging trade sign | 116 | 2 |
| `CUS-Sign_Jar_wood` | hanging trade sign | 140 | 3 |
| `CUS-Sign_Loaf_wood` | hanging trade sign | 116 | 2 |
| `CUS-Sign_Scroll_burgundy` | hanging trade sign | 104 | 1 |
| `CUS-Sign_Scroll_wood` | hanging trade sign | 104 | 3 |

79 placements, 12,120 triangles in total (1.3% of the town). New in P1.4: the awning, the pennant line and the paving seal. Flat colours from the palette; no texture.

## Multi-source coherence

Architecture, roofs, paving, lamps and fences: Quaternius only. Counters, tables and goods: Syntaxes of Play and Avramania (as P1.2). Cloth and signs: custom, flat-coloured.
The weakest join is the custom cloth beside hand-painted textures; it is acceptable at street distance and should receive a woven texture in P2 (13).
