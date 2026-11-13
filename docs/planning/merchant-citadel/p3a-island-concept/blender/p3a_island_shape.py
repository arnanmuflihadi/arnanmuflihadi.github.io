"""Merchant Citadel P3-A: floating-island CONCEPT shapes (massing prototypes, not production terrain).

Pure numpy, no bpy: the Blender massing script (p3a_island_blender.py) and the measured plan (p3a_plan.py) both import this file,
so every image of a concept uses one spatial arrangement.

Frame: plan x east, n north (Blender x, y), z up, metres. Datum: paved street level 0.01, stand-in ground 0.
A landmass is a star-shaped polar solid round a centre: rim radius R(theta), top height h(x, n), and below the rim a stack of
rings whose radius shrinks with depth (cliff with strata ledges, then an underside that tapers to an offset apex).
"""
import math
import numpy as np

TAU = 2 * math.pi
TEA = (6.0, 6.5, 1.7)                # tea benches: first contour 6 m + one bench width from the lookout, bench width, step height (m)
GROUND = -0.02                      # grass level under the town (paving top is +0.01)
PAD = (-34.0, 44.0, -20.0, 73.2)    # x0, x1, n0, n1: the town must stand on flat ground inside this rectangle (plus the hall shelf)


# ------------------------------------------------------------------ small deterministic helpers
def smooth(a, b, v):
    t = np.clip((np.asarray(v, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def catmull_periodic(ctrl, theta):
    """ctrl: [(deg, value)] sorted by deg; periodic Catmull-Rom in angle."""
    ang = np.array([math.radians(a) for a, _ in ctrl]); val = np.array([v for _, v in ctrl], float); n = len(ctrl)
    th = np.mod(np.asarray(theta, float), TAU); out = np.zeros_like(th)
    ext = np.concatenate([ang, [ang[0] + TAU]])
    idx = np.clip(np.searchsorted(ext, th, side="right") - 1, 0, n - 1)
    for i in range(n):
        m = idx == i
        if not m.any():
            continue
        a0, a1 = ext[i], ext[i + 1]; t = (th[m] - a0) / (a1 - a0)
        p0, p1, p2, p3 = val[(i - 1) % n], val[i], val[(i + 1) % n], val[(i + 2) % n]
        out[m] = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
    return out


def ring_noise(theta, seed, freqs=(3, 5, 8, 13, 21, 34), amps=(1.0, 0.7, 0.5, 0.35, 0.22, 0.14)):
    """Periodic noise in angle, roughly -1..1."""
    rng = np.random.default_rng(seed); th = np.asarray(theta, float); out = np.zeros_like(th)
    for f, a in zip(freqs, amps):
        out += a * np.sin(f * th + rng.uniform(0, TAU))
    return out / sum(amps)


def field_noise(x, y, seed, waves=(60, 34, 19, 11), amps=(1.0, 0.6, 0.35, 0.2)):
    rng = np.random.default_rng(seed); out = np.zeros_like(np.asarray(x, float))
    for w, a in zip(waves, amps):
        for _ in range(2):
            d = rng.uniform(0, TAU); out += a * np.sin((np.cos(d) * x + np.sin(d) * y) * TAU / w + rng.uniform(0, TAU))
    return out / (2 * sum(amps))


def rect_dist(x, y, r):
    """Distance outside rectangle r = (x0, x1, y0, y1); 0 inside."""
    dx = np.maximum(np.maximum(r[0] - x, x - r[1]), 0.0); dy = np.maximum(np.maximum(r[2] - y, y - r[3]), 0.0)
    return np.hypot(dx, dy)


# ------------------------------------------------------------------ shared pieces of the top surface
def hall_shelf(x, y):
    """Ground rises 2 m beside and behind the Exchange Hall so the podium (2.01 m) becomes a cut shelf, not a slab with 2 m drops.
    Stays at datum south of n 73.2 (B15, B16 and the tea house stand at datum up to n 72.3)."""
    s = 2.0 * smooth(73.2, 76.0, y) * (1 - smooth(40.0, 50.0, np.abs(x)))
    inner = (np.abs(x) < 14.3) & (y > 61.5) & (y < 74.0)          # the built terrace (1.01 m): terrain stays under it
    s = np.where(inner, 0.0, s)
    under = (np.abs(x) < 14.3) & (y >= 74.0) & (y < 90.2)         # under the podium deck: just below 2.01
    return np.where(under, 1.9, s)


def rim_lip(x, y, c, height=0.7, width=5.0):
    d = edge_distance(x, y, c)
    return height * (1 - smooth(1.2, width, d))


def edge_distance(x, y, c):
    cx, cy = c["centre"]; r = np.hypot(x - cx, y - cy); th = np.arctan2(y - cy, x - cx)
    return outline(c, th) - r


# ------------------------------------------------------------------ concept definitions
def _height_A(x, y, c):
    out = rect_dist(x, y, PAD); far = smooth(4.0, 16.0, out)
    h = GROUND + hall_shelf(x, y) + 0.5 * far * field_noise(x, y, 11) + rim_lip(x, y, c)
    h += 3.5 * np.exp(-(((x + 44) / 14) ** 2 + ((y - 78) / 12) ** 2)) * far                       # one low knoll north-west
    return h


def _height_B(x, y, c):
    out = rect_dist(x, y, PAD); far = smooth(4.0, 14.0, out)
    h = GROUND + hall_shelf(x, y) + 0.6 * far * field_noise(x, y, 23) + rim_lip(x, y, c, 0.9)
    h += -3.2 * smooth(-46.0, -50.0, x)                                                            # west block dropped along a fault scarp
    h += 4.5 * smooth(96.0, 101.0, y) * smooth(18.0, 26.0, x)                                      # north-east block lifted
    return h


def _height_C(x, y, c):
    out = rect_dist(x, y, PAD); far = smooth(4.0, 14.0, out)
    h = GROUND + hall_shelf(x, y) + 0.45 * far * field_noise(x, y, 37) * smooth(-33.0, -27.0, y) + rim_lip(x, y, c, 0.6)
    # the Counting Crag: an asymmetric layered outcrop north-east of the hall, a lower shoulder north-west
    g = 21.0 * np.exp(-(((x - 40) / 30) ** 2 + ((y - 116) / 16) ** 2))
    g = g + 2.2 * field_noise(x, y, 5, (26, 14, 8), (1, 0.6, 0.3)) * smooth(2.0, 8.0, g)
    table = np.minimum(11.0 * np.exp(-(((x + 36) / 24) ** 2 + ((y - 112) / 14) ** 2)), 7.2)        # the Shoulder Table: a flat-topped bench, 7.2 m
    g = g + table
    bench = np.round(g / 3.6) * 3.6
    g = (0.28 * g + 0.72 * bench) * smooth(95.0, 103.0, y)
    h += np.maximum(g, 0.0)
    # tea terraces: contour benches stepping down east of the lookout (36, 57) to the eastern cliff
    d = np.hypot(x - 36.0, y - 57.0); sector = smooth(44.5, 47.5, x) * (1 - smooth(84.0, 94.0, y)) * smooth(-2.0, 8.0, y)
    k = np.clip(np.floor((d - TEA[0]) / TEA[1]), 0, 5)
    h += -TEA[2] * k * sector
    # the Sky Quay: a lower landing shelf on the southern prow, reached by a broad stair from the arrival court
    h += -3.0 * smooth(-25.0, -31.0, y)
    return h


def _clear(c):
    return c


CONCEPTS = {
    "A": {
        "key": "A", "name": "Merchant Plateau", "centre": (5.0, 40.0), "seed": 101,
        "ctrl": [(0, 62), (40, 72), (80, 66), (100, 66), (135, 72), (180, 58), (225, 64), (262, 66), (270, 76), (278, 66), (315, 68)],
        "rim_noise": 2.2, "notches": [],
        "depth": lambda th: 52 + 6 * np.sin(th - 1.0), "cliff": 20.0, "cliff_batter": 0.10, "taper": 0.8, "apex": (8.0, 8.0), "keel": 0.0, "overhang": 0.0,
        "height": _height_A, "satellites": [],
    },
    "B": {
        "key": "B", "name": "Fractured Trading Isle", "centre": (2.0, 44.0), "seed": 202,
        "ctrl": [(0, 60), (25, 74), (50, 88), (80, 72), (100, 70), (125, 82), (150, 70), (180, 66), (210, 76), (240, 66), (262, 66), (270, 70), (278, 66), (300, 68), (330, 70)],
        "rim_noise": 3.6, "notches": [(18, 9, 16), (112, 7, 14), (196, 8, 15), (322, 7, 12)],
        "depth": lambda th: 52 + 30 * np.cos(th - 0.9), "cliff": 16.0, "cliff_batter": -0.10, "taper": 1.45, "apex": (24.0, 30.0), "keel": 0.0, "overhang": 2.6,
        "height": _height_B,
        "satellites": [
            {"key": "B-quay", "name": "arrival shard", "centre": (0.0, -62.0), "seed": 211, "top": -2.0,
             "ctrl": [(0, 24), (60, 20), (90, 23), (120, 20), (180, 25), (240, 22), (270, 30), (300, 22)], "rim_noise": 1.6, "notches": [],
             "depth": lambda th: 34 + 0 * th, "cliff": 9.0, "cliff_batter": -0.05, "taper": 1.3, "apex": (0.0, -8.0), "keel": 0.0, "overhang": 1.2},
            {"key": "B-stack", "name": "lookout stack", "centre": (84.0, 58.0), "seed": 212, "top": 2.5,
             "ctrl": [(0, 12), (90, 14), (180, 11), (270, 13)], "rim_noise": 1.0, "notches": [],
             "depth": lambda th: 48 + 0 * th, "cliff": 18.0, "cliff_batter": 0.02, "taper": 1.6, "apex": (3.0, 0.0), "keel": 0.0, "overhang": 0.8},
            {"key": "B-slab", "name": "broken north-west slab", "centre": (-84.0, 104.0), "seed": 213, "top": -9.0,
             "ctrl": [(0, 22), (70, 16), (140, 24), (200, 18), (290, 20)], "rim_noise": 1.8, "notches": [],
             "depth": lambda th: 22 + 0 * th, "cliff": 7.0, "cliff_batter": -0.04, "taper": 1.2, "apex": (-4.0, 4.0), "keel": 0.0, "overhang": 1.0},
        ],
    },
    "C": {
        "key": "C", "name": "Terraced Merchant Highlands", "centre": (5.0, 42.0), "seed": 303,
        "ctrl": [(0, 90), (22, 94), (45, 104), (70, 98), (90, 94), (115, 98), (140, 96), (165, 86), (185, 88), (210, 84), (235, 74), (250, 72), (258, 108), (270, 122), (282, 108), (290, 70), (305, 70), (330, 80)],
        "rim_noise": 3.0, "notches": [(12, 5, 13), (154, 6, 11), (238, 6, 10)],
        "depth": lambda th: 48 + 46 * (0.5 + 0.5 * np.cos(th - math.radians(72))), "cliff": 23.0, "cliff_batter": 0.05, "taper": 0.62, "apex": (6.0, 10.0), "keel": 0.30, "keel_len": 46.0, "overhang": 1.0,
        "height": _height_C, "satellites": [],
    },
}


def outline(c, theta):
    th = np.asarray(theta, float)
    r = catmull_periodic(c["ctrl"], th) + c["rim_noise"] * ring_noise(th, c["seed"])
    for deg, width, depth in c.get("notches", []):                   # fractures: narrow V bites into the rim
        d = np.abs(np.arctan2(np.sin(th - math.radians(deg)), np.cos(th - math.radians(deg)))) / math.radians(width)
        r = r - depth * np.clip(1 - d, 0, 1) ** 1.4
    return r


def top_height(c, x, y):
    if "height" in c:
        return c["height"](np.asarray(x, float), np.asarray(y, float), c)
    return c["top"] + 0.4 * field_noise(x, y, c["seed"]) + rim_lip(np.asarray(x, float), np.asarray(y, float), c, 0.5, 3.0)


STRATA = 5.5                        # metres per rock layer in the cliff


def ring_radius(c, theta, depth):
    """Radius of the solid at `depth` metres below the rim, for bearing theta. depth = 0 is the rim."""
    th = np.asarray(theta, float); R = outline(c, th); D = np.asarray(c["depth"](th), float); Dc = c["cliff"]
    dep = np.asarray(depth, float)
    layer = np.floor(dep / STRATA); step = (np.mod(layer, 2) * 1.6 + np.mod(layer, 3) * 0.7)          # alternating ledges and recesses
    wob = 1.5 * ring_noise(th * 1.0 + layer * 0.9, c["seed"] + 7, (7, 12, 19, 31), (1, 0.7, 0.5, 0.3))
    inset_cliff = c["cliff_batter"] * np.minimum(dep, Dc) + (step + wob) * smooth(0.3, 2.5, dep) - c["overhang"] * np.exp(-((dep - 3.0) / 2.5) ** 2)
    t = np.clip((dep - Dc) / np.maximum(D - Dc, 1.0), 0.0, 1.0)
    lump = 1 + 0.16 * ring_noise(th * 1.0 + t * 3.0, c["seed"] + 13, (2, 4, 7, 11), (1, 0.8, 0.5, 0.3)) * np.sin(math.pi * t) ** 0.6
    keel = 1 - c["keel"] * t * np.abs(np.cos(th)) ** 1.5                                               # C: squeeze east-west with depth: a keel running north-south
    under = (1 - t) ** c["taper"]                                                                  # < 1 bulbous hull, 1 cone, > 1 thin hanging root
    r = (R - inset_cliff) * np.where(dep > Dc, np.clip(under, 0, 1) * lump * keel, 1.0)
    return np.maximum(r, 0.0), D


def depth_levels(c):
    D = 95.0
    lv = list(np.arange(0.0, c["cliff"] + 0.01, 1.1)) + list(np.linspace(c["cliff"] + 1.5, D, 34))
    return np.array(lv)


def contains(c, x, y, margin=0.0):
    return edge_distance(np.asarray(x, float), np.asarray(y, float), c) >= margin


# ------------------------------------------------------------------ design features of each concept (used by massing and plan)
FEATURES = {
    "A": {
        "paths": [[(0, -8), (0, -16), (0, -30)], [(42, 57), (56, 60), (62, 52)], [(-24, 20), (-40, 22), (-48, 30)]],
        "water": [], "falls": [],
        "landing": [("North-east lawn", 24, 89, 8), ("East common", 50, 26, 7.5)],
        "viewpoints": [("Tea lookout", 36, 57, 0), ("Hall headland", 0, 100, 90)],
        "woods": [(-44, 78, 16, 22), (40, 92, 14, 14), (-30, -10, 10, 8)],
    },
    "B": {
        "paths": [[(0, -8), (0, -16), (0, -28), (0, -44), (0, -60)], [(42, 57), (58, 58), (72, 58), (84, 58)], [(-24, 20), (-44, 22), (-58, 26)], [(-20, 92), (-40, 100), (-62, 100)]],
        "water": [], "falls": [],
        "bridges": [((0, -20.0), (0, -42.0), 5.0, 0.2, -1.9), ((62.0, 57.0), (75.0, 58.0), 2.2, 0.9, 2.6)],
        "landing": [("Arrival shard", 0, -62, 12), ("North-west lawn", -30, 94, 11)],
        "viewpoints": [("Tea lookout", 36, 57, 0), ("Lookout stack", 84, 58, 0), ("Chasm bridge", 0, -35, 270)],
        "woods": [(-36, 86, 14, 20), (44, 104, 12, 10), (-62, 44, 10, 14)],
    },
    "C": {
        "paths": [[(0, -8), (0, -16), (0, -24), (0, -32), (0, -44), (0, -58)],                                 # arrival axis to the Sky Quay
                  [(42, 57), (50, 57), (60, 54), (70, 52), (80, 54)],                                              # tea promenade to the cloudfall overlook
                  [(-24, 20), (-30, 20), (-36, 22)],                                                    # artisan gate to the Caravan Green
                  [(18, 92), (26, 98), (22, 106), (32, 110), (40, 114)],                                           # crag stair to the Counting Stone
                  [(-16, 92), (-24, 100), (-30, 106)],                                                             # west shoulder path
                  [(33, 20), (44, 18), (52, 24), (58, 36), (60, 48), (60, 54)]],                                   # porters' loop through the lower tea benches
        "water": [[(36, 104), (44, 96), (50, 88), (56, 80), (63, 72), (70, 68), (78, 66), (88, 64)]],          # spring on the crag, stream along the benches
        "falls": [((90.0, 64.0), 30.0)],                                                                         # the Cloudfall: off the eastern cliff
        "landing": [("Caravan Green", -50, 18, 14), ("Sky Quay", 5, -52, 11), ("Shoulder Table", -36, 112, 6), ("Hall lawn (west)", -32.5, 85, 7.5)],
        "viewpoints": [("Tea lookout", 36, 57, 0), ("Cloudfall overlook", 80, 54, 10), ("Counting Stone", 40, 116, 220), ("Sky Quay prow", 0, -70, 270)],
        "woods": [(34, 112, 28, 12), (-50, 100, 10, 8), (-18, 116, 10, 6), (-70, 62, 9, 16), (-52, -14, 12, 7), (52, -8, 10, 8), (68, 96, 10, 8), (-36, 60, 7, 12)],
    },
}


# ------------------------------------------------------------------ the selected design: concept C refined after the comparison
# Borrowed from B: one detached stack (the Tea Stack) off the eastern cliff as the focal point of the lookout panorama, and long
# hanging roots under the thick northern end. Everything else is concept C unchanged, so the comparison images stay valid.
CONCEPTS["S"] = dict(CONCEPTS["C"]); CONCEPTS["S"].update({
    "key": "S", "base": "C", "name": "Terraced Merchant Highlands with the Tea Stack (selected)", "roots": 7,
    "satellites": [{"key": "S-stack", "name": "Tea Stack", "centre": (111.0, 45.0), "seed": 311, "top": -5.0,
                    "ctrl": [(0, 11), (70, 9), (130, 12), (200, 10), (290, 12)], "rim_noise": 1.0, "notches": [],
                    "depth": lambda th: 62 + 0 * th, "cliff": 20.0, "cliff_batter": 0.03, "taper": 1.7, "apex": (2.0, -1.0), "keel": 0.0, "overhang": 0.9}]})
FEATURES["S"] = dict(FEATURES["C"]); FEATURES["S"].update({
    "bridges": [((93.5, 46.0), (101.5, 45.6), 2.0, -7.6, -4.8)],
    "ponds": [(36.0, 104.0, 4.5)],
    "pavilions": [(111.0, 45.0, 5.0, 5.5)],
    "viewpoints": FEATURES["C"]["viewpoints"] + [("Tea Stack", 111, 45, 0)],
})
