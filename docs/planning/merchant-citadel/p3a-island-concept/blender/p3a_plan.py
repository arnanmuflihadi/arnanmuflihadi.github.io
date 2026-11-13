#!/usr/bin/env python3
"""Merchant Citadel P3-A: measured top-down plans and measurements of the island concepts against the REAL built town.

Reads the batch-5 terrain-interface.json (building envelopes from the live scene) and the same p3a_island_shape.py the Blender
massing uses. Writes plan-<key>.png and island-measurements.json.
Usage: python3 p3a_plan.py <terrain-interface.json> <out_dir>
"""
import json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3a_island_shape as S

TI, OUT = sys.argv[1:3]
os.makedirs(OUT, exist_ok=True)
T = json.load(open(TI)); B = T["buildings"]
th = np.linspace(0, S.TAU, 1440, endpoint=False)
WALK, RUN = 2.1, 4.6
RES = {}


def ring(c, inset=0.0):
    R = S.outline(c, th) - inset; cx, cy = c["centre"]
    return cx + R * np.cos(th), cy + R * np.sin(th), R


def poly_len(p):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p[:-1], p[1:]))


for key in ("A", "B", "C", "S"):
    c = S.CONCEPTS[key]; F = S.FEATURES[key]
    X, Y, R = ring(c); area = float(0.5 * np.sum(R * R) * (th[1] - th[0]))
    sats = c.get("satellites", [])
    fig, ax = plt.subplots(figsize=(13, 14), dpi=110)
    xs = np.arange(X.min() - 4, X.max() + 4, 1.0); ys = np.arange(Y.min() - 4, Y.max() + 4, 1.0); GX, GY = np.meshgrid(xs, ys)
    H = S.top_height(c, GX, GY); inside = S.contains(c, GX, GY, 0.0); Hm = np.ma.masked_where(~inside, H)
    lv = [-9, -7, -5, -3.2, -1.5, -0.3, 0.6, 1.5, 3, 6, 10, 14, 18, 23]
    cf = ax.contourf(GX, GY, Hm, levels=lv, cmap="YlGn_r", alpha=0.85)
    ax.contour(GX, GY, Hm, levels=lv, colors="k", linewidths=0.25, alpha=0.5)
    plt.colorbar(cf, ax=ax, shrink=0.5, label="terrain top above the town datum (m)")
    ax.plot(np.append(X, X[0]), np.append(Y, Y[0]), color="#5a3d1e", lw=2.2, label="island rim (cliff top)")
    xi, yi, _ = ring(c, 6.0); ax.plot(np.append(xi, xi[0]), np.append(yi, yi[0]), color="#b03030", lw=0.9, ls="--", label="6 m cliff setback (contract)")
    for s_ in sats:
        sx, sy, sr = ring(s_); ax.fill(sx, sy, color="#cfe3a8", ec="#5a3d1e", lw=1.6); ax.text(s_["centre"][0], s_["centre"][1] - sr.max() - 4, s_["name"], ha="center", fontsize=8)
        area += float(0.5 * np.sum(sr * sr) * (th[1] - th[0]))
    ax.add_patch(Rectangle((T["paved_extent_x"][0], T["paved_extent_n"][0]), T["paved_extent_x"][1] - T["paved_extent_x"][0], T["paved_extent_n"][1] - T["paved_extent_n"][0], fc="#b9b6ae", ec="none", alpha=0.55, label="paved extent (built)"))
    ax.add_patch(Rectangle((-14, 62), 28, 12, fc="#d9d3c4", ec="#555", lw=0.6)); ax.add_patch(Rectangle((-14, 74), 28, 16, fc="#e6dfcc", ec="#555", lw=0.6))
    ax.text(0, 68, "terrace 1.01", ha="center", va="center", fontsize=6.5);
    worst = (1e9, None)
    for b in B:
        x0, x1 = b["envelope_x"]; n0, n1 = b["envelope_n"]
        ax.add_patch(Rectangle((x0, n0), x1 - x0, n1 - n0, fc="#c0623a", ec="#3a1a0c", lw=0.7, alpha=0.9))
        ax.text((x0 + x1) / 2, (n0 + n1) / 2, b["id"].replace("_main", ""), ha="center", va="center", fontsize=5.5, color="white")
        for x in (x0, x1):
            for y in (n0, n1):
                d = float(S.edge_distance(np.array([x]), np.array([y]), c)[0])
                if d < worst[0]:
                    worst = (d, b["id"], x, y)
    for i, p in enumerate(F.get("paths", [])):
        ax.plot([q[0] for q in p], [q[1] for q in p], color="#8a6a3a", lw=2.4 if i == 0 else 1.5, solid_capstyle="round", label="proposed trail" if i == 0 else None)
    for p in F.get("water", []):
        ax.plot([q[0] for q in p], [q[1] for q in p], color="#2a7fb8", lw=2.2, label="stream")
    for (fx, fy), drop in F.get("falls", []):
        ax.plot(fx + 4, fy, marker=">", color="#2a7fb8", ms=11); ax.text(fx + 8, fy + 3, "Cloudfall\n(%d m drop)" % drop, fontsize=7.5, color="#1b5d88")
    for br in F.get("bridges", []):
        ax.plot([br[0][0], br[1][0]], [br[0][1], br[1][1]], color="#3a2414", lw=3.2)
    zones = []
    for name, lx, ly, lr in F.get("landing", []):
        a = np.linspace(0, S.TAU, 48, endpoint=False); rr = np.linspace(0, lr, 8)
        cz = next((m for m in [c] + sats if S.contains(m, np.array([lx]), np.array([ly]))[0]), c)                  # the landmass the disc stands on
        px = lx + np.outer(rr, np.cos(a)); py = ly + np.outer(rr, np.sin(a)); hh = S.top_height(cz, px, py)
        rim = float(S.edge_distance(np.array([lx]), np.array([ly]), cz)[0]) - lr
        bd = min(max(max(b["envelope_x"][0] - lx, lx - b["envelope_x"][1], 0), 0) ** 2 + max(max(b["envelope_n"][0] - ly, ly - b["envelope_n"][1], 0), 0) ** 2 for b in B) ** 0.5 - lr
        ok = (float(hh.max() - hh.min()) <= 0.6) and rim >= 8 and bd >= 8
        zones.append({"name": name, "centre": [lx, ly], "radius_m": lr, "level_m": round(float(hh.mean()), 2), "height_range_m": round(float(hh.max() - hh.min()), 2), "clear_to_rim_m": round(rim, 1), "clear_to_nearest_building_m": round(bd, 1), "on": cz.get("name", "main"),
                      "meets_concept_criteria": bool(ok)})
        ax.add_patch(Circle((lx, ly), lr, fc="none", ec="#1565c0" if ok else "#c62828", lw=1.8, ls="-" if ok else ":")); ax.text(lx, ly, "L\n" + name, ha="center", va="center", fontsize=6.5, color="#0d3c75")
    for name, vx, vy, deg in F.get("viewpoints", []):
        ax.plot(vx, vy, marker="*", color="#f2b632", ms=13, mec="k", mew=0.5); ax.text(vx + 2.5, vy + 2.5, name, fontsize=7)
    ax.plot(0, -16, marker="s", color="#6a1b9a", ms=8); ax.text(2.5, -17.5, "N20 transport\nreservation", fontsize=7, color="#6a1b9a")
    ax.plot([X.min(), X.max()], [Y.min() - 9, Y.min() - 9], color="k", lw=1); ax.text((X.min() + X.max()) / 2, Y.min() - 13.5, "%.0f m east-west" % (X.max() - X.min()), ha="center", fontsize=9)
    ax.plot([X.max() + 9, X.max() + 9], [Y.min(), Y.max()], color="k", lw=1); ax.text(X.max() + 11.5, (Y.min() + Y.max()) / 2, "%.0f m north-south" % (Y.max() - Y.min()), rotation=90, va="center", fontsize=9)
    ax.plot([X.min() + 4, X.min() + 54], [Y.max() + 6, Y.max() + 6], color="k", lw=4); ax.text(X.min() + 29, Y.max() + 8.5, "50 m", ha="center", fontsize=9)
    ax.annotate("N", xy=(X.max() - 4, Y.max() + 12), xytext=(X.max() - 4, Y.max() + 1), arrowprops=dict(arrowstyle="-|>", color="k"), ha="center", fontsize=11)
    ax.set_aspect("equal"); ax.grid(True, lw=0.3, alpha=0.5); ax.set_xticks(np.arange(-120, 141, 20)); ax.set_yticks(np.arange(-100, 161, 20))
    lim = [min(X.min(), *(ring(s_)[0].min() for s_ in sats)) - 14 if sats else X.min() - 14, max(X.max(), *(ring(s_)[0].max() for s_ in sats)) + 18 if sats else X.max() + 18]
    ax.set_xlim(*lim); ax.set_ylim(min(Y.min(), *(ring(s_)[1].min() for s_ in sats)) - 18 if sats else Y.min() - 18, Y.max() + 16)
    ax.set_xlabel("plan x (m, east)"); ax.set_ylabel("plan n (m, north)")
    ax.set_title("Merchant Citadel P3-A  concept %s: %s\nMASSING CONCEPT measured against the real 24-building town (envelopes from the live Three.js scene, batch 5)" % (key, c["name"]), fontsize=11)
    ax.legend(loc="lower left", fontsize=7.5, framealpha=0.9)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "plan-%s.png" % key)); plt.close(fig)
    D = np.asarray(c["depth"](th), float)
    rim_h = S.top_height(c, X - 0.2 * np.cos(th), Y - 0.2 * np.sin(th))
    cell = 1.0; flat = float(np.sum(inside & (np.abs(np.gradient(H, cell)[0]) + np.abs(np.gradient(H, cell)[1]) < 0.12)) * cell * cell)
    # largest landing discs this concept can offer at all (grid search on the main landmass, same criteria)
    gx, gy = np.meshgrid(np.arange(X.min(), X.max(), 2.0), np.arange(Y.min(), Y.max(), 2.0)); gx, gy = gx.ravel(), gy.ravel()
    drim = S.edge_distance(gx, gy, c); dbl = np.full_like(gx, 1e9)
    for b in B:
        dbl = np.minimum(dbl, np.hypot(np.maximum(np.maximum(b['envelope_x'][0] - gx, gx - b['envelope_x'][1]), 0), np.maximum(np.maximum(b['envelope_n'][0] - gy, gy - b['envelope_n'][1]), 0)))
    dbl = np.minimum(dbl, S.rect_dist(gx, gy, (T['paved_extent_x'][0], T['paved_extent_x'][1], T['paved_extent_n'][0], T['paved_extent_n'][1])) + 8.0)   # paving itself is allowed up to the disc edge
    rmax = np.minimum(drim, dbl) - 8.0; order = np.argsort(-rmax); best = []
    for i in order[:4000]:
        r0 = float(rmax[i])
        if r0 < 4 or any(math.hypot(gx[i] - q['centre'][0], gy[i] - q['centre'][1]) < q['radius_m'] + r0 for q in best):
            continue
        r_ok = 0.0
        for r_try in np.arange(min(r0, 20.0), 3.9, -1.0):
            a = np.linspace(0, S.TAU, 36, endpoint=False); rr = np.linspace(0, r_try, 6); hh = S.top_height(c, gx[i] + np.outer(rr, np.cos(a)), gy[i] + np.outer(rr, np.sin(a)))
            if float(hh.max() - hh.min()) <= 0.6:
                r_ok = float(r_try); break
        if r_ok >= 4:
            best.append({'centre': [float(gx[i]), float(gy[i])], 'radius_m': round(r_ok, 1)})
        if len(best) >= 4:
            break
    RES_best = best
    RES[key] = {
        "name": c["name"], "extent_x_m": [round(float(X.min()), 1), round(float(X.max()), 1)], "extent_n_m": [round(float(Y.min()), 1), round(float(Y.max()), 1)],
        "size_m": [round(float(X.max() - X.min()), 1), round(float(Y.max() - Y.min()), 1)], "top_area_m2_incl_satellites": round(area), "rim_perimeter_m": round(float(np.sum(np.hypot(np.diff(np.append(X, X[0])), np.diff(np.append(Y, Y[0])))))),
        "town_footprint_share_of_top": round(((T["town_extent"]["x"][1] - T["town_extent"]["x"][0]) * (T["town_extent"]["n"][1] - T["town_extent"]["n"][0])) / area, 3),
        "walkable_near_level_area_m2": round(flat), "top_height_range_m": [round(float(Hm.min()), 1), round(float(Hm.max()), 1)], "rim_height_range_m": [round(float(rim_h.min()), 1), round(float(rim_h.max()), 1)],
        "underside_depth_below_rim_m": [round(float(D.min())), round(float(D.max()))], "cliff_band_m": c["cliff"],
        "min_building_to_rim_m": {"distance": round(worst[0], 1), "building": worst[1], "corner": [worst[2], worst[3]]},
        "N20_to_rim_m": round(float(S.edge_distance(np.array([0.0]), np.array([-16.0]), c)[0]), 1),
        "satellites": [{"name": s_["name"], "centre": list(s_["centre"]), "top_m": s_["top"]} for s_ in sats],
        "landing_zones": zones, "largest_possible_landing_discs_main_landmass": RES_best, "viewpoints": [{"name": n_, "at": [x_, y_]} for n_, x_, y_, _d in F.get("viewpoints", [])],
        "trails": [{"from": list(p[0]), "to": list(p[-1]), "length_m": round(poly_len(p), 1), "walk_s": round(poly_len(p) / WALK), "run_s": round(poly_len(p) / RUN)} for p in F.get("paths", [])],
        "streams_m": [round(poly_len(p), 1) for p in F.get("water", [])],
    }
    print(key, "best discs", [(q["centre"], q["radius_m"]) for q in RES_best]); print(key, RES[key]["size_m"], RES[key]["top_area_m2_incl_satellites"], "min setback", RES[key]["min_building_to_rim_m"], [(z["name"], z["meets_concept_criteria"], z["height_range_m"], z["clear_to_rim_m"], z["clear_to_nearest_building_m"]) for z in zones])
json.dump({"source": "p3a_island_shape.py + p2e-batch5/terrain-interface.json", "landing_zone_concept_criteria": "disc of the stated radius with a height range <= 0.6 m, >= 8 m from the disc to the rim and >= 8 m to the nearest building envelope; trees are excluded from the discs by the massing generator. These are CONCEPT criteria: the game's dynamic landing system has its own rules, not evaluated here.",
           "concepts": RES}, open(os.path.join(OUT, "island-measurements.json"), "w"), indent=1)
