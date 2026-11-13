"""Merchant Citadel P3-B batch 1: custom low-poly vegetation, rocks and quay props (numpy primitives, vertex colours, z up, origin at the base).
All custom geometry authored for this project (no third-party licence). Each builder returns (V (n,3), F (m,3), C (n,3))."""
import math
import numpy as np

TAU = 2 * math.pi


def _join(parts):
    V, F, C = [], [], []; o = 0
    for v, f, c in parts:
        V.append(v); F.append(np.asarray(f) + o); C.append(c); o += len(v)
    return np.concatenate(V), np.concatenate(F), np.concatenate(C)


def _col(n, rgb):
    return np.tile(np.asarray(rgb, float), (n, 1))


def box(c, s, rgb, jitter=0.0, seed=0):
    x, y, z = c; sx, sy, sz = s[0] / 2, s[1] / 2, s[2] / 2
    V = np.array([(x + dx * sx, y + dy * sy, z + dz * sz) for dz in (-1, 1) for dy in (-1, 1) for dx in (-1, 1)], float)
    F = np.array([(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4), (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)])
    if jitter:
        V = V + np.random.default_rng(seed).uniform(-jitter, jitter, V.shape)
    return V, F, _col(8, rgb)


def cyl(c, r0, r1, h, n, rgb, cap_top=True, cap_bottom=True, rgb_top=None, wobble=0.0, seed=0):
    x, y, z = c; rng = np.random.default_rng(seed); V = []; F = []
    for k, (r, zz) in enumerate(((r0, z), (r1, z + h))):
        for i in range(n):
            a = TAU * i / n; rr = r * (1 + wobble * rng.uniform(-1, 1)); V.append((x + rr * math.cos(a), y + rr * math.sin(a), zz))
    for i in range(n):
        j = (i + 1) % n; F += [(i, j, n + i), (j, n + j, n + i)]
    V = np.array(V, float); C = np.vstack([_col(n, rgb), _col(n, rgb_top or rgb)])
    if cap_top and r1 > 0:
        V = np.vstack([V, [(x, y, z + h)]]); ci = len(V) - 1; C = np.vstack([C, [rgb_top or rgb]]); F += [(n + (i + 1) % n, n + i, ci) for i in range(n)]
    if cap_bottom and r0 > 0:
        V = np.vstack([V, [(x, y, z)]]); ci = len(V) - 1; C = np.vstack([C, [rgb]]); F += [(i, (i + 1) % n, ci) for i in range(n)]
    return V, np.array(F), C


def ico(c, r, sub=1, scale=(1, 1, 1), noise=0.0, seed=0, rgb_fn=None):
    t = (1 + math.sqrt(5)) / 2
    V = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    V = [tuple(np.array(v, float) / np.linalg.norm(v)) for v in V]
    for _ in range(sub):
        cache = {}; nf = []
        def mid(a, b):
            k = (min(a, b), max(a, b))
            if k not in cache:
                m = (np.array(V[a]) + np.array(V[b])) / 2; V.append(tuple(m / np.linalg.norm(m))); cache[k] = len(V) - 1
            return cache[k]
        for a, b, cc in F:
            ab, bc, ca = mid(a, b), mid(b, cc), mid(cc, a); nf += [(a, ab, ca), (b, bc, ab), (cc, ca, bc), (ab, bc, ca)]
        F = nf
    V = np.array(V, float); rng = np.random.default_rng(seed)
    d = rng.normal(size=(3, 3)); amp = np.zeros(len(V))
    for k in range(3):
        amp += np.sin(V @ (d[k] * 2.3) + k)
    V = V * (1 + noise * amp / 3)[:, None] * np.array(scale) * r + np.array(c)
    C = rgb_fn(V) if rgb_fn else _col(len(V), (0.5, 0.5, 0.5))
    return V, np.array(F), C


def shade_green(base, v0, v1, dark=0.55):
    base = np.asarray(base, float)
    def f(V):
        t = np.clip((V[:, 2] - v0) / max(v1 - v0, 1e-6), 0, 1); return base * (dark + (1 - dark) * t)[:, None]
    return f


# ---------------------------------------------------------------------------------------------------- vegetation
def tree_round(seed=1):
    g = (0.23, 0.42, 0.15); parts = [cyl((0, 0, 0), 0.30, 0.17, 3.4, 6, (0.36, 0.25, 0.15), cap_bottom=False, wobble=0.05, seed=seed)]
    parts.append(ico((0, 0, 4.3), 2.1, 1, (1.0, 1.0, 0.82), 0.16, seed, shade_green(g, 2.2, 6.2, 0.55)))
    parts.append(ico((0.9, 0.4, 5.3), 1.55, 1, (1.0, 1.0, 0.85), 0.18, seed + 1, shade_green((0.27, 0.47, 0.17), 3.5, 7.0, 0.6)))
    parts.append(ico((-0.8, -0.5, 4.9), 1.35, 1, (1.0, 1.0, 0.85), 0.18, seed + 2, shade_green((0.20, 0.38, 0.14), 3.3, 6.6, 0.6)))
    return _join(parts)


def tree_tall(seed=2):
    parts = [cyl((0, 0, 0), 0.28, 0.14, 5.2, 6, (0.34, 0.24, 0.15), cap_bottom=False, seed=seed)]
    for k, (r, z, h) in enumerate(((1.9, 2.0, 2.6), (1.6, 3.6, 2.5), (1.2, 5.1, 2.3), (0.75, 6.5, 2.0))):
        parts.append(cyl((0, 0, z), r, 0.05, h, 8, (0.13 + 0.02 * k, 0.30 + 0.03 * k, 0.18), cap_bottom=True, wobble=0.12, seed=seed + k))
    return _join(parts)


def palm(seed=3):
    rng = np.random.default_rng(seed); parts = []; z = 0.0; x = 0.0; r = 0.26
    for k in range(7):
        parts.append(cyl((x, 0, z), r, r * 0.9, 1.0, 6, (0.50, 0.42, 0.30), cap_bottom=False, cap_top=False, seed=seed + k)); z += 1.0; x += 0.10 * k * 0.5; r *= 0.93
    top = (x, 0, z)
    for i in range(9):
        a = TAU * i / 9 + rng.uniform(-0.2, 0.2); L = rng.uniform(2.3, 3.0); droop = rng.uniform(0.9, 1.5)
        pts = [(top[0] + math.cos(a) * L * s, math.sin(a) * L * s, top[2] + 0.5 * math.sin(s * 3.0) - droop * s * s) for s in (0.0, 0.35, 0.7, 1.0)]
        V = []; F = []
        for k, p in enumerate(pts):
            w = 0.55 * math.sin(math.pi * min(0.15 + k / 3.0 * 0.85, 1.0)) + 0.04; nx, ny = -math.sin(a), math.cos(a)
            V += [(p[0] + nx * w, p[1] + ny * w, p[2]), (p[0] - nx * w, p[1] - ny * w, p[2])]
        for k in range(3):
            q = 2 * k; F += [(q, q + 1, q + 2), (q + 1, q + 3, q + 2), (q, q + 2, q + 1), (q + 1, q + 2, q + 3)]
        parts.append((np.array(V, float), np.array(F), _col(8, (0.24 + 0.08 * rng.random(), 0.45, 0.16))))
    return _join(parts)


def shrub(seed=4):
    return ico((0, 0, 0.45), 0.9, 1, (1.0, 1.0, 0.65), 0.2, seed, shade_green((0.25, 0.42, 0.16), 0.0, 1.0, 0.6))


def tea_hedge(seed=5):
    return ico((0, 0, 0.32), 0.8, 1, (1.9, 0.75, 0.55), 0.10, seed, shade_green((0.18, 0.40, 0.13), 0.0, 0.8, 0.62))


def rock(seed=6, rgb=(0.58, 0.54, 0.47)):
    return ico((0, 0, 0.0), 1.0, 1, (1.0, 0.85, 0.65), 0.30, seed, lambda V: np.tile(rgb, (len(V), 1)) * (0.8 + 0.3 * np.clip((V[:, 2] + 0.6) / 1.2, 0, 1))[:, None])


# ---------------------------------------------------------------------------------------------------- quay props
WOOD = (0.47, 0.33, 0.19); WOOD_D = (0.33, 0.22, 0.12); IRON = (0.17, 0.16, 0.16); STONE = (0.55, 0.51, 0.45); ROPE = (0.72, 0.62, 0.42); CLOTH = (0.72, 0.30, 0.20)


def crate(seed=7):
    parts = [box((0, 0, 0.4), (0.9, 0.8, 0.8), WOOD, 0.01, seed)]
    for dz in (0.08, 0.72):
        parts.append(box((0, 0, dz), (0.94, 0.84, 0.10), WOOD_D))
    for dx in (-0.4, 0.4):
        parts.append(box((dx, 0, 0.4), (0.10, 0.84, 0.84), WOOD_D))
    return _join(parts)


def barrel(seed=8):
    parts = [cyl((0, 0, 0), 0.34, 0.38, 0.55, 8, WOOD, cap_top=False, cap_bottom=False), cyl((0, 0, 0.55), 0.38, 0.33, 0.55, 8, WOOD, cap_top=True, cap_bottom=False, rgb_top=WOOD_D)]
    for z in (0.12, 0.55, 0.98):
        parts.append(cyl((0, 0, z - 0.03), 0.40, 0.40, 0.06, 8, IRON, cap_top=False, cap_bottom=False))
    return _join(parts)


def sack(seed=9):
    return ico((0, 0, 0.3), 0.42, 1, (1.0, 0.75, 0.75), 0.20, seed, lambda V: np.tile((0.70, 0.62, 0.46), (len(V), 1)) * (0.85 + 0.2 * np.clip(V[:, 2] / 0.6, 0, 1))[:, None])


def bollard(seed=10):
    return _join([cyl((0, 0, 0), 0.30, 0.24, 0.72, 8, STONE, cap_bottom=False, wobble=0.04, seed=seed), cyl((0, 0, 0.70), 0.34, 0.34, 0.12, 8, IRON), cyl((0, 0, 0.32), 0.27, 0.27, 0.07, 8, ROPE, cap_top=False, cap_bottom=False)])


def lamp(seed=11):
    return _join([cyl((0, 0, 0), 0.10, 0.07, 3.4, 6, WOOD_D, cap_bottom=False), box((0, 0, 3.55), (0.42, 0.42, 0.55), (0.95, 0.78, 0.38)), box((0, 0, 3.9), (0.55, 0.55, 0.10), IRON), box((0, 0, 3.0), (0.42, 0.10, 0.10), WOOD_D)])


def crate_stack(seed=12):
    parts = []; rng = np.random.default_rng(seed)
    for (x, y, z, ry) in ((0, 0, 0, 0), (1.0, 0.1, 0, 0.1), (0.5, 0.05, 0.8, -0.05), (-0.95, 0.0, 0, 0.0), (0.05, 0.95, 0, 0.2)):
        V, F, C = crate(int(rng.integers(100))); c, s = math.cos(ry), math.sin(ry)
        V = np.column_stack([V[:, 0] * c - V[:, 1] * s + x, V[:, 0] * s + V[:, 1] * c + y, V[:, 2] + z]); parts.append((V, F, C))
    parts += [(lambda v, f, c: (v + [1.5, -0.8, 0], f, c))(*sack(1)), (lambda v, f, c: (v + [1.9, -0.5, 0], f, c))(*sack(2)), (lambda v, f, c: (v + [1.7, -0.9, 0.5], f, c))(*sack(3))]
    return _join(parts)


def crane(seed=13):
    """Timber quay crane: two posts, A-brace, 7 m jib that projects toward +x, rope, hook and a hanging crate. Footprint about 2.4 x 1.4 m."""
    parts = [box((0, -0.55, 2.8), (0.42, 0.42, 5.6), WOOD_D), box((0, 0.55, 2.8), (0.42, 0.42, 5.6), WOOD_D), box((0, 0, 0.15), (1.6, 1.8, 0.30), STONE), box((0, 0, 5.4), (0.5, 1.5, 0.35), WOOD)]
    parts.append(box((3.0, 0, 5.2), (7.2, 0.30, 0.38), WOOD)); parts.append(box((1.7, 0, 4.1), (3.4, 0.22, 0.22), WOOD_D))
    V, F, C = box((1.7, 0, 4.1), (3.6, 0.22, 0.22), WOOD_D); a = -0.62; c, s = math.cos(a), math.sin(a)
    parts[-1] = (np.column_stack([(V[:, 0] - 1.7) * c - (V[:, 2] - 4.1) * s + 1.7, V[:, 1], (V[:, 0] - 1.7) * s + (V[:, 2] - 4.1) * c + 4.1]), F, C)
    parts.append(cyl((6.4, 0, 2.6), 0.03, 0.03, 2.6, 4, ROPE, cap_bottom=False)); parts.append(box((6.4, 0, 2.5), (0.25, 0.25, 0.22), IRON)); V, F, C = crate(); parts.append((V + [6.4, 0, 1.6], F, C))
    return _join(parts)


def beacon(seed=14):
    """Sky Quay beacon: stone tower with a lantern room and a pennant mast. 9 m tall, about 3.4 m across."""
    parts = [cyl((0, 0, 0), 1.7, 1.25, 4.0, 8, (0.80, 0.74, 0.60), cap_bottom=False, wobble=0.015), cyl((0, 0, 4.0), 1.45, 1.45, 0.25, 8, (0.62, 0.36, 0.24)), cyl((0, 0, 4.25), 1.0, 0.9, 2.2, 8, (0.84, 0.78, 0.64), cap_top=False)]
    parts.append(cyl((0, 0, 6.45), 1.3, 1.3, 0.22, 8, (0.62, 0.36, 0.24))); parts.append(cyl((0, 0, 6.67), 0.75, 0.75, 1.1, 8, (1.0, 0.85, 0.45), cap_top=False, cap_bottom=False))
    parts.append(cyl((0, 0, 7.77), 1.15, 0.05, 1.5, 8, (0.60, 0.33, 0.22)))
    parts.append(cyl((0, 0, 9.2), 0.05, 0.03, 2.6, 4, WOOD_D)); parts.append(box((0.55, 0, 10.9), (1.1, 0.03, 0.6), CLOTH))
    for k in range(4):
        parts.append(box((0, 0, 1.0 + k * 0.9), (0.45, 0.5, 0.06), (0.30, 0.26, 0.22)))
    return _join(parts)



TERRA = (0.58, 0.30, 0.20); CANVAS = (0.82, 0.74, 0.56)


def pavilion(seed=16):
    """Open timber pavilion for the Tea Stack: stone plinth, four posts, terracotta pyramid roof, lantern. About 5 x 5 m, 4.8 m tall."""
    parts = [box((0, 0, 0.2), (5.2, 5.2, 0.4), STONE)]
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        parts.append(box((sx * 2.0, sy * 2.0, 1.65), (0.28, 0.28, 2.5), WOOD_D))
    parts.append(box((0, 0, 2.95), (4.6, 4.6, 0.2), WOOD))
    parts.append(cyl((0, 0, 3.05), 3.7, 0.12, 1.7, 4, TERRA, cap_bottom=True, wobble=0.0))
    parts.append(cyl((0, 0, 4.7), 0.12, 0.08, 0.5, 6, IRON)); parts.append(box((0, 0, 1.0), (1.2, 1.2, 0.5), WOOD))
    V, F, C = _join(parts); V = V.copy(); V[:, :2] = np.column_stack([V[:, 0], V[:, 1]]); return V, F, C


def counting_stone(seed=17):
    parts = [box((0, 0, 0.3), (2.2, 2.2, 0.6), STONE), box((0, 0, 1.6), (1.5, 1.5, 2.0), (0.62, 0.58, 0.50), 0.03, seed), box((0, 0, 2.85), (1.15, 1.15, 0.5), (0.58, 0.54, 0.46), 0.02, seed + 1)]
    for z in (1.0, 1.7, 2.4):
        parts.append(box((0, 0, z), (1.58, 1.58, 0.07), TERRA))
    return _join(parts)


def wagon(seed=18):
    """Merchant caravan wagon: bed, canvas hood, two big wheels, shafts. 3.4 x 1.7 m, 2.3 m tall."""
    parts = [box((0, 0, 0.95), (3.0, 1.5, 0.22), WOOD), box((0, -0.75, 1.3), (3.0, 0.1, 0.55), WOOD_D), box((0, 0.75, 1.3), (3.0, 0.1, 0.55), WOOD_D)]
    hood = cyl((0, 0, 0), 0.8, 0.8, 2.8, 8, CANVAS, cap_top=True, cap_bottom=True)
    V = hood[0].copy(); Vr = np.column_stack([V[:, 2] - 1.4, V[:, 1], V[:, 0] * 0.0 + V[:, 0]])      # lay the cylinder along x
    Vr = np.column_stack([V[:, 2] - 1.4, V[:, 0], V[:, 1] * 0.8 + 1.55]); parts.append((Vr, hood[1], hood[2]))
    for dx in (-1.0, 1.0):
        for dy in (-0.9, 0.9):
            w = cyl((0, 0, 0), 0.62, 0.62, 0.12, 10, WOOD_D, cap_top=True, cap_bottom=True); Vw = w[0]; parts.append((np.column_stack([Vw[:, 0] + dx, Vw[:, 2] + dy - 0.06, Vw[:, 1] + 0.62]), w[1], w[2]))
    parts.append(box((2.4, 0, 0.9), (1.8, 0.12, 0.12), WOOD_D)); parts.append(box((2.4, 0.5, 0.9), (1.8, 0.1, 0.1), WOOD_D))
    return _join(parts)


def campfire(seed=19):
    parts = []
    for k in range(9):
        a = TAU * k / 9; parts.append(box((0.8 * math.cos(a), 0.8 * math.sin(a), 0.12), (0.34, 0.26, 0.24), (0.50, 0.47, 0.42), 0.03, seed + k))
    for a in (0.0, 1.1, 2.2):
        V, F, C = box((0, 0, 0.2), (1.1, 0.16, 0.16), WOOD_D); c, s = math.cos(a), math.sin(a); parts.append((np.column_stack([V[:, 0] * c - V[:, 1] * s, V[:, 0] * s + V[:, 1] * c, V[:, 2]]), F, C))
    parts.append(ico((0, 0, 0.45), 0.28, 0, (1, 1, 1.4), 0.1, seed, lambda V: np.tile((1.0, 0.62, 0.18), (len(V), 1))))
    return _join(parts)


def cloud(seed=15):
    return ico((0, 0, 0), 10.0, 1, (1.6, 1.0, 0.5), 0.2, seed, lambda V: np.ones((len(V), 3)))


PROTOS = {"pavilion": pavilion, "counting_stone": counting_stone, "wagon": wagon, "campfire": campfire, "cloud": cloud, "tree_round": tree_round, "tree_tall": tree_tall, "palm": palm, "shrub": shrub, "tea": tea_hedge, "rock_a": lambda: rock(6), "rock_b": lambda: rock(16, (0.62, 0.50, 0.38)), "rock_c": lambda: rock(26, (0.52, 0.52, 0.48)),
          "crate": crate, "barrel": barrel, "sack": sack, "bollard": bollard, "lamp": lamp, "crate_stack": crate_stack, "crane": crane, "beacon": beacon}
