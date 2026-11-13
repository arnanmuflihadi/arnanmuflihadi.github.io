#!/usr/bin/env python3
"""Build the Merchant Citadel P1.4 planning package (visuals, schedules, documents) from measured data.

Usage: python3 make_p14_package.py <inspection_dir> <package_dir>
Needs <inspection_dir>/p1.4/{data,renders,archetypes,massing,tiles,validation.json} and the P1.3 results in <inspection_dir>/p1.3.
Narrative is authored here; tables and numbers are read from the data.
"""
import csv, json, math, os, re, shutil, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layouts_p14 as LY
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrow

I, P = sys.argv[1], sys.argv[2]
D, D3 = f"{I}/p1.4", f"{I}/p1.3"
L = json.load(open(f"{D}/data/layout.json")); ARCH = json.load(open(f"{D}/data/archetypes.json")); AREP = json.load(open(f"{D}/archetypes/archetype-report.json"))
STATS = json.load(open(f"{D}/renders/town-stats.json")); VAL = json.load(open(f"{D}/validation.json")); RES = json.load(open(f"{D}/massing/alternatives.json")); ITEMS = json.load(open(f"{D}/tiles/p14-items.json"))
S13 = json.load(open(f"{D3}/renders/town-stats.json")); V13 = json.load(open(f"{D3}/validation.json")); L13 = json.load(open(f"{D3}/data/layout.json"))
MAN = {m["pack_id"]: m for m in json.load(open(f"{I}/archives/archive-manifest.json"))}
os.makedirs(f"{P}/visuals", exist_ok=True); os.makedirs(f"{P}/asset-evidence", exist_ok=True)
DATE = "2026-11-12"
U, TE = STATS["usage"], STATS["tris_each"]; U13 = S13["usage"]
ENV = {a["id"]: a for a in VAL["A_envelopes"]}; SUM, SUM13 = VAL["summary"], V13["summary"]
RB, RD, RE = RES["B"], RES["D"], RES["E"]
nb, ns, nr = len(L["buildings"]), len(L["stalls"]), len(L["rows"])
x0, x1, n0, n1 = L["envelope"]; rx0, rx1, rn0, rn1 = L["reserved"][0][1:]
ux0, ux1, un0, un1 = min(x0, rx0), max(x1, rx1), min(n0, rn0), max(n1, rn1)
base_mats = sorted({re.sub(r"\.\d+", "", m) for m in STATS["materials"]}); mats13 = sorted({re.sub(r"\.\d+", "", m) for m in S13["materials"]})
arche_n = collections.Counter(b["archetype"] for b in L["buildings"])
tbl = lambda head, rows: "\n".join(["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]) + "\n"
w = lambda name, text: open(f"{P}/{name}", "w").write(text.strip() + "\n")


def font(size, bold=False):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1 if bold else 0)
    except Exception:
        return ImageFont.load_default()


def label(src, dst, title, klass, note):
    im = Image.open(src).convert("RGB"); wd, h = im.size
    out = Image.new("RGB", (wd, h + 64), (24, 44, 40)); out.paste(im, (0, 0)); d = ImageDraw.Draw(out)
    d.text((16, h + 8), title, font=font(22, True), fill=(245, 240, 225)); d.text((16, h + 37), note, font=font(15), fill=(190, 205, 198))
    tw = d.textlength(klass, font=font(18, True)); d.rectangle([wd - tw - 40, h + 14, wd - 14, h + 50], fill=(196, 120, 40)); d.text((wd - tw - 27, h + 21), klass, font=font(18, True), fill=(255, 255, 255))
    out.save(dst, **({"quality": 92} if dst.endswith(".jpg") else {"optimize": True}))


# ---------------------------------------------------------------- outputs and before/after
BLK = "ASSET-BACKED BLENDER BLOCKOUT"
note = "P1.4 selected layout D (24 buildings). Downloaded CC0 models; CUSTOM: seal, trade signs, cloth awnings, pennant lines, paving seal. Temporary: ground, yards, dark fills, 1.9 m explorer, afternoon light."
VIEWS = [("view-a-aerial", "output-a-hero-aerial", "OUTPUT A - Hero aerial (same camera as P1.0-P1.3)"), ("view-b-merchant-street", "output-b-merchant-street-gameplay", "OUTPUT B - Merchant Street at the documented gameplay camera (FOV 60, 11.8 m behind, +6.6 m)"),
         ("view-b2-merchant-street-eye", "output-b2-merchant-street-eye", "OUTPUT B2 - Merchant Street at eye height (1.65 m)"), ("view-c-central-bazaar", "output-c-central-bazaar", "OUTPUT C - Central Bazaar from its southern edge (same camera as P1.2 and P1.3)"),
         ("view-c2-bazaar-eye", "output-c2-central-bazaar-eye", "OUTPUT C2 - Central Bazaar at eye height: goods, awning rows, halls, tower houses, Exchange Hall"), ("view-d-exchange-court", "output-d-exchange-hall", "OUTPUT D - Exchange Hall and civic terrace at eye height (same camera as P1.3)"),
         ("view-e-service-court", "output-e-secondary-service-court", "OUTPUT E - Secondary: junction pocket court, warehouse lane and service court, eye height"), ("view-e2-artisan-lane", "output-e2-secondary-artisan-lane", "OUTPUT E2 - Secondary: artisan lane at the gameplay camera"),
         ("view-f-tea-route", "output-f-tea-lookout", "OUTPUT F - Tea lane, lookout terrace and tea house, eye height"), ("view-g-bazaar-from-terrace", "experiment-bazaar-from-terrace", "EXPERIMENT - The bazaar seen from the civic terrace (tests the return view)")]
for v, o, title in VIEWS:
    label(f"{D}/renders/{v}.png", f"{P}/visuals/{o}" + (".jpg" if o.startswith("experiment") else ".png"), title, BLK, note)
    if os.path.exists(f"{D3}/renders/{v}.png"):
        a, b = Image.open(f"{D3}/renders/{v}.png").convert("RGB"), Image.open(f"{D}/renders/{v}.png").convert("RGB"); wd, h = 1280, 720
        s = Image.new("RGB", (wd * 2 + 12, h + 56), (24, 44, 40)); s.paste(a.resize((wd, h), Image.LANCZOS), (0, 56)); s.paste(b.resize((wd, h), Image.LANCZOS), (wd + 12, 56)); d = ImageDraw.Draw(s)
        d.text((16, 14), "BEFORE - P1.3 (22 buildings)", font=font(24, True), fill=(235, 200, 170)); d.text((wd + 28, 14), "AFTER - P1.4 (24 buildings)", font=font(24, True), fill=(170, 230, 215))
        d.text((420, 20), "same camera, same light", font=font(15), fill=(190, 205, 198))
        s.save(f"{P}/visuals/before-after-{o[7:]}.jpg", quality=92)
label(f"{D}/renders/blockout-top-ortho.png", f"{P}/visuals/blockout-top-orthographic.jpg", "Top orthographic render of the P1.4 blockout (north up)", BLK, note)

# massing comparison -------------------------------------------------------------------------------
wd, h = 1400, 900
sheet = Image.new("RGB", (3 * wd, h + 70), (24, 44, 40)); d = ImageDraw.Draw(sheet)
d.text((16, 12), "Merchant Citadel P1.4 - aerial MASSING comparison, one camera. Boxes and roof prisms at real module dimensions; no downloaded model. Gold roof = new or re-typed building.", font=font(26, True), fill=(245, 240, 225))
for i, k in enumerate(("B", "D", "E")):
    sheet.paste(Image.open(f"{D}/massing/massing-{k}.png").convert("RGB"), (i * wd, 70)); d.rectangle([i * wd, 70, i * wd + 720, 112], fill=(24, 44, 40))
    d.text((i * wd + 12, 78), f"{RES[k]['title']} - {RES[k]['buildings']} buildings", font=font(22, True), fill=(245, 240, 225))
sheet.save(f"{P}/visuals/alternatives-massing.jpg", quality=92)

# evidence sheet: new archetypes, custom elements, newly used modules, rejected candidates ----------
cells = [(f"{D}/archetypes/{a}-front.png", f"{a} {ARCH[a]['name']}"[:44], f"{AREP[a]['instances']} instances, {AREP[a]['triangles']:,} tris", "NEW ASSEMBLY (verified modules)") for a in ("A01", "A09", "A11", "A11m", "A10p", "A10c", "A03c", "A04b")]
KIND = {"CUS": ("CUSTOM geometry (authored, not downloaded)", (150, 90, 20)), "MV-": ("Quaternius module first used in P1.4", (30, 110, 60)), "ALE": ("EXAMINED, NOT ADOPTED (licence)", (160, 50, 40))}
for it in ITEMS:
    k = KIND[it["id"][:3]]; dm = it["dimensions_m"]
    if it["id"].startswith("MV-") and it["id"] in U13:
        k = ("Quaternius module (in use before P1.4), key to a new assembly", (30, 110, 60))
    cells.append((f"{D}/tiles/{it['id']}.png", it["id"][:40], f"{dm[0]} x {dm[1]} x {dm[2]} m, {it['triangles']:,} tris", k[0]))
cols, px = 6, 330
sheet = Image.new("RGB", (cols * px, ((len(cells) + cols - 1) // cols) * (px + 62) + 76), (244, 243, 238)); d = ImageDraw.Draw(sheet)
d.text((14, 10), "Merchant Citadel P1.4 - evidence of new assemblies, custom elements, newly used modules and rejected candidates (real Blender renders, 1.9 m figure for scale)", font=font(20, True), fill=(24, 44, 40))
for i, (f, name, sub, kind) in enumerate(cells):
    x, y = (i % cols) * px, 76 + (i // cols) * (px + 62)
    col = (30, 110, 60) if "verified" in kind or "Quaternius" in kind else (150, 90, 20) if "CUSTOM" in kind else (160, 50, 40)
    d.rectangle([x + 3, y, x + px - 3, y + px + 58], fill=(226, 232, 226) if col == (30, 110, 60) else (240, 230, 212) if col == (150, 90, 20) else (238, 222, 218))
    t = Image.open(f).convert("RGBA"); t.thumbnail((px - 10, px - 10), Image.LANCZOS); sheet.paste(t, (x + (px - t.size[0]) // 2, y + 2), t)
    d.text((x + 8, y + px), name, font=font(14, True), fill=(20, 30, 30)); d.text((x + 8, y + px + 19), sub, font=font(12), fill=(70, 80, 78)); d.text((x + 8, y + px + 36), kind, font=font(12, True), fill=col)
sheet.save(f"{P}/visuals/new-asset-evidence-sheet.png", optimize=True)

# ---------------------------------------------------------------- plans
COL = {"A01": "#b5533c", "A02": "#c98a4b", "A03": "#d6a15c", "A03b": "#d6a15c", "A03c": "#d6a15c", "A04": "#e3bf86", "A04b": "#e3bf86", "A05": "#a9744f", "A06": "#8f8f8a", "A07": "#7d7468", "A08": "#c7a2b8", "A09": "#b98ac0", "A11": "#8c5a3c", "A11m": "#8c5a3c"}
TILE = {"MV-Floor_UnevenBrick": "#cfc7b6", "MV-Floor_Brick": "#c2b29f", "MV-Floor_RedBrick": "#cfa58e"}
EC = {"primary": ("#d62728", 2.4), "secondary": ("#1f77b4", 1.6), "service": ("#e6a700", 1.6), "market": ("#8a4fbf", 1.3), "scenic": ("#2a9d8f", 1.6), "reserved link": ("#3a6ea5", 1.0)}


def swing_poly(x0_, x1_, n0_, n1_):
    return [LY.swing(*p) for p in ((x0_, n0_), (x1_, n0_), (x1_, n1_), (x0_, n1_))]


fig, axs = plt.subplots(1, 3, figsize=(22, 10.4), dpi=110)
base = {b[0]: b for b in LY.ALTS["B"]["buildings"]}
for ax, (key, alt) in zip(axs, LY.ALTS.items()):
    r = RES[key]; ax.set_facecolor("#dfe8cf")
    for pv in alt["paving"]:
        a, b_, c, e = pv[1:5]; fc = TILE[pv[5]]
        if alt["swing"] and c < 18:
            ax.add_patch(Polygon(swing_poly(a, b_, c, min(e, 18)), fc=fc, ec="none"))
            if e > 18: ax.add_patch(Rectangle((a, 18), b_ - a, e - 18, fc=fc, ec="none"))
        else:
            ax.add_patch(Rectangle((a, c), b_ - a, e - c, fc=fc, ec="#8a7a5a" if len(pv) > 6 else "none", lw=1.4 if len(pv) > 6 else 0))
    for bld in alt["buildings"]:
        st = "new" if bld[0] not in base else "kept" if base[bld[0]][1:6] == bld[1:6] else "changed"
        if key == "B": st = "kept"
        ax.add_patch(Polygon(LY.corners(bld), fc={"new": "#e9b949", "changed": "#c9d6e8", "kept": "#c98a6b"}[st], ec="#222", lw=0.9))
        cx, cn = sum(p[0] for p in LY.corners(bld)) / 4, sum(p[1] for p in LY.corners(bld)) / 4
        ax.text(cx, cn, f"{bld[0]}\n{bld[1]}", ha="center", va="center", fontsize=5.6, weight="bold")
    for s in alt["stalls"]:
        ax.add_patch(Rectangle((s[2] - 0.8, s[3] - 0.8), 1.6, 1.6, fc="#5b7fa8", ec="none"))
    for rw in alt["rows"]:
        ax.add_patch(Rectangle((rw[2] - 0.8, rw[3] - 4), 1.6, 8, fc="#345D80" if rw[1] == "provisions" else "#8C3E45", ec="#111", lw=0.5))
    for p, q, kind in alt["edges"]:
        k = kind.split(",")[0]; ax.plot([alt["nodes"][p][0], alt["nodes"][q][0]], [alt["nodes"][p][1], alt["nodes"][q][1]], color=EC[k][0], lw=EC[k][1] * 0.6, alpha=0.85)
    ax.set_xlim(-38, 50); ax.set_ylim(-27, 96); ax.set_aspect("equal"); ax.grid(True, color="#fff", lw=0.3, alpha=0.6)
    ax.set_title(f"{alt['title']}: {r['buildings']} buildings, envelope {r['envelope_size'][0]:g} x {r['envelope_size'][1]:g} m\nwall enclosure {r['overall_wall_pct']}%, active frontage {r['overall_active_pct']}%, "
                 f"camera fully clear on {r['camera_fully_clear']} of {r['camera_directions']} directions (massing)", fontsize=9)
    ax.set_xlabel("x east (m)"); ax.set_ylabel("n north (m); project z = -n")
fig.suptitle("Merchant Citadel P1.4 - measured layout alternatives (gold = new building, blue = re-typed, turned or moved against P1.3, terracotta = unchanged; brown outline = raised terrace)", fontsize=11)
fig.tight_layout(); fig.savefig(f"{P}/visuals/alternatives-plans.png"); plt.close(fig)

fig, ax = plt.subplots(figsize=(15, 18.5), dpi=130); ax.set_facecolor("#dfe8cf")
ax.add_patch(Rectangle((ux0 - 10, un0 - 10), ux1 - ux0 + 20, un1 - un0 + 20, fill=False, ls=(0, (6, 4)), lw=1.6, ec="#4d6b3a"))
ax.text(ux0 - 9.5, un1 + 8.2, f"Terrain support zone = (developed envelope + transport reservation) + 10 m: {ux1 - ux0 + 20:.1f} x {un1 - un0 + 20:.0f} m (assumption)", fontsize=8.5, color="#3c5a2c")
ax.add_patch(Rectangle((x0, n0), x1 - x0, n1 - n0, fill=False, ls=":", lw=1.2, ec="#555"))
for pv in L["paving"]:
    ax.add_patch(Rectangle((pv[1], pv[3]), pv[2] - pv[1], pv[4] - pv[3], fc=TILE[pv[5]], ec="#6b4a2a" if len(pv) > 6 else "none", lw=2.0 if len(pv) > 6 else 0))
for y in L["yards"]:
    ax.add_patch(Rectangle((y[1], y[3]), y[2] - y[1], y[4] - y[3], fc="#d9c7a3", ec="#a08a5c", lw=0.6, ls=":"))
for name, a, b_, c, e in L["reserved"]:
    ax.add_patch(Rectangle((a, c), b_ - a, e - c, fill=False, hatch="//", ec="#3a6ea5", lw=1.2)); ax.text((a + b_) / 2, (c + e) / 2, "RESERVED\nfuture transport\n20 x 16 m", ha="center", va="center", fontsize=8, color="#3a6ea5")
ax.add_patch(Rectangle((-6, 60), 12, 2, fc="#a99c86", ec="#6b4a2a", lw=1, hatch="|||")); ax.text(0, 59.0, "12 m steps", ha="center", fontsize=6.5)
for b in L["buildings"]:
    e = ENV.get(b["id"]); new = b["status"] == "new"
    if e:
        ax.add_patch(Rectangle((e["full_x"][0], e["full_n"][0]), e["full_x"][1] - e["full_x"][0], e["full_n"][1] - e["full_n"][0], fill=False, ls="--", lw=0.7, ec="#7a2d1c"))
    ax.add_patch(Polygon(b["corners"], fc=COL[b["archetype"]], ec="#b8860b" if new else "#2b2b2b", lw=2.6 if new else 1.1))
    cx, cn = sum(p[0] for p in b["corners"]) / 4, sum(p[1] for p in b["corners"]) / 4
    ax.text(cx, cn, f"{b['id']}\n{b['archetype']}", ha="center", va="center", fontsize=7.8, weight="bold", color="white" if b["archetype"] in ("A01", "A05", "A06", "A07", "A11", "A11m") else "#222")
    ax.plot(*b["door"], "o", color="#111", ms=3.5)
for sx in (-3, 3):
    ax.add_patch(Rectangle((sx - 1, 3), 2, 4, fc="#b98a55", ec="#3a2412", lw=1.2))
ax.add_patch(Rectangle((-1, 48), 2, 2, fc="#8C3E45", ec="#111", lw=1))
for s in L["stalls"]:
    ax.add_patch(Polygon(s["corners"], fc="#5b7fa8", ec="#111", lw=0.5))
for rw in L["rows"]:
    ax.add_patch(Polygon(rw["corners"], fc="#345D80" if rw["kit"] == "provisions" else "#8C3E45", ec="#111", lw=0.6)); ax.text(rw["x"], rw["n"], rw["id"], ha="center", va="center", fontsize=5.5, color="white", rotation=90)
for a, b_, kind in L["edges"]:
    k = kind.split(",")[0]; (xa, na, _), (xb, nb_, _) = L["nodes"][a], L["nodes"][b_]
    ax.plot([xa, xb], [na, nb_], color=EC[k][0], lw=EC[k][1], ls="--" if k in ("service", "reserved link") else "-", alpha=0.9, zorder=5)
for k, (x, n, nm) in L["nodes"].items():
    ax.plot(x, n, "o", ms=8.5, mfc="white", mec="#111", zorder=6); ax.text(x, n, k[1:], ha="center", va="center", fontsize=5.8, zorder=7)
for (xa, na), col in (((0, 0), "#b03a2e"), ((0, 20), "#b03a2e"), ((0, 37.5), "#b03a2e")):   # key sightlines to the tower
    ax.annotate("", (0, 82), (xa + 0.9, na), arrowprops=dict(arrowstyle="->", color=col, lw=0.7, ls=":"))


def dim(xa, na, xb, nb_, txt, off=(0, 0)):
    ax.annotate("", (xa, na), (xb, nb_), arrowprops=dict(arrowstyle="<->", color="#111", lw=0.9))
    ax.text((xa + xb) / 2 + off[0], (na + nb_) / 2 + off[1], txt, fontsize=7.5, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.85))


dim(-4, 13, 4, 13, "8.0 m clear", (0, 1.1)); dim(-5.05, 46.8, 5.05, 46.8, "market street 10.1 m", (0, 1.2)); dim(-14, 75.2, 14, 75.2, "civic terrace 28 x 12 m, +1.0 m", (0, -1.2))
dim(-18, 27, -14, 27, "4 m", (0, 1.1)); dim(14, 30.5, 18, 30.5, "4 m", (0, 1.1)); dim(22, 54.6, 30, 54.6, "tea lane 4 m", (0, -1.1))
dim(x0, n0 - 19, x1, n0 - 19, f"developed envelope {x1 - x0:.1f} m (E-W)", (14, -1.4)); dim(x1 + 5, n0, x1 + 5, n1, f"{n1 - n0:.0f} m (N-S)", (3.4, 0))
for t, x, n in (("D1 Gerbang Niaga", -3, -6.8), ("D2 Koridor Niaga", 0, 27.5), ("Simpang Timbangan", 0, 23.4), ("D3 Pasar Awan", 0, 38.9), ("D4 Pelataran Bursa (terrace)", 0, 70.6), ("D5 Balai Niaga Awan", 0, 88),
                ("D6 Lorong Lentera", -16, 8.2), ("D7 Jalur Gudang", 16, 8.6), ("Pelataran Gudang", 26.5, 20), ("D8 Tea Lookout", 36, 54.5), ("artisan workyard", -21, 37.2)):
    ax.text(x, n, t, ha="center", fontsize=8.2, style="italic", color="#16302b", bbox=dict(fc="#f4f1e6", ec="#16302b", lw=0.5, pad=1.5), zorder=8)
ax.add_patch(FancyArrow(x1 + 9, n1 - 4, 0, 8, width=0.6, head_width=2.6, head_length=3, color="#111")); ax.text(x1 + 9, n1 + 8.6, "N", ha="center", fontsize=13, weight="bold")
ax.plot([x0, x0 + 20], [un0 - 5, un0 - 5], color="#111", lw=3); ax.text(x0 + 10, un0 - 4.2, "20 m", ha="center", fontsize=8)
handles = ([plt.Line2D([0], [0], color=c, lw=wd_, label=k) for k, (c, wd_) in EC.items()] + [plt.Line2D([0], [0], color="#b03a2e", lw=0.8, ls=":", label="key sightline to the hall tower")]
           + [Rectangle((0, 0), 1, 1, fc=COL[a], ec="#222", label=f"{a} {ARCH[a]['name']}"[:46]) for a in ("A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A11")]
           + [Rectangle((0, 0), 1, 1, fc="#eee", ec="#b8860b", lw=2.4, label="gold outline = building not in P1.3"), Rectangle((0, 0), 1, 1, fill=False, ls="--", ec="#7a2d1c", label="measured envelope incl. roof, signs"),
              Rectangle((0, 0), 1, 1, fc="#345D80", label="awning row, provisions"), Rectangle((0, 0), 1, 1, fc="#8C3E45", label="awning row, crafts"), Rectangle((0, 0), 1, 1, fc=TILE["MV-Floor_Brick"], ec="#6b4a2a", lw=2, label="raised civic terrace")])
ax.legend(handles=handles, loc="lower right", fontsize=7.0, framealpha=0.95, title="Routes, archetypes, surfaces")
ax.set_xlim(ux0 - 14, ux1 + 15); ax.set_ylim(un0 - 14, un1 + 12); ax.set_aspect("equal"); ax.set_xlabel("x east (m)  -  project x"); ax.set_ylabel("n north (m)  -  project z = -n")
ax.set_title("Merchant Citadel / Kota Niaga Awan - P1.4 selected layout (alternative D), measured plan generated from layout data and measured envelopes", fontsize=10.5)
ax.grid(True, color="#ffffff", lw=0.4, alpha=0.6); fig.tight_layout(); fig.savefig(f"{P}/visuals/output-g-orthographic-masterplan.png"); plt.close(fig)

# ---------------------------------------------------------------- schedules and evidence
with open(f"{P}/06-building-schedule.csv", "w", newline="") as f:
    cw = csv.writer(f)
    cw.writerow("building_id,archetype_id,district,label,position_x,position_y,position_z,rotation_y_deg,footprint_width,footprint_depth,height,entrance_location_x,entrance_location_z,"
                "measured_envelope_x_min,measured_envelope_x_max,measured_envelope_z_min,measured_envelope_z_max,options,change_since_p1_3,status".split(","))
    for b in L["buildings"]:
        a = ARCH[b["archetype"]]; e = ENV[b["id"]]; o = b.get("opts", {})
        cw.writerow([b["id"], b["archetype"], b["district"], b["label"], b["x"], o.get("elev", 0.0) + (1.0 if b["archetype"] == "A01" else 0.0), -b["n"], b["rz"], a["footprint"][0], a["footprint"][1], a["height_m"],
                     round(b["door"][0], 2), round(-b["door"][1], 2), e["full_x"][0], e["full_x"][1], -e["full_n"][1], -e["full_n"][0],
                     "; ".join(f"{k}={v}" for k, v in sorted(o.items()) if k != "add") + ("; per-building extras" if o.get("add") else ""), b["status"], "PLANNED - asset-backed blockout rendered in P1.4"])
with open(f"{P}/06b-stall-and-awning-row-schedule.csv", "w", newline="") as f:
    cw = csv.writer(f); cw.writerow("id,type,kit,position_x,position_y,position_z,rotation_y_deg,footprint_width,footprint_depth,note".split(","))
    for s in L["stalls"]:
        cw.writerow([s["id"], "free stall", s["kit"], s["x"], 0.0, -s["n"], s["rz"], *L["stall_kits"][s["kit"]]["rect"], "kit as in P1.2"])
    for r in L["rows"]:
        cw.writerow([r["id"], "awning row (4 bays)", r["kit"], r["x"], 0.0, -r["n"], r["rz"], 8.2, 1.9, "A10p" if r["kit"] == "provisions" else "A10c"])
for a, b_ in ((f"{D}/validation.json", "spatial-validation-actual-geometry.json"), (f"{D}/massing/alternatives.json", "alternatives-metrics.json"), (f"{D}/tiles/p14-items.json", "new-and-rejected-items.json")):
    shutil.copyfile(a, f"{P}/asset-evidence/{b_}")
top = sorted(((U[a] * TE[a], a, U[a], TE[a]) for a in U), reverse=True)[:20]
json.dump({"revision": "P1.4", "town": {k: v for k, v in STATS.items() if k not in ("usage", "tris_each", "materials")}, "top_triangle_contributors": [{"asset_id": a, "instances": n, "triangles_each": e, "triangles": t} for t, a, n, e in top],
           "archetypes": AREP, "usage": U}, open(f"{P}/asset-evidence/usage-and-triangles.json", "w"), indent=1)
newly = sorted(a for a in U if a.split("@")[0] not in {k.split("@")[0] for k in U13})
with open(f"{P}/03b-asset-inventory-additions.csv", "w", newline="") as f:
    cw = csv.writer(f); cw.writerow("asset_id,class,source,licence,triangles_each,instances_in_p1_4,status".split(","))
    for a in newly:
        cls = "CUSTOM geometry (authored in citadel_lib.py)" if a.startswith("CUS") else "downloaded model first used in P1.4"
        src = "authored for this project" if a.startswith("CUS") else {"MV": "Quaternius Medieval Village MegaKit [Standard]", "FP": "Quaternius Fantasy Props MegaKit [Standard]", "SY": "Syntaxes of Play Medieval Cafe", "AV": "Avramania Free Collection", "SN": "Quaternius Stylized Nature MegaKit [Standard]"}[a[:2]]
        cw.writerow([a, cls, src, "n/a (custom)" if a.startswith("CUS") else "CC0 1.0", TE[a], U[a], "ASSEMBLED_IN_P1.4_BLOCKOUT"])
    for it in ITEMS:
        if it["id"].startswith("ALE"):
            cw.writerow([it["id"], "downloaded model, examined", "Alefran - Medieval Stylized Assets pack (free)", "custom licence: commercial use allowed; modification for personal use only; no redistribution", it["triangles"], 0, "NOT ADOPTED (licence unsuitable for a public web build)"])

# ---------------------------------------------------------------- numbers
ACTIONS = {"FP-Lantern_Wall": 600, "MV-Corner_Exterior_Brick": 300, "SN-CommonTree_3": 1500, "SN-CommonTree_1": 1500, "FP-FarmCrate_Apple": 600, "FP-FarmCrate_Carrot": 600, "SN-Bush_Common_Flowers": 500,
           "MV-Door_8_Round": 400, "FP-Crate_Wooden": 230, "MV-Balcony_Simple_Straight": 132, "FP-Stall_Cart_Empty": 1500, "FP-Barrel": 300, "FP-Bag": 300, "SN-TwistedTree_2": 3000, "FP-Barrel_Apples": 700,
           "FP-Dummy": 900, "AV-mdvl_food_cabbage_01": 300, "AV-mdvl_food_cheese_wheel_01": 300, "AV-mdvl_village_window_box_01": 400, "AV-mdvl_food_grain_sack_01": 350, "AV-mdvl_food_ham_01": 300,
           "AV-mdvl_food_fish_01": 250, "AV-mdvl_village_well_01": 600, "FP-Table_Large": 400, "MV-Roof_Tower_RoundTiles": 2000}
TOWN_NEW = sum(n * min(TE[a], ACTIONS.get(a.split("@")[0], 10 ** 9)) for a, n in U.items())
optrows = sorted(([f"`{a}`", n, f"{TE[a]:,}", f"{n * TE[a]:,}", f"{ACTIONS[a.split('@')[0]]:,}", f"{n * (TE[a] - ACTIONS[a.split('@')[0]]):,}"] for a, n in U.items() if a.split("@")[0] in ACTIONS and TE[a] > ACTIONS[a.split("@")[0]]), key=lambda r: -int(r[5].replace(",", "")))[:12]
custom_tris = sum(n * TE[a] for a, n in U.items() if a.startswith("CUS")); custom_n = sum(n for a, n in U.items() if a.startswith("CUS"))
edges = [(a, b_, k, round(math.hypot(L["nodes"][a][0] - L["nodes"][b_][0], L["nodes"][a][1] - L["nodes"][b_][1]), 1)) for a, b_, k in L["edges"]]
built = [e for e in edges if not e[2].startswith("reserved")]; net = round(sum(e[3] for e in built), 1)
PRIM = ["N01", "N02", "N03", "N04", "N05", "N29", "N27", "N06", "N07", "N08"]
ln = lambda p, q: math.hypot(L["nodes"][p][0] - L["nodes"][q][0], L["nodes"][p][1] - L["nodes"][q][1]); prim = round(sum(ln(p, q) for p, q in zip(PRIM, PRIM[1:])), 1)
share = lambda vv: round(100 * sum(g["samples"] * g["unobstructed_pct"] / 100 for g in vv["G_camera"]) / sum(g["samples"] for g in vv["G_camera"]))
cam14 = {g["travel"]: g for g in VAL["G_camera"]}; cam13 = {g["travel"]: g for g in V13["G_camera"]}
hang = sorted([c for c in VAL["C_hanging"] if c["clearance_m"] is not None and c["over_paving"]], key=lambda c: c["clearance_m"])
worst = sorted([g for g in VAL["G_camera"] if g["unobstructed_pct"] < 100], key=lambda g: g["min_camera_distance_m"])[:12]
camrows = [[g["travel"], g["type"], f"{g['unobstructed_pct']}%", g["min_camera_distance_m"], ", ".join(b.split("_")[0] for b in g["main_blockers"][:2]) or "-",
            (f"{cam13[g['travel']]['unobstructed_pct']}% / {cam13[g['travel']]['min_camera_distance_m']}" if g["travel"] in cam13 else "new edge")] for g in worst]
primrows = [[t, f"{cam14[t]['unobstructed_pct']}%", cam14[t]["min_camera_distance_m"], ", ".join(b.split("_")[0] for b in cam14[t]["main_blockers"][:2]) or "-"] for t in [f"{p}->{q}" for p, q in zip(PRIM, PRIM[1:])]]
gaps = [[g["a"], g["b"], g["gap_m"], g["status"]] for g in VAL["B_roof_gaps_under_3m"] if g["status"] != "OK"]
drow = [[d_["edge"], d_["type"], d_["length_m"], d_["unpaved_samples"], d_["max_step_m"], d_["min_headroom_m"] if d_["min_headroom_m"] else "open sky", d_["min_side_clearance_m"], d_["status"]] for d_ in VAL["D_edges"]]
GR = list(RD["enclosure_groups"])
encrows = [[g] + [f"{RES[k]['enclosure_groups'][g][0]}% / {RES[k]['enclosure_groups'][g][1]}%" for k in ("B", "D", "E")] for g in GR] + [["**All tested edges**"] + [f"**{RES[k]['overall_wall_pct']}% / {RES[k]['overall_active_pct']}%**" for k in ("B", "D", "E")]]
STATUS = {"A01": "READY", "A02": "CONDITIONAL", "A03": "CONDITIONAL", "A03b": "READY", "A03c": "READY", "A04": "CONDITIONAL", "A04b": "CONDITIONAL", "A05": "READY", "A06": "READY", "A07": "READY", "A08": "CONDITIONAL",
          "A09": "CONDITIONAL", "A11": "READY", "A11m": "READY", "A10p": "CONDITIONAL", "A10c": "CONDITIONAL"}
WHYC = {"A02": "cafe-pack materials re-linked on export; Avramania goods", "A03": "windows mounted on the jetty face", "A04": "custom cloth awning to author", "A04b": "custom cloth awning to author", "A08": "Avramania sign and flower boxes",
        "A09": "Avramania inn sign and flower boxes", "A10p": "custom cloth awning; cafe counters; stretched posts", "A10c": "custom cloth awning; cafe counters; stretched posts"}
PURPOSE = {"A01": "Exchange Hall: taller tower with the seal on four faces, dormers, porch; stands on the terrace", "A02": "Covered market hall (two dressing kits)", "A03": "Jettied two-storey shophouse", "A03b": "Two-storey shophouse, eaves to street",
           "A03c": "Shallow two-storey merchant house", "A04": "Single-storey shop with a cloth awning", "A04b": "Single-storey shop, eaves to street, cloth awning", "A05": "Stone-based corner building with two fronts", "A06": "Stone workshop", "A07": "Guild warehouse",
           "A08": "Tea house with veranda", "A09": "**New.** Merchants' inn: 10 x 8 m, stone ground floor, balcony on posts, two dormers, two chimneys", "A11": "**New.** Corner tower house: A05 body with a three-storey corner turret standing 1 m proud of both fronts",
           "A11m": "**New.** Mirror of A11 (turret on the left)", "A10p": "**New.** Market awning row, provisions (blue)", "A10c": "**New.** Market awning row, crafts (burgundy)"}
order = ["A01", "A02", "A03", "A03b", "A03c", "A04", "A04b", "A05", "A06", "A07", "A08", "A09", "A11", "A11m", "A10p", "A10c"]
arows = []
for a in order:
    A, R = ARCH[a], AREP[a]; n_inst = arche_n.get(a, 0) if not a.startswith("A10") else sum(1 for r in L["rows"] if ("provisions" if a == "A10p" else "crafts") == r["kit"])
    used = ", ".join(b["id"] for b in L["buildings"] if b["archetype"] == a) or ", ".join(r["id"] for r in L["rows"] if ("provisions" if a == "A10p" else "crafts") == r["kit"])
    packs = sorted({k.split("-")[0] for k in R["usage"]}); src = ", ".join({"MV": "Q. Medieval Village", "FP": "Q. Fantasy Props", "SY": "SoP Medieval Cafe", "AV": "Avramania", "CUS": "custom", "SN": "Q. Nature"}[p] for p in packs)
    arows.append([a, PURPOSE[a], n_inst, used, f"{A['footprint'][0]} x {A['footprint'][1]}", A["height_m"], f"{R['instances']} / {R['unique_assets']}", f"{R['triangles']:,}", src, STATUS[a] + (f" ({WHYC[a]})" if a in WHYC else "")])
changed = [b for b in L["buildings"] if b["status"] != "kept"]
brow = [[b["id"], b["archetype"], b["label"], f"({b['x']}, {(b.get('opts') or {}).get('elev', 0.0) + (1.0 if b['archetype'] == 'A01' else 0.0)}, {-b['n']})", f"{b['rz']:g}", f"{ENV[b['id']]['full_size'][0]} x {ENV[b['id']]['full_size'][1]}", b["status"]] for b in L["buildings"]]
vis = lambda k: ", ".join(RES[k]["tower_visible_from"])
ALE = MAN.get("alefran-medieval-stylized-free", {})

# visual quality review: per output, nine criteria (score, evidence) --------------------------------
CRIT = ["Composition", "Reference interpretation", "Cohesion", "Spatial hierarchy", "Architectural quality", "Atmosphere", "Gameplay readability", "Constructibility", "Performance feasibility"]
QA = {
    "A Hero aerial": ([4, 4, 4, 4, 4, 3.5, 4, 4, 3], "Reads as one cluster with four tower and turret points, awning rows marking the market street and a raised terrace before the hall. Weak: the town still stands in an open field, and the bazaar's west and east edges are only half built (46% enclosed)."),
    "B Merchant street (gameplay camera and eye height)": ([4, 3.5, 4, 4, 4, 4, 4, 4, 3], "Junction tower house, paving seal, pennant line, cloth awnings and the hall on its terrace as the destination. Weak: the 6.6 m camera still shows more roof than shopfront on the nearest buildings; the frontage itself is unchanged from P1.3 (71% enclosed)."),
    "C Central bazaar": ([4.5, 4, 3.5, 4.5, 4, 4.5, 4, 4, 3], "Three clear layers: goods and striped awning rows, the two halls, then tower houses and the hall. A 10 m market street with a cross-passage is immediately legible. Weak: the awning cloth is flat-coloured custom geometry beside hand-painted kit textures; the plaza floor is still one cobble tile."),
    "D Exchange Hall and civic terrace": ([4, 3.5, 4, 4.5, 4, 3.5, 4, 4, 3], "Hierarchy now comes from level (terrace +1 m, podium +2 m), a 12 m flight of steps, guild standards, a taller tower with a seal on each face and dormers. Weak: still assembled from house modules, so the stone-and-timber detail is that of a large house; R08 and R09 could not be located, so their specifics were not studied."),
    "E Secondary street (service court, artisan lane)": ([3.5, 3, 4, 4, 3.5, 3.5, 3.5, 4, 3.5], "Unchanged in form from P1.3 except two workshops turned 6 degrees. Honest position: P1.4 put its effort into the bazaar, hall and street; the secondary quarters gained least. R10 images were not viewed."),
    "F Tea lookout": ([3.5, 3.5, 4, 3.5, 3.5, 3.5, 4, 4, 4], "Tea house turned 18 degrees to face the lookout corner, veranda on posts, lamp on the lane, laid tables, red tree. Weak against R11: no wrap-around deck or level change, and without terrain there is nothing to look out over yet."),
}
qrows = [[k] + [f"{s:g}" for s in v[0]] + [f"**{sum(v[0]) / len(v[0]):.2f}**"] for k, v in QA.items()]
qavg = sum(sum(v[0]) / len(v[0]) for v in QA.values()) / len(QA)

# =============================================================================================== documents
w("README.md", f"""
# Merchant Citadel / Kota Niaga Awan - P1.4 planning package

**Status: MERCHANT CITADEL P1.4 - PENDING HUMAN VISUAL APPROVAL.** Planning and Blender concept only. Dated {DATE}. P2 has not started.

P1.4 is a creative redesign on the P1.3 foundation. The street network of P1.3 is kept; what changed is what stands on it and how it is composed:
a raised civic terrace with a 12 m flight of steps, a taller Exchange Hall tower, three corner tower houses, a merchants' inn, two more bazaar-edge shops,
a market street lined by four striped awning rows in place of scattered stalls, cloth awnings and pennant lines, and six buildings turned off the grid.
**{nb} buildings** (22 in P1.3). No asset was adopted from a new source; one new pack was downloaded, examined and rejected on its licence.

This folder is separate from `../p1.3/` and `../p1/`, which are unchanged.

| # | Deliverable | File |
|---|---|---|
| 1 | Revised town design bible | [01-town-design-bible.md](01-town-design-bible.md) |
| 2 | Visual reference board R01-R11 and traceability | [02-visual-reference-board.md](02-visual-reference-board.md) |
| 3 | Updated external asset inventory | [03-asset-inventory-update.md](03-asset-inventory-update.md), [03b-asset-inventory-additions.csv](03b-asset-inventory-additions.csv) |
| 4 | Evidence of newly verified models | [new-asset-evidence-sheet.png](visuals/new-asset-evidence-sheet.png) |
| 5 | Alternative layout studies | [04-layout-alternatives.md](04-layout-alternatives.md), [alternatives-plans.png](visuals/alternatives-plans.png), [alternatives-massing.jpg](visuals/alternatives-massing.jpg) |
| 6 | Selected measured masterplan | [05-selected-masterplan.md](05-selected-masterplan.md), [OUTPUT G](visuals/output-g-orthographic-masterplan.png) |
| 7 | Building schedule | [06-building-schedule.csv](06-building-schedule.csv), [06b-stall-and-awning-row-schedule.csv](06b-stall-and-awning-row-schedule.csv) |
| 8 | Archetype and construction specifications | [07-archetype-construction-specifications.md](07-archetype-construction-specifications.md) |
| 9 | Seven visual outputs | [A](visuals/output-a-hero-aerial.png), [B](visuals/output-b-merchant-street-gameplay.png) / [B2](visuals/output-b2-merchant-street-eye.png), [C](visuals/output-c-central-bazaar.png) / [C2](visuals/output-c2-central-bazaar-eye.png), [D](visuals/output-d-exchange-hall.png), [E](visuals/output-e-secondary-service-court.png) / [E2](visuals/output-e2-secondary-artisan-lane.png), [F](visuals/output-f-tea-lookout.png), [G](visuals/output-g-orthographic-masterplan.png); experiment: [bazaar from the terrace](visuals/experiment-bazaar-from-terrace.jpg) |
| 10 | Before/after comparison and visual quality review | [08-before-after-and-visual-review.md](08-before-after-and-visual-review.md) |
| 11 | Spatial and camera validation | [09-spatial-camera-validation.md](09-spatial-camera-validation.md) |
| 12 | Technical feasibility and optimisation | [10-technical-feasibility-optimisation.md](10-technical-feasibility-optimisation.md) |
| 13 | Town-first terrain support contract | [11-terrain-support-contract.md](11-terrain-support-contract.md) |
| 14 | P2 construction contract | [12-p2-construction-contract.md](12-p2-construction-contract.md) |
| 15 | Remaining decisions and risks | [13-decisions-and-risks.md](13-decisions-and-risks.md) |

Evidence classes: outputs A-F and the archetype tiles are ASSET-BACKED BLENDER BLOCKOUT; the alternatives massing is boxes and prisms at module dimensions; plans are drawings generated from the layout data.
No illustrative concept image and no AI-generated image is included. No image from any reference is reproduced in this package.

## Reproduce

```bash
D=.asset-inspection/merchant-citadel-p1; S=docs/planning/merchant-citadel/p1.4/blender-inspection; B="/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --disable-autoexec"
python3 $S/town_data.py $D/p1.4/data
$B --python $S/render_archetypes.py -- $D/extracted $D/measurements.json $D/p1.4/data/archetypes.json $D/p1.4/archetypes
$B --python $S/massing_p14.py -- $D/p1.4/data/archetypes.json $D/p1.4/massing
$B --python $S/build_town.py -- $D/extracted $D/measurements.json $D/p1.4/data $D/p1.4/renders $D/p1.4/merchant-citadel-p1.4-blockout.blend
$B --python $S/validate_envelopes.py -- $D/p1.4/merchant-citadel-p1.4-blockout.blend $D/p1.4/data $D/p1.4/validation.json
$B --python $S/inspect_p14.py -- $D/extracted $D/measurements.json $D/p1.4/tiles
python3 $S/make_p14_package.py $D docs/planning/merchant-citadel/p1.4
```
""")

w("01-town-design-bible.md", f"""
# 01 - Town design bible (P1.4): The City of a Thousand Trades

## What the visitor meets

Two shopfronts flank the arrival court; the gate lodges frame a street of jetties, awnings and painted signs. At mid-length a **tower house** stands on the corner
of a cross street and the guild seal is set in the paving. The street opens into the bazaar, which is now a **market street**: two rows of striped awnings on each
side, blue for provisions and burgundy for crafts, under lines of pennants strung between the market halls, with the market cross at the centre. At the far end a
**flight of steps twelve metres wide** climbs to the civic terrace between two more tower houses, and the Exchange Hall stands above it, its tower carrying the
seal on all four faces. An inn with a balcony overlooks the market from the west. Lanes lead to workshops, a service court and a tea house turned to face the edge.

## Design moves and the reason for each

| Move | Improves | Why |
|---|---|---|
| Civic court raised 1 m as a terrace, hall podium 1 m above that | Landmark hierarchy, spatial coherence | Level is the one means of emphasis the earlier revisions never used. The hall now dominates by standing higher, not by being bigger |
| 12 m steps with guild standards and tower houses either side | Hierarchy, navigation | A ceremonial threshold between commerce and institution; visible from the gate |
| Hall tower one storey taller, seal on four faces, dormers | Architectural identity | The tower is the town's clock-face landmark from every side, including the lanes |
| Three corner tower houses (junction, terrace west, terrace east) | Silhouette, corner quality | P1.3 used the plain corner building four times; corners were its weakest buildings. With the hall tower, turrets give the skyline four vertical accents where P1.3 had one |
| Bazaar stalls replaced by four 8 m awning rows forming a 10 m market street | Market organisation, storytelling | The plaza was an open rectangle with stalls in it. Rows make a street inside the square, leave the cross-passage and the halls readable, and group trades by colour |
| Merchants' inn on the bazaar's west edge; two more edge shops | Enclosure, commercial identity | A new function and a balcony overlooking the market; bazaar edge enclosure rises from 38% to 46% |
| Cloth awnings on single-storey shops; pennant lines over the street and the market | Atmosphere, commercial identity | Trade shows itself in cloth. Three colours only |
| Six buildings turned 6-18 degrees off the grid | Visual quality | Small departures at the edges of the town (gateway shop, workshops, edge shops, tea house) break the grid without disturbing the validated streets |
| Guild seal inlaid at the junction and on the terrace | Navigation, identity | Marks the two decision points on the axis |

## What did not change, deliberately

The street network, lane positions, hall positions, service court, workyard and tea lane are those of P1.3, which were validated and which the references do not argue against.
The palette, seal, trade signs and goods are those of P1.2. No building was removed.

## Districts

| District | Composition in P1.4 |
|---|---|
| D1 Gerbang Niaga | Court between a single-storey shop turned 12 degrees to open the funnel and a shallow two-storey house; lodges; the tower of the junction house in view |
| D2 Koridor Niaga | Jettied houses, canopies, cloth awnings; gate arches in the two closed gaps; pennant line; paving seal at the junction; tower house on the corner |
| D3 Pasar Awan | Market street between four awning rows; cross-passage; two halls; inn, perimeter shops and registry on the edges; pennant lines from hall to hall |
| D4 Pelataran Bursa | Terrace 28 x 12 m at +1.0 m; steps, balustrade, standards, benches, seal; no stalls |
| D5 Balai Niaga Awan | Hall on a podium at +2.0 m; porch, dormers, tower to {ARCH['A01']['height_m'] + 1:.1f} m above the bazaar |
| D6 Lorong Lentera | Lane of workshops turned slightly to each other; workyard with well |
| D7 Jalur Gudang | Warehouse and counting house across the service court |
| D8 Tea Lookout | Tea lane with lamp, terrace with laid tables, tea house turned 18 degrees towards the corner of the lookout |
""")

REFS = [
    ("R01", "Medieval Kingdom (beffio), Behance, 2018; a paid Unity art pack", "behance.net/gallery/83167111/Medieval-Kingdom", "**Viewed** (aerial stills)",
     "A tight cluster seen from above at night; steep roofs at several heights; slender towers and turrets punctuate the mass; lanes thread between buildings; one stylised material throughout",
     "Punctuate the skyline: three corner tower houses and a taller hall tower. Keep the P1.3 density. Do not let lighting carry the image (daylight only)", "A11 / A11m (verified Quaternius modules), A01 tower", "OUTPUT A; envelopes of B04, B15, B16 in 06"),
    ("R02", "Stylized Medieval Village - isometric environment concept", "not found under this title", "**Not located.** Principles are the brief's own list",
     "(from the brief) readable silhouette, clear zoning, compact groups, recognisable circulation from above", "District legibility from above by roof value (civic dark), ground material (brick terrace, red-brick lane, cobble) and awning colour by trade side",
     "MI_RoundTiles@dark variant; three paving tiles; awning rows", "OUTPUT A, OUTPUT G"),
    ("R03", "Stylized 3D Environment - Medieval Street, Jeokjone", "not found", "**Not located.** Principles are the brief's own list",
     "(from the brief) layered facades, shopfront proportion, pedestrian perspective, a destination", "Five shopfront types on one street (jetty, timber canopy, cloth awning, tower house, shallow house); judged at the gameplay camera and at eye height",
     "A03, A03b, A03c, A04, A04b, A11", "OUTPUT B and B2; edges N02-N03, N03-N04 in 09"),
    ("R04", "Stylised Street Market Oasis (UE4), Louis J. Sullivan, ArtStation", "artstation.com/artwork/BmqgPD; UE4 project on itch.io with no licence stated", "**Viewed** (hero image)",
     "Cloth canopies stretched overhead between buildings; crates and baskets layered in the foreground; a winding street opening to a plaza; saturated warm and violet palette",
     "Cloth overhead and at shopfronts: awnings and pennant lines. Goods grouped at the fronts. Not adopted: the regional architecture and the saturated palette. Its downloadable project is not used (no licence)",
     "CUS-Awning (custom), CUS-Bunting (custom), existing goods", "OUTPUT B, C2; hanging clearances in 09"),
    ("R05", "Fantasy Town Market, Cyril Yong Zhou", "piece not found; a Creative Bloq article on his Blender-and-Photoshop workflow exists but its text could not be read", "**Not located.** Principles are the brief's own list",
     "(from the brief) foreground goods, middle-ground halls and walking space, background buildings and landmark", "Three depth layers in the bazaar views: awning rows and goods, halls, tower houses and hall",
     "A10p, A10c, A02, A11, A01", "OUTPUT C, C2"),
    ("R06", "Stylized Medieval Market, StylArts / Leartes Studios; showcase scene by Kristina Nakic after a concept by Darya Suvorava; a paid pack", "80.lv article 'Medieval Market: a detailed guide on stylized environment art'", "**Viewed** (hero image) and the artist's breakdown read",
     "A street funnels to a clock tower; bunting crosses between buildings; awnings; five house variants built from about 130 pieces sharing one design language; warm low sun with bluish sky fill",
     "Tower as terminus with a clock-like roundel (the seal on four faces); pennant lines; variation by recombining one kit (16 assemblies from one module set). Lighting was already of this kind",
     "A01 v2, CUS-Bunting, CUS-Seal", "OUTPUT C2, D; experiment view"),
    ("R07", "Dungeon Defenders II - Trading Hub, Xbox Wire", "news.xbox.com 'Protean Shift Expansion' (2018-06-27) mentions Player Shops and Markets but describes no layout", "**Located, images not viewed.** Principles are the brief's own list",
     "(from the brief) stalls organised round a public space, clear paths, colour grouping, framing entrance", "A 10.1 m market street between stall rows with a 2.8 m cross-passage; blue = provisions (west), burgundy = crafts (east)",
     "A10p, A10c", "Clear corridors in town_data.py; edges N04-N05-N27-N06 in 09"),
    ("R08", "Stylized Guild Hall Environment, ArtStation", "not found under this title", "**Not located.** Principles are the brief's own list",
     "(from the brief) identity from massing, roof articulation, entrance, tower, civic frontage, insignia", "Hall emphasis by level, steps, taller tower, dormers and seal; no palace or fortress ornament added",
     "A01 v2, TERRACE (stairs, skirt, balustrade modules)", "OUTPUT D; stairs and terrace edges in 09"),
    ("R09", "Adventurers' Guild - Kickback Kingdom", "not found", "**Not located.** Principles are the brief's own list",
     "(from the brief) prominent entrance, hierarchy of roof, entrance and ornament, banners that state the role", "Ceremonial approach: steps, two guild standards at their head, tower houses framing; guild banners only on guild buildings",
     "FP-Banner_2@burgundy on stretched posts, A11", "OUTPUT D"),
    ("R10", "Lineage W - Giran, NCSoft", "about.ncsoft.com article on Giran's characters; no environment description", "**Located, images not viewed.** Principles are the brief's own list",
     "(from the brief) dense merchant streets, secondary public spaces, multi-directional exploration", "Secondary quarters keep the P1.3 spaces (service court, pocket court, workyard); workshops turned to each other. Least-changed area of P1.4",
     "A06, A07, A05", "OUTPUT E, E2"),
    ("R11", "Mergo's Tea House: concept by Oscar Molin; 3D recreation thread by 'screenshotrian' on Polycount (assumed to be Rian Kessler)", "artstation.com/artwork/0l32qe", "**Concept viewed**; the Polycount thread could not be read (HTTP 403)",
     "A tea house perched at an edge on a stilted wrap-around deck; steep pointed roofs; lantern posts along the approach; autumn trees", "Tea house turned 18 degrees to the lookout corner; veranda on posts; a lamp on the lane; a red tree beside. Not adopted: pointed blue roofs and the whimsical tower, which would leave the town's language",
     "A08, lamp, SN-TwistedTree_2, cafe furniture", "OUTPUT F; edges N24-N41-N16-N17 in 09"),
]
w("02-visual-reference-board.md", f"""
# 02 - Visual reference board R01-R11 and traceability

**How the references were studied, stated plainly.** The brief named eleven references without links. Each was searched for by title and author.
Four were found and **looked at** in a browser (R01, R04, R06, R11). Two more were found but only as text that does not describe the scene (R07, R10).
Five could not be found under the given title (R02, R03, R05, R08, R09); for those the principles below are the brief's own "what to study" list, and no claim is made that the image was seen.
Visual references authorise nothing: no model, texture or image from any of them is used or reproduced, and several are paid products.

## Traceability: reference to design decision to assets to evidence to validation

""" + tbl(["Ref", "Reference", "Status", "Principle taken", "Design decision in Merchant Citadel", "Actual 3D assets", "Evidence and validation"],
          [[r[0], f"{r[1]} ({r[2]})", r[3], r[4], r[5], r[6], r[7]] for r in REFS]) + f"""
## What the four viewed references changed

1. **R06** showed a market street closed by a tower and crossed by bunting. That is the P1.4 bazaar: awning rows, pennants, and the hall tower with a roundel on every face.
2. **R01** showed that a dense stylised town reads through its vertical accents. P1.3 had one (the hall tower); P1.4 has four (the hall tower and three turrets).
3. **R04** showed cloth doing the work of commercial atmosphere overhead and at the fronts. Awnings and pennants are the only new colour in P1.4.
4. **R11** showed a tea house composed towards its view. The tea house was turned; the wrap-around deck and the level change were not built (no terrain yet).

## Deliberately not taken

Night lighting (R01), regional architecture and saturated violet (R04), a Ghibli-style painted finish (R06), pointed whimsical roofs (R11). Each would either hide architecture or leave the kit's language.
""")

w("03-asset-inventory-update.md", f"""
# 03 - External asset inventory update (P1.4)

The P1.2 inventory (918 inspected models, hashes and licences in `../p1/02`, `../p1/03`, `../p1/04`) remains the base. P1.4 changes it as follows.
Evidence: [new-asset-evidence-sheet.png](visuals/new-asset-evidence-sheet.png); list: [03b-asset-inventory-additions.csv](03b-asset-inventory-additions.csv).

## Sources examined in P1.4

| Source | What was done | Result |
|---|---|---|
| Alefran - Medieval Stylized Assets pack (free), alefrandev.itch.io | Downloaded from the creator's free path ({ALE.get('bytes', 0):,} bytes, SHA-256 `{ALE.get('sha256', '')[:16]}...`), 33 glTF models extracted, licence file read, five models imported and measured | **Not adopted.** Textured and close in style, with a street lamp, a stall and a sign that the town lacks. But `Free version license.txt` allows commercial use while limiting modification to personal use and forbidding redistribution "even if modified". A public browser game serves its model files and P2 must optimise them, so the terms do not fit. The street lamp alone is a 34 MB file |
| WizP - Stylized Medieval Village, itch.io | Page read (CC0 stated, with a contradictory "can't be resold" line; three palette materials); download attempted | **Not obtained.** The free path listed no upload. Flat palette style, so it would not have suited the architecture |
| skfod - Stylized Medieval Market, itch.io | Page read | **Rejected unseen:** CC BY-ND and a minimum price |
| KayKit Medieval Hexagon | Page read | **Rejected unseen:** hex-tile strategy miniatures, the same family as the Medieval Builder Pack measured in P1.2 (buildings about 1 m tall) |
| Louis J. Sullivan - Stylised Street Market (UE4 project), itch.io | Page read (it is reference R04) | **Not usable as assets:** no licence stated; Unreal project format |
| Quaternius, other packs | Site listing checked | No further fantasy-town pack; the three MegaKits already in use are the relevant ones |

**Conclusion of the search:** no free, clearly licensed pack offers architecture or street furniture in a style that sits beside the Quaternius kit. The gain in P1.4 comes from the kit's own unused modules and from five small custom elements.

## Downloaded models first used in P1.4 ({len([a for a in newly if not a.startswith('CUS')])})

{", ".join(f"`{a}`" for a in newly if not a.startswith("CUS"))}

All are from packs already verified (CC0). The roof `8x10`, the cross-braced balustrade and the plinth use of the stair skirt are the notable ones.

## Custom geometry (authored for this project, not downloaded)

| Item | What it is | Triangles each | Placed |
|---|---|---|---|
""" + "\n".join(f"| `{a}` | {('striped cloth awning bay, 2 m' if 'Awning' in a else 'line of pennants' if 'Bunting' in a else 'guild seal inlaid in the paving, 3.2 m' if 'Paving' in a else 'guild seal' if 'Seal' in a else 'hanging trade sign')} | {TE[a]} | {U[a]} |" for a in sorted(U) if a.startswith("CUS")) + f"""

{custom_n} placements, {custom_tris:,} triangles in total ({100 * custom_tris / STATS['triangles']:.1f}% of the town). New in P1.4: the awning, the pennant line and the paving seal. Flat colours from the palette; no texture.

## Multi-source coherence

Architecture, roofs, paving, lamps and fences: Quaternius only. Counters, tables and goods: Syntaxes of Play and Avramania (as P1.2). Cloth and signs: custom, flat-coloured.
The weakest join is the custom cloth beside hand-painted textures; it is acceptable at street distance and should receive a woven texture in P2 (13).
""")

altrow = lambda k: [RES[k]["title"], RES[k]["buildings"], RES[k]["new_buildings"], RES[k]["re_typed"], f"{RES[k]['free_stalls']} + {RES[k]['awning_rows']} rows", f"{RES[k]['envelope_size'][0]:g} x {RES[k]['envelope_size'][1]:g}", f"{RES[k]['coverage_pct']}%",
                    f"{RES[k]['overall_wall_pct']}% / {RES[k]['overall_active_pct']}%", f"{RES[k]['camera_fully_clear']} of {RES[k]['camera_directions']}", f"{RES[k]['camera_secondary_mean_clear_pct']}%", len(RES[k]["tower_visible_from"]), f"{RES[k]['building_triangles']:,}"]
w("04-layout-alternatives.md", f"""
# 04 - Alternative layout studies

Plans: [alternatives-plans.png](visuals/alternatives-plans.png). Massing from one camera: [alternatives-massing.jpg](visuals/alternatives-massing.jpg). Data: `layouts_p14.py`; measurements: `asset-evidence/alternatives-metrics.json`.
Footprints are oriented rectangles from the archetype data; massing is boxes and roof prisms at module dimensions.

| | B - P1.3 selected | D - Terraced Citadel | E - Crooked Spine |
|---|---|---|---|
| Idea | Baseline | Keep the validated streets; add level, vertical accents, a market street, an inn and edge shops; turn edge buildings off the grid | D, with the whole southern quarter swung 14 degrees about the junction so the street bends and the hall is revealed at the corner |
| Street geometry | Straight axis | Straight axis | Dog-leg at Simpang Timbangan |
| Court | 28 m, level | Terrace at +1 m, 12 m steps | as D |
| Bazaar | 12 free stalls | 4 awning rows + 4 free stalls | as D |

{tbl(["Layout", "Buildings", "New", "Re-typed", "Stalls", "Envelope (m)", "Covered", "Enclosed / active edges", "Camera fully clear (massing)", "Secondary routes, mean clear", "Tower visible from (of 15)", "Building triangles (estimate)"], [altrow("B"), altrow("D"), altrow("E")])}
Enclosure by place (wall / active):

{tbl(["Place", "B", "D", "E"], encrows)}
## Selection: D

- **D against B.** Enclosure rises from {RB['overall_wall_pct']}% to {RD['overall_wall_pct']}% and the bazaar edge from {RB['enclosure_groups']['Bazaar'][0]}% to {RD['enclosure_groups']['Bazaar'][0]}%. The civic "active" figure falls to 0 because the tower houses now face the bazaar, not the terrace; that is intended (a terrace has no shop doors on it).
  The cost is in the camera test: {RD['camera_fully_clear']} of {RD['camera_directions']} directions fully clear against {RB['camera_fully_clear']} of {RB['camera_directions']}.
- **E against D.** The bend is the more characterful plan from above and gives a reveal at the junction. Measured, it loses: lane enclosure falls (artisan {RD['enclosure_groups']['Artisan lane'][0]}% to {RE['enclosure_groups']['Artisan lane'][0]}%, warehouse {RD['enclosure_groups']['Warehouse lane'][0]}% to {RE['enclosure_groups']['Warehouse lane'][0]}%), one workshop has no room on the inside of the bend, the camera test is worse again ({RE['camera_fully_clear']} of {RE['camera_directions']}), and the warehouse swings away from the service court it was placed to enclose.
  The tower stays visible from the same {len(RE['tower_visible_from'])} points, so the bend does not cost the landmark.
- **E is not dismissed.** If the owner prefers a bent street, the south-west quarter needs re-planning (workshop positions, the cross lane) and the whole southern quarter needs re-validating. E was measured as massing only and has not been built with assets.

D is selected because it delivers the visible changes (level, skyline, market street) on streets that are already validated, and because the one thing E adds is bought with losses in the secondary quarters that the brief asks to strengthen.
""")

w("05-selected-masterplan.md", f"""
# 05 - Selected measured masterplan (P1.4, alternative D)

Drawing: [OUTPUT G](visuals/output-g-orthographic-masterplan.png). Data: `layouts_p14.py`, `town_data.py`. Metres; origin = centre of the arrival court; plan x = east, n = north; project (x, y, z) = (x, elevation, -n).
`rotation_y`: 0 = front faces south, 90 = east, -90 = west; any angle is allowed, and footprints are oriented rectangles.

Developed envelope: x {x0}..{x1} ({x1 - x0:.1f} m), z {-n1}..{-n0} ({n1 - n0:.0f} m). P1.3 was 70.5 x 98 m; the inn adds 2 m on the west.

**{nb} permanent buildings, {len(arche_n)} building archetypes in use, {nr} awning rows (16 bays), {ns} free stalls, split gateway, market cross, civic terrace.**

## Levels

| Surface | Elevation | Reached by |
|---|---|---|
| Streets, lanes, bazaar, lookout | y = 0 | - |
| Civic terrace, x -14..14, z -74..-62 | y = +1.0 | Steps 12 m wide at z = -60..-62 (five risers, modules `Stairs_Exterior_Straight_L / _Center / _R`) |
| Exchange Hall podium | y = +2.0 | Hall steps 10 m wide from the terrace (unchanged modules) |

## Public spaces and street widths

| Space | Size | Note |
|---|---|---|
| Merchant street | 10 m between facades, 8 m clear | unchanged |
| Market street in the bazaar | 10.1 m between awning-row fronts; 2.8 m cross-passage; 2.45 m back lanes between rows and halls | new |
| Bazaar plaza | 44 x 26 m | unchanged outline |
| Civic terrace | 28 x 12 m, +1.0 m | raised |
| Lanes, cross street, tea lane | 4 m | unchanged |
| Pocket court, workyard, service court, lookout terrace | 8 x 6, 6 x 4, 14 x 8, 12 x 10 m | unchanged |

## Building positions

{tbl(["ID", "Archetype", "Name", "Position (x, y, z)", "rotation_y", "Measured envelope (m)", "Change since P1.3"], brow)}
{len(changed)} of {nb} are new, re-typed, turned or moved against P1.3; {nb - len(changed)} are unchanged. Nothing was deleted. Full figures: [06-building-schedule.csv](06-building-schedule.csv).

## Key sightlines (drawn on the plan)

Arrival court, street junction and bazaar entrance to the hall tower: all clear in the massing test (04). Tower visible from {len(RD['tower_visible_from'])} of 15 tested points: {vis('D')}.
""")

w("07-archetype-construction-specifications.md", f"""
# 07 - Archetype and construction specifications (P1.4)

Sheet with renders: [new-asset-evidence-sheet.png](visuals/new-asset-evidence-sheet.png). Module lists, facade strings and collision notes of the unchanged archetypes are in `../p1/08` and `../p1.3/07`.
The data that builds every assembly is `blender-inspection/town_data.py`; exact module ids and counts per assembly are in `asset-evidence/usage-and-triangles.json`.

{tbl(["ID", "Purpose", "Instances", "Used by", "Footprint (m)", "Height (m)", "Module instances / ids", "Triangles each", "Sources", "Readiness"], arows)}
## New and changed assemblies

| Assembly | Construction | Collision | Acceptance |
|---|---|---|---|
| **A01 Exchange Hall v2** | As P1.2, plus: tower walls on levels 4-6 (was 4-5), middle level plain with a 2.3 m seal on each face, top level with round windows; two dormers on the front slope; a plinth row of stair-skirt panels 1 m below the podium on the sides and back, because the hall now stands on the terrace | Boxes as before, raised 1 m; plinth 28 x 16 x 2 | Tower reads from the gate; no gap under the podium at the sides and back |
| **A09 Merchants' Inn** | Body 10 x 8, two storeys, stone ground floor (`srors` / `RORGR`), roof `Roof_RoundTiles_8x10` with the ridge along the frontage; balcony of three dark-wood floor tiles and five rail pieces on four posts; two dormers, two chimneys; cup sign, hanging inn sign, two flower boxes, two lanterns | One box 10 x 8 x 6; four post proxies | Balcony posts clear the side lane by 1.4 m; nothing below 2.1 m over paving |
| **A11 / A11m Corner Tower House** | A05 body (8 x 8, two storeys, stone ground floor) with one corner post omitted; turret 4 x 4, three storeys (`Ss` / `PR` / `RR` on the two outer faces), centred 3 m out on both axes so it stands 1 m proud of both fronts; roof `Roof_Tower_RoundTiles`. A11m is the mirror | One box 8 x 8 x 6 plus one 4 x 4 x 9 | Turret roof rises clear of the body roof; projection 1 m, leaving 3 m of the cross street at the junction |
| **A10p / A10c Market Awning Row** | 8 m long: three front posts (2.46 m) and three back posts (3.2 m), all `Corner_Exterior_Wood` scaled in height; four custom awning bays fixed to the back rail; two cafe counters and one table beneath; goods of one trade | Six post proxies; counters as two boxes | Customers' side clear; front edge of the cloth 2.3 m above paving; cross-passage 2.8 m between rows |
| **Civic terrace** | 84 brick tiles at +1.0 m; six stair modules; skirt panels on the front (not behind the steps) and sides; eight cross-braced balustrade pieces. Hollow in the blockout with a temporary dark fill | One box 28 x 12 x 1; steps as five 0.2 m treads or a ramp proxy | Top riser is the deck edge (0.18 m); no visible void |
| **A04, A04b** | Timber canopy replaced by two or three custom cloth awning bays | unchanged | Valance 2.18 m above paving |
| **Gate arches** | One `Wall_Arch` in each of the two closed street gaps | Two post proxies | Not a route |

## Custom elements: construction strategy for P2

| Element | Blockout | P2 |
|---|---|---|
| Cloth awning bay | 48 triangles, flat colours, two-sided | One mesh with a woven cloth texture and vertex-coloured stripes; three colourways as material instances |
| Pennant line | 42-76 triangles | One instanced pennant along a curve, or keep as a single mesh per length |
| Paving seal | 266 triangles, 3 cm proud | A decal or a texture on one paving plane |
| Seal, trade signs | as P1.2 | as P1.2 |
""")

w("08-before-after-and-visual-review.md", f"""
# 08 - Before/after comparison and visual quality review

Pairs from the same cameras and light: [A aerial](visuals/before-after-a-hero-aerial.jpg), [B merchant street](visuals/before-after-b-merchant-street-gameplay.jpg), [B2 street at eye height](visuals/before-after-b2-merchant-street-eye.jpg),
[C bazaar](visuals/before-after-c-central-bazaar.jpg), [D Exchange Hall](visuals/before-after-d-exchange-hall.jpg), [E service court](visuals/before-after-e-secondary-service-court.jpg), [E2 artisan lane](visuals/before-after-e2-secondary-artisan-lane.jpg), [F tea route](visuals/before-after-f-tea-lookout.jpg).

## What changed, measured

| Measure | P1.3 | P1.4 |
|---|---|---|
| Permanent buildings | 22 | **{nb}** |
| Building archetypes in use | 11 | {len(arche_n)} |
| Vertical accents on the skyline (towers, turrets) | 1 | 4 (hall tower and three turrets) |
| Levels | 2 (ground, podium +1) | 3 (ground, terrace +1, podium +2) |
| Highest point above the bazaar | 22.8 m | {ARCH['A01']['height_m'] + 1:.1f} m |
| Bazaar: free stalls / awning rows | 12 / 0 | {ns} / {nr} (16 bays) |
| Bazaar edge enclosed / active | {RB['enclosure_groups']['Bazaar'][0]}% / {RB['enclosure_groups']['Bazaar'][1]}% | {RD['enclosure_groups']['Bazaar'][0]}% / {RD['enclosure_groups']['Bazaar'][1]}% |
| All tested edges enclosed / active | {RB['overall_wall_pct']}% / {RB['overall_active_pct']}% | {RD['overall_wall_pct']}% / {RD['overall_active_pct']}% |
| Buildings off the grid | 0 | 6 (6 to 18 degrees) |
| Developed envelope | 70.5 x 98 m | {x1 - x0:.1f} x {n1 - n0:.0f} m |
| Triangles, unoptimised | {S13['triangles']:,} | {STATS['triangles']:,} ({100 * (STATS['triangles'] - S13['triangles']) / S13['triangles']:+.0f}%) |
| Camera: directions fully clear / share of all samples clear | {SUM13['camera_edges_fully_clear']} of {SUM13['camera_travel_directions']} / {share(V13)}% | {SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']} / {share(VAL)}% |

## View by view

| View | Changed in form | Not changed, or weaker |
|---|---|---|
| Aerial | Turrets at the junction and both terrace corners; awning rows draw a street through the bazaar; the terrace reads as a platform before the hall; the inn closes the west edge | Still an open field around the town; lanes as P1.3 |
| Merchant street | Tower house on the junction corner; paving seal; pennant line; cloth awnings; the hall sits visibly higher at the end | Street walls are where they were |
| Bazaar | A market street instead of scattered stalls; pennants; tower houses and steps close the north side | Plaza floor is one tile; awning cloth is flat-coloured |
| Exchange Hall | Terrace, steps, standards, taller tower with four seals, dormers | The hall's walls are unchanged |
| Secondary | Workshops turned 6 degrees | Otherwise as P1.3. **This is the area P1.4 improved least** |
| Tea lookout | Tea house turned to the view; lamp; rearranged tables | No level change, no view until terrain exists |

**Changing only light or colour would not count as redesign, and P1.4 did not change either:** light, palette and materials are those of P1.3.

## Visual quality review (internal, provisional; not an approval)

Scores are 1-5 for the nine criteria of the brief.

{tbl(["Output"] + CRIT + ["Mean"], qrows)}
""" + "\n".join(f"- **{k}.** {v[1]}" for k, v in QA.items()) + f"""

**Mean of the six outputs: {qavg:.2f} / 5.** The target is a human-reviewed 4 / 5; this internal figure is below it and is not a claim of approval.
The lowest column is performance feasibility: every image is a Blender render and the triangle count rose again.

## Where it is still generic, and the root cause

1. **Secondary quarters.** Root cause: they are built from the two plainest archetypes (workshop, warehouse) with no form of their own. More dressing would not fix that; a distinct workshop type (open-fronted, with a lean-to) would.
2. **Exchange Hall walls.** Root cause: the kit has no civic-scale module (tall windows, stone arcade). Level and tower compensate; a small set of custom civic modules would be the real fix.
3. **Cloth and painted texture side by side.** Root cause: custom cloth is untextured.
4. **No terrain.** Root cause: phase order (town first). The lookout and the aerial both wait on it.
""")

w("09-spatial-camera-validation.md", f"""
# 09 - Spatial and camera validation (P1.4 selected layout)

Method as P1.1-P1.3 (`validate_envelopes.py`): the assembled Blender scene, {VAL['triangles_tested']:,} triangles, ray casts and nearest-surface queries with constants copied from the project's controller and camera files.
The production controller and camera were not modified or run. Raw results: [asset-evidence/spatial-validation-actual-geometry.json](asset-evidence/spatial-validation-actual-geometry.json).

| Check | Result |
|---|---|
| Nominal: oriented footprint overlaps, clear corridors, paved door approaches, stalls and rows on paving, connectivity | {"PASS" if L["checks_pass"] else "FAIL"} |
| Roof and envelope gaps | {SUM['roof_gaps_fail']} failing; {SUM['roof_gaps_narrow']} narrow (0.3-1.0 m) |
| Walking edges on real geometry | **{SUM['edges_total'] - 1 - SUM['edges_fail']} of {SUM['edges_total'] - 1} built edges pass** |
| Steps | Terrace steps: largest step on N06-N07 {next(d_['max_step_m'] for d_ in VAL['D_edges'] if d_['edge'] == 'N06-N07')} m; hall steps: {VAL['E_stairs']['riser_count']} risers, largest {VAL['E_stairs']['max_riser_m']:.3f} m (limit 0.42 m) |
| Hanging objects over paving (lanterns, banners, signs, awnings, pennants, flower boxes: {len(VAL['C_hanging'])} measured) | None below 2.1 m; lowest {hang[0]['clearance_m']} m (`{hang[0]['asset']}`) |
| Market hall arch | 1.67 m wide, 2.74 m high (unchanged) |
| Follow camera | {SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']} directions fully clear; {share(VAL)}% of all samples clear |

Walking graph: {len(L['nodes'])} nodes, {len(edges)} edges, {len(edges) - len(L['nodes']) + 1} independent loops, {net} m built. Primary route {prim} m. (P1.3: 37 nodes, 47 edges, 11 loops. The terrace has one flight of steps, so the two court-side loops of P1.3 are gone.)

## Defects found by validation during P1.4 and corrected

Roofs of the terrace tower house and the north-west shop overlapping by 0.02 m; tea-route shop and cloth seller 0.14 m apart; a stone skirt panel behind the terrace steps blocking the top riser;
a lane standard on the path to the workyard. All were corrected in the layout and re-tested. A void under the terrace deck, visible behind the top step, was closed with a temporary fill.

## Narrow gaps (not failures)

{tbl(["A", "B", "Gap (m)", "Status"], gaps)}
## Every edge

{tbl(["Edge", "Type", "Length (m)", "Unpaved samples", "Largest step (m)", "Least headroom (m)", "Nearest obstacle at 1 m (m)", "Result"], drow)}
## Follow camera

| | P1.3 | P1.4 |
|---|---|---|
| Travel directions tested | {SUM13['camera_travel_directions']} | {SUM['camera_travel_directions']} |
| Fully clear | {SUM13['camera_edges_fully_clear']} ({100 * SUM13['camera_edges_fully_clear'] // SUM13['camera_travel_directions']}%) | {SUM['camera_edges_fully_clear']} ({100 * SUM['camera_edges_fully_clear'] // SUM['camera_travel_directions']}%) |
| Share of all samples with a clear camera line | {share(V13)}% | {share(VAL)}% |
| Shortest camera distance anywhere | {SUM13['camera_min_distance_m']} m | {SUM['camera_min_distance_m']} m |

**Stated plainly:** fewer travel directions are fully clear than in P1.3, although the share of the walked distance with a clear camera is the same. More things now stand near the routes (awning rows, pennant lines, turrets), so more
directions have at least one obstructed sample. Thin objects such as pennant lines are counted here and may not be in the game's camera collision set.

Primary axis, walking towards the hall:

{tbl(["Travel", "Samples clear", "Shortest camera distance (m)", "Blocked by"], primrows)}
Twelve shortest camera distances:

{tbl(["Travel", "Type", "Samples clear", "Shortest (m)", "Blocked by", "P1.3: clear / shortest"], camrows)}
The test places the camera exactly behind the direction of travel, so corners and door exits are worst cases. The inn's balcony on the west side lane ({SUM['camera_min_distance_m']} m) is the new worst case and the first candidate for adjustment if it troubles the game camera.

## Outstanding in-engine validation

Camera at the listed corners with the game's collision set and smoothing; controller on both flights of steps and on the 0.18 m deck-edge riser; whether pennants, awnings and signs collide with the camera; frame time.
""")

crows = []
def catof(a):
    b = a.split("@")[0]
    if b.startswith("MV-Floor"): return "paving"
    if b.startswith(("MV-Wall", "MV-Roof", "MV-Corner", "MV-Window", "MV-Door", "MV-Stairs", "MV-Balcony", "MV-Overhang", "MV-Prop_Chimney")): return "architecture modules"
    if b.startswith("SN-"): return "vegetation"
    if "Lantern" in b: return "lanterns"
    if b.startswith(("FP-Stall", "AV-mdvl_village_stall")): return "stall bases"
    if b.startswith("CUS"): return "custom elements"
    return "goods, furniture and street props"
def cats(usage, te):
    c = collections.Counter()
    for a, n in usage.items(): c[catof(a)] += n * te[a]
    return c
C14, C13 = cats(U, TE), cats(U13, S13["tris_each"])
crows = [[k, f"{C13[k]:,}", f"{C14[k]:,}", f"{C14[k] - C13[k]:+,}"] for k, _ in C14.most_common()]
w("10-technical-feasibility-optimisation.md", f"""
# 10 - Technical feasibility and optimisation assessment

All figures are Blender measurements of the blockout. **No browser measurement exists; no frame rate is claimed.**

| | P1.3 | P1.4 |
|---|---|---|
| Buildings | 22 | {nb} |
| Instances | {S13['instances']:,} | {STATS['instances']:,} |
| Distinct meshes | {S13['unique_assets']} | {STATS['unique_assets']} |
| Triangles, unoptimised | {S13['triangles']:,} | **{STATS['triangles']:,}** ({100 * (STATS['triangles'] - S13['triangles']) / S13['triangles']:+.0f}%) |
| Distinct materials | {len(mats13)} | {len(base_mats)} |
| Paving tiles | {S13['paving_tiles']} | {STATS['paving_tiles']} |
| After the substitutions below (projection) | 515,072 | **{TOWN_NEW:,}** |

{tbl(["Category", "P1.3", "P1.4", "Change"], crows)}
The increase is mostly architecture: two more buildings, three turrets, a taller tower, the inn's larger roof and the terrace's stair and skirt modules. The custom cloth, pennants and paving seals together are {custom_tris:,} triangles.

## Largest contributors and proposed substitutions (targets are for meshes P2 must make and measure)

{tbl(["Component", "Instances", "Triangles each", "Total now", "Target each", "Saving"], optrows)}
## Assessment by topic

| Topic | Assessment |
|---|---|
| Geometry | {STATS['triangles']:,} now; {TOWN_NEW:,} projected. The earlier 350,000 figure is not reached by substitutions; reaching it needs lower-detail wall and roof modules or fewer backdrop trees, decided on a browser measurement |
| Materials | {len(base_mats)} distinct ({len(base_mats) - len(mats13):+d} against P1.3: flat cloth, pennant and paving colours). The cafe pack's textured materials should be atlased; custom flat colours can share one palette texture |
| Draw calls | Depends on materials, not on building count, if each district is merged by material; repeated modules (wall bays, windows, piers, lanterns, awning bays) suit `InstancedMesh` |
| Texture memory | Unchanged from P1.2: architecture and nature up to 2048 px, props up to 4096 px (to be downscaled), cafe pack with normal and roughness maps |
| Visibility | The terrace and the denser bazaar hide more of the far town from any one street; a distance-based level for backdrop trees and far roofs is plausible. To be measured |
| Collision | Box proxies only: about {sum({'A01': 10, 'A02': 12, 'A08': 5, 'A09': 5, 'A11': 2, 'A11m': 2}.get(b['archetype'], 1) for b in L['buildings']) + 6 * nr + 2} boxes for buildings, rows and terrace; steps as treads or ramp proxies |
| Level of detail | Three candidates carry most of the load: lanterns, brick piers, trees |
| Two-sided cloth | Awnings and pennants are single-surface and must render double-sided; alpha is not needed |

**Credible path:** substitutions, instancing of repeated modules, per-district static merge, one LOD step for trees and far roofs. **Unproven** until one archetype is measured in the real page (12).
""")

w("11-terrain-support-contract.md", f"""
# 11 - Town-first terrain support contract (P1.4; no island is modelled)

| Requirement | P1.3 | P1.4 |
|---|---|---|
| Developed envelope | x -28.5..42, z -90..8 (70.5 x 98 m) | x {x0}..{x1}, z {-n1}..{-n0} (**{x1 - x0:.1f} x {n1 - n0:.0f} m**) |
| Transport reservation | x -10..10, z 8..24 | unchanged |
| Combined footprint | 70.5 x 114 m | **{ux1 - ux0:.1f} x {un1 - un0:.0f} m** |
| Terrain support zone (combined + 10 m, assumption) | 90.5 x 134 m | **{ux1 - ux0 + 20:.1f} x {un1 - un0 + 20:.0f} m** (x {ux0 - 10}..{ux1 + 10}, z {-un1 - 10}..{-un0 + 10}) |
| Base elevation | y = 0 | y = 0 |
| Raised surfaces | Hall podium +1.0 | **Civic terrace +1.0 (x -14..14, z -74..-62) and hall podium +2.0 (x -14..14, z -90..-74)** |
| How the raised surfaces are made | Town geometry | Either town geometry (as in the blockout) **or** a 1 m terrain step under the terrace and a 2 m step under the hall. To be decided in P4; the steps and skirt stay town geometry either way |
| Foundation zones | 22 | {nb} measured envelopes (06) |
| Lookout | Terrace x 30..42, z -62..-52 | unchanged; tea house apron extends to z = -66 |

The 1 m level change is the first vertical demand the town makes on the island. If the terrain supplies it, the ground behind the hall (north) can stay at +1 or +2 and the plinth row is not needed.
No cliff, drop or waterfall inside the support zone except beside the lookout. Likely island size about 112 x 155 m or larger.

Not created: island mesh, cliffs, waterfalls, underside, terrain export.
""")

w("12-p2-construction-contract.md", f"""
# 12 - P2 construction contract for the P1.4 design (not started; needs explicit authorisation)

P2 builds the archetypes as reusable assemblies and proves one in the real Three.js scene. It does not assemble the town (P3) or build terrain (P4).
This replaces `../p1.3/10-p2-construction-contract.md` where they differ.

## Roster

{tbl(["ID", "Purpose", "Instances", "Used by", "Footprint (m)", "Height (m)", "Module instances / ids", "Triangles each", "Sources", "Readiness"], arows)}
Structures: split gateway (READY), market cross (READY), civic terrace (READY), two gate arches (READY). Free-stall kits as P1.2.

**READY** {sum(1 for a in order if STATUS[a] == 'READY')} of {len(order)}; **CONDITIONAL** {sum(1 for a in order if STATUS[a] == 'CONDITIONAL')} (each with one named dependency above); **BLOCKED** none.
The conditional items share three dependencies: the custom cloth awning (new in P1.4), the cafe-pack material conversion, and owner acceptance of Avramania.

## To author rather than assemble

Seal; trade sign with seven pictograms; **cloth awning bay in three colourways; pennant line; paving seal**; cloth and dark-roof material instances; graded textures; a purpose-made lamp post; a solid terrace mass.

## Sequence

1. Scale scene: 2 m grid, 3 m storey, 1.9 m explorer.
2. Materials: bake the colour grade; merge duplicates only where node set-ups match; material instances; one palette texture for the custom flat colours. Convert the used cafe-pack models to GLB once.
3. Shared wall, window, door, roof and signage sub-assemblies; the awning bay.
4. A04, A04b. 5. A03b, A03c, A03. 6. A05, **A11 / A11m**, A06.
7. A02, **A10 rows**, gateway, market cross. 8. **Terrace**, A01. 9. A07, A08, **A09**.
10. Substitutions of 10; join static meshes per building by material.
11. One archetype exported and loaded in the real scene; measurements recorded; stop for approval.

## Measurable verification steps

| Step | Measure | Pass condition (proposed) |
|---|---|---|
| 1 | Triangles per archetype GLB | At or below an agreed budget |
| 2 | Distinct materials and textures | At or below {len(base_mats)}; no texture above 2048 px |
| 3 | One archetype in the real page: `renderer.info.render.triangles` and `.calls` at three fixed cameras against the island-1 baseline | Recorded |
| 4 | Scale and orientation: door 2.1 m, storey 3.0 m, +y up | Within 1 cm |
| 5 | Controller on both flights of steps, the 0.18 m deck-edge riser, a hall arch and a 4 m lane | No sticking |
| 6 | Follow camera at the places listed in 09, with awnings and pennants in or out of the collision set | Recorded; decision on the set |
| 7 | Double-sided cloth renders correctly from below | Visual check |
| 8 | Frame time over a fixed 60 s walk at 1280 x 720 | Recorded with hardware |

**Browser performance has not been validated.**
""")

w("13-decisions-and-risks.md", f"""
# 13 - Remaining design decisions and risks (P1.4)

## Decisions for the owner

1. **P1.4 against P1.3.** Both are complete and separate; either can go forward.
2. **The level change.** A raised terrace is the largest single change. It adds steps to the primary route and a vertical demand on the island (11).
3. **Custom cloth.** Awnings, pennants and the paving seal are authored, not downloaded. They carry much of the atmosphere; without them the bazaar keeps its form but loses colour.
4. **Straight or bent street.** D is selected; E (bent) is measured in 04 and would need a further pass.
5. **Carried over, still open:** the P1.2 look (seal, burgundy and blue, sign pictograms), the Syntaxes of Play and Avramania sources, a triangle and draw-call budget.
6. **Authorisation to start P2.** Not assumed.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Triangle load ({STATS['triangles']:,}; +{100 * (STATS['triangles'] - S13['triangles']) / S13['triangles']:.0f}% on P1.3) | Medium to high | Substitutions project {TOWN_NEW:,}; measure early; turrets and the inn are the first things to simplify |
| Camera clear on fewer directions ({SUM['camera_edges_fully_clear']} of {SUM['camera_travel_directions']}) | Medium | Decide whether cloth and pennants are in the camera collision set; adjust the inn balcony; engine test |
| Steps on the primary route | Low to medium | Five risers of about 0.2 m, as on the hall steps already validated; engine test; a ramp proxy is possible |
| Custom cloth looks flat beside painted textures | Medium | Woven texture and vertex-colour stripes in P2 |
| References not located (R02, R03, R05, R08, R09) | Certain | Their principles came from the brief's text; if the owner supplies links, the board can be completed |
| Alefran-like packs tempting later | Low | Licence recorded in 03; do not adopt without written permission from the creator |
| Hall still made of house modules | Certain | Accept, or commission a small custom civic module set |
| Secondary quarters least improved | Certain | A distinct workshop type in a later pass |

## Not verified

Nothing was loaded in Three.js. Appearance, collision, camera and performance in the game are untested. The massing metrics for E are from boxes, not assets.

## Scope confirmation

No production town implementation, island terrain, Three.js change, first-island asset reuse, gameplay system, GLB export, deployment or commit. One pack was downloaded for inspection and not adopted.

**MERCHANT CITADEL P1.4 - PENDING HUMAN VISUAL APPROVAL. STOP.**
""")
print("package written:", nb, "buildings,", STATS["triangles"], "tris ->", TOWN_NEW, "| QA", round(qavg, 2), "| camera", SUM["camera_edges_fully_clear"], "/", SUM["camera_travel_directions"], "| newly used", len(newly))
