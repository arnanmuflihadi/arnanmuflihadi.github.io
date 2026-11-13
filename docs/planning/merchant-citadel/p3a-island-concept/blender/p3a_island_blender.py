"""Merchant Citadel P3-A: island MASSING PROTOTYPES round the real, built town (concept evidence, not production terrain).

Opens the saved batch-5 Blender assembly of the 24-building town (unchanged), removes only the temporary ground plane, builds the
massing of one concept from p3a_island_shape.py (terrain top, cliffs with strata, underside, massing trees, tea rows, paths,
water) and renders named views. Everything this script adds is named P3A_* and is temporary concept geometry.

Run: Blender --background <town.blend> --python p3a_island_blender.py -- <out_dir> <concept A|B|C> <view,view,...|all> [--save]
"""
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p3a_island_shape as S                                      # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
OUT, KEY, VIEWS = args[0], args[1], args[2]
SAVE = "--save" in args
os.makedirs(OUT, exist_ok=True)
C = S.CONCEPTS[KEY]; F = S.FEATURES[KEY]; IS_C = C.get("base", KEY) == "C"
rng = np.random.default_rng(C["seed"] + 1)
NS, NR = 384, 96
STATS = {"concept": KEY, "name": C["name"], "triangles": {}}

for name in ("TMP_ground",):
    o = bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)
coll = bpy.data.collections.new("P3A_" + KEY); bpy.context.scene.collection.children.link(coll)


def mat(name, rgb, rough=0.92, emit=0.0, alpha=1.0):
    m = bpy.data.materials.new("P3A_" + name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    return m


M = {k: mat(k, *v) for k, v in {
    "grass": ((0.20, 0.27, 0.10),), "meadow": ((0.27, 0.31, 0.12),), "tea": ((0.10, 0.22, 0.09),), "tea_soil": ((0.25, 0.21, 0.13),),
    "rock_cream": ((0.62, 0.55, 0.42),), "rock_ochre": ((0.52, 0.38, 0.22),), "rock_red": ((0.45, 0.22, 0.15),), "rock_dark": ((0.20, 0.17, 0.15),),
    "rock_under": ((0.30, 0.25, 0.21),), "path": ((0.50, 0.42, 0.30),), "quay": ((0.46, 0.44, 0.41),), "water": ((0.20, 0.45, 0.62), 0.15),
    "fall": ((0.80, 0.90, 0.96), 0.4, 0.35), "tree_a": ((0.09, 0.20, 0.08),), "tree_b": ((0.15, 0.27, 0.09),), "trunk": ((0.22, 0.15, 0.10),),
    "cloud": ((0.95, 0.96, 0.98), 0.9, 0.25), "timber": ((0.33, 0.22, 0.13),)}.items()}
MATLIST = list(M.keys())


def finish(bm, name, flat=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for k in MATLIST:
        me.materials.append(M[k])
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    if not flat:
        for p in me.polygons:
            p.use_smooth = True
    STATS["triangles"][name] = STATS["triangles"].get(name, 0) + sum(len(p.vertices) - 2 for p in me.polygons)
    return o


def mi(k):
    return MATLIST.index(k)


# ------------------------------------------------------------------ one landmass: top, cliff, underside
def build_landmass(c, tag):
    th = np.linspace(0, S.TAU, NS, endpoint=False); cx, cy = c["centre"]; R = S.outline(c, th)
    bm = bmesh.new()
    # top
    fr = (np.arange(1, NR + 1) / NR) ** 0.92
    X = cx + np.outer(fr, R * np.cos(th)); Y = cy + np.outer(fr, R * np.sin(th)); Z = S.top_height(c, X, Y)
    v0 = bm.verts.new((cx, cy, float(S.top_height(c, np.array([cx]), np.array([cy]))[0])))
    rings = [[bm.verts.new((X[j, i], Y[j, i], Z[j, i])) for i in range(NS)] for j in range(NR)]
    is_main = "height" in c

    def top_mat(vs):
        zs = [v.co.z for v in vs]; ctr = sum((v.co for v in vs), Vector()) / len(vs)
        a, b, cc = vs[0].co, vs[1].co, vs[-1].co; nrm = (b - a).cross(cc - a); slope = 1.0 if nrm.length == 0 else abs(nrm.normalized().z)
        if slope < 0.80:
            return mi("rock_cream") if (int(ctr.z / 3.6) % 2 == 0) else mi("rock_ochre")
        if IS_C and is_main:
            if -32.5 < ctr.y < -24.0:
                return mi("rock_cream")                              # the retaining bank between the quay and the arrival court
            if ctr.y <= -32.5:
                return mi("quay")
            if ctr.x > 48 and -2 < ctr.y < 90 and ctr.z < 0.2:
                return mi("tea_soil")
            if ((ctr.x + 56) / 24) ** 2 + ((ctr.y - 18) / 28) ** 2 < 1:
                return mi("meadow")
        if KEY == "B" and not is_main and c["key"] == "B-quay":
            return mi("quay")
        return mi("grass")

    for i in range(NS):
        f = bm.faces.new((v0, rings[0][i], rings[0][(i + 1) % NS])); f.material_index = top_mat(f.verts)
    for j in range(NR - 1):
        for i in range(NS):
            vs = (rings[j][i], rings[j + 1][i], rings[j + 1][(i + 1) % NS], rings[j][(i + 1) % NS])
            f = bm.faces.new(vs); f.material_index = top_mat(vs)
    # cliff and underside
    zr = Z[-1]; D = np.asarray(c["depth"](th), float); Dc = c["cliff"]; ax, ay = c["apex"]; L = c.get("keel_len", 0.0)
    Dbar = D.min() + (D.max() - D.min()) * S.smooth(-1.0, 1.0, np.sin(th)) if L else np.full_like(th, D.max())
    prev = rings[-1]; levels = [("cliff", d) for d in np.arange(1.1, Dc + 0.01, 1.1)] + [("under", t) for t in np.linspace(0.03, 1.0, 34)]
    for kind, v in levels:
        if kind == "cliff":
            dep = np.full_like(th, v); t = np.zeros_like(th)
        else:
            t = np.full_like(th, v); dep = Dc + t * (D - Dc)
        r, _ = S.ring_radius(c, th, dep)
        s = S.smooth(0.0, 1.0, t)
        px = (1 - s) * cx + s * (cx + ax) + r * np.cos(th); py = (1 - s) * cy + s * (cy + ay + L * np.sin(th)) + r * np.sin(th)
        b = S.smooth(0.5, 1.0, t); pz = (1 - b) * (zr - dep) + b * (-Dbar)
        ring = [bm.verts.new((px[i], py[i], pz[i])) for i in range(NS)]
        for i in range(NS):
            f = bm.faces.new((prev[i], ring[i], ring[(i + 1) % NS], prev[(i + 1) % NS]))
            if kind == "cliff":
                layer = int(v / S.STRATA); f.material_index = mi(("rock_cream", "rock_cream", "rock_ochre", "rock_cream", "rock_red", "rock_ochre")[layer % 6])
            else:
                f.material_index = mi("rock_ochre") if v < 0.12 else (mi("rock_under") if v < 0.55 else mi("rock_dark"))
        prev = ring
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    o = finish(bm, "P3A_landmass_" + tag)
    return {"R": R, "th": th, "zr": zr, "D": D, "Dbar": Dbar}


def cone(bm, base, radius, height, sides, k, tip_scale=0.0, rot=0.0):
    bx, by, bz = base; ring = [bm.verts.new((bx + radius * math.cos(rot + S.TAU * i / sides), by + radius * math.sin(rot + S.TAU * i / sides), bz)) for i in range(sides)]
    if tip_scale > 0:
        top = [bm.verts.new((bx + radius * tip_scale * math.cos(rot + S.TAU * i / sides), by + radius * tip_scale * math.sin(rot + S.TAU * i / sides), bz + height)) for i in range(sides)]
        for i in range(sides):
            bm.faces.new((ring[i], ring[(i + 1) % sides], top[(i + 1) % sides], top[i])).material_index = k
        bm.faces.new(top).material_index = k
    else:
        tip = bm.verts.new((bx, by, bz + height))
        for i in range(sides):
            bm.faces.new((ring[i], ring[(i + 1) % sides], tip)).material_index = k


def h_at(c, x, y):
    return float(S.top_height(c, np.array([float(x)]), np.array([float(y)]))[0])


def ribbon(c, pts, width, k, name, lift=0.08, step=1.0):
    bm = bmesh.new(); prev = None; pts = [Vector((p[0], p[1], 0)) for p in pts]
    samples = []
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int((b - a).length / step))
        samples += [a.lerp(b, i / n) for i in range(n)]
    samples.append(pts[-1])
    for i, p in enumerate(samples):
        d = (samples[min(i + 1, len(samples) - 1)] - samples[max(i - 1, 0)]); d = d.normalized() if d.length else Vector((1, 0, 0)); nrm = Vector((-d.y, d.x, 0)) * width / 2
        l, r = p + nrm, p - nrm
        vl = bm.verts.new((l.x, l.y, h_at(c, l.x, l.y) + lift)); vr = bm.verts.new((r.x, r.y, h_at(c, r.x, r.y) + lift))
        if prev:
            bm.faces.new((prev[0], prev[1], vr, vl)).material_index = k
        prev = (vl, vr)
    return finish(bm, name)


def blocked_for_planting(x, y):
    if S.rect_dist(np.array([x]), np.array([y]), (-38.0, 47.0, -24.0, 76.0))[0] < 0.5:
        return True
    if abs(x) < 20 and 70 < y < 96:
        return True
    for p in F.get("paths", []) + F.get("water", []):
        for a, b in zip(p[:-1], p[1:]):
            ab = Vector((b[0] - a[0], b[1] - a[1])); ap = Vector((x - a[0], y - a[1])); t = max(0, min(1, ap.dot(ab) / max(ab.length_squared, 1e-6)))
            if (ap - ab * t).length < 3.0:
                return True
    for _, lx, ly, lr in F.get("landing", []):
        if math.hypot(x - lx, y - ly) < lr + 2:
            return True
    for _, vx, vy, _a in F.get("viewpoints", []):                  # keep every viewpoint and its outlook clear
        if math.hypot(x - vx, y - vy) < 12:
            return True
    return False


def plant(c):
    bm = bmesh.new(); n_trees = 0
    spots = []
    for wx, wy, rx, ry in F.get("woods", []):
        for _ in range(int(rx * ry * math.pi / 26)):
            a = rng.uniform(0, S.TAU); q = math.sqrt(rng.uniform(0, 1)); spots.append((wx + q * rx * math.cos(a), wy + q * ry * math.sin(a), 1.0))
    th = rng.uniform(0, S.TAU, 260); rr = np.sqrt(rng.uniform(0, 1, 260))
    cx, cy = c["centre"]; R = S.outline(c, th)
    spots += [(cx + rr[i] * R[i] * math.cos(th[i]), cy + rr[i] * R[i] * math.sin(th[i]), 0.8) for i in range(260) if rng.uniform() < 0.34]
    for x, y, sc in spots:
        if not S.contains(c, np.array([x]), np.array([y]), 3.5)[0] or blocked_for_planting(x, y):
            continue
        if IS_C and x > 47 and -2 < y < 88 and h_at(c, x, y) < 0.3 and rng.uniform() < 0.85:
            continue                                                 # keep the tea benches open
        z = h_at(c, x, y); hgt = rng.uniform(6.0, 11.0) * sc; rad = hgt * rng.uniform(0.24, 0.34); k = mi("tree_a") if rng.uniform() < 0.55 else mi("tree_b")
        cone(bm, (x, y, z - 0.2), 0.32 * sc, hgt * 0.35, 5, mi("trunk"), tip_scale=0.7)
        if rng.uniform() < 0.5:                                      # layered conifer
            for q in range(3):
                cone(bm, (x, y, z + hgt * (0.22 + 0.22 * q)), rad * (1 - 0.22 * q), hgt * 0.42, 7, k, rot=rng.uniform(0, 1))
        else:                                                        # broad crown
            cone(bm, (x, y, z + hgt * 0.28), rad * 1.25, hgt * 0.34, 7, k, tip_scale=1.15); cone(bm, (x, y, z + hgt * 0.62), rad * 1.44, hgt * 0.38, 7, k)
        n_trees += 1
    STATS["trees"] = n_trees
    return finish(bm, "P3A_trees")


def tea_rows(c):
    """Low hedge strips along the bench contours: reads as tea rows from the lookout and from the air."""
    bm = bmesh.new(); k = mi("tea"); rows = 0
    for bench in range(0, 6):
        for off in (1.6, 3.4, 5.2):
            d = S.TEA[0] + S.TEA[1] * (bench + 1) + off * S.TEA[1] / 7.0; prev = None
            for a in np.arange(math.radians(-62), math.radians(66), 1.3 / d):
                x, y = 36 + d * math.cos(a), 57 + d * math.sin(a)
                ok = x > 48.5 and -1 < y < 86 and S.contains(c, np.array([x]), np.array([y]), 3.0)[0] and not blocked_for_planting(x, y)
                if not ok:
                    prev = None; continue
                z = h_at(c, x, y); nx, ny = math.cos(a) * 0.36, math.sin(a) * 0.36
                cur = [bm.verts.new((x - nx, y - ny, z)), bm.verts.new((x - nx * 0.6, y - ny * 0.6, z + 0.6)), bm.verts.new((x + nx * 0.6, y + ny * 0.6, z + 0.6)), bm.verts.new((x + nx, y + ny, z))]
                if prev:
                    for q in range(3):
                        bm.faces.new((prev[q], prev[q + 1], cur[q + 1], cur[q])).material_index = k
                    rows += 1
                prev = cur
    STATS["tea_row_segments"] = rows
    return finish(bm, "P3A_tea_rows")


def hanging_rock(info, c):
    """Pinnacles under the hull and a few detached boulders near the rim (massing)."""
    bm = bmesh.new(); cx, cy = c["centre"]; ax, ay = c["apex"]; n = 0
    for _ in range(34):
        a = rng.uniform(0, S.TAU); t = rng.uniform(0.15, 0.85); i = int(a / S.TAU * NS) % NS
        dep = c["cliff"] + t * (info["D"][i] - c["cliff"]); r, _ = S.ring_radius(c, np.array([a]), np.array([dep])); s = float(S.smooth(0, 1, t))
        q = rng.uniform(0.25, 0.9); x = cx + s * ax + q * r[0] * math.cos(a); y = cy + s * (ay + c.get("keel_len", 0) * math.sin(a)) + q * r[0] * math.sin(a)
        z = (1 - float(S.smooth(0.5, 1, t))) * (info["zr"][i] - dep) + float(S.smooth(0.5, 1, t)) * (-info["Dbar"][i])
        length = rng.uniform(10, 34); cone(bm, (x, y, z + 6), rng.uniform(2.4, 6.0), -(length + 6), 6, mi("rock_under") if rng.uniform() < 0.5 else mi("rock_dark"), rot=rng.uniform(0, 1)); n += 1
    for deg, width, depth in c.get("notches", []):                   # debris floating in each fracture
        for _ in range(3):
            a = math.radians(deg + rng.uniform(-width, width) * 0.6); rr = float(S.outline(c, np.array([a]))[0]) + rng.uniform(4, 14)
            x, y, z = cx + rr * math.cos(a), cy + rr * math.sin(a), rng.uniform(-26, -4); sz = rng.uniform(1.8, 4.5)
            cone(bm, (x, y, z), sz, sz * 1.1, 6, mi("rock_cream")); cone(bm, (x, y, z), sz, -sz * 1.9, 6, mi("rock_ochre")); n += 1
    for _ in range(c.get("roots", 0)):                               # selected design: long roots under the thick northern end
        x, y = cx + rng.uniform(-34, 40), cy + rng.uniform(18, 62); length = rng.uniform(30, 58)
        cone(bm, (x, y, -34), rng.uniform(5, 9), -(length + 30), 7, mi("rock_dark"), rot=rng.uniform(0, 1)); n += 1
    STATS["hanging_rocks"] = n
    return finish(bm, "P3A_hanging_rock")


def box(name, lo, hi, k):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector(((lo[0] + hi[0]) / 2 + v.co.x * (hi[0] - lo[0]), (lo[1] + hi[1]) / 2 + v.co.y * (hi[1] - lo[1]), (lo[2] + hi[2]) / 2 + v.co.z * (hi[2] - lo[2])))
    for f in bm.faces:
        f.material_index = k
    return finish(bm, name)


def clouds():
    bm = bmesh.new()
    for _ in range(46):
        a = rng.uniform(0, S.TAU); d = rng.uniform(170, 900); x, y, z = 5 + d * math.cos(a), 40 + d * math.sin(a), rng.uniform(-190, -60); s = rng.uniform(26, 80)
        for q in range(4):
            m = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
            ox, oy, sz = rng.uniform(-0.8, 0.8) * s, rng.uniform(-0.5, 0.5) * s, rng.uniform(0.45, 1.0) * s
            for v in m["verts"]:
                v.co = Vector((x + ox + v.co.x * sz, y + oy + v.co.y * sz * 0.8, z + v.co.z * sz * 0.22))
    for f in bm.faces:
        f.material_index = mi("cloud")
    o = finish(bm, "P3A_clouds", flat=False); o.visible_shadow = False
    return o


# ------------------------------------------------------------------ build
info = build_landmass(C, "main")
for sat in C.get("satellites", []):
    sat_info = build_landmass(sat, sat["key"])
hanging_rock(info, C)
plant(C)
for i, p in enumerate(F.get("paths", [])):
    ribbon(C, p, 2.6 if i else 5.0, mi("path"), "P3A_path_%d" % i)
for i, p in enumerate(F.get("water", [])):
    ribbon(C, p, 2.4, mi("water"), "P3A_stream_%d" % i, lift=0.12)
for i, ((fx, fy), drop) in enumerate(F.get("falls", [])):
    a = math.atan2(fy - C["centre"][1], fx - C["centre"][0]); rr = float(S.outline(C, np.array([a]))[0]) + 0.8
    ex, ey = C["centre"][0] + rr * math.cos(a), C["centre"][1] + rr * math.sin(a); z0 = h_at(C, ex - 3 * math.cos(a), ey - 3 * math.sin(a))
    bm = bmesh.new(); tx, ty = -math.sin(a) * 1.6, math.cos(a) * 1.6; prev = None
    for q in range(0, 13):
        f = q / 12; out = 1.0 + 4.5 * f ** 0.6; w = 1 + 0.9 * f
        cur = (bm.verts.new((ex + out * math.cos(a) - tx * w, ey + out * math.sin(a) - ty * w, z0 - drop * f ** 1.5)), bm.verts.new((ex + out * math.cos(a) + tx * w, ey + out * math.sin(a) + ty * w, z0 - drop * f ** 1.5)))
        if prev:
            bm.faces.new((prev[0], prev[1], cur[1], cur[0])).material_index = mi("fall")
        prev = cur
    finish(bm, "P3A_cloudfall_%d" % i)
    ribbon(C, [(fx - 6 * math.cos(a), fy - 6 * math.sin(a)), (ex, ey)], 2.4, mi("water"), "P3A_fall_lip_%d" % i, lift=0.12)
if IS_C:
    tea_rows(C)
    for sx in (-12, -4, 4, 12, 20):                                  # mooring bollards on the Sky Quay (massing)
        box("P3A_bollard", (sx - 0.35, -72.0, h_at(C, sx, -72)), (sx + 0.35, -71.3, h_at(C, sx, -72) + 1.1), mi("timber"))
    for q in range(10):                                              # the quay stair: ten 0.3 m risers, 14 m wide, on the town axis (massing)
        box("P3A_quay_stair", (-7.0, -31.2 + 0.62 * q, -3.1), (7.0, -24.6, -3.0 + 0.3 * (q + 1)), mi("quay"))
    for sx in (-8.2, 7.0):
        box("P3A_quay_stair_cheek", (sx, -31.6, -3.1), (sx + 1.2, -24.2, 0.9), mi("rock_cream"))
    box("P3A_quay_beacon", (-17.6, -58.0, h_at(C, -17, -57)), (-16.0, -56.4, h_at(C, -17, -57) + 8.0), mi("quay"))          # prow beacon tower (massing landmark for arrival)
    box("P3A_counting_stone", (43.5, 113.0, h_at(C, 44.5, 114)), (45.5, 115.0, h_at(C, 44.5, 114) + 4.2), mi("rock_cream"))  # summit marker
for (p0, p1, w, za, zb) in F.get("bridges", []):
    a, b = Vector((p0[0], p0[1])), Vector((p1[0], p1[1])); d = (b - a); n = Vector((-d.y, d.x)).normalized() * w / 2
    bm = bmesh.new()
    vs = [bm.verts.new((a.x + n.x, a.y + n.y, za)), bm.verts.new((a.x - n.x, a.y - n.y, za)), bm.verts.new((b.x - n.x, b.y - n.y, zb)), bm.verts.new((b.x + n.x, b.y + n.y, zb))]
    lo = [bm.verts.new((v.co.x, v.co.y, v.co.z - 0.6)) for v in vs]
    bm.faces.new(vs).material_index = mi("timber"); bm.faces.new(lo[::-1]).material_index = mi("timber")
    for q in range(4):
        bm.faces.new((vs[q], lo[q], lo[(q + 1) % 4], vs[(q + 1) % 4])).material_index = mi("timber")
    finish(bm, "P3A_bridge")
for (px, py, pr) in F.get("ponds", []):
    bm = bmesh.new(); z = h_at(C, px, py) + 0.18
    bm.faces.new([bm.verts.new((px + pr * math.cos(S.TAU * q / 14), py + pr * 0.8 * math.sin(S.TAU * q / 14), z)) for q in range(14)]).material_index = mi("water")
    finish(bm, "P3A_tarn")
for (px, py, half, hgt) in F.get("pavilions", []):                   # massing of an open pavilion (the tea-drying loft on the stack)
    z = -5.0 + 0.4
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        box("P3A_pavilion_post", (px + sx * half * 0.5 - 0.2, py + sy * half * 0.5 - 0.2, z), (px + sx * half * 0.5 + 0.2, py + sy * half * 0.5 + 0.2, z + hgt * 0.6), mi("timber"))
    bm = bmesh.new(); cone(bm, (px, py, z + hgt * 0.6), half * 0.95, hgt * 0.5, 4, mi("rock_red"), rot=math.pi / 4); finish(bm, "P3A_pavilion_roof")
clouds()

# ------------------------------------------------------------------ light and sky for a floating island (declared: the lower hemisphere is sky haze, not ground bounce)
sc = bpy.context.scene
w = sc.world
if w and w.use_nodes:
    for n in w.node_tree.nodes:
        if n.type == "VALTORGB":
            n.color_ramp.elements[0].color = (0.74, 0.83, 0.93, 1); n.color_ramp.elements[1].color = (0.90, 0.88, 0.84, 1)
sc.render.resolution_x, sc.render.resolution_y = 1600, 900
for attr, val in (("shadow_ray_count", 1), ("taa_render_samples", 32)):
    try:
        setattr(sc.eevee, attr, val)
    except Exception:
        pass
sun = bpy.data.objects.get("SUN")
if sun:
    try:
        sun.data.shadow_cascade_max_distance = 900
    except Exception:
        pass


def camera(name, loc, look, fov=None, ortho=None):
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name)); sc.collection.objects.link(cam); cam.location = loc
    cam.rotation_euler = (Vector(loc) - Vector(look)).to_track_quat("Z", "Y").to_euler()
    if ortho:
        cam.data.type = "ORTHO"; cam.data.ortho_scale = ortho; cam.rotation_euler = (0, 0, 0)       # north up
    else:
        cam.data.sensor_fit = "VERTICAL"; cam.data.angle_y = math.radians(fov or 50)
    cam.data.clip_start, cam.data.clip_end = 0.3, 6000
    return cam


def figure(x, y):
    z = h_at(C, x, y) + 0.03 if S.rect_dist(np.array([x]), np.array([y]), S.PAD)[0] > 0 else 0.01
    m = bpy.data.materials.get("TMP_explorer") or mat("explorer", (0.05, 0.42, 0.45))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.56, location=(x, y, z + 0.78)); a = bpy.context.object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(x, y, z + 1.73)); b = bpy.context.object
    for o in (a, b):
        o.data.materials.append(m); o.name = "P3A_figure"
    return [a, b]


Q = h_at(C, 0, -52)
VIEW = {
    # comparison set (identical cameras for every concept)
    "cmp-aerial": ((235, -195, 118), (5, 40, -16), 36, None, None),
    "cmp-side": ((390, 40, -8), (5, 44, -24), 30, None, None),
    "cmp-top": ((5, 30, 500), (5, 30, 0), None, 250, None),
    "cmp-approach": ((-360, -300, 60), (5, 40, -14), 32, None, None),
    # the selected concept's full set
    "v1-aerial": ((225, -185, 120), (5, 36, -14), 38, None, None),
    "v1b-aerial-northwest": ((-210, 250, 140), (5, 46, -8), 38, None, None),
    "v2-side-east": ((400, 30, -6), (5, 40, -24), 30, None, None),
    "v2b-side-south": ((20, -430, -6), (5, 30, -24), 30, None, None),
    "v3-southern-arrival": ((1.2, -66.0, Q + 4.8), (0, 20, 9.0), 56, None, (-2.6, -57)),
    "v3b-arrival-edge": ((78, -118, 16), (0, -34, -6), 42, None, None),
    "v4-exchange-hall": ((0, 47.5, 7.2), (0, 84, 10.5), 60, None, (0, 59.3)),
    "v4b-hall-from-street": ((0, 14, 5.0), (0, 84, 11), 50, None, (0, 24)),
    "v5-tea-lookout": ((32.2, 55.4, 4.6), (88, 58, -13.0), 62, None, (37.5, 56.6)),
    "v5b-tea-benches": ((47, 40, 9), (84, 64, -9), 60, None, (58, 46)),
    "v6-dragon-approach": ((-420, -330, 95), (5, 40, -8), 26, None, None),
    "v6b-dragon-approach-east": ((330, 250, 70), (5, 44, -10), 30, None, None),
    "v7-top": ((12, 30, 500), (12, 30, 0), None, 250, None),
    "v8-crag-to-town": ((46.0, 124.5, h_at(C, 40, 116) + 6.0), (2, 62, 4), 58, None, (38.0, 113.0)),
    "v9-caravan-green": ((-74, 4, 9), (-18, 38, 6), 55, None, (-50, 18)),
}
want = list(VIEW) if VIEWS == "all" else VIEWS.split(",")
for name in want:
    pos, look, fov, ortho, who = VIEW[name]
    fig = figure(*who) if who else []
    cam = camera(name, pos, look, fov, ortho); sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = (1500, 1500) if ortho else (1600, 900); sc.render.filepath = os.path.join(OUT, "%s-%s.png" % (KEY, name))
    bpy.ops.render.render(write_still=True); print("[p3a] rendered", sc.render.filepath, flush=True)
    for o in fig:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.objects.remove(cam, do_unlink=True)

STATS["total_triangles"] = sum(STATS["triangles"].values())
th = info["th"]; R = info["R"]; cx, cy = C["centre"]
STATS["extent_x"] = [float((cx + R * np.cos(th)).min()), float((cx + R * np.cos(th)).max())]; STATS["extent_n"] = [float((cy + R * np.sin(th)).min()), float((cy + R * np.sin(th)).max())]
STATS["top_area_m2"] = float(0.5 * np.sum(R * R) * (th[1] - th[0])); STATS["depth_m"] = [float(info["D"].min()), float(info["D"].max())]
json.dump(STATS, open(os.path.join(OUT, "%s-massing-stats.json" % KEY), "w"), indent=1)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "p3a-island-%s-with-town.blend" % KEY), compress=True)
print("[p3a] done", json.dumps(STATS["triangles"]), flush=True)
