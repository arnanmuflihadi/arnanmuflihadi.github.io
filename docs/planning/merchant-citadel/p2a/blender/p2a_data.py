#!/usr/bin/env python3
"""Merchant Citadel P2-A: slice definition, placements and collision proxies (plain Python, no Blender).

Reads the P1.4 design data (town_data / layouts_p14 in ../../p1.4/blender-inspection) and writes
merchant-citadel-p2a/data/scene.json for the Blender exporter and for the Three.js preview.

Conventions: plan coordinates x = east, n = north; Three.js (x, y, z) = (x, elevation, -n).
Obstacle format is the one the existing first-island controller and camera consume:
  {x, z, w, d, h, [minY], [cameraOnly], [oriented:{rotation,w,d}]}   h = top y (absolute), minY = bottom y (default -0.2)
plus a `group` tag used only by the preview's camera-collision experiments.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P14 = os.path.join(HERE, "..", "..", "p1.4", "blender-inspection")
sys.path.insert(0, P14)
import town_data as T            # noqa: E402
from p2a_hall import hall_modules, HALL_NODES   # noqa: E402
from p2a_bazaar import load_dims, hall_archetype, HALL_VARIANTS, NODE_FOR_KIT, NODE_FOR_BLD   # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "..", "..", "..", "merchant-citadel-p2a", "data", "scene.json")
INSPECT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "..", "..", "..", "..", ".asset-inspection", "merchant-citadel-p1")
DIMS = load_dims(INSPECT)

SLICE_BUILDINGS = ["B04", "B05", "B06", "B07", "B08", "B09", "E03", "B17", "B01", "B02", "B03", "B14", "E06", "E07",
                   "B10", "B11", "B12", "E01", "E02", "B13", "E04", "E05", "B15", "B16"]      # batch 5: the Civic Terrace tower houses; all 24 buildings of P1.4 now stand;      # batch 4: Eastern Trade Quarter (warehouse B13, counting house E04) and the tea route (E05); batch 3: Lorong Lentera (artisan lane, D6) and the south gateway (D1)   # street segment, junction corner, inn (balcony), tea house (N16-N17), Exchange Hall (batch 1)
# P2-A closeout corrections, each measured in 01-test-results / p2a-closeout: name -> (dx, dn) metres.
#  B04: the A11 corner house projects a turret to n 19, which narrowed the 4 m cross street to 3.0 m between walls and to 1.34 m between roof eaves,
#       and put the street centre at n 20.5 instead of the junction node N03 (n 20). Moving the house 1.2 m south restores a 4.2 m street centred on n 19.9.
ADJUST = {"B04": (0.0, -1.2)}
N17_NEW = (36.16, 62.24, "Tea house veranda (centre of the gap between the first two porch posts)")
RECTS = [(-16, 16, -8, 36), (-34, 34, 34, 62), (-16, 16, 60, 96), (18, 48, 44, 72), (-34, -16, 0, 36),
         (16, 40, 0, 36), (30, 34, 36, 52), (-26, -14, 56, 76), (14, 26, 56, 76)]            # batch 5: the tower houses' plots            # batch 4: warehouse lane east half, service court, tea porters' path   # street + arrival strip, bazaar, terrace and hall podium, tea lane and lookout
inreg = lambda x, n: any(a <= x <= b and c <= n <= d for a, b, c, d in RECTS)
ROOF = T.ROOF if hasattr(T, "ROOF") else {4: (3.73, 0.52, 2.757), 6: (4.89, 0.78, 4.125), 8: (6.0, 0.78, 4.976)}
ROOF = dict(ROOF); ROOF.setdefault(2, (1.9, 0.3, 1.5))
FOOT = {   # small prop footprints (w, d, top y) measured on the models or taken from 08 of P1.4
    "FP-Barrel": (0.75, 0.75, 0.95), "MV-Prop_Crate": (0.85, 0.85, 0.85), "FP-Crate_Wooden": (0.95, 0.95, 0.95), "FP-Bag": (0.6, 0.6, 0.7), "FP-Bench": (1.7, 0.55, 0.6),
    "SY-keg01": (0.75, 0.8, 0.8), "SY-keg02": (0.9, 0.9, 0.9), "SY-menu-stand01": (0.6, 0.35, 1.6), "SY-table01": (1.1, 1.1, 0.82), "SY-table02": (1.6, 1.6, 0.82),
    "FP-Bucket_Wooden_1": (0.5, 0.5, 0.45), "FP-Workbench": (1.6, 0.8, 0.95), "FP-Anvil_Log": (0.7, 0.7, 0.9), "MV-Prop_Wagon": (2.6, 1.4, 1.2), "AV-mdvl_village_well_01": (1.7, 1.45, 2.2),
    "MV-Prop_WoodenFence_Single": (2.0, 0.25, 1.1), "SY-stool": (0.4, 0.4, 0.8), "SY-chair01": (0.6, 0.55, 1.2),
}


def district_at(x, n):
    """District of a world position for merging and culling: D5 civic court and hall, D8 tea lookout, D2 market street (south), D3 the bazaar."""
    if n >= 60 and abs(x) <= 20:
        return "D5"
    if x <= -14 and n < 36:
        return "D6"
    if n < 8 and x < 14:
        return "D1"
    if x >= 14 and n < 37:
        return "D7"                                                  # batch 4: Jalur Gudang, the warehouse lane, the service court and the counting house
    if x >= 22 and n >= 52:
        return "D8"                                                  # batch 4: E05 (x 21.5-29.5, n 51.5-55.5) belongs to the tea route
    if x >= 26 and n >= 48:
        return "D8"
    return "D2" if n < 34 else "D3"


def rot90(lx, ly, rz):
    """Rotate a local plan vector by rz degrees (multiple of 90 exactly, otherwise a float rotation)."""
    a = math.radians(rz); c, s = round(math.cos(a), 10), round(math.sin(a), 10)
    return lx * c - ly * s, lx * s + ly * c


class Obs:
    def __init__(self, ox, on, rz, elev=0.0):
        self.ox, self.on, self.rz, self.elev, self.out = ox, on, rz, elev, []

    def box(self, cx, cy, w, d, y0, y1, group, cam=False, extra_rz=0.0):
        """Local box centre (cx, cy), size w along local x and d along local y, absolute-in-local y range y0..y1."""
        rz = self.rz + extra_rz
        wx, wn = rot90(cx, cy, self.rz)
        X, N = self.ox + wx, self.on + wn
        o = {"x": round(X, 3), "z": round(-N, 3), "w": round(w, 3), "d": round(d, 3), "h": round(self.elev + y1, 3), "group": group}
        if y0 is not None and (cam or y0 > 0.05):
            o["minY"] = round(self.elev + y0, 3)
        if cam:
            o["cameraOnly"] = True
        r = rz % 360
        if abs(r % 90) < 1e-6:
            if round(r / 90) % 2 == 1:
                o["w"], o["d"] = o["d"], o["w"]
        else:
            a = math.radians(rz)
            c, s = abs(math.cos(a)), abs(math.sin(a))
            o["oriented"] = {"rotation": round(math.radians(rz), 6), "w": round(w, 3), "d": round(d, 3)}
            o["w"], o["d"] = round(w * c + d * s, 3), round(w * s + d * c, 3)          # axis-aligned bound, used by the camera
        self.out.append(o)


ROOF_STEPS = int(os.environ.get("P2D_ROOF_STEPS", "6"))      # batch 4: 6 bands (P2-A to batch 3: 3). Each band is as wide as its lower edge, so the proxy never lies inside the real roof; 3 bands overshot it by up to a third of the rise (1.2 m on an 8 m span)


def roof_bands(ob, span, length, ridge, top, ox=0.0, oy=0.0, shift=(0.0, 0.0), tower=False):
    """Camera-only stepped boxes approximating a prefab roof (ROOF_STEPS bands, each as wide as the band's lower edge)."""
    if tower:
        rise, drop, hw, hl = 6.8, 0.5, 2.8, 2.8
    else:
        rise, drop, hw = ROOF[span]; hl = length / 2 + 0.45
    base = top - drop
    for k in range(ROOF_STEPS):
        y0, y1 = base + (rise + drop) * k / ROOF_STEPS, base + (rise + drop) * (k + 1) / ROOF_STEPS
        half = hw * (1 - k / ROOF_STEPS)
        w, d = (2 * hl, 2 * half) if ridge == "x" else (2 * half, 2 * hl)
        if tower:
            w = d = 2 * half
        ob.box(ox + shift[0], oy + shift[1], w, d, y0, y1, "roof", cam=True)


def roof_shell(ob, span, length, top, cx, cy, steps=6, thick=0.8):
    """Open arcade roof (ridge along local y): two stepped slopes of thin camera-only boxes with the space below left free, instead of the solid slab of roof_bands.
    P2-B finding: the slab put the camera 0.94 m behind the player everywhere inside the covered market halls."""
    rise, drop, hw = ROOF[span]; hl = length / 2 + 0.45
    ridge_ub, eave_ub = top + rise - thick, top - drop                      # roof underside at the ridge and at the eave edge
    ub = lambda u: ridge_ub - (ridge_ub - eave_ub) * u / hw
    for sx in (-1, 1):
        for i in range(steps - 1):                                            # the outermost step (the thin 0.83 m eave edge, 2.2 m above the floor) is left out: it clipped the camera 1 m behind a player standing under the eave
            u0, u1 = hw * i / steps, hw * (i + 1) / steps
            y0, y1 = ub(u1), ub(u0) + thick
            ob.box(cx + sx * (u0 + u1) / 2, cy, (u1 - u0) + 0.05, 2 * hl, y0, y1, "roof", cam=True)


def proxies_for(arch_id, A, ob, elev_parts=0.0, kit=None):
    """Collision proxies for one archetype placed through Obs `ob`. Local frame: front at -y, origin = footprint centre on the ground."""
    for p in A["parts"]:
        W, D, fl = p["W"], p["D"], p["floors"]; ox, oy, oz = p.get("offset", (0, 0, 0)); top = oz + fl * 3
        if p.get("core", True):
            ob.box(ox, oy, W, D, oz + p.get("floor_from", 0) * 3, top, "wall")
        else:
            for sx in (-1, 1):
                for sy in (-1, 1):
                    ob.box(ox + sx * (W / 2 - 0.15), oy + sy * (D / 2 - 0.15), 0.4, 0.4, 0, top, "post")
        if p.get("jetty") is not None:
            ob.box(ox, oy - D / 2 - 0.56, W, 1.123, oz + 3.0, top, "overhang", cam=True)
        if p.get("roof"):
            span, length = (int(v) for v in p["roof"].split("x")); sh = p.get("roof_shift", (0, 0))
            if p.get("jetty") is not None:
                length += 2; sh = (sh[0], sh[1] - 1)
            if A.get("open_roof") and p.get("ridge", "y") == "y":
                roof_shell(ob, span, length, top, ox + sh[0], oy + sh[1])
            else:
                roof_bands(ob, span, length, p.get("ridge", "y"), top, ox, oy, sh)
        if p.get("tower_roof"):
            roof_bands(ob, 0, 0, "y", top, ox, oy, tower=True)
    for (x0, y0, x1, y1) in A.get("solid_runs", []):                       # closed bays added by a variant (hall-local plan coordinates, 3 m high, 0.3 m thick)
        ob.box((x0 + x1) / 2, (y0 + y1) / 2, max(abs(x1 - x0), 0.3), max(abs(y1 - y0), 0.3), 0, 3.0, "wall")
    for e in A.get("extras", []):
        if e.get("kit") and kit and e["kit"] != kit:
            continue
        a, (px, py, pz), erz, sc = e["asset"], e["pos"], e.get("rz", 0), e.get("scale", 1.0)
        if e.get("solid"):                                                 # an assembled solid (kiln) built from wall modules that carry no proxy of their own
            sw, sd, sh, scx, scy = e["solid"]; ob.box(scx, scy, sw, sd, 0, sh, "wall")
        s = sc if not isinstance(sc, list) else sc[0]
        if a.startswith("CUS-Sign"):
            cx, cy = rot90(0, -0.61 * s, erz)
            ob.box(px + cx, py + cy, 0.12, 0.5 * s, pz - 0.56 * s, pz - 0.16 * s, "sign", cam=True, extra_rz=erz)
        elif a.startswith("CUS-Awning"):
            cx, cy = rot90(0, -0.75, erz)
            ob.box(px + cx, py + cy, 2.0, 1.5, pz - 0.89, pz, "cloth", cam=True, extra_rz=erz)
        elif a == "MV-Floor_WoodDark":
            ob.box(px, py, 2.0, 2.0, pz - 0.1, pz + 0.05, "balcony", cam=True)
        elif a.startswith("MV-Balcony_"):
            cx, cy = rot90(0, 0.5, erz)
            ob.box(px + cx, py + cy, 2.0, 0.25, pz, pz + 1.1, "balcony", cam=True, extra_rz=erz)
        elif a == "MV-Corner_Exterior_Wood":
            zs = sc[2] if isinstance(sc, list) else 1.0
            ob.box(px, py, 0.4, 0.4, 0, round(pz + 3.0 * zs, 3), "post")
        elif a in ("FP-Table_Large",):
            ob.box(px, py, 2.84, 1.1, 0, 0.82, "counter", extra_rz=erz)
        elif a.startswith("SY-counter_"):
            ob.box(px + 0.75, py - 0.05, 1.5, 0.9, 0, 1.15, "counter", extra_rz=erz)
        elif a in FOOT and a not in ("FP-Bench",):
            w, d, h = FOOT[a]; ob.box(px, py, w * s, d * s, pz, pz + h * s, "prop", extra_rz=erz)
        elif a in DIMS and pz < 0.3 and not a.startswith(("CUS-", "FP-Banner", "FP-Lantern", "MV-Roof", "MV-Wall", "MV-Floor", "MV-Stairs", "MV-Corner", "SN-")):
            d = DIMS[a]; w, dd, ymin, ymax = d["max"][0] - d["min"][0], d["max"][2] - d["min"][2], d["min"][1], d["max"][1]       # floor-standing merchandise: footprint measured on the real model
            if (w * s < 0.25 and dd * s < 0.25) or (ymax - ymin) * s < 0.12:       # tiny pieces and flat rugs do not block
                continue
            cx, cn = rot90(((d["min"][0] + d["max"][0]) / 2) * s, -((d["min"][2] + d["max"][2]) / 2) * s, erz)
            ob.box(px + cx, py + cn, w * s, dd * s, pz + ymin * s, pz + ymax * s, "prop", extra_rz=erz)


def measured_box(a, s):
    """Footprint (w, d, ymin, ymax, cx, cn) of a floor-standing asset measured on the real model, or None for flat or tiny pieces."""
    if a not in DIMS or a.startswith(("CUS-", "FP-Banner", "FP-Lantern", "MV-Roof", "MV-Wall", "MV-Floor", "MV-Stairs", "MV-Corner", "SN-", "SY-herb")):
        return None
    d = DIMS[a]; w, dd, ymin, ymax = d["max"][0] - d["min"][0], d["max"][2] - d["min"][2], d["min"][1], d["max"][1]
    if (w * s < 0.25 and dd * s < 0.25) or (ymax - ymin) * s < 0.12:
        return None
    return w * s, dd * s, ymin * s, ymax * s, ((d["min"][0] + d["max"][0]) / 2) * s, -((d["min"][2] + d["max"][2]) / 2) * s


# batch 4: stand-in 'sign' choices per building (the P1.4 schedule gives E05 the cup, the tea house's own pictogram; the tea merchant gets a leaf)
SIGN_OVERRIDE = {"E05": "CUS-Sign_Leaf_wood", "B16": "CUS-Sign_Compass_wood"}
# batch 4: additional dressing for the Eastern Trade Quarter, as [asset, x, n, z, rz, scale] in plan coordinates (same schema as T.DRESSING)
EAST_DRESS = (
    [["MV-Prop_WoodenFence_Single", 35.0, float(nn), 0, 90, 1] for nn in range(25, 52, 2)]                          # east edge of the tea porters' path (the gap at n 52 is the gate into the lookout terrace)
    + [["MV-Prop_WoodenFence_Single", 32.0, 17.0, 0, 90, 1]]
    + [["MV-Prop_WoodenFence_Single", 23.3, 50.3, 0, 90, 1], ["MV-Prop_WoodenFence_Single", 29.3, 50.4, 0, 90, 1]]      # closes the 2.2 m slot between E05 and E06 (flood-fill checked: the interior is unreachable): standing in it the camera is pulled to 0.52 m (median 1.13 m), measured in compression-cause.json. The west fence stands 0.8 m inside the mouth so that E06's west-facing door stays clear
    + [["MV-Balcony_Cross_Straight", float(x_), 76.2, 2.0, 0, 1] for x_ in (-4, -2, 0, 2, 4)] + [["MV-Balcony_Cross_Straight", float(sx_ * 5.0), float(n_), 2.0, 90, 1] for sx_ in (-1, 1) for n_ in (77.2, 79.2)]     # batch 5: a ceremonial rail round the hall porch's forecourt (front at n 76.2, returns at x +-5): north of it the camera is pulled to 0.94 m and the character to 0.14 opacity in 46-63 % of a full turn (03); the player stops at n 75.7 where the minimum is 2.2 m
    + [["MV-Prop_WoodenFence_Single", 19.4, 37.3, 0, 90, 1]]                                                     # closes the 1.8 m dead-end pocket between the lane fence (n 36.15) and B14's south wall (found by the E05 block circuit: the autopilot jammed in it)
    + [["MV-Prop_WoodenFence_Single", float(xx), 60.4, 0, 0, 1] for xx in (23, 25, 27)]                              # north edge of the tea lane facing E05 (gives the lane a side; ground and hedges beyond are stand-ins)                                                         # closes the corner between the warehouse and the path
    + [["MV-Corner_Exterior_Wood", 34.4, 24.0, 0, 0, [1, 1, 1.3]], ["FP-Lantern_Wall", 34.4, 24.0, 2.45, 90, 1], ["MV-Corner_Exterior_Wood", 34.4, 38.0, 0, 0, [1, 1, 1.3]], ["FP-Lantern_Wall", 34.4, 38.0, 2.45, 90, 1],
       ["MV-Corner_Exterior_Wood", 34.4, 46.0, 0, 0, [1, 1, 1.3]], ["FP-Lantern_Wall", 34.4, 46.0, 2.45, 90, 1]]            # lantern posts along the path (outside its 2 m width, against the fence)
    # the lookout terrace's west end keeps its tea-house furniture, moved 2.8 m east of the gate so the porters' path reaches E05's east door
    + [["FP-Bench", 34.6, 53.0, 0, 0, 1], ["SY-table01", 35.8, 54.8, 0, 0, 1], ["SY-table-cloth01", 35.8, 54.8, 0.82, 0, 1], ["SY-stool", 34.9, 54.8, 0, 0, 1], ["SY-stool", 36.7, 54.8, 0, 0, 1], ["SY-mug03", 35.7, 54.7, 0.84, 0, 1], ["SY-platter-of-pie", 36.0, 54.95, 0.84, 0, 1]]
    + [["FP-Barrel", 31.0, 40.5, 0, 0, 1], ["MV-Prop_Crate", 30.8, 42.0, 0, 20, 1], ["AV-mdvl_props_sack_01", 31.3, 47.6, 0, 40, 1], ["AV-mdvl_props_sack_01", 30.8, 48.1, 0, 90, 1]]     # back doors of the east shops
)
# batch 4 paving rows (2 m cells, later rows overwrite earlier ones): the tea porters' path, the red-brick loading apron under B13's canopy, E04's tally loggia floor and the gallery strip in front of E05 (red brick = threshold, as at the market halls)
EAST_PAVING = [("D7 Tea porters' path (Jalur Teh)", 32, 34, 18, 48, "MV-Floor_UnevenBrick"), ("D8 Tea porters' path, gate bend", 30, 32, 48, 52, "MV-Floor_UnevenBrick"), ("D7 Loading apron (B13)", 24, 32, 16, 18, "MV-Floor_RedBrick"), ("D7 Tally loggia floor (E04)", 18, 26, 22, 24, "MV-Floor_RedBrick"),
               ("D8 Tea house gallery strip (E05)", 22, 30, 54, 58, "MV-Floor_RedBrick")]
# a message from the data to the preview: dressing P1.4 placed where the batch-4 buildings now stand (each removal is a documented correction)
DRESS_DROP_B4 = {("MV-Prop_Crate", 27.0, 17.3): "B13's canopy now carries its own loading station (tally table, sacks, barrels); these stood inside it", ("MV-Prop_Crate", 28.2, 17.4): "same", ("MV-Prop_Crate", 27.5, 17.35): "same",
                 ("FP-Barrel", 29.5, 17.3): "same", ("FP-Barrel", 30.4, 17.5): "same",
                 ("FP-Crate_Wooden", 20.0, 23.2): "inside E04's tally loggia, which now carries its own goods", ("MV-Prop_WoodenFence_Single", 31.0, 52): "the gate from the tea porters' path into the lookout terrace (x 30-32)",
                 ("MV-Corner_Exterior_Wood", 30.6, 51.4): "stood in the gate", ("FP-Lantern_Wall", 30.6, 51.4): "stood in the gate",
                 ("FP-Bench", 33.0, 53): "moved 1.6 m east (re-added), it overlapped the gate", ("SY-table01", 33.0, 54.8): "moved 2.8 m east (re-added), it stood in front of E05's east door", ("SY-table-cloth01", 33.0, 54.8): "moved with the table",
                 ("SY-stool", 32.1, 54.8): "moved with the table", ("SY-stool", 33.9, 54.8): "moved with the table", ("SY-mug03", 32.9, 54.7): "moved with the table", ("SY-platter-of-pie", 33.2, 54.95): "moved with the table"}


def sign_instances(bid, A, x, n, rz, elev, chosen, inst, signs):
    """Trade signs and banners are separate placed objects (so each building can carry its own, as in the P1.4 schedule): one small kit node per (asset, scale)."""
    for k, e in enumerate([e for e in A.get("extras", []) if e.get("role") == "sign"]):
        asset = chosen or e["asset"]; sc = e.get("scale", 1.0); sc = sc[0] if isinstance(sc, list) else sc
        node = "SIGN_" + asset.replace("@", "_at_") + ("" if sc == 1.0 else ("_x%g" % sc).replace(".", "p"))
        wx, wn = rot90(e["pos"][0], e["pos"][1], rz)
        inst.append({"id": f"{bid}_sign{k}", "node": node, "x": round(x + wx, 3), "y": round(elev + e["pos"][2], 3), "z": round(-(n + wn), 3), "ry": rz + e.get("rz", 0), "label": "sign " + asset})
        signs[node] = {"asset": asset, "scale": sc}


def build():
    out = {"revision": "P2-A", "source": "P1.4 layout D", "rects": RECTS}
    bmap = {b[0]: b for b in T.BUILDINGS}
    arch = dict(T.ARCHETYPES); arch["A10p"] = T.ROW_KITS["provisions"]; arch["A10c"] = T.ROW_KITS["crafts"]
    inst, obs, signs = [], [], {}
    for bid in SLICE_BUILDINGS:
        b = bmap[bid]; _, a, dist, x, n, rz, label, opts, status = b
        opts = dict(opts or {}); opts["sign"] = SIGN_OVERRIDE.get(bid, opts.get("sign"))
        dx, dn = ADJUST.get(bid, (0.0, 0.0)); x, n = x + dx, n + dn
        elev = (opts or {}).get("elev", 0.0)
        kit = (opts or {}).get("kit")
        if a == "A02":                                              # covered market hall: one kit node per merchandise kit
            node = NODE_FOR_KIT[kit]; inst.append({"id": bid, "node": node, "x": x, "y": elev, "z": -n, "ry": rz, "label": label, "sign": (opts or {}).get("sign")})
            hall = hall_archetype(node, arch); sign_instances(bid, hall, x, n, rz, elev, (opts or {}).get("sign"), inst, signs)
            ob = Obs(x, n, rz, elev); proxies_for(a, hall, ob, kit=kit); obs += [dict(o, src=bid) for o in ob.out]; continue
        if a == "A01":                                              # Exchange Hall: five reusable modules at one transform
            for node in HALL_NODES:
                inst.append({"id": bid + node[3:], "node": node, "x": x, "y": elev, "z": -n, "ry": rz, "label": label + " (" + node[4:] + ")", "sign": None})
        else:
            node = NODE_FOR_BLD.get(bid, a)                                  # batch 3: district buildings are variants of their P1.4 archetype
            A = hall_archetype(node, arch) if node in HALL_VARIANTS else arch[a]
            inst.append({"id": bid, "node": node, "x": x, "y": elev, "z": -n, "ry": rz, "label": label, "sign": (opts or {}).get("sign")})
            sign_instances(bid, A, x, n, rz, elev, (opts or {}).get("sign"), inst, signs)
            ob = Obs(x, n, rz, elev); proxies_for(a, A, ob); obs += [dict(o, src=bid) for o in ob.out]; continue
        ob = Obs(x, n, rz, elev); proxies_for(a, arch[a], ob); obs += [dict(o, src=bid) for o in ob.out]
    for r in T.ROWS:
        node = "A10p" if r[1] == "provisions" else "A10c"
        inst.append({"id": r[0], "node": node, "x": r[2], "y": 0.0, "z": -r[3], "ry": r[4], "label": f"Market awning row ({r[1]})"})
        ob = Obs(r[2], r[3], r[4]); proxies_for(node, arch[node], ob); obs += [dict(o, src=r[0]) for o in ob.out]
    # market cross, gate arches (closed street gaps), terrace and hall podium, hall stand-in
    cx, cn, _ = T.CROSS_POS
    inst.append({"id": "M01", "node": "CROSS", "x": cx, "y": 0.0, "z": -cn, "ry": 0, "label": "Market cross"})
    obs += [{"x": cx, "z": -cn, "w": 2.0, "d": 2.0, "h": 1.0, "group": "wall", "src": "M01"}, {"x": cx, "z": -cn, "w": 0.5, "d": 0.5, "h": 4.0, "group": "post", "src": "M01"}]
    for a in T.DRESSING:
        if a[0] == "MV-Wall_Arch":
            inst.append({"id": f"ARCH{len([i for i in inst if i['node'] == 'ARCH']) + 1}", "node": "ARCH", "x": a[1], "y": a[3], "z": -a[2], "ry": a[4], "label": "Gate arch in a closed street gap"})
            ob = Obs(a[1], a[2], a[4], a[3]); ob.box(-0.95, 0, 0.15, 0.2, 0, 2.2, "post"); ob.box(0.95, 0, 0.15, 0.2, 0, 2.2, "post"); ob.box(0, 0, 2.0, 0.2, 2.2, 3.0, "arch", cam=True); obs += [dict(o, src="ARCH") for o in ob.out]
    tx, tn, _ = T.TERRACE_POS
    inst.append({"id": "TERRACE", "node": "TERRACE", "x": tx, "y": 0.0, "z": -tn, "ry": 0, "label": "Civic terrace steps, skirt and balustrade"})
    for e in T.TERRACE["extras"]:
        if e["asset"] == "MV-Balcony_Cross_Straight":
            obs.append({"x": tx + e["pos"][0], "z": -(tn + e["pos"][1] + 0.5), "w": 2.0, "d": 0.3, "h": 2.1, "group": "balustrade", "src": "TERRACE"})
    inst.append({"id": "PODIUM", "node": "PODIUM", "x": 0, "y": 1.0, "z": -84, "ry": 0, "label": "Hall podium deck and steps"})
    # cell paving: later PAVING rows overwrite earlier ones (as build_town does)
    cells = {}
    for pv in list(T.PAVING) + EAST_PAVING:
        name, a, b, c, d, tile = pv[:6]; z = pv[6] if len(pv) > 6 else 0.0
        for ix in range(int(a), int(b), 2):
            for iy in range(int(c), int(d), 2):
                cells[(ix + 1, iy + 1)] = (tile, z)
    for (cxx, cyy), (tile, z) in list(cells.items()):                      # P2-B batch 2: red-brick threshold apron in front of each market hall (two tile rows, hall width)
        if 42 <= cyy <= 43 and (-17.5 <= cxx <= -8.5 or 8.5 <= cxx <= 17.5):
            cells[(cxx, cyy)] = ("MV-Floor_RedBrick", z)
    tiles = {"cobble": [], "brick": [], "red": []}
    key = {"MV-Floor_UnevenBrick": "cobble", "MV-Floor_Brick": "brick", "MV-Floor_RedBrick": "red"}
    for (cxx, cyy), (tile, z) in sorted(cells.items()):
        if inreg(cxx, cyy):
            tiles[key[tile]].append([cxx, -cyy, z])
    # dressing: only items next to the slice; no vegetation (out of scope)
    keep_rect = [(-16, 16, 6, 60), (-34, -14, 34, 60), (-16, 16, 58, 96), (16, 48, 34, 70), (-34, -12, 0, 36), (-16, 16, -8, 6), (16, 40, 0, 36)]
    # P2-B batch 3 correction: the joiner's open drying shed (B12, north side) stands exactly where P1.4 put three workyard props; the shed is the covered half of that yard, so the duplicates are dropped
    # (the well stays). Evidence: 4 solid overlaps between B12's proxies and these props in the first district test (p2c-batch3 doc 04).
    DRESS_DROP = {("FP-Workbench", -22.7, 32.9), ("FP-Anvil_Log", -20.9, 32.8), ("FP-Barrel", -23.5, 33.7)}
    dress = [d for d in T.DRESSING if not d[0].startswith("SN-") and d[0] != "MV-Wall_Arch" and (d[0], d[1], d[2]) not in DRESS_DROP and (d[0], d[1], d[2]) not in DRESS_DROP_B4 and any(a <= d[1] <= b and c <= d[2] <= e for a, b, c, e in keep_rect)]
    dress += EAST_DRESS
    for d in dress:
        a = d[0]
        if a in FOOT:
            w, dd, h = FOOT[a]; s = d[5] if not isinstance(d[5], list) else d[5][0]
            ob = Obs(d[1], d[2], d[4]); ob.elev = 0; ob.box(0, 0, w * s, dd * s, d[3], d[3] + h * s, "prop")
            if a != "FP-Bench":
                obs += [dict(o, src="dressing") for o in ob.out]
            else:
                obs += [dict(o, src="dressing", group="bench") for o in ob.out]
        elif a == "MV-Corner_Exterior_Wood":
            zs = d[5][2] if isinstance(d[5], list) else 1.0
            obs.append({"x": d[1], "z": -d[2], "w": 0.4, "d": 0.4, "h": round(d[3] + 3.0 * zs, 3), "group": "post", "src": "dressing"})
        elif d[3] < 0.3 and measured_box(a, d[5] if not isinstance(d[5], list) else d[5][0]):                   # batch 4: floor-standing AV/SY dressing gets its measured footprint too
            s_ = d[5] if not isinstance(d[5], list) else d[5][0]; w_, dd_, y0_, y1_, cx_, cn_ = measured_box(a, s_)
            ob = Obs(d[1], d[2], d[4]); ob.elev = 0; ob.box(cx_, cn_, w_, dd_, d[3] + y0_, d[3] + y1_, "prop"); obs += [dict(o, src="dressing") for o in ob.out]
        elif a == "CUS-Bunting_10":
            ang = math.radians(d[4])
            for k in range(11):
                t = (k - 5) * 0.96
                x, n = d[1] + t * math.cos(ang) * (d[5][0] if isinstance(d[5], list) else 1), d[2] + t * math.sin(ang)
                sag = 0.6 * (1 - (t / 4.8) ** 2)
                obs.append({"x": round(x, 3), "z": round(-n, 3), "w": 1.1, "d": 0.5, "h": round(d[3] + 0.05, 3), "minY": round(d[3] - 0.6 * (1 - (abs(t) / 4.8) ** 2) * 1.0 - 0.45, 3), "cameraOnly": True, "group": "pennant", "src": "dressing"})
    out["dressing"] = [[d[0], d[1], d[2], d[3], d[4], d[5]] for d in dress]
    for i in inst:
        i["district"] = {"D1": "D1", "D2": "D2", "D3": "D3", "D5": "D5", "D6": "D6", "D7": "D7", "D8": "D8"}[district_at(i["x"], -i["z"])] if not i["node"] in ("TERRACE", "PODIUM") and not i["node"].startswith("A01_") else "D5"
    out["dressing_district"] = [district_at(d[1], d[2]) for d in dress]
    for (px, pn, w_, d_) in tuple((x_, 76.2, 2.0, 0.25) for x_ in (-4.0, -2.0, 0.0, 2.0, 4.0)) + tuple((s_ * 5.0, n_, 0.25, 2.0) for s_ in (-1, 1) for n_ in (77.2, 79.2)):      # batch 5: the Exchange Hall forecourt rail (solid for the body; the porch is not reachable)
        obs.append({"x": px, "z": -pn, "w": w_, "d": d_, "h": 3.1, "minY": 2.0, "group": "balustrade", "src": "PORCH_RAIL"})
    for sx in (-1, 1):                                                       # batch 5: solid side edges of the +1.0 m terrace for the body standing on the ground (the controller's step rule only looks at the centre, so the body overlapped the plinth by its radius); the terrace surface (y 1.01) is above the 1.0 top and unaffected
        obs.append({"x": sx * 13.95, "z": -68.0, "w": 0.1, "d": 12.0, "h": 1.0, "group": "wall", "src": "TERRACE"})
    out["instances"] = inst; out["tiles"] = tiles; out["collision"] = obs; out["signs"] = signs
    out["spawn"] = {"x": 0.0, "z": -4.0, "yaw": 0.0}
    out["nodes"] = {k: [v[0], v[1], v[2]] for k, v in T.NODES.items()}
    out["nodes"]["N17"] = list(N17_NEW)
    out["nodes"]["N29"] = [2.9, 49, "Cross-passage east of the cross (centre of the 3.85 m gap to the awning-row posts)"]
    out["nodes"]["N30"] = [-2.9, 49, "Cross-passage west of the cross (centre of the 3.85 m gap to the awning-row posts)"]
    # polyline waypoints for edges whose straight node-to-node line passed within 0.5 m of a solid (measured in the P2-A closeout network test)
    out["nodes"]["N18"] = [-13, 42.5, "Market Hall West south entrance (centre of the 4 m open front)"]
    out["nodes"]["N31"] = [-13, 49, "Market Hall West interior (centre of the aisle)"]
    out["nodes"]["N19"] = [13, 42.5, "Market Hall East south entrance (centre of the 4 m opening between the closed bays)"]
    out["nodes"]["N32"] = [13, 49, "Market Hall East interior (centre of the aisle)"]
    out["edge_via"] = {"N05-N29": [[2.9, 46.4]], "N29-N27": [[2.9, 51.6]], "N05-N30": [[-2.9, 46.4]], "N30-N27": [[-2.9, 51.6]], "N23-N06": [[-7.5, 60.3]], "N24-N06": [[7.5, 60.3]]}
    out["corrections"] = {"adjust": {k: list(v) for k, v in ADJUST.items()}, "N17": list(N17_NEW[:2]), "N29": [2.9, 49], "N30": [-2.9, 49], "N18": [-13, 42.5], "N31": [-13, 49], "N19": [13, 42.5], "N32": [13, 49], "N40": [-20.1, 35.4], "dress_dropped": [list(d) for d in sorted(DRESS_DROP)]}
    # P2-B batch 3: door nodes of the district buildings (spurs off the P1.4 lane and court nodes) and the first alley (B10-B11). Positions are first estimates; the network test measures the free span.
    out["nodes"]["N40"] = [-21.5, 35.0, "Artisan workyard (north of the joiner's drying shed)"]
    out["nodes"]["N40"] = [-20.1, 35.4, "Artisan workyard (east of the well, north of the joiner's drying shed)"]
    out["nodes"].update({"N42": [-16.3, 10.9, "Smithy (B10) front, lane centre of the free span"], "N43": [-16.0, 19.8, "Potter's shop (B11) front, closing the cross street"],
                         "N44": [-15.7, 29.7, "Joiner (B12) front, lane centre of the free span"], "N45": [-6.1, 2.0, "Outfitter (E01) front, arrival court west"], "N46": [5.8, 2.5, "Carrier's office (E02) front, arrival court east"]})
    out["edges"] = [list(e) for e in T.EDGES] + [["N09", "N42", "district"], ["N42", "N10", "district"], ["N10", "N43", "district"], ["N10", "N44", "district"], ["N44", "N11", "district"],
                                                   ["N01", "N45", "district"], ["N01", "N46", "district"]]
    # P2-B batch 4: door nodes of B13, E04, E05, the court, the tea porters' path (Jalur Teh) and the loop it closes (court -> path -> lookout terrace -> tea lane -> bazaar -> warehouse lane).
    # N41 moves 1 m north: the lane centre of P1.4 (n 58) is 0.6 m from E05's gallery posts (n 57.4). Positions are first estimates; the network test measures the free span and they are corrected there.
    out["nodes"]["N41"] = [26.0, 59.0, "Tea lane in front of E05's gallery (north of the gallery posts)"]
    out["nodes"].update({
        "N47": [16.0, 12.0, "Warehouse (B13) lane gable doors, lane centre"], "N48": [28.6, 19.0, "Warehouse (B13) loading bays, court side, beyond the canopy"],
        "N49": [23.5, 21.3, "Counting house (E04) tally loggia, court side"], "N50": [16.0, 29.0, "Counting house (E04) lane door, lane centre"],
        "N51": [33.0, 20.0, "Tea porters' path, south end at the court's east opening"], "N52": [33.0, 30.0, "Tea porters' path behind the counting house"],
        "N53": [33.0, 41.0, "Tea porters' path behind the east shops"], "N54": [31.0, 50.0, "Tea porters' path, bend before the gate into the lookout terrace"],
        "N58": [19.7, 54.5, "E05 west (bazaar-side) door, east market lane"], "N59": [31.3, 54.5, "E05 east (porters') door, west end of the lookout terrace, reached through the gate at x 30-32"]})
    out["edges"] += [["N12", "N47", "district"], ["N47", "N13", "district"], ["N13", "N50", "district"], ["N50", "N14", "district"], ["N33", "N48", "district"], ["N33", "N49", "district"], ["N33", "N51", "district"],
                     ["N51", "N52", "porters"], ["N52", "N53", "porters"], ["N53", "N54", "porters"], ["N54", "N59", "porters"], ["N39", "N58", "district"], ["N58", "N24", "district"], ["N16", "N59", "district"]]
    out["edge_via"]["N53-N54"] = [[32.6, 46.8]]
    out["corrections"]["batch4"] = {"N41": [26.0, 59.0], "dress_dropped": [list(k) + [v] for k, v in sorted(DRESS_DROP_B4.items())], "sign_override": SIGN_OVERRIDE}
    # P2-B batch 5: door nodes of the two tower houses (their entrances face the bazaar's north plaza) and edges from the plaza corners
    out["nodes"].update({"N60": [-19.0, 60.8, "Assay office (B15) door, bazaar north-west plaza"], "N61": [19.0, 60.8, "Chart maker (B16) door, bazaar north-east plaza"]})
    out["edges"] += [["N23", "N60", "district"], ["N24", "N61", "district"]]
    out["corrections"]["batch5"] = {"terrace_edge_walls": "x = -13.95 and 13.95, n 62-74, top 1.0: the body stops 0.34 m from the terrace edge (batch 4 platform test: centre reached the edge)", "N60": [-19.0, 60.8], "N61": [19.0, 60.8]}
    out["views"] = {k: {"pos": [v[0][0], v[0][2], -v[0][1]], "look": [v[1][0], v[1][2], -v[1][1]], "fov": v[2], "who": v[3]} for k, v in T.VIEWS.items()}
    # additional parity cameras for the slice: (camera x, n, z), (look-at x, n, z), vertical fov, explorer (x, n) or None
    extra = {"p2a-aerial": ((34, -38, 52), (2, 52, 2), 40, None), "p2a-junction": ((2.2, 4.6, 1.65), (-6.5, 17, 5.0), 62, (0.4, 8.5)),
             "p2a-inn": ((-14.5, 38.5, 1.65), (-26.5, 46, 3.4), 64, (-19.0, 42.0)), "p2a-terrace": ((0.8, 50.5, 1.65), (0, 74, 3.0), 62, (-0.6, 55.0)),
             "p2a-tea": ((24.0, 55.0, 1.65), (36.5, 66, 3.2), 62, (29.0, 57.5)),
             "p2b-hall-aerial": ((38, 46, 30), (0, 82, 8), 42, None), "p2b-hall-porch": ((-4.5, 70.5, 3.7), (0.5, 80.5, 4.2), 62, (0.4, 75.5, 2.0)),
             "p2b-hall-tower": ((-14, 62, 2.4), (0, 82, 14), 62, (-9.5, 64.5, 1.0)), "p2b-junction-fixed": ((2.2, 4.6, 1.65), (-8.5, 19.9, 4.0), 62, (0.4, 8.5)),
             # batch 2 (Central Bazaar): elevated, central aisle at eye height, follow-camera equivalent, both hall entrances, covered interior, axis to the Exchange Hall
             "p3-bazaar-aerial": ((30, 24, 22), (0, 50, 2), 44, None), "p3-aisle-eye": ((0.5, 36.5, 1.65), (0, 62, 2.4), 62, (0.3, 41.0)),
             "p3-gameplay": ((0.0, 24.2, 7.2), (0, 36, 2.1), 60, (0.0, 36.0)), "p3-west-entrance": ((-9.5, 37.5, 1.65), (-13, 46, 2.3), 62, (-12.4, 40.5)),
             "p3-east-entrance": ((9.5, 37.5, 1.65), (13, 46, 2.3), 62, (12.4, 40.5)), "p3-west-interior": ((-13.6, 45.4, 1.65), (-12.5, 56, 2.4), 64, (-12.0, 48.6)),
             "p3-east-interior": ((13.6, 45.4, 1.65), (12.5, 56, 2.4), 64, (12.0, 48.6)), "p3-axis-to-hall": ((0.0, 31.0, 1.65), (0, 76, 4.5), 62, (0.4, 34.5)),
             "p3-shops-east": ((19.4, 36.8, 1.65), (25.6, 44.2, 2.6), 72, (21.0, 40.3)), "p3-shop-e07": ((-17.0, 52.4, 1.65), (-24.8, 56.0, 2.3), 64, (-19.3, 53.6)),
             # batch 3: the artisan lane and the south gateway
             "p4-district-aerial": ((-44, -8, 26), (-12, 18, 2), 46, None), "p4-lane-north": ((-16.0, 2.5, 1.65), (-16.0, 30, 2.4), 62, (-16.0, 6.0)),
             "p4-cross-vista": ((-3.5, 20.0, 1.65), (-20.5, 20.0, 2.6), 60, (-1.6, 20.1)), "p4-smithy": ((-14.4, 6.0, 1.65), (-19.5, 11.8, 1.8), 68, (-15.8, 8.4)),
             "p4-joiner": ((-14.4, 24.0, 1.65), (-20.0, 29.8, 1.8), 68, (-15.8, 26.6)), "p4-potter": ((-14.2, 16.0, 1.65), (-20.5, 21.0, 1.8), 68, (-15.8, 18.2)),
             "p4-gate-back": ((0.0, 10.5, 1.65), (0.0, -2.0, 2.6), 72, (0.0, 4.5)), "p4-carrier": ((3.5, 6.5, 1.65), (11.5, -1.6, 2.0), 64, (5.5, 3.5)),
             "p4-outfitter": ((-2.5, 6.5, 1.65), (-11.5, -0.2, 1.8), 64, (-4.5, 3.5)), "p4-lane-south": ((-16.0, 36.0, 1.65), (-16.0, 8.0, 2.4), 62, (-16.0, 32.0)),
             "p4-town-aerial": ((70, -30, 80), (0, 42, 0), 50, None), "p4-west-hall-interior-b": ((-13.0, 40.5, 1.65), (-13.0, 56, 3.2), 70, (-13.0, 43.5)),
             # batch 4: the Eastern Trade Quarter (warehouse lane D7, service court, counting house) and the tea route (E05)
             "p5-east-aerial": ((60, 46, 40), (26, 22, 1), 40, None), "p5-quarter-sw": ((-4, -12, 32), (26, 26, 2), 44, None), "p5-lane-east": ((16.0, 2.5, 1.65), (16.0, 30, 2.4), 62, (16.0, 6.0)),
             "p5-warehouse-gable": ((15.4, 5.2, 1.65), (22.5, 12.0, 3.2), 66, (16.2, 7.6)), "p5-court-from-lane": ((17.0, 20.0, 1.65), (28.0, 20.0, 2.8), 68, (18.6, 20.4)),
             "p5-court-from-east": ((34.2, 18.4, 1.65), (22.0, 20.0, 3.0), 70, (32.6, 18.8)), "p5-loading-bay": ((23.5, 19.6, 1.65), (27.5, 16.0, 3.4), 64, (24.4, 19.4)),
             "p5-counting-front": ((15.5, 31.0, 1.65), (21.0, 26.0, 4.5), 66, (16.0, 29.0)), "p5-counting-loggia": ((21.0, 20.5, 1.65), (23.5, 25.0, 3.0), 62, (21.8, 21.5)),
             "p5-tea-entrance": ((18.8, 60.2, 1.65), (26.5, 56.0, 2.8), 64, (20.2, 59.4)), "p5-tea-lane-east": ((20.5, 58.8, 1.65), (37.0, 58.0, 3.0), 62, (22.0, 58.6)),
             "p5-tea-back": ((30.0, 44.0, 1.65), (28.5, 56.0, 2.6), 62, (29.8, 46.5)), "p5-bazaar-ne": ((13.0, 58.4, 2.6), (27.0, 55.0, 3.0), 62, (15.2, 58.6)),
             "p5-quarter-gameplay": ((16.0, 2.4, 8.4), (16.0, 20.0, 2.0), 60, (16.0, 14.0)), "p5-route-aerial": ((46, 20, 40), (26, 46, 2), 44, None),
             # batch 5: whole-town set (t01-t10) and Civic Terrace views (c01-c04); eye-level cameras use a player at the given (x, n)
             "t01-town-aerial": ((52, -34, 66), (0, 46, 3), 46, None), "t02-southern-arrival": ((0.0, -3.5, 1.65), (0, 36, 5.5), 64, (0.0, 1.0)), "t03-merchant-street": ((0.4, 22.0, 1.65), (0, 50, 4.5), 62, (0.2, 25.0)),
             "t04-central-bazaar": ((16.0, 38.0, 2.0), (-2, 54, 3.0), 66, (14.5, 39.0)), "t05-artisan-lane": ((-16.0, 2.5, 1.65), (-16.0, 30, 2.4), 62, (-16.0, 6.0)), "t06-warehouse-district": ((17.0, 20.0, 1.65), (28.0, 20.0, 2.8), 68, (18.6, 20.4)),
             "t07-tea-route": ((20.5, 58.8, 1.65), (37.0, 58.0, 3.0), 62, (22.0, 58.6)), "t08-civic-terrace": ((0.0, 56.0, 2.6), (0, 79, 6), 72, (0.0, 58.5)), "t09-exchange-hall-approach": ((0.0, 64.5, 2.65), (0, 86, 6.5), 64, (0.0, 66.0)),
             "t10-lookout-to-terrace": ((38.5, 58.0, 2.8), (0, 70, 6), 70, (37.0, 57.0)),
             "c01-terrace-aerial": ((40, 44, 28), (0, 72, 5), 46, None), "c02-assay-office": ((-12.0, 58.8, 1.65), (-19.5, 64.0, 3.6), 64, (-13.6, 59.2)), "c03-chart-maker": ((12.0, 58.8, 1.65), (19.5, 64.0, 3.6), 64, (13.6, 59.2)), "c04-terrace-from-hall": ((0.0, 76.0, 3.2), (0, 60, 3.0), 70, (0.0, 74.5))}
    out["kit_nodes"] = sorted({i["node"] for i in inst} | {"TILE_cobble", "TILE_brick", "TILE_red"})
    for k, v in extra.items():
        out["views"][k] = {"pos": [v[0][0], v[0][2], -v[0][1]], "look": [v[1][0], v[1][2], -v[1][1]], "fov": v[2], "who": v[3]}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=0)
    print("scene.json:", len(inst), "instances,", sum(len(v) for v in tiles.values()), "tiles,", len(dress), "dressing items,", len(obs), "obstacles;",
          {g: sum(1 for o in obs if o["group"] == g) for g in sorted({o["group"] for o in obs})})


if __name__ == "__main__":
    build()
