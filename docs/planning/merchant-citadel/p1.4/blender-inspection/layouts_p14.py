#!/usr/bin/env python3
"""Merchant Citadel P1.4 - layout alternatives (plain Python, single source of truth).

Baseline  B  = the P1.3 selected layout (22 buildings), imported unchanged from layouts_p13.
          D  = "Terraced Citadel": the P1.3 street network kept, the civic court raised 1 m as a terrace, corner tower houses,
               a merchants' inn, two more bazaar-edge shops, the bazaar's free stalls replaced by four awning rows along a
               market street, several buildings turned off the grid by 6-15 degrees.  24 buildings.
          E  = "Crooked Spine": D with the whole southern quarter swung 14 degrees about the street junction, so the merchant
               street bends and the hall is revealed at the junction.  23 buildings (one workshop has no room on the inside of the bend).

Plan coordinates: x = east, n = north (metres); project (x, y, z) = (x, elevation, -n).  rz: 0 = front faces south, 90 = east,
-90 = west, 180 = north; any angle is allowed in P1.4 (footprints are oriented rectangles).
"""
import math
import layouts_p13 as L13
from layouts_p13 import COBBLE, BRICK, RED, S

FOOT = dict(L13.FOOT); FOOT.update({"A09": (10, 8), "A11": (8, 8), "A11m": (8, 8)})
EAVE = dict(L13.EAVE); EAVE.update({"A09": 6.0, "A11": 6.0, "A11m": 6.0})
FRONT_EXTRA = {"A08": 2, "A09": 2}
BASE = {b[0]: b for b in L13.ALT_B}


def status(bid, arch, x, n, rz):
    if bid not in BASE:
        return "new"
    _, a0, _, x0, n0, r0 = BASE[bid][:6]
    out = []
    if a0 != arch: out.append(f"re-typed {a0} to {arch}")
    if (x0, n0) != (x, n): out.append(f"moved {math.hypot(x - x0, n - n0):.1f} m")
    if r0 != rz: out.append(f"turned {r0} to {rz:g}")
    return "; ".join(out) or "kept"


def B(bid, arch, district, x, n, rz, label, opts=None):
    return (bid, arch, district, x, n, rz, label, opts, status(bid, arch, x, n, rz))


keep = lambda bid, **kw: B(bid, kw.get("arch", BASE[bid][1]), BASE[bid][2], kw.get("x", BASE[bid][3]), kw.get("n", BASE[bid][4]), kw.get("rz", BASE[bid][5]), kw.get("label", BASE[bid][6]), kw.get("opts", BASE[bid][7]))
ALT_D = [
    keep("B01", opts={"elev": 1.0}, label="Exchange Hall on the civic terrace"),
    keep("B02"), keep("B03"),
    keep("B04", arch="A11", label="Junction Tower House (money changer)"),
    keep("B05"), keep("B06"), keep("B07"), keep("B08"), keep("B09"),
    keep("B10", rz=84), keep("B11"), keep("B12", rz=96), keep("B13"), keep("B14", n=40.2),
    keep("B15", arch="A11", label="Terrace Tower House West (assay office, guild)"),
    keep("B16", arch="A11m", rz=0, label="Terrace Tower House East (chart maker)"),
    keep("B17", rz=18, x=36.5, n=67.5, label="Tea House, turned to the view"),
    keep("E01", rz=78), keep("E02"),
    B("E03", "A09", "D3 Pasar Awan", -26.5, 45, 90, "Merchants' Inn (Penginapan Saudagar)", S("Cup")),
    keep("E04"), keep("E05"),
    B("E06", "A04", "D3 Pasar Awan", 25.8, 46.9, -82, "Bazaar Perimeter Shop East (cloth seller)", S("Crate")),
    B("E07", "A04b", "D3 Pasar Awan", -24.8, 55.6, 98, "Bazaar Perimeter Shop North-West (potter's outlet)", S("Jar")),
]

# free stalls (kit, x, n, rz) and awning rows (kit, x, n, rz): the rows line the central market street, the cross-passage runs between them
STALLS = [("S%02d" % (i + 1),) + s for i, s in enumerate([("S03", -10.0, 40.6, 0), ("S05", 10.0, 40.6, 0), ("S01b", -13.0, 57.4, 0), ("S02g", 13.0, 57.4, 0)])]
ROWS = [("R01", "provisions", -5.8, 43.6, 90), ("R02", "provisions", -5.8, 54.4, 90), ("R03", "crafts", 5.8, 43.6, -90), ("R04", "crafts", 5.8, 54.4, -90)]

PAVE_D = [p for p in L13.PAVE_B if p[0] != "D4 Civic court"] + [
    ("D4 Civic terrace (+1.0 m)", -14, 14, 62, 74, BRICK, 1.0), ("Inn forecourt", -24, -22, 40, 52, COBBLE), ("Tea house deck apron", 32, 42, 62, 66, RED)]
YARDS_D = list(L13.YARDS_B)
RESERVED = list(L13.RESERVED)


def graph():
    N, E = dict(L13.NB), [e for e in L13.EB]
    for k in ("N25", "N26", "N21", "N22"):
        N.pop(k)
    E = [e for e in E if not ({"N25", "N26", "N21", "N22"} & set(e[:2]))]
    N["N06"] = (0, 59.4, "Foot of the terrace stairs"); N["N07"] = (0, 67, "Civic terrace centre (+1.0 m)"); N["N08"] = (0, 75, "Exchange Hall podium, top of stairs (+2.0 m)")
    N["N38"] = (-19.2, 41, "Market west side lane, south"); N["N23"] = (-19.2, 58.6, "Bazaar north-west"); N["N39"] = (19.2, 41, "Market east side lane, south")
    N["N24"] = (19.2, 58.6, "Bazaar north-east (tea lane entrance)"); N["N17"] = (37.6, 62.6, "Tea house veranda")
    N["N21"] = (-9.5, 68, "Terrace west (benches)"); N["N22"] = (9.5, 68, "Terrace east (benches)")
    E += [("N23", "N06", "secondary"), ("N24", "N06", "secondary"), ("N07", "N21", "secondary"), ("N07", "N22", "secondary")]
    return N, E


ND, ED = graph()


def lines():
    out = [l for l in L13.lines(16) if not l[0].startswith("Civic")]
    return out + [("Civic terrace, west edge", (-14, 62), (-14, 74), (-1, 0), 4), ("Civic terrace, east edge", (14, 62), (14, 74), (1, 0), 4)]


# ---------------------------------------------------------------- alternative E: southern quarter swung about the junction
PIVOT, THETA = (0.0, 18.0), -14.0          # clockwise: the east side (warehouse, service court) is the outside of the bend


def swing(x, n, deg=THETA):
    a = math.radians(deg); dx, dn = x - PIVOT[0], n - PIVOT[1]
    return (round(PIVOT[0] + dx * math.cos(a) - dn * math.sin(a), 2), round(PIVOT[1] + dx * math.sin(a) + dn * math.cos(a), 2))


SOUTH = {"B04", "B07", "B13", "E01", "E02"}          # buildings that swing with the southern quarter; B10 is dropped (no room inside the bend)
ALT_E = []
for b in ALT_D:
    if b[0] == "B10":
        continue
    if b[0] in SOUTH:
        x, n = swing(b[3], b[4]); ALT_E.append(B(b[0], b[1], b[2], x, n, b[5] + THETA, b[6] + " (swung)", b[7]))
    else:
        ALT_E.append(b)
SOUTH_PAVE = {"D1 Arrival court", "D1 Gate forecourt", "South cross lane W", "South cross lane E", "Warehouse lane widening behind the jettied house", "Artisan lane widening behind the corner house"}
NE = {k: ((*swing(v[0], v[1]), v[2]) if v[1] < 18 else v) for k, v in ND.items()}


def frame(b):
    """Centre, rotation and half sizes of a building's nominal footprint, including a front veranda."""
    _, aid, _, x, n, rz = b[:6]
    W, D = FOOT[aid]
    if aid == "A01":
        return x, n, rz, 14, 9, 0, -3          # podium and stairs: 28 x 18 centred 3 m in front of the hall centre
    f = FRONT_EXTRA.get(aid, 0)
    return x, n, rz, W / 2, (D + f) / 2, 0, -f / 2


def corners(b):
    x, n, rz, hw, hd, ox, oy = frame(b)
    a = math.radians(rz); c, s = math.cos(a), math.sin(a)
    return [(x + (ox + px) * c - (oy + py) * s, n + (ox + px) * s + (oy + py) * c) for px, py in ((-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd))]


def inside(b, qx, qn, grow=0.0):
    x, n, rz, hw, hd, ox, oy = frame(b)
    a = math.radians(-rz); c, s = math.cos(a), math.sin(a)
    lx, ly = (qx - x) * c - (qn - n) * s - ox, (qx - x) * s + (qn - n) * c - oy
    return abs(lx) <= hw + grow and abs(ly) <= hd + grow


def bbox(b):
    cs = corners(b)
    return (min(p[0] for p in cs), max(p[0] for p in cs), min(p[1] for p in cs), max(p[1] for p in cs))


def overlap(pa, pb):
    """Separating-axis test for two convex polygons (lists of (x, n))."""
    for poly in (pa, pb):
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            ax, ay = y2 - y1, x1 - x2
            a = [ax * px + ay * py for px, py in pa]; c = [ax * px + ay * py for px, py in pb]
            if max(a) <= min(c) + 1e-9 or max(c) <= min(a) + 1e-9:
                return False
    return True


def front_normals(b):
    rz, aid = b[5], b[1]
    a = math.radians(rz)
    out = [(math.sin(a), -math.cos(a))]
    if aid in ("A05",):
        out.append((math.cos(a), math.sin(a)))
    if aid == "A02":
        out = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    return out


def door_point(b, out=1.5):
    x, n, rz, hw, hd, ox, oy = frame(b)
    d = (12 if b[1] == "A01" else hd - oy) + out
    a = math.radians(rz)
    return (round(x + d * math.sin(a), 2), round(n - d * math.cos(a), 2))


def enclosure(buildings, line, step=0.5):
    name, (xa, na), (xb, nb), (ux, un), depth = line
    Lg = math.hypot(xb - xa, nb - na); k = max(1, int(Lg / step)); wall = act = 0
    for i in range(k):
        t = (i + 0.5) / k; px, pn = xa + (xb - xa) * t, na + (nb - na) * t
        hit = hita = False
        for j in range(int(depth / 0.25) + 1):
            qx, qn = px + ux * j * 0.25, pn + un * j * 0.25
            for b in buildings:
                if inside(b, qx, qn):
                    hit = True
                    if any(fx * -ux + fn * -un > 0.85 for fx, fn in front_normals(b)):
                        hita = True
            if hit:
                break
        wall += hit; act += hita
    return round(Lg, 1), round(100 * wall / k), round(100 * act / k)


def swing_line(l):
    name, a, b, u, depth = l
    if max(a[1], b[1]) > 18.01 and not name.startswith(("Arrival",)):
        return l
    ang = math.radians(THETA); c, s = math.cos(ang), math.sin(ang)
    return (name, swing(*a), swing(*b), (u[0] * c - u[1] * s, u[0] * s + u[1] * c), depth)


ALTS = {
    "B": {"title": "P1.3 selected (B)", "buildings": [tuple(b) for b in L13.ALT_B], "paving": L13.PAVE_B, "yards": L13.YARDS_B, "nodes": L13.NB, "edges": L13.EB, "lines": L13.lines(16), "stalls": L13.STALLS, "rows": [], "swing": False, "foot": L13.FOOT},
    "D": {"title": "D - Terraced Citadel", "buildings": ALT_D, "paving": PAVE_D, "yards": YARDS_D, "nodes": ND, "edges": ED, "lines": lines(), "stalls": STALLS, "rows": ROWS, "swing": False},
    "E": {"title": "E - Crooked Spine", "buildings": ALT_E, "paving": PAVE_D, "yards": YARDS_D, "nodes": NE, "edges": [e for e in ED], "lines": [swing_line(l) for l in lines()], "stalls": STALLS, "rows": ROWS, "swing": True},
}
