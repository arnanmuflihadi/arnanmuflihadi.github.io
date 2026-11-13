#!/usr/bin/env python3
"""Write the Merchant Citadel P1.1 planning documents. Narrative is authored here; every table and number comes from
the measured data (layout, archetypes, archetype report, town stats, model measurements, archive manifest, validation).
Usage: python3 make_docs.py <inspection_dir> <package_dir>
"""
import json, math, os, re, sys, collections

I, P = sys.argv[1], sys.argv[2]
L = json.load(open(f"{I}/data/layout.json")); ARCH = json.load(open(f"{I}/data/archetypes.json"))
AREP = json.load(open(f"{I}/archetypes/archetype-report.json")); STATS = json.load(open(f"{I}/renders/town-stats.json"))
MEAS = json.load(open(f"{I}/measurements.json")); MAN = json.load(open(f"{I}/archives/archive-manifest.json")); VAL = json.load(open(f"{I}/validation.json"))
S0 = json.load(open(f"{I}/p1.0/town-stats.json")); L0 = json.load(open(f"{I}/p1.0/data/layout.json"))
PFX = {"quaternius-medieval-village": "MV", "quaternius-fantasy-props": "FP", "quaternius-stylized-nature": "SN", "kenney-fantasy-town-kit": "KFT", "kenney-modular-buildings": "KMB"}
DATE = "2026-11-11"


def tbl(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]) + "\n"


def w(name, text):
    os.makedirs(os.path.dirname(f"{P}/{name}") or P, exist_ok=True)
    open(f"{P}/{name}", "w").write(text.strip() + "\n")


count = collections.Counter(m["pack_id"] for m in MEAS); man = {m["pack_id"]: m for m in MAN}
ADV = {"quaternius-medieval-village": 304, "quaternius-fantasy-props": 211, "quaternius-stylized-nature": 116, "kenney-fantasy-town-kit": 160, "kenney-modular-buildings": 100}
NAME = {"quaternius-medieval-village": "Quaternius Medieval Village MegaKit", "quaternius-fantasy-props": "Quaternius Fantasy Props MegaKit",
        "quaternius-stylized-nature": "Quaternius Stylized Nature MegaKit", "kenney-fantasy-town-kit": "Kenney Fantasy Town Kit 2.0", "kenney-modular-buildings": "Kenney Modular Buildings 2.1"}
ZIP = {"kenney-fantasy-town-kit": "kenney_fantasy-town-kit.zip", "kenney-modular-buildings": "kenney_modular-buildings.zip"}
U, TE = STATS["usage"], dict(STATS["tris_each"])
for _m in MEAS:   # triangles of every downloaded model by base id, so variants and unused bases resolve too
    TE.setdefault(f"{PFX[_m['pack_id']]}-{_m['asset_name']}", _m["triangle_count"])
for _a in list(TE):
    TE.setdefault(_a.split("@")[0], TE[_a])
used_models = {a.split("@")[0] for a in U if not a.startswith("CUS-")}
used_by_pack = collections.Counter(a.split("-")[0] for a in used_models)
x0, x1, n0, n1 = L["envelope"]; rx0, rx1, rn0, rn1 = L["reserved"][0][1:]
ux0, ux1, un0, un1 = min(x0, rx0), max(x1, rx1), min(n0, rn0), max(n1, rn1)
nb, ns = len(L["buildings"]), len(L["stalls"])
arche_n = collections.Counter(b["archetype"] for b in L["buildings"])
STATUS = {"A01": "READY", "A02": "READY", "A03": "READY", "A03b": "READY", "A04": "READY", "A04b": "READY", "A05": "READY", "A06": "READY", "A07": "READY", "A08": "READY"}
edges = []
for a, b, kind in L["edges"]:
    (xa, na, _), (xb, nb2, _) = L["nodes"][a], L["nodes"][b]
    edges.append((a, b, kind, round(math.hypot(xa - xb, na - nb2), 1)))
net_total = round(sum(e[3] for e in edges), 1)
prim = round(sum(e[3] for e in edges if e[0:2] in [("N01", "N02"), ("N02", "N03"), ("N03", "N04"), ("N04", "N05"), ("N05", "N29"), ("N29", "N27"), ("N27", "N06"), ("N06", "N07"), ("N07", "N08")]), 1)
loops = len(edges) - len(L["nodes"]) + 1
SUM = VAL["summary"]; ENV = {a["id"]: a for a in VAL["A_envelopes"]}
SEALS = U.get("CUS-Emblem_NiagaAwan", 0); DORMERS = U.get("MV-Roof_Dormer_RoundTile", 0)
EXCESS = max(max(x0 - e["full_x"][0], e["full_x"][1] - x1, n0 - e["full_n"][0], e["full_n"][1] - n1) for e in ENV.values())
base_mats = sorted({re.sub(r"\.\d+", "", m) for m in STATS["materials"]})
ST = VAL["E_stairs"]; AR = VAL["F_arch"]
hang = [c for c in VAL["C_hanging"] if c["clearance_m"] is not None and c["over_paving"]]
cam = VAL["G_camera"]

# quantified optimisation projection ------------------------------------------------------------------
ACTIONS = [("FP-Lantern_Wall", 600, "simplified bracket lantern (flat chain, 8-sided cage)"), ("MV-Corner_Exterior_Brick", 300, "simplified quoin pier, same silhouette"),
           ("SN-CommonTree_3", 1500, "lower-detail tree for the backdrop ring"), ("SN-CommonTree_1", 1500, "lower-detail tree for the backdrop ring"),
           ("FP-FarmCrate_Apple", 600, "produce as a textured mound"), ("FP-FarmCrate_Carrot", 600, "produce as a textured mound"), ("SN-Bush_Common_Flowers", 500, "fewer leaf cards"),
           ("MV-Door_8_Round", 400, "flatten studs and ring into the texture"), ("FP-Crate_Wooden", 230, "swap for MV-Prop_Crate (existing model, measured 230)"),
           ("MV-Balcony_Simple_Straight", 132, "swap for MV-Balcony_Cross_Straight (existing model, measured 132)"), ("FP-Stall_Cart_Empty", 1500, "simplify wheel and frame"),
           ("FP-Barrel", 300, "12-sided barrel"), ("FP-Bag", 300, "simplified sack"), ("SN-TwistedTree_2", 3000, "lower-detail feature tree")]
ACT = {a: (t, why) for a, t, why in ACTIONS}


def project(usage, tris_each):
    cur = sum(tris_each.get(a, TE.get(a, 0)) * n for a, n in usage.items()); new = 0
    for a, n in usage.items():
        e = tris_each.get(a, TE.get(a, 0)); base = a.split("@")[0]
        new += n * (min(e, ACT[base][0]) if base in ACT else e)
    return cur, new


TOWN_CUR, TOWN_NEW = project(U, TE)
PAVE = sum(n * TE[a] for a, n in U.items() if a.startswith("MV-Floor_"))
opt_rows = []
for a, (t, why) in ACT.items():
    n = sum(v for k, v in U.items() if k.split("@")[0] == a)
    if n:
        e = TE[a]; opt_rows.append([f"`{a}`", n, f"{e:,}", f"{n * e:,}", f"{t:,}", f"{n * (e - t):,}", why])
opt_rows.sort(key=lambda r: -int(r[5].replace(",", "")))

# =============================================================================================== README
w("README.md", f"""
# Merchant Citadel / Kota Niaga Awan - P1 planning package (revision P1.1)

**Status: MERCHANT CITADEL P1.1 - PENDING HUMAN VISUAL APPROVAL.** Planning and concept only. Dated {DATE}. P2 has not started.

P1.1 is a targeted correction of P1, not a new plan. It keeps the 17 buildings, the street network and the Quaternius building system, and
changes five things: the town now has a guild identity, the composition is tighter, spatial checks run on the real geometry, the known
architectural defects are fixed, and the feasibility numbers are reconciled and quantified. What changed, file by file, is in
[14-p1.1-change-log.md](14-p1.1-change-log.md).

| # | Document | P1.1 |
|---|---|---|
| 01 | [Design bible](01-design-bible.md) | Identity vocabulary added |
| 02 | [External asset research](02-external-asset-research.md) | Unchanged findings; no new search |
| 03 | [Verified asset inventory](03-verified-asset-inventory.csv), [custom and variant register](03b-custom-and-variant-register.csv) | Register of non-downloaded items is new |
| 04 | [Source and licence register](04-source-license-register.md) | Unchanged (hashes preserved) |
| 05 | [Architectural direction and material specification](05-architectural-direction.md) | Signage, canopy and hierarchy rules added |
| 06 | [Revised measured masterplan](06-measured-town-masterplan.md) | Revised |
| 07 | [Building schedule](07-building-placement-schedule.csv), [stall schedule](07b-market-stall-schedule.csv) | Revised, with measured envelopes |
| 08 | [Archetype specifications](08-archetype-specifications.md) | Revised |
| 09 | [Walking network and spatial validation](09-walking-network.md) | Validation on actual geometry is new |
| 10 | [Terrain interface contract](10-terrain-interface-contract.md) | Support zone corrected |
| 11 | [Visual QA report, before and after](11-visual-qa-report.md) | Rewritten as a comparison |
| 12 | [P2 construction contract](12-p2-construction-contract.md) | Revised, with a quantified optimisation plan |
| 13 | [Limitations and risks](13-limitations-and-risks.md) | Updated |
| 14 | [P1.1 change log and approval dependencies](14-p1.1-change-log.md) | New |

## Visuals

| File | Evidence class |
|---|---|
| [view-a-aerial.png](visuals/view-a-aerial.png), [view-b-merchant-street.png](visuals/view-b-merchant-street.png), [view-c-central-bazaar.png](visuals/view-c-central-bazaar.png), [view-d-exchange-court.png](visuals/view-d-exchange-court.png) | ASSET-BACKED BLENDER BLOCKOUT, P1.1 (one town, four cameras) |
| [before-after-a-aerial.png](visuals/before-after-a-aerial.png), [-b-](visuals/before-after-b-merchant-street.png), [-c-](visuals/before-after-c-central-bazaar.png), [-d-](visuals/before-after-d-exchange-court.png) | P1.0 beside P1.1, same camera (C moved 3.9 m, stated on the image) |
| [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png), [archetype-roof-plans.png](visuals/archetype-roof-plans.png) | ASSET-BACKED ASSEMBLY, front, rear and roof plan of all twelve assemblies |
| [orthographic-town-plan.png](visuals/orthographic-town-plan.png) | Measured drawing generated from layout data and measured envelopes |
| [blockout-top-orthographic.png](visuals/blockout-top-orthographic.png) | ASSET-BACKED BLENDER BLOCKOUT (top view) |
| [real-asset-contact-sheet.png](visuals/real-asset-contact-sheet.png) | REAL ASSET RENDER (unchanged from P1.0) |
| [visuals/p1.0/](visuals/p1.0/) | The P1.0 images, kept for comparison |

## What is and is not downloaded geometry

- **Downloaded, as authored:** {len(used_models)} Quaternius models ({STATS['instances'] - sum(n for a, n in U.items() if a.startswith('CUS-') or '@' in a):,} instances).
- **Material variants of downloaded models:** {STATS['material_variant_ids']} ids; only the cloth material is tinted (teal, saffron, gold, cream). Geometry unchanged.
- **Stretched downloaded model:** the plain timber post, 1.3x and 1.6x in height, for lamp posts and lane standards.
- **Custom, authored in P1.1:** one item, the guild seal `CUS-Emblem_NiagaAwan` ({U.get('CUS-Emblem_NiagaAwan', 0)} instances, {STATS['triangles_custom']:,} triangles in total).
- **Temporary, never an asset:** flat green ground, dark interior boxes, the teal 1.9 m explorer.

All of it is itemised in [03b-custom-and-variant-register.csv](03b-custom-and-variant-register.csv). No AI-generated image is in this package.

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1/blender-inspection; B=/Applications/Blender.app/Contents/MacOS/Blender
python3 $S/fetch_archives.py $D/archives            # free archives only; unzip each into $D/extracted/<pack_id>/
$B --background --factory-startup --python $S/measure_assets.py -- $D/extracted $D/measurements.json
python3 $S/town_data.py $D/data                     # nominal checks
$B --background --factory-startup --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/data/archetypes.json $D/archetypes
$B --background --factory-startup --python $S/build_town.py -- $D/extracted $D/measurements.json $D/data $D/renders $D/blender/merchant-citadel-p1-blockout.blend
$B --background --factory-startup --python $S/validate_envelopes.py -- $D/blender/merchant-citadel-p1-blockout.blend $D/data $D/validation.json
python3 $S/make_package_assets.py $D docs/planning/merchant-citadel/p1 && python3 $S/make_docs.py $D docs/planning/merchant-citadel/p1
```
The before/after images need the P1.0 renders kept in `$D/p1.0/`.
""")

# =============================================================================================== 01
w("01-design-bible.md", f"""
# 01 - Design bible (P1.1)

## Vision

Kota Niaga Awan is the trading town of the Niaga Awan guild. A visitor passes between two gate lodges, follows a band of dressed brick
(the guild way) up a street of shopfronts, reaches a bazaar gathered around the guild's market cross, and climbs to the Exchange Hall,
whose tower carries the guild seal. Workshops, the guild warehouse and a tea terrace sit on side routes. The Exchange Hall is the home
of the CBD and commercial-clustering research.

## Identity vocabulary (deliberately small)

| Element | Rule | Where |
|---|---|---|
| **Guild seal** | One original emblem: gold rim, teal field, eight-point compass star (the Atlas compass), coin at the centre. It marks what the guild runs, and nothing else | Exchange Hall portal and tower, both market halls, gateway lodges, warehouse, market cross ({U.get('CUS-Emblem_NiagaAwan', 0)} placements) |
| **Guild teal** | Civic cloth only | Exchange Hall banners, registry office sign, warehouse-lane standards |
| **Saffron** | Market cloth only | Market hall banners, stall canopies (with cream and the shipped red-brown) |
| **Madder red** | Private trade, as shipped | One hanging sign per shop; artisan-lane standards |
| **Guild way** | A 4 m band of dressed brick along the whole axis from arrival court to civic court | Guidance and identity in one move |
| **Market cross** | Timber guild standard on a stone block with two seals and two lanterns | Centre of the bazaar, on the hall-to-hall cross-passage |

Three accent colours, one emblem, one paving band. The shipped blue banner is no longer used anywhere.

## Hierarchy of building classes

| Class | How it reads |
|---|---|
| Ordinary shops | Plaster and timber, one or two storeys, one red sign, shutters; gable-fronted shophouses carry a timber shopfront canopy |
| Market halls | No walls: a timber arcade under a large roof, seal on each gable, saffron banners, goods inside |
| Exchange Hall | Only building with a stone ground floor across a 26 m front, a podium, wings, a triple portal, teal banners and a tower through the roof |
| Guild service buildings | Warehouse (stone, seal on the gable, loading dormers), registry (teal sign) |

## What P1.1 did not do

It did not force Indonesian-tropical architecture, add palms, or add decoration for its own sake. The supplied concept images remain
ILLUSTRATIVE; the differences are listed in 13.

## Lessons from the first island, applied

| Earlier problem | Response |
|---|---|
| Buildings placed without a plan | Coordinates, frontage and a paved approach for every building, checked on real geometry |
| Mismatched styles | One kit for all architecture |
| Weak streets and frontage | Two straight frontage lines 10 m apart; fenced back courts give the lanes a second edge |
| No landmark hierarchy | Tower with the seal closes the 75 m axis |
| Images that could not be built | Every render is assembled from the downloaded models; the one custom item is named as custom |
""")

# =============================================================================================== 02 / 04 / evidence
rows = [[NAME[pid], ADV[pid], count[pid], f"{man[pid]['bytes'] / 1e6:.1f} MB", used_by_pack.get(PFX[pid], 0), "Selected" if not pid.startswith("kenney") else "Rejected for this town"] for pid in PFX]
w("02-external-asset-research.md", f"""
# 02 - External asset research

**P1.1 note:** no new asset search and no new download were made. The archives, hashes and model identifiers are those of P1.0. The
"used" column is updated for the P1.1 blockout.

All archives were downloaded on {DATE} from the publishers' own distribution, then imported and measured in Blender 5.2.3
(`measure_assets.py`). Catalogue figures are the publishers' advertising; the "in free archive" column is what was counted.

{tbl(["Pack", "Advertised models", "Models in free archive (imported)", "Archive size", "Unique models used in the P1.1 blockout", "Decision"], rows)}
All {len(MEAS)} models imported without error and every referenced texture loaded.

## How each archive was obtained

- **Quaternius.** quaternius.com links each pack to its official itch.io page, which lists `[Standard].zip` (free), `[Pro].zip` (US$9.99 or more)
  and `[Source].zip` (US$14.99 or more). Only the Standard upload was requested. The in-archive licence file states it is "the standard FREE version".
- **Kenney.** kenney.nl serves each kit through its own "Continue without donating" link.
- **OpenGameArt mirrors** returned HTTP 403 to automated requests and were not used.

## Findings that shaped the design

1. **Medieval Village is a complete building system**: 2 m wall bays, 3 m storeys, plaster / half-timber / rough-stone walls with matching doors and
   windows, 17 ready-made tile roofs for 4, 6 and 8 m spans, gables, a tower roof, dormers, chimneys, a timber shopfront canopy, stairs, balconies.
2. **The modules are in metres and suit the 1.9 m explorer as authored.** Door leaves are 1.12 x 2.10 m (flat) and 2.32 m (round).
3. **No complete building exists in any free archive.** Every shell is an assembly.
4. **Fantasy Props has two stall models, one canopy colour, no awnings and no street lamps.**
5. **Stylized Nature has no palms or tropical plants.**
6. **Kenney's kits are a different scale and style** (1.0 unit walls, flat pastel colours).
7. `Roof_Front_Brick*` are plaster-and-timber gables despite the name.
8. Models are open-edged game meshes (non-manifold edges on every model).

## Gaps and how P1.1 answers them without new downloads

| Wanted | Free archives | P1.1 answer |
|---|---|---|
| Coloured canopies | One colour | Four cloth tints of the shipped material (disclosed variants) |
| Shopfront awnings | None in cloth | The kit's timber canopy `Roof_Wooden_2x1_L/Center/R` on gable-fronted shophouses |
| Street lamps | None | Timber post stretched 1.3x in height plus `Lantern_Wall` (disclosed) |
| A civic emblem | None | One custom seal (disclosed) |
| Civic centrepiece | None | Market cross composed from a stair block, a post, lanterns and the seal |
| Palms, tropical planting | None | Not pursued, by owner direction |
| Collision meshes | Not in Standard | Box proxies per building in P2 |
""")
rows = [[NAME[pid], man[pid]["publisher"], man[pid]["edition"], man[pid]["source_page"], man[pid]["distribution"], "CC0 1.0 (file inside archive)", ZIP.get(pid, man[pid]["archive_filename"]),
         f"{man[pid]['bytes']:,}", f"`{man[pid]['sha256']}`"] for pid in PFX]
w("04-source-license-register.md", f"""
# 04 - Source and licence register

Unchanged in P1.1: no new source, download or licence.

{tbl(["Pack", "Publisher", "Edition", "Source page", "Distribution used", "Licence", "Archive", "Bytes", "SHA-256"], rows)}
- Licence confirmed on the publisher page, on the distribution page, and in the licence file inside each archive ([asset-evidence/license-evidence.md](asset-evidence/license-evidence.md)).
- CC0 covers use. It does not make the paid Pro or Source uploads free to download, and none were accessed.
- Kenney's signed links deliver a file named by hash; it was saved under the names above.
- Per-model provenance: [03-verified-asset-inventory.csv](03-verified-asset-inventory.csv). Items that are **not** downloaded geometry: [03b-custom-and-variant-register.csv](03b-custom-and-variant-register.csv).
""")
w("asset-evidence/archive-manifest.md", "# Archive manifest\n\nDownloaded by `blender-inspection/fetch_archives.py`. Archives are kept outside Git in `.asset-inspection/merchant-citadel-p1/archives/`. Unchanged in P1.1.\n\n"
  + tbl(["pack_id", "archive", "bytes", "sha256", "downloaded (UTC)", "uploads listed on the free download page"],
        [[m["pack_id"], ZIP.get(m["pack_id"], m["archive_filename"]), m["bytes"], f"`{m['sha256']}`", m.get("downloaded_utc", ""), "; ".join(m.get("listed_uploads", [])) or "n/a (single signed link)"] for m in MAN])
  + "\nModels counted after extraction and import: " + ", ".join(f"{NAME[p]} {count[p]}" for p in PFX) + ".\n")

# =============================================================================================== 05
WT = (0.35, 0.25, 0.20, 0.15, 0.05)
cands = [("A - Asset-native fantasy town", (5, 5, 4, 3, 4)), ("B - Cozy adventure merchant town", (3, 4, 4, 5, 4)), ("C - Unified merchant citadel (chosen)", (5, 4, 5, 4, 5))]
w("05-architectural-direction.md", f"""
# 05 - Architectural direction and material specification (P1.1)

The direction chosen in P1.0 stands: **C - Unified Merchant Citadel**, one family from the Quaternius Medieval Village kit.

{tbl(["Candidate", "Verified modules 35%", "Construction efficiency 25%", "Coherence 20%", "Third-person readability 15%", "Reuse 5%", "Weighted"], [[n, *s, f"**{sum(a * b for a, b in zip(s, WT)):.2f}**"] for n, s in cands])}
P1.1 does not change the system. It adds an identity layer made of material variants, existing geometry and one small custom detail.

## Architectural identity contract

| Element | Rule | Verified modules |
|---|---|---|
| Roof silhouettes | Three street orientations now mix: gable to street, eaves to street, and the hall's long ridge. Dormers and chimneys break the larger roofs | `Roof_RoundTiles_*`, `Roof_Dormer_RoundTile`, `Prop_Chimney`, `Prop_Chimney2` |
| Walls, light | Cream plaster with timber frame | `Wall_Plaster_*` |
| Walls, heavy | Rough stone ground floor: corner houses, workshops, warehouse, and now the whole Exchange Hall | `Wall_UnevenBrick_*` |
| Corners | Stone pier at ground level of stone buildings, timber post above and on plaster buildings | `Corner_Exterior_Brick`, `Corner_ExteriorWide_Wood` |
| Shopfront | Door bay beside a wide window with open shutters; timber canopy on gable-fronted shophouses | `Roof_Wooden_2x1_L / _Center / _R` |
| Market canopy | Open timber arcade under a full tile roof | `Wall_Arch`, `Roof_RoundTiles_8x12` |
| Landmark | Stone base, triple portal, wings, tower through the ridge, podium deck | 08, A01 |
| Paving | Cobble for streets and plaza; dressed brick for the guild way, halls and civic court; red brick for the artisan lane and tea terrace | `Floor_UnevenBrick`, `Floor_Brick`, `Floor_RedBrick` |

## Signage and banner system

| Class | Cloth | Model | Mounting rule |
|---|---|---|---|
| Civic (guild) | Teal | `FP-Banner_2_Cloth@teal`, `FP-Banner_2@teal` | Flat banners between upper windows of the hall; one bracket sign on the registry; lane standards |
| Market | Saffron | `FP-Banner_1@saffron` | Four bracket banners per hall, on the corners |
| Private trade | Madder red (as shipped) | `FP-Banner_1` | Exactly one bracket sign per shop, lowest edge 2.65 m or higher |
| Guild seal | Gold and teal | `CUS-Emblem_NiagaAwan` (custom) | Guild-run buildings and the market cross only; 0.8 to 1.9 m across |

Stall canopies use three cloths: gold (saffron family), cream, and the shipped red-brown. Lowest measured hanging edge over any walkable surface: **{hang[0]['clearance_m']} m** (09).

## Material specification

Downloaded materials used as authored: {", ".join(f"`{m}`" for m in base_mats if not m.startswith(("CUS", "MI_Banner@")))}.

| Added in P1.1 | Type | Definition |
|---|---|---|
| `MI_Banner@teal` | Variant | Shipped cloth texture, hue -0.13, value x0.95 |
| `MI_Banner@saffron` | Variant | Hue +0.075, saturation x1.15, value x1.75 (tuned for the red banner cloth) |
| `MI_Banner@gold` | Variant | Hue +0.035, saturation x1.25, value x1.55 (tuned for the brown canopy cloth) |
| `MI_Banner@cream` | Variant | Hue +0.09, saturation x0.32, value x1.75 |
| `CUS_guild_gold`, `CUS_guild_teal` | Custom flat materials | Gold (0.83, 0.60, 0.16), metallic 0.55; teal (0.035, 0.33, 0.35) |

That is **{len(base_mats)} distinct materials** in the town. The Blender scene holds {STATS['material_count']} material slots because the importer duplicates a
material for every model it loads; P2 must merge them back to these {len(base_mats)} (12).

Principal compromise, unchanged: this is a European half-timber language with its own guild identity, not the Indonesian-tropical look of the earlier islands.
""")

# =============================================================================================== 06
FR = {0: "south", 90: "east", -90: "west", 180: "north"}
old = {b["id"]: b for b in L0["buildings"]}
brow, changes = [], []
for b in L["buildings"]:
    e = ENV[b["id"]]; o = old[b["id"]]
    brow.append([b["id"], b["archetype"], b["label"], f"({b['x']}, {1.0 if b['archetype'] == 'A01' else 0.0}, {-b['n']})", b["rz"], FR[b["rz"]],
                 f"{b['rect'][1] - b['rect'][0]:g} x {b['rect'][3] - b['rect'][2]:g}", f"{e['full_size'][0]} x {e['full_size'][1]}"])
    ch = []
    if o["archetype"] != b["archetype"]: ch.append(f"archetype {o['archetype']} to {b['archetype']}")
    if (o["x"], o["n"]) != (b["x"], b["n"]): ch.append(f"centre ({o['x']}, {-o['n']}) to ({b['x']}, {-b['n']})")
    if o["rz"] != b["rz"]: ch.append(f"rotation {o['rz']} to {b['rz']}")
    if ch: changes.append([b["id"], b["label"], "; ".join(ch)])
WHY = {"B03": "Both halls now face the same way so their cross-passage bays line up on z = -49", "B05": "Turned eaves-to-street (A03b) to vary the roofline; alley to B04 widened to 3 m",
       "B06": "Moved north to close the gap to the bazaar; 0.5 m back from the plaza edge after validation found the bazaar path grazing its side window",
       "B08": "Turned eaves-to-street (A04b); alleys widened to 3.5 m", "B09": "Moved north to meet the bazaar edge", "B10": "Shifted 1 m south so its roof clears B11",
       "B11": "Turned eaves-to-lane (A04b) for roof variety", "B12": "Shifted north so its roof clears B11", "B17": "Moved 1 m north to make room for the 2 m veranda"}
pav = [[p[0], f"{p[1]}..{p[2]}", f"{-p[4]}..{-p[3]}", f"{p[2] - p[1]} x {p[4] - p[3]}", p[5]] for p in L["paving"]]
w("06-measured-town-masterplan.md", f"""
# 06 - Revised measured town masterplan (P1.1)

Drawing: [visuals/orthographic-town-plan.png](visuals/orthographic-town-plan.png). Data: `blender-inspection/town_data.py`. This revises the P1.0
masterplan in place; the street network, districts and building count are the same.

## Coordinates

Metres. Origin = centre of the arrival court. Plan axes: x = east, n = north. Project / Three.js: **(x, y, z) = (x, elevation, -n)**, +y up.
`rotation_y`: 0 = front faces south (+z), 90 = east, -90 = west, 180 = north.

## Size

Developed envelope (nominal): x {x0}..{x1} ({x1 - x0} m), z {-n1}..{-n0} ({n1 - n0} m). With the transport reservation: {ux1 - ux0} x {un1 - un0} m (10).

## Programme

**{nb} permanent buildings, 8 archetypes (two with an eaves-to-street variant), {ns} market stalls, 1 split gateway, 1 market cross.**
Stalls rose from 10 to 12 to hold the four bazaar quadrants; the count stays inside the brief's 8-12.

## What changed in the plan, and why

{tbl(["ID", "Building", "Change"], [[c[0], c[1], c[2] + ". " + WHY.get(c[0], "")] for c in changes])}
| Other element | Change | Reason |
|---|---|---|
| Gateway G01 | One roofed pavilion across the street became two lodges either side of a 4 m lane open to the sky, moved from z = -8.5 to z = -5 | The old roof blocked the follow camera; the first P1.1 position overlapped two roofs by 0.6-1.2 m (found by validation) |
| Market cross M01 | New, at (0, 0, -49) | Gives the bazaar a centre and a guild marker; sits on the hall-to-hall cross-passage |
| Stalls | 10 in two straight rows became 12: eight in four quadrants, two at the south band, two at the north band | The 10 m bare aisle is now 9.0 m between stall fronts, divided by the market cross into two 3.5 m lanes, with a cross-passage |
| Market hall interiors | Tables moved outward and regrouped; the bay at z = -49 is kept clear | Makes a walkable route through each hall |
| Guild way | New 4 m dressed-brick band on the axis, z = 0 to -62 | Guidance and identity |
| Lanes | Artisan lane in red brick with five lamps and yard fences; warehouse lane with fences and teal standards | Lanes had one built side and no edge |
| Back courts | Fences, trees, crates and a wagon between street buildings and lanes | Leftover strips become yards |
| Walking nodes | N23/N24 moved, N25/N26 added; N21 and N22 are now reached across the civic court paving | The old N23-N21 and N24-N22 links crossed unpaved ground and clipped building corners |
| Tea terrace | Veranda floor paved; furniture moved off the route | Validation found the approach unpaved and blocked |

## Building positions, nominal footprint and measured envelope

{tbl(["ID", "Archetype", "Name", "Position (x, y, z)", "rotation_y", "Front faces", "Nominal footprint on plan (m)", "Measured envelope incl. roof, signs, props (m)"], brow)}
The measured envelope is the axis-aligned bound of everything attached to the building in the assembled scene. It is what must be kept clear, and it
is drawn dashed on the plan. Roofs overhang the wall lines by 0.8 to 1.1 m on each side. Full figures: [07-building-placement-schedule.csv](07-building-placement-schedule.csv).

## Paved surfaces (2 m tiles; later rows overlay earlier ones)

{tbl(["Surface", "x", "z", "Size (m)", "Tile"], pav)}
Reserved, no construction: future transport pad x -10..10, z 8..24.

## Checks

- Nominal checks (`town_data.py`): **{"PASS" if L["checks_pass"] else "FAIL"}** - footprint overlaps, clear corridors, paved entrance approaches, stalls on paving, graph connectivity.
- Checks on actual geometry (`validate_envelopes.py`): reported in 09. Roof gaps failing: {SUM['roof_gaps_fail']}; hanging objects too low: {SUM['hanging_fail']}; walking edges failing: {SUM['edges_fail']} of {SUM['edges_total'] - 1} built.
""")

# =============================================================================================== 08
CODE_LEGEND = "P plaster, G half-timber grid, F/R/T plaster window (wide flat / wide round / thin round), D/O plaster door (flat / round), I inset round portal, S stone, s/r stone window, o/d stone door, A open timber arch, X no module (hidden face or floor below the roof)"
NOTES = {
    "A01": ("Dominant civic landmark and research venue", "P1.1: tower moved to the centre of the plan and its walls start above the roof, so roof and tower meet on four symmetric lines and the front eave is intact. Podium is one brick deck on a continuous stone skirt (was 112 blocks). Stone ground floor and triple portal added.",
            "Box proxies: main 14 x 8 x 6, tower 4 x 4 above 10 m, wings 6 x 6 x 6, podium 28 x 16 x 1; stairs as five 0.2 m steps or one ramp proxy", "Guild seal (custom) x3"),
    "A02": ("Covered market, used twice", "P1.1: seal on both gables, saffron banners, regrouped tables, one bay kept clear as a cross-passage. Arch opening measured 1.67 m wide, 2.74 m high.", "Post proxies only; arcade stays walkable", "Guild seal (custom) x2"),
    "A03": ("Two-storey shophouse, gable to the street", "P1.1: timber shopfront canopy, one dormer, chimney; sign raised to 5.9 m.", "One box 6 x 8 x 6; canopy non-colliding (low edge 2.44 m)", "None"),
    "A03b": ("Two-storey shophouse, eaves to the street (variant of A03, same modules)", "New in P1.1 for roofline variety. Two dormers on the street slope.", "One box 8 x 6 x 6", "None"),
    "A04": ("Single-storey shop, gable to the street; registry office", "Unchanged. The registry instance swaps its red sign for a teal one.", "One box 4 x 6 x 3", "None"),
    "A04b": ("Single-storey shop, eaves to the street (variant of A04, same modules)", "New in P1.1.", "One box 6 x 4 x 3", "None"),
    "A05": ("Heavy corner building with two active fronts", "P1.1: stone piers on the ground floor only (timber posts above), dormer, chimney, both signs red.", "One box 8 x 8 x 6", "None"),
    "A06": ("Stone workshop with outdoor work area", "P1.1: forge chimney and a trade sign.", "One box 6 x 6 x 3 plus prop proxies", "None"),
    "A07": ("Guild warehouse with paired doors and loading yard", "P1.1: three dormers, seal on the gable, piers on the ground floor only.", "One box 8 x 14 x 6", "Guild seal (custom) x1"),
    "A08": ("Tea house with a veranda", "P1.1: the balcony is now a 6 x 2 m deck with front and end rails carried on four posts to the ground, replacing the unsupported 1 m shelf.", "One box 6 x 6 x 6; four post proxies; deck not walkable in P2", "None"),
}
out = ["# 08 - Archetype specifications (P1.1)\n",
       "Module ids prefixed MV- / FP- exist in the downloaded archives and are instanced at authored scale on a 2 m / 3 m grid with 90-degree rotations. Ids with `@` are cloth-tint material variants. `CUS-Emblem_NiagaAwan` is custom P1.1 geometry. See 03b.\n",
       f"Facade codes: {CODE_LEGEND}. Strings read left to right from outside, one per floor.\n",
       "Renders: [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png) (front and rear), [archetype-roof-plans.png](visuals/archetype-roof-plans.png) (roof junctions from above).\n",
       "**Shared assembly order:** (1) 2 m grid and 3 m storey; (2) ground-floor wall bays per facade string; (3) window inserts, door leaves, shutters; (4) corner piers or posts per floor; (5) upper floors; (6) gable infills; (7) prefab roof at wall-top height; (8) dormers and chimney seated on the slope; (9) canopy, sign, lantern, seal, props.\n"]
for a in ["A01", "A02", "A03", "A03b", "A04", "A04b", "A05", "A06", "A07", "A08"]:
    A, R = ARCH[a], AREP[a]; purpose, change, coll, custom = NOTES[a]
    roofs = ", ".join(sorted({p.get("roof_asset", "MV-Roof_RoundTiles_" + p["roof"])[3:] if p.get("roof") else "Roof_Tower_RoundTiles" for p in A["parts"]}))
    out.append(f"## {a} - {A['name']}\n")
    out.append(tbl(["Field", "Value"], [
        ["Purpose", purpose], ["Instances planned", arche_n[a]], ["Nominal footprint (m)", f"{A['footprint'][0]} x {A['footprint'][1]}" + (f" + {A['front_extra']} m veranda" if A.get("front_extra") else "")],
        ["Measured bounds incl. roof and props (m)", f"{R['measured_bounds_m'][0]} x {R['measured_bounds_m'][1]} x {R['measured_bounds_m'][2]} high"], ["Floors", A["floors"]], ["Roof", roofs],
        ["Source", "Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF"], ["Scale / rotation", "1.0; 0, 90, 180, 270 degrees"],
        ["Module instances", f"{R['instances']} ({R['unique_assets']} ids)"], ["Triangles, unoptimised", f"{R['triangles']:,}" + (f" (of which custom {R['triangles_custom']:,})" if R.get("triangles_custom") else "")],
        ["Triangles after the P2 substitutions (projection)", f"{project(R['usage'], {})[1]:,}"], ["P1.1 change", change], ["Collision", coll], ["Custom geometry", custom], ["Readiness", STATUS[a]]]))
    out.append(tbl(["Block", "W x D (m)", "Floors", "Roof", "Offset (x, y, z)", "front", "right", "back", "left"],
                   [[p["id"], f"{p['W']} x {p['D']}", f"{p['floors']}" + (f" (walls from level {p['floor_from'] + 1})" if p.get("floor_from") else ""), p.get("roof") or ("tower" if p.get("tower_roof") else "-"),
                     p.get("offset", [0, 0, 0]), *[" / ".join(p["facades"].get(s, ["-"])) for s in ("front", "right", "back", "left")]] for p in A["parts"]]))
    out.append("**Modules (id x count):** " + ", ".join(f"`{k}` x{v}" for k, v in sorted(R["usage"].items(), key=lambda kv: -kv[1])) + "\n")
for key, title, txt in (("GATE", "G01 - Gerbang Niaga split gateway (structure)", "Two open timber lodges, each 2 x 4 m with arches on all sides and a small gabled roof (`Roof_2x4_RoundTile`, `Roof_Front_Brick2`), flank a 4 m lane open to the sky. Seal on each south gable. Readiness: READY."),
                        ("CROSS", "M01 - Tugu Timbangan market cross (structure)", "One stair block as a 2 x 2 x 1 m base, one timber post, two seals, two bracket lanterns at 2.4 m, goods at the foot. Readiness: READY.")):
    R = AREP[key]
    out.append(f"## {title}\n\n{txt} {R['instances']} instances, {R['triangles']:,} triangles, measured {R['measured_bounds_m'][0]} x {R['measured_bounds_m'][1]} x {R['measured_bounds_m'][2]} m.\n\n"
               + ", ".join(f"`{k}` x{v}" for k, v in sorted(R["usage"].items(), key=lambda kv: -kv[1])) + "\n")
out.append("## Market stall kits\n\n" + tbl(["Kit", "Base model", "Canopy", "Goods and props", "Collision footprint (m)"],
           [[k, v["base"].split("@")[0], (v["base"].split("@")[1] + " (variant)") if "@" in v["base"] else "as shipped", ", ".join(p[0] for p in v["props"]), "3.1 x 1.2" if k.startswith("S02") else "1.9 x 1.0"] for k, v in L["stall_kits"].items()])
           + "\nCounter height set by eye at 0.93 m (not measured from the mesh). Readiness: READY with the three canopy cloths.\n")
out.append("""## Assembly notes: junctions checked in P1.1

| Junction | State |
|---|---|
| Exchange Hall tower and main roof | **Fixed.** Tower walls begin at level 4, above the roof surface; the roof passes into the tower's dark core. No eave is cut |
| Exchange Hall wings and main block | Wing ridges (10.9 m) sit below the main roof's gable overhang; wing roofs run 1 m into the main gable wall. Intended telescoping; hidden inside the wall |
| Podium | **Fixed.** One brick deck; stone skirt on all four sides including behind the stair flanks |
| Tea house balcony | **Fixed.** Deck, three rails and four posts form a complete veranda |
| Dormers | Seated so the dormer ridge meets the slope; the cheeks sink into the tiles by a few centimetres |
| Chimneys | Shafts pass through the slope without a flashing piece. Acceptable at gameplay distance; noted |
| Gable infill and roof | Infill sits inside the roof's barge boards; small overlap at the verge by design of the kit |
| Stone piers and wall trims | Timber wall trims run into the stone pier at corners (2-3 cm overlap) |
| Timber canopy and shutters | Open shutters stand under the canopy; no intersection |
| Gate lodge roofs | 2.7 m apart across the lane; clear of B04 and B07 by 1.3 m and 1.5 m |
""")
w("08-archetype-specifications.md", "\n".join(out))

# =============================================================================================== 09
drow = [[d["edge"], d["type"], d["length_m"], d["unpaved_samples"], d["max_step_m"], d["min_headroom_m"] if d["min_headroom_m"] else "open sky", d["min_side_clearance_m"], d["status"]] for d in VAL["D_edges"]]
fwd = ["N01->N02", "N02->N03", "N03->N04", "N04->N05", "N05->N29", "N29->N27", "N27->N06", "N06->N07", "N07->N08"]
camrow = [[g["travel"], g["type"], f"{g['unobstructed_pct']}%", g["min_camera_distance_m"], ", ".join(b.split("_")[0] for b in g["main_blockers"]) or "-"] for g in cam if g["unobstructed_pct"] < 100]
camrow.sort(key=lambda r: r[3])
gaps = [[g["a"], g["b"], g["gap_m"], g["status"]] for g in VAL["B_roof_gaps_under_3m"]]
w("09-walking-network.md", f"""
# 09 - Walking network and spatial validation (P1.1)

## Technical constraints read from the project (configuration only)

| Item | Value | Source |
|---|---|---|
| Axes and units | +y up, metres, GLB/glTF through `GLTFLoader` | `assets/js/vendor/three-atlas.module.js` |
| Explorer | 1.9 m tall, collision radius 0.34 m, maximum step 0.42 m | `player-controller.js`, `floating-atlas/collision.js` |
| Movement | walk 2.1 m/s, run 4.6 m/s | `player-controller.js` |
| Camera | FOV 60, 11.8 m behind, +6.6 m, looks at player +1.25 m; shortened to (hit distance - 0.28 m), minimum 0.8 m | `urban-atlas/camera.js` |

The production controller and camera were not modified or run. Their constants were copied into `validate_envelopes.py`.

## Two layers of checking

1. **Nominal** (`town_data.py`): footprint rectangles, clear corridors, paved approaches, graph connectivity. Result: {"PASS" if L["checks_pass"] else "FAIL"}.
2. **Actual geometry** (`validate_envelopes.py`, new in P1.1): the assembled Blender scene, {VAL['triangles_tested']:,} triangles, tested with ray casts and nearest-surface queries.
   Raw results: [asset-evidence/spatial-validation-actual-geometry.json](asset-evidence/spatial-validation-actual-geometry.json).

## A. Gaps between real building envelopes (roof overhangs included)

All pairs closer than 3 m:

{tbl(["A", "B", "Gap (m)", "Status"], gaps)}
Rule: under 0.3 m fails, under 1.0 m is narrow. **No pair fails.** The first P1.1 layout had two overlaps (gateway roofs against B04 and B07, -0.63 and -1.17 m);
the gateway was moved. P1.0's 2.5 m alleys, which left about 0.2 m between roofs, are now 3 to 3.5 m.

## B. Physical walkability of every edge

Each edge is sampled every 0.25 m. At each sample: a downward ray must find a paved tile or stair; the rise from the previous sample must be 0.42 m or less;
no geometry may lie within 0.34 m of the body axis at 0.5, 1.0, 1.5 and 1.85 m; headroom must be 2.0 m or more.

{tbl(["Edge", "Type", "Length (m)", "Unpaved samples", "Largest step (m)", "Least headroom (m)", "Nearest obstacle at 1 m height (m)", "Result"], drow)}
**{SUM['edges_total'] - 1 - SUM['edges_fail']} of {SUM['edges_total'] - 1} built edges pass.** The reserved link to the future transport pad is unpaved by design.
The first P1.1 run failed seven built edges: planting and furniture on four paths, a shop's side window on the bazaar's south-west path, and the tea-house
approach leaving the paving. All were corrected in the layout and re-tested. The tightest passages are beside the market cross (0.4 to 0.6 m to its goods).

### The two transitions named in the review

N23-N21 and N24-N22 no longer exist. In P1.0 they ran from the bazaar corners diagonally to the court sides, across 1 m of unpaved ground and through the
corners of B15 and B16. Each is replaced by two paved edges through new court entrances: N23-N25-N21 and N24-N26-N22. Both pass.

## C. Exchange Hall stair approach (edge N07-N08)

Measured risers: {", ".join(f"{r:.2f}" for r in ST['risers_m'])} m. **{ST['riser_count']} risers, largest {ST['max_riser_m']:.3f} m against the 0.42 m limit, total rise {ST['total_rise_m']:.2f} m.**
The approach is paved from the court to the podium deck with no gap. Whether the controller climbs it smoothly is an engine test for P2.

## D. Lanterns and banners

All {len(VAL['C_hanging'])} lanterns and banners were measured against the surface beneath them. Rule: 2.1 m or more over walkable paving.

| Lowest five over paving | On | Clearance (m) |
|---|---|---|
""" + "\n".join(f"| `{c['asset']}` | {c['on'].split('_')[0]} | {c['clearance_m']} |" for c in hang[:5]) + f"""

**None is below 2.1 m.** P1.0's lamp-post lanterns hung at about 1.6 m inside the walking line. They are now on 3.9 m posts with the lantern at 2.5 m,
set 0.7 m outside the street's clear width with the arm along the frontage. The first P1.1 run also caught the tea-house sign 1.34 m above the veranda deck; it was moved to the side wall.

## E. Market hall arch opening (`MV-Wall_Arch`, measured on the mesh)

Clear width {AR['clear_width_at_1.0m']} m from the ground to 1.9 m, {AR['clear_width_at_2.2m']} m at 2.2 m; clear height at the centre {AR['clear_height_centre_m']} m.
The 0.68 m wide, 1.9 m tall explorer passes with about 0.5 m each side. Edges N18-N31, N31-N30, N19-N32 and N32-N29 walk through arches and pass.

## F. Follow-camera line of sight

For every edge and both directions of travel, a ray is cast from the look-at point (player +1.25 m) to the documented camera position (11.8 m behind, +6.6 m).
Full distance is {cam[0]['full_distance_m']} m.

- **{SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']} travel directions are completely unobstructed.**
- **The whole primary axis, walking towards the hall, is unobstructed** except the 6 m after the market cross, where the cross's post stands between player and camera (camera shortens to 3.4 m, then recovers). The P1.0 gateway roof problem is gone.
- Where the camera does shorten:

{tbl(["Travel", "Type", "Samples unobstructed", "Shortest camera distance (m)", "Blocked by"], camrow)}
These are the expected cases: walking away from a facade the player is standing against (court sides, hall podium, tea house), and walking under a roof (market halls, veranda).
Under the hall roofs the camera settles at about 2.3 to 2.9 m. The game's own collision set may differ from this ray test (it may ignore thin banners and posts), so P2 must repeat it in the engine.

## Nodes

{tbl(["Node", "x", "z", "Place"], [[k, v[0], -v[1], v[2]] for k, v in L["nodes"].items()])}
{len(L["nodes"])} nodes, {len(edges)} edges, {loops} independent loops, {net_total} m in total. Primary route from arrival to the hall podium: **{prim} m**, about {prim / 2.1:.0f} s walking or {prim / 4.6:.0f} s running.

## Vertical design

Flat at y = 0 except the Exchange Hall podium (+1.0 m, five risers over 2.08 m). No ramp module exists in the kit.
""")

# =============================================================================================== 10
w("10-terrain-interface-contract.md", f"""
# 10 - Terrain interface contract (P1.1; no island is modelled)

Sequence: approve town, construct buildings, assemble town, derive the terrain envelope, sculpt the island around the settlement.

## Measured requirements

| Requirement | Value |
|---|---|
| Developed envelope (paving and nominal footprints) | x {x0}..{x1}, z {-n1}..{-n0} ({x1 - x0} x {n1 - n0} m) |
| Future transport reservation | x {rx0}..{rx1}, z {-rn1}..{-rn0} ({rx1 - rx0} x {rn1 - rn0} m), level, joined to node N01 |
| **Combined footprint the terrain must carry** | x {ux0}..{ux1}, z {-un1}..{-un0} (**{ux1 - ux0} x {un1 - un0} m**) |
| Largest measured building envelope beyond the developed envelope | Roofs overhang wall lines by 0.8-1.1 m; the furthest any measured envelope reaches outside the developed envelope is {EXCESS:.2f} m |
| Base elevation | y = 0.0 for every street, court, lane, building floor and the reservation |
| Only raised surface | Exchange Hall podium, y = +1.0, x -14..14, z -90..-74 |
| Building foundation zones | The 17 measured envelopes in 07; each needs a level pad at y = 0 |
| Lookout orientation | Terrace faces east (+x); fence line x = 46 and z = -44 |

**Correction in P1.1:** the P1.0 support zone was drawn around the developed envelope only (94.5 x 118 m) and left the southern half of the transport
reservation outside it. The zone below includes the reservation.

## Assumptions (to confirm in P4)

| Assumption | Value |
|---|---|
| Terrain support zone | Combined footprint plus 10 m on every side: **{ux1 - ux0 + 20:.1f} x {un1 - un0 + 20:.0f} m** of buildable, near-level ground (x {ux0 - 10}..{ux1 + 10}, z {-un1 - 10}..{-un0 + 10}) |
| Cliff exclusion | No cliff edge, drop or waterfall inside the support zone, except beside the lookout |
| Lookout exception | The island edge may come to about 3 m east and south of the terrace fence |
| Arrival side | If the transport pad becomes a landing or dock, the island edge may meet its south side; that replaces the 10 m margin there |
| Likely island size | About 115 x 155 m or larger; silhouette not fixed |

Not created: island mesh, cliffs, waterfalls, underside, terrain export.
""")

# =============================================================================================== 11
QA = [("Architectural coherence", 4, 4, "Still one kit and one roof material. Variety now comes from three roof orientations, dormers, chimneys and stone on the hall, without leaving the family."),
      ("Asset feasibility", 4, 4, "Everything is still assembled from downloaded models, now with real-geometry validation. Held at 4: one custom emblem, cloth tints and stretched posts are needed, and nothing has been loaded in Three.js."),
      ("Spatial organisation", 4, 4, "Lanes have a second edge, back strips are yards, the bazaar has quadrants and a centre. Held at 4: lanes are still built on one side and the plan is loose at the east."),
      ("Player-scale credibility", 4, 4, "Now measured rather than judged: all edges walkable, stairs 0.18-0.22 m, arches 1.67 m, nothing hanging below 2.27 m, camera clear on the axis. Held at 4 until tested in the engine."),
      ("Exchange Hall hierarchy", 4, 4, "Stone base, triple portal, seal and a tower that crosses the roof make it a different class of building. Held at 4: at the gameplay camera on the street the tower top is out of frame, and the hall is still built from house parts."),
      ("Market functionality", 3, 4, "Three canopy colours, twelve stalls in quadrants, a market cross, a cross-passage through both halls, goods inside the halls. Still only two stall models."),
      ("Environmental identity", 3, 4, "A guild seal, three cloth colours with fixed meanings and a brick guild way give the town its own vocabulary. It is a fantasy trading town with an owner now, not a generic village; it is still not tropical."),
      ("Visual polish", 3, 3, "Unchanged limits of a blockout: flat ground and sky, simple light, visible tile repetition, no terrain or backdrop. Paving now has three types."),
      ("Performance suitability", 3, 3, f"Triangles fell from {S0['triangles']:,} to {STATS['triangles']:,} while content was added, and a quantified plan projects {TOWN_NEW:,}. Nothing has been measured in a browser, so the score does not move.")]
a0 = sum(q[1] for q in QA) / len(QA); a1 = sum(q[2] for q in QA) / len(QA)
w("11-visual-qa-report.md", f"""
# 11 - Visual QA report: P1.0 and P1.1 compared

Reviewed: the four ASSET-BACKED BLENDER BLOCKOUT views of each revision from the same cameras (View C moved 3.9 m north because two buildings now
stand at its P1.0 position), the archetype sheets and roof plans. These are Blender EEVEE renders, **not browser renders**. Scores are internal and provisional.

Side by side: [A aerial](visuals/before-after-a-aerial.png), [B merchant street](visuals/before-after-b-merchant-street.png), [C bazaar](visuals/before-after-c-central-bazaar.png), [D Exchange Hall](visuals/before-after-d-exchange-court.png).

{tbl(["Criterion", "P1.0", "P1.1", "What changed, and why the score is what it is"], QA)}
**Average {a0:.2f} to {a1:.2f} out of 5.** Seven criteria are at 4. The two at 3, visual polish and performance, cannot be raised inside a Blender blockout:
polish needs terrain, backdrop and the game's lighting; performance needs a browser measurement. The 4 / 5 target is therefore not claimed, and
**human approval is pending**.

## Review points and their resolution

| Review point | P1.0 | P1.1 |
|---|---|---|
| Generic medieval village | No emblem, banners in shipped red and blue | Guild seal in {SEALS} places on guild-run structures; teal, saffron, red with fixed meanings; guild way |
| Shops, halls and hall look alike | Same walls everywhere | Shops plaster with canopy and red sign; halls open arcade with seal and saffron; Exchange Hall stone-based with tower and teal |
| Bazaar too open | 10 m bare aisle, ten identical stalls | Market cross at the centre, four stall quadrants, two 3.5 m lanes past the cross, cross-passage, three canopy colours |
| Market interiors underused | Six tables each | Regrouped tables, goods, barrels, bench, a walkable route through each hall |
| Empty space between buildings | Bare strips | Fenced back courts with trees, crates, a wagon |
| Weak lanes | One-sided, same cobble | Red-brick lantern lane with five lamps; warehouse lane with fences and standards |
| Repetitive roofs | All gables to the street, bare slopes | Three orientations, {DORMERS} dormers across four archetypes, chimneys on six |
| Tower cuts the roof | Front tower intersected the eave | Tower crosses the ridge; roof plan in [archetype-roof-plans.png](visuals/archetype-roof-plans.png) |
| Podium seams | 112 blocks | One deck, continuous skirt |
| Balcony unsupported | 1 m shelf with a front rail | 2 m veranda on four posts with three rails |
| Low lanterns | 1.6 m at lamp posts | Lowest hanging object 2.27 m |
| Gateway and camera | Roof across the path | Split gateway, lane open to the sky |

## Defects found by P1.1's own validation and corrected

Gateway roofs overlapping B04 and B07; tea-house sign 1.34 m above the veranda deck; four paths blocked by planting or furniture; the bazaar's south-west
path grazing B06's side window; tea-house approach off the paving; podium skirt missing beside the stair flanks (seen in View D); saffron tint turning olive on the brown canopy cloth.

## Unresolved (largest first)

1. **Not seen in the game.** Lighting, scale and motion are unverified in Three.js.
2. **Blockout finish.** Flat ground and sky; one cobble tile repeats visibly on the plaza.
3. **Hall at the street camera.** From the merchant street the gameplay camera frames the hall's front but cuts the tower top; the tower is fully visible from the bazaar and court.
4. **Two stall models.** Variety comes from cloth and goods only.
5. **East side is loose.** The warehouse, registry and tea house stand apart; a P3 pass could add a fenced yard or a small structure.
6. **Chimneys have no flashing piece** and dormer cheeks sink slightly into the tiles.
7. **Seal design** is a first proposal and needs the owner's eye.
8. **Lantern model** is heavy (2,822 triangles) and renders pale blue-grey.
""")

# =============================================================================================== 12
rows = []
for a in ["A01", "A02", "A03", "A03b", "A04", "A04b", "A05", "A06", "A07", "A08"]:
    cur, new = project(AREP[a]["usage"], {})
    rows.append([a, ARCH[a]["name"], arche_n[a], AREP[a]["instances"], f"{cur:,}", f"{new:,}", STATUS[a]])
w("12-p2-construction-contract.md", f"""
# 12 - P2 construction contract (revised in P1.1; not started; needs explicit authorisation)

P2 builds the eight archetypes with their two variants, the split gateway, the market cross and the stall kits as reusable assemblies. It does not
assemble the town (P3) or build terrain (P4). No further asset search is needed.

## Inputs

- Archives and hashes: 04. Modules per archetype: 08. Custom and variant items: 03b. Assembler and data: `citadel_lib.py`, `town_data.py`.
- Grid: 2 m bays, 3 m storeys, authored scale, 90-degree rotations.

## Roster, readiness and triangle budget

{tbl(["ID", "Archetype", "Instances in town", "Module instances", "Triangles now", "Triangle budget (projection)", "Readiness"], rows)}
All archetypes are READY: every essential module is verified and every assembly was rendered front, rear and from above. The two P1.0 conditions
(Exchange Hall tower junction and podium; tea-house balcony) are resolved. Items P2 must author rather than assemble are in 03b: the seal, four cloth
material instances, and a purpose-made lamp post.

## Shared components (build first)

| Component | Used by |
|---|---|
| Plaster bays `Wall_Plaster_*`; stone bays `Wall_UnevenBrick_*` | all enclosed archetypes |
| Window inserts, shutters, door leaves | all enclosed archetypes |
| Posts `Corner_ExteriorWide_Wood`; ground-floor piers `Corner_Exterior_Brick` | all |
| Roofs `Roof_RoundTiles_4x6, 6x6, 6x8, 8x8, 8x12, 8x14`, `Roof_2x4_RoundTile`; gables `Roof_Front_Brick2/4/6/8` | all |
| Dormer, chimneys, timber canopy | A03, A03b, A05, A06, A07, A08 |
| `Wall_Arch` arcade bay | A02, gateway |
| Signage kit: red sign, teal and saffron variants, seal, lantern | all frontages |

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Merge duplicate materials to the {len(base_mats)} listed in 05; author the four cloth instances and the seal.
3. Shared wall, window and door sub-assemblies.
4. A04 and A04b. 5. A03 and A03b. 6. A05 and A06.
7. A02 market hall, gateway lodges, market cross (same arcade system).
8. A01 Exchange Hall: main block, wings, tower above the roof, deck and skirt, stairs.
9. A07 warehouse, A08 tea house.
10. Apply the substitutions below; join static meshes per building by material.
11. One archetype exported and loaded in the real Three.js scene; measurements recorded; stop for approval.

## Quantified preliminary optimisation plan

Measured in Blender for the P1.1 blockout: **{STATS['instances']:,} instances, {len(used_models)} downloaded models, {STATS['triangles']:,} triangles, {len(base_mats)} distinct materials
({STATS['material_count']} duplicated slots as imported), 50 source textures** (architecture and nature up to 2048 px, props up to 4096 px). P1.0 was {S0['triangles']:,} triangles.
Island 1 is documented at 327-412 draw calls and about 2.5 million submitted triangles across all passes.

High-triangle components and the substitution proposed for each:

{tbl(["Component", "Instances", "Triangles each", "Total now", "Target each", "Saving", "How"], opt_rows)}
| Projection | Triangles |
|---|---|
| P1.1 blockout, measured | {TOWN_CUR:,} |
| After the substitutions above | **{TOWN_NEW:,}** ({100 * (TOWN_CUR - TOWN_NEW) / TOWN_CUR:.0f}% lower) |
| Paving as one plane per surface instead of {STATS['paving_tiles']} tiles | saves a further {PAVE - 2 * len(L['paving']):,} |

Two of the targets are existing models with measured counts (`MV-Prop_Crate` 230, `MV-Balcony_Cross_Straight` 132). The others are **targets for a
simplified mesh that P2 has to produce and measure**; they are not achieved results. Draw calls: {len(base_mats)} materials means roughly {len(base_mats)} to {len(base_mats) * 2} static batches if each
building is merged by material and grouped by district; instanced props add a handful.

## Measurable P2 verification steps

| Step | Measure | Pass condition (proposed, to be agreed) |
|---|---|---|
| 1 | Triangles per archetype GLB (glTF accessor counts, `docs/tooling/glb-inventory.mjs`) | At or below the budget column above |
| 2 | Distinct materials and textures in the exported set | Materials at or below {len(base_mats)}; no texture above 2048 px |
| 3 | One archetype in the real page: `renderer.info.render.triangles` and `.calls` at three fixed cameras, against the island-1 baseline at the same cameras | Recorded; increase within the agreed budget |
| 4 | Scale and orientation in Three.js: door 2.1 m, storey 3.0 m, +y up, front on +z | Matches within 1 cm |
| 5 | Controller on the hall stairs and through a market-hall arch | Climbs and passes without sticking |
| 6 | Follow camera on the primary route in the engine | Matches section F of 09 or better |
| 7 | Frame time over a fixed 60 s walk at 1280 x 720, standard quality | Recorded with hardware noted; no claim before this exists |

**Browser performance has not been validated.** Every number in this section comes from Blender.

## Acceptance for P2 as a whole

Each archetype matches its P1.1 render, uses only inventoried modules plus the items in 03b, loads in the real scene at correct scale, and has triangle,
material and draw-call counts recorded. Then stop for approval before P3.
""")

# =============================================================================================== 13
w("13-limitations-and-risks.md", f"""
# 13 - Limitations and risks (P1.1)

## Not verified

- **Nothing was loaded in Three.js.** All renders are Blender EEVEE. Browser appearance, frame rate, real collision and real camera behaviour are untested.
- The walkability and camera checks use ray casts against render geometry with constants copied from the project. They are evidence about the layout, not a run of the game.
- Stall counter height is set by eye. Overhang/jetty modules and balcony corner pieces remain unassembled.
- OpenGameArt mirrors could not be read. Pro and Source editions were not accessed.

## Resolved since P1.0

| P1.0 risk | State |
|---|---|
| Follow camera collides with the gateway | Resolved: split gateway; axis unobstructed in the ray test |
| Stairs possibly not climbable | Reduced: five risers of 0.18-0.22 m measured; engine test still required |
| Arch width unknown | Resolved: 1.67 m by 2.74 m measured |
| Roofs nearly touching across alleys | Resolved: tightest measured gap 0.89 m |
| Lanterns at head height | Resolved: lowest 2.27 m |
| Town reads as a generic kit village | Reduced: guild identity layer; owner to judge |
| Tropical identity undecided | Closed by owner direction: keep the Quaternius system, do not force tropical |

## Differences from the supplied concept images (unchanged)

| Concept images show | P1.1 gives |
|---|---|
| Indonesian-tropical architecture, palms | European half-timber and stone with a guild identity; broadleaf trees |
| Teal banners, striped awnings | Teal civic banners (tinted); timber shopfront canopies; no striped cloth |
| 21 buildings, 12 stalls | {nb} buildings, {ns} stalls |
| Curved streets, dense frontage | Straight streets on a 2 m grid with 3 m alleys and fenced yards |
| Ornate multi-tier hall roof | Stone-based hall with wings and a crossing tower |

## Open risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Triangle load too high in the browser | Medium | Substitutions in 12 project {TOWN_NEW:,}; measure one archetype early in P2 |
| Draw calls inflated by duplicated materials | High if not handled | Merge to {len(base_mats)} materials as step 2 of P2 |
| Simplified lantern, pier and tree meshes do not reach their targets | Medium | Targets are stated as projections; fall back to fewer instances |
| Seal design not to the owner's taste | Medium | It is one small mesh and two flat materials; cheap to redraw |
| Cloth tints look different under the game's lighting | Medium | Recreate as material instances and check in the engine |
| Large props textures (4096 px) | Medium | Downscale or atlas in P2 |
| East side reads as loose | Low to medium | P3 dressing pass |
| Engine collision differs from the ray test | Medium | Repeat sections B and F of 09 in the engine |

## Housekeeping

- Downloads, extracted files, tiles, P1.0 comparison renders and the blockout `.blend` are in `.asset-inspection/merchant-citadel-p1/` (about 1.1 GB, ignored by Git).
- No production file, earlier asset, island-1 content or game code was changed. No GLB was exported. Nothing was committed or deployed.
""")

# =============================================================================================== 14
w("14-p1.1-change-log.md", f"""
# 14 - P1.1 change log and approval dependencies

P1.1 corrects P1.0 in place. Sources, archive hashes and model identifiers are unchanged; no asset search, download, production export, game-code change, commit or deployment was made.

## Changed files (all under `docs/planning/merchant-citadel/p1/`)

| File | Change |
|---|---|
| `README.md` | Rewritten for P1.1 |
| `01-design-bible.md` | Identity vocabulary and building-class hierarchy added |
| `02-external-asset-research.md` | Note that no new search was made; "used" counts updated; gap table shows P1.1 answers |
| `03-verified-asset-inventory.csv` | `modification_required` and `verification_status` updated for P1.1 use; rows, hashes and paths unchanged |
| `03b-custom-and-variant-register.csv` | **New.** Every item that is not downloaded geometry as authored |
| `04-source-license-register.md` | Text note only; table unchanged |
| `05-architectural-direction.md` | Signage system, canopy colours, hierarchy and material specification added |
| `06-measured-town-masterplan.md` | Revised masterplan with a change table and measured envelopes |
| `07-building-placement-schedule.csv` | Revised positions; new columns for measured envelope, sign cloth and the P1.1 change |
| `07b-market-stall-schedule.csv` | 12 stalls, canopy column |
| `08-archetype-specifications.md` | All archetypes revised; A03b, A04b, gateway and market cross added; junction table |
| `09-walking-network.md` | Rewritten around the validation on actual geometry |
| `10-terrain-interface-contract.md` | Support zone corrected to include the transport reservation |
| `11-visual-qa-report.md` | Rewritten as a before/after comparison |
| `12-p2-construction-contract.md` | Readiness updated; quantified optimisation plan and measurable verification steps |
| `13-limitations-and-risks.md` | Updated |
| `14-p1.1-change-log.md` | **New** (this file) |
| `asset-evidence/spatial-validation-actual-geometry.json` | **New.** Raw validation results |
| `asset-evidence/usage-and-triangles.json`, `imported-model-register.csv` | Regenerated for P1.1 |
| `asset-evidence/archive-manifest.md`, `license-evidence.md` | Unchanged content |
| `visuals/view-a..d-*.png`, `orthographic-town-plan.png`, `blockout-top-orthographic.png`, `archetype-assembly-sheet.png` | Re-rendered |
| `visuals/before-after-*.png` (4), `visuals/archetype-roof-plans.png` | **New** |
| `visuals/p1.0/` | **New folder:** the seven P1.0 images, kept unchanged for comparison |
| `visuals/real-asset-contact-sheet.png` | Unchanged |
| `blender-inspection/citadel_lib.py` | Cloth-tint variants, custom seal, per-floor corner types, walls starting above a roof, alternative roof and gable assets |
| `blender-inspection/town_data.py` | Revised archetypes and layout |
| `blender-inspection/build_town.py` | Market cross, sign overrides, tile type per surface, material count |
| `blender-inspection/render_archetypes.py` | Adds a top view |
| `blender-inspection/validate_envelopes.py` | **New.** Validation on actual geometry |
| `blender-inspection/make_package_assets.py`, `make_docs.py` | Rewritten for P1.1 |
| `blender-inspection/fetch_archives.py`, `measure_assets.py`, `render_tiles.py`, `compose_contact_sheet.py` | Unchanged |

Outside the package: `../merchant-citadel-p1.1-review.zip` is generated from this folder and replaces the P1.0 zip.

## How the review's five priorities were met

| Priority | Outcome | Where |
|---|---|---|
| 1 Identity | One seal, three cloth colours with fixed meanings, guild way, market cross, three building classes | 01, 05, Views B-D |
| 2 Composition | Fenced back courts, articulated lanes, three roof orientations with dormers and chimneys, bazaar in quadrants, used hall interiors | 06, View A, View C |
| 3 Spatial verification | New validation on {VAL['triangles_tested']:,} triangles: roof gaps, every edge, stairs, hanging objects, arches, camera | 09 |
| 4 Architectural defects | Tower crosses the ridge; podium is one deck; veranda is supported; junction table | 08 |
| 5 Technical feasibility | Nominal and measured envelopes side by side; support zone includes the reservation; quantified plan | 06, 07, 10, 12 |

## Remaining approval dependencies

1. **Visual approval of P1.1** by the owner. Self-assessed average {a1:.2f} / 5; the 4 / 5 target is not claimed.
2. **The guild seal design** (`CUS-Emblem_NiagaAwan`) and its name. It is the only custom geometry.
3. **The cloth colours**: teal for civic, saffron and cream for market, red for trade.
4. **Acceptance of 12 stalls** (was 10) and of the eaves-to-street variants A03b and A04b.
5. **A triangle and draw-call budget** for the town, so the pass conditions in 12 can be fixed.
6. **Authorisation to start P2.** Not assumed.

**MERCHANT CITADEL P1.1 - PENDING HUMAN VISUAL APPROVAL. STOP.**
""")
print("docs written", f"QA {a0:.2f} -> {a1:.2f}", "projection", TOWN_CUR, "->", TOWN_NEW, "materials", len(base_mats), "primary", prim, "seal", U.get("CUS-Emblem_NiagaAwan"))
