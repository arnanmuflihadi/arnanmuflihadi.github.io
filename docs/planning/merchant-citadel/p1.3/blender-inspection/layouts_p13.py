#!/usr/bin/env python3
"""Merchant Citadel P1.3 - three measured layout alternatives (plain Python, single source of truth).

Plan coordinates: x = east, n = north (metres), origin = centre of the arrival court; project (x, y, z) = (x, elevation, -n).
rz: 0 = front faces south, 90 = east, -90 = west, 180 = north.  Footprints come from the archetype data (2 m module grid).

  A  Refined existing layout   - P1.2 street network (outer lanes), selected buildings relocated, one infill
  B  Compact Merchant Citadel  - lanes moved in behind the street rows, mid-street cross street, five infill buildings
  C  Expanded Trading Quarter  - B plus two more bazaar-edge buildings

Each alternative: buildings (id, archetype, district, x, n, rz, label, opts, status), paving, yards, nodes, edges,
frontage lines (for the enclosure metrics) and stalls.  status = kept | moved | rotated | re-typed | new.
"""
COBBLE, BRICK, RED = "MV-Floor_UnevenBrick", "MV-Floor_Brick", "MV-Floor_RedBrick"
S = lambda glyph, field="wood": {"sign": f"CUS-Sign_{glyph}_{field}"}
FOOT = {"A01": (28, 16), "A02": (8, 12), "A03": (6, 8), "A03b": (8, 6), "A04": (4, 6), "A04b": (6, 4), "A05": (8, 8), "A06": (6, 6), "A07": (8, 14), "A08": (6, 6), "A03c": (8, 4)}
EAVE = {"A01": 7.0, "A02": 3.0, "A03": 6.0, "A03b": 6.0, "A04": 3.0, "A04b": 3.0, "A05": 6.0, "A06": 3.0, "A07": 6.0, "A08": 6.0, "A03c": 6.0}   # wall-top height (m)
P12 = {  # approved-baseline positions (P1.2 = P1.1): id -> (archetype, x, n, rz)
    "B01": ("A01", 0, 84, 0), "B02": ("A02", -13, 50, 0), "B03": ("A02", 13, 50, 0), "B04": ("A05", -9, 14, 0), "B05": ("A03b", -8, 25, 90), "B06": ("A04", -8, 33.5, 90),
    "B07": ("A03", 9, 13, -90), "B08": ("A04b", 7, 22.5, -90), "B09": ("A03", 9, 32, -90), "B10": ("A06", -25.5, 13, 90), "B11": ("A04b", -24.5, 22.5, 90), "B12": ("A06", -25.5, 31.5, 90),
    "B13": ("A07", 29.5, 18, -90), "B14": ("A04", 25.5, 29, -90), "B15": ("A05", -22, 67, 90), "B16": ("A03", 22, 67, -90), "B17": ("A08", 40, 58, 0)}


def status(bid, arch, x, n, rz):
    if bid not in P12:
        return "new"
    a0, x0, n0, r0 = P12[bid]
    out = []
    if a0 != arch: out.append(f"re-typed {a0} to {arch}")
    if (x0, n0) != (x, n): out.append(f"moved from ({x0}, {-n0}) by {((x - x0) ** 2 + (n - n0) ** 2) ** 0.5:.1f} m")
    if r0 != rz: out.append(f"rotated {r0} to {rz}")
    return "; ".join(out) or "kept"


def B(bid, arch, district, x, n, rz, label, opts=None):
    return (bid, arch, district, x, n, rz, label, opts, status(bid, arch, x, n, rz))


CORE = [  # the same in all three alternatives
    B("B01", "A01", "D5 Balai Niaga Awan", 0, 84, 0, "Exchange Hall"),
    B("B02", "A02", "D3 Pasar Awan", -13, 50, 0, "Market Hall West (provisions)", {"kit": "provisions", "sign": "FP-Banner_1@blue"}),
    B("B03", "A02", "D3 Pasar Awan", 13, 50, 0, "Market Hall East (crafts and general trade)", {"kit": "crafts", "sign": "FP-Banner_1@burgundy"}),
    # merchant street: gaps aligned at n 18..22 so a cross street can pass; B04 turned to face the street and the cross street
    B("B04", "A05", "D2 Koridor Niaga", -9, 14, 90, "Junction Corner House (money changer)", S("Coin")),
    B("B05", "A03b", "D2 Koridor Niaga", -8, 26, 90, "Shophouse W1, eaves to street (baker)", S("Loaf")),
    B("B06", "A04", "D2 Koridor Niaga", -8, 34.4, 90, "Compact Shop W2 (dry goods)", S("Crate")),
    B("B07", "A03", "D2 Koridor Niaga", 9, 13, -90, "Jettied Shophouse E1 (map and book seller)", S("Scroll")),
    B("B08", "A04b", "D2 Koridor Niaga", 7, 25, -90, "Compact Shop E2, eaves to street (potter)", S("Jar")),
    B("B09", "A03", "D2 Koridor Niaga", 9, 33.6, -90, "Jettied Shophouse E3 (provisioner)", S("Loaf")),
    B("B15", "A05", "D4 Pelataran Bursa", -18, 67, 0, "Court Corner House West (assay office, guild)", S("Coin", "burgundy")),
]
E01 = B("E01", "A04b", "D1 Gerbang Niaga", -12, -1, 90, "South Gateway Shop (traveller's outfitter)", S("Crate"))
E02 = B("E02", "A03c", "D1 Gerbang Niaga", 12, -2, -90, "Arrival Corner Merchant House (carrier's office)", S("Scroll"))
E03 = B("E03", "A03b", "D3 Pasar Awan", -25.5, 46, 90, "Bazaar Perimeter Shop West (grain and oil merchant)", S("Jar"))
E04 = B("E04", "A05", "D7 Jalur Gudang", 22.5, 28, -90, "Merchant Counting House (guild)", S("Coin", "burgundy"))
E05 = B("E05", "A04b", "D8 Tea Lookout", 25.5, 53.5, 180, "Tea Route Merchant House (tea and spice seller)", S("Cup"))
E06 = B("E06", "A04", "D3 Pasar Awan", 25.5, 47.3, -90, "Bazaar Perimeter Shop East (cloth seller)", S("Crate"))
E07 = B("E07", "A04b", "D3 Pasar Awan", -24.5, 56, 90, "Bazaar Perimeter Shop North-West (potter's outlet)", S("Jar"))
TEA = B("B17", "A08", "D8 Tea Lookout", 36, 67, 0, "Tea House", S("Cup"))
REG = B("B14", "A04", "D3 Pasar Awan", 25.5, 41, -90, "Registry Office (guild), on the bazaar edge", S("Scroll", "burgundy"))

ALT_A = CORE + [
    B("B10", "A06", "D6 Lorong Lentera", -25.5, 13, 90, "Workshop South (smith)", S("Hammer")),
    B("B11", "A04b", "D6 Lorong Lentera", -24.5, 22.5, 90, "Lane Shop, eaves to lane (potter's yard)", S("Jar")),
    B("B12", "A06", "D6 Lorong Lentera", -25.5, 31.5, 90, "Workshop North (joiner)", S("Hammer")),
    B("B13", "A07", "D7 Jalur Gudang", 29.5, 18, -90, "Guild Warehouse"),
    REG, B("B16", "A03", "D4 Pelataran Bursa", 18, 67, -90, "Court Shophouse East (chart maker)", S("Scroll")), TEA, E01]
INNER = [  # lanes moved in behind the street rows (B and C)
    B("B10", "A06", "D6 Lorong Lentera", -21.5, 11, 90, "Workshop South (smith)", S("Hammer")),
    B("B11", "A04b", "D6 Lorong Lentera", -20.5, 20, 90, "Lane Shop closing the cross street (potter's yard)", S("Jar")),
    B("B12", "A06", "D6 Lorong Lentera", -21.5, 29, 90, "Workshop North (joiner)", S("Hammer")),
    B("B13", "A07", "D7 Jalur Gudang", 25.5, 12, -90, "Guild Warehouse"),
    REG, B("B16", "A05", "D4 Pelataran Bursa", 18, 67, -90, "Court Corner House East (chart maker)", S("Scroll")), TEA]
ALT_B = CORE + INNER + [E01, E02, E03, E04, E05]
ALT_C = ALT_B + [E06, E07]

STALLS = [("S%02d" % (i + 1),) + s for i, s in enumerate([
    ("S01b", -5.0, 40.5, 90), ("S03", -5.0, 44.5, 90), ("S04", -5.0, 53.5, 90), ("S01c", -5.0, 57.5, 90),
    ("S01g", 5.0, 40.5, -90), ("S02c", 5.0, 44.5, -90), ("S05", 5.0, 53.5, -90), ("S01g", 5.0, 57.5, -90),
    ("S03", -10.0, 40.6, 0), ("S05", 10.0, 40.6, 0), ("S01b", -12.0, 58.6, 0), ("S02g", 12.0, 58.6, 0)])]


def paving(xl):
    """xl = lane centre distance from the axis: 20 (outer lanes, alternative A) or 16 (inner lanes, B and C)."""
    a, b = xl - 2, xl + 2
    return [
        ("D1 Arrival court", -10, 10, -8, 8, COBBLE), ("D1 Gate forecourt", -14, 14, 6, 10, COBBLE), ("D2 Merchant street", -6, 6, 8, 36, COBBLE),
        ("South cross lane W", -b, -10, 2, 6, COBBLE), ("South cross lane E", 10, b, 2, 6, COBBLE),
        ("D6 Artisan lane (red brick)", -b, -a, 6, 36, RED), ("D7 Warehouse lane", a, b, 6, 36, COBBLE),
        ("Cross street W (Simpang Timbangan)", -a, -6, 18, 22, COBBLE), ("Cross street E", 6, a, 18, 22, COBBLE),
        ("D3 Bazaar plaza", -22, 22, 36, 62, COBBLE), ("Market Hall West floor", -18, -8, 44, 56, BRICK), ("Market Hall East floor", 8, 18, 44, 56, BRICK),
        ("Hall-to-hall cross-passage", -8, 8, 48, 50, BRICK), ("Guild way (axis band)", -2, 2, 0, 62, BRICK),
        ("D4 Civic court", -14, 14, 62, 74, BRICK), ("D8 Tea lane", 22, 30, 56, 60, COBBLE), ("D8 Lookout terrace (red brick)", 30, 42, 52, 62, RED),
        ("Tea house veranda floor", 32, 40, 62, 64, RED)]


PAVE_B = paving(16) + [("D7 Service court (Pelataran Gudang)", 18, 32, 16, 24, COBBLE), ("D6 Artisan workyard", -24, -18, 32, 36, RED),
                       ("Junction pocket court (Simpang Timbangan, east)", 6, 14, 16, 18, COBBLE), ("Artisan lane widening behind the corner house", -14, -12, 6, 18, RED),
                       ("Warehouse lane widening behind the jettied house", 12, 14, 6, 16, COBBLE)]
PAVE_A = paving(20)
YARDS_B = [("West yards behind the street row", -14, -10, 22, 36), ("East service yard", 10, 14, 22, 30), ("Counting house yard", 18, 26, 32, 36)]
YARDS_A = [("West back courts", -18, -10, 10, 36), ("East back courts", 10, 18, 10, 36)]
RESERVED = [("Future transport reservation (no construction in P1-P3)", -10, 10, -24, -8)]


def graph(xl, service=True):
    N = {
        "N01": (0, 0, "Arrival court"), "N02": (0, 5.0, "Gateway centre lane"), "N03": (0, 20, "Simpang Timbangan (street junction)"),
        "N04": (0, 37.5, "Bazaar south entrance"), "N05": (0, 45.5, "Bazaar, south of the market cross"), "N29": (2.7, 49, "Cross-passage east of the cross"),
        "N30": (-2.7, 49, "Cross-passage west of the cross"), "N27": (0, 52.5, "Bazaar, north of the market cross"), "N06": (0, 62, "Court south"),
        "N07": (0, 67, "Civic court centre"), "N08": (0, 75, "Exchange Hall podium, top of stairs (+1.0 m)"),
        "N35": (-9, 4, "Arrival court west exit"), "N09": (-xl, 4, "Artisan lane south"), "N10": (-xl, 20, "Artisan lane at the cross street"), "N11": (-xl, 38.5, "Bazaar south-west"),
        "N36": (9, 4, "Arrival court east exit"), "N12": (xl, 4, "Warehouse lane south"), "N13": (xl, 20, "Warehouse lane at the cross street"), "N14": (xl, 38.5, "Bazaar south-east"),
        "N18": (-12, 42.5, "Market Hall West south arch"), "N31": (-12, 49, "Market Hall West interior"), "N19": (12, 42.5, "Market Hall East south arch"), "N32": (12, 49, "Market Hall East interior"),
        "N38": (-19.75, 41, "Market west side lane, south"), "N23": (-19.75, 58.5, "Bazaar north-west"), "N39": (19.75, 41, "Market east side lane, south"),
        "N24": (19.75, 58.5, "Bazaar north-east (tea lane entrance)"),
        "N25": (-11, 61.3, "Court south-west entrance"), "N26": (11, 61.3, "Court south-east entrance"), "N21": (-12, 67, "Court west (corner house door)"), "N22": (12, 67, "Court east (corner house door)"),
        "N41": (26, 58, "Tea lane"), "N16": (36, 57, "Lookout terrace"), "N17": (36, 62.3, "Tea house veranda"), "N20": (0, -16, "Future transport reservation")}
    E = [("N20", "N01", "reserved link"), ("N01", "N02", "primary"), ("N02", "N03", "primary"), ("N03", "N04", "primary"), ("N04", "N05", "primary"),
         ("N05", "N29", "primary"), ("N29", "N27", "primary"), ("N05", "N30", "primary"), ("N30", "N27", "primary"), ("N27", "N06", "primary"), ("N06", "N07", "primary"), ("N07", "N08", "primary, stairs"),
         ("N01", "N35", "secondary"), ("N35", "N09", "secondary"), ("N09", "N10", "secondary"), ("N10", "N11", "secondary"), ("N11", "N04", "secondary"), ("N10", "N03", "secondary"),
         ("N01", "N36", "service"), ("N36", "N12", "service"), ("N12", "N13", "service"), ("N13", "N14", "service"), ("N14", "N04", "service"), ("N03", "N13", "service"),
         ("N11", "N18", "market"), ("N18", "N31", "market"), ("N31", "N30", "market"), ("N14", "N19", "market"), ("N19", "N32", "market"), ("N32", "N29", "market"),
         ("N11", "N38", "secondary"), ("N38", "N23", "secondary"), ("N23", "N25", "secondary"), ("N25", "N21", "secondary"), ("N25", "N06", "secondary"), ("N21", "N07", "secondary"),
         ("N14", "N39", "secondary"), ("N39", "N24", "secondary"), ("N24", "N26", "secondary"), ("N26", "N22", "secondary"), ("N26", "N06", "secondary"), ("N22", "N07", "secondary"),
         ("N24", "N41", "scenic"), ("N41", "N16", "scenic"), ("N16", "N17", "scenic")]
    if service:
        N["N33"] = (25, 20, "Service court (Pelataran Gudang)"); N["N40"] = (-21, 34, "Artisan workyard")
        E += [("N13", "N33", "service"), ("N11", "N40", "secondary")]
    return N, E


def lines(xl, court=14):
    """Frontage lines for the enclosure metrics: name, (x0, n0), (x1, n1), outward normal, search depth (m)."""
    a, b = xl - 2, xl + 2
    return [("Merchant street, west side", (-4, 10), (-4, 36), (-1, 0), 3), ("Merchant street, east side", (4, 10), (4, 36), (1, 0), 3),
            ("Artisan lane, outer side", (-b, 6), (-b, 36), (-1, 0), 3), ("Artisan lane, inner side", (-a, 6), (-a, 36), (1, 0), 3.5),
            ("Warehouse lane, outer side", (b, 6), (b, 36), (1, 0), 3), ("Warehouse lane, inner side", (a, 6), (a, 36), (-1, 0), 3.5),
            ("Bazaar, west edge", (-22, 36), (-22, 62), (-1, 0), 4), ("Bazaar, east edge", (22, 36), (22, 62), (1, 0), 4),
            ("Bazaar, south edge", (-22, 36), (22, 36), (0, -1), 4), ("Bazaar, north edge", (-22, 62), (22, 62), (0, 1), 4),
            ("Arrival court, west edge", (-10, -8), (-10, 8), (-1, 0), 4), ("Arrival court, east edge", (10, -8), (10, 8), (1, 0), 4),
            ("Civic court, west edge", (-court, 62), (-court, 74), (-1, 0), 4), ("Civic court, east edge", (court, 62), (court, 74), (1, 0), 4)]


NB, EB = graph(16)
NA, EA = graph(20, service=False)
ALTS = {
    "A": {"title": "A - Refined existing layout", "buildings": ALT_A, "paving": PAVE_A, "yards": YARDS_A, "nodes": NA, "edges": EA, "lines": lines(20), "stalls": STALLS},
    "B": {"title": "B - Compact Merchant Citadel", "buildings": ALT_B, "paving": PAVE_B, "yards": YARDS_B, "nodes": NB, "edges": EB, "lines": lines(16), "stalls": STALLS},
    "C": {"title": "C - Expanded Trading Quarter", "buildings": ALT_C, "paving": PAVE_B, "yards": YARDS_B, "nodes": NB, "edges": EB, "lines": lines(16), "stalls": STALLS},
}
P12_LINES = lines(20, court=18)


def rect_of(b):
    """Nominal footprint rectangle (x0, x1, n0, n1): wall lines, plus podium and stairs (A01) or veranda (A08)."""
    _, aid, _, x, n, rz = b[:6]
    W, D = FOOT[aid]
    if aid == "A01":
        return (x - 14, x + 14, n - 12, n + 6)
    f = 2 if aid == "A08" else 0
    lo = {0: (-W / 2, W / 2, -D / 2 - f, D / 2), 180: (-W / 2, W / 2, -D / 2, D / 2 + f), 90: (-D / 2, D / 2 + f, -W / 2, W / 2), -90: (-D / 2 - f, D / 2, -W / 2, W / 2)}[rz]
    return (x + lo[0], x + lo[1], n + lo[2], n + lo[3])


def fronts(b):
    """Outward unit normals of the building's active (door) sides. A05 has two fronts: its front and its right side."""
    rz = b[5]
    f = {0: (0, -1), 90: (1, 0), -90: (-1, 0), 180: (0, 1)}[rz]
    out = [f]
    if b[1] == "A05":
        out.append({0: (1, 0), 90: (0, 1), -90: (0, -1), 180: (-1, 0)}[rz])
    if b[1] == "A02":
        out = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    return out


def enclosure(buildings, line, step=0.5):
    """Share of a frontage line that has (a) any building wall, (b) an active front, within the search depth."""
    name, (xa, na), (xb, nb), (ux, un), depth = line
    L = ((xb - xa) ** 2 + (nb - na) ** 2) ** 0.5
    k = max(1, int(L / step)); wall = act = 0
    rects = [(rect_of(b), fronts(b)) for b in buildings]
    for i in range(k):
        t = (i + 0.5) / k; px, pn = xa + (xb - xa) * t, na + (nb - na) * t
        hit = hita = False
        for j in range(int(depth / 0.25) + 1):
            qx, qn = px + ux * j * 0.25, pn + un * j * 0.25
            for r, fr in rects:
                if r[0] <= qx <= r[1] and r[2] <= qn <= r[3]:
                    hit = True
                    if any(fx * -ux + fn * -un > 0.9 for fx, fn in fr):
                        hita = True
            if hit:
                break
        wall += hit; act += hita
    return round(L, 1), round(100 * wall / k), round(100 * act / k)
