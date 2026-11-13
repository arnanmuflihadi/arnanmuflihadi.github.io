#!/usr/bin/env python3
"""Merchant Citadel P1.3 - measure and compare the P1.2 baseline and the three layout alternatives (plain Python).

Usage: python3 compare_p13.py <inspection_dir> <package_dir>
Reads the P1.2 snapshot (<inspection_dir>/p1.2) and the massing ray tests (<inspection_dir>/p1.3/massing/massing-metrics.json).
Writes <inspection_dir>/p1.3/alternatives.json, visuals/alternatives-plans.png and visuals/alternatives-massing.png.
"""
import json, math, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layouts_p13 as LY
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

I, P = sys.argv[1], sys.argv[2]
L12 = json.load(open(f"{I}/p1.2/data/layout.json")); AREP = json.load(open(f"{I}/p1.3/archetypes/archetype-report.json")); S12 = json.load(open(f"{I}/p1.2/renders/town-stats.json"))
MM = json.load(open(f"{I}/p1.3/massing/massing-metrics.json"))
BUDGET = {"A01": 53214, "A02": 25014, "A03": 15156, "A03b": 15372, "A04": 5978, "A04b": 5912, "A05": 18338, "A06": 15996, "A07": 22791, "A08": 12692, "A03c": 15400}   # P1.2 projection per archetype; A03c estimated from A03b
PROXY = {"A01": 9, "A02": 12, "A08": 5}
b12 = [(k, v[0], "", v[1], v[2], v[3], k, None, "kept") for k, v in LY.P12.items()]
SETS = {"P12": {"title": "P1.2 baseline (approved positions)", "buildings": b12, "paving": L12["paving"], "yards": L12.get("yards", []), "nodes": {k: tuple(v) for k, v in L12["nodes"].items()},
                "edges": [tuple(e) for e in L12["edges"]], "lines": LY.P12_LINES, "stalls": [(s["id"], s["kit"], s["x"], s["n"], s["rz"]) for s in L12["stalls"]]}}
SETS.update(LY.ALTS)
rest12 = S12["triangles"] - sum(AREP[v[0]]["triangles"] for v in LY.P12.values())
PRIMARY = {"P12": ["N01", "N02", "N03", "N04", "N05", "N29", "N27", "N06", "N07", "N08"]}


def evaluate(key, a):
    bs = a["buildings"]; rects = [LY.rect_of(b) for b in bs]
    xs = [v for r in rects for v in r[:2]] + [v for p in a["paving"] for v in p[1:3]]; ns = [v for r in rects for v in r[2:]] + [v for p in a["paving"] for v in p[3:5]]
    env = (min(xs), max(xs), min(ns), max(ns))
    N, E = a["nodes"], [e for e in a["edges"]]
    ln = lambda p, q: math.hypot(N[p][0] - N[q][0], N[p][1] - N[q][1])
    built = [e for e in E if not e[2].startswith("reserved")]
    prim_nodes = PRIMARY["P12"]
    prim = sum(ln(p, q) for p, q in zip(prim_nodes, prim_nodes[1:]))
    enc = {l[0]: LY.enclosure(bs, l) for l in a["lines"]}
    grp = lambda keys: (sum(enc[k][0] * enc[k][1] for k in keys) / sum(enc[k][0] for k in keys), sum(enc[k][0] * enc[k][2] for k in keys) / sum(enc[k][0] for k in keys))
    groups = {"Merchant street": [k for k in enc if k.startswith("Merchant")], "Artisan lane": [k for k in enc if k.startswith("Artisan")], "Warehouse lane": [k for k in enc if k.startswith("Warehouse")],
              "Bazaar perimeter": [k for k in enc if k.startswith("Bazaar")], "Arrival court sides": [k for k in enc if k.startswith("Arrival")], "Civic court sides": [k for k in enc if k.startswith("Civic")]}
    gsum = {g: [round(v) for v in grp(ks)] for g, ks in groups.items()}
    tri_b = sum(AREP[b[1]]["triangles"] for b in bs); tri_opt = sum(BUDGET[b[1]] for b in bs)
    cam = MM[key]["camera"]; vis = MM[key]["hall_visibility"]
    sec = [c for c in cam if c["type"] != "primary"]
    arch = collections.Counter(b[1] for b in bs)
    return {
        "title": a["title"], "buildings": len(bs), "new_buildings": sum(b[8] == "new" for b in bs), "moved_or_changed": sum(b[8] not in ("new", "kept") for b in bs), "kept_in_place": sum(b[8] == "kept" for b in bs),
        "archetypes_used": dict(sorted(arch.items())), "archetype_count": len(arch), "stalls": len(a["stalls"]), "envelope": env, "envelope_size": [env[1] - env[0], env[3] - env[2]],
        "support_zone": [env[1] - env[0] + 20, max(env[3], 90) - min(env[2], -24) + 20], "footprint_area_m2": round(sum((r[1] - r[0]) * (r[3] - r[2]) for r in rects)),
        "coverage_pct": round(100 * sum((r[1] - r[0]) * (r[3] - r[2]) for r in rects) / ((env[1] - env[0]) * (env[3] - env[2])), 1),
        "nodes": len(N), "edges": len(E), "loops": len(E) - len(N) + 1, "network_m": round(sum(ln(p, q) for p, q, _ in built), 1), "primary_route_m": round(prim, 1),
        "enclosure_lines": enc, "enclosure_groups_wall_active_pct": gsum,
        "overall_wall_pct": round(sum(v[0] * v[1] for v in enc.values()) / sum(v[0] for v in enc.values())), "overall_active_pct": round(sum(v[0] * v[2] for v in enc.values()) / sum(v[0] for v in enc.values())),
        "triangles_buildings": tri_b, "triangles_estimate_unoptimised": tri_b + rest12, "triangles_estimate_after_substitutions": tri_opt + round(rest12 * 0.50),
        "collision_proxies_buildings": sum(PROXY.get(b[1], 1) for b in bs),
        "camera_directions": len(cam), "camera_fully_clear": sum(c["clear_pct"] == 100 for c in cam), "camera_secondary_mean_clear_pct": round(sum(c["clear_pct"] for c in sec) / len(sec)),
        "camera_worst": sorted([c for c in cam if c["clear_pct"] < 60], key=lambda c: c["clear_pct"])[:8],
        "hall_tower_visible_from": [k for k, v in vis.items() if v["tower seal"]], "hall_porch_visible_from": [k for k, v in vis.items() if v["porch gable"]], "hall_points_tested": list(vis)}


RES = {k: evaluate(k, a) for k, a in SETS.items()}
os.makedirs(f"{I}/p1.3", exist_ok=True); os.makedirs(f"{P}/visuals", exist_ok=True)
json.dump(RES, open(f"{I}/p1.3/alternatives.json", "w"), indent=1)

# ---- four plans ------------------------------------------------------------------------------------
TILE = {"MV-Floor_UnevenBrick": "#cfc7b6", "MV-Floor_Brick": "#c2b29f", "MV-Floor_RedBrick": "#cfa58e"}
EC = {"primary": ("#d62728", 2.0), "secondary": ("#1f77b4", 1.2), "service": ("#e6a700", 1.2), "market": ("#8a4fbf", 1.0), "scenic": ("#2a9d8f", 1.2), "reserved link": ("#3a6ea5", 0.8)}
fig, axs = plt.subplots(1, 4, figsize=(26, 9.6), dpi=110)
for ax, (key, a) in zip(axs, SETS.items()):
    r = RES[key]; ax.set_facecolor("#dfe8cf")
    for pv in a["paving"]:
        ax.add_patch(Rectangle((pv[1], pv[3]), pv[2] - pv[1], pv[4] - pv[3], fc=TILE[pv[5]], ec="none"))
    for y in a["yards"]:
        ax.add_patch(Rectangle((y[1], y[3]), y[2] - y[1], y[4] - y[3], fc="#d9c7a3", ec="#a08a5c", lw=0.4, ls=":"))
    ax.add_patch(Rectangle((-10, -24), 20, 16, fill=False, hatch="//", ec="#3a6ea5", lw=0.8))
    for b in a["buildings"]:
        x0, x1, n0, n1 = LY.rect_of(b); st = b[8]
        fc = "#e9b949" if st == "new" else "#c9d6e8" if st != "kept" else "#c98a6b"
        ax.add_patch(Rectangle((x0, n0), x1 - x0, n1 - n0, fc=fc, ec="#222", lw=0.9))
        ax.text((x0 + x1) / 2, (n0 + n1) / 2, f"{b[0]}\n{b[1]}", ha="center", va="center", fontsize=5.6, weight="bold")
        for fx, fn in LY.fronts(b)[:2] if b[1] != "A02" else []:
            cx, cn = (x0 + x1) / 2, (n0 + n1) / 2
            ax.plot([cx + fx * (x1 - x0) / 2], [cn + fn * (n1 - n0) / 2], marker=(3, 0, {(0, -1): 180, (0, 1): 0, (1, 0): -90, (-1, 0): 90}[(fx, fn)]), color="#111", ms=4)
    for s in a["stalls"]:
        ax.add_patch(Rectangle((s[2] - 0.8, s[3] - 0.8), 1.6, 1.6, fc="#5b7fa8", ec="none"))
    for p, q, kind in a["edges"]:
        k = kind.split(",")[0]
        ax.plot([a["nodes"][p][0], a["nodes"][q][0]], [a["nodes"][p][1], a["nodes"][q][1]], color=EC[k][0], lw=EC[k][1], alpha=0.85)
    e = r["envelope"]; ax.add_patch(Rectangle((e[0], e[2]), e[1] - e[0], e[3] - e[2], fill=False, ls=":", ec="#444", lw=0.9))
    ax.set_xlim(-36, 50); ax.set_ylim(-27, 94); ax.set_aspect("equal"); ax.grid(True, color="#fff", lw=0.3, alpha=0.6)
    ax.set_title(f"{a['title']}\n{r['buildings']} buildings ({r['new_buildings']} new, {r['moved_or_changed']} moved or changed) - envelope {r['envelope_size'][0]:g} x {r['envelope_size'][1]:g} m\n"
                 f"wall enclosure {r['overall_wall_pct']}%, active frontage {r['overall_active_pct']}% of the tested street and court edges", fontsize=8.6)
    ax.set_xlabel("x east (m)"); ax.set_ylabel("n north (m); project z = -n")
fig.suptitle("Merchant Citadel P1.3 - measured layout alternatives (gold = new building, blue = moved, rotated or re-typed, terracotta = unchanged; triangle = door side; lines = walking graph)", fontsize=11)
fig.tight_layout(); fig.savefig(f"{P}/visuals/alternatives-plans.png"); plt.close(fig)

# ---- massing comparison ---------------------------------------------------------------------------
def font(size, bold=False):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1 if bold else 0)
    except Exception:
        return ImageFont.load_default()


w, h = 1400, 900
sheet = Image.new("RGB", (2 * w, 2 * h + 70), (24, 44, 40)); d = ImageDraw.Draw(sheet)
d.text((16, 12), "Merchant Citadel P1.3 - aerial MASSING comparison, one camera. Boxes and roof prisms at real module dimensions; no downloaded model. Gold roof = building that P1.2 does not have.", font=font(24, True), fill=(245, 240, 225))
for i, key in enumerate(SETS):
    im = Image.open(f"{I}/p1.3/massing/massing-{key}.png").convert("RGB"); x, y = (i % 2) * w, 70 + (i // 2) * h
    sheet.paste(im, (x, y)); r = RES[key]
    d.rectangle([x, y, x + 760, y + 40], fill=(24, 44, 40)); d.text((x + 12, y + 8), f"{SETS[key]['title']} - {r['buildings']} buildings", font=font(22, True), fill=(245, 240, 225))
sheet.save(f"{P}/visuals/alternatives-massing.png", optimize=True)

for k, r in RES.items():
    print(k, r["buildings"], "env", r["envelope_size"], "cover", r["coverage_pct"], "wall/active", r["overall_wall_pct"], r["overall_active_pct"], r["enclosure_groups_wall_active_pct"])
    print("   net", r["network_m"], "loops", r["loops"], "tris", r["triangles_estimate_unoptimised"], "->", r["triangles_estimate_after_substitutions"], "cam clear", r["camera_fully_clear"], "/", r["camera_directions"], "sec mean", r["camera_secondary_mean_clear_pct"],
          "tower from", len(r["hall_tower_visible_from"]), "/", len(r["hall_points_tested"]), "worst", [(c["travel"], c["clear_pct"]) for c in r["camera_worst"][:5]])
