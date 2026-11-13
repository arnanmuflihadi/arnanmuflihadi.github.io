#!/usr/bin/env python3
"""Build the non-Blender P1.2 package artefacts from the measured data (plain Python + Pillow + matplotlib).

Usage: python3 make_package_assets.py <inspection_dir> <package_dir>
Outputs: visuals/*.png (labelled views, before/after pairs, archetype sheets, dimensioned plan), the schedules,
         03-verified-asset-inventory.csv, 03b-custom-and-variant-register.csv, asset-evidence/*.
"""
import csv, json, math, os, shutil, sys
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

I, P = sys.argv[1], sys.argv[2]
L = json.load(open(f"{I}/data/layout.json")); ARCH = json.load(open(f"{I}/data/archetypes.json"))
MEAS = json.load(open(f"{I}/measurements.json")) + json.load(open(f"{I}/measurements-expansion.json")); MAN = {m["pack_id"]: m for m in json.load(open(f"{I}/archives/archive-manifest.json"))}
STATS = json.load(open(f"{I}/renders/town-stats.json")); AREP = json.load(open(f"{I}/archetypes/archetype-report.json"))
VAL = json.load(open(f"{I}/validation.json"))
os.makedirs(f"{P}/visuals", exist_ok=True); os.makedirs(f"{P}/asset-evidence", exist_ok=True)
PFX = {"quaternius-medieval-village": "MV", "quaternius-fantasy-props": "FP", "quaternius-stylized-nature": "SN", "kenney-fantasy-town-kit": "KFT", "kenney-modular-buildings": "KMB",
       "synofplay-medieval-cafe": "SY", "avramania-free-collection": "AV", "kaykit-medieval-builder": "KK"}
PFX.update({k: "PP" for k in MAN if k.startswith("polypizza")})
AV_OK = ("Food_Market", "Village_Builder")          # Avramania packs whose ReadMe states that no model was AI-generated
AV_AI = ("Props_Tools_Fencing", "Interiors_Furniture", "Nature_Terrain")   # ReadMe: some models started as Tripo AI meshes, not identified individually
ZIPNAME = {"kenney-fantasy-town-kit": "kenney_fantasy-town-kit.zip (signed link; saved under this name)", "kenney-modular-buildings": "kenney_modular-buildings.zip (signed link; saved under this name)"}
SRC = {k: v["source_page"] for k, v in MAN.items()}
ENV = {a["id"]: a for a in VAL["A_envelopes"]}


def font(size, bold=False):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1 if bold else 0)
    except Exception:
        return ImageFont.load_default()


def label(src, dst, title, klass, note):
    im = Image.open(src).convert("RGB"); w, h = im.size; bar = 64
    out = Image.new("RGB", (w, h + bar), (24, 44, 40)); out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    d.text((16, h + 8), title, font=font(22, True), fill=(245, 240, 225)); d.text((16, h + 37), note, font=font(15), fill=(190, 205, 198))
    tw = d.textlength(klass, font=font(18, True))
    d.rectangle([w - tw - 40, h + 14, w - 14, h + 50], fill=(196, 120, 40)); d.text((w - tw - 27, h + 21), klass, font=font(18, True), fill=(255, 255, 255))
    out.save(dst, optimize=True)


BLK = "ASSET-BACKED BLENDER BLOCKOUT"
note = "P1.2. Downloaded CC0 models (Quaternius, Syntaxes of Play, Avramania) + CUSTOM seal and trade signs, cloth / roof colour variants, colour grade. Temporary: ground, dark interior cores, 1.9 m explorer. Afternoon presentation light."
VIEWS = [("view-a-aerial", "View A - The Trading Town: elevated three-quarter aerial (same camera as P1.0 and P1.1)"), ("view-b-merchant-street", "View B - The Merchant's Walk: Koridor Niaga at the gameplay camera (FOV 60, 11.8 m behind, +6.6 m)"),
         ("view-c-central-bazaar", "View C - The Bazaar of Awan: Pasar Awan from the southern edge (same camera as P1.1)"), ("view-d-exchange-court", "View D - The Exchange: Balai Niaga Awan from Pelataran Bursa at 1.65 m eye height (same camera)")]
for v, title in VIEWS:
    label(f"{I}/renders/{v}.png", f"{P}/visuals/{v}.png", title, BLK, note)
    a, b = Image.open(f"{I}/p1.1/{v}.png").convert("RGB"), Image.open(f"{I}/renders/{v}.png").convert("RGB")
    w, h = 1280, 720
    s = Image.new("RGB", (w * 2 + 12, h + 56), (24, 44, 40)); s.paste(a.resize((w, h), Image.LANCZOS), (0, 56)); s.paste(b.resize((w, h), Image.LANCZOS), (w + 12, 56))
    d = ImageDraw.Draw(s); d.text((16, 14), "BEFORE - P1.1 (approved)", font=font(24, True), fill=(235, 200, 170)); d.text((w + 28, 14), "AFTER - P1.2", font=font(24, True), fill=(170, 230, 215))
    d.text((340, 20), title.split(" - ")[1][:64], font=font(15), fill=(190, 205, 198))
    s.save(f"{P}/visuals/before-after-{v[5]}-{v[7:]}.png", optimize=True)
label(f"{I}/renders/blockout-top-ortho.png", f"{P}/visuals/blockout-top-orthographic.png", "Top orthographic render of the same blockout (north up)", BLK, note)

ids = ["A01", "A02", "A03", "A03b", "A04", "A04b", "A05", "A06", "A07", "A08", "GATE", "CROSS"]
tw, th = 620, 524
sheet = Image.new("RGB", (4 * tw, 6 * (th + 54) + 70), (244, 243, 238)); d = ImageDraw.Draw(sheet)
d.text((14, 12), "Merchant Citadel P1.2 - archetype assemblies (ASSET-BACKED ASSEMBLY, front and rear). Seal and trade signs = CUSTOM geometry; cloth colours and dark civic roofs = material variants.", font=font(22, True), fill=(24, 44, 40))
for i, a in enumerate(ids):
    col, row = i % 4, i // 4
    for j, v in enumerate(("front", "rear")):
        im = Image.open(f"{I}/archetypes/{a}-{v}.png").convert("RGBA").resize((tw, th), Image.LANCZOS)
        x, y = col * tw, 70 + (row * 2 + j) * (th + 54)
        d.rectangle([x + 4, y, x + tw - 4, y + th + 50], fill=(226, 228, 226)); sheet.paste(im, (x, y), im)
        r = AREP[a]
        d.text((x + 12, y + th + 4), f"{a} {ARCH[a]['name']} - {v}"[:66], font=font(16, True), fill=(20, 30, 30))
        d.text((x + 12, y + th + 27), f"{r['instances']} instances, {r['unique_assets']} ids, {r['triangles']:,} tris unoptimised ({r.get('triangles_custom', 0):,} custom)", font=font(14), fill=(70, 80, 78))
sheet.save(f"{P}/visuals/archetype-assembly-sheet.png", optimize=True)
tops = Image.new("RGB", (6 * 420, 2 * 400 + 60), (244, 243, 238)); d = ImageDraw.Draw(tops)
d.text((14, 12), "Merchant Citadel P1.2 - roof plans (top orthographic) of every assembly: evidence for roof junctions", font=font(22, True), fill=(24, 44, 40))
for i, a in enumerate(ids):
    im = Image.open(f"{I}/archetypes/{a}-top.png").convert("RGBA").resize((420, 355), Image.LANCZOS)
    x, y = (i % 6) * 420, 60 + (i // 6) * 400
    tops.paste(im, (x, y), im); d.text((x + 10, y + 360), f"{a} {ARCH[a]['name']}"[:48], font=font(14, True), fill=(20, 30, 30))
tops.save(f"{P}/visuals/archetype-roof-plans.png", optimize=True)

# ---- dimensioned orthographic plan -------------------------------------------------------------
COL = {"A01": "#b5533c", "A02": "#c98a4b", "A03": "#d6a15c", "A03b": "#d6a15c", "A04": "#e3bf86", "A04b": "#e3bf86", "A05": "#a9744f", "A06": "#8f8f8a", "A07": "#7d7468", "A08": "#c7a2b8"}
TILE = {"MV-Floor_UnevenBrick": "#cfc7b6", "MV-Floor_Brick": "#c2b29f", "MV-Floor_RedBrick": "#cfa58e"}
fig, ax = plt.subplots(figsize=(15, 18.5), dpi=130); ax.set_facecolor("#dfe8cf")
x0, x1, n0, n1 = L["envelope"]
rx0, rx1, rn0, rn1 = L["reserved"][0][1:]
ux0, ux1, un0, un1 = min(x0, rx0), max(x1, rx1), min(n0, rn0), max(n1, rn1)
ax.add_patch(Rectangle((ux0 - 10, un0 - 10), ux1 - ux0 + 20, un1 - un0 + 20, fill=False, ls=(0, (6, 4)), lw=1.6, ec="#4d6b3a"))
ax.text(ux0 - 9.5, un1 + 8.2, f"Terrain support zone = (developed envelope + transport reservation) + 10 m: {ux1 - ux0 + 20:.1f} x {un1 - un0 + 20:.0f} m (assumption)", fontsize=8.5, color="#3c5a2c")
ax.add_patch(Rectangle((x0, n0), x1 - x0, n1 - n0, fill=False, ls=":", lw=1.2, ec="#555"))
for pv in L["paving"]:
    name, a, b, c, e, tile = pv
    ax.add_patch(Rectangle((a, c), b - a, e - c, fc=TILE[tile], ec="none", lw=0))
for name, a, b, c, e in L.get("yards", []):
    ax.add_patch(Rectangle((a, c), b - a, e - c, fc="#d9c7a3", ec="#a08a5c", lw=0.6, ls=":"))
    ax.text((a + b) / 2, e - 1.4, "packed-earth court", ha="center", fontsize=6.2, color="#6b5a35")
for name, a, b, c, e in L["reserved"]:
    ax.add_patch(Rectangle((a, c), b - a, e - c, fill=False, hatch="//", ec="#3a6ea5", lw=1.2))
    ax.text((a + b) / 2, (c + e) / 2, "RESERVED\nfuture transport\n20 x 16 m", ha="center", va="center", fontsize=8, color="#3a6ea5")
for b in L["buildings"]:
    r = b["rect"]; e = ENV.get(b["id"])
    if e:
        ax.add_patch(Rectangle((e["full_x"][0], e["full_n"][0]), e["full_x"][1] - e["full_x"][0], e["full_n"][1] - e["full_n"][0], fill=False, ls="--", lw=0.8, ec="#7a2d1c"))
    ax.add_patch(Rectangle((r[0], r[2]), r[1] - r[0], r[3] - r[2], fc=COL[b["archetype"]], ec="#2b2b2b", lw=1.1))
    ax.text((r[0] + r[1]) / 2, (r[2] + r[3]) / 2, f"{b['id']}\n{b['archetype']}", ha="center", va="center", fontsize=8.2, weight="bold", color="white" if b["archetype"] in ("A01", "A05", "A06", "A07") else "#222")
    ax.plot(*b["door"], marker="^" if b["rz"] == 180 else "v" if b["rz"] == 0 else ">" if b["rz"] == 90 else "<", color="#111", ms=5)
gx, gn = L["gate"][0], L["gate"][1]
for sx in (-3, 3):
    ax.add_patch(Rectangle((gx + sx - 1, gn - 2), 2, 4, fc="#b98a55", ec="#3a2412", lw=1.2))
ax.text(gx + 5.0, gn, "G01 split gateway", fontsize=7.5, va="center")
cx, cn = L["cross"][0], L["cross"][1]
ax.add_patch(Rectangle((cx - 1, cn - 1), 2, 2, fc="#8C3E45", ec="#111", lw=1)); ax.text(cx, cn + 1.9, "M01 market cross", ha="center", fontsize=7, color="#4a1c22")
for s in L["stalls"]:
    r = s["rect"]; kit = s["kit"]
    ax.add_patch(Rectangle((r[0], r[2]), r[1] - r[0], r[3] - r[2], fc={"S01b": "#345D80", "S01g": "#8C3E45", "S01c": "#efe6cf", "S02c": "#efe6cf", "S02g": "#8C3E45", "S03": "#b9c6d6", "S04": "#8a6a46", "S05": "#8a6a46"}[kit], ec="#111", lw=0.5))
EC = {"primary": ("#d62728", 2.4), "secondary": ("#1f77b4", 1.6), "service": ("#e6a700", 1.6), "market": ("#8a4fbf", 1.3), "scenic": ("#2a9d8f", 1.6), "reserved link": ("#3a6ea5", 1.0)}
for a, b, kind in L["edges"]:
    k = kind.split(",")[0]
    (xa, na, _), (xb, nb, _) = L["nodes"][a], L["nodes"][b]
    ax.plot([xa, xb], [na, nb], color=EC[k][0], lw=EC[k][1], ls="--" if k in ("service", "reserved link") else "-", alpha=0.9, zorder=5)
for k, (x, n, nm) in L["nodes"].items():
    ax.plot(x, n, "o", ms=8.5, mfc="white", mec="#111", zorder=6); ax.text(x, n, k[1:], ha="center", va="center", fontsize=5.8, zorder=7)


def dim(xa, na, xb, nb, txt, off=(0, 0)):
    ax.annotate("", (xa, na), (xb, nb), arrowprops=dict(arrowstyle="<->", color="#111", lw=0.9))
    ax.text((xa + xb) / 2 + off[0], (na + nb) / 2 + off[1], txt, fontsize=7.5, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.85))


dim(-4, 15.5, 4, 15.5, "8.0 m clear", (0, 1.2)); dim(-22, 64.2, 22, 64.2, "bazaar plaza 44 m", (-11, 1.2)); dim(-23.2, 36, -23.2, 62, "26 m", (-2.2, 0))
dim(-18, 73, 18, 73, "civic court 36 x 12 m", (10.5, -1.2)); dim(-4.5, 46.8, 4.5, 46.8, "9.0 m between stall fronts", (0, 1.2))
dim(-22, 30, -18, 30, "4 m", (0, 1.1)); dim(18, 33, 22, 33, "4 m", (0, 1.1)); dim(-2, 2.6, 2, 2.6, "4 m open", (0, -1.1))
dim(x0, n0 - 19, x1, n0 - 19, f"developed envelope {x1 - x0:.1f} m (E-W)", (16, -1.4)); dim(x1 + 5, n0, x1 + 5, n1, f"{n1 - n0:.0f} m (N-S)", (3.4, 0)); dim(-14, 91.3, 14, 91.3, "podium 28 m (+1.0 m)", (0, 1.2))
for t, x, n in (("D1 Gerbang Niaga", -10.5, -6.6), ("D2 Koridor Niaga", 0, 29.5), ("D3 Pasar Awan", 0, 37.6), ("D4 Pelataran Bursa", 0, 69.6), ("D5 Balai Niaga Awan", 0, 88),
                ("D6 Lorong Lentera", -20, 8.6), ("D7 Jalur Gudang", 20, 8.6), ("D8 Tea Lookout", 40, 46.2)):
    ax.text(x, n, t, ha="center", fontsize=8.5, style="italic", color="#16302b", bbox=dict(fc="#f4f1e6", ec="#16302b", lw=0.5, pad=1.5), zorder=8)
ax.add_patch(FancyArrow(x1 + 9, n1 - 4, 0, 8, width=0.6, head_width=2.6, head_length=3, color="#111")); ax.text(x1 + 9, n1 + 8.6, "N", ha="center", fontsize=13, weight="bold")
ax.plot([x0, x0 + 20], [un0 - 5, un0 - 5], color="#111", lw=3); ax.text(x0 + 10, un0 - 4.2, "20 m", ha="center", fontsize=8)
handles = ([plt.Line2D([0], [0], color=c, lw=w, label=k) for k, (c, w) in EC.items()]
           + [Rectangle((0, 0), 1, 1, fc=COL[a], ec="#222", label=f"{a} {ARCH[a]['name']}"[:44]) for a in ("A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08")]
           + [Rectangle((0, 0), 1, 1, fill=False, ls="--", ec="#7a2d1c", label="measured envelope incl. roof, signs"), Rectangle((0, 0), 1, 1, fc=TILE["MV-Floor_Brick"], label="dressed brick (guild way, court, halls)"),
              Rectangle((0, 0), 1, 1, fc=TILE["MV-Floor_RedBrick"], label="red brick (artisan lane, terrace)"), Rectangle((0, 0), 1, 1, fc=TILE["MV-Floor_UnevenBrick"], label="cobble")])
ax.legend(handles=handles, loc="lower right", fontsize=7.2, framealpha=0.95, title="Routes, archetypes, surfaces")
ax.set_xlim(ux0 - 14, ux1 + 15); ax.set_ylim(un0 - 14, un1 + 12); ax.set_aspect("equal")
ax.set_xlabel("x east (m)  -  project x"); ax.set_ylabel("n north (m)  -  project z = -n")
ax.set_title("Merchant Citadel / Kota Niaga Awan - revised measured town plan (P1.2, generated from layout data and measured envelopes; origin = arrival court centre)", fontsize=10.5)
ax.grid(True, color="#ffffff", lw=0.4, alpha=0.6); fig.tight_layout(); fig.savefig(f"{P}/visuals/orthographic-town-plan.png"); plt.close(fig)

# ---- schedules (nominal + measured) --------------------------------------------------------------
FRONT = {0: "south (+z)", 90: "east (+x)", -90: "west (-x)", 180: "north (-z)"}
with open(f"{P}/07-building-placement-schedule.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow("building_id,archetype_id,district,label,position_x,position_y,position_z,rotation_y,footprint_width,footprint_depth,height,entrance_location_x,entrance_location_z,frontage_direction,"
               "measured_envelope_x_min,measured_envelope_x_max,measured_envelope_z_min,measured_envelope_z_max,measured_envelope_width_x,measured_envelope_depth_z,sign_or_kit,asset_dependencies,status,change_since_p1_1".split(","))
    P10 = {b["id"]: b for b in json.load(open(f"{I}/p1.1/data/layout.json"))["buildings"]}
    OLDENV = {a["id"]: a for a in json.load(open(f"{I}/p1.1/validation.json"))["A_envelopes"]}
    NOTE = {"A01": "entrance porch added; roofs civic dark; burgundy banners; new seal", "A02": "restocked (kit per hall); roof civic dark; new seal", "A03": "upper floor jettied 1.12 m (roof 2 m longer); trade sign; flower boxes",
            "A03b": "timber canopy, trade sign and flower boxes added", "A04": "timber canopy and trade sign added", "A04b": "trade sign, lantern and vine added", "A05": "trade signs and flower boxes added",
            "A06": "trade sign and vine added", "A07": "roof civic dark; new seal; vines", "A08": "trade sign, hanging inn sign, flower boxes"}
    DEPS = lambda arch: "Quaternius Medieval Village + Fantasy Props [Standard]" + ("; Syntaxes of Play Medieval Cafe; Avramania Food & Market" if arch == "A02" else "; Avramania Village Builder" if arch in ("A03", "A03b", "A05", "A08") else "") + "; CUSTOM seal / trade sign"
    for b in L["buildings"]:
        a = ARCH[b["archetype"]]; e = ENV[b["id"]]; old = P10.get(b["id"], {})
        ch = []
        if old.get("archetype") != b["archetype"]: ch.append(f"archetype {old.get('archetype')} -> {b['archetype']}")
        if (old.get("x"), old.get("n")) != (b["x"], b["n"]): ch.append(f"moved from ({old.get('x')}, {-old.get('n', 0)})")
        if old.get("rz") != b["rz"]: ch.append(f"rotation {old.get('rz')} -> {b['rz']}")
        w.writerow([b["id"], b["archetype"], b["district"], b["label"], b["x"], 1.0 if b["archetype"] == "A01" else 0.0, -b["n"], b["rz"], a["footprint"][0], a["footprint"][1], a["height_m"],
                    round(b["door"][0], 2), round(-b["door"][1], 2), FRONT[b["rz"]], e["full_x"][0], e["full_x"][1], -e["full_n"][1], -e["full_n"][0], e["full_size"][0], e["full_size"][1],
                    "; ".join(f"{k}={v}" for k, v in sorted(b.get("opts", {}).items())) or "guild seal", DEPS(b["archetype"]),
                    "PLANNED - asset-backed blockout rendered in P1.2", "; ".join(ch + ["position unchanged" if not ch else "", NOTE[b["archetype"]],
                                                                                         f"envelope {OLDENV[b['id']]['full_size'][0]} x {OLDENV[b['id']]['full_size'][1]} -> {e['full_size'][0]} x {e['full_size'][1]} m"]).replace("; ; ", "; ").strip("; ")])
    for gid, key, pos in (("G01", "GATE", L["gate"]), ("M01", "CROSS", L["cross"])):
        e = ENV[gid]
        w.writerow([gid, key, "D1 Gerbang Niaga" if gid == "G01" else "D3 Pasar Awan", ARCH[key]["name"] + " (structure)", pos[0], 0.0, -pos[1], 0, *ARCH[key]["footprint"], ARCH[key]["height_m"], "", "", "south (+z)",
                    e["full_x"][0], e["full_x"][1], -e["full_n"][1], -e["full_n"][0], e["full_size"][0], e["full_size"][1], "guild seal", "Quaternius Medieval Village [Standard]; CUSTOM seal",
                    "PLANNED - asset-backed blockout rendered in P1.2", "position unchanged; roofs civic dark; new seal" if gid == "G01" else "position unchanged; new seal"])
with open(f"{P}/07b-market-stall-schedule.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow("stall_id,kit_id,base_asset,canopy,district,position_x,position_y,position_z,rotation_y,footprint_width,footprint_depth,height,customer_side,status".split(","))
    CAN = {"S01b": "blue cloth (material variant)", "S01g": "burgundy cloth (material variant)", "S01c": "cream cloth (material variant)", "S02c": "cream cloth (material variant)", "S02g": "burgundy cloth (material variant)",
           "S03": "striped canopy as shipped (Avramania)", "S04": "open counter, no canopy (Syntaxes of Play)", "S05": "open table with cloth runner (Syntaxes of Play)"}
    for s in L["stalls"]:
        kit = L["stall_kits"][s["kit"]]; base = kit["base"]
        w.writerow([s["id"], s["kit"], base.split("@")[0], CAN[s["kit"]], "D3 Pasar Awan", s["x"], 0.0, -s["n"], s["rz"], kit["rect"][0], kit["rect"][1],
                    {"S03": 2.26, "S04": 1.15, "S05": 0.81}.get(s["kit"], 2.63), FRONT[s["rz"]], "PLANNED - asset-backed blockout rendered in P1.2"])

# ---- inventories -----------------------------------------------------------------------------------
usage = STATS["usage"]
used_base = {}
for aid, n in usage.items():
    if not aid.startswith("CUS-"):
        used_base[aid.split("@")[0]] = used_base.get(aid.split("@")[0], 0) + n


def role(n, pid):
    rules = [("Wall_", "wall module (2 m bay)"), ("Roof_Front", "gable infill"), ("Roof_Tower", "tower roof"), ("Roof_RoundTiles", "prefab gabled roof"), ("Roof_2x4", "small gabled roof (gate lodge)"),
             ("Roof_Dormer", "roof dormer"), ("Roof_Wooden", "timber shopfront canopy"), ("Roof_", "roof component"), ("Corner_", "corner post / pier"), ("DoorFrame", "door frame"), ("Door_", "door leaf"),
             ("WindowShutters", "shutters"), ("Window_", "window insert"), ("Floor_", "floor / paving tile"), ("Stairs_Exterior_Platform", "monument base block"), ("Stairs_Exterior_SingleSide", "podium skirt panel"),
             ("Stair", "stairs"), ("Balcony", "balcony rail"), ("Prop_Chimney", "chimney"), ("Overhang", "jetty / overhang module"), ("Prop_Vine", "wall vine"), ("Stall", "market stall base"), ("Banner", "sign / banner"), ("Lantern", "lantern"),
             ("CommonTree", "tree"), ("TwistedTree", "feature tree"), ("Pine", "tree (not used)"), ("Bush", "shrub"), ("Flower", "flowers"), ("Fern", "ground plant"), ("Rock", "rock")]
    for k, v in rules:
        if n.startswith(k):
            return v
    if pid == "synofplay-medieval-cafe":
        return "cafe / market furniture and goods"
    if pid == "avramania-free-collection":
        return "market goods" if "food_" in n else "village prop" if "village_" in n else "prop (pack not adopted)"
    return {"quaternius-fantasy-props": "merchant / street prop", "quaternius-stylized-nature": "vegetation / ground detail", "quaternius-medieval-village": "architecture detail"}.get(pid, "rejected kit part")


inv_cols = "asset_id,pack,edition,publisher,source_url,license,archive_filename,archive_sha256,internal_filepath,format,dimensions_m,triangle_count,material_status,blender_import_status,proposed_role,modification_required,verification_status".split(",")
with open(f"{P}/03-verified-asset-inventory.csv", "w", newline="") as f, open(f"{P}/asset-evidence/imported-model-register.csv", "w", newline="") as g:
    w = csv.writer(f); w.writerow(inv_cols)
    r2 = csv.writer(g); r2.writerow("asset_id,pack_id,internal_filepath,import_status,width_m,height_m,depth_m,bbox_min_xyz,bbox_max_xyz,triangles,vertices,mesh_objects,materials,textures,textures_loaded,has_uv,has_vertex_color,non_manifold_edges,instances_in_p1_2_blockout".split(","))
    for m in MEAS:
        pid = m["pack_id"]; aid = f"{PFX[pid]}-{m['asset_name']}"; man = MAN[pid]
        used = used_base.get(aid, 0); ok = m["blender_import_status"] == "IMPORTED"
        mat = f"{len(m.get('materials', []))} material(s), {len(m.get('textures', {}))} texture(s), " + ("all loaded" if m.get("textures_loaded") in (True, None) else "TEXTURE MISSING")
        variants = sorted(a.split("@")[1] for a in usage if a.startswith(aid + "@"))
        if pid.startswith("kenney"):
            status, mod = "VERIFIED_DOWNLOADED; VERIFIED_IMPORTED; REJECTED (toy scale 1 unit walls, flat-colour style clashes)", "x3 scale and restyle - not pursued"
        elif pid.startswith("kaykit"):
            status, mod = "VERIFIED_DOWNLOADED; VERIFIED_IMPORTED; REJECTED (city-builder miniatures: whole buildings about 1 m tall)", "none - not usable at player scale"
        elif pid.startswith("polypizza"):
            status, mod = "VERIFIED_DOWNLOADED; VERIFIED_IMPORTED; REJECTED (" + ("miniature scale and flat-colour style" if "market" in pid else "modern sign, wrong period") + ")", "not pursued"
        elif pid.startswith("avramania") and any(k in m["internal_filepath"] for k in AV_AI) and not used:
            status, mod = "VERIFIED_DOWNLOADED; VERIFIED_IMPORTED; NOT ADOPTED (pack ReadMe: some models began as AI-generated meshes, not identified individually; project rule excludes AI-generated assets)", "none"
        elif used:
            status = "VERIFIED_DOWNLOADED; VERIFIED_IMPORTED; ASSEMBLED_IN_P1.2_BLOCKOUT" + ("; RECOMPOSITION_REQUIRED" if m["asset_name"].startswith(("Wall_", "Roof_", "Corner_", "Stairs_", "Floor_", "Balcony")) else "")
            mod = ("material variant(s): " + ", ".join(variants)) if variants else "geometry from the FBX; materials taken by name from the pack's own all-merged.blend (FBX texture paths do not resolve)" if pid.startswith("synofplay") else "height stretched 1.3x / 1.6x for lamp posts and lane standards" if m["asset_name"] == "Corner_Exterior_Wood" else "none (instanced as authored)"
        else:
            status, mod = ("VERIFIED_DOWNLOADED; VERIFIED_IMPORTED" if ok else "VERIFIED_DOWNLOADED; IMPORT_FAILED"), "UNKNOWN (not assembled)"
        dm = m.get("dimensions_m", ["UNKNOWN"] * 3)
        w.writerow([aid, m["pack"], m["edition"], m["publisher"], SRC[pid], "CC0-1.0", ZIPNAME.get(pid, man["archive_filename"]), man["sha256"], m["internal_filepath"], m["format"],
                    "x".join(str(v) for v in dm), m.get("triangle_count", "UNKNOWN"), mat, m["blender_import_status"], role(m["asset_name"], pid), mod, status])
        r2.writerow([aid, pid, m["internal_filepath"], m["blender_import_status"], *dm, m.get("bbox_min_xyz_gltf"), m.get("bbox_max_xyz_gltf"), m.get("triangle_count"), m.get("vertex_count"),
                     m.get("mesh_objects"), ";".join(m.get("materials", [])), ";".join(f"{k}:{v[0]}x{v[1]}" for k, v in m.get("textures", {}).items()), m.get("textures_loaded"),
                     m.get("has_uv"), m.get("has_vertex_color"), m.get("non_manifold_edges"), used])
GRADE = {"MI_RoundTiles": "roof tiles: hue +0.012, saturation x0.90, value x0.94 (towards #BB6345)", "MI_WoodTrim / MI_WoodTrim_Wear": "timber: saturation x0.82, value x0.76 (towards #75543B)",
         "MI_Plaster": "plaster: saturation x0.80, value x1.14 (towards #E8D9BC)", "MI_UnevenBrick": "stone walls: saturation x0.50 (towards #858078)", "MI_Brick": "paving: saturation x0.70, value x1.10 (towards #A69E8E)",
         "MI_RockTrim / MI_RedBrick / MI_Trim_Furniture": "minor saturation and value trims", "Leaves_NormalTree / Leaves / Flowers": "foliage: saturation x0.70-0.85, value x0.90-1.0 (muted natural green)"}
with open(f"{P}/03b-custom-and-variant-register.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow("item_id,class,based_on_downloaded_asset,what_is_changed,triangles_each,instances_in_p1_2_blockout,where_used,is_downloaded_geometry,p2_action".split(","))
    for aid in sorted(usage):
        if aid.startswith("CUS-Seal"):
            w.writerow([aid, "CUSTOM GEOMETRY (authored in P1.2, procedural, citadel_lib.make_seal)", "none", "original guild seal: gold rim, burgundy field, two crossing trade routes with a way-station disc at each end, gold diamond with a blue heart; 1.0 m, scaled 0.8-1.9. Replaces the P1.1 compass-star seal.",
                        STATS["tris_each"][aid], usage[aid], "Exchange Hall porch gable and tower, market hall gables, gateway lodges, warehouse gable, market cross", "NO", "rebuild as one authored mesh or a textured disc; owner to approve the design"])
        elif aid.startswith("CUS-Sign"):
            _, glyph, field = aid.split("_")
            w.writerow([aid, "CUSTOM GEOMETRY (authored in P1.2, procedural, citadel_lib.make_sign)", "none", f"hanging trade sign: iron arm, timber board, {field} field, '{glyph}' pictogram on both faces; board 0.50 x 0.40 m, placed at scale 1.4",
                        STATS["tris_each"][aid], usage[aid], "one per shop, workshop and guild office (burgundy field = guild-run)", "NO", "author one sign mesh with a pictogram atlas; owner to approve the pictograms"])
        elif "@" in aid:
            base, v = aid.split("@")
            what = ("civic roof tile value: extra hue +0.004, saturation x0.84, value x0.72 on the graded MI_RoundTiles material (towards #9F523D)" if v == "dark"
                    else f"cloth colour {dict(burgundy='#8C3E45', blue='#345D80', gold='#C8A15A', cream='#E6D8B8')[v]}: the vertex-colour mix of the downloaded MI_Banner material is replaced by texture x colour")
            where = ("Exchange Hall, market halls, warehouse, gate lodges" if v == "dark" else {"burgundy": "guild: Exchange Hall banners, east market hall, crafts stalls, warehouse-lane standards", "blue": "market: west market hall banners, provisions stalls",
                                                                                              "gold": "not used in the final scene", "cream": "neutral stalls, artisan-lane standards"}[v])
            w.writerow([aid, "MATERIAL VARIANT (" + ("roof tile value" if v == "dark" else "cloth colour") + ")", base, what, STATS["tris_each"][aid], usage[aid], where, "YES (geometry unchanged)", "recreate as a material instance (material.color) or a recoloured texture"])
    for k, v in GRADE.items():
        w.writerow([f"GRADE {k}", "MATERIAL NORMALISATION (colour grade of downloaded materials, all instances)", "every model using the material", v, "", "all", "whole town", "YES (geometry and UVs unchanged)", "bake the grade into copies of the base-colour textures at export, then verify in Three.js"])
    w.writerow(["MV-Corner_Exterior_Wood (lamp post)", "NON-UNIFORM SCALE of downloaded model", "MV-Corner_Exterior_Wood", "height x1.3 (3.9 m lamp post) and x1.6 (4.8 m lane standard); width unchanged", 12,
                sum(1 for a in L["dressing"] if a[0] == "MV-Corner_Exterior_Wood"), "street lamps, lane standards", "YES (stretched)", "replace with a purpose-made post or accept the stretch"])
    w.writerow(["MV-Window_* on a jetty face", "ASSEMBLY NOTE", "MV-Window_Wide_Round1", "window insert mounted on the plain face of MV-Overhang_Plaster_Short (the overhang module has no window opening)", "", 6, "jettied shophouses A03 (B07, B09, B16)", "YES (as authored)", "check for z-fighting in Three.js; cut an opening or keep surface-mounted"])
    w.writerow(["FP-Vase_2 / FP-Pot_1 (large floor jars)", "UNIFORM SCALE of downloaded model", "FP-Vase_2, FP-Pot_1", "scale x1.3 for two floor-standing jars at the east hall corners", "", 2, "bazaar", "YES (scaled)", "keep or drop"])

# ---- contact sheet of the expansion candidates (real tiles: as authored, beside the adopted Quaternius barrel) ----
EXP = [m for m in MEAS if m["pack_id"] in PFX and PFX[m["pack_id"]] in ("SY", "AV", "KK", "PP")]
adopted = sorted((m for m in EXP if used_base.get(f"{PFX[m['pack_id']]}-{m['asset_name']}", 0)), key=lambda m: (m["pack_id"], m["asset_name"]))
rej_names = {"kaykit-medieval-builder": ("market.gltf", "house.gltf", "castle.gltf"), "avramania-free-collection": ("mdvl_props_basket_01", "mdvl_interiors_pottedplant_01", "mdvl_village_cottage_01")}
rejected = [m for m in EXP if (m["pack_id"].startswith("polypizza") or m["asset_name"] in rej_names.get(m["pack_id"], ())) and m not in adopted]
cells = [(m, "ADOPTED") for m in adopted] + [(m, "REJECTED") for m in rejected]
cols, px = 9, 210
rows_n = (len(cells) + cols - 1) // cols
cs = Image.new("RGB", (cols * px, rows_n * (px + 46) + 78), (244, 243, 238)); d = ImageDraw.Draw(cs)
d.text((14, 10), "Merchant Citadel P1.2 - expansion assets: REAL ASSET RENDERS of downloaded models, as authored, each beside the adopted Quaternius barrel (and a 1.9 m figure for large items)", font=font(19, True), fill=(24, 44, 40))
d.text((14, 40), f"{len(adopted)} adopted models (Syntaxes of Play Medieval Cafe, Avramania Food & Market / Village Builder) and {len(rejected)} representative rejected candidates (KayKit, Poly Pizza, Avramania packs not adopted)", font=font(15), fill=(70, 80, 78))
for i, (m, st) in enumerate(cells):
    x, y = (i % cols) * px, 78 + (i // cols) * (px + 46)
    tile = f"{I}/tiles-expansion/{m['pack_id']}__{m['asset_name']}.png"
    d.rectangle([x + 3, y, x + px - 3, y + px + 42], fill=(226, 232, 226) if st == "ADOPTED" else (238, 222, 218))
    if os.path.exists(tile):
        t = Image.open(tile).convert("RGBA").resize((px - 8, px - 8), Image.LANCZOS); cs.paste(t, (x + 4, y + 2), t)
    dm = m.get("dimensions_m", [0, 0, 0])
    d.text((x + 8, y + px - 4), f"{PFX[m['pack_id']]}-{m['asset_name']}".replace("mdvl_", "")[:27], font=font(12, True), fill=(20, 30, 30))
    d.text((x + 8, y + px + 12), f"{dm[0]:.2f} x {dm[1]:.2f} x {dm[2]:.2f} m, {m.get('triangle_count', 0)} tris", font=font(11), fill=(70, 80, 78))
    d.text((x + 8, y + px + 26), st, font=font(11, True), fill=(30, 110, 60) if st == "ADOPTED" else (160, 50, 40))
cs.save(f"{P}/visuals/expansion-asset-contact-sheet.png", optimize=True)

top = sorted(((usage[a] * STATS["tris_each"][a], a, usage[a], STATS["tris_each"][a]) for a in usage), reverse=True)[:20]
json.dump({"revision": "P1.2", "town": {k: v for k, v in STATS.items() if k not in ("usage", "tris_each", "materials")},
           "top_triangle_contributors": [{"asset_id": a, "instances": n, "triangles_each": e, "triangles": t} for t, a, n, e in top], "archetypes": AREP, "usage": usage},
          open(f"{P}/asset-evidence/usage-and-triangles.json", "w"), indent=1)
shutil.copyfile(f"{I}/validation.json", f"{P}/asset-evidence/spatial-validation-actual-geometry.json")
print("package assets written; top", [(a, n, t) for t, a, n, e in top[:5]])
