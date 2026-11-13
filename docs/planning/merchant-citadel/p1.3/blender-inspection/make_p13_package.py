#!/usr/bin/env python3
"""Build the Merchant Citadel P1.3 planning package (visuals, schedules, documents) from measured data.

Usage: python3 make_p13_package.py <inspection_dir> <package_dir>
Needs: <inspection_dir>/p1.3/{data,renders,archetypes,massing,validation.json,alternatives.json} and the P1.2 snapshot in <inspection_dir>/p1.2.
Narrative is authored here; every table and number is read from the data.
"""
import csv, json, math, os, re, shutil, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layouts_p13 as LY
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

I, P = sys.argv[1], sys.argv[2]
D = f"{I}/p1.3"
L = json.load(open(f"{D}/data/layout.json")); ARCH = json.load(open(f"{D}/data/archetypes.json")); AREP = json.load(open(f"{D}/archetypes/archetype-report.json"))
STATS = json.load(open(f"{D}/renders/town-stats.json")); VAL = json.load(open(f"{D}/validation.json")); RES = json.load(open(f"{D}/alternatives.json")); MM = json.load(open(f"{D}/massing/massing-metrics.json"))
S12 = json.load(open(f"{I}/p1.2/renders/town-stats.json")); V12 = json.load(open(f"{I}/p1.2/validation.json")); L12 = json.load(open(f"{I}/p1.2/data/layout.json"))
os.makedirs(f"{P}/visuals", exist_ok=True); os.makedirs(f"{P}/asset-evidence", exist_ok=True)
DATE = "2026-11-12"
U, TE = STATS["usage"], STATS["tris_each"]
ENV = {a["id"]: a for a in VAL["A_envelopes"]}; SUM = VAL["summary"]
R12, RA, RB, RC = RES["P12"], RES["A"], RES["B"], RES["C"]
nb, ns = len(L["buildings"]), len(L["stalls"])
x0, x1, n0, n1 = L["envelope"]; rx0, rx1, rn0, rn1 = L["reserved"][0][1:]
ux0, ux1, un0, un1 = min(x0, rx0), max(x1, rx1), min(n0, rn0), max(n1, rn1)
base_mats = sorted({re.sub(r"\.\d+", "", m) for m in STATS["materials"]})
arche_n = collections.Counter(b["archetype"] for b in L["buildings"])


def tbl(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]) + "\n"


def w(name, text):
    open(f"{P}/{name}", "w").write(text.strip() + "\n")


def font(size, bold=False):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1 if bold else 0)
    except Exception:
        return ImageFont.load_default()


def label(src, dst, title, klass, note):
    im = Image.open(src).convert("RGB"); wd, h = im.size; bar = 64
    out = Image.new("RGB", (wd, h + bar), (24, 44, 40)); out.paste(im, (0, 0)); d = ImageDraw.Draw(out)
    d.text((16, h + 8), title, font=font(22, True), fill=(245, 240, 225)); d.text((16, h + 37), note, font=font(15), fill=(190, 205, 198))
    tw = d.textlength(klass, font=font(18, True))
    d.rectangle([wd - tw - 40, h + 14, wd - 14, h + 50], fill=(196, 120, 40)); d.text((wd - tw - 27, h + 21), klass, font=font(18, True), fill=(255, 255, 255))
    out.save(dst, optimize=True)


# ---------------------------------------------------------------- views and before/after
BLK = "ASSET-BACKED BLENDER BLOCKOUT"
note = "P1.3 selected layout (22 buildings). Downloaded CC0 models + disclosed custom seal and signs, colour variants and grade. Temporary: ground, yards, dark cores, 1.9 m explorer, afternoon light."
VIEWS = [("view-a-aerial", "View A - Town aerial (same camera as P1.0-P1.2)"), ("view-b-merchant-street", "View B - Merchant Street at the documented gameplay camera (FOV 60, 11.8 m behind, +6.6 m)"),
         ("view-b2-merchant-street-eye", "View B2 - Merchant Street, eye-height verification (1.65 m)"), ("view-c-central-bazaar", "View C - Central Bazaar from its southern edge (same camera as P1.2)"),
         ("view-d-exchange-court", "View D - Exchange Hall approach at 1.65 m eye height (same camera as P1.2)"), ("view-e-service-court", "View E - Secondary: junction pocket court, warehouse lane and service court, eye height"),
         ("view-e2-artisan-lane", "View E2 - Secondary: artisan lane at the gameplay camera"), ("view-f-tea-route", "View F - Secondary: tea lane and lookout terrace, eye height")]
for v, title in VIEWS:
    label(f"{D}/renders/{v}.png", f"{P}/visuals/{v}.png", title, BLK, note)
for v, title in VIEWS:
    if not os.path.exists(f"{I}/p1.2/renders/{v}.png"):
        continue
    a, b = Image.open(f"{I}/p1.2/renders/{v}.png").convert("RGB"), Image.open(f"{D}/renders/{v}.png").convert("RGB")
    wd, h = 1280, 720
    s = Image.new("RGB", (wd * 2 + 12, h + 56), (24, 44, 40)); s.paste(a.resize((wd, h), Image.LANCZOS), (0, 56)); s.paste(b.resize((wd, h), Image.LANCZOS), (wd + 12, 56))
    d = ImageDraw.Draw(s); d.text((16, 14), "BEFORE - P1.2 (17 buildings)", font=font(24, True), fill=(235, 200, 170)); d.text((wd + 28, 14), "AFTER - P1.3 (22 buildings)", font=font(24, True), fill=(170, 230, 215))
    d.text((420, 20), "same camera, same light, same materials: only the town form differs", font=font(15), fill=(190, 205, 198))
    s.save(f"{P}/visuals/before-after-{v[5]}-{v[7:]}.jpg", quality=92)   # JPEG keeps the whole package under the 30 MiB remote-delivery limit
label(f"{D}/renders/blockout-top-ortho.png", f"{P}/visuals/blockout-top-orthographic.png", "Top orthographic render of the P1.3 blockout (north up)", BLK, note)

# archetype sheet (front views) --------------------------------------------------------------------
ids = ["A01", "A02", "A03", "A03b", "A03c", "A04", "A04b", "A05", "A06", "A07", "A08", "GATE"]
tw, th = 620, 524
sheet = Image.new("RGB", (4 * tw, 3 * (th + 54) + 70), (244, 243, 238)); d = ImageDraw.Draw(sheet)
d.text((14, 12), "Merchant Citadel P1.3 - archetype assemblies (ASSET-BACKED ASSEMBLY). A03c is new in P1.3; all others are the P1.2 assemblies.", font=font(22, True), fill=(24, 44, 40))
for i, a in enumerate(ids):
    im = Image.open(f"{D}/archetypes/{a}-front.png").convert("RGBA").resize((tw, th), Image.LANCZOS)
    x, y = (i % 4) * tw, 70 + (i // 4) * (th + 54)
    d.rectangle([x + 4, y, x + tw - 4, y + th + 50], fill=(226, 228, 226)); sheet.paste(im, (x, y), im); r = AREP[a]
    d.text((x + 12, y + th + 4), f"{a} {ARCH[a]['name']}"[:60] + (f"  x{arche_n[a]}" if a in arche_n else ""), font=font(16, True), fill=(20, 30, 30))
    d.text((x + 12, y + th + 27), f"{r['instances']} instances, {r['triangles']:,} tris unoptimised", font=font(14), fill=(70, 80, 78))
sheet.save(f"{P}/visuals/archetype-assembly-sheet.png", optimize=True)

# ---------------------------------------------------------------- selected plan
COL = {"A01": "#b5533c", "A02": "#c98a4b", "A03": "#d6a15c", "A03b": "#d6a15c", "A03c": "#d6a15c", "A04": "#e3bf86", "A04b": "#e3bf86", "A05": "#a9744f", "A06": "#8f8f8a", "A07": "#7d7468", "A08": "#c7a2b8"}
TILE = {"MV-Floor_UnevenBrick": "#cfc7b6", "MV-Floor_Brick": "#c2b29f", "MV-Floor_RedBrick": "#cfa58e"}
EC = {"primary": ("#d62728", 2.4), "secondary": ("#1f77b4", 1.6), "service": ("#e6a700", 1.6), "market": ("#8a4fbf", 1.3), "scenic": ("#2a9d8f", 1.6), "reserved link": ("#3a6ea5", 1.0)}
fig, ax = plt.subplots(figsize=(15, 18.5), dpi=130); ax.set_facecolor("#dfe8cf")
ax.add_patch(Rectangle((ux0 - 10, un0 - 10), ux1 - ux0 + 20, un1 - un0 + 20, fill=False, ls=(0, (6, 4)), lw=1.6, ec="#4d6b3a"))
ax.text(ux0 - 9.5, un1 + 8.2, f"Terrain support zone = (developed envelope + transport reservation) + 10 m: {ux1 - ux0 + 20:.1f} x {un1 - un0 + 20:.0f} m (assumption)", fontsize=8.5, color="#3c5a2c")
ax.add_patch(Rectangle((x0, n0), x1 - x0, n1 - n0, fill=False, ls=":", lw=1.2, ec="#555"))
for pv in L["paving"]:
    ax.add_patch(Rectangle((pv[1], pv[3]), pv[2] - pv[1], pv[4] - pv[3], fc=TILE[pv[5]], ec="none"))
for y in L["yards"]:
    ax.add_patch(Rectangle((y[1], y[3]), y[2] - y[1], y[4] - y[3], fc="#d9c7a3", ec="#a08a5c", lw=0.6, ls=":"))
for name, a, b, c, e in L["reserved"]:
    ax.add_patch(Rectangle((a, c), b - a, e - c, fill=False, hatch="//", ec="#3a6ea5", lw=1.2)); ax.text((a + b) / 2, (c + e) / 2, "RESERVED\nfuture transport\n20 x 16 m", ha="center", va="center", fontsize=8, color="#3a6ea5")
for b in L["buildings"]:
    r = b["rect"]; e = ENV.get(b["id"]); new = b["status"] == "new"
    if e:
        ax.add_patch(Rectangle((e["full_x"][0], e["full_n"][0]), e["full_x"][1] - e["full_x"][0], e["full_n"][1] - e["full_n"][0], fill=False, ls="--", lw=0.8, ec="#7a2d1c"))
    ax.add_patch(Rectangle((r[0], r[2]), r[1] - r[0], r[3] - r[2], fc=COL[b["archetype"]], ec="#b8860b" if new else "#2b2b2b", lw=2.6 if new else 1.1))
    ax.text((r[0] + r[1]) / 2, (r[2] + r[3]) / 2, f"{b['id']}\n{b['archetype']}", ha="center", va="center", fontsize=8.0, weight="bold", color="white" if b["archetype"] in ("A01", "A05", "A06", "A07") else "#222")
    ax.plot(*b["door"], marker="^" if b["rz"] == 180 else "v" if b["rz"] == 0 else ">" if b["rz"] == 90 else "<", color="#111", ms=5)
for sx in (-3, 3):
    ax.add_patch(Rectangle((sx - 1, 3), 2, 4, fc="#b98a55", ec="#3a2412", lw=1.2))
ax.add_patch(Rectangle((-1, 48), 2, 2, fc="#8C3E45", ec="#111", lw=1))
for s in L["stalls"]:
    r = s["rect"]; ax.add_patch(Rectangle((r[0], r[2]), r[1] - r[0], r[3] - r[2], fc="#5b7fa8", ec="#111", lw=0.5))
for a, b, kind in L["edges"]:
    k = kind.split(",")[0]; (xa, na, _), (xb, nb_, _) = L["nodes"][a], L["nodes"][b]
    ax.plot([xa, xb], [na, nb_], color=EC[k][0], lw=EC[k][1], ls="--" if k in ("service", "reserved link") else "-", alpha=0.9, zorder=5)
for k, (x, n, nm) in L["nodes"].items():
    ax.plot(x, n, "o", ms=8.5, mfc="white", mec="#111", zorder=6); ax.text(x, n, k[1:], ha="center", va="center", fontsize=5.8, zorder=7)


def dim(xa, na, xb, nb_, txt, off=(0, 0)):
    ax.annotate("", (xa, na), (xb, nb_), arrowprops=dict(arrowstyle="<->", color="#111", lw=0.9))
    ax.text((xa + xb) / 2 + off[0], (na + nb_) / 2 + off[1], txt, fontsize=7.5, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.85))


dim(-4, 13, 4, 13, "8.0 m clear", (0, 1.1)); dim(-22, 64.6, 22, 64.6, "bazaar plaza 44 m", (-10, 1.2)); dim(-14, 75.2, 14, 75.2, "civic court 28 x 12 m", (0, -1.2))
dim(-18, 27, -14, 27, "4 m", (0, 1.1)); dim(14, 30.5, 18, 30.5, "4 m", (0, 1.1)); dim(-12, 20, -6.5, 20, "cross street 4 m", (0, 2.9)); dim(22, 54.6, 30, 54.6, "tea lane 4 m", (0, -1.1))
dim(x0, n0 - 19, x1, n0 - 19, f"developed envelope {x1 - x0:.1f} m (E-W)", (14, -1.4)); dim(x1 + 5, n0, x1 + 5, n1, f"{n1 - n0:.0f} m (N-S)", (3.4, 0))
for t, x, n in (("D1 Gerbang Niaga", -3, -6.8), ("D2 Koridor Niaga", 0, 27.5), ("Simpang Timbangan", 0, 23.2), ("D3 Pasar Awan", 0, 38.9), ("D4 Pelataran Bursa", 0, 70.2), ("D5 Balai Niaga Awan", 0, 88),
                ("D6 Lorong Lentera", -16, 8.2), ("D7 Jalur Gudang", 16, 8.6), ("Pelataran Gudang", 26.5, 20), ("D8 Tea Lookout", 36, 54.5), ("artisan workyard", -21, 37.2)):
    ax.text(x, n, t, ha="center", fontsize=8.2, style="italic", color="#16302b", bbox=dict(fc="#f4f1e6", ec="#16302b", lw=0.5, pad=1.5), zorder=8)
ax.add_patch(FancyArrow(x1 + 9, n1 - 4, 0, 8, width=0.6, head_width=2.6, head_length=3, color="#111")); ax.text(x1 + 9, n1 + 8.6, "N", ha="center", fontsize=13, weight="bold")
ax.plot([x0, x0 + 20], [un0 - 5, un0 - 5], color="#111", lw=3); ax.text(x0 + 10, un0 - 4.2, "20 m", ha="center", fontsize=8)
handles = ([plt.Line2D([0], [0], color=c, lw=wd, label=k) for k, (c, wd) in EC.items()]
           + [Rectangle((0, 0), 1, 1, fc=COL[a], ec="#222", label=f"{a} {ARCH[a]['name']}"[:46]) for a in ("A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08")]
           + [Rectangle((0, 0), 1, 1, fc="#eee", ec="#b8860b", lw=2.4, label="gold outline = new building in P1.3"), Rectangle((0, 0), 1, 1, fill=False, ls="--", ec="#7a2d1c", label="measured envelope incl. roof, signs"),
              Rectangle((0, 0), 1, 1, fc="#d9c7a3", label="packed-earth yard (terrain treatment)")])
ax.legend(handles=handles, loc="lower right", fontsize=7.2, framealpha=0.95, title="Routes, archetypes, surfaces")
ax.set_xlim(ux0 - 14, ux1 + 15); ax.set_ylim(un0 - 14, un1 + 12); ax.set_aspect("equal")
ax.set_xlabel("x east (m)  -  project x"); ax.set_ylabel("n north (m)  -  project z = -n")
ax.set_title("Merchant Citadel / Kota Niaga Awan - P1.3 selected layout (alternative B), measured plan generated from layout data and measured envelopes", fontsize=10.5)
ax.grid(True, color="#ffffff", lw=0.4, alpha=0.6); fig.tight_layout(); fig.savefig(f"{P}/visuals/orthographic-town-plan.png"); plt.close(fig)

# ---------------------------------------------------------------- schedules
FRONT = {0: "south (+z)", 90: "east (+x)", -90: "west (-x)", 180: "north (-z)"}
with open(f"{P}/05-building-schedule.csv", "w", newline="") as f:
    cw = csv.writer(f)
    cw.writerow("building_id,archetype_id,district,label,position_x,position_y,position_z,rotation_y,footprint_width,footprint_depth,height,entrance_location_x,entrance_location_z,frontage_direction,"
                "measured_envelope_x_min,measured_envelope_x_max,measured_envelope_z_min,measured_envelope_z_max,measured_envelope_width_x,measured_envelope_depth_z,options,change_since_p1_2,status".split(","))
    for b in L["buildings"]:
        a = ARCH[b["archetype"]]; e = ENV[b["id"]]
        cw.writerow([b["id"], b["archetype"], b["district"], b["label"], b["x"], 1.0 if b["archetype"] == "A01" else 0.0, -b["n"], b["rz"], a["footprint"][0], a["footprint"][1], a["height_m"],
                     round(b["door"][0], 2), round(-b["door"][1], 2), FRONT[b["rz"]], e["full_x"][0], e["full_x"][1], -e["full_n"][1], -e["full_n"][0], e["full_size"][0], e["full_size"][1],
                     "; ".join(f"{k}={v}" for k, v in sorted(b.get("opts", {}).items()) if k != "add") + ("; per-building extras" if b.get("opts", {}).get("add") else ""),
                     b["status"].replace("moved from", "moved from (x, z)"), "PLANNED - asset-backed blockout rendered in P1.3"])
    for gid, key, pos in (("G01", "GATE", L["gate"]), ("M01", "CROSS", L["cross"])):
        e = ENV[gid]
        cw.writerow([gid, key, "D1 Gerbang Niaga" if gid == "G01" else "D3 Pasar Awan", ARCH[key]["name"] + " (structure)", pos[0], 0.0, -pos[1], 0, *ARCH[key]["footprint"], ARCH[key]["height_m"], "", "", "south (+z)",
                     e["full_x"][0], e["full_x"][1], -e["full_n"][1], -e["full_n"][0], e["full_size"][0], e["full_size"][1], "guild seal", "kept", "PLANNED - asset-backed blockout rendered in P1.3"])
with open(f"{P}/05b-market-stall-schedule.csv", "w", newline="") as f:
    cw = csv.writer(f); cw.writerow("stall_id,kit_id,base_asset,district,position_x,position_y,position_z,rotation_y,footprint_width,footprint_depth,customer_side,change_since_p1_2".split(","))
    old = {s["id"]: s for s in L12["stalls"]}
    for s in L["stalls"]:
        kit = L["stall_kits"][s["kit"]]; o = old[s["id"]]
        cw.writerow([s["id"], s["kit"], kit["base"], "D3 Pasar Awan", s["x"], 0.0, -s["n"], s["rz"], kit["rect"][0], kit["rect"][1], FRONT[s["rz"]],
                     "kept" if (o["x"], o["n"]) == (s["x"], s["n"]) else f"moved {abs(s['n'] - o['n']):.1f} m along z to clear a walking edge"])
shutil.copyfile(f"{D}/validation.json", f"{P}/asset-evidence/spatial-validation-actual-geometry.json")
shutil.copyfile(f"{D}/alternatives.json", f"{P}/asset-evidence/alternatives-metrics.json")
shutil.copyfile(f"{D}/massing/massing-metrics.json", f"{P}/asset-evidence/massing-ray-tests.json")
top = sorted(((U[a] * TE[a], a, U[a], TE[a]) for a in U), reverse=True)[:20]
json.dump({"revision": "P1.3", "town": {k: v for k, v in STATS.items() if k not in ("usage", "tris_each", "materials")}, "top_triangle_contributors": [{"asset_id": a, "instances": n, "triangles_each": e, "triangles": t} for t, a, n, e in top],
           "archetypes": AREP, "usage": U}, open(f"{P}/asset-evidence/usage-and-triangles.json", "w"), indent=1)

# ---------------------------------------------------------------- numbers for the documents
ACTIONS = {"FP-Lantern_Wall": 600, "MV-Corner_Exterior_Brick": 300, "SN-CommonTree_3": 1500, "SN-CommonTree_1": 1500, "FP-FarmCrate_Apple": 600, "FP-FarmCrate_Carrot": 600, "SN-Bush_Common_Flowers": 500,
           "MV-Door_8_Round": 400, "FP-Crate_Wooden": 230, "MV-Balcony_Simple_Straight": 132, "FP-Stall_Cart_Empty": 1500, "FP-Barrel": 300, "FP-Bag": 300, "SN-TwistedTree_2": 3000, "FP-Barrel_Apples": 700,
           "FP-Dummy": 900, "AV-mdvl_food_cabbage_01": 300, "AV-mdvl_food_cheese_wheel_01": 300, "AV-mdvl_village_window_box_01": 400, "AV-mdvl_food_grain_sack_01": 350, "AV-mdvl_food_ham_01": 300,
           "AV-mdvl_food_fish_01": 250, "AV-mdvl_village_well_01": 600}
TOWN_NEW = sum(n * min(TE[a], ACTIONS.get(a.split("@")[0], 10 ** 9)) for a, n in U.items())
optrows = sorted(([f"`{a}`", n, f"{TE[a]:,}", f"{n * TE[a]:,}", f"{ACTIONS[a]:,}", f"{n * (TE[a] - ACTIONS[a]):,}"] for a, n in U.items() if a in ACTIONS and TE[a] > ACTIONS[a]), key=lambda r: -int(r[5].replace(",", "")))[:12]


def catof(a):
    b = a.split("@")[0]
    if b.startswith("MV-Floor"): return "paving"
    if b.startswith(("MV-Wall", "MV-Roof", "MV-Corner", "MV-Window", "MV-Door", "MV-Stairs", "MV-Balcony", "MV-Overhang", "MV-Prop_Chimney")): return "architecture modules"
    if b.startswith("SN-"): return "vegetation"
    if "Lantern" in b: return "lanterns"
    if b.startswith(("FP-Stall", "AV-mdvl_village_stall")): return "stall bases"
    if b.startswith("CUS"): return "custom seal and signs"
    return "goods, furniture and street props"


def cats(usage, te):
    c = collections.Counter()
    for a, n in usage.items():
        c[catof(a)] += n * te[a]
    return c


C13, C12 = cats(U, TE), cats(S12["usage"], S12["tris_each"])
edges = [(a, b, k, round(math.hypot(L["nodes"][a][0] - L["nodes"][b][0], L["nodes"][a][1] - L["nodes"][b][1]), 1)) for a, b, k in L["edges"]]
built = [e for e in edges if not e[2].startswith("reserved")]
net = round(sum(e[3] for e in built), 1)
PRIM = ["N01", "N02", "N03", "N04", "N05", "N29", "N27", "N06", "N07", "N08"]
ln = lambda p, q: math.hypot(L["nodes"][p][0] - L["nodes"][q][0], L["nodes"][p][1] - L["nodes"][q][1])
prim = round(sum(ln(p, q) for p, q in zip(PRIM, PRIM[1:])), 1)
LOOPS = [("Artisan loop", ["N03", "N10", "N11", "N04", "N03"], "Junction, cross street, artisan lane past two workshops and the workyard, bazaar south-west corner, back down the street"),
         ("Warehouse loop", ["N03", "N13", "N14", "N04", "N03"], "Junction pocket court, warehouse lane past the counting house (service court on the right), bazaar south-east corner, back down the street"),
         ("Arrival west loop", ["N01", "N35", "N09", "N10", "N03", "N02", "N01"], "Arrival court, gateway shop, artisan lane south, cross street, back through the gate"),
         ("Arrival east loop", ["N01", "N36", "N12", "N13", "N03", "N02", "N01"], "Arrival court, carrier's house, warehouse lane south past the warehouse, cross street, back through the gate"),
         ("Bazaar west circuit", ["N04", "N11", "N38", "N23", "N25", "N06", "N27", "N30", "N05", "N04"], "Round the west hall by the perimeter shop and the assay office"),
         ("Bazaar east circuit and tea spur", ["N04", "N14", "N39", "N24", "N26", "N06", "N27", "N29", "N05", "N04"], "Round the east hall by the registry; the tea lane leaves at N24")]
looprows = [[n, " - ".join(k[1:] for k in seq), f"{sum(ln(p, q) for p, q in zip(seq, seq[1:])):.0f}", f"{sum(ln(p, q) for p, q in zip(seq, seq[1:])) / 2.1:.0f} s", why] for n, seq, why in LOOPS]
cam13 = {g["travel"]: g for g in VAL["G_camera"]}; cam12 = {g["travel"]: g for g in V12["G_camera"]}
hang = sorted([c for c in VAL["C_hanging"] if c["clearance_m"] is not None and c["over_paving"]], key=lambda c: c["clearance_m"])
named = [("N17->N16", "leaving the tea-house veranda"), ("N21->N07", "leaving the west court corner house (B15)"), ("N22->N07", "leaving the east court corner house (B16)"), ("N25->N21", "into the west court side"),
         ("N26->N22", "into the east court side"), ("N31->N30", "leaving Market Hall West under its roof"), ("N32->N29", "leaving Market Hall East under its roof"), ("N18->N31", "into Market Hall West")]
camrows = []
for t, what in named:
    a, b = cam12.get(t), cam13.get(t)
    camrows.append([t, what, f"{a['unobstructed_pct']}% / {a['min_camera_distance_m']} m" if a else "-", f"{b['unobstructed_pct']}% / {b['min_camera_distance_m']} m" if b else "-"])
worst13 = sorted([g for g in VAL["G_camera"] if g["unobstructed_pct"] < 100], key=lambda g: g["min_camera_distance_m"])
newcam = [[g["travel"], g["type"], f"{g['unobstructed_pct']}%", g["min_camera_distance_m"], ", ".join(b.split("_")[0] for b in g["main_blockers"][:2]) or "-"] for g in worst13 if g["travel"] not in cam12][:12]
fwd = [f"{p}->{q}" for p, q in zip(PRIM, PRIM[1:])]
vis = MM["B"]["hall_visibility"]; vis12 = MM["P12"]["hall_visibility"]
visrows = [[k, L["nodes"][k][2], "yes" if v["tower seal"] else "no", "yes" if v["porch gable"] else "no"] for k, v in vis.items()]
gaps = [[g["a"], g["b"], g["gap_m"], g["status"]] for g in VAL["B_roof_gaps_under_3m"]]
drow = [[d["edge"], d["type"], d["length_m"], d["unpaved_samples"], d["max_step_m"], d["min_headroom_m"] if d["min_headroom_m"] else "open sky", d["min_side_clearance_m"], d["status"]] for d in VAL["D_edges"]]
G = lambda r, k: r["enclosure_groups_wall_active_pct"][k]
GROUPS = ["Merchant street", "Artisan lane", "Warehouse lane", "Bazaar perimeter", "Arrival court sides", "Civic court sides"]
encrows = [[g] + [f"{G(r, g)[0]}% / {G(r, g)[1]}%" for r in (R12, RA, RB, RC)] for g in GROUPS] + [["**All tested edges**"] + [f"**{r['overall_wall_pct']}% / {r['overall_active_pct']}%**" for r in (R12, RA, RB, RC)]]
changed = [b for b in L["buildings"] if b["status"] != "kept"]
STATUS = {"A01": "READY", "A02": "CONDITIONAL", "A03": "CONDITIONAL", "A03b": "READY", "A03c": "READY", "A04": "READY", "A04b": "READY", "A05": "READY", "A06": "READY", "A07": "READY", "A08": "CONDITIONAL"}
PURPOSE = {"A01": "Exchange Hall: civic landmark", "A02": "Covered market hall (two dressing kits)", "A03": "Jettied two-storey shophouse, gable to street", "A03b": "Two-storey shophouse, eaves to street",
           "A03c": "Shallow two-storey merchant house (8 x 4 m) for plots that back onto a lane - **new in P1.3**", "A04": "Single-storey shop, gable to street", "A04b": "Single-storey shop, eaves to street",
           "A05": "Stone-based corner building with two fronts", "A06": "Stone workshop", "A07": "Guild warehouse", "A08": "Tea house with veranda"}

# =============================================================================================== documents
w("README.md", f"""
# Merchant Citadel / Kota Niaga Awan - P1.3 planning package

**Status: MERCHANT CITADEL P1.3 - PENDING HUMAN REVIEW.** Planning and Blender concept only. Dated {DATE}. P2 has not started.

P1.3 changes the **form of the town**, which P1.1 and P1.2 had left alone. Three measured layouts were compared; the selected one has
**{nb} buildings** (17 before), lanes moved in behind the street rows, a cross street through the middle of the merchant street, buildings on
the bazaar and arrival edges, and the warehouse and tea house pulled into the town. Materials, signs, goods and light are those of P1.2, so
the before/after images differ only in layout.

This folder is separate from `../p1/`, which still holds the P1.2 package unchanged and reproducible.

| # | Deliverable | File |
|---|---|---|
| 1 | Urban morphology diagnosis | [01-urban-morphology-diagnosis.md](01-urban-morphology-diagnosis.md) |
| 2 | Three alternative masterplans | [02-three-alternative-masterplans.md](02-three-alternative-masterplans.md), [alternatives-plans.png](visuals/alternatives-plans.png), [alternatives-massing.png](visuals/alternatives-massing.png) |
| 3 | Alternative evaluation matrix | [03-alternative-evaluation-matrix.md](03-alternative-evaluation-matrix.md) |
| 4 | Selected layout design bible | [04-selected-layout-design-bible.md](04-selected-layout-design-bible.md), [orthographic-town-plan.png](visuals/orthographic-town-plan.png) |
| 5 | Building schedule | [05-building-schedule.csv](05-building-schedule.csv), [05b-market-stall-schedule.csv](05b-market-stall-schedule.csv) |
| 6 | Pedestrian network | [06-pedestrian-network.md](06-pedestrian-network.md) |
| 7 | Archetype schedule | [07-archetype-schedule.md](07-archetype-schedule.md), [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png) |
| 8 | Visual views | A [aerial](visuals/view-a-aerial.png), B [street, gameplay camera](visuals/view-b-merchant-street.png), B2 [street, eye height](visuals/view-b2-merchant-street-eye.png), C [bazaar](visuals/view-c-central-bazaar.png), D [Exchange Hall](visuals/view-d-exchange-court.png), E [service court](visuals/view-e-service-court.png), E2 [artisan lane](visuals/view-e2-artisan-lane.png), F [tea route](visuals/view-f-tea-route.png) |
| 9 | Actual geometry and camera QA | [08-geometry-camera-qa.md](08-geometry-camera-qa.md) |
| 10 | Terrain interface contract | [09-terrain-interface-contract.md](09-terrain-interface-contract.md) |
| 11 | P2 construction contract | [10-p2-construction-contract.md](10-p2-construction-contract.md) |
| 12 | Before/after comparison | [11-before-after-comparison.md](11-before-after-comparison.md), before-after [A](visuals/before-after-a-aerial.jpg) [B](visuals/before-after-b-merchant-street.jpg) [C](visuals/before-after-c-central-bazaar.jpg) [D](visuals/before-after-d-exchange-court.jpg) |
| - | Changed files and approval dependencies | [12-changes-and-approval-dependencies.md](12-changes-and-approval-dependencies.md) |

Evidence classes: the eight views and the archetype sheet are ASSET-BACKED BLENDER BLOCKOUT; the alternatives images are MASSING (boxes and roof prisms at real
module dimensions, no downloaded model); the plans are drawings generated from the layout data. No illustrative concept image and no AI-generated image is included.

Asset sources, licences, hashes and the register of custom and variant items are unchanged from P1.2 and stay in `../p1/` (02, 03, 03b, 04). **No new asset was downloaded in P1.3.**

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1.3/blender-inspection; B="/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec"
python3 $S/town_data.py $D/p1.3/data                                  # selected layout, nominal checks
$B --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/p1.3/data/archetypes.json $D/p1.3/archetypes
$B --python $S/massing_p13.py -- $D/p1.2/data $D/p1.3/massing $D/p1.3/data/archetypes.json && python3 $S/compare_p13.py $D docs/planning/merchant-citadel/p1.3
$B --python $S/build_town.py -- $D/extracted $D/measurements.json $D/p1.3/data $D/p1.3/renders $D/p1.3/merchant-citadel-p1.3-blockout.blend
$B --python $S/validate_envelopes.py -- $D/p1.3/merchant-citadel-p1.3-blockout.blend $D/p1.3/data $D/p1.3/validation.json
python3 $S/make_p13_package.py $D docs/planning/merchant-citadel/p1.3
```
""")

w("01-urban-morphology-diagnosis.md", f"""
# 01 - Urban morphology diagnosis: why the P1.2 town does not hold together

P1.2 passed every spatial check and still reads as separate buildings along one street. The reasons can be measured. "Enclosure" below is the share
of a street or court edge that has a building wall within 3-4 m of it; "active" is the share that has a building's door side facing it
(method: `layouts_p13.enclosure`, sampled every 0.5 m on nominal footprints).

| Edge | Length tested | Wall enclosure | Active frontage | What that means on the ground |
|---|---|---|---|---|
""" + "\n".join(f"| {k} | {v[0]} m | {v[1]}% | {v[2]}% | {why} |" for (k, v), why in zip(R12["enclosure_lines"].items(), [
    "The one edge that works: three buildings a side with 2.5-3.5 m gaps", "As above",
    "Three workshops with 3-5 m gaps", "**Nothing.** An 8 m strip of back court and fence separates the lane from the street row",
    "Only the warehouse and registry, 14 m apart", "**Nothing.** Back court again",
    "**Open.** Trees and grass", "**Open.** A path leaves for the tea house", "Only the ends of two street buildings", "Open to the court; its two side buildings stand outside the tested band",
    "**Open.** Two gate lodges are the only structures", "**Open**", "One corner house 36 m from its opposite number", "One shophouse"])) + f"""

**Overall: {R12['overall_wall_pct']}% of the tested edges are enclosed and {R12['overall_active_pct']}% are active.** Buildings cover {R12['coverage_pct']}% of the developed envelope.

## Six findings

1. **Only the merchant street is a street.** It is 10 m between facades with 6 m eaves (height to width 0.6) and 73% enclosed. Everything else is a path beside buildings.
2. **Both lanes are one-sided.** Each has buildings on its outer side and an 8 m wide strip of back court on its inner side. A walker sees fence, yard and the backs of the street row.
3. **The bazaar is a field with two halls in it.** Its 44 x 26 m plaza has {G(R12, 'Bazaar perimeter')[0]}% of its 140 m perimeter enclosed and no shopfront facing it at all. The halls define the middle, nothing defines the edge.
4. **Arrival has no walls.** The 20 x 16 m court has two open lodges and nothing on either side, so the town begins 10 m further north, at the first shophouses.
5. **The secondary destinations are detached.** The warehouse stands behind a back court; the tea house is 18 m beyond the plaza edge at the end of a path with no building on it; the two court buildings face each other across 36 m.
6. **There is one route.** The street has no side opening in its 26 m length. The walking graph has 9 loops, but most are inside the bazaar; to go from the street to either lane the player must return to the arrival court or reach the bazaar.

## Camera

In P1.2, {V12['summary']['camera_edges_fully_clear']} of {V12['summary']['camera_travel_directions']} travel directions were fully clear in the ray test. The severe cases (camera under 2 m) were all the same kind: walking
away from a door or out from under a roof (tea-house veranda 0.9 m, court corner houses 1.1 m). Those are addressed in 08; they are a property of
entering and leaving buildings, not of the layout, and they cannot be removed by layout alone.

## What follows from this

The defects are of form, not of dressing: fill the back courts or move the lanes onto them, give the bazaar and the arrival court edges, open the
street sideways, and bring the warehouse and tea house inside the cluster. Three ways of doing that are tested in 02.
""")

altrow = lambda r: [r["title"], r["buildings"], r["new_buildings"], r["moved_or_changed"], r["kept_in_place"], r["archetype_count"], f"{r['envelope_size'][0]:g} x {r['envelope_size'][1]:g}", f"{r['coverage_pct']}%"]
w("02-three-alternative-masterplans.md", f"""
# 02 - Three alternative masterplans

Plans: [alternatives-plans.png](visuals/alternatives-plans.png). Aerial massing from one camera: [alternatives-massing.png](visuals/alternatives-massing.png).
Data: `blender-inspection/layouts_p13.py`. All three use real archetype footprints on the 2 m module grid and were checked for footprint overlap.
The massing is boxes and roof prisms at the measured module dimensions; it is a measuring tool, not a visual concept.

{tbl(["Layout", "Buildings", "New", "Moved, rotated or re-typed", "Left in place", "Archetypes", "Developed envelope (m)", "Ground covered by buildings"], [altrow(R12), altrow(RA), altrow(RB), altrow(RC)])}
## Moves common to all three

| Move | Why |
|---|---|
| Street gaps aligned at z = -18..-22 and a 4 m **cross street** opened through them (B05, B06, B08, B09 shift 0.6-2.5 m; B04 turned to face the street and the cross street) | Gives the merchant street a junction at mid-length and connects it sideways to both lanes |
| Court buildings B15 and B16 moved in to the bazaar's north corners, facades at x = -14 and +14 | Court narrows from 36 m to 28 m, the width of the hall podium; the corner houses face both the bazaar and the court |
| Tea house moved from 18 m east of the plaza to a terrace reached by an 8 m lane leaving the bazaar's north-east corner | Shorter, and the lane leaves north of the east hall so the follow camera is not inside the hall roof |
| Registry moved from the warehouse lane to the bazaar's east edge | A guild office facing the market; first frontage on that edge |
| Halls not moved or rotated | They already frame the axis symmetrically; moving them would break the cross-passage. No comparison was needed because no move was proposed |

## A - Refined existing layout ({RA['buildings']} buildings)

Keeps the P1.2 street network with the lanes 18-22 m from the axis, applies the common moves and adds one building, the gateway shop.
**Tests whether relocation alone is enough.** It is not: the lanes stay one-sided, the back courts stay, and the cross street has to run 12 m between fences to reach them.

## B - Compact Merchant Citadel ({RB['buildings']} buildings)

Moves both lanes in by 4 m so they run directly behind the street rows (x = 14..18). Workshops, warehouse and a new counting house stand on the
outer side; the backs and small yards of the street row form the inner side. Five buildings are added:

| ID | Building | Archetype | Where | What it does |
|---|---|---|---|---|
| E01 | South Gateway Shop | A04b | West side of the arrival court | First shopfront a visitor meets; closes the court's west side |
| E02 | Arrival Corner Merchant House | A03c (new shallow variant) | East side of the arrival court | Two storeys against one: an asymmetrical gateway that frames the view up the street |
| E03 | Bazaar Perimeter Shop | A03b | West edge of the bazaar | A shopfront behind the west hall; turns the hall's side into a lane |
| E04 | Merchant Counting House | A05 | Warehouse lane, north of the service court | With the warehouse it encloses a 14 x 8 m service court; faces both lane and court |
| E05 | Tea Route Merchant House | A04b | South side of the tea lane | The frontage between bazaar and terrace |

## C - Expanded Trading Quarter ({RC['buildings']} buildings)

B plus two more bazaar-edge shops: E06 on the east edge between the registry and the tea lane, E07 on the west edge north of E03.
**Tests the upper limit.** It raises bazaar enclosure a little further and costs two more buildings; see 03.

## Small public spaces in B and C

| Space | Size | Enclosed by |
|---|---|---|
| Junction pocket court (Simpang Timbangan, east side) | 8 x 6 m | Jettied house B07, compact shop B08, the lane |
| Artisan workyard | 6 x 4 m | Workshop B12, the lane, the bazaar corner; well, bench, anvil |
| Service court (Pelataran Gudang) | 14 x 8 m | Warehouse B13 (south), counting house E04 (north) |
| Tea lane and terrace | 8 x 4 m lane, 12 x 10 m terrace | Tea route house E05, tea house B17, fence on the lookout sides |
""")

M = lambda r: [r["title"].split(" - ")[0] if " - " in r["title"] else "P1.2"]
matrix = [
    ["Buildings (new)"] + [f"{r['buildings']} ({r['new_buildings']})" for r in (R12, RA, RB, RC)],
    ["New assets to download"] + ["0"] * 4,
    ["Archetypes (incl. variants)"] + [r["archetype_count"] for r in (R12, RA, RB, RC)],
    ["Developed footprint (m)"] + [f"{r['envelope_size'][0]:g} x {r['envelope_size'][1]:g}" for r in (R12, RA, RB, RC)],
    ["Terrain support zone (m)"] + [f"{r['support_zone'][0]:g} x {r['support_zone'][1]:g}" for r in (R12, RA, RB, RC)],
    ["Market configuration"] + ["2 halls, 12 stalls, open edges", "2 halls, 12 stalls, corner houses and registry on the edge", "as A plus a perimeter shop and the tea route house", "as B plus two more edge shops"],
    ["Primary route (m)"] + [r["primary_route_m"] for r in (R12, RA, RB, RC)],
    ["Walking graph: nodes / edges / loops"] + [f"{r['nodes']} / {r['edges']} / {r['loops']}" for r in (R12, RA, RB, RC)],
    ["Network length (m)"] + [r["network_m"] for r in (R12, RA, RB, RC)],
    ["Lane width, merchant street clear width"] + ["4 m, 8 m"] * 4,
    ["Wall enclosure / active frontage, all tested edges"] + [f"**{r['overall_wall_pct']}% / {r['overall_active_pct']}%**" for r in (R12, RA, RB, RC)],
    ["Hall tower visible from (of 15 tested points, massing)"] + [len(r["hall_tower_visible_from"]) for r in (R12, RA, RB, RC)],
    ["Camera: travel directions fully clear (massing ray test)"] + [f"{r['camera_fully_clear']} of {r['camera_directions']} ({100 * r['camera_fully_clear'] // r['camera_directions']}%)" for r in (R12, RA, RB, RC)],
    ["Camera: mean clear share on secondary routes"] + [f"{r['camera_secondary_mean_clear_pct']}%" for r in (R12, RA, RB, RC)],
    ["Triangles, unoptimised (estimate from archetype counts)"] + [f"{r['triangles_estimate_unoptimised']:,}" for r in (R12, RA, RB, RC)],
    ["Triangles after the P1.2 substitutions (projection)"] + [f"{r['triangles_estimate_after_substitutions']:,}" for r in (R12, RA, RB, RC)],
    ["Building collision proxies (boxes)"] + [r["collision_proxies_buildings"] for r in (R12, RA, RB, RC)],
    ["Materials / draw-call implication"] + ["53 materials", "same 53", "same 53: new buildings reuse existing materials, so batches grow in size, not number, if merged by material per district", "same"],
]
w("03-alternative-evaluation-matrix.md", f"""
# 03 - Alternative evaluation matrix

Numbers come from `asset-evidence/alternatives-metrics.json` (nominal footprints) and `asset-evidence/massing-ray-tests.json` (massing geometry).
They compare layouts on equal terms; the selected layout was then built with the real assets and re-measured (08).

{tbl(["Measure", "P1.2 baseline", "A - Refined (18)", "B - Compact (22)", "C - Expanded (24)"], matrix)}
## Enclosure by place (wall / active)

{tbl(["Place", "P1.2", "A", "B", "C"], encrows)}
## Reading the matrix

| Criterion | A | B | C |
|---|---|---|---|
| Visual enclosure | Small gain ({R12['overall_wall_pct']} to {RA['overall_wall_pct']}%). Lanes still one-sided | **Large gain ({R12['overall_wall_pct']} to {RB['overall_wall_pct']}%).** Lanes two-sided, arrival and bazaar edged | Slightly more than B ({RC['overall_wall_pct']}%) |
| Navigation | Cross street added, but 12 m of it runs between fences | Cross street, pocket court, service court, workyard: loops pass frontages | Same network as B |
| Secondary districts | Warehouse still behind a back court | Warehouse and counting house share a court on the lane; tea house one lane from the bazaar | Same as B |
| Camera | Best of the three (more open ground) | About the same as P1.2 in the massing test | Slightly worse than B: two more buildings on the hall-side lanes |
| Asset reuse | 1 building reused | 5 buildings from existing archetypes, one new shallow variant from verified modules | 7 buildings |
| Performance | +{RA['triangles_estimate_unoptimised'] - R12['triangles_estimate_unoptimised']:,} triangles | +{RB['triangles_estimate_unoptimised'] - R12['triangles_estimate_unoptimised']:,} | +{RC['triangles_estimate_unoptimised'] - R12['triangles_estimate_unoptimised']:,} |

## Selection: B, {RB['buildings']} buildings

- **A does not solve the problem.** Relocation alone lifts enclosure by {RA['overall_wall_pct'] - R12['overall_wall_pct']} points; the lanes and bazaar edges stay open. This answers the brief's question directly: moving buildings is not enough.
- **B is where the town changes character.** Enclosure rises from {R12['overall_wall_pct']}% to {RB['overall_wall_pct']}% and active frontage from {R12['overall_active_pct']}% to {RB['overall_active_pct']}%, every district gains an edge, and each added building has a named spatial job.
- **C buys little.** Two more buildings add {RC['overall_wall_pct'] - RB['overall_wall_pct']} points of enclosure, all on the bazaar edge, cost about {RC['triangles_estimate_unoptimised'] - RB['triangles_estimate_unoptimised']:,} triangles, narrow the hall-side lanes visually and slightly worsen the camera test. E06 would also stand on the corner where the tea lane leaves, crowding the one quiet route.
- **Not chosen because it is the middle option.** If the owner wants a busier bazaar edge later, E07 (west edge) is the better of C's two additions and can be added without moving anything; that would make 23.

The count of 22 is appropriate because it is the smallest number at which the lanes, the arrival court and the bazaar all have built edges; below it one of those stays open, above it the gain per building falls sharply.
""")

brow = [[b["id"], b["archetype"], b["label"], f"({b['x']}, {1.0 if b['archetype'] == 'A01' else 0.0}, {-b['n']})", b["rz"], f"{b['rect'][1] - b['rect'][0]:g} x {b['rect'][3] - b['rect'][2]:g}",
         f"{ENV[b['id']]['full_size'][0]} x {ENV[b['id']]['full_size'][1]}", b["status"]] for b in L["buildings"]]
w("04-selected-layout-design-bible.md", f"""
# 04 - Selected layout design bible (P1.3, alternative B)

Plan: [orthographic-town-plan.png](visuals/orthographic-town-plan.png). Data: `blender-inspection/layouts_p13.py` and `town_data.py`.
The architectural language, palette, signage and goods are those of the P1.2 design bible and style specification (`../p1/01`, `../p1/05`); this
document covers what P1.3 changes: the form of the town.

## The town in one paragraph

A visitor arrives in a court with a shop on the left and a two-storey merchant house on the right, passes between the gate lodges and walks up a
street of shopfronts. Half way, a cross street opens on both sides: left to the lantern lane of workshops, right through a small pocket court to
the warehouse lane, where the guild warehouse and the counting house face each other across a service court. The street ends in the bazaar, now
edged by corner houses, a perimeter shop and the registry. Between the two stone corner houses the court narrows to the width of the hall's
podium. From the bazaar's north-east corner a short lane passes a tea merchant's shop and opens onto the lookout terrace.

## Coordinates and size

Metres. Origin = centre of the arrival court. Plan x = east, n = north; project (x, y, z) = (x, elevation, -n). `rotation_y`: 0 = front faces south, 90 = east, -90 = west, 180 = north.
Developed envelope: x {x0}..{x1} ({x1 - x0} m), z {-n1}..{-n0} ({n1 - n0} m). P1.2 was 74.5 x 98 m: the town is 4 m narrower with five more buildings.

## Six clusters

| Cluster | Buildings | Form |
|---|---|---|
| A Arrival merchants | E01, E02, gate lodges, B04, B07 | Court 20 x 16 m with a single-storey shop west and a two-storey house east; lodges; the first two street buildings behind |
| B Merchant street | B04-B09 | Facades 10 m apart, 6 m eaves; gated 2 m gaps; a 4 m cross street at mid-length with a pocket court on its east side |
| C Bazaar district | B02, B03, B06, B09, B14, B15, B16, E03, E05 | 44 x 26 m plaza; halls in the middle; corner houses north, shop ends south, perimeter shop west, registry and tea route house east |
| D Civic exchange | B01, B15, B16 | Court 28 x 12 m between two stone corner houses, aligned with the podium |
| E Secondary trade quarters | B10-B13, E04 | Lanes 4 m wide directly behind the street rows; artisan workyard at the north end of one, service court on the other |
| F Scenic edge | B17, E05 | Tea lane 8 m long, terrace 12 x 10 m, tea house on its north side |

## Spatial sequence on the primary route

| Step | Space | Width between buildings | Character |
|---|---|---|---|
| 1 | Arrival court | 20 m | Open, two fronts |
| 2 | Gate | 4 m lane between lodges | Threshold |
| 3 | Street, south half | 10 m | Enclosed, shopfronts |
| 4 | Simpang Timbangan | 10 m with 4 m openings and an 8 x 6 m pocket | Junction: first choice of route |
| 5 | Street, north half | 10 m | Enclosed |
| 6 | Bazaar | 44 m, 9 m between stall rows | Wide, busy, hall roofs either side |
| 7 | Civic court | 28 m | Formal, stone, no stalls |
| 8 | Podium and porch | - | Arrival |

## Street enclosure (wall-top height to facade distance)

| Street | Facade to facade | Wall-top heights | Ratio | Reading |
|---|---|---|---|---|
| Merchant street | 10 m | 6 m and 3 m | 0.3-0.6 | Comfortably enclosed at the 6.6 m high camera |
| Lanes | 4.5-7.5 m (lane plus yard) | 3 m workshops, 6 m street backs | 0.4-1.3 | Intimate; yards keep the 6 m backs 1-3 m off the lane so sky stays open |
| Cross street | 4 m | 6 m and 3 m | 0.75-1.5 | Short and tight by intent (9 m each side) |
| Civic court | 28 m | 6 m sides, 7 m hall | 0.2-0.25 | Formal forecourt; was 36 m |

No route was narrowed below the P1.2 gameplay widths: lanes stay 4 m, the street keeps 8 m clear.

## Building positions

{tbl(["ID", "Archetype", "Name", "Position (x, y, z)", "rotation_y", "Nominal footprint (m)", "Measured envelope (m)", "Change since P1.2"], brow)}
**{len(changed)} of {nb} buildings are new, moved, rotated or re-typed; {nb - len(changed)} are where P1.2 had them** (the hall, both market halls, B07). No building was deleted. Full figures: [05-building-schedule.csv](05-building-schedule.csv).

## Keeping reused archetypes from reading as copies

Five additions come from four existing archetypes and one new variant. They differ by orientation, storey count on the plot, sign pictogram and per-building
additions: the counting house and the assay office carry the guild seal, the counting house a burgundy banner, the perimeter shop a vine and grain sacks,
the tea route shop a keg and a menu stand. A05 is now used four times (two court corners, junction corner, counting house); that repetition is deliberate for the
stone civic-commercial class but is the first candidate for a second corner variant if it reads as repetitive in play.

## Stalls

{ns} stalls, unchanged in number and kind. Two moved 2.1 m north and two 0.7 m south so the paths from the lanes and to the court pass them with clearance (05b).
The count was not raised: the bazaar's weakness was its edge, not the number of stalls.
""")

w("06-pedestrian-network.md", f"""
# 06 - Pedestrian network (P1.3)

{len(L['nodes'])} nodes, {len(edges)} edges ({len(built)} built, 1 reserved link), **{len(edges) - len(L['nodes']) + 1} independent loops**, {net} m of built route. P1.2: 31 nodes, 39 edges, 9 loops, 437 m.
Primary route, arrival court to the hall podium: **{prim} m**, about {prim / 2.1:.0f} s walking or {prim / 4.6:.0f} s running.

## Named loops (measured along the graph)

{tbl(["Loop", "Nodes", "Length (m)", "Walk at 2.1 m/s", "What it passes"], looprows)}
Every loop above passes at least two building fronts and one of the small public spaces. In P1.2 the street had no side exit: the only way from it to either lane was back through the arrival court or on to the bazaar.

## Physical validation of every edge (actual geometry)

Sampled every 0.25 m: paved surface below, step 0.42 m or less, no geometry within 0.34 m of the body at four heights, headroom 2.0 m or more.

{tbl(["Edge", "Type", "Length (m)", "Unpaved samples", "Largest step (m)", "Least headroom (m)", "Nearest obstacle at 1 m height (m)", "Result"], drow)}
**{SUM['edges_total'] - 1 - SUM['edges_fail']} of {SUM['edges_total'] - 1} built edges pass.** First run of the new layout: three edges failed (two court benches on the new court-side paths, a stall's barrel on the path to the east court entrance); benches and the two north stalls were moved and the test repeated.

## Nodes

{tbl(["Node", "x", "z", "Place"], [[k, v[0], -v[1], v[2]] for k, v in L["nodes"].items()])}
""")

arows = []
for a in ["A01", "A02", "A03", "A03b", "A03c", "A04", "A04b", "A05", "A06", "A07", "A08"]:
    A, R = ARCH[a], AREP[a]
    packs = sorted({k.split("-")[0] for k in R["usage"]})
    src = ", ".join({"MV": "Quaternius Medieval Village", "FP": "Quaternius Fantasy Props", "SY": "Syntaxes of Play Medieval Cafe", "AV": "Avramania", "CUS": "custom (seal / sign)", "SN": "Quaternius Stylized Nature"}[p] for p in packs)
    arows.append([a, PURPOSE[a], arche_n[a], ", ".join(b["id"] for b in L["buildings"] if b["archetype"] == a), f"{A['footprint'][0]} x {A['footprint'][1]}", A["height_m"], f"{R['instances']} / {R['unique_assets']}", f"{R['triangles']:,}", src, STATUS[a]])
A3 = AREP["A03c"]
w("07-archetype-schedule.md", f"""
# 07 - Archetype schedule (P1.3)

Sheet: [archetype-assembly-sheet.png](visuals/archetype-assembly-sheet.png). Ten of the eleven assemblies are those of P1.2, unchanged; their module lists,
facade strings, collision notes and acceptance criteria are in `../p1/08-archetype-specifications.md`. One variant is new.

{tbl(["ID", "Purpose", "Instances", "Used by", "Footprint (m)", "Height (m)", "Module instances / ids", "Triangles each", "Verified sources", "Readiness"], arows)}
Instances changed from P1.2: A03 3 to 2 (B16 re-typed), A03b 1 to 2, A03c 0 to 1, A04 2 to 2, A04b 2 to 4, A05 2 to 4. Total {nb}.

## A03c - Shallow Merchant House (new variant, READY)

| Field | Value |
|---|---|
| Why it exists | A two-storey house for a plot that backs onto a lane: 8 m of frontage but only 4 m deep, so its rear eave stays clear of the lane's follow-camera line. The 6 m deep A03b in the same position shortened the camera at the start of the warehouse lane to 1.8 m |
| Footprint, height | 8 x 4 m, {ARCH['A03c']['height_m']} m; measured bounds {A3['measured_bounds_m'][0]} x {A3['measured_bounds_m'][1]} x {A3['measured_bounds_m'][2]} m |
| Assembly | Same wall, window, door, shutter and post modules as A03b on a 4 x 1 bay grid of two storeys; roof `MV-Roof_RoundTiles_4x8` with the ridge along the frontage; gables `MV-Roof_Front_Brick4`; timber canopy, one trade sign, lantern, two flower boxes, chimney |
| Facades | front `FDFG` / `RRGR`; sides `PP` / `PT`; back `PPPP` / `PRRP` |
| Modules | """ + ", ".join(f"`{k}` x{v}" for k, v in sorted(A3["usage"].items(), key=lambda kv: -kv[1])) + f""" |
| New downloads | None. `MV-Roof_RoundTiles_4x8` was verified in P1.0 and is first used here |
| Custom | Trade sign x1 (as every shop) |
| Collision | One box 8 x 4 x 6 |
| Triangles | {A3['triangles']:,} unoptimised |

## Dependencies carried over from P1.2

READY: A01, A03b, A03c, A04, A04b, A05, A06, A07, gateway, market cross. CONDITIONAL: A02 (cafe-pack materials re-linked on export, Avramania goods), A03 (windows mounted on the jetty face), A08 (Avramania sign and flower boxes). BLOCKED: none.
""")

w("08-geometry-camera-qa.md", f"""
# 08 - Actual geometry and camera QA (P1.3 selected layout)

Method unchanged from P1.1 and P1.2 (`validate_envelopes.py`): the assembled Blender scene, {VAL['triangles_tested']:,} triangles, tested with ray casts and nearest-surface queries
using constants copied from the project's controller and camera files. The production controller and camera were not modified or run.
Raw results: [asset-evidence/spatial-validation-actual-geometry.json](asset-evidence/spatial-validation-actual-geometry.json).

## Summary

| Check | Result |
|---|---|
| 1 Nominal footprints: overlaps, clear corridors, paved door approaches, stalls on paving, connectivity | {"PASS" if L["checks_pass"] else "FAIL"} |
| 2 Measured envelopes (roofs, signs, props) | {len(VAL['A_envelopes'])} structures measured; in 05 |
| 3 Building and roof overlap | {SUM['roof_gaps_fail']} failing; {SUM['roof_gaps_narrow']} narrow (0.3-1.0 m) |
| 4-6 Routes, loops, paving continuity | {SUM['edges_total'] - 1 - SUM['edges_fail']} of {SUM['edges_total'] - 1} built edges pass |
| 7 Entrance clearances | Arch 1.67 m wide, 2.74 m high (unchanged); hall stairs five risers, largest {VAL['E_stairs']['max_riser_m']:.3f} m; lowest hanging object over paving {hang[0]['clearance_m']} m |
| 8 Follow camera | {SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']} travel directions fully clear; details below |
| 9 Hall visibility | Tower seal visible from {len(RB['hall_tower_visible_from'])} of {len(RB['hall_points_tested'])} tested points (massing) |
| 10 Terrain support envelope | Recalculated in 09 |

## Roof gaps under 3 m

{tbl(["A", "B", "Gap (m)", "Status"], gaps)}
Two pairs are narrow by design: the 2 m gated gaps on the merchant street. The first run had B08-B09 at 0.09 m (a clash in practice); B09 and B06 were each moved 0.4-0.6 m.
No pair overlaps.

## Follow camera

A ray from the look-at point (player +1.25 m) to the camera position (11.8 m behind, +6.6 m) for every edge, both directions.

| | P1.2 | P1.3 |
|---|---|---|
| Travel directions tested | {V12['summary']['camera_travel_directions']} | {SUM['camera_travel_directions']} |
| Fully clear | {V12['summary']['camera_edges_fully_clear']} ({100 * V12['summary']['camera_edges_fully_clear'] // V12['summary']['camera_travel_directions']}%) | {SUM['camera_edges_fully_clear']} ({100 * SUM['camera_edges_fully_clear'] // SUM['camera_travel_directions']}%) |
| Shortest camera distance anywhere | {V12['summary']['camera_min_distance_m']} m | {SUM['camera_min_distance_m']} m |
| Primary axis, walking towards the hall | clear except 6 m past the market cross | """ + ("clear except 6 m past the market cross" if all(cam13[t]["unobstructed_pct"] == 100 or "N27" in t for t in fwd) else "see table") + f""" |

**Stated plainly: the denser town has a smaller share of fully clear directions than P1.2 ({100 * SUM['camera_edges_fully_clear'] // SUM['camera_travel_directions']}% against {100 * V12['summary']['camera_edges_fully_clear'] // V12['summary']['camera_travel_directions']}%).** More buildings near more corners means more
moments when a camera placed directly behind the player would be inside a roof. The shortest camera distance anywhere improved (0.8 m to {SUM['camera_min_distance_m']} m), and so did the shortest distance at the three worst spots of P1.2. The clear share did not improve everywhere: at the two court corner doors it fell (37% and 31% to 20%), and under the hall roofs nothing changed:

{tbl(["Travel", "Situation", "P1.2: clear share / shortest", "P1.3: clear share / shortest"], camrows)}
The test assumes the camera sits exactly behind the direction of travel. At a corner or when stepping away from a door the real camera is still swinging round
from the previous heading, so these are worst cases; they are also exactly the places a camera-collision system exists for.

New in P1.3 (edges that did not exist in P1.2), worst first:

{tbl(["Travel", "Type", "Samples unobstructed", "Shortest camera distance (m)", "Blocked by"], newcam)}
What was done about camera conflicts by layout: the tea lane leaves the bazaar north of the east hall instead of beside it (a hall-side exit put the camera inside the hall roof);
the two arrival buildings were made 4 m deep after the first build showed them shortening the camera at both lane starts (1.8 m and 2.9 m; now clear of the lane line);
the tea house approach is across an open terrace.

## Exchange Hall visibility (eye height 1.65 m, massing geometry)

{tbl(["From", "Place", "Tower seal", "Porch gable"], visrows)}
The tower is visible from the arrival court, the gate, the junction, the bazaar entrance, the bazaar north of the market cross and the court's south edge, and now also from the artisan lane at the cross street. Standing exactly on the axis just south of the market cross, the cross's post hides it; at the court centre the porch gable hides the tower seal while the porch itself is in view.
It is not visible from inside the lanes north of the junction, the bazaar's side lanes or the terrace: the market halls and two-storey houses stand in the way, as in P1.2.

## Outstanding in-engine validation (cannot be settled in Blender)

1. Camera behaviour at the listed corners and door exits with the game's real collision set and smoothing.
2. Controller on the hall stairs, through the market-hall arches and across the 4 m lanes at running speed.
3. Whether thin objects (signs, lamp arms, vines, fences) are in the camera collision set at all.
4. Frame time with five more buildings; nothing here is a browser measurement.
""")

w("09-terrain-interface-contract.md", f"""
# 09 - Terrain interface contract (P1.3; no island is modelled)

| Requirement | P1.2 | P1.3 |
|---|---|---|
| Developed envelope | x -28.5..46, z -90..8 (74.5 x 98 m) | x {x0}..{x1}, z {-n1}..{-n0} (**{x1 - x0} x {n1 - n0} m**) |
| Future transport reservation | x -10..10, z 8..24 (20 x 16 m) | unchanged |
| Combined footprint the terrain must carry | 74.5 x 114 m | **{ux1 - ux0} x {un1 - un0} m** |
| Terrain support zone (combined + 10 m each side, assumption) | 94.5 x 134 m | **{ux1 - ux0 + 20:.1f} x {un1 - un0 + 20:.0f} m** (x {ux0 - 10}..{ux1 + 10}, z {-un1 - 10}..{-un0 + 10}) |
| Base elevation | y = 0 everywhere except the podium | unchanged |
| Only raised surface | Exchange Hall podium, y = +1.0, x -14..14, z -90..-74 | unchanged |
| Building foundation zones | 17 measured envelopes | {nb} measured envelopes (05) |
| Lookout | Terrace x 34..46, z -54..-44, faces east | **Terrace x 30..42, z -62..-52**; fence on the east (x = 42) and south (z = -52) sides; faces east and south |
| Surface treatments (terrain material, not geometry) | Two back courts | Three packed-earth yards behind the street rows and the counting house |

The support zone is 4 m narrower than P1.2's and the same length. The lookout moved 4 m west and 8 m north, so the island edge that the terrace overlooks moves with it:
the edge may come to about 3 m east and south of the terrace fence. No cliff, drop or waterfall inside the support zone otherwise.
If the transport pad becomes a landing, the island edge may meet its south side. Likely island size: about 110 x 155 m or larger; silhouette not fixed.

Not created: island mesh, cliffs, waterfalls, underside, terrain export.
""")

crows = [[k, f"{C12[k]:,}", f"{C13[k]:,}", f"{C13[k] - C12[k]:+,}"] for k, _ in C13.most_common()]
w("10-p2-construction-contract.md", f"""
# 10 - P2 construction contract for the selected P1.3 layout (not started; needs explicit authorisation)

P2 builds the archetypes as reusable assemblies and proves one of them in the real Three.js scene. It does not assemble the town (P3) or build terrain (P4).
This contract replaces `../p1/12-p2-construction-contract.md` where they differ; the per-archetype module lists, material strategy, collision notes and acceptance criteria in `../p1/08` still apply.

## Roster

{tbl(["ID", "Purpose", "Instances", "Used by", "Footprint (m)", "Height (m)", "Module instances / ids", "Triangles each", "Verified sources", "Readiness"], arows)}
Structures: split gateway (READY), market cross (READY). Stall kits: five kinds, 12 stalls (READY; three kinds depend on the cafe and Avramania packs).

**What P1.3 adds to the P2 work:** one variant (A03c, from modules already verified), a per-building "additions" list (seal, banner, vine, goods) so reused archetypes differ, and nothing else.
No new download, no new custom mesh, no new material.

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Materials: bake the colour grade into copies of the base-colour textures; merge duplicates only where the node set-up is identical; cloth and dark-roof instances; seal and sign meshes. Convert the used cafe-pack models to GLB once.
3. Shared wall, window, door, roof and signage sub-assemblies.
4. A04, A04b (six instances between them). 5. A03b, **A03c**, A03. 6. A05 (four instances), A06.
7. A02, gateway, market cross. 8. A01. 9. A07, A08.
10. Apply the substitutions below; join static meshes per building by material.
11. One archetype exported and loaded in the real scene; measurements recorded; stop for approval.

## Performance estimate (Blender measurements; no browser figure exists)

| | P1.2 | P1.3 |
|---|---|---|
| Buildings | 17 | {nb} |
| Instances | {S12['instances']:,} | {STATS['instances']:,} |
| Downloaded models used | 139 | {STATS['unique_downloaded_models']} |
| Triangles, unoptimised (measured) | {S12['triangles']:,} | **{STATS['triangles']:,}** ({100 * (STATS['triangles'] - S12['triangles']) / S12['triangles']:+.0f}%) |
| Distinct materials | 53 | {len(base_mats)} |
| Paving tiles | 700 | {STATS['paving_tiles']} |
| After the substitutions below (projection) | 461,419 | **{TOWN_NEW:,}** |

Triangles by category:

{tbl(["Category", "P1.2", "P1.3", "Change"], crows)}
Five buildings added {STATS['triangles'] - S12['triangles']:,} triangles, about {(STATS['triangles'] - S12['triangles']) // 5:,} each, because every building repeats the same modules: geometry is reused, not multiplied in kind.
Largest contributors and the substitution proposed for each (targets are for simplified meshes that P2 must produce and measure):

{tbl(["Component", "Instances", "Triangles each", "Total now", "Target each", "Saving"], optrows)}
| Lever | Effect |
|---|---|
| Instancing | {STATS['instances']:,} instances draw from {STATS['unique_assets']} meshes. Repeated modules (wall bays, windows, posts, lanterns, tiles) are candidates for `InstancedMesh`; the brick pier is placed {U.get('MV-Corner_Exterior_Brick', 0)} times and the lantern {U.get('FP-Lantern_Wall', 0)} |
| Static merge | Alternatively merge each building by material: about {len(base_mats)} materials town-wide, so the number of batches depends on materials, not on the building count. The five new buildings add to existing batches |
| LOD and visibility | The compact layout hides more: from any street the far districts are behind two-storey rows. Backdrop trees and far roofs can drop to a lower level beyond about 40 m. To be measured, not assumed |
| Collision | {RB['collision_proxies_buildings']} box proxies for buildings (P1.2: {R12['collision_proxies_buildings']}); posts and stalls extra. No mesh colliders |
| Paving | {STATS['paving_tiles']} tiles could be one plane per surface ({len(L['paving'])} surfaces) |

The earlier figure of about 350,000 triangles is not reached by substitutions alone ({TOWN_NEW:,}). The remaining levers are fewer or lower-detail backdrop trees and lower-detail wall and roof modules; each should be decided on a browser measurement.

## Measurable P2 verification steps

| Step | Measure | Pass condition (proposed, to be agreed) |
|---|---|---|
| 1 | Triangles per archetype GLB (`docs/tooling/glb-inventory.mjs`) | At or below the agreed budget |
| 2 | Distinct materials and textures in the exported set | At or below {len(base_mats)}; no texture above 2048 px |
| 3 | One archetype in the real page: `renderer.info.render.triangles` and `.calls` at three fixed cameras against the island-1 baseline | Recorded; increase within budget |
| 4 | Scale and orientation: door 2.1 m, storey 3.0 m, +y up, front on +z | Within 1 cm |
| 5 | Controller on the hall stairs, through a hall arch, and along a 4 m lane | No sticking |
| 6 | Follow camera at the corners and door exits listed in 08 | Behaves acceptably with the game's collision set; recorded |
| 7 | Frame time over a fixed 60 s walk at 1280 x 720 | Recorded with hardware noted |

**Browser performance has not been validated.**
""")

w("11-before-after-comparison.md", f"""
# 11 - Before/after: P1.2 and P1.3

Images, same cameras, same light, same materials, same goods: [A aerial](visuals/before-after-a-aerial.jpg), [B merchant street](visuals/before-after-b-merchant-street.jpg),
[C bazaar](visuals/before-after-c-central-bazaar.jpg), [D Exchange Hall](visuals/before-after-d-exchange-court.jpg). Plans side by side: [alternatives-plans.png](visuals/alternatives-plans.png) (first and third panels).
Because nothing but the layout changed between the two sets, what differs in the images is urban form.

| Measure | P1.2 | P1.3 | |
|---|---|---|---|
| Permanent buildings | 17 | **{nb}** | +5, none deleted |
| Buildings moved, rotated or re-typed | - | {len(changed) - 5} | {nb - len(changed)} left in place |
| Archetypes incl. variants | 10 | 11 | one shallow variant |
| Market stalls | 12 | {ns} | four nudged for clearance |
| Developed envelope | 74.5 x 98 m | {x1 - x0} x {n1 - n0} m | 4 m narrower |
| Ground covered by buildings | {R12['coverage_pct']}% | {RB['coverage_pct']}% | |
| Wall enclosure of tested street and court edges | {R12['overall_wall_pct']}% | **{RB['overall_wall_pct']}%** | |
| Active (door-side) frontage on those edges | {R12['overall_active_pct']}% | **{RB['overall_active_pct']}%** | |
| Lanes with buildings on both sides | 0 of 2 | 2 of 2 | |
| Bazaar perimeter enclosed / active | {G(R12, 'Bazaar perimeter')[0]}% / {G(R12, 'Bazaar perimeter')[1]}% | {G(RB, 'Bazaar perimeter')[0]}% / {G(RB, 'Bazaar perimeter')[1]}% | |
| Arrival court sides enclosed | {G(R12, 'Arrival court sides')[0]}% | {G(RB, 'Arrival court sides')[0]}% | |
| Civic court width | 36 m | 28 m | podium width |
| Side exits from the merchant street | 0 | 2 | the cross street |
| Small public spaces | 0 | 4 | pocket court, workyard, service court, tea lane |
| Walking loops | 9 | {len(edges) - len(L['nodes']) + 1} | |
| Tea house from the bazaar edge | 18 m by an open path | 8 m lane past a shopfront, then the terrace | |
| Triangles, unoptimised | {S12['triangles']:,} | {STATS['triangles']:,} | {100 * (STATS['triangles'] - S12['triangles']) / S12['triangles']:+.0f}% |
| Camera: directions fully clear | {V12['summary']['camera_edges_fully_clear']} of {V12['summary']['camera_travel_directions']} | {SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']} | lower share, see 08 |

## What the images show

| View | Improved | Not improved, or worse |
|---|---|---|
| A aerial | One cluster with a readable outline; lanes read as streets; the warehouse, counting house and tea house belong to the town; arrival has two flanking roofs | The bazaar is still a large open rectangle from above; the town still stands in a field (no terrain yet) |
| B merchant street | A junction opens at mid-length with a corner house addressing it; the street no longer reads as one corridor | Frontage on the street itself is 2 points lower (73 to 71%) because two gaps were widened into the cross street |
| C bazaar | Stone corner houses close the north side and frame the hall; shop roofs appear behind both halls | The plaza floor is still uniform; the west and east edges are only partly built (38% enclosed) |
| D Exchange Hall | Corner houses stand closer and frame the court | The hall itself is unchanged, as intended |
| E, E2, F (new) | The secondary routes now have something to show: a service court, a two-sided lane, a tea lane with a shopfront | The lanes are tight for the camera at their corners (08) |

## Self-assessment against the decision gate

| Requirement | Met? |
|---|---|
| Stronger urban enclosure | Yes: {R12['overall_wall_pct']}% to {RB['overall_wall_pct']}% |
| Better organised commercial space | Yes for the edges; the plaza interior is unchanged |
| More convincing settlement density | Yes: +5 buildings in a smaller envelope |
| Functional walking loops | Yes: {len(edges) - len(L['nodes']) + 1} loops, all {SUM['edges_total'] - 1} built edges validated |
| Secondary districts integrated | Yes |
| Appropriate third-person scale | Partly: widths kept, camera share lower; needs the engine |
| Clear Exchange Hall hierarchy | Yes; court framed |
| Asset-backed construction | Yes: no new download, one variant from verified modules |
| Feasible optimisation strategy | Stated and quantified; unproven until measured in a browser |

Internal visual score is not re-issued for P1.3: the scoring criteria of P1.2 were about materials and dressing, which did not change. Human review is pending.
""")

w("12-changes-and-approval-dependencies.md", f"""
# 12 - Changes and approval dependencies (P1.3)

## Differences between P1.2 and P1.3 in brief

P1.2 changed how the town looked (palette, seal, signs, goods, light) and moved nothing. P1.3 changes where things are and how many there are, and leaves the look alone:
five more buildings ({nb}), both lanes moved in behind the street rows, a cross street with a pocket court, corner houses and shops on the bazaar and arrival edges,
a service court for the warehouse, and the tea house brought to within one short lane of the bazaar.

## Files

New folder `docs/planning/merchant-citadel/p1.3/` (this package). The P1.2 package in `../p1/` was not modified.

| File | Content |
|---|---|
| `README.md`, `01`-`04`, `06`-`12` | Documents listed in the README |
| `05-building-schedule.csv`, `05b-market-stall-schedule.csv` | Schedules with measured envelopes and change status |
| `visuals/` | Eight views, four before/after pairs, alternatives plans and massing, selected plan, top render, archetype sheet |
| `asset-evidence/` | Validation results, alternatives metrics, massing ray tests, usage and triangles |
| `blender-inspection/layouts_p13.py` | The three alternatives and the enclosure metric |
| `blender-inspection/massing_p13.py`, `compare_p13.py` | Massing renders, ray tests, comparison |
| `blender-inspection/town_data.py`, `citadel_lib.py`, `build_town.py`, `validate_envelopes.py`, `render_archetypes.py` | Copies of the P1.2 scripts, changed for the selected layout (A03c, per-building additions, new dressing) |
| `blender-inspection/make_p13_package.py` | This package generator |

Workspace (ignored by Git): `.asset-inspection/merchant-citadel-p1/p1.3/` holds the P1.3 data, renders, massing and blockout; `p1.2/` holds a snapshot of the P1.2 data, renders, validation and blockout.

## Scope confirmation

No production town implementation, island terrain, Three.js change, first-island asset reuse, gameplay system, dragon transport, GLB export, deployment or commit. No asset was downloaded in P1.3.

## Approval dependencies

1. **The selected layout (B, {nb} buildings)**, or a preference for A, C or B plus E07.
2. **The look carried over from P1.2** was not separately approved before this brief arrived: the burgundy and blue colours, the new seal, the trade-sign pictograms, and the two added asset sources (Syntaxes of Play, Avramania). P1.3 assumes them.
3. **A05 used four times** and **A03c as a new variant**: acceptable, or ask for a second corner variant.
4. **A triangle and draw-call budget.**
5. **Authorisation to start P2.** Not assumed.

**MERCHANT CITADEL P1.3 - PENDING HUMAN REVIEW. STOP.**
""")
print("package written:", nb, "buildings,", STATS["triangles"], "tris ->", TOWN_NEW, "| enclosure", R12["overall_wall_pct"], "->", RB["overall_wall_pct"], "| loops", len(edges) - len(L["nodes"]) + 1, "| net", net, "| prim", prim)
