"""Merchant Citadel P3-B batch 2: deterministic scenery scatter and wildlife habitat layout from the batch 1 terrain model.

  python3 p3b2_scatter.py <scene.json> <out island-flora.json> [<evidence dir>]

Everything is sampled from distance/slope fields computed ONCE on the 0.5 m terrain grid (vectorised), not from per-point model calls.
Outputs: flora instances per prototype, trunk/rock collision proxies, rim-ledge rocks, habitat definitions with validated home points, roof/rock/tree perch points,
dragon-landing keep-outs. Seed 20261113: same inputs -> same island.
"""
import sys, os, json, math
import numpy as np
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../p3b-batch1/source")
import p3b_model as M, p3b_geo as G

SCENE, OUT = sys.argv[1], sys.argv[2]; EV = sys.argv[3] if len(sys.argv) > 3 else None
rng = np.random.default_rng(20261113)
spec = M.grid_spec(); X, N, H = M.sample_grid(spec); C = spec["cell"]; nx, nn = spec["nx"], spec["nn"]
HH = np.where(np.isnan(H), -80.0, H)
gy, gx = np.gradient(HH, C); SLOPE = np.hypot(gx, gy)


def at(arr, x, n, fill=0.0):
    fx = (np.asarray(x) - spec["x0"]) / C; fy = (np.asarray(n) - spec["n0"]) / C; i = np.clip(np.round(fx).astype(int), 0, nx - 1); j = np.clip(np.round(fy).astype(int), 0, nn - 1); return arr[j, i]


def tz(x, n):
    return M.terrain(x, n)


EDGE = np.maximum(M.edge_distance(M.MAIN, X, N), M.edge_distance(M.STACK, X, N))
sc = json.load(open(SCENE))
# distance to solids (town buildings and props), to routes, to paths, to stream, to clearings
solid = np.zeros(X.shape, bool)
for (x0, x1, n0, n1) in M.load_solids(SCENE):
    i0, i1 = int((x0 - spec["x0"]) / C), int((x1 - spec["x0"]) / C) + 1; j0, j1 = int((n0 - spec["n0"]) / C), int((n1 - spec["n0"]) / C) + 1; solid[max(j0, 0):j1 + 1, max(i0, 0):i1 + 1] = True
D_SOLID = ndimage.distance_transform_edt(~solid) * C
route = np.zeros(X.shape, bool)
nodes = sc["nodes"]; via = sc.get("edge_via", {})
for a, b, kind in sc["edges"]:
    pts = [nodes[a][:2]] + via.get(a + "-" + b, via.get(b + "-" + a, [])) + [nodes[b][:2]]
    for p, q in zip(pts[:-1], pts[1:]):
        k = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 0.25))
        for t in np.linspace(0, 1, k):
            x, n = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t; i, j = int((x - spec["x0"]) / C), int((n - spec["n0"]) / C)
            if 0 <= i < nx and 0 <= j < nn: route[j, i] = True
D_ROUTE = ndimage.distance_transform_edt(~route) * C
D_PATH = M.path_distance(X, N); D_STREAM = M.stream_distance(X, N); D_CLEAR = M.clearing_distance(X, N)
PAD_D = M.rect_dist(X, N, M.PAD)                    # > 0 outside the town pad
walk, comf, _sl = M.masks(H, M.edge_distance(M.MAIN, X, N), M.edge_distance(M.STACK, X, N), M.bridge_height(X, N))
LOOK = np.array(M.LOOKOUT)
BENCH_D = np.hypot(X - LOOK[0], N - LOOK[1])


def noise(x, n, seed, scale=30.0):
    return 0.5 + 0.5 * M.field_noise(np.asarray(x, float) / scale * 60.0, np.asarray(n, float) / scale * 60.0, seed)


def accept(x, n, *, edge=3.0, solid=3.0, route=1.5, path=1.8, stream=1.8, clear=0.0, slope=0.55, pad_ok=False, walkable=True):
    ok = at(EDGE, x, n) >= edge
    ok &= at(D_SOLID, x, n) >= solid; ok &= at(D_ROUTE, x, n) >= route; ok &= at(D_PATH, x, n) >= path; ok &= at(D_STREAM, x, n) >= stream
    ok &= at(D_CLEAR, x, n) >= clear; ok &= at(SLOPE, x, n) <= slope
    if walkable: ok &= at(walk, x, n)                                  # the same walk mask the player collision uses
    if not pad_ok: ok &= at(PAD_D, x, n) > 0.5
    return ok


out = {"seed": 20261113, "instances": {}, "trunks": [], "rocks_solid": [], "habitats": {}, "perches": {"roof": [], "rock": [], "tree": [], "prop": []}, "keepouts": []}
inst = out["instances"]
add = lambda name, x, n, z, yaw, s: inst.setdefault(name, []).append([round(float(x), 3), round(float(n), 3), round(float(z), 3), round(float(yaw), 3), round(float(s), 3)])

# ---------------------------------------------------------------------------------------------- dragon-landing keep-outs (animals stay out; flora kept low)
KEEP = [("Caravan Green core", -50.0, 18.0, 9.0), ("Sky Quay core", 5.0, -52.0, 11.0), ("Shoulder Table", -36.0, 112.0, 6.5), ("Hall lawn west", -32.5, 85.0, 7.5), ("Counting Stone", 40.0, 116.0, 3.5)]
out["keepouts"] = [dict(name=k[0], x=k[1], n=k[2], r=k[3]) for k in KEEP]


def keep_ok(x, n, margin=0.0):
    return all(math.hypot(x - kx, n - kn) > r + margin for _, kx, kn, r in KEEP)


# ---------------------------------------------------------------------------------------------- trees in groves
# zone: cx, cn, rx, rn, mixture (common, pine, twisted, dead), density per 100 m2
ZONES = [("west wood", -68, 56, 11, 20, (0.8, 0.1, 0.0, 0.0), 3.2), ("south-west grove", -52, -14, 13, 8, (0.85, 0.1, 0.05, 0.0), 3.0), ("south-east grove", 54, -9, 10, 8, (0.8, 0.2, 0.0, 0.0), 2.6),
         ("green edge north", -58, 36, 10, 7, (0.9, 0.0, 0.1, 0.0), 2.4), ("green edge south", -52, 2, 9, 5, (0.85, 0.0, 0.15, 0.0), 2.4), ("crag pines", 50, 112, 26, 12, (0.1, 0.65, 0.0, 0.25), 3.4), ("crag west", -20, 118, 12, 6, (0.35, 0.5, 0.0, 0.15), 2.6),
         ("hall rear grove", 14, 124, 12, 4, (0.5, 0.4, 0.0, 0.1), 2.6), ("north-east wood", 70, 98, 12, 9, (0.5, 0.4, 0.1, 0.0), 2.6), ("west shore", -72, 20, 6, 22, (0.9, 0.0, 0.1, 0.0), 2.0), ("north-west meadow", -52, 100, 12, 9, (0.7, 0.2, 0.1, 0.0), 2.4), ("shoulder grove", -52, 112, 6, 5, (0.6, 0.3, 0.1, 0.0), 2.0)]
TREE_NAMES = ["common", "pine", "twisted", "dead"]; VAR = {"common": ["CommonTree_1", "CommonTree_3", "CommonTree_4"], "pine": ["Pine_1", "Pine_5"], "twisted": ["TwistedTree_2"], "dead": ["DeadTree_3"]}
SCALE = {"common": (0.85, 1.35), "pine": (0.85, 1.4), "twisted": (0.55, 0.8), "dead": (0.7, 1.0)}
trees = []
for zn, cx, cn, rx, rn, mix, dens in ZONES:
    n_try = int(math.pi * rx * rn * dens / 100 * 6)
    for _ in range(n_try):
        a = rng.uniform(0, 2 * math.pi); r = math.sqrt(rng.uniform()); x = cx + rx * r * math.cos(a); n = cn + rn * r * math.sin(a)
        if rng.uniform() > noise(x, n, 7, 18.0) ** 0.8 + 0.15: continue
        if not accept(x, n, edge=3.5, solid=4.0, route=2.5, path=2.5, stream=2.4, clear=3.0, slope=0.5) or not keep_ok(x, n, 3.0): continue
        if x > 46 and n < 92 and abs(n - 57) < 42 and float(tz(np.array(x), np.array(n))) < 1.0: continue          # tea lookout wedge: low planting only
        if any(math.hypot(x - t[0], n - t[1]) < 4.2 for t in trees): continue
        kind = TREE_NAMES[rng.choice(4, p=np.array(mix) / sum(mix))]; name = VAR[kind][rng.integers(len(VAR[kind]))]; s = rng.uniform(*SCALE[kind])
        z = float(tz(np.array(x), np.array(n))); trees.append((x, n, z, rng.uniform(0, 2 * math.pi), s, name, zn))
# hero trees: a twisted tree at the Tea Lookout lawn edge and one at the Cloudfall overlook, framing the view (kept out of the sightline centre)
for (hx, hn, nm) in ((30.0, 49.0, "TwistedTree_2"), (76.0, 61.5, "TwistedTree_2"), (-30.0, 58.0, "CommonTree_1")):
    z = float(tz(np.array(hx), np.array(hn)));
    if accept(hx, hn, edge=2.0, solid=1.5, route=1.0, path=1.5, stream=1.5, slope=0.5, pad_ok=True): trees.append((hx, hn, z, rng.uniform(0, 6), 0.75 if "Twisted" in nm else 1.0, nm, "hero"))
# P3-B batch 3 (crag pass): dead trees on the crag benches and shoulders (separate generator so every earlier random draw stays identical)
rng2 = np.random.default_rng(31415)
for _ in range(900):
    if sum(1 for t in trees if t[6] == "crag dead") >= 9: break
    x = rng2.uniform(8, 84); n = rng2.uniform(94, 132)
    if not accept(x, n, edge=3.5, solid=4.0, route=2.5, path=2.5, stream=2.4, clear=3.0, slope=0.5) or not keep_ok(x, n, 3.0) or any(math.hypot(x - t[0], n - t[1]) < 5.0 for t in trees): continue
    trees.append((x, n, float(tz(np.array(x), np.array(n))), rng2.uniform(0, 6.3), rng2.uniform(0.8, 1.15), "DeadTree_3", "crag dead"))
for x, n, z, yaw, s, name, zn in trees:
    add(name, x, n, z - 0.05, yaw, s); out["trunks"].append(dict(x=round(x, 2), n=round(n, 2), r=0.35 * s + 0.12)); out["perches"]["tree"].append([round(x, 2), round(n, 2), round(z + (6.0 if name.startswith(("Common", "Pine")) else 7.0) * s * 0.85, 2)])

# ---------------------------------------------------------------------------------------------- understory around trees and along woods
def around(name_list, per, rmin, rmax, scale, yoff=-0.03, filt=None, pool=None):
    for x, n, z, yaw, s, nm, zn in (pool or trees):
        for _ in range(per):
            if rng.uniform() > 0.7: continue
            a = rng.uniform(0, 2 * math.pi); r = rng.uniform(rmin, rmax); px, pn = x + r * math.cos(a), n + r * math.sin(a)
            if not accept(px, pn, edge=2.0, solid=2.0, route=1.2, path=1.4, stream=1.0, clear=1.0, slope=0.55) or not keep_ok(px, pn, 1.0): continue
            if filt and not filt(zn): continue
            add(name_list[rng.integers(len(name_list))], px, pn, float(tz(np.array(px), np.array(pn))) + yoff, rng.uniform(0, 6.3), rng.uniform(*scale))
around(["Bush_Common", "Bush_Common_Flowers"], 2, 2.0, 5.0, (0.7, 1.15)); around(["Fern_1", "Plant_1_Big", "Plant_7_Big"], 3, 1.5, 4.5, (0.7, 1.2)); around(["Mushroom_Common"], 1, 1.2, 3.0, (0.7, 1.3))
trees_all = trees

# ---------------------------------------------------------------------------------------------- meadow flowers and grass (patchy, noise-driven)
def meadow(names, count, scale, thresh, seed, **kw):
    n_ok = 0; tries = 0
    while n_ok < count and tries < count * 40:
        tries += 1; x = rng.uniform(-82, 98); n = rng.uniform(-80, 136)
        if noise(x, n, seed, 14.0) < thresh or n < -26: continue          # nothing grows through the quay paving
        if not accept(x, n, **kw) or not keep_ok(x, n, 0.0 if kw.get("core_ok") else 0.0): continue
        add(names[rng.integers(len(names))], x, n, float(tz(np.array(x), np.array(n))) - 0.02, rng.uniform(0, 6.3), rng.uniform(*scale)); n_ok += 1
meadow(["Flower_3_Single", "Flower_4_Single"], 150, (0.8, 1.3), 0.58, 31, edge=3.0, solid=2.5, route=1.5, path=1.5, stream=1.0, slope=0.4)
meadow(["Flower_3_Group", "Flower_4_Group"], 60, (0.8, 1.2), 0.64, 37, edge=3.0, solid=3.0, route=2.0, path=1.8, stream=1.0, slope=0.35)
meadow(["Clover_1"], 160, (0.8, 1.4), 0.45, 41, edge=2.5, solid=1.5, route=1.0, path=1.2, stream=0.8, slope=0.45)
meadow(["Grass_Common_Tall", "Grass_Common_Short", "Grass_Wispy_Tall"], 420, (0.9, 1.5), 0.40, 43, edge=2.5, solid=1.5, route=0.8, path=1.0, stream=0.6, slope=0.6)

# ---------------------------------------------------------------------------------------------- tea terraces: contour rows (Bush_Common pruned as a tea-plant stand-in) with ground cover between
for k in range(6):
    for f in (0.22, 0.58):
        target = M.TEA_D0 + M.TEA_W * (k + f)
        for th in np.arange(math.radians(-64), math.radians(56), 1.15 / max(target, 8)):
            r = target
            for _ in range(4):
                p = LOOK + r * np.array([math.cos(th), math.sin(th)]); wob = 2.4 * M.field_noise(p[0], p[1], 91, (38, 21, 12), (1, 0.6, 0.35)); r = target - float(wob)
            p = LOOK + r * np.array([math.cos(th), math.sin(th)]); x, n = float(p[0]), float(p[1])
            if x < 49 or not (6 < n < 88) or not accept(x, n, edge=3.0, solid=2.0, route=1.2, path=1.5, stream=1.5, slope=0.22, pad_ok=True): continue
            z = float(tz(np.array(x), np.array(n))); tang = math.atan2(math.cos(th), -math.sin(th))
            add("Bush_Common", x, n, z - 0.04, tang + rng.uniform(-0.3, 0.3), rng.uniform(0.42, 0.56))
    # between the rows: clover and short grass strip (f 0.40), flowers at bench ends
    target = M.TEA_D0 + M.TEA_W * (k + 0.40)
    for th in np.arange(math.radians(-64), math.radians(56), 2.2 / max(target, 8)):
        p = LOOK + target * np.array([math.cos(th), math.sin(th)]); x, n = float(p[0]), float(p[1])
        if x < 49 or not (6 < n < 88) or not accept(x, n, edge=3.0, solid=2.0, route=1.2, path=1.5, stream=1.5, slope=0.25, pad_ok=True): continue
        add(["Clover_1", "Grass_Common_Short"][rng.integers(2)], x, n, float(tz(np.array(x), np.array(n))) - 0.02, rng.uniform(0, 6.3), rng.uniform(0.9, 1.3))

# ---------------------------------------------------------------------------------------------- rocks: crag foot, stream banks, path edges, cliff-top, ledge outcrops
ROCKS = ["Rock_Medium_1", "Rock_Medium_2", "Rock_Medium_3"]
def rock_at(x, n, s, solid=False, sink=0.25):
    z = float(tz(np.array(x), np.array(n))); add(ROCKS[rng.integers(3)], x, n, z - sink * s * 0.8, rng.uniform(0, 6.3), s)
    if solid: out["rocks_solid"].append(dict(x=round(x, 2), n=round(n, 2), r=round(1.15 * s, 2))); out["perches"]["rock"].append([round(x, 2), round(n, 2), round(z + 1.6 * s, 2)])
for _ in range(2500):                                                        # crag: boulder fields at the foot and on benches
    if sum(1 for k in inst if k.startswith("Rock_Medium") for _ in inst[k]) > 125: break
    x = rng.uniform(8, 84); n = rng.uniform(92, 128)
    if noise(x, n, 61, 10.0) < 0.48 or not accept(x, n, edge=4.0, solid=3.0, route=2.0, path=2.5, stream=2.0, slope=0.6) or not keep_ok(x, n, 2.0): continue
    rock_at(x, n, rng.uniform(0.9, 3.0), True)
for pth in range(len(M.PATHS)):                                              # path edges: pebbles and stepping stones, alternating sides
    nm, kind, w, pts = M.PATHS[pth]
    if kind == "road": continue
    Pd, _z = M._dense(pts, 0.5)
    for i in range(0, len(Pd), 5):
        if rng.uniform() > 0.55: continue
        d = Pd[min(i + 1, len(Pd) - 1)] - Pd[i]; ln = np.hypot(*d) or 1; perp = np.array([-d[1], d[0]]) / ln; side = rng.choice([-1, 1]); off = w / 2 + rng.uniform(0.15, 0.7); x, n = Pd[i] + perp * side * off
        if not accept(x, n, edge=2.0, solid=1.0, route=0.3, path=-5, stream=0.5, slope=0.7, pad_ok=True): continue
        z = float(tz(np.array(x), np.array(n)));
        add(["Pebble_Round_1", "Pebble_Round_3", "Pebble_Square_1", "Pebble_Square_3"][rng.integers(4)], x, n, z, rng.uniform(0, 6.3), rng.uniform(1.0, 2.2))
        if rng.uniform() < 0.12: add(["RockPath_Round_Small_1", "RockPath_Round_Small_2", "RockPath_Square_Small_1"][rng.integers(3)], x - perp[0] * side * 0.9, n - perp[1] * side * 0.9, z, rng.uniform(0, 6.3), 1.2)
Sd, _z = M._dense(M.WATER, 0.5)
for i in range(0, len(Sd), 4):                                               # stream banks: rocks and ferns / big plants
    d = Sd[min(i + 1, len(Sd) - 1)] - Sd[i]; ln = np.hypot(*d) or 1; perp = np.array([-d[1], d[0]]) / ln; side = rng.choice([-1, 1]); x, n = Sd[i] + perp * side * rng.uniform(1.4, 2.6)
    if not accept(x, n, edge=2.0, solid=2.0, route=1.0, path=1.0, stream=0.6, slope=0.7, pad_ok=True): continue
    z = float(tz(np.array(x), np.array(n)))
    if rng.uniform() < 0.35: rock_at(x, n, rng.uniform(0.5, 1.1), False, 0.3)
    else: add(["Fern_1", "Plant_1_Big", "Plant_7_Big"][rng.integers(3)], x, n, z - 0.03, rng.uniform(0, 6.3), rng.uniform(0.7, 1.2))
# rim rocks: sparse cluster on the cliff top (never on the quay, the Green core or the shelf front)
rim, th, L = M.rim_points(M.MAIN, 1.0)
for i in range(0, len(rim), 7):
    x, n = rim[i] - (rim[i] - np.array(M.CENTRE)) / np.linalg.norm(rim[i] - np.array(M.CENTRE)) * rng.uniform(1.4, 2.4)
    if rng.uniform() > 0.5 or n < -27 or not accept(x, n, edge=0.8, solid=3.0, route=1.5, path=1.5, stream=1.0, slope=0.9, pad_ok=False) or not keep_ok(x, n, 1.0): continue
    rock_at(x, n, rng.uniform(0.7, 1.7), False, 0.2)
# ledge outcrops on the cliff face (from the real shell rings): rocks half-buried in ledges, protruding outward
V, F, info = G.build_shell(M.MAIN); Nn = info["N"]; nr = info["rings"]; ringV = V.reshape(nr, Nn, 3); ledge_rings = [2 * s + 2 for s in range(4)]
ledges = []
for k in ledge_rings:
    for i in range(0, Nn, 9):
        if rng.uniform() > 0.45: continue
        p = ringV[k, i]; u = info["u"][i]; s = rng.uniform(1.4, 3.6); pos = p + np.array([u[0], u[1], 0]) * (0.02 * s) + np.array([0, 0, -0.3 * s])      # half buried in the ledge, not standing proud
        ledges.append([round(float(pos[0]), 2), round(float(pos[1]), 2), round(float(pos[2]), 2), round(float(rng.uniform(0, 6.3)), 2), round(float(s), 2)])
        if len(ledges) > 120: break
out["ledge_rocks"] = ledges
# P3-B batch 3 (crag + Cloudfall pass): scree at the foot of the crag risers and planting along the last stretch of the stream (separate generator)
n_scree = 0
for _ in range(9000):
    if n_scree >= 460: break
    x = rng2.uniform(6, 86); n = rng2.uniform(92, 134)
    if at(SLOPE, x, n) < 0.26 or not accept(x, n, edge=2.0, solid=0.8, route=0.4, path=1.6, stream=1.0, slope=0.9, pad_ok=True) or not keep_ok(x, n, 1.0): continue
    z = float(tz(np.array(x), np.array(n))); n_scree += 1
    if rng2.uniform() < 0.12: rock_at(x, n, rng2.uniform(0.35, 0.65), False, 0.3)
    else: add(["Pebble_Round_1", "Pebble_Round_3", "Pebble_Square_1", "Pebble_Square_3"][rng2.integers(4)], x, n, z - 0.02, rng2.uniform(0, 6.3), rng2.uniform(1.4, 2.8))
Sb, _z = M._dense([p for p in M.WATER if p[0] > 62], 0.5); n_bank = 0
for i in range(len(Sb)):
    for _ in range(2):
        d = Sb[min(i + 1, len(Sb) - 1)] - Sb[max(i - 1, 0)]; ln = np.hypot(*d) or 1; perp = np.array([-d[1], d[0]]) / ln; side = rng2.choice([-1, 1]); x, n = Sb[i] + perp * side * rng2.uniform(0.9, 2.3)
        if not accept(x, n, edge=1.5, solid=1.5, route=0.8, path=1.0, stream=0.5, slope=0.8, pad_ok=True): continue
        z = float(tz(np.array(x), np.array(n))); n_bank += 1
        add(["Grass_Wispy_Tall", "Fern_1", "Plant_1_Big", "Grass_Common_Tall", "Plant_7_Big"][rng2.integers(5)], x, n, z - 0.03, rng2.uniform(0, 6.3), rng2.uniform(0.8, 1.4))
        if rng2.uniform() < 0.15: rock_at(x, n, rng2.uniform(0.4, 0.8), False, 0.3)
for lx, ln, ls in ((88.2, 62.9, 0.8), (89.6, 65.3, 0.7), (86.4, 63.2, 0.55), (87.6, 65.6, 0.5), (85.0, 65.6, 0.6), (89.2, 63.0, 0.45)):      # lip stones: they break the water as it leaves the edge
    z = float(tz(np.array(lx), np.array(ln))); add(ROCKS[rng2.integers(3)], lx, ln, z - 0.22 * ls, rng2.uniform(0, 6.3), ls)
out["_batch3"] = dict(scree=n_scree, bank_plants=n_bank)

# ---------------------------------------------------------------------------------------------- perches
roof = {}
for o in sc["collision"]:
    if o.get("cameraOnly") and o.get("group") == "roof" and o["src"] in ("B02", "B03", "B05", "B06", "B07", "B08", "B09", "B13", "B14", "B17", "E04", "E06", "A11a", "B15", "B16", "B01", "B10", "B12"):
        k = o["src"]
        if k not in roof or o["h"] > roof[k]["h"]: roof[k] = o
for k, o in roof.items():
    out["perches"]["roof"].append(dict(src=k, x=round(o["x"], 2), n=round(-o["z"], 2), z=round(o["h"], 2), w=round(o["w"], 2), d=round(o["d"], 2)))
for (px, pn, nm) in ((5.0, -73.6, "Sky Quay beacon"), (34.5, -47.0, "crane jib"), (111.0, 45.0, "pavilion roof"), (-9.2, -56.0, "lamp w"), (9.2, -56.0, "lamp e"), (-9.2, -39.5, "lamp w2"), (9.2, -39.5, "lamp e2")):
    z = {"Sky Quay beacon": 10.9 - 3.0, "crane jib": -3.0 + 5.4, "pavilion roof": float(M.stack_top(np.array(111.0), np.array(45.0))) + 4.9}.get(nm, -3.0 + 3.95); out["perches"]["prop"].append(dict(name=nm, x=px, n=pn, z=round(z, 2)))

# ---------------------------------------------------------------------------------------------- habitats (defined by what must be true there; points validated against the fields)
def open_dirs(x, n):
    """Escape routes: of 12 bearings, how many are free (walkable, gentle, outside trunk/boulder proxies) out to 6 m."""
    c = 0
    for k in range(12):
        ang = k * math.pi / 6; ok = True
        for d in (1.5, 3.0, 4.5, 6.0):
            px, pn = x + d * math.cos(ang), n + d * math.sin(ang)
            if not accept(px, pn, edge=1.0, solid=0.3, route=0.0, path=-9, stream=0.0, slope=0.6, pad_ok=True) or any(math.hypot(px - o['x'], pn - o['n']) < o['r'] + 0.4 for o in out['trunks'] + out['rocks_solid']): ok = False; break
        c += ok
    return c


def points(cx, cn, r0, r1, count, *, slope=0.3, edge=4.0, solid=3.0, route=2.0, path=1.0, stream=1.5, min_sep=3.0, pad_ok=False, keep=True, cover=None, tries=3000, ang=None):
    pts = []
    for _ in range(tries):
        if len(pts) >= count: break
        a = rng.uniform(0, 2 * math.pi) if ang is None else rng.uniform(*ang); r = math.sqrt(rng.uniform(r0 * r0, r1 * r1)); x, n = cx + r * math.cos(a), cn + r * math.sin(a)
        if not accept(x, n, edge=edge, solid=solid, route=route, path=path, stream=stream, slope=slope, pad_ok=pad_ok) or (keep and not keep_ok(x, n, 1.5)): continue
        if any(math.hypot(x - c['x'], n - c['n']) < c['r'] + 0.9 for c in out['trunks'] + out['rocks_solid']): continue          # never inside a trunk or boulder proxy
        if open_dirs(x, n) < 5: continue
        if cover and not any(math.hypot(x - c[0], n - c[1]) < cover[0] for c in cover[1]): continue
        if any(math.hypot(x - p[0], n - p[1]) < min_sep for p in pts): continue
        pts.append((round(float(x), 2), round(float(n), 2)))
    return pts


bush_xy = [(x, n) for k in ("Bush_Common", "Bush_Common_Flowers") for x, n, *_ in inst.get(k, [])]
tree_xy = [(t[0], t[1]) for t in trees]; rock_xy = [(r["x"], r["n"]) for r in out["rocks_solid"]]
cover_xy = bush_xy + tree_xy + rock_xy
HAB = {}
HAB["A_settlement"] = dict(name="Merchant settlement: back yards and service court", density="sparse", radius=7.0,
    species={"Chick": 4, "Cat": 2, "Pug": 1, "Pig": 2, "Bird": 6},
    ground_zones=[dict(name="artisan back yard", cx=-29.5, cn=14.0, r0=0, r1=5.5), dict(name="porters yard", cx=42.0, cn=28.0, r0=0, r1=3.2), dict(name="quay service corner", cx=22.0, cn=-44.0, r0=0, r1=5.0)])
HAB["B_caravan_green"] = dict(name="Caravan Green meadow (annulus outside the 9 m landing core)", density="moderate", radius=17.0,
    species={"Sheep": 5, "Lamb": 2, "Llama": 2, "Horse": 2, "Cow": 2, "Bird": 2, "Swallowtail": 6}, ground_zones=[dict(name="green annulus", cx=-50.0, cn=18.0, r0=10.5, r1=17.0)])
HAB["C_counting_crag"] = dict(name="Counting Crag benches and foot", density="sparse", radius=26.0,
    species={"RedFox": 2, "Eagle": 2, "Bird": 2}, ground_zones=[dict(name="crag benches", cx=46.0, cn=106.0, r0=0, r1=26.0)])
HAB["D_tea_terraces"] = dict(name="Tea terraces", density="sparse to moderate", radius=30.0,
    species={"Llama": 2, "Bird": 3, "Swallowtail": 6}, ground_zones=[dict(name="terrace benches", cx=70.0, cn=42.0, r0=0, r1=24.0)])
HAB["E_cloudfall"] = dict(name="Cloudfall stream and overlook", density="sparse", radius=18.0, species={"Bird": 2, "Swallowtail": 4}, ground_zones=[])
HAB["F_tea_lookout_stack"] = dict(name="Tea Lookout and Tea Stack", density="very sparse", radius=14.0, species={"Bird": 1, "Swallowtail": 2}, ground_zones=[dict(name="lookout lawn", cx=32.0, cn=52.0, r0=0, r1=6.0)])
HAB["G_sky_quay"] = dict(name="Sky Quay", density="restrained", radius=30.0, species={"Bird": 2, "Dog": 1}, ground_zones=[dict(name="quay service corner", cx=22.0, cn=-44.0, r0=0, r1=5.0)])
out["habitats"] = HAB
# validated home points for ground species
GROUND = {"Sheep": "open", "Lamb": "open", "Cow": "open", "Horse": "open", "Llama": "open", "RedFox": "cover", "Chick": "yard", "Cat": "yard", "Pug": "yard", "Pig": "yard", "Dog": "yard"}
homes = {}
def zone_pts(z, n, kind):
    kw = dict(slope=0.3, edge=4.0, solid=3.0, route=2.0, stream=1.5, min_sep=3.0)
    if kind == "yard": kw.update(solid=1.0, route=1.6, edge=2.0, pad_ok=True, min_sep=1.2, slope=0.2)
    if kind == "rocky": kw.update(slope=0.45, solid=3.0, min_sep=4.0)
    if kind == "water": kw.update(stream=0.4, slope=0.4)
    p = points(z["cx"], z["cn"], z["r0"], z["r1"], n * 6, cover=(5.0, cover_xy) if kind == "cover" else None, **kw)
    if kind == "rocky": p = [q for q in p if any(math.hypot(q[0] - r[0], q[1] - r[1]) < 7 for r in rock_xy)] or p
    return p[:n * 3]
for hid, h in HAB.items():
    h["homes"] = {}
    for sp, cnt in h["species"].items():
        if sp in GROUND and cnt:
            pool = []
            for z in h["ground_zones"]:
                pool += zone_pts(z, cnt, GROUND[sp])
            h["homes"][sp] = [list(p) for p in pool[:max(cnt * 3, 3)]]
# habitat sanity
chk = {}
for hid, h in HAB.items():
    for sp, pts in h["homes"].items():
        for (x, n) in pts: chk.setdefault(hid, []).append(dict(sp=sp, slope=float(at(SLOPE, x, n)), edge=float(at(EDGE, x, n)), solid=float(at(D_SOLID, x, n)), route=float(at(D_ROUTE, x, n))))
out["_counts"] = {k: len(v) for k, v in inst.items()}; out["_totals"] = dict(instances=sum(len(v) for v in inst.values()), trees=len(trees), ledge_rocks=len(ledges), habitats={h: {sp: len(p) for sp, p in HAB[h]["homes"].items()} for h in HAB})
json.dump(out, open(OUT, "w"), separators=(",", ":"))
if EV:
    os.makedirs(EV, exist_ok=True); rep = dict(totals=out["_totals"], counts=out["_counts"], placement_checks={h: dict(n=len(v), max_slope=max(i["slope"] for i in v), min_edge=min(i["edge"] for i in v), min_solid=min(i["solid"] for i in v), min_route=min(i["route"] for i in v)) for h, v in chk.items()})
    json.dump(rep, open(os.path.join(EV, "scatter-report.json"), "w"), indent=1)
print(json.dumps(out["_totals"]), os.path.getsize(OUT))
