#!/usr/bin/env python3
"""Write the Merchant Citadel P1.2 planning documents (supersedes make_docs.py, the P1.1 generator). Narrative is authored here; every table and number comes from
the measured data (layout, archetypes, archetype report, town stats, model measurements, archive manifest, validation).
Usage: python3 make_docs_p12.py <inspection_dir> <package_dir>
"""
import json, math, os, re, sys, collections

I, P = sys.argv[1], sys.argv[2]
L = json.load(open(f"{I}/data/layout.json")); ARCH = json.load(open(f"{I}/data/archetypes.json"))
AREP = json.load(open(f"{I}/archetypes/archetype-report.json")); STATS = json.load(open(f"{I}/renders/town-stats.json"))
MEAS = json.load(open(f"{I}/measurements.json")) + json.load(open(f"{I}/measurements-expansion.json")); MAN = json.load(open(f"{I}/archives/archive-manifest.json")); VAL = json.load(open(f"{I}/validation.json"))
S0 = json.load(open(f"{I}/p1.1/town-stats.json")); L0 = json.load(open(f"{I}/p1.1/data/layout.json"))   # baseline = approved P1.1
PFX = {"quaternius-medieval-village": "MV", "quaternius-fantasy-props": "FP", "quaternius-stylized-nature": "SN", "kenney-fantasy-town-kit": "KFT", "kenney-modular-buildings": "KMB",
       "synofplay-medieval-cafe": "SY", "avramania-free-collection": "AV", "kaykit-medieval-builder": "KK"}
PFX.update({m["pack_id"]: "PP" for m in MAN if m["pack_id"].startswith("polypizza")})
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
STATUS = {"A01": "READY", "A02": "CONDITIONAL", "A03": "CONDITIONAL", "A03b": "READY", "A04": "READY", "A04b": "READY", "A05": "READY", "A06": "READY", "A07": "READY", "A08": "CONDITIONAL"}
edges = []
for a, b, kind in L["edges"]:
    (xa, na, _), (xb, nb2, _) = L["nodes"][a], L["nodes"][b]
    edges.append((a, b, kind, round(math.hypot(xa - xb, na - nb2), 1)))
net_total = round(sum(e[3] for e in edges), 1)
prim = round(sum(e[3] for e in edges if e[0:2] in [("N01", "N02"), ("N02", "N03"), ("N03", "N04"), ("N04", "N05"), ("N05", "N29"), ("N29", "N27"), ("N27", "N06"), ("N06", "N07"), ("N07", "N08")]), 1)
loops = len(edges) - len(L["nodes"]) + 1
SUM = VAL["summary"]; ENV = {a["id"]: a for a in VAL["A_envelopes"]}
SEALS = U.get("CUS-Seal_NiagaAwan", 0); SIGNS = sum(n for a, n in U.items() if a.startswith("CUS-Sign")); DORMERS = U.get("MV-Roof_Dormer_RoundTile", 0)
EXCESS = max(max(x0 - e["full_x"][0], e["full_x"][1] - x1, n0 - e["full_n"][0], e["full_n"][1] - n1) for e in ENV.values())
base_mats = sorted({re.sub(r"\.\d+", "", m) for m in STATS["materials"]})
ST = VAL["E_stairs"]; AR = VAL["F_arch"]
hang = sorted([c for c in VAL["C_hanging"] if c["clearance_m"] is not None and c["over_paving"]], key=lambda c: c["clearance_m"])
NEWMV = sorted({a[3:] for a in used_models if a.startswith("MV-")} - {a.split("@")[0][3:] for a in S0["usage"] if a.startswith("MV-")})
SYMATS = {x for m in MEAS if m["pack_id"] == "synofplay-medieval-cafe" for x in m.get("materials", []) + m.get("materials_remapped_from_blend", [])}
cam = VAL["G_camera"]

# quantified optimisation projection ------------------------------------------------------------------
ACTIONS = [("FP-Lantern_Wall", 600, "simplified bracket lantern (flat chain, 8-sided cage)"), ("MV-Corner_Exterior_Brick", 300, "simplified quoin pier, same silhouette"),
           ("SN-CommonTree_3", 1500, "lower-detail tree for the backdrop ring"), ("SN-CommonTree_1", 1500, "lower-detail tree for the backdrop ring"),
           ("FP-FarmCrate_Apple", 600, "produce as a textured mound"), ("FP-FarmCrate_Carrot", 600, "produce as a textured mound"), ("SN-Bush_Common_Flowers", 500, "fewer leaf cards"),
           ("MV-Door_8_Round", 400, "flatten studs and ring into the texture"), ("FP-Crate_Wooden", 230, "swap for MV-Prop_Crate (existing model, measured 230)"),
           ("MV-Balcony_Simple_Straight", 132, "swap for MV-Balcony_Cross_Straight (existing model, measured 132)"), ("FP-Stall_Cart_Empty", 1500, "simplify wheel and frame"),
           ("FP-Barrel", 300, "12-sided barrel"), ("FP-Bag", 300, "simplified sack"), ("SN-TwistedTree_2", 3000, "lower-detail feature tree"),
           ("FP-Barrel_Apples", 700, "apples as a textured mound"), ("FP-Dummy", 900, "simplified armour stand"), ("AV-mdvl_food_cabbage_01", 300, "lower-detail cabbage"),
           ("AV-mdvl_food_cheese_wheel_01", 300, "16-sided wheel"), ("AV-mdvl_village_window_box_01", 400, "flowers as cards"), ("AV-mdvl_food_grain_sack_01", 350, "simplified sack"),
           ("AV-mdvl_food_ham_01", 300, "simplified"), ("AV-mdvl_food_fish_01", 250, "simplified"), ("AV-mdvl_village_well_01", 600, "simplified well")]
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


_cat = collections.Counter()
def _catof(a):
    b = a.split("@")[0]
    if b.startswith("MV-Floor"): return "paving"
    if b.startswith(("MV-Wall", "MV-Roof", "MV-Corner", "MV-Window", "MV-Door", "MV-Stairs", "MV-Balcony", "MV-Overhang", "MV-Prop_Chimney")): return "architecture modules"
    if b.startswith("SN-"): return "vegetation"
    if "Lantern" in b: return "lanterns"
    if b.startswith(("FP-Stall", "AV-mdvl_village_stall")): return "stall bases"
    if b.startswith("CUS"): return "custom seal and signs"
    return "goods, furniture and street props"
for _a, _n in U.items():
    _cat[_catof(_a)] += _n * TE[_a]
CATLINE = ", ".join(f"{k} {v:,}" for k, v in _cat.most_common())

w("README.md", f"""
# Merchant Citadel / Kota Niaga Awan - P1 planning package (revision P1.2)

**Status: MERCHANT CITADEL P1.2 - PENDING HUMAN VISUAL AND ASSET APPROVAL.** Planning and concept only. Dated {DATE}. P2 has not started.

P1.2 carries out the owner's brief "P1.1 - Complete visual redesign and expanded asset integration". It is numbered P1.2 here because a
revision called P1.1 already exists and was approved by the owner on {DATE} ([15-owner-approval-record.md](15-owner-approval-record.md)).
P1.2 **builds on that approved town**: no building, stall, walking node or paved surface moved. It changes how the town looks and what it
is dressed with. Everything approved in P1.1 is kept unchanged in [visuals/p1.1/](visuals/p1.1/) so the two can be compared and either can be chosen.

**Two approved items are superseded by this brief and need a fresh decision:** the guild seal (now crossing trade routes and a diamond, in
burgundy and gold) and the cloth colours (now burgundy for the guild and blue for the market). See [16-p1.2-change-log.md](16-p1.2-change-log.md).

| # | Document | P1.2 |
|---|---|---|
| 01 | [Town design bible](01-design-bible.md) | Rewritten around the "City of a Thousand Trades" vision |
| 02 | [External asset research](02-external-asset-research.md) | Targeted expansion: eight new sources examined, two adopted |
| 03 | [Verified asset inventory](03-verified-asset-inventory.csv), [custom and variant register](03b-custom-and-variant-register.csv) | {len(MEAS)} rows (was 613); register extended |
| 04 | [Source and licence register](04-source-license-register.md) | New sources, hashes and licence evidence added |
| 05 | [Architectural style specification](05-architectural-direction.md) | Palette, colour grade, signage and roof hierarchy |
| 06 | [Measured masterplan](06-measured-town-masterplan.md) | Positions unchanged; envelopes re-measured |
| 07 | [Building schedule](07-building-placement-schedule.csv), [stall schedule](07b-market-stall-schedule.csv) | Regenerated |
| 08 | [Archetype specifications](08-archetype-specifications.md) | Jetty, porch, signs, kits; readiness per archetype |
| 09 | [Walking network and spatial validation](09-walking-network.md) | Re-run on the new geometry |
| 10 | [Terrain interface contract](10-terrain-interface-contract.md) | Envelope re-measured; packed-earth courts added as a surface treatment |
| 11 | [Visual QA report, before and after](11-visual-qa-report.md) | Rewritten on the brief's ten criteria |
| 12 | [P2 construction contract](12-p2-construction-contract.md) | Exact dependencies, READY / CONDITIONAL / BLOCKED |
| 13 | [Risk and feasibility register](13-limitations-and-risks.md) | Updated |
| 14 | [P1.1 change log](14-p1.1-change-log.md) | Historical, unchanged |
| 15 | [Owner approval record](15-owner-approval-record.md) | Unchanged |
| 16 | [P1.2 change log and approval dependencies](16-p1.2-change-log.md) | New |

## Visuals

| File | Evidence class |
|---|---|
| [view-a-aerial.png](visuals/view-a-aerial.png), [view-b-merchant-street.png](visuals/view-b-merchant-street.png), [view-c-central-bazaar.png](visuals/view-c-central-bazaar.png), [view-d-exchange-court.png](visuals/view-d-exchange-court.png) | ASSET-BACKED BLENDER BLOCKOUT, P1.2 (one town, four cameras, same cameras as P1.1) |
| [before-after-a-aerial.png](visuals/before-after-a-aerial.png), [-b-](visuals/before-after-b-merchant-street.png), [-c-](visuals/before-after-c-central-bazaar.png), [-d-](visuals/before-after-d-exchange-court.png) | Approved P1.1 beside P1.2, same camera |
| [expansion-asset-contact-sheet.png](visuals/expansion-asset-contact-sheet.png) | REAL ASSET RENDER of the newly downloaded models, adopted and rejected |
| [real-asset-contact-sheet.png](visuals/real-asset-contact-sheet.png) | REAL ASSET RENDER of the original packs (unchanged from P1.0) |
| [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png), [archetype-roof-plans.png](visuals/archetype-roof-plans.png) | ASSET-BACKED ASSEMBLY, front, rear and roof plan of all twelve assemblies |
| [orthographic-town-plan.png](visuals/orthographic-town-plan.png) | Measured drawing generated from layout data and measured envelopes |
| [blockout-top-orthographic.png](visuals/blockout-top-orthographic.png) | ASSET-BACKED BLENDER BLOCKOUT (top view) |
| [visuals/p1.1/](visuals/p1.1/), [visuals/p1.0/](visuals/p1.0/) | Earlier revisions, kept unchanged |

No ILLUSTRATIVE CONCEPT image and no AI-generated image is in this package.

## What is and is not downloaded geometry

- **Downloaded, as authored:** {len(used_models)} models - {used_by_pack['MV']} Quaternius Medieval Village, {used_by_pack['FP']} Fantasy Props, {used_by_pack['SN']} Stylized Nature, {used_by_pack['SY']} Syntaxes of Play Medieval Cafe, {used_by_pack['AV']} Avramania.
- **Material variants of downloaded models:** {STATS['material_variant_ids']} ids - cloth in burgundy, blue and cream; civic roofs one value darker. Geometry unchanged.
- **Colour grade:** eleven downloaded materials are shifted towards the brief's palette (roof, timber, plaster, stone, paving, foliage). Geometry and UVs unchanged.
- **Custom, authored here:** the guild seal ({SEALS} placements) and {SIGNS} hanging trade signs in {STATS['custom_ids'] - 1} pictogram/colour versions; {STATS['triangles_custom']:,} triangles in total.
- **Scaled:** the plain timber post (lamp posts, lane standards) and two floor jars.
- **Temporary, never an asset:** ground plane, packed-earth court planes, dark interior boxes, the 1.9 m explorer, and the afternoon light itself.

All of it is itemised in [03b-custom-and-variant-register.csv](03b-custom-and-variant-register.csv).

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1/blender-inspection; B="/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec"
python3 $S/fetch_archives.py $D/archives && python3 $S/fetch_expansion.py $D/archives   # free uploads only; unzip each into $D/extracted/<pack_id>/
$B --python $S/measure_assets.py -- $D/extracted $D/measurements.json
$B --python $S/inspect_expansion.py -- $D/extracted $D/measurements-expansion.json $D/tiles-expansion 300
python3 $S/town_data.py $D/data                     # nominal checks
$B --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/data/archetypes.json $D/archetypes
$B --python $S/build_town.py -- $D/extracted $D/measurements.json $D/data $D/renders $D/blender/merchant-citadel-p1-blockout.blend
$B --python $S/validate_envelopes.py -- $D/blender/merchant-citadel-p1-blockout.blend $D/data $D/validation.json
python3 $S/make_package_assets.py $D docs/planning/merchant-citadel/p1 && python3 $S/make_docs_p12.py $D docs/planning/merchant-citadel/p1
```
The before/after images need the P1.1 renders kept in `$D/p1.1/`. `make_docs.py` is the P1.1 generator and is kept for the record; do not run it over this revision.
""")


w("01-design-bible.md", f"""
# 01 - Town design bible (P1.2): The City of a Thousand Trades

## Vision

Kota Niaga Awan is a prosperous trading town built around an exchange. Traders from other realms come to sell, weigh, bargain and
provision. It is not a fortress, a palace or a village with a few stalls: its economy is visible in what stands on the street.

A visitor passes between two gate lodges and sees the whole promise of the town at once: a street of shopfronts with a painted sign
over every door, the market cross beyond it, and the gabled porch and tower of the Exchange Hall closing the view. The street opens
into the bazaar, framed by two covered market halls; past the bazaar the court is quiet and formal; the hall stands above it on a podium.
Side routes lead to workshops, the guild warehouse and a tea terrace at the edge.

## Emotional progression and what carries it

| Stage | District | What the visitor meets |
|---|---|---|
| Arrival | D1 Gerbang Niaga | Two timber lodges with the guild seal; the hall's porch and tower in the gap between them |
| Curiosity | D2 Koridor Niaga | Jettied upper floors, timber shopfront canopies, a trade sign per shop, flower boxes, goods by the doors |
| Discovery | D6 Lorong Lentera, D7 Jalur Gudang | A lantern lane of workshops with a well in the back court; a plain stone warehouse lane |
| Commercial activity | D3 Pasar Awan | Two halls with different trades, twelve stalls of five kinds around the market cross |
| Civic importance | D4 Pelataran Bursa, D5 Balai Niaga Awan | Dressed-brick court, no stalls; stone-based hall with a porch, burgundy banners and the seal on the tower |
| Scenic reward | D8 Tea Lookout | A veranda tea house and a terrace with laid tables facing the future island edge |

## Identity system

| Element | Rule | Where |
|---|---|---|
| **Guild seal** (custom) | A circle with two crossing trade routes, a way station at each end and a diamond at the centre: commerce, connection, exchange, many realms. Gold on burgundy with a blue heart | Guild-run structures only: hall porch and tower, both market halls, gate lodges, warehouse, market cross ({SEALS} placements) |
| **Burgundy** `#8C3E45` | The guild | Hall banners, east market hall, crafts stalls, warehouse-lane standards, sign boards of guild offices |
| **Blue** `#345D80` | The market | West market hall banners, provisions stalls |
| **Cream** | Neutral trade | Two stalls, artisan-lane standards |
| **Timber signs** (custom) | One hanging board per shop with a pictogram of its trade: loaf, jar, hammer, crate, coin, cup, scroll | {SIGNS} signs; boards with a burgundy field mark the two guild offices |
| **Guild way** | The 4 m band of dressed brick on the axis | Arrival court to civic court |
| **Dark roofs** | Civic and guild roofs are one value darker than shop roofs | Hall, market halls, warehouse, gate lodges |

A visitor can tell a shop (sign, canopy or jetty, shutters) from a workshop (stone, bench and anvil outside, hammer sign), a market hall
(no walls, banners, goods) from the warehouse (stone, paired doors, seal, crates), and the tea house (veranda, laid tables, cup sign)
from all of them, without reading a label.

## Trades shown (static dressing only; no shop system)

| Place | Trade | Evidence |
|---|---|---|
| Market Hall West | Provisions | Bread, cheese, ham, fish, cabbages, apples and carrots, kegs, grain sacks, scales |
| Market Hall East | Crafts and general trade | Pottery, bottles and potions, books and scrolls, a cloth-covered table, shelves, an armour stand |
| Stalls, west side | Provisions | Blue and striped canopies, bread counter with scales and a keg |
| Stalls, east side | Crafts | Burgundy and cream canopies, a wares table with a runner |
| Koridor Niaga | Money changer, baker, dry goods, map and book seller, potter, provisioner | Sign pictograms |

## What P1.2 did not do

It did not add buildings, change the street plan, enlarge the hall, force tropical architecture, or use references from existing games as
anything but a standard for readability. It did not use every attractive model it found: see 02.

## Lessons from the first island, applied

| Earlier problem | Response |
|---|---|
| Buildings placed without a plan | Coordinates, frontage and a paved approach for every building, checked on real geometry |
| Mismatched styles | One kit for all architecture; other publishers supply goods and furniture only |
| No landmark hierarchy | Porch, dark roof and tower with the seal close the axis |
| Images that could not be built | Every render is assembled from downloaded models; custom items are named as custom |
""")


PACKROWS = [
    ("quaternius-medieval-village", "Quaternius Medieval Village MegaKit [Standard]", "304", "Architecture", "KEPT - the only building system"),
    ("quaternius-fantasy-props", "Quaternius Fantasy Props MegaKit [Standard]", "211", "Props, stalls, banners", "KEPT"),
    ("quaternius-stylized-nature", "Quaternius Stylized Nature MegaKit [Standard]", "116", "Vegetation", "KEPT"),
    ("kenney-fantasy-town-kit", "Kenney Fantasy Town Kit 2.0", "160", "-", "Rejected in P1.0 (scale, flat style)"),
    ("kenney-modular-buildings", "Kenney Modular Buildings 2.1", "100", "-", "Rejected in P1.0"),
    ("synofplay-medieval-cafe", "Syntaxes of Play - Medieval Cafe Asset Pack", "65+", "Counters, tables, chairs, shelves, kegs, bread, platters, menu stand", "**ADOPTED** (furniture and goods)"),
    ("avramania-free-collection", "Avramania - Free Low-Poly Medieval Collection", "203", "Food and market goods, one stall, inn sign, flower box, well", "**ADOPTED in part** (2 of 9 packs)"),
    ("kaykit-medieval-builder", "KayKit Medieval Builder Pack 1.0 (legacy)", "200+", "-", "REJECTED: city-builder miniatures"),
]
rows = [[n, adv, count[pid], f"{man[pid]['bytes'] / 1e6:.1f} MB", used_by_pack.get(PFX[pid], 0), role, dec] for pid, n, adv, role, dec in PACKROWS]
pprows = [[man[p]["publisher"], man[p]["source_page"], f"{man[p]['bytes']:,}", "REJECTED: " + ("miniature (stall 0.55 m tall) and flat-colour" if "market" in p else "modern sign, wrong period")] for p in man if p.startswith("polypizza")]
w("02-external-asset-research.md", f"""
# 02 - External asset research (P1.2: targeted expansion)

P1.0 audited five packs. P1.2 did **not** repeat that audit. It looked for models that fix specific weaknesses of the approved town:
plain shopfronts, a thin bazaar with two stall models, no shop signs, sparse tea-house furniture.

All archives were downloaded from the creators' own pages, extracted into separate folders, imported in Blender 5.2.3 and measured
(`fetch_expansion.py`, `inspect_expansion.py`). Catalogue figures are the publishers' advertising; "imported" is what was counted.

{tbl(["Pack", "Advertised models", "Models imported", "Archive size", "Unique models used in the P1.2 town", "Used for", "Decision"], rows)}
Individual Poly Pizza models (each a single GLB with a CC0 link on its page):

{tbl(["Creator", "Page", "Bytes", "Decision"], pprows)}
All {len(MEAS)} models imported. Evidence: [expansion-asset-contact-sheet.png](visuals/expansion-asset-contact-sheet.png) shows every adopted model and
representative rejected ones, as authored, beside the Quaternius barrel already in the town.

## The seven selection questions, answered per source

| Source | Solves a P1 problem? | Fits the vocabulary? | Scale and material work | Legitimately downloadable? | Licence | Worth the integration? | Geometry |
|---|---|---|---|---|---|---|---|
| Syntaxes of Play Medieval Cafe | Yes: counters, tables, chairs, shelves, kegs, breads | Yes after the timber grade: muted brown wood close to the palette | Metres as authored. FBX texture paths do not resolve; materials come by name from the pack's own Blender file | Yes, free upload on the creator's itch.io page | CC0 1.0 stated on the page; **no licence file inside the archive** | Yes | 40-530 triangles each |
| Avramania Food & Market, Village Builder | Yes: produce, bread, fish, sacks, scales, a striped stall, a hanging inn sign, flower boxes, a well | Partly: flat-shaded palette style. Acceptable for small goods and one stall type; not for architecture | Metres as authored; one 256 px palette texture | Yes, free upload on the creator's itch.io page | CC0 1.0, `License.txt` inside the archive | Yes | Small goods are heavy for their size (cabbage 1,448, flower box 1,330) |
| Avramania Props, Interiors, Nature (same download) | Some would (basket, sack, potted plant) | - | - | Yes | CC0 | **Not adopted:** each ReadMe says some models began as meshes generated by Tripo AI, without saying which. The project rule excludes AI-generated assets unless the owner asks | - |
| Avramania Castle, Weapons, Dungeon, Farm | No | - | - | Yes | CC0 | Not needed | - |
| KayKit Medieval Builder | No | No | Whole buildings are about 1 m tall (board-game scale) | Yes | CC0, `License.txt` | No | - |
| Poly Pizza: Quaternius market stalls | Would add canopy shapes | No: flat colours, miniature | 0.55 m tall; needs x4 scale | Yes | CC0 on page | No | - |
| Poly Pizza: signs | No | No: modern road signs | - | Yes | CC0 on page | No | - |
| OpenGameArt, itch.io 3D tag (general browsing) | Not pursued | | | | | The two adopted packs covered goods and furniture; architecture stays in one kit by design | |

## What the expansion did not find

No free pack offered commercial architecture, civic stone columns, shop signs or fabric awnings in a style that sits beside the
Quaternius kit. Those needs were met inside the existing kit instead, using {len(NEWMV)} of its modules that P1.1 had not assembled:

{", ".join(f"`{m}`" for m in NEWMV)}.

The jettied upper floor (`Overhang_*`), the entrance porch (arches, stone piers and a 6 x 6 roof), wall vines and round-headed shutters
come from that set. Shop signs are custom (03b) because no suitable free model exists.

## Findings carried over from P1.0

1. Medieval Village is a complete building system: 2 m bays, 3 m storeys, matching doors, windows and 17 prefab roofs.
2. Modules are in metres and suit the 1.9 m explorer as authored.
3. No complete building exists in any free archive; every shell is an assembly.
4. Kenney's kits are a different scale and style. Quaternius models are open-edged game meshes.
""")
lic = {"synofplay-medieval-cafe": "CC0 1.0 - stated on the creator's page only (no licence file in the archive)", "avramania-free-collection": "CC0 1.0 - `License.txt` in the archive and the creator's page",
       "kaykit-medieval-builder": "CC0 1.0 - `License.txt` in the archive and the creator's page"}
rows = [[n, man[pid]["publisher"], man[pid]["edition"], man[pid]["source_page"], man[pid]["distribution"],
         lic.get(pid, "CC0 1.0 (file inside archive)"), ZIP.get(pid, man[pid]["archive_filename"]), f"{man[pid]['bytes']:,}", f"`{man[pid]['sha256']}`"] for pid, n, *_ in PACKROWS]
rows += [["Poly Pizza single model", man[p]["publisher"], man[p]["edition"], man[p]["source_page"], man[p]["distribution"], "CC0 1.0 - link on the model page", man[p]["archive_filename"], f"{man[p]['bytes']:,}", f"`{man[p]['sha256']}`"] for p in man if p.startswith("polypizza")]
w("04-source-license-register.md", f"""
# 04 - Source and licence register (P1.2)

The five P1.0 archives are unchanged: same files, same hashes. Eight sources were added in P1.2; two are used.

{tbl(["Pack", "Publisher", "Edition", "Source page", "Distribution used", "Licence and where it is stated", "Archive", "Bytes", "SHA-256"], rows)}
- Nothing was purchased. Every new file came from the free path of the creator's own page (itch.io name-your-own-price with a zero minimum, or a Poly Pizza static file). No account or key was used.
- Licence statements and what was checked for each new source: [asset-evidence/license-evidence.md](asset-evidence/license-evidence.md).
- **Syntaxes of Play:** the CC0 statement is on the page, not in the archive. Keep a dated copy of the page with the P2 assets.
- **Avramania:** only the Food & Market and Village Builder packs are used; their ReadMe files state that no model was generated by an AI 3D or image tool. All models were built by scripts written with an AI coding assistant, which the creator discloses.
- CC0 needs no attribution. Crediting the creators in the portfolio is still recommended.
- Per-model provenance: [03-verified-asset-inventory.csv](03-verified-asset-inventory.csv). Items that are **not** downloaded geometry: [03b-custom-and-variant-register.csv](03b-custom-and-variant-register.csv).
""")
w("asset-evidence/archive-manifest.md", "# Archive manifest\n\nDownloaded by `blender-inspection/fetch_archives.py` (P1.0) and `fetch_expansion.py` (P1.2). Archives are kept outside Git in `.asset-inspection/merchant-citadel-p1/archives/`. The first five rows are unchanged since P1.0.\n\n"
  + tbl(["pack_id", "archive", "bytes", "sha256", "downloaded (UTC)", "uploads listed on the free download page"],
        [[m["pack_id"], ZIP.get(m["pack_id"], m["archive_filename"]), m["bytes"], f"`{m['sha256']}`", m.get("downloaded_utc", ""), "; ".join(m.get("listed_uploads", [])) or "n/a (single file)"] for m in MAN])
  + "\nModels counted after extraction and import: " + ", ".join(f"{p} {count[p]}" for p in count) + ".\n")
_le = f"{P}/asset-evidence/license-evidence.md"
_add = """
## P1.2 addendum - sources added in the targeted expansion (2026-11-11)

| Source | Statement read | Where |
|---|---|---|
| Syntaxes of Play, Medieval Cafe Asset Pack | "This asset pack is released under the CC0 1.0 Universal license." Free for personal and commercial use; attribution optional | Creator's itch.io page. **No licence file inside `medv-cafe.zip`** (it holds `fbx/`, `tex/` and two `.blend` files) |
| Avramania, Free Collection | "LICENCE: Creative Commons Zero 1.0 Universal (CC0 1.0), public domain ... copy them, change them, and use them in anything you make, including games you sell." | `License.txt` at the root of the archive and in each pack folder; same on the page |
| Avramania, how the models were made | Food_Market and Village_Builder: "Every model here was built by Python scripts in Blender, written with the help of an AI coding assistant. None was generated by an AI 3D or image tool." Props_Tools_Fencing, Interiors_Furniture, Nature_Terrain: 6 of 20, 4 of 25 and 13 of 41 models "started as 3D meshes generated by Tripo AI" (not identified individually) | `ReadMe.txt` in each pack folder |
| KayKit, Medieval Builder Pack | "Free for personal and commercial use, no attribution required. (CC0)" | Creator's itch.io page; `License.txt` in the archive |
| Poly Pizza single models (Quaternius x4, iPoly3D x1) | Each model page links to creativecommons.org/publicdomain/zero/1.0 | Model pages listed in 04 |

The archive's own request, not a condition: Avramania asks that the collection is not re-uploaded as it is. This package does not redistribute any archive.
"""
_cur = open(_le).read() if os.path.exists(_le) else "# Licence evidence\n"
if "P1.2 addendum" not in _cur:
    open(_le, "w").write(_cur.rstrip() + "\n" + _add)


GR = [("Roof tiles `MI_RoundTiles`", "#B35430", "#BB6345", "hue +0.012, saturation x0.90, value x0.94"), ("Civic roofs `MI_RoundTiles@dark`", "-", "#9F523D", "further saturation x0.84, value x0.72"),
      ("Timber `MI_WoodTrim`, `_Wear`", "#896A4A", "#75543B", "saturation x0.82, value x0.76"), ("Plaster `MI_Plaster`", "#B29C80", "#E8D9BC", "saturation x0.80, value x1.14"),
      ("Stone walls `MI_UnevenBrick`", "#867966", "#858078", "saturation x0.50"), ("Paving `MI_Brick`", "#918376", "#A69E8E", "saturation x0.70, value x1.10"),
      ("Foliage `Leaves_NormalTree`, `Leaves`", "#587B00", "muted natural green", "saturation x0.70-0.75, value x0.90")]
w("05-architectural-direction.md", f"""
# 05 - Architectural style specification (P1.2)

## Language

Asset-native stylised merchant architecture from one kit, the Quaternius Medieval Village MegaKit: cream plaster, exposed timber frame,
stone ground floors on the heavier buildings, terracotta tile roofs. Warm and slightly whimsical; not a castle and not historically exact.
The merchant character comes from function: shopfronts, signs, halls, a warehouse, an exchange.

**Rule for mixing publishers:** architecture, roofs, paving and street furniture come from Quaternius only. Other publishers supply goods and
furniture below about 2.3 m, where a different shading style is not read as a different building.

## Palette and colour grade

The brief's palette is reached by grading the downloaded materials, not by repainting textures. Average texture colour was measured for each
material and a hue / saturation / value correction derived.

{tbl(["Surface and material", "Measured average", "Palette target", "Grade applied"], GR)}
| Accent | Colour | Carrier |
|---|---|---|
| Merchant burgundy | `#8C3E45` | Cloth variant; seal field; guild sign boards |
| Trading blue | `#345D80` | Cloth variant; heart of the seal |
| Civic gold | `#C8A15A` | Seal; sign pictograms |

Roofs stay in one terracotta family: shops at the main value, guild and civic roofs one step darker. No building has its own colour.

## Architectural identity contract

| Element | Rule | Verified modules |
|---|---|---|
| Shop, two storeys, gable to street | Upper floor **jettied 1.12 m** over the shopfront on timber brackets; flower boxes under the upper windows; one dormer and a chimney | `Overhang_Plaster_Short`, `Overhang_Side_Plaster_Short_L/R`, `Roof_RoundTiles_6x10` |
| Shop, two storeys, eaves to street | Timber shopfront canopy along the whole front; two dormers | `Roof_Wooden_2x1_L / _Center / _R` |
| Compact shop | Canopy on the gable-fronted form; shutters and a wall vine on the eaves-fronted form | as above, `Prop_Vine1` |
| Corner building, warehouse, workshop | Stone ground floor, stone piers below, timber posts above | `Wall_UnevenBrick_*`, `Corner_Exterior_Brick` |
| Market hall | Open timber arcade under a dark roof; seal on both gables; four cloth banners | `Wall_Arch`, `Roof_RoundTiles_8x12@dark` |
| Exchange Hall | Stone base across a 26 m front, wings, **gabled entrance porch on stone piers**, four burgundy banners, tower through the ridge, dark roofs, podium | 08, A01 |
| Roofscape | Three orientations to the street, {DORMERS} dormers, chimneys, the porch gable and two roof values | `Roof_Dormer_RoundTile`, `Prop_Chimney*` |
| Paving | Cobble for streets and plaza; dressed brick for the guild way, halls and court; red brick for the artisan lane and terrace; packed earth in the back courts (terrain treatment) | `Floor_UnevenBrick`, `Floor_Brick`, `Floor_RedBrick` |

## Signage and banner system

| Class | Carrier | Model | Mounting rule |
|---|---|---|---|
| Shop or workshop | Timber board with a gold pictogram | `CUS-Sign_<glyph>_wood` (custom) | Exactly one per shop, on an iron arm at right angles to the wall; underside 2.1 m or more above paving |
| Guild office | Same board with a burgundy field | `CUS-Sign_<glyph>_burgundy` (custom) | Registry and assay office only |
| Tea house | Cup sign plus a small hanging inn sign | `CUS-Sign_Cup_wood`, `AV-mdvl_village_sign_inn_01` | Side wall; under the veranda |
| Guild cloth | Burgundy | `FP-Banner_2_Cloth@burgundy`, `FP-Banner_1@burgundy`, `FP-Banner_2@burgundy` | Hall front between upper windows; east market hall corners; warehouse-lane standards |
| Market cloth | Blue | `FP-Banner_1@blue` | West market hall corners |
| Guild seal | Gold, burgundy, blue | `CUS-Seal_NiagaAwan` (custom) | Guild-run structures and the market cross only; 0.8 to 1.9 m across |

Long cloth banners no longer serve as shop signs. Lowest measured hanging edge over any walkable surface: **{hang[0]['clearance_m']} m** (09).

## Materials

{len(base_mats)} distinct materials are in the town (P1.1: 29). The increase is {len([m for m in base_mats if m in SYMATS])} textured materials from the cafe pack, 1 palette material from Avramania,
{len([m for m in base_mats if m.startswith('CUS_')])} flat custom materials and the cloth and roof variants. The cafe pack's materials carry normal and roughness maps; P2 should atlas them to a few (12).

## Lighting used for the views (presentation, not an asset)

Warm afternoon sun about 38 degrees above the horizon from the south-west, a blue-to-warm sky gradient for fill, soft shadows, and the
Khronos PBR Neutral view transform (the tone mapping three.js offers as `NeutralToneMapping`). Shadows fall across half the street, so
both lit and shaded facades are visible; nothing is hidden in darkness. The game's own lighting will differ and must be checked in P2.

Principal compromise, unchanged: this is a European half-timber language with its own guild identity, not the Indonesian-tropical look of the first island. That is the owner's stated direction.
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
# 06 - Measured town masterplan (P1.2)

Drawing: [visuals/orthographic-town-plan.png](visuals/orthographic-town-plan.png). Data: `blender-inspection/town_data.py`. P1.2 keeps the plan the owner
approved in P1.1: no building, stall, walking node or paved surface was moved. What changed is on and around the buildings.

## Coordinates

Metres. Origin = centre of the arrival court. Plan axes: x = east, n = north. Project / Three.js: **(x, y, z) = (x, elevation, -n)**, +y up.
`rotation_y`: 0 = front faces south (+z), 90 = east, -90 = west, 180 = north.

## Size

Developed envelope (nominal): x {x0}..{x1} ({x1 - x0} m), z {-n1}..{-n0} ({n1 - n0} m). With the transport reservation: {ux1 - ux0} x {un1 - un0} m (10).

## Programme

**{nb} permanent buildings, 8 archetypes (two with an eaves-to-street variant), {ns} market stalls, 1 split gateway, 1 market cross.**
All counts are those of the approved P1.1. (The brief's baseline of 10 stalls is the P1.0 figure; P1.1 raised it to 12 and P1.2 keeps 12.)

## What changed in P1.2, and why

Positions and rotations: **none changed**. The P1.1 change table is kept in the P1.1 documents (`.asset-inspection/merchant-citadel-p1/p1.1/docs/`).

| Element | Change | Spatial reason |
|---|---|---|
| A03 shophouses (B07, B09, B16) | Upper floor jettied 1.12 m towards the street; measured envelope 10.54 to 11.85 m deep | Gives the street a second, closer layer at first-floor height; the ground-floor line and the 8 m clear width are unchanged |
| A03b, A04 (B05, B06, B14) | Timber shopfront canopy across the front | Marks shop entrances at eye level |
| Exchange Hall B01 | Gabled porch 6 x 2 m in front of the doors, inside the existing podium | Gives the entrance a depth and a centre; no footprint change (still 28 x 16 m podium) |
| Market halls B02, B03 | Interiors restocked as two different kits; aisle and cross-passage kept clear | Halls now differ by trade |
| Stalls | Same 12 positions; kinds changed (07b) | Variety without moving anything |
| Hall corners, bazaar | Goods stacked at the four inner hall corners, outside the arcades | Fills the dead corners beside the stall rows; clear of every walking edge |
| Back courts | Shown as packed earth; a well in the west court | Reads as yards, not leftover grass |
| Tea terrace | Cafe furniture replaces the bench set | A place to sit, as the brief asks |

## Building positions, nominal footprint and measured envelope

{tbl(["ID", "Archetype", "Name", "Position (x, y, z)", "rotation_y", "Front faces", "Nominal footprint on plan (m)", "Measured envelope incl. roof, signs, props (m)"], brow)}
The measured envelope is the axis-aligned bound of everything attached to the building in the assembled scene. It is what must be kept clear, and it
is drawn dashed on the plan. Roofs overhang the wall lines by 0.8 to 1.1 m on each side; the A03 jetty adds 1.12 m at the front above 3 m. Full figures: [07-building-placement-schedule.csv](07-building-placement-schedule.csv).

## Paved surfaces (2 m tiles; later rows overlay earlier ones)

{tbl(["Surface", "x", "z", "Size (m)", "Tile"], pav)}
Reserved, no construction: future transport pad x -10..10, z 8..24.

## Checks

- Nominal checks (`town_data.py`): **{"PASS" if L["checks_pass"] else "FAIL"}** - footprint overlaps, clear corridors, paved entrance approaches, stalls on paving, graph connectivity.
- Checks on actual geometry (`validate_envelopes.py`): reported in 09. Roof gaps failing: {SUM['roof_gaps_fail']}; hanging objects too low: {SUM['hanging_fail']}; walking edges failing: {SUM['edges_fail']} of {SUM['edges_total'] - 1} built.
""")

# =============================================================================================== 08
CODE_LEGEND = "P plaster, G half-timber grid, F/R/T plaster window (wide flat / wide round / thin round), D/O plaster door (flat / round), I inset round portal, S stone, s/r stone window, o/d stone door, A open timber arch, X no module (hidden face or floor below the roof)"
NOTES = {  # purpose, P1.2 change, collision, custom, non-Quaternius assets, acceptance
    "A01": ("Dominant civic landmark and research venue", "Gabled entrance porch added (arches on stone piers, 6 x 6 roof run back into the main slope); three upper windows behind it became plain bays; all roofs civic dark; burgundy banners; new seal in the porch gable and on the tower.",
            "Box proxies: main 14 x 8 x 6, tower 4 x 4 above 10 m, wings 6 x 6 x 6, podium 28 x 16 x 1, four porch pier proxies; stairs as five 0.2 m steps or one ramp proxy", "Guild seal x3", "None",
            "Porch ridge buried in the main roof with no open end; doors reachable through the porch; tower seal visible from the bazaar and court"),
    "A02": ("Covered market, used twice with different dressing kits", "One assembly, two kits chosen per building: provisions (west) and crafts (east). Dark roof, new seal, blue or burgundy banners.", "Post proxies only; arcade stays walkable; goods as box proxies clear of the aisle", "Guild seal x2",
            "Syntaxes of Play: counters, food display, shelf, table, cloth, kegs, crate, basket, sausage, scale. Avramania: loaf, cheese, ham, cabbage, fish, scales, grain sack",
            "Centre aisle and cross-passage bay free of geometry; goods rest on the measured surfaces (0.81, 0.75, 1.15 m)"),
    "A03": ("Two-storey shophouse, gable to the street, jettied", "Upper floor jettied 1.12 m on `Overhang_Plaster_Short` with side cheeks and brackets; roof is the 6 x 10 shifted 1 m forward; trade sign under the jetty; flower boxes; the timber canopy of P1.1 is removed.",
            "One box 6 x 8 x 6; jetty non-colliding (underside 3.0 m)", "Trade sign x1", "Avramania flower box x2", "Jetty windows sit flush without flicker; sign underside 2.1 m or more; roof covers the jetty"),
    "A03b": ("Two-storey shophouse, eaves to the street (variant of A03 without the jetty)", "Timber canopy along the front, trade sign, flower boxes.", "One box 8 x 6 x 6; canopy non-colliding", "Trade sign x1", "Avramania flower box x2", "Canopy clears open shutters; sign visible along the street"),
    "A04": ("Single-storey shop, gable to the street; registry office", "Timber canopy and trade sign added.", "One box 4 x 6 x 3", "Trade sign x1", "None", "Matches the render"),
    "A04b": ("Single-storey shop, eaves to the street (variant of A04)", "Trade sign, lantern and wall vine added.", "One box 6 x 4 x 3", "Trade sign x1", "None", "Matches the render"),
    "A05": ("Heavy corner building with two active fronts", "Two trade signs (one per front) replace the banners; flower boxes.", "One box 8 x 8 x 6", "Trade sign x2", "Avramania flower box x2", "Both fronts read as entrances"),
    "A06": ("Stone workshop with outdoor work area", "Trade sign (hammer) and wall vine added.", "One box 6 x 6 x 3 plus prop proxies", "Trade sign x1", "None", "Matches the render"),
    "A07": ("Guild warehouse with paired doors and loading yard", "Dark roof, new seal, two wall vines.", "One box 8 x 14 x 6", "Guild seal x1", "None", "Matches the render"),
    "A08": ("Tea house with a veranda", "Cup sign on the side wall, hanging inn sign under the veranda, flower boxes on side windows, vine.", "One box 6 x 6 x 6; four post proxies; deck not walkable in P2", "Trade sign x1", "Avramania inn sign x1, flower box x2 (terrace furniture is town dressing, not part of the archetype)",
            "Nothing hangs below 2.1 m over the veranda approach"),
}
out = ["# 08 - Archetype specifications (P1.2)\n",
       "Module ids prefixed MV- / FP- (Quaternius), SY- (Syntaxes of Play) and AV- (Avramania) exist in the downloaded archives and are instanced at authored scale. Architecture sits on a 2 m / 3 m grid with 90-degree rotations. Ids with `@` are material variants (cloth colour, dark roof). `CUS-` ids are custom geometry. See 03b.\n",
       "**Material strategy, all archetypes:** downloaded materials with the colour grade of 05 baked into the base-colour textures; cloth and dark-roof variants as material instances; cafe-pack materials atlased; no per-building colours.\n",
       f"Facade codes: {CODE_LEGEND}. Strings read left to right from outside, one per floor.\n",
       "Renders: [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png) (front and rear), [archetype-roof-plans.png](visuals/archetype-roof-plans.png) (roof junctions from above).\n",
       "**Shared assembly order:** (1) 2 m grid and 3 m storey; (2) ground-floor wall bays per facade string; (3) window inserts, door leaves, shutters; (4) corner piers or posts per floor; (5) upper floors; (6) gable infills; (7) prefab roof at wall-top height; (8) dormers and chimney seated on the slope; (9) canopy, sign, lantern, seal, props.\n"]
for a in ["A01", "A02", "A03", "A03b", "A04", "A04b", "A05", "A06", "A07", "A08"]:
    A, R = ARCH[a], AREP[a]; purpose, change, coll, custom, extra, accept = NOTES[a]
    roofs = ", ".join(sorted({p.get("roof_asset", "MV-Roof_RoundTiles_" + p["roof"])[3:] if p.get("roof") else "Roof_Tower_RoundTiles" for p in A["parts"]}))
    out.append(f"## {a} - {A['name']}\n")
    out.append(tbl(["Field", "Value"], [
        ["Purpose", purpose], ["Instances planned", arche_n[a]], ["Nominal footprint (m)", f"{A['footprint'][0]} x {A['footprint'][1]}" + (f" + {A['front_extra']} m veranda" if A.get("front_extra") else "")],
        ["Measured bounds incl. roof and props (m)", f"{R['measured_bounds_m'][0]} x {R['measured_bounds_m'][1]} x {R['measured_bounds_m'][2]} high"], ["Floors", A["floors"]], ["Roof", roofs],
        ["Source", "Quaternius Medieval Village [Standard] + Fantasy Props [Standard], glTF"], ["Other publishers' models", extra], ["Scale / rotation", "1.0; 0, 90, 180, 270 degrees"],
        ["Module instances", f"{R['instances']} ({R['unique_assets']} ids)"], ["Triangles, unoptimised", f"{R['triangles']:,}" + (f" (of which custom {R['triangles_custom']:,})" if R.get("triangles_custom") else "")],
        ["Triangles after the P2 substitutions (projection)", f"{project(R['usage'], {})[1]:,}"], ["P1.2 change", change], ["Collision", coll], ["Custom geometry", custom], ["Acceptance", accept], ["Readiness", STATUS[a] + ("" if STATUS[a] == "READY" else " - see 12")]]))
    out.append(tbl(["Block", "W x D (m)", "Floors", "Roof", "Offset (x, y, z)", "front", "right", "back", "left"],
                   [[p["id"], f"{p['W']} x {p['D']}", f"{p['floors']}" + (f" (walls from level {p['floor_from'] + 1})" if p.get("floor_from") else ""), p.get("roof") or ("tower" if p.get("tower_roof") else "-"),
                     p.get("offset", [0, 0, 0]), *[" / ".join(p["facades"].get(s, ["-"])) for s in ("front", "right", "back", "left")]] for p in A["parts"]]))
    if any(p.get("jetty") is not None for p in A["parts"]):
        out.append("Jetty: front facade from level 2 is built from `MV-Overhang_Plaster_Short` instead of the wall modules listed; windows are mounted on its face.\n")
    out.append("**Modules (id x count):** " + ", ".join(f"`{k}` x{v}" for k, v in sorted(R["usage"].items(), key=lambda kv: -kv[1])) + "\n")
for key, title, txt in (("GATE", "G01 - Gerbang Niaga split gateway (structure)", "Two open timber lodges, each 2 x 4 m with arches on all sides and a small gabled roof (`Roof_2x4_RoundTile`, `Roof_Front_Brick2`), flank a 4 m lane open to the sky. Seal on each south gable; dark roofs. Readiness: READY."),
                        ("CROSS", "M01 - Tugu Timbangan market cross (structure)", "One stair block as a 2 x 2 x 1 m base, one timber post, two seals, two bracket lanterns at 2.4 m, goods at the foot. Readiness: READY.")):
    R = AREP[key]
    out.append(f"## {title}\n\n{txt} {R['instances']} instances, {R['triangles']:,} triangles, measured {R['measured_bounds_m'][0]} x {R['measured_bounds_m'][1]} x {R['measured_bounds_m'][2]} m.\n\n"
               + ", ".join(f"`{k}` x{v}" for k, v in sorted(R["usage"].items(), key=lambda kv: -kv[1])) + "\n")
out.append("## Market stall kits\n\n" + tbl(["Kit", "Base model", "Canopy", "Goods and props", "Collision footprint (m)", "Used"],
           [[k, v["base"].split("@")[0], (v["base"].split("@")[1] + " cloth (variant)") if "@" in v["base"] else "as shipped", ", ".join(sorted({p[0] for p in v["props"]})), f"{v['rect'][0]} x {v['rect'][1]}",
             sum(1 for s in L["stalls"] if s["kit"] == k)] for k, v in L["stall_kits"].items()])
           + "\nGoods rest on flat tops measured on the meshes: Quaternius stall and cart 0.83 m, Avramania stall 0.96 m, cafe counter 1.15 m, cafe long table 0.75 m. Readiness: READY (S03, S04, S05 depend on the cafe and Avramania packs).\n")
out.append("""## Assembly notes: junctions checked

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
| Exchange Hall porch and main roof (P1.2) | Porch roof is a full 6 x 6 roof centred 1.4 m behind the porch, so its ridge runs 3 m into the main slope and is buried. The hidden half passes through the upper wall into the dark core. No open roof end |
| Jetty and roof (P1.2) | 6 x 10 roof shifted 1 m forward covers the jetty; gable infill moved to the jetty face; side cheeks are the kit's own two-storey pieces with brackets |
| Jetty windows (P1.2) | Window inserts are mounted on the plain jetty face (the overhang module has no opening). Looks correct in Blender; check for flicker in the engine |
| Timber canopy and trade sign | Signs are mounted above or beside canopies; none intersects |
""")
w("08-archetype-specifications.md", "\n".join(out))

# =============================================================================================== 09
drow = [[d["edge"], d["type"], d["length_m"], d["unpaved_samples"], d["max_step_m"], d["min_headroom_m"] if d["min_headroom_m"] else "open sky", d["min_side_clearance_m"], d["status"]] for d in VAL["D_edges"]]
fwd = ["N01->N02", "N02->N03", "N03->N04", "N04->N05", "N05->N29", "N29->N27", "N27->N06", "N06->N07", "N07->N08"]
camrow = [[g["travel"], g["type"], f"{g['unobstructed_pct']}%", g["min_camera_distance_m"], ", ".join(b.split("_")[0] for b in g["main_blockers"]) or "-"] for g in cam if g["unobstructed_pct"] < 100]
camrow.sort(key=lambda r: r[3])
gaps = [[g["a"], g["b"], g["gap_m"], g["status"]] for g in VAL["B_roof_gaps_under_3m"]]
w("09-walking-network.md", f"""
# 09 - Walking network and spatial validation (P1.2)

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
2. **Actual geometry** (`validate_envelopes.py`, re-run on the P1.2 scene): the assembled Blender scene, {VAL['triangles_tested']:,} triangles, tested with ray casts and nearest-surface queries.
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
P1.2 added jetties, a porch, signs, goods and furniture and re-ran the whole test: no edge failed on the first run, because new items were placed against the P1.1 clear zones.
(P1.1's first run had failed seven edges, all corrected then.) The tightest passages are beside the market cross (0.4 to 0.6 m to its goods).

### The two transitions named in the review

N23-N21 and N24-N22 no longer exist. In P1.0 they ran from the bazaar corners diagonally to the court sides, across 1 m of unpaved ground and through the
corners of B15 and B16. Each is replaced by two paved edges through new court entrances: N23-N25-N21 and N24-N26-N22. Both pass.

## C. Exchange Hall stair approach (edge N07-N08)

Measured risers: {", ".join(f"{r:.2f}" for r in ST['risers_m'])} m. **{ST['riser_count']} risers, largest {ST['max_riser_m']:.3f} m against the 0.42 m limit, total rise {ST['total_rise_m']:.2f} m.**
The approach is paved from the court to the podium deck with no gap. Whether the controller climbs it smoothly is an engine test for P2.

## D. Lanterns, banners, trade signs, flower boxes and vines

All {len(VAL['C_hanging'])} hanging or wall-mounted objects were measured against the surface beneath them. Rule: 2.1 m or more over walkable paving.

| Lowest five over paving | On | Clearance (m) |
|---|---|---|
""" + "\n".join(f"| `{c['asset']}` | {c['on'].split('_')[0]} | {c['clearance_m']} |" for c in hang[:5]) + f"""

**None is below 2.1 m.** P1.0's lamp-post lanterns hung at about 1.6 m inside the walking line. They are now on 3.9 m posts with the lantern at 2.5 m,
set 0.7 m outside the street's clear width with the arm along the frontage. P1.2's first run flagged two flower boxes 0.68 m above the tea-house balcony deck (moved to side windows) and showed the trade signs under the jetties at 2.11 m (raised; now 2.18 m).

## E. Market hall arch opening (`MV-Wall_Arch`, measured on the mesh)

Clear width {AR['clear_width_at_1.0m']} m from the ground to 1.9 m, {AR['clear_width_at_2.2m']} m at 2.2 m; clear height at the centre {AR['clear_height_centre_m']} m.
The 0.68 m wide, 1.9 m tall explorer passes with about 0.5 m each side. Edges N18-N31, N31-N30, N19-N32 and N32-N29 walk through arches and pass.

## F. Follow-camera line of sight

For every edge and both directions of travel, a ray is cast from the look-at point (player +1.25 m) to the documented camera position (11.8 m behind, +6.6 m).
Full distance is {cam[0]['full_distance_m']} m.

- **{SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']} travel directions are completely unobstructed.**
- **The whole primary axis, walking towards the hall, is unobstructed** except the 6 m after the market cross, where the cross's post stands between player and camera (camera shortens to 3.4 m, then recovers). The new porch, jetties and signs do not enter the camera line on the axis.
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
# 10 - Terrain interface contract (P1.2; no island is modelled)

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
| Surface treatments | Packed earth in the two back courts (x -18..-10 and 10..18, z -36..-10): a terrain material, not geometry |

**Unchanged in P1.2** (no footprint moved; jetties and the porch stay inside the P1.1 envelope). **Correction made in P1.1:** the P1.0 support zone was drawn around the developed envelope only (94.5 x 118 m) and left the southern half of the transport
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

QA = [("Architectural coherence", 4, 4, "One building kit throughout. New publishers appear only as goods and furniture. Held at 4: the Avramania stall and goods are flat-shaded and read as a different hand at close range."),
      ("Commercial identity", 3, 4, "Every shop now has a trade sign with a pictogram, a canopy or a jetty, and goods by the door; the two halls sell different things; guild offices are marked. In P1.1 shops were told apart only by long red banners."),
      ("Building proportions", 4, 4, "Unchanged modules and heights. The jetty adds 1.12 m of overhang at 3 m and reads correctly beside the 1.9 m figure. The hall was not enlarged."),
      ("Landmark hierarchy", 4, 4, "The hall gains a gabled entrance porch with the seal, darker roofs and burgundy banners, and is the visible end of the street from the gate. Held at 4: at the gameplay camera on the street the top of the tower is still out of frame."),
      ("Bazaar quality", 3, 4, "Five stall kinds instead of two, counters and tables stocked with bread, cheese, fish, pottery and books, goods stacked at the hall corners, two halls with different trades. Held at 4: from above the plaza is still a large even field of cobble."),
      ("Spatial readability", 4, 4, "Plan unchanged and still validated. The darker civic roofs and the porch make the destination easier to pick out; the lanes are as before."),
      ("Player-scale compatibility", 4, 4, f"Re-measured: {SUM['edges_total'] - 1 - SUM['edges_fail']} of {SUM['edges_total'] - 1} built edges walkable, nothing hanging below {hang[0]['clearance_m']} m, camera clear on the axis. Held at 4 until tested in the engine."),
      ("Asset constructibility", 4, 4, "Every visible component is a downloaded model, a disclosed variant or a disclosed custom item. Held at 4, not raised: there are now three publishers, an FBX pack that needs its materials re-linked, and windows mounted on the jetty face."),
      ("Visual polish", 3, 3.5, "Colour grade to the palette, afternoon light, sky gradient and a quieter ground lift the images clearly. Not a 4: no terrain or backdrop, the cobble tile still repeats, and none of it has been seen in the game's renderer."),
      ("Production efficiency", 3, 3, f"Modular system kept, no new building type, 0 new downloads for architecture. But triangles rose from {S0['triangles']:,} to {STATS['triangles']:,}, materials from 29 to {len(base_mats)}, and there are {STATS['custom_ids']} custom meshes to author. The plan in 12 projects {TOWN_NEW:,} triangles; nothing is measured in a browser.")]
a0 = sum(q[1] for q in QA) / len(QA); a1 = sum(q[2] for q in QA) / len(QA)
w("11-visual-qa-report.md", f"""
# 11 - Visual QA report: approved P1.1 and P1.2 compared

Reviewed: the four ASSET-BACKED BLENDER BLOCKOUT views of each revision from the same cameras, the archetype sheets and roof plans. These are
Blender EEVEE renders, **not browser renders**. Scores are internal and provisional. The ten criteria are those of the owner's brief; P1.1 was
re-scored on them (its own report used nine different criteria and averaged 3.78).

Side by side: [A aerial](visuals/before-after-a-aerial.png), [B merchant street](visuals/before-after-b-merchant-street.png), [C bazaar](visuals/before-after-c-central-bazaar.png), [D Exchange Hall](visuals/before-after-d-exchange-court.png).

{tbl(["Criterion", "P1.1", "P1.2", "What changed, and why the score is what it is"], QA)}
**Average {a0:.2f} to {a1:.2f} out of 5. The 4 / 5 target is not reached and is not claimed.** No criterion is at 5. The two below 4 cannot be raised inside a
Blender blockout: polish needs terrain, a backdrop and the game's lighting; efficiency needs the P2 substitutions made and measured. **Human approval is pending.**

Part of the visible improvement is presentation: the P1.2 views use warmer light and a different tone mapping than the P1.1 views. To judge
the design changes alone, compare shapes and content (jetties, porch, signs, goods), not brightness.

## View by view

| View | Works | Weak, and the root cause |
|---|---|---|
| A - The Trading Town | Roof hierarchy now reads: dark hall, halls, warehouse and lodges against lighter shops; porch marks the hall | The town still sits in an open field ringed by trees. Root cause: no terrain or island edge exists yet (P4), not a lack of props |
| B - The Merchant's Walk | Signs, canopies, jetties and flower boxes at eye level; porch and tower seal as the destination; clear centre | The camera's height shows more roof than shopfront on the near buildings. Root cause: the documented camera sits 6.6 m up in a 10 m wide street |
| C - The Bazaar of Awan | Five stall kinds, stocked counters, market cross, hall goods visible, hall dominant | Plaza surface is uniform. Root cause: one cobble tile; a paving pattern or a second tile is a P2 or P3 material task |
| D - The Exchange | Porch gives the entrance a hierarchy the flat front lacked; banners and seal in the guild colours | Court is plain by design; the lamp posts are still stretched house posts |

## Unresolved (largest first)

1. **Not seen in the game.** Lighting, colour grade, scale and motion are unverified in Three.js.
2. **Blockout finish.** Temporary ground, no backdrop, repeating cobble.
3. **Mixed shading styles at close range.** The Avramania stall and goods are flat-shaded; the cafe pack is semi-realistic; Quaternius is hand-painted.
4. **Tower top at the street camera** is cropped, as in P1.1.
5. **Jetty windows** are mounted on the face of a module that has no opening; fine in Blender, to be checked for flicker in the engine.
6. **Seal and sign pictograms** are first proposals and need the owner's eye.
7. **Chimneys have no flashing piece**; dormer cheeks sink slightly into the tiles (unchanged).
""")


# =============================================================================================== 12
rows = []
for a in ["A01", "A02", "A03", "A03b", "A04", "A04b", "A05", "A06", "A07", "A08"]:
    cur, new = project(AREP[a]["usage"], {})
    rows.append([a, ARCH[a]["name"], arche_n[a], AREP[a]["instances"], f"{cur:,}", f"{new:,}", STATUS[a]])
w("12-p2-construction-contract.md", f"""
# 12 - P2 construction contract (revised in P1.2; not started; needs explicit authorisation)

P2 builds the eight archetypes with their two variants, the split gateway, the market cross and the stall kits as reusable assemblies. It does not
assemble the town (P3) or build terrain (P4). No further asset search is needed; the sources are fixed in 04.

## Inputs

- Archives and hashes: 04. Modules per archetype, with exact model identifiers, material strategy, collision and acceptance: 08. Custom and variant items: 03b. Assembler and data: `citadel_lib.py`, `town_data.py`.
- Grid: 2 m bays, 3 m storeys, authored scale, 90-degree rotations.

## Roster, readiness and triangle budget

{tbl(["ID", "Archetype", "Instances in town", "Module instances", "Triangles now", "Triangle budget (projection)", "Readiness"], rows)}
**READY** (essential modules verified, assembly executable as written): A01, A03b, A04, A04b, A05, A06, A07, gateway, market cross.

**CONDITIONAL** (one specific dependency each):

| ID | Dependency | Closes when |
|---|---|---|
| A02 | The two dressing kits use the cafe pack, whose FBX files need their materials re-linked from the pack's Blender file, and Avramania goods | One conversion of the used cafe models to GLB with materials embedded is made and checked; owner approves both sources |
| A03 | Windows are mounted on the face of the jetty module, which has no opening | First A03 export shows no flicker in the engine, or an opening is cut |
| A08 | Hanging inn sign and flower boxes are Avramania models | Owner approves the source |

**BLOCKED:** none.

Items P2 must author rather than assemble (03b): the seal, one trade-sign mesh with seven pictograms and three field colours, three cloth material
instances, the dark roof material instance, the graded textures, and a purpose-made lamp post.

## Shared components (build first)

| Component | Used by |
|---|---|
| Plaster bays `Wall_Plaster_*`; stone bays `Wall_UnevenBrick_*` | all enclosed archetypes |
| Window inserts, shutters, door leaves | all enclosed archetypes |
| Posts `Corner_ExteriorWide_Wood`; ground-floor piers `Corner_Exterior_Brick` | all |
| Roofs `Roof_RoundTiles_4x6, 6x6, 6x8, 8x8, 8x12, 8x14`, `Roof_2x4_RoundTile`; gables `Roof_Front_Brick2/4/6/8` | all |
| Dormer, chimneys, timber canopy | A03, A03b, A04, A05, A06, A07, A08 |
| Jetty set `Overhang_Plaster_Short`, `Overhang_Side_Plaster_Short_L/R`, roof `6x10` | A03 |
| Porch set: `Wall_Arch`, `Corner_Exterior_Brick`, roof `6x6`, gable `Roof_Front_Brick6` | A01 |
| `Wall_Arch` arcade bay | A02, gateway |
| Signage kit: custom trade sign, burgundy / blue / cream cloth instances, seal, lantern | all frontages |
| Goods kit: cafe counters, tables, shelves, kegs; Avramania food; Quaternius pots, bottles, books | A02, stalls, tea terrace |

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Bake the colour grade of 05 into copies of the base-colour textures. Merge duplicate materials **only where the node set-up is identical** (same-named Quaternius materials differ by whether the mesh has vertex colours). Author the cloth and dark-roof instances, the seal and the sign.
2b. Convert the used cafe-pack models to GLB once, with their materials; atlas them.
3. Shared wall, window and door sub-assemblies.
4. A04 and A04b. 5. A03 and A03b. 6. A05 and A06.
7. A02 market hall, gateway lodges, market cross (same arcade system).
8. A01 Exchange Hall: main block, wings, tower above the roof, entrance porch, deck and skirt, stairs.
9. A07 warehouse, A08 tea house.
10. Apply the substitutions below; join static meshes per building by material.
11. One archetype exported and loaded in the real Three.js scene; measurements recorded; stop for approval.

## Quantified preliminary optimisation plan

Measured in Blender for the P1.2 blockout: **{STATS['instances']:,} instances, {len(used_models)} downloaded models, {STATS['triangles']:,} triangles, {len(base_mats)} distinct materials
({STATS['material_count']} duplicated slots as imported)** (architecture and nature textures up to 2048 px, props up to 4096 px, cafe pack with normal and roughness maps). The approved P1.1 was {S0['triangles']:,} triangles and 29 materials.

Triangles by category: {CATLINE}.
Island 1 is documented at 327-412 draw calls and about 2.5 million submitted triangles across all passes.

High-triangle components and the substitution proposed for each:

{tbl(["Component", "Instances", "Triangles each", "Total now", "Target each", "Saving", "How"], opt_rows)}
| Projection | Triangles |
|---|---|
| P1.2 blockout, measured | {TOWN_CUR:,} |
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

The brief's earlier figure of about 350,000 triangles is treated as provisional: the projection above does not reach it with substitutions alone. Reaching it would need fewer or lower-detail backdrop trees, lower-detail wall and roof modules, or fewer lanterns, each to be decided on measured evidence, not by deleting architecture.

**Browser performance has not been validated.** Every number in this section comes from Blender.

## Acceptance for P2 as a whole

Each archetype matches its P1.2 render, uses only inventoried modules plus the items in 03b, loads in the real scene at correct scale, and has triangle,
material and draw-call counts recorded. Then stop for approval before P3.
""")

w("13-limitations-and-risks.md", f"""
# 13 - Risk and feasibility register (P1.2)

## Not verified

- **Nothing was loaded in Three.js.** All renders are Blender EEVEE. Browser appearance, frame rate, real collision and real camera behaviour are untested.
- The walkability and camera checks use ray casts against render geometry with constants copied from the project. They are evidence about the layout, not a run of the game.
- The colour grade and cloth colours were judged under Blender's light and tone mapping only.
- General browsing of OpenGameArt and the itch.io 3D tag was not carried out beyond the named candidates.

## Licensing and provenance

| Item | State | Action |
|---|---|---|
| Syntaxes of Play cafe pack | CC0 stated on the page; no licence file in the archive | Save a dated copy of the page with the P2 assets |
| Avramania Food & Market, Village Builder | CC0 in the archive; ReadMe states no AI-generated meshes | Owner to confirm that script-built models made with an AI coding assistant are acceptable |
| Avramania Props, Interiors, Nature | Contain unidentified AI-generated meshes | Not used. Do not add them later without an owner decision |
| Quaternius, Kenney | Unchanged | - |

## Geometry and assembly

| Item | Risk | Mitigation |
|---|---|---|
| Jetty windows surface-mounted on `Overhang_Plaster_Short` | Z-fighting or a visible frame gap in the engine | Check on the first A03 export; if needed cut an opening or offset the insert 1 cm |
| Porch roof runs through the hall's upper wall into the main roof | Hidden inside the walls in Blender; overlapping roof surfaces could flicker at the junction | Inspect the junction in the engine; trim the hidden half of the porch roof on export |
| Cafe pack FBX | Texture paths do not resolve; materials come from the pack's `.blend` by name | Convert once to GLB with materials embedded and record the conversion |
| Same-named Quaternius materials differ by mesh | Merging them by name turned lantern metal black in this revision (the importer adds a vertex-colour multiply only where the mesh has vertex colours) | Merge materials only where the node set-up is identical |
| Custom seal and signs | {STATS['custom_ids']} small meshes to author | One seal mesh and one sign mesh with a pictogram atlas |

## Performance

| Risk | Likelihood | Mitigation |
|---|---|---|
| Triangle load too high in the browser | Medium | {STATS['triangles']:,} now; substitutions in 12 project {TOWN_NEW:,}; measure one archetype early in P2 |
| Material and texture count | Medium to high | {len(base_mats)} materials now; atlas the cafe pack; bake the grade into shared textures |
| Small goods are heavy | Medium | Avramania cabbage 1,448 and flower box 1,330 triangles each; simplify or merge per stall |
| Lanterns, piers and trees | Medium | Still the three largest contributors (12) |

## Design

| Risk | Likelihood | Mitigation |
|---|---|---|
| Owner prefers the approved P1.1 seal or colours | Open | P1.1 is preserved in `visuals/p1.1/`; either set can be built |
| Mixed shading styles noticed in play | Medium | Keep other publishers to small goods; drop the Avramania stall if it jars |
| Town reads as standing in a field | Certain until P4 | Terrain and island edge are P4; the support zone is defined in 10 |
| Engine collision differs from the ray test | Medium | Repeat sections B and F of 09 in the engine |

## Resolved or reduced since P1.1

| P1.1 limitation | State |
|---|---|
| Only two stall models | Reduced: five stall kinds from three sources |
| Shops identified only by red banners | Resolved: pictogram trade signs |
| Hall built from house parts with a flat front | Reduced: entrance porch, dark roofs |
| Overhang / jetty modules unassembled | Resolved: assembled on A03 and rendered |
| Stall counter height set by eye | Resolved: flat tops measured on the meshes (0.83, 0.96, 1.15 m) |

## Differences from the supplied concept images (unchanged)

European half-timber and stone, not Indonesian-tropical; {nb} buildings and {ns} stalls rather than 21 and 12; straight streets on a 2 m grid; a stone-based hall with a porch and crossing tower rather than a multi-tier roof.

## Housekeeping

- Downloads, extracted files, tiles, the P1.0 and P1.1 comparison sets and the blockout `.blend` are in `.asset-inspection/merchant-citadel-p1/` (about 1.5 GB, ignored by Git).
- No production file, earlier asset, island-1 content or game code was changed. No GLB was exported. Nothing was committed or deployed.
""")


w("16-p1.2-change-log.md", f"""
# 16 - P1.2 change log and approval dependencies

P1.2 executes the owner's brief titled "Merchant Citadel P1.1 - Complete visual redesign and expanded asset integration". It revises the approved
P1.1 town in place. The approved P1.1 images are preserved in `visuals/p1.1/`; P1.1 data, documents and blockout are preserved in the inspection
workspace under `p1.1/`.

## Baseline confirmed from the files (the brief quoted P1.0 figures)

| Attribute | Brief (P1.0) | Approved P1.1 | P1.2 |
|---|---|---|---|
| Permanent buildings | 17 | 17 | {nb} |
| Market stalls | 10 | 12 | {ns} (count kept; five kinds instead of two) |
| Archetypes | 8 | 8 + 2 variants | 8 + 2 variants |
| Developed footprint | 74.5 x 98 m | 74.5 x 98 m | {x1 - x0} x {n1 - n0} m |
| Walking graph | 24 nodes, 32 edges | 31 nodes, 39 edges | {len(L['nodes'])} nodes, {len(L['edges'])} edges |
| Unique downloaded models used | 82 | 84 | {len(used_models)} |
| Instances | 1,971 | 2,092 | {STATS['instances']:,} |
| Triangles, unoptimised | 858,850 | {S0['triangles']:,} | {STATS['triangles']:,} |
| Internal QA average | 3.56 | 3.78 (own criteria) / {a0:.2f} (brief's criteria) | {a1:.2f} |

## What changed

| Area | Change |
|---|---|
| Colour | Roof, timber, plaster, stone, paving and foliage graded to the brief's palette; civic roofs one value darker |
| Identity | New seal (crossing trade routes and diamond); burgundy guild and blue market cloth replace teal and saffron; long red shop banners replaced by {SIGNS} timber trade signs with pictograms |
| Shophouses | A03 upper floor jettied 1.12 m; A03b and A04 gain timber canopies; flower boxes, vines, lanterns |
| Exchange Hall | Gabled entrance porch on stone piers with the seal; three upper windows behind it replaced by plain bays; dark roofs; burgundy banners |
| Market halls | One assembly, two dressing kits: provisions (west, blue) and crafts (east, burgundy) |
| Stalls | Same 12 positions; five kinds: Quaternius stall and cart in three cloths, Avramania striped stall, cafe counter, cloth-covered wares table; goods on measured counter heights |
| Tea house | Cafe tables, chairs, stools, cloths, mugs, pitcher, menu stand, keg; cup sign and hanging inn sign |
| Dressing | Goods at the four inner hall corners; a well in the west back court; packed-earth back courts |
| Presentation | Afternoon light, sky gradient, Khronos PBR Neutral view transform, larger and quieter temporary ground |
| Unchanged | Every building position and rotation, the 12 stall positions, all {len(L['nodes'])} nodes and {len(L['edges'])} edges, all paved surfaces, the gateway, the market cross position, the four cameras |

## Defects found and corrected during P1.2

Hall porch lanterns poking through the porch roof (removed); cloth colours too bright at the first gain (reduced per colour); trade signs under the jetties 1 cm
above the 2.1 m limit (raised to 2.18 m); two flower boxes over the tea-house balcony flagged by the hanging check (moved to side windows);
lantern metal rendering black after same-named materials were merged (merge removed; recorded as a P2 rule).

## Changed files (all under `docs/planning/merchant-citadel/p1/`)

| File | Change |
|---|---|
| `README.md`, `01`, `02`, `04`, `05`, `11`, `13` | Rewritten for P1.2 |
| `06`, `08`, `09`, `10`, `12` | Updated for P1.2 (tables regenerated from the new measurements) |
| `03-verified-asset-inventory.csv` | {len(MEAS)} rows: 613 unchanged originals plus 305 expansion models with decisions |
| `03b-custom-and-variant-register.csv` | New seal, trade signs, cloth and roof variants, colour grade, assembly notes |
| `07-building-placement-schedule.csv`, `07b-market-stall-schedule.csv` | Regenerated; positions unchanged |
| `16-p1.2-change-log.md` | **New** (this file) |
| `14-p1.1-change-log.md`, `15-owner-approval-record.md` | Unchanged |
| `asset-evidence/archive-manifest.md`, `license-evidence.md` | New sources appended; earlier content unchanged |
| `asset-evidence/spatial-validation-actual-geometry.json`, `usage-and-triangles.json`, `imported-model-register.csv` | Regenerated |
| `visuals/view-a..d-*.png`, `before-after-*.png`, `archetype-*.png`, `orthographic-town-plan.png`, `blockout-top-orthographic.png` | Regenerated |
| `visuals/expansion-asset-contact-sheet.png` | **New** |
| `visuals/p1.1/` | **New folder:** the 13 approved P1.1 images, unchanged |
| `blender-inspection/fetch_expansion.py`, `inspect_expansion.py`, `make_docs_p12.py` | **New** |
| `blender-inspection/citadel_lib.py`, `town_data.py`, `build_town.py`, `validate_envelopes.py`, `make_package_assets.py` | Updated |
| `blender-inspection/make_docs.py` | Unchanged; it is the P1.1 generator |

Outside the package: `../merchant-citadel-p1.2-review.zip` is generated from this folder. The P1.1 zip is left in place.

## Remaining approval dependencies

1. **Visual approval of P1.2**, or a decision to stay with the approved P1.1. Self-assessed average {a1:.2f} / 5; the 4 / 5 target is not claimed.
2. **Asset approval:** use of the Syntaxes of Play cafe pack and of Avramania's Food & Market and Village Builder packs, including the point that Avramania's models are script-built with an AI coding assistant.
3. **The new guild seal**, which replaces the seal approved in P1.1.
4. **The new cloth colours** (burgundy guild, blue market), which replace the teal, saffron and red approved in P1.1.
5. **The trade-sign pictograms** (loaf, jar, hammer, crate, coin, cup, scroll).
6. **A triangle and draw-call budget** for the town, so the pass conditions in 12 can be fixed.
7. **Authorisation to start P2.** Not assumed.

**MERCHANT CITADEL P1.2 - PENDING HUMAN VISUAL AND ASSET APPROVAL. STOP.**
""")
print("docs written", f"QA {a0:.2f} -> {a1:.2f}", "projection", TOWN_CUR, "->", TOWN_NEW, "materials", len(base_mats), "primary", prim, "seals", SEALS, "signs", SIGNS)

