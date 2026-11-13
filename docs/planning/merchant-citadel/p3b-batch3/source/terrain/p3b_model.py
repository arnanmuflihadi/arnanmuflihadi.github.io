"""Merchant Citadel P3-B batch 1: the authoritative spatial definition of the floating island (Concept S, refined).

Pure numpy (no bpy, no scipy) so that the same file runs in system Python (runtime export, measurements) and inside Blender (mesh build).
ONE definition feeds: the walkable height grid shipped to the browser, the visible top mesh, the cliff/underside shell, vegetation placement,
clearings and the checks. Nothing is hand-sculpted.

Frame: plan x east, n north (Blender x, y), z up, metres. Three.js position = (x, z_up, -n).
Datum: paving top 0.01, stand-in ground under the town -0.02 (see GROUND).

Refinements relative to the P3-A concept (p3a_island_shape.py), each one visible in the geometry:
  * tea benches: wobbling contours, soft eroded risers, riser height fades in with distance from the town instead of a wall at x 47
  * counting crag: benches from a warped quantisation (no sawtooth), switchback ascent cut as a graded path
  * every walking route is a graded path (cut/fill with shoulders), so ramps and slopes are authored, not accidental
  * quay: a 14 m wide graded ramp (the stair of P3-A could not be both a mesh and a heightfield at 1 m resolution) between retaining walls
  * cliffs: strata of unequal thickness, ledges that pinch out, fractures, buttresses, three hero formations
  * underside: keel ridge + lumps + hanging boulders instead of a smooth bulb
"""
import math
import numpy as np

TAU = 2 * math.pi
GROUND = -0.02
PAD = (-34.0, 44.0, -20.0, 73.2)            # town pad (x0, x1, n0, n1): flat, exact
CENTRE = (5.0, 42.0)
LOOKOUT = (36.0, 57.0)
TEA_D0, TEA_W, TEA_STEP = 6.0, 6.5, 1.7
NOSUP = -80.0                               # support height outside the island (m): a fall target, below minY
MAX_SLOPE = 0.90                            # walkable slope limit (rise/run); riser walls are steeper
COMFORT_SLOPE = 0.60                        # "safe ground" (recovery point) limit
RIM_MARGIN = 1.2                            # m from the rim edge that the body can reach
STRATA_BASE = 5.5

# ---------------------------------------------------------------------------------------------------- helpers


def smooth(a, b, v):
    t = np.clip((np.asarray(v, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def catmull_periodic(ctrl, theta):
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
    dx = np.maximum(np.maximum(r[0] - x, x - r[1]), 0.0); dy = np.maximum(np.maximum(r[2] - y, y - r[3]), 0.0)
    return np.hypot(dx, dy)


# ---------------------------------------------------------------------------------------------------- landmasses (rim outlines)
MAIN = {
    "key": "main", "centre": CENTRE, "seed": 303,
    "ctrl": [(0, 90), (22, 94), (45, 104), (70, 98), (90, 94), (115, 98), (140, 96), (165, 86), (185, 88), (210, 84), (235, 74), (250, 72), (258, 108), (270, 122), (282, 108), (290, 70), (305, 70), (330, 80)],
    "rim_noise": 3.0, "notches": [(12, 5, 13), (154, 6, 11), (238, 6, 10)],
}
STACK = {
    "key": "stack", "centre": (111.0, 45.0), "seed": 311,
    "ctrl": [(0, 11), (70, 9), (130, 12), (200, 10), (290, 12)], "rim_noise": 1.0, "notches": [], "top": -5.0,
}


def outline(c, theta):
    th = np.asarray(theta, float)
    r = catmull_periodic(c["ctrl"], th) + c["rim_noise"] * ring_noise(th, c["seed"])
    r = r + 0.9 * ring_noise(th, c["seed"] + 5, (47, 61, 83, 109), (1, 0.7, 0.5, 0.3)) * (c["rim_noise"] / 3.0)     # fine rim breakup (P3-B)
    for deg, width, depth in c.get("notches", []):
        d = np.abs(np.arctan2(np.sin(th - math.radians(deg)), np.cos(th - math.radians(deg)))) / math.radians(width)
        r = r - depth * np.clip(1 - d, 0, 1) ** 1.4
    return r


def edge_distance(c, x, y):
    cx, cy = c["centre"]; r = np.hypot(np.asarray(x, float) - cx, np.asarray(y, float) - cy); th = np.arctan2(np.asarray(y, float) - cy, np.asarray(x, float) - cx)
    return outline(c, th) - r


def rim_points(c, spacing=1.0):
    """Closed polyline of the rim, resampled by arc length. Returns (N,2) plan points and the bearing of each."""
    th = np.linspace(0, TAU, 8001)[:-1]; r = outline(c, th); cx, cy = c["centre"]
    p = np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1)
    seg = np.linalg.norm(np.roll(p, -1, 0) - p, axis=1); s = np.concatenate([[0], np.cumsum(seg)]); L = s[-1]
    m = int(round(L / spacing)); target = np.linspace(0, L, m, endpoint=False)
    pe = np.concatenate([p, p[:1]]); xs = np.interp(target, s, pe[:, 0]); ys = np.interp(target, s, pe[:, 1])
    pts = np.stack([xs, ys], 1); return pts, np.arctan2(ys - cy, xs - cx), L


def inside(x, y, margin=0.0):
    return (edge_distance(MAIN, x, y) >= margin) | (edge_distance(STACK, x, y) >= margin)


# ---------------------------------------------------------------------------------------------------- features that shape the terrain
def hall_shelf(x, y):
    """The ground rises 2 m beside and behind the Exchange Hall: the podium (2.01 m) becomes a cut shelf, not a slab with 2 m drops."""
    s = 2.0 * smooth(73.2, 76.0, y) * (1 - smooth(40.0, 50.0, np.abs(x)))
    inner = (np.abs(x) < 14.3) & (y > 61.5) & (y < 74.0)
    s = np.where(inner, 0.0, s)
    under = (np.abs(x) < 14.3) & (y >= 74.0) & (y < 90.2)
    return np.where(under, 1.9, s)


def _benchify(u, lo=0.70, hi=1.0):
    k = np.floor(u); f = u - k
    return k + smooth(lo, hi, f)


def crag(x, n):
    g = 21.0 * np.exp(-(((x - 40) / 30) ** 2 + ((n - 116) / 16) ** 2))
    g = g + 2.4 * field_noise(x, n, 5, (26, 14, 8), (1, 0.6, 0.3)) * smooth(2.0, 8.0, g)
    # a broken north face: a second, lower knob east and a saddle, so the crag is not a single dome
    g = g + 5.0 * np.exp(-(((x - 70) / 10) ** 2 + ((n - 104) / 9) ** 2)) - 3.0 * np.exp(-(((x - 58) / 5) ** 2 + ((n - 110) / 8) ** 2))
    u = g / 3.6 + 0.35 * field_noise(x, n, 77, (23, 13, 7), (1, 0.6, 0.3))
    ben = 3.6 * _benchify(np.maximum(u, 0.0), 0.62, 1.0)
    table = np.minimum(11.0 * np.exp(-(((x + 36) / 24) ** 2 + ((n - 112) / 14) ** 2)), 7.2)           # the Shoulder Table: flat-topped
    t_u = table / 3.6; ben_t = 3.6 * _benchify(t_u, 0.55, 1.0)
    return np.maximum(ben, ben_t) * smooth(95.0, 103.0, n) * (0.88 + 0.12 * smooth(0, 6, g))


def tea(x, n):
    """Tea contours around the lookout. The riser height grows with distance from the town; contours wobble."""
    d = np.hypot(x - LOOKOUT[0], n - LOOKOUT[1]) + 2.4 * field_noise(x, n, 91, (38, 21, 12), (1, 0.6, 0.35))
    u = np.clip((d - TEA_D0) / TEA_W, 0.0, 5.0)
    k = np.floor(u); f = u - k
    bench = k + smooth(0.78, 1.0, f)
    sector = smooth(47.0, 62.0, x) * (1 - smooth(84.0, 94.0, n)) * smooth(-2.0, 10.0, n)
    return -TEA_STEP * bench * sector


def quay(x, n):
    return -3.0 * smooth(-26.0, -29.5, n)


def meadow(x, n):
    out = rect_dist(x, n, PAD); far = smooth(4.0, 14.0, out)
    return 0.45 * far * field_noise(x, n, 37) * smooth(-33.0, -27.0, n) * (1 - smooth(60, 80, n) * 0.5)


# clearings: flat open ground kept flat on purpose (dragon landing examples, events, viewpoints). (name, x, n, radius, z or None -> local base)
CLEARINGS = [
    ("Caravan Green", -50.0, 18.0, 14.0, GROUND),
    ("Sky Quay", 5.0, -52.0, 11.0, -3.0),
    ("Shoulder Table", -36.0, 112.0, 6.0, None),
    ("Hall lawn west", -32.5, 85.0, 7.5, 2.0),
    ("Cloudfall overlook", 80.0, 54.0, 3.5, None),
    ("Counting Stone", 40.0, 116.0, 3.0, None),
]

# graded paths: (name, kind, width m, [(x, n) or (x, n, z)]) ; z pins fix the height at that vertex
PATHS = [
    ("Arrival ramp", "road", 14.0, [(0, -16, GROUND), (0, -24, GROUND), (0, -36, -3.0), (0, -52, -3.0)]),
    ("Tea promenade", "trail", 3.2, [(42, 57), (50, 57.5), (60, 55.5), (70, 53), (80, 54)]),
    ("Porters' loop", "trail", 2.6, [(33, 20), (44, 18), (52, 24), (58, 36), (60, 48), (60, 54)]),
    ("Crag ascent", "trail", 2.6, [(18, 84), (34, 88), (20, 95), (36, 101), (22, 107), (34, 111), (37.6, 113.8)]),
    ("West shoulder path", "trail", 2.6, [(-16, 84), (-24, 94), (-30, 103), (-31.5, 106.5)]),
    ("Green road", "trail", 3.2, [(-7, -11), (-16, -4), (-26, 5), (-35, 12), (-46, 16), (-50, 18)]),                       # arrival court to the Caravan Green round the south-west of the artisan block (found by A* on the real collision)
]

WATER = [(36, 104), (44, 96), (50, 88), (56, 80), (63, 72), (70, 68), (78, 66), (88, 64)]       # stream: spring on the crag to the Cloudfall
FALLS = ((90.0, 64.0), 30.0)


_DENSE = {}


def _dense(pts, step=0.25):
    key = (tuple(map(tuple, pts)), step)
    if key in _DENSE:
        return _DENSE[key]
    out = _dense_raw(pts, step); _DENSE[key] = out; return out


def _dense_raw(pts, step=0.25):
    out = [np.array(pts[0][:2], float)]; zz = [pts[0][2] if len(pts[0]) > 2 else None]
    for a, b in zip(pts[:-1], pts[1:]):
        pa, pb = np.array(a[:2], float), np.array(b[:2], float); L = np.linalg.norm(pb - pa); k = max(1, int(math.ceil(L / step)))
        for i in range(1, k + 1):
            out.append(pa + (pb - pa) * i / k); zz.append(None)
        zz[-1] = b[2] if len(b) > 2 else None
    return np.array(out), zz


_PATH_CACHE = {}


def path_profile(idx, base_fn):
    """Graded height profile along a path: base terrain smoothed, slope-clamped to 0.26, pinned where z is given."""
    if idx in _PATH_CACHE:
        return _PATH_CACHE[idx]
    name, kind, width, pts = PATHS[idx]; P, pins = _dense(pts); ds = 0.25
    pinned = [(i, p) for i, p in enumerate(pins) if p is not None]
    if len(pinned) >= 2:                                   # pinned path: piecewise linear between the pins (ramps, level quay)
        zs = np.empty(len(P)); zs[:] = pinned[0][1]
        for (a, za), (b, zb) in zip(pinned[:-1], pinned[1:]):
            zs[a:b + 1] = np.linspace(za, zb, b - a + 1)
        zs[pinned[-1][0]:] = pinned[-1][1]
    else:                                                  # trail: base terrain smoothed over 24 m, slope-clamped to 0.26
        z = base_fn(P[:, 0], P[:, 1]).astype(float); k = max(3, int(12 / ds))
        zs = np.convolve(np.pad(z, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid"); lim = 0.26 * ds
        for _ in range(3):
            for i in range(1, len(zs)):
                zs[i] = min(max(zs[i], zs[i - 1] - lim), zs[i - 1] + lim)
            for i in range(len(zs) - 2, -1, -1):
                zs[i] = min(max(zs[i], zs[i + 1] - lim), zs[i + 1] + lim)
    _PATH_CACHE[idx] = (P, zs); return P, zs


def _nearest_polyline(x, n, P):
    """Distance from points to a dense polyline and the index of the nearest sample (brute force, chunked)."""
    best = np.full(x.shape, 1e9); arg = np.zeros(x.shape, int)
    for i0 in range(0, len(P), 64):
        q = P[i0:i0 + 64]; d = np.hypot(x[..., None] - q[:, 0], n[..., None] - q[:, 1]); j = d.argmin(-1); dm = np.take_along_axis(d, j[..., None], -1)[..., 0]
        m = dm < best; best = np.where(m, dm, best); arg = np.where(m, i0 + j, arg)
    return best, arg


def terrain_nopath(x, n):
    x = np.asarray(x, float); n = np.asarray(n, float)
    h = GROUND + hall_shelf(x, n) + meadow(x, n) + crag(x, n) + tea(x, n) + quay(x, n)
    for _nm, cx, cn, r, z in CLEARINGS:
        d = np.hypot(x - cx, n - cn)
        zz = z if z is not None else float(np.mean([GROUND + hall_shelf(np.array(cx), np.array(cn)) + crag(np.array(cx), np.array(cn)) + tea(np.array(cx), np.array(cn))]))
        w = 1 - smooth(r, r + 6.0, d); h = h * (1 - w) + zz * w
    return h


def terrain(x, n):
    """The island top height (m) at plan points; defined everywhere (use `inside` to know where the island is). Accepts scalars and arrays."""
    x = np.asarray(x, float); n = np.asarray(n, float); shp = np.broadcast(x, n).shape
    return _terrain(np.atleast_1d(np.broadcast_to(x, shp)).astype(float), np.atleast_1d(np.broadcast_to(n, shp)).astype(float)).reshape(shp)


def _terrain(x, n):
    h = terrain_nopath(x, n).copy()
    for i, (name, kind, width, pts) in enumerate(PATHS):
        P, zs = path_profile(i, lambda a, b: terrain_nopath(a, b))
        x0, x1 = P[:, 0].min() - width, P[:, 0].max() + width; n0, n1 = P[:, 1].min() - width, P[:, 1].max() + width
        sel = (x >= x0 - 3) & (x <= x1 + 3) & (n >= n0 - 3) & (n <= n1 + 3)
        if not sel.any():
            continue
        d, j = _nearest_polyline(x[sel], n[sel], P)
        sh = 3.0 if kind == "trail" else 2.5
        w = 1 - smooth(width / 2, width / 2 + sh, d)
        h[sel] = h[sel] * (1 - w) + zs[j] * w
    lip = 0.6 * (1 - smooth(1.2, 5.0, edge_distance(MAIN, x, n)))
    bed = 0.35 * (1 - smooth(0.4, 1.5, stream_distance(x, n)))                       # the stream runs in a shallow bed
    return h + lip * (edge_distance(MAIN, x, n) >= 0) - bed                            # rock lip all round the rim


def stack_top(x, n):
    d = edge_distance(STACK, x, n)
    notch = 0.95 * (1 - smooth(1.5, 4.5, np.hypot(x - 101.4, n - 45.55)))                     # the bridge lands in a shallow hollow on the stack
    return STACK["top"] + 0.35 * field_noise(x, n, 311) + 0.5 * (1 - smooth(1.0, 3.5, d)) - notch


# optional exploration bridge: deck from the lowest bench (x 93) to the hollow on the stack (x 101.4); deck end height derived from the stack surface
BRIDGE = ("Tea Stack bridge", 2.4, (93.0, 46.0), (101.4, 45.55), -8.40, round(float(stack_top(np.array(101.4), np.array(45.55))) + 0.03, 3))


# ---------------------------------------------------------------------------------------------------- the runtime grids
CELL = 0.5


def bridge_height(x, n):
    """Deck height of the optional bridge (NaN outside the 2 m strip)."""
    name, w, a, b, za, zb = BRIDGE
    a = np.array(a); b = np.array(b); ab = b - a; L2 = float(ab @ ab)
    t = ((x - a[0]) * ab[0] + (n - a[1]) * ab[1]) / L2
    dist = np.abs((x - a[0]) * ab[1] - (n - a[1]) * ab[0]) / math.sqrt(L2)
    ok = (t >= 0) & (t <= 1 + 1.6 / math.sqrt(L2)) & (dist <= w / 2)                 # the walkable strip runs 1.6 m past the deck end onto the stack (inside its 1.2 m rim margin)
    return np.where(ok, za + (zb - za) * np.clip(t, 0, 1), np.nan)


def extents():
    """Authoritative bounds from ALL geometry: both rims, the bridge. Returns dict in plan metres."""
    out = {}
    for c in (MAIN, STACK):
        p, _, L = rim_points(c, 0.5); out[c["key"]] = dict(x=[float(p[:, 0].min()), float(p[:, 0].max())], n=[float(p[:, 1].min()), float(p[:, 1].max())], rim_m=float(L))
    xs = [v for k in out.values() for v in k["x"]]; ns = [v for k in out.values() for v in k["n"]]
    out["all"] = dict(x=[min(xs), max(xs)], n=[min(ns), max(ns)])
    return out


def grid_spec(margin=8.0):
    e = extents()["all"]
    x0 = math.floor((e["x"][0] - margin) / CELL) * CELL; x1 = math.ceil((e["x"][1] + margin) / CELL) * CELL
    n0 = math.floor((e["n"][0] - margin) / CELL) * CELL; n1 = math.ceil((e["n"][1] + margin) / CELL) * CELL
    return dict(x0=x0, n0=n0, cell=CELL, nx=int(round((x1 - x0) / CELL)) + 1, nn=int(round((n1 - n0) / CELL)) + 1)


def sample_grid(spec=None):
    """Heights (m, float) at the nodes of the runtime grid; NaN where there is no support. Plus the walkable/safe masks."""
    s = spec or grid_spec(); xs = s["x0"] + CELL * np.arange(s["nx"]); ns = s["n0"] + CELL * np.arange(s["nn"])
    X, N = np.meshgrid(xs, ns)
    h = np.full(X.shape, np.nan)
    inm = edge_distance(MAIN, X, N) >= 0
    h = np.where(inm, terrain(X, N), h)
    ins = edge_distance(STACK, X, N) >= 0
    h = np.where(ins & ~inm, stack_top(X, N), h)
    br = bridge_height(X, N); h = np.where(~np.isnan(br), np.where(np.isnan(h), br, np.maximum(h, br)), h)
    return X, N, h


def masks(h, edge_main, edge_stack, br):
    """walkable (bit0): supported, >= RIM_MARGIN from the rim, slope <= MAX_SLOPE.  comfortable (bit1): slope <= COMFORT_SLOPE and >= 2.5 m from the rim."""
    hh = np.where(np.isnan(h), NOSUP, h)
    gy, gx = np.gradient(hh, CELL); slope = np.hypot(gx, gy)
    sup = ~np.isnan(h)
    # a cell next to the void has a huge numerical slope: judge slope only against supported neighbours
    nb = np.where(sup, hh, np.nan)
    sx = np.nanmax(np.abs(np.stack([np.roll(nb, 1, 1) - nb, np.roll(nb, -1, 1) - nb])), axis=0) / CELL
    sy = np.nanmax(np.abs(np.stack([np.roll(nb, 1, 0) - nb, np.roll(nb, -1, 0) - nb])), axis=0) / CELL
    slope = np.nan_to_num(np.hypot(sx, sy) * 0.8, nan=9.0)
    rim_ok = np.where(~np.isnan(br), True, (np.maximum(edge_main, edge_stack) >= RIM_MARGIN))
    walk = sup & rim_ok & (slope <= MAX_SLOPE)
    deck_slope = abs(BRIDGE[5] - BRIDGE[4]) / math.hypot(BRIDGE[3][0] - BRIDGE[2][0], BRIDGE[3][1] - BRIDGE[2][1])
    walk = np.where(~np.isnan(br), sup & (deck_slope <= MAX_SLOPE), walk)             # a bridge deck is judged by its own slope, not by the void beside it
    comf = walk & (slope <= COMFORT_SLOPE) & (np.where(~np.isnan(br), True, np.maximum(edge_main, edge_stack) >= 2.5))
    return walk, comf, slope


# ---------------------------------------------------------------------------------------------------- surface classes (vertex colour logic and vegetation rules)
def stream_distance(x, n):
    P, _ = _dense([(a, b) for a, b in WATER], 0.5); d, _j = _nearest_polyline(np.asarray(x, float), np.asarray(n, float), P); return d


def path_distance(x, n):
    best = np.full(np.shape(x), 1e9); x = np.asarray(x, float); n = np.asarray(n, float)
    for i, (_nm, kind, width, pts) in enumerate(PATHS):
        P, _ = _dense(pts, 0.5); d, _j = _nearest_polyline(x, n, P); best = np.minimum(best, d - width / 2)
    return best                                                         # < 0 inside a path


def clearing_distance(x, n):
    best = np.full(np.shape(x), 1e9)
    for _nm, cx, cn, r, _z in CLEARINGS:
        best = np.minimum(best, np.hypot(x - cx, n - cn) - r)
    return best


# ---------------------------------------------------------------------------------------------------- vegetation (deterministic)
def load_solids(scene_json):
    """Footprints of the built town (solid, non-camera proxies) as (x0, x1, n0, n1)."""
    import json
    d = json.load(open(scene_json)); out = []
    for o in d["collision"]:
        if o.get("cameraOnly"):
            continue
        out.append((o["x"] - o["w"] / 2, o["x"] + o["w"] / 2, -o["z"] - o["d"] / 2, -o["z"] + o["d"] / 2))
    return np.array(out)


WOODS = [(34, 112, 28, 12), (-50, 100, 10, 8), (-18, 116, 10, 6), (-70, 62, 9, 16), (-52, -14, 12, 7), (52, -8, 10, 8), (68, 96, 10, 8), (-36, 60, 7, 12), (14, 122, 14, 5), (-64, 20, 6, 22), (-42, 44, 6, 12)]


def plant(solids, seed=2026):
    """Returns dict of lists of (x, n, z, yaw, scale). Rules: not on the town pad (+3 m), not near solids (4 m), paths (2.5 m), clearings (3 m), stream (2.2 m), steep ground, the rim (2.5 m);
    no tall trees in the lookout view wedge east of the town (tea rows instead)."""
    rng = np.random.default_rng(seed); out = {"tree_round": [], "tree_tall": [], "palm": [], "shrub": [], "rock": [], "tea": []}

    def ok(x, n, margin_pad=3.0, solid=4.0):
        if rect_dist(x, n, PAD) < margin_pad and not (n > PAD[3]):      # the pad is bare ground between buildings
            return False
        if n > PAD[3] and abs(x) < 16.5 and n < 98:                      # hall, tower, shelf front
            return False
        if edge_distance(MAIN, x, n) < 2.5 or edge_distance(MAIN, x, n) < 0:
            return False
        if path_distance(np.array(x), np.array(n)) < 2.5 or clearing_distance(np.array(x), np.array(n)) < 3.0 or stream_distance(np.array(x), np.array(n)) < 2.2:
            return False
        if len(solids) and np.any((x > solids[:, 0] - solid) & (x < solids[:, 1] + solid) & (n > solids[:, 2] - solid) & (n < solids[:, 3] + solid)):
            return False
        return True

    for (cx, cn, rx, rn) in WOODS:
        area = math.pi * rx * rn; count = int(area / 14.0)
        tries = 0
        while count > 0 and tries < 4000:
            tries += 1
            a = rng.uniform(0, TAU); r = math.sqrt(rng.uniform()); x = cx + rx * r * math.cos(a); n = cn + rn * r * math.sin(a)
            if not ok(x, n):
                continue
            hh = float(terrain(np.array(x), np.array(n)))
            gx = (terrain(np.array(x + 0.5), np.array(n)) - terrain(np.array(x - 0.5), np.array(n))); gy = (terrain(np.array(x), np.array(n + 0.5)) - terrain(np.array(x), np.array(n - 0.5)))
            if math.hypot(float(gx), float(gy)) > 0.55:
                continue
            if x > 46 and n < 90 and abs(n - LOOKOUT[1]) < 40 and hh < 1.0:                    # lookout wedge: low planting only
                continue
            kind = rng.choice(["tree_round", "tree_tall", "palm"], p=[0.45, 0.2, 0.35])
            if any(math.hypot(x - p[0], n - p[1]) < 3.0 for p in sum(out.values(), [])):
                continue
            out[kind].append((float(x), float(n), hh, float(rng.uniform(0, TAU)), float(rng.uniform(0.85, 1.35)))); count -= 1
    # shrubs: under the trees and along path edges
    pts = out["tree_round"] + out["tree_tall"] + out["palm"]
    for (x, n, *_r) in pts:
        for _ in range(1):
            a = rng.uniform(0, TAU); q = rng.uniform(1.6, 3.2); xx, nn = x + q * math.cos(a), n + q * math.sin(a)
            if ok(xx, nn, 2.0, 2.5):
                out["shrub"].append((float(xx), float(nn), float(terrain(np.array(xx), np.array(nn))), float(rng.uniform(0, TAU)), float(rng.uniform(0.7, 1.3))))
    # rocks: scattered on the meadows and at the foot of the crag
    for _ in range(140):
        x = rng.uniform(-72, 90); n = rng.uniform(-60, 128)
        if inside(x, n, 4.0) and ok(x, n, 1.5, 2.0):
            out["rock"].append((float(x), float(n), float(terrain(np.array(x), np.array(n))), float(rng.uniform(0, TAU)), float(rng.uniform(0.6, 1.8))))
    # tea rows: contour-following hedge segments on the benches
    L = np.array(LOOKOUT)
    for k in range(6):
        for f in (0.22, 0.55):
            target = TEA_D0 + TEA_W * (k + f)
            for th in np.arange(math.radians(-62), math.radians(52), 1.5 / max(target, 8)):
                r = target
                for _ in range(4):
                    p = L + r * np.array([math.cos(th), math.sin(th)]); wob = 2.4 * field_noise(p[0], p[1], 91, (38, 21, 12), (1, 0.6, 0.35)); r = target - float(wob)
                p = L + r * np.array([math.cos(th), math.sin(th)])
                if p[0] < 49 or not inside(p[0], p[1], 3.0) or p[1] > 88 or p[1] < 6:
                    continue
                if path_distance(np.array(p[0]), np.array(p[1])) < 1.4 or clearing_distance(np.array(p[0]), np.array(p[1])) < 1.0 or stream_distance(np.array(p[0]), np.array(p[1])) < 1.6:
                    continue
                g = np.array([float(terrain(np.array(p[0] + 0.6), np.array(p[1])) - terrain(np.array(p[0] - 0.6), np.array(p[1]))), float(terrain(np.array(p[0]), np.array(p[1] + 0.6)) - terrain(np.array(p[0]), np.array(p[1] - 0.6)))]) / 1.2
                if np.hypot(*g) > 0.22:
                    continue
                tang = math.atan2(math.cos(th), -math.sin(th))
                out["tea"].append((float(p[0]), float(p[1]), float(terrain(np.array(p[0]), np.array(p[1]))), float(tang), 1.0))
    return out
