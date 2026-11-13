"""Merchant Citadel P3-B batch 1: geometry generators (numpy only; return vertex/face/colour arrays). Used inside Blender by p3b_blender_build.py.

Everything samples p3b_model, the single spatial definition. Colour logic is geological: rock layers are horizontal in ABSOLUTE elevation (warped by noise),
so the cream / ochre / terracotta / grey sequence continues from one cliff section to the next and from the cliff into the underside.
"""
import math
import numpy as np
import p3b_model as M

TAU = M.TAU
STRATA_PALETTE = np.array([(0.70, 0.60, 0.44), (0.62, 0.45, 0.26), (0.54, 0.30, 0.19), (0.49, 0.46, 0.41), (0.72, 0.64, 0.49), (0.58, 0.40, 0.25)])
BASALT = np.array([0.30, 0.27, 0.25])


def noise3(x, y, z, seed, waves=((23, 1.0), (11, 0.55), (5.5, 0.3))):
    rng = np.random.default_rng(seed); out = np.zeros_like(np.asarray(x, float)); tot = 0.0
    for w, a in waves:
        for _ in range(3):
            d = rng.normal(size=3); d /= np.linalg.norm(d); out = out + a * np.sin((d[0] * x + d[1] * y + d[2] * z) * TAU / w + rng.uniform(0, TAU)); tot += a
    return out / tot * 1.6


def layer_colour(z, x, y):
    """Rock layers horizontal in absolute elevation: thickness varies (1.2-5 m), warped by noise. Returns (n,3)."""
    zz = np.asarray(z, float) + 2.2 * noise3(x * 0.6, y * 0.6, z * 0.2, 5, ((40, 1.0), (17, 0.5)))
    # non-uniform thickness: integrate a varying rate so layers are unequal but continuous
    u = zz * (0.26 + 0.09 * np.sin(zz * 0.13 + 1.0))
    k = np.floor(u).astype(int); f = u - np.floor(u)
    a = STRATA_PALETTE[np.mod(k, len(STRATA_PALETTE))]; b = STRATA_PALETTE[np.mod(k + 1, len(STRATA_PALETTE))]
    w = M.smooth(0.82, 1.0, f)[..., None]                                   # crisp bedding planes, soft shift inside
    fine = (1 + 0.07 * noise3(x * 2.2, y * 2.2, z * 1.6, 9, ((6, 1.0), (2.6, 0.6))))[..., None]
    return (a * (1 - w) + b * w) * fine


def vertex_normals(V, F):
    n = np.zeros_like(V); a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]; fn = np.cross(b - a, c - a)
    for k in range(3):
        np.add.at(n, F[:, k], fn)
    l = np.linalg.norm(n, axis=1, keepdims=True); return n / np.maximum(l, 1e-9)


# ---------------------------------------------------------------------------------------------------- top surface
def top_vertices(c, terrain_fn, coarse=2.0):
    """Plan points of the top mesh: the rim polyline (constrained boundary) + an adaptive lattice inside: 2 m where the ground is flat, 1 m where it varies (> 0.10 m
    across the cell), 0.5 m where it is steep (> 0.40 m), plus a 1 m band along the rim. The constrained Delaunay triangulation handles the mixed resolution."""
    rim, th, L = M.rim_points(c, 1.0)
    x0, x1 = rim[:, 0].min() - 1, rim[:, 0].max() + 1; n0, n1 = rim[:, 1].min() - 1, rim[:, 1].max() + 1
    f = 0.5; X0 = math.floor(x0 / coarse) * coarse; N0 = math.floor(n0 / coarse) * coarse
    nx = int(math.ceil((x1 - X0) / f)) + 1; ny = int(math.ceil((n1 - N0) / f)) + 1
    LX, LY = np.meshgrid(X0 + f * np.arange(nx), N0 + f * np.arange(ny)); H = terrain_fn(LX, LY)
    ed = M.edge_distance(c, LX, LY)
    k = int(round(coarse / f)); pts = set()
    for j in range(0, ny - k, k):
        for i in range(0, nx - k, k):
            blk = H[j:j + k + 1, i:i + k + 1]
            u_ = np.linspace(0, 1, k + 1)[None, :]; v_ = np.linspace(0, 1, k + 1)[:, None]      # deviation of the ground from the bilinear surface through the cell's four corners
            bil = blk[0, 0] * (1 - u_) * (1 - v_) + blk[0, -1] * u_ * (1 - v_) + blk[-1, 0] * (1 - u_) * v_ + blk[-1, -1] * u_ * v_
            rg = float(np.abs(blk - bil).max())
            step = 1 if rg > 0.16 else (2 if rg > 0.035 else k)
            for jj in range(j, j + k + 1, step):
                for ii in range(i, i + k + 1, step):
                    if ed[jj, ii] >= 0.8: pts.add((ii, jj))
    band = (ed >= 0.8) & (ed < 3.0)
    for jj, ii in zip(*np.nonzero(band)):
        if (ii % 2 == 0 and jj % 2 == 0): pts.add((int(ii), int(jj)))
    P = np.array(sorted(pts)); return rim, np.column_stack([X0 + f * P[:, 0], N0 + f * P[:, 1]])


# ---------------------------------------------------------------------------------------------------- cliff and underside shell
def _bump(dth, w, p=1.6):
    return np.clip(1 - np.abs(dth) / w, 0, 1) ** p


def _dth(th, deg):
    a = math.radians(deg); return np.arctan2(np.sin(th - a), np.cos(th - a))


SHELLS = {
    "main": dict(seed=303, S=4, J=14, keel=[(6.0, -13.0), (6.0, 33.0)], p=1.18),
    "stack": dict(seed=311, S=3, J=10, keel=[(111.0, 44.0), (112.0, 46.0)], p=1.05),
}


def shell_params(c, th):
    """Cliff height Dc(theta) and total depth D(theta) below the rim."""
    if c["key"] == "main":
        Dc = 22.0 + 5.0 * _bump(_dth(th, 68), 0.75, 1.2) - 2.5 * _bump(_dth(th, 12), 0.3) + 2.0 * np.sin(th * 3 + 1)
        D = 48.0 + 46.0 * (0.5 + 0.5 * np.cos(th - math.radians(72))) + 6.0 * M.ring_noise(th, 8, (4, 7, 11), (1, .6, .3))
    else:
        Dc = 17.0 + 3.0 * np.sin(th * 2 + 0.4); D = 58.0 + 7.0 * np.sin(th * 3)
    return Dc, D


def build_shell(c, spacing=1.0):
    """Returns V (n,3 plan x, plan n, z), F (m,3), ring_index list, extras. Ring 0 is the rim (same points as the top mesh boundary)."""
    sp = SHELLS[c["key"]]; seed = sp["seed"]; S = sp["S"]; J = sp["J"]
    pts, th, L = M.rim_points(c, spacing); N = len(pts); cx, cy = c["centre"]
    r = np.hypot(pts[:, 0] - cx, pts[:, 1] - cy); u = (pts - np.array([cx, cy])) / r[:, None]
    s_arc = np.arange(N) * (L / N)
    zr = (M.terrain(pts[:, 0], pts[:, 1]) if c["key"] == "main" else M.stack_top(pts[:, 0], pts[:, 1]))
    Dc, D = shell_params(c, th)
    # strata thickness fractions vary along the rim
    fr = np.stack([1.0 + 0.45 * M.ring_noise(th * (2 + s) + s * 1.7, seed + 20 + s, (3, 5, 9), (1, .6, .3)) for s in range(S)], 1); fr = np.maximum(fr, 0.35); cum = np.cumsum(fr, 1) / fr.sum(1, keepdims=True)
    depths = [np.zeros(N)]; insets = [np.zeros(N)]
    # fractures (recesses) and fluted crag face
    frac = np.zeros(N)
    for deg, w, dep in ((12, 0.16, 6.0), (154, 0.14, 4.5), (238, 0.12, 4.0), (45, 0.07, 3.5), (97, 0.08, 3.0), (198, 0.06, 3.2), (320, 0.07, 3.0), (128, 0.05, 2.6)):
        frac = frac + dep * _bump(_dth(th, deg), w, 1.4)
    flute = 1.3 * (0.5 + 0.5 * np.sin(s_arc * TAU / 8.5 + 1.3 * M.ring_noise(th, 2, (7, 13), (1, .6)))) * _bump(_dth(th, 70), 0.62, 0.8)
    butt = _bump(_dth(th, 270), 0.45, 0.8) + _bump(_dth(th, 62), 0.12, 1.0)               # prow of the quay and the crag buttress: cliff drops straight
    inset = np.zeros(N)
    for s in range(S):
        dtop = depths[-1]; dbot = Dc * cum[:, s]; T = dbot - dtop
        rn = M.ring_noise(th * (1 + 0.5 * s) + s * 2.3, seed + 40 + s, (4, 7, 12, 19), (1, .8, .5, .3))
        batter = 0.05 + 0.10 * (0.5 + 0.5 * rn) - 0.14 * np.clip(rn - 0.55, 0, 1) * 2.2                       # some layers undercut
        face_in = inset + batter * T + (frac * (0.35 + 0.22 * s) * (s < S - 1 or True)) * (1.0 if s == 0 else 0.45) + flute * (0.8 if s < 2 else 0.3)
        face_in = np.maximum(face_in, inset - 0.3)
        ledge = (2.6 * M.smooth(-0.15, 0.7, M.ring_noise(th * 1.3 + s * 4.1, seed + 60 + s, (5, 9, 15, 24), (1, .8, .5, .3))) + 0.2) * (1 - 0.8 * butt)
        ledge = ledge * (1 - 0.7 * np.clip(frac / 4.0, 0, 1))
        depths.append(dbot - 0.4); insets.append(face_in)
        inset = face_in + ledge; depths.append(dbot); insets.append(inset)
    # smooth the inset along the rim so rings never zig-zag; keep fractures sharp enough
    def circ(a, k=2):
        return sum(np.roll(a, i) for i in range(-k, k + 1)) / (2 * k + 1)
    insets = [np.minimum(circ(i), 0.5 * r) for i in insets]
    rings = []
    for d, i in zip(depths, insets):
        P = np.array([cx, cy]) + (r - i)[:, None] * u
        rings.append(np.column_stack([P[:, 0], P[:, 1], zr - d]))
    # underside
    Pc = rings[-1][:, :2]; dc = depths[-1]
    A0, A1 = np.array(sp["keel"][0]), np.array(sp["keel"][1]); ab = A1 - A0; tt = np.clip(((Pc - A0) @ ab) / (ab @ ab), 0, 1); K = A0 + tt[:, None] * ab
    pexp = sp["p"] + 0.35 * M.ring_noise(th, seed + 80, (3, 5, 9), (1, .6, .3))
    for j in range(1, J + 1):
        t = (j / J) ** 1.2; d = dc + t * (D - dc)
        lump = 1 + 0.16 * M.ring_noise(th * 1.7 + t * 4.0, seed + 90, (2, 4, 7, 11), (1, .8, .5, .3)) * np.sin(math.pi * min(t * 1.1, 1.0)) ** 0.7
        stepw = 0.9 * np.sin(d * 0.9 + th * 3.0) * (1 - t) ** 2 * (t < 0.6)                            # bedding ledges continue into the upper underside
        s = np.clip((1 - t) ** pexp, 0.0, 1.0) * lump
        P = K + (Pc - K) * s[:, None] + (Pc - K) / np.maximum(np.linalg.norm(Pc - K, axis=1, keepdims=True), 1e-6) * stepw[:, None]
        rings.append(np.column_stack([P[:, 0], P[:, 1], zr - d]))
    # 3D rock noise on everything below the rim: ridges, bulges, gullies (zero at the rim, so the top and shell stay joined)
    out = []
    for k, R in enumerate(rings):
        dep = zr - R[:, 2]; w = M.smooth(0.0, 3.0, dep)
        amp = 0.5 + 1.4 * M.smooth(Dc.mean() * 0.6, Dc.mean() * 2.0, dep)
        n1 = noise3(R[:, 0], R[:, 1], R[:, 2], seed + 100); n2 = noise3(R[:, 0] * 1.9, R[:, 1] * 1.9, R[:, 2] * 1.9, seed + 101, ((9, 1.0), (4.2, 0.6), (2.2, 0.3)))
        radial = np.column_stack([u[:, 0], u[:, 1], np.zeros(N)])
        n3 = 1.0 - 2.0 * np.abs(noise3(R[:, 0] * 1.3, R[:, 1] * 1.3, R[:, 2] * 0.9, seed + 102, ((13, 1.0), (6, 0.6))))                 # ridged: creases and arêtes
        Rn = R.copy(); Rn += (w * amp * (0.7 * n1 + 0.45 * n2 + 0.55 * n3))[:, None] * radial; Rn[:, 2] += w * 0.45 * n2
        out.append(Rn)
    rings = out
    # keep the bottom ring on its keel line (no noise), cap it
    nr = len(rings)
    V = np.concatenate(rings, 0); F = []
    for k in range(nr - 1):
        for i in range(N):
            a = k * N + i; b = k * N + (i + 1) % N; cc = (k + 1) * N + i; d = (k + 1) * N + (i + 1) % N
            if (i + k) % 2: F += [(a, b, d), (a, d, cc)]
            else: F += [(a, b, cc), (b, d, cc)]
    F = np.array(F)
    info = dict(N=N, rings=nr, zr=zr, th=th, u=u, r=r, Dc=Dc, D=D, K=K, pts=pts, cliff_rings=1 + 2 * S, depth_rings=depths)
    return V, F, info


def shell_colours(V, F, info):
    nrm = vertex_normals(V, F); x, y, z = V[:, 0], V[:, 1], V[:, 2]
    col = layer_colour(z, x, y)
    nr = info["rings"]; N = info["N"]
    dep = np.tile(info["zr"], nr) - z
    t = np.clip((dep - info["Dc"].mean()) / max(info["D"].mean() - info["Dc"].mean(), 1.0), 0, 1)
    dark = 1.0 - 0.40 * M.smooth(0.0, 1.0, t)
    col = col * dark[:, None] + BASALT * (0.35 * M.smooth(0.55, 1.0, t))[:, None] * 1.0
    up = np.clip(nrm[:, 2], 0, 1); down = np.clip(-nrm[:, 2], 0, 1)
    col = col * (1 - 0.35 * down)[:, None]                                                                # undersides of ledges and overhangs: AO-like
    moss = (up > 0.55) & (dep < info["Dc"].mean() + 6)
    col = np.where(moss[:, None], col * 0.55 + np.array([0.28, 0.38, 0.15]) * 0.45, col)               # ledge tops carry moss / grass
    seep = 0.5 + 0.5 * noise3(x * 3.0, y * 3.0, z * 0.25, 33, ((14, 1.0), (6, 0.6)))
    col = col * (1 - 0.22 * (seep > 0.72)[:, None])                                                      # dark vertical seep stains
    return np.clip(col, 0, 1)


# ---------------------------------------------------------------------------------------------------- top colours
def top_colours(x, n, z, nrm_z, stack=False):
    slope = np.sqrt(np.clip(1 - nrm_z ** 2, 0, 1)) / np.maximum(nrm_z, 1e-3)
    var = 0.5 + 0.5 * M.field_noise(x, n, 3, (30, 14, 7), (1, .6, .35))
    grass = np.array([0.30, 0.44, 0.17]) * (0.85 + 0.30 * var)[:, None] + np.array([0.06, 0.04, 0.0]) * (var > 0.55)[:, None]
    dry = np.array([0.50, 0.47, 0.27]); lush = np.array([0.20, 0.38, 0.14])
    col = grass * (1 - 0.35 * M.smooth(0.55, 0.9, var))[:, None] + lush * (0.35 * M.smooth(0.55, 0.9, var))[:, None]
    pad = (M.rect_dist(x, n, M.PAD) < 0.5)
    col = np.where(pad[:, None], 0.55 * col + 0.45 * dry, col)
    # tea soil on the benches and their contours
    d = np.hypot(x - M.LOOKOUT[0], n - M.LOOKOUT[1]); tea = (x > 47) & (x < 99) & (n < 90) & (n > 4) & (z < -0.6)
    dw = d + 2.4 * M.field_noise(x, n, 91, (38, 21, 12), (1, 0.6, 0.35)); u = (dw - M.TEA_D0) / M.TEA_W; f = u - np.floor(u)       # P3-B batch 2: soil only in the planting rows, grass between
    wr = np.maximum(np.exp(-((f - 0.22) / 0.10) ** 2), np.exp(-((f - 0.58) / 0.10) ** 2)); laterite = np.array([0.45, 0.28, 0.18])
    lushg = np.array([0.27, 0.45, 0.16]) * (0.85 + 0.3 * var)[:, None]
    col = np.where(tea[:, None], lushg * (1 - wr)[:, None] + laterite * wr[:, None] * 0.55, col)
    # quay: warm stone paving; ramp likewise
    quay = (n < -26.5)
    stone = np.array([0.56, 0.52, 0.45]) * (0.94 + 0.10 * var)[:, None]
    col = np.where(quay[:, None], stone, col)
    # paths: packed earth (road: stone)
    pdist = M.path_distance(x, n)
    earth = np.array([0.66, 0.55, 0.38]); inpath = (pdist < 0.2) & (n > -26)
    col = np.where(inpath[:, None], earth * (0.9 + 0.2 * var)[:, None], col)
    # stream bed and pond
    sd = M.stream_distance(x, n); col = np.where((sd < 1.1)[:, None], np.array([0.20, 0.27, 0.22]), col)
    # steep ground: dry-stone terraces / rock; crag rock above the grass line
    rock = layer_colour(z, x, n)
    w = M.smooth(0.45, 0.95, slope) + (z > 8.0) * M.smooth(0.40, 0.75, slope) * 0.55
    col = col * (1 - np.clip(w, 0, 1))[:, None] + rock * np.clip(w, 0, 1)[:, None]
    lip = (M.edge_distance(M.MAIN, x, n) < 1.6) & (M.edge_distance(M.MAIN, x, n) >= 0)
    col = np.where(lip[:, None], 0.6 * col + 0.4 * rock, col)
    cls = np.select([quay, inpath, w > 0.5, tea], [2, 1, 3, 4], 0).astype(np.float32)
    return np.clip(col, 0, 1), cls
