#!/usr/bin/env python3
"""Single source of truth for Merchant Citadel P1.4 (creative redesign; selected layout = alternative D of layouts_p14.py): archetype assemblies and the measured town layout.

Plain Python (no Blender). Running it writes archetypes.json / layout.json for the Blender scripts and
the CSV schedules for the planning package, after running the nominal spatial checks.  The checks on
ACTUAL rendered geometry (roof overhangs, banners, lanterns, walkability, camera) are in validate_envelopes.py.

Local archetype frame (Blender): x = along the frontage, y = depth (front facade at y = -D/2, facing -y), z = up.
Facade strings list 2 m modules left-to-right as seen from outside; one string per floor. Codes: see citadel_lib.CODES
  P plaster  G half-timber grid  F/R/T plaster window (wide flat / wide round / thin round)  D/O plaster door (flat / round)
  I plaster inset round portal  S stone  s/r stone window  o/d stone door  A open timber arch  X nothing (hidden face)

Asset ids:  MV-/FP-/SN- = downloaded Quaternius model;  SY- = downloaded Syntaxes of Play cafe model;  AV- = downloaded
Avramania model;  "<id>@burgundy|blue|gold|cream" = cloth MATERIAL VARIANT;  "<roof id>@dark" = civic roof-tile MATERIAL
VARIANT;  CUS-Seal_NiagaAwan and CUS-Sign_<glyph>_<field> = CUSTOM concept geometry (not downloaded).
"""
import csv, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layouts_p14 as LY

REVISION = "P1.4"
EMBLEM = "CUS-Seal_NiagaAwan"
ROOF = {4: (3.73, 0.52, 2.757), 6: (4.89, 0.78, 4.125), 8: (6.0, 0.78, 4.976)}  # span: ridge rise, eave drop, half width (measured)


def roof_z(span, d):
    """Height of the tile surface above the wall top, d metres from the ridge line."""
    r, e, h = ROOF[span]
    return r - (r + e) * d / h


def lantern(x, y, z=2.2, rz=0):
    return {"asset": "FP-Lantern_Wall", "pos": [x, y, z], "rz": rz}


def banner(x, y, z, rz=-90, asset="FP-Banner_1@blue"):
    """Civic / market cloth banner. role=sign lets a building swap the cloth colour."""
    return {"asset": asset, "pos": [x, y, z], "rz": rz, "role": "sign"}


def tsign(x, y, z, glyph, field="wood", rz=0):
    """Hanging trade sign (custom). Origin on the wall; rz = facade rotation (0 front, 90 right wall, -90 left wall).
    Scale 1.4: 0.70 x 0.56 m board, underside 0.78 m below the arm."""
    return {"asset": f"CUS-Sign_{glyph}_{field}", "pos": [x, y, z], "rz": rz, "scale": 1.4, "role": "sign"}


def awning(x, y, z, colour, rz=0):
    """Striped cloth shop awning, one 2 m bay (custom). Underside of the valance is 0.89 m below the fixing edge."""
    return {"asset": f"CUS-Awning_{colour}", "pos": [x, y, z], "rz": rz}


def wbox(x, y, z, rz=0):
    """Flower box under a window sill (Avramania Village Builder)."""
    return {"asset": "AV-mdvl_village_window_box_01", "pos": [x, y, z], "rz": rz}


def vine(x, y, z, rz=0, kind=1):
    return {"asset": f"MV-Prop_Vine{kind}", "pos": [x, y, z], "rz": rz}


def emblem(x, y, z, size, rz=0):
    return {"asset": EMBLEM, "pos": [x, y, z], "rz": rz, "scale": size}


def dormer(span, top, along, side, x0=0.9, ridge="y"):
    """Roof_Dormer_RoundTile seated on a slope. side = +1 / -1 picks the slope."""
    z = top + roof_z(span, x0 + 1.9)
    if ridge == "y":
        return {"asset": "MV-Roof_Dormer_RoundTile", "pos": [side * x0, along, z], "rz": 0 if side > 0 else 180}
    return {"asset": "MV-Roof_Dormer_RoundTile", "pos": [along, side * x0, z], "rz": 90 if side > 0 else -90}


def chimney(span, top, x, y, d, asset="MV-Prop_Chimney2"):
    return {"asset": asset, "pos": [x, y, top + roof_z(span, d) - 0.25]}


def pentice(W, D, z=2.6):
    """Timber shopfront canopy across the whole front (Roof_Wooden_2x1 L / Center / R)."""
    n = W // 2
    out = []
    for i in range(n):
        kind = "L" if i == 0 else "R" if i == n - 1 else "Center"
        out.append({"asset": f"MV-Roof_Wooden_2x1_{kind}", "pos": [-W / 2 + 1 + 2 * i, -D / 2, z]})
    return out


def exchange_hall():
    z0 = 1.0  # podium height
    parts = [
        # stone ground floor, plaster upper floor; central inset portal flanked by two round doors
        {"id": "main", "W": 14, "D": 8, "floors": 2, "roof": "8x14", "ridge": "x", "offset": [0, 0, z0], "corner": ["brick", "wood"], "core_inset": 1.05, "roof_variant": "dark",
         "facades": {"front": ["rsoIosr", "RRPPPRR"], "back": ["SsSsSsS", "PRPRPRP"], "right": ["SXXS", "PXXP"], "left": ["SXXS", "PXXP"]}},
        # P1.1: tower moved to the centre of the plan. It rises through the ridge (walls start at floor 3, above the roof)
        # so the front eave is no longer cut and the roof meets the tower on four symmetric lines.
        # P1.4: tower one storey taller (walls 9..18 m above the podium); its middle storey carries a seal on all four faces
        {"id": "tower", "W": 4, "D": 4, "floors": 6, "floor_from": 3, "tower_roof": True, "roof_variant": "dark", "offset": [0, 0, z0], "corner": "wood",
         "facades": {"front": ["XX", "XX", "XX", "PP", "PP", "RR"], "right": ["XX", "XX", "XX", "TT", "PP", "RR"],
                     "back": ["XX", "XX", "XX", "PP", "PP", "RR"], "left": ["XX", "XX", "XX", "TT", "PP", "RR"]}},
        {"id": "wing_e", "W": 6, "D": 6, "floors": 2, "roof": "6x6", "ridge": "x", "gables": ["a"], "offset": [10, 0, z0], "corner": ["brick", "wood"], "roof_variant": "dark",
         "skip_corners": [[-1, -1], [-1, 1]],
         "facades": {"front": ["sss", "RRR"], "back": ["SsS", "PRP"], "right": ["SsS", "PRP"], "left": ["XXX", "XXX"]}},
        {"id": "wing_w", "W": 6, "D": 6, "floors": 2, "roof": "6x6", "ridge": "x", "gables": ["b"], "offset": [-10, 0, z0], "corner": ["brick", "wood"], "roof_variant": "dark",
         "skip_corners": [[1, -1], [1, 1]],
         "facades": {"front": ["sss", "RRR"], "back": ["SsS", "PRP"], "left": ["SsS", "PRP"], "right": ["XXX", "XXX"]}},
        # P1.2 entrance porch: a gabled loggia on stone piers in front of the three doors. Its 6 x 6 roof runs back into the
        # main roof slope (the ridge is buried 3 m behind the wall line), so no open roof end is left.
        {"id": "porch", "W": 6, "D": 2, "floors": 1, "roof": "6x6", "ridge": "y", "gables": ["a"], "offset": [0, -5, z0], "corner": "brick",
         "core": False, "roof_shift": [0, 1.4], "roof_variant": "dark", "skip_corners": [[-1, 1], [1, 1]],
         "facades": {"front": ["AAA"], "right": ["A"], "left": ["A"], "back": ["XXX"]}},
    ]
    extras = []
    # P1.1 podium: one continuous dressed-brick deck (2 m tiles at +1.0 m) on a stone skirt, replacing 112 separate blocks
    side = "MV-Stairs_Exterior_SingleSide"
    for ix in range(-7, 7):
        cx = ix * 2 + 1
        for iy in range(-5, 3):
            extras.append({"asset": "MV-Floor_Brick", "pos": [cx, iy * 2 + 1, z0]})
        extras.append({"asset": side, "pos": [cx, -9, 0], "rz": 90})   # full front skirt, also behind the stair flanks
        extras.append({"asset": side, "pos": [cx, 5, 0], "rz": -90})
    for iy in range(-5, 3):
        extras.append({"asset": side, "pos": [-13, iy * 2 + 1, 0], "rz": 0})
        extras.append({"asset": side, "pos": [13, iy * 2 + 1, 0], "rz": 180})
    for i, a in enumerate(["Straight_L", "Straight_Center", "Straight_Center", "Straight_Center", "Straight_R"]):
        extras.append({"asset": f"MV-Stairs_Exterior_{a}", "pos": [-4 + 2 * i, -11, 0], "rz": 0})
    # guild identity: seal in the porch gable and on the tower, four burgundy cloth banners between the upper windows
    extras += [emblem(0, -6.12, z0 + 4.75, 1.45), emblem(0, -2.11, z0 + 13.5, 2.3), emblem(0, 2.11, z0 + 13.5, 2.3, rz=180),
               emblem(2.11, 0, z0 + 13.5, 2.3, rz=90), emblem(-2.11, 0, z0 + 13.5, 2.3, rz=-90)]
    extras += [dormer(8, z0 + 6, x, -1, 1.2, ridge="x") for x in (-5.0, 5.0)]
    # plinth row: the hall stands on the civic terrace (+1 m), so its podium is 2 m above the ground behind and beside it
    for ix in range(-7, 7):
        extras.append({"asset": side, "pos": [ix * 2 + 1, 5, -1.0], "rz": -90})
    for iy in range(-5, 3):
        extras.append({"asset": side, "pos": [-13, iy * 2 + 1, -1.0], "rz": 0}); extras.append({"asset": side, "pos": [13, iy * 2 + 1, -1.0], "rz": 180})
    extras += [{"asset": "FP-Banner_2_Cloth@burgundy", "pos": [x, -4.13, z0 + 5.95]} for x in (-5, -3, 3, 5)]
    extras += [lantern(-1.0, -4.1, z0 + 2.3), lantern(1.0, -4.1, z0 + 2.3)]
    return {"name": "Exchange Hall (Balai Niaga Awan)", "parts": parts, "extras": extras,
            "footprint": [28, 16], "height_m": 25.8, "floors": "2 storeys + central tower (walls above the roof on levels 4-6), gabled entrance porch, dormers, 1 m podium on the 1 m civic terrace"}


def market_hall():
    """One assembly, two dressing kits chosen per building: 'provisions' (west hall, blue) and 'crafts' (east hall, burgundy).
    The centre aisle (|x| < 1) and the cross-passage bay (y -2..0) stay clear in both kits."""
    T = "FP-Table_Large"
    K = lambda kit, asset, x, y, z=0, rz=0, sc=1.0: {"asset": asset, "pos": [x, y, z], "rz": rz, "scale": sc, "kit": kit}
    P, C = "provisions", "crafts"
    extras = [
        # --- provisions: produce, bread and cured goods, kegs, sacks ---
        K(P, "SY-food-display", -2.6, -3.6, 0, 90), K(P, "SY-crate02", -2.75, -5.1), K(P, "FP-Barrel_Apples", -3.2, -2.35),
        K(P, T, -2.6, 2.6, 0, 90), K(P, "AV-mdvl_food_loaf_01", -2.6, 1.7, 0.82), K(P, "AV-mdvl_food_loaf_01", -2.45, 2.05, 0.82, 40),
        K(P, "AV-mdvl_food_cheese_wheel_01", -2.65, 2.7, 0.82), K(P, "AV-mdvl_food_ham_01", -2.6, 3.4, 0.82, 70), K(P, "SY-basket-of-pastries", -2.75, 3.85, 0.82),
        K(P, T, 2.6, -3.6, 0, 90), K(P, "FP-FarmCrate_Apple", 2.6, -4.4, 0.82), K(P, "FP-FarmCrate_Carrot", 2.6, -3.5, 0.82, 90),
        K(P, "AV-mdvl_food_cabbage_01", 2.5, -2.75, 0.82), K(P, "AV-mdvl_food_cabbage_01", 2.75, -2.55, 0.82, 50),
        K(P, "SY-counter_L", 2.65, 3.55, 0, -90), K(P, "SY-counter_M", 2.65, 2.05, 0, -90), K(P, "AV-mdvl_food_scales_01", 2.6, 2.9, 1.16, 90),
        K(P, "AV-mdvl_food_fish_01", 2.6, 1.6, 1.16, 20), K(P, "AV-mdvl_food_fish_01", 2.7, 1.25, 1.16, -15), K(P, "SY-food-sausage", 2.6, 3.9, 1.16),
        K(P, "SY-keg01", -3.1, 4.9, 0, 90), K(P, "SY-keg02", -2.2, 5.3), K(P, "AV-mdvl_food_grain_sack_01", 3.2, 4.9), K(P, "AV-mdvl_food_grain_sack_01", 2.7, 5.25, 0, 40),
        K(P, "AV-mdvl_food_grain_sack_01", 3.25, 5.45, 0, 110), K(P, "FP-Barrel", 3.3, -5.3), K(P, "AV-mdvl_food_grain_sack_01", -3.3, -5.45, 0, 20),
        # --- crafts and general trade: pottery, bottles, books, cloth, tools ---
        K(C, T, -2.6, -3.6, 0, 90), K(C, "FP-Vase_2", -2.6, -4.4, 0.82), K(C, "FP-Pot_1", -2.6, -3.7, 0.82), K(C, "FP-Vase_4", -2.6, -3.0, 0.82), K(C, "FP-Pot_1_Lid", -2.45, -2.55, 0.82),
        K(C, "SY-table03", -2.6, 2.6, 0, 90), K(C, "SY-table-cloth03", -2.6, 2.6, 0.76, 90), K(C, "FP-Potion_1", -2.6, 1.9, 0.78), K(C, "FP-Potion_2", -2.5, 2.2, 0.78),
        K(C, "FP-SmallBottles_1", -2.65, 2.7, 0.78), K(C, "FP-Chalice", -2.6, 3.2, 0.78), K(C, "FP-CandleStick", -2.6, 3.5, 0.78),
        K(C, "SY-shelf01", 3.05, -3.6, 0, -90), K(C, "FP-Vase_2", 3.0, -3.9, 0.86), K(C, "FP-Bottle_1", 3.0, -3.3, 0.86), K(C, "SY-shelf01", 3.05, -5.0, 0, -90), K(C, "FP-Pot_1", 3.0, -5.0, 0.86),
        K(C, T, 2.6, 2.6, 0, 90), K(C, "FP-BookGroup_Medium_1", 2.6, 1.8, 0.82, 90), K(C, "FP-Scroll_1", 2.6, 2.5, 0.82), K(C, "FP-Scroll_2", 2.5, 2.85, 0.82, 60),
        K(C, "FP-Coin_Pile", 2.65, 3.3, 0.82), K(C, "SY-balance-scale", 2.6, 3.75, 0.82),
        K(C, "FP-Crate_Wooden", -3.3, -5.3), K(C, "MV-Prop_Crate", -3.2, 5.2, 0, 12), K(C, "MV-Prop_Crate", -3.1, 5.15, 1.06, 25), K(C, "FP-Bag", 3.2, 4.6, 0, 30),
        K(C, "FP-Barrel", -3.3, 4.4), K(C, "FP-Dummy", 3.3, 5.3, 0, 200), K(C, "FP-Crate_Metal", -2.5, -5.4, 0, 10),
        # --- shared ---
        {"asset": "FP-Bench", "pos": [0, 4.9, 0]},
    ]
    # market identity: seal on both gables, cloth banners on the four corners (blue by default; the east hall hangs burgundy)
    extras += [emblem(0, -6.12, 5.25, 1.3), emblem(0, 6.12, 5.25, 1.3, rz=180)]
    extras += [banner(-4.1, -6.1, 3.9, -90), banner(4.1, -6.1, 3.9, -90), banner(-4.1, 6.1, 3.9, 90), banner(4.1, 6.1, 3.9, 90)]
    return {"name": "Covered Market Hall (Los Pasar)", "extras": extras, "footprint": [8, 12], "height_m": 9.0, "floors": "1, open timber arcade",
            "parts": [{"id": "hall", "W": 8, "D": 12, "floors": 1, "roof": "8x12", "ridge": "y", "corner": "wood", "core": False, "roof_variant": "dark",
                       "facades": {"front": ["AAAA"], "back": ["AAAA"], "right": ["AAAAAA"], "left": ["AAAAAA"]}}]}


def tea_house():
    ex = [{"asset": "MV-Floor_WoodDark", "pos": [x, -4, 3.0]} for x in (-2, 0, 2)]                     # veranda deck, 6 x 2 m
    ex += [{"asset": "MV-Balcony_Simple_Straight", "pos": [x, -4, 3.0]} for x in (-2, 0, 2)]           # front rail
    ex += [{"asset": "MV-Balcony_Simple_Straight", "pos": [2, -4, 3.0], "rz": 90}, {"asset": "MV-Balcony_Simple_Straight", "pos": [-2, -4, 3.0], "rz": -90}]  # end rails
    ex += [{"asset": "MV-Corner_Exterior_Wood", "pos": [x, -4.9, 0]} for x in (-2.9, -1.0, 1.0, 2.9)]  # posts carry the deck to the ground
    ex += [tsign(3.05, -1.0, 3.25, "Cup", rz=90), {"asset": "AV-mdvl_village_sign_inn_01", "pos": [0, -4.95, 2.95], "rz": 90},
           {"asset": "FP-Bench", "pos": [-1.9, -3.5, 0]}, chimney(6, 6, 1.3, 1.5, 1.8), wbox(3.03, 1.0, 4.09, 90), wbox(-3.03, 1.0, 1.09, -90), vine(-3.04, -1.2, 5.3, -90)]
    return {"name": "Tea House (Rumah Teh)", "footprint": [6, 6], "front_extra": 2, "height_m": 10.9, "floors": "2, with a post-supported veranda and balcony",
            "parts": [{"id": "body", "W": 6, "D": 6, "floors": 2, "roof": "6x6", "ridge": "y", "corner": "wood",
                       "facades": {"front": ["FOF", "ROR"], "right": ["PFP", "PRP"], "back": ["PPP", "PTP"], "left": ["PFP", "PRP"]}}],
            "extras": ex}


ARCHETYPES = {
    "A01": exchange_hall(),
    "A02": market_hall(),
    "A03": {"name": "Jettied Merchant Shophouse (gable to street)", "footprint": [6, 8], "height_m": 10.9, "floors": "2",
            "parts": [{"id": "body", "W": 6, "D": 8, "floors": 2, "roof": "6x8", "ridge": "y", "corner": "wood", "shutters": True, "jetty": 1,
                       "facades": {"front": ["FDF", "RGR"], "right": ["PFPP", "PRPR"], "back": ["PPP", "PTP"], "left": ["PPFP", "RPRP"]}}],
            # P1.2: the upper floor is jettied 1.12 m over the shopfront (Overhang modules), replacing the timber canopy
            "extras": [tsign(-2.55, -4.05, 2.97, "Loaf"), lantern(0.1, -4.1), wbox(-2, -5.15, 4.09), wbox(2, -5.15, 4.09), dormer(6, 6, 0.6, 1), chimney(6, 6, -1.4, 2.3, 1.9)]},
    "A03b": {"name": "Medium Merchant Shophouse (eaves to street)", "variant_of": "A03", "footprint": [8, 6], "height_m": 10.9, "floors": "2",
             "parts": [{"id": "body", "W": 8, "D": 6, "floors": 2, "roof": "6x8", "ridge": "x", "corner": "wood", "shutters": True,
                        "facades": {"front": ["FDFG", "RRGR"], "right": ["PFP", "PTP"], "back": ["PPPP", "PRRP"], "left": ["PPP", "PTP"]}}],
             "extras": pentice(8, 6) + [tsign(-3.55, -3.05, 5.2, "Loaf"), lantern(-0.85, -3.1), wbox(-3, -3.03, 4.09), wbox(3, -3.03, 4.09),
                        dormer(6, 6, -2.0, -1, ridge="x"), dormer(6, 6, 2.0, -1, ridge="x"), chimney(6, 6, 3.0, 1.2, 1.7)]},
    # P1.3: shallow two-storey house, 8 m frontage and only 4 m deep, for plots that back onto a lane (keeps the lane's camera line open)
    "A03c": {"name": "Shallow Merchant House (eaves to street)", "variant_of": "A03b", "footprint": [8, 4], "height_m": 9.7, "floors": "2",
             "parts": [{"id": "body", "W": 8, "D": 4, "floors": 2, "roof": "4x8", "ridge": "x", "corner": "wood", "shutters": True,
                        "facades": {"front": ["FDFG", "RRGR"], "right": ["PP", "PT"], "back": ["PPPP", "PRRP"], "left": ["PP", "PT"]}}],
             "extras": pentice(8, 4) + [tsign(-3.55, -2.05, 5.2, "Scroll"), lantern(-0.85, -2.1), wbox(-3, -2.03, 4.09), wbox(3, -2.03, 4.09), chimney(4, 6, 3.0, 0.8, 0.8)]},
    "A04": {"name": "Compact Shop (gable to street)", "footprint": [4, 6], "height_m": 6.7, "floors": "1",
            "parts": [{"id": "body", "W": 4, "D": 6, "floors": 1, "roof": "4x6", "ridge": "y", "corner": "wood", "shutters": True,
                       "facades": {"front": ["DF"], "right": ["PFP"], "back": ["PP"], "left": ["PGP"]}}],
            "extras": [awning(-1, -3.03, 3.08, "burgundy"), awning(1, -3.03, 3.08, "burgundy"), lantern(0.1, -3.1), tsign(1.45, -3.05, 4.75, "Crate")]},
    "A04b": {"name": "Compact Shop (eaves to street)", "variant_of": "A04", "footprint": [6, 4], "height_m": 6.7, "floors": "1",
             "parts": [{"id": "body", "W": 6, "D": 4, "floors": 1, "roof": "4x6", "ridge": "x", "corner": "wood", "shutters": True,
                        "facades": {"front": ["FDF"], "right": ["PP"], "back": ["PGP"], "left": ["PP"]}}],
             "extras": [awning(-2, -2.03, 3.08, "blue"), awning(0, -2.03, 3.08, "blue"), awning(2, -2.03, 3.08, "blue"), tsign(-2.9, -2.05, 4.3, "Jar"), lantern(1.15, -2.1), vine(3.04, 0.3, 4.6, 90)]},
    "A05": {"name": "Corner Commercial Building", "footprint": [8, 8], "height_m": 12.0, "floors": "2, stone ground floor, two active fronts",
            "parts": [{"id": "body", "W": 8, "D": 8, "floors": 2, "roof": "8x8", "ridge": "y", "corner": ["brick", "wood"],
                       "facades": {"front": ["sosr", "RGGR"], "right": ["rsos", "RGGR"], "back": ["SSSS", "PTTP"], "left": ["SsSS", "PRRP"]}}],
            "extras": [lantern(-0.85, -4.1), lantern(4.1, 2.15, rz=90), tsign(-3.3, -4.05, 3.1, "Coin"), tsign(4.05, -3.3, 3.1, "Coin", rz=90),
                       wbox(-3, -4.03, 4.09), wbox(3, -4.03, 4.09), dormer(8, 6, -1.0, 1, 1.2), chimney(8, 6, -1.6, 2.0, 2.1)]},
    "A06": {"name": "Artisan Workshop", "footprint": [6, 6], "height_m": 7.9, "floors": "1, stone",
            "parts": [{"id": "body", "W": 6, "D": 6, "floors": 1, "roof": "6x6", "ridge": "y", "corner": "brick",
                       "facades": {"front": ["sos"], "right": ["SsS"], "back": ["SSS"], "left": ["SSs"]}}],
            "extras": [lantern(1.15, -3.1), tsign(-2.55, -3.05, 3.05, "Hammer"), vine(3.04, 1.0, 2.9, 90), chimney(6, 3, -1.3, 1.2, 1.8, "MV-Prop_Chimney"),
                       {"asset": "FP-Workbench", "pos": [-2.0, -4.3, 0]}, {"asset": "FP-Anvil_Log", "pos": [2.3, -4.2, 0]},
                       {"asset": "FP-WeaponStand", "pos": [3.9, -2.2, 0], "rz": 90}, {"asset": "FP-Barrel", "pos": [-3.6, -2.4, 0]}]},
    "A07": {"name": "Warehouse (Gudang Niaga)", "footprint": [8, 14], "height_m": 12.0, "floors": "2, stone ground floor",
            "parts": [{"id": "body", "W": 8, "D": 14, "floors": 2, "roof": "8x14", "ridge": "y", "corner": ["brick", "wood"], "roof_variant": "dark",
                       "facades": {"front": ["SooS", "PGGP"], "right": ["SSsSsSS", "PPTPTPP"], "back": ["SSSS", "PGGP"], "left": ["SSsSsSS", "PPTPTPP"]}}],
            "extras": [lantern(-2.9, -7.1), lantern(2.9, -7.1), emblem(0, -7.12, 8.3, 1.2), vine(-4.04, 2.0, 5.4, -90, 5), vine(-4.04, -3.5, 5.6, -90),
                       dormer(8, 6, -3.5, 1, 1.2), dormer(8, 6, 3.5, 1, 1.2), dormer(8, 6, 0, -1, 1.2),
                       {"asset": "MV-Prop_Wagon", "pos": [6.2, -5.0, 0], "rz": 20},
                       {"asset": "MV-Prop_Crate", "pos": [-5.0, -6.0, 0]}, {"asset": "MV-Prop_Crate", "pos": [-5.1, -4.8, 0], "rz": 15},
                       {"asset": "MV-Prop_Crate", "pos": [-5.0, -5.4, 1.06], "rz": 30}, {"asset": "FP-Barrel", "pos": [-4.9, -3.6, 0]},
                       {"asset": "FP-Crate_Wooden", "pos": [5.0, -7.6, 0]}, {"asset": "FP-Barrel", "pos": [4.9, -6.6, 0]}]},
    "A08": tea_house(),
    # P1.4 new archetypes ------------------------------------------------------------------------------
    "A09": {"name": "Merchants' Inn (Penginapan Saudagar)", "footprint": [10, 8], "front_extra": 2, "height_m": 12.0, "floors": "2, stone ground floor, balcony on posts",
            "parts": [{"id": "body", "W": 10, "D": 8, "floors": 2, "roof": "8x10", "ridge": "x", "corner": ["brick", "wood"],
                       "facades": {"front": ["srors", "RORGR"], "right": ["SsSS", "PRRP"], "back": ["SSsSS", "PTPTP"], "left": ["SSsS", "PRRP"]}}],
            "extras": [{"asset": "MV-Floor_WoodDark", "pos": [x, -5, 3.0]} for x in (-2, 0, 2)] + [{"asset": "MV-Balcony_Simple_Straight", "pos": [x, -5, 3.0]} for x in (-2, 0, 2)]
            + [{"asset": "MV-Balcony_Simple_Straight", "pos": [2, -5, 3.0], "rz": 90}, {"asset": "MV-Balcony_Simple_Straight", "pos": [-2, -5, 3.0], "rz": -90}]
            + [{"asset": "MV-Corner_Exterior_Wood", "pos": [x, -5.9, 0]} for x in (-2.9, -1.0, 1.0, 2.9)]
            + [tsign(-4.5, -4.05, 3.15, "Cup"), {"asset": "AV-mdvl_village_sign_inn_01", "pos": [0, -5.95, 2.95], "rz": 90}, lantern(-3.2, -4.1), lantern(3.2, -4.1),
               wbox(-4, -4.03, 4.09), wbox(4, -4.03, 4.09), dormer(8, 6, -2.5, -1, 1.2, ridge="x"), dormer(8, 6, 2.5, -1, 1.2, ridge="x"),
               chimney(8, 6, 4.0, 1.4, 1.4), chimney(8, 6, -4.0, 1.4, 1.4, "MV-Prop_Chimney"), {"asset": "FP-Bench", "pos": [3.6, -4.6, 0]}, {"asset": "SY-keg01", "pos": [-3.9, -4.7, 0]}]},
}


def tower_house(mirror=False):
    """A11 / A11m: stone-based corner house with a three-storey corner turret standing 1 m proud of both street fronts.
    mirror=False puts the turret at the front-right corner, mirror=True at the front-left."""
    k = -1 if mirror else 1
    body = {"id": "body", "W": 8, "D": 8, "floors": 2, "roof": "8x8", "ridge": "y", "corner": ["brick", "wood"], "skip_corners": [[k, -1]],
            "facades": {"front": ["sosr" if not mirror else "rsos", "RGGR"], "right": ["rsSs", "RGGR"] if not mirror else ["SsSS", "PRRP"],
                        "back": ["SSSS", "PTTP"], "left": ["SsSS", "PRRP"] if not mirror else ["sSsr", "RGGR"]}}
    vis, hid = (["Ss", "PR", "RR"], ["XX", "XX", "PP"])
    tower = {"id": "turret", "W": 4, "D": 4, "floors": 3, "tower_roof": True, "offset": [3 * k, -3, 0], "corner": ["brick", "wood", "wood"], "core_inset": 0.4,
             "facades": {"front": vis, "right": vis if not mirror else hid, "left": hid if not mirror else vis, "back": hid}}
    ex = [lantern(-0.85 * k, -4.1), tsign(-3.3 * k, -4.05, 3.1, "Coin"), wbox(-3 * k, -4.03, 4.09), dormer(8, 6, 1.0, -k, 1.2), chimney(8, 6, -1.6 * k, 2.0, 2.1)]
    return {"name": "Corner Tower House" + (" (mirrored)" if mirror else ""), "footprint": [8, 8], "height_m": 15.8, "floors": "2, stone ground floor, three-storey corner turret",
            "parts": [body, tower], "extras": ex}


ARCHETYPES["A11"] = tower_house(False)
ARCHETYPES["A11m"] = tower_house(True)


def awning_row(kit, colour):
    """A10: a market awning row, 8 m long. Four striped cloth bays (custom) on timber posts (downloaded, stretched in height),
    counters and a table beneath, goods of one trade. Customers stand on the -y side."""
    ex = [{"asset": "MV-Corner_Exterior_Wood", "pos": [x, -0.75, 0], "scale": [1, 1, 0.82]} for x in (-4, 0, 4)]
    ex += [{"asset": "MV-Corner_Exterior_Wood", "pos": [x, 0.75, 0], "scale": [1, 1, 1.07]} for x in (-4, 0, 4)]
    ex += [awning(x, 0.78, 3.2, colour) for x in (-3, -1, 1, 3)]
    ex += [{"asset": "SY-counter_M", "pos": [-3.7, 0.05, 0]}, {"asset": "FP-Table_Large", "pos": [0, 0.1, 0]}, {"asset": "SY-counter_M", "pos": [2.2, 0.05, 0]}]
    g = lambda a, x, y, z, rz=0, sc=1.0: {"asset": a, "pos": [x, y, z], "rz": rz, "scale": sc}
    if kit == "provisions":
        ex += [g("AV-mdvl_food_loaf_01", -3.3, 0.0, 1.16), g("SY-basket-of-pastries", -2.6, 0.05, 1.16), g("AV-mdvl_food_cheese_wheel_01", -0.8, 0.1, 0.82), g("FP-FarmCrate_Apple", 0.1, 0.1, 0.82),
               g("AV-mdvl_food_cabbage_01", 0.9, 0.0, 0.82), g("AV-mdvl_food_fish_01", 2.6, 0.0, 1.16, 20), g("AV-mdvl_food_scales_01", 3.3, 0.05, 1.16), g("AV-mdvl_food_grain_sack_01", 1.6, 0.95, 0), g("SY-keg01", -1.6, 0.95, 0)]
    else:
        ex += [g("FP-Vase_2", -3.3, 0.0, 1.16), g("FP-Pot_1", -2.6, 0.05, 1.16), g("FP-BookGroup_Medium_1", -0.8, 0.1, 0.82, 90), g("FP-Scroll_1", 0.0, 0.1, 0.82), g("FP-Coin_Pile", 0.8, 0.05, 0.82),
               g("FP-Potion_1", 2.6, 0.0, 1.16), g("FP-SmallBottles_1", 3.2, 0.05, 1.16), g("FP-Crate_Wooden", 1.6, 0.95, 0, 10), g("FP-Vase_4", -1.6, 0.95, 0, 0, 1.3)]
    return {"name": f"Market Awning Row ({kit})", "footprint": [8, 2], "height_m": 3.3, "floors": "open stall row", "parts": [], "extras": ex}


ROW_KITS = {"provisions": awning_row("provisions", "blue"), "crafts": awning_row("crafts", "burgundy")}


def terrace():
    """Civic terrace (Pelataran Bursa): local origin = terrace centre. Deck tiles come from PAVING (+1.0 m); this adds the
    12 m flight of steps on the south side, the stone skirt and the balustrade either side of the steps."""
    side = "MV-Stairs_Exterior_SingleSide"
    ex = [{"asset": f"MV-Stairs_Exterior_{a}", "pos": [-5 + 2 * i, -7, 0]} for i, a in enumerate(["Straight_L"] + ["Straight_Center"] * 4 + ["Straight_R"])]
    ex += [{"asset": side, "pos": [cx, -5, 0], "rz": 90} for cx in range(-13, 14, 2) if abs(cx) > 5]   # none behind the steps: the top riser is the deck edge
    ex += [{"asset": side, "pos": [s * 13, cy, 0], "rz": 0 if s < 0 else 180} for s in (-1, 1) for cy in range(-5, 6, 2)]
    ex += [{"asset": "MV-Balcony_Cross_Straight", "pos": [cx, -5, 1.0]} for cx in (-13, -11, -9, -7, 7, 9, 11, 13)]
    return {"name": "Civic terrace steps, skirt and balustrade", "footprint": [28, 12], "height_m": 2.1, "floors": "terrace", "parts": [], "extras": ex}


TERRACE = terrace()
TERRACE_POS = (0, 68, 0)


def lodge(x):
    return {"id": "lodge_w" if x < 0 else "lodge_e", "W": 2, "D": 4, "floors": 1, "roof": "2x4", "roof_asset": "MV-Roof_2x4_RoundTile",
            "gable_asset": "MV-Roof_Front_Brick2", "ridge": "y", "offset": [x, 0, 0], "corner": "wood", "core": False, "roof_variant": "dark",
            "facades": {"front": ["A"], "back": ["A"], "right": ["AA"], "left": ["AA"]}}


# P1.1 gateway: a split gate. Two roofed timber lodges flank a 4 m centre lane that is open to the sky, so the
# follow camera (6.6 m up) clears it. Guild seal on both south gables.
GATE = {"name": "Gerbang Niaga split gateway", "footprint": [8, 4], "height_m": 5.3, "floors": "two open lodges",
        "parts": [lodge(-3), lodge(3)],
        "extras": [emblem(-3, -2.12, 3.72, 0.8), emblem(3, -2.12, 3.72, 0.8), lantern(-4.0, -2.1, 2.2), lantern(4.0, -2.1, 2.2),
                   {"asset": "FP-Table_Large", "pos": [-3, 0.2, 0], "rz": 90, "scale": 0.6}, {"asset": "MV-Prop_Crate", "pos": [3, 0.6, 0], "rz": 10},
                   {"asset": "FP-Barrel", "pos": [3, -0.6, 0]}]}
GATE_POS = (0, 5.0, 0)   # P1.1 validation: moved 3.5 m south so the lodge roofs clear B04 and B07

# P1.1 market cross: guild standard at the bazaar centre, on the cross-passage between the two halls.
CROSS = {"name": "Tugu Timbangan market cross", "footprint": [2, 2], "height_m": 4.0, "floors": "monument", "parts": [],
         "extras": [{"asset": "MV-Stairs_Exterior_Platform", "pos": [0, 0, 0]}, {"asset": "MV-Corner_ExteriorWide_Wood", "pos": [0, 0, 1.0]},
                    emblem(0, -0.17, 3.3, 0.85), emblem(0, 0.17, 3.3, 0.85, rz=180), lantern(0.15, 0, 2.35, 90), lantern(-0.15, 0, 2.35, -90),
                    {"asset": "FP-Bag", "pos": [0.55, -1.3, 0]}, {"asset": "FP-Barrel", "pos": [-0.6, -1.35, 0]}, {"asset": "MV-Prop_Crate", "pos": [0.1, 1.55, 0], "rz": 15}]}
CROSS_POS = (0, 49, 0)

# ---------------------------------------------------------------------------------------------
# Town layout.  Plan coordinates: x = east, n = north (metres), origin = centre of the arrival court.
# Project / Three.js coordinates: (x, y, z) = (x, elevation, -n).   rz: 0 = front faces south,
# 90 = front faces east, -90 = front faces west, 180 = front faces north.
# ---------------------------------------------------------------------------------------------
# Selected layout: alternative B (22 buildings). Tuples: id, archetype, district, x, n, rz, label, options, status vs P1.2.
# Per-building additions keep reused archetypes from reading as copies: guild offices carry the seal, others a vine or a banner.
ADD = {"E04": [emblem(0, -4.12, 8.25, 1.2), {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [2.0, -4.13, 5.6]}],
       "B15": [emblem(-1.4, -4.12, 8.0, 1.1)],
       "E02": [{"asset": "MV-Prop_Crate", "pos": [3.0, -2.8, 0], "rz": 10}, {"asset": "FP-Bag", "pos": [3.6, -2.6, 0]}],
       "E05": [{"asset": "SY-keg01", "pos": [2.3, -2.7, 0]}, {"asset": "SY-menu-stand01", "pos": [-2.4, -2.9, 0]}],
       "E01": [{"asset": "FP-Barrel", "pos": [-2.5, -2.6, 0]}, {"asset": "FP-Crate_Wooden", "pos": [2.4, -2.8, 0], "rz": 15}]}
BUILDINGS = []
for _b in LY.ALT_D:
    _o = dict(_b[7] or {})
    if _b[0] in ADD:
        _o["add"] = ADD[_b[0]]
    BUILDINGS.append(_b[:7] + (_o or None, _b[8]))

# Stall kits. Local frame: customer side = -y. Flat tops: Quaternius stall and cart 0.83 m, Avramania stall 0.96 m,
# cafe counters 1.15 m, cafe table03 0.75 m (measured).  "rect" = nominal footprint (width, depth).
STALL_KITS = {
    "S01b": {"base": "FP-Stall_Empty@blue", "rect": [1.9, 1.0], "props": [["AV-mdvl_food_loaf_01", -0.5, 0.0, 0.84, 0], ["AV-mdvl_food_cheese_wheel_01", 0.05, 0.02, 0.84, 0], ["FP-FarmCrate_Apple", 0.55, 0.0, 0.84, 0],
                                                                          ["AV-mdvl_food_grain_sack_01", 1.45, 0.1, 0, 20], ["FP-Barrel_Apples", -1.45, 0.1, 0, 0]]},
    "S01g": {"base": "FP-Stall_Empty@burgundy", "rect": [1.9, 1.0], "props": [["FP-Vase_4", -0.5, 0.0, 0.84, 0], ["FP-Vase_2", 0.0, 0.03, 0.84, 0], ["FP-Pot_1", 0.5, 0.0, 0.84, 0], ["FP-Crate_Wooden", 1.5, 0.1, 0, 8], ["FP-Bag", -1.35, 0.15, 0, 0]]},
    "S01c": {"base": "FP-Stall_Empty@cream", "rect": [1.9, 1.0], "props": [["FP-Potion_1", -0.5, 0.0, 0.84, 0], ["FP-SmallBottles_1", 0.0, 0.0, 0.84, 0], ["FP-Bottle_1", 0.45, 0.05, 0.84, 0], ["FP-Barrel", 1.45, 0.1, 0, 0], ["FP-Bucket_Wooden_1", -1.3, -0.2, 0, 0]]},
    "S02c": {"base": "FP-Stall_Cart_Empty@cream", "rect": [3.1, 1.2], "props": [["MV-Prop_Crate", 1.6, 0.3, 0, 12], ["FP-Bag", -2.7, 0.2, 0, 0], ["FP-Vase_2", 0.2, 0.0, 0.84, 0], ["FP-Pot_1", -0.4, 0.05, 0.84, 0]]},
    "S02g": {"base": "FP-Stall_Cart_Empty@burgundy", "rect": [3.1, 1.2], "props": [["FP-Bag", 1.3, -0.2, 0, 0], ["FP-Barrel", 1.9, 0.5, 0, 0], ["FP-Bag", -2.7, 0.3, 0, 40], ["FP-Vase_4", 0.1, 0.0, 0.84, 0]]},
    "S03": {"base": "AV-mdvl_village_stall_01", "base_pos": [-1.0, -0.6, 0], "rect": [2.3, 1.2],
            "props": [["AV-mdvl_food_fish_01", -0.6, -0.05, 0.97, 15], ["AV-mdvl_food_ham_01", -0.05, 0.0, 0.97, 80], ["AV-mdvl_food_cabbage_01", 0.5, -0.1, 0.97, 0], ["AV-mdvl_food_cabbage_01", 0.72, 0.12, 0.97, 60],
                      ["SY-crate02", 1.6, 0.0, 0, 0], ["AV-mdvl_food_produce_crate_01", -1.55, 0.1, 0, 15]]},
    "S04": {"base": "SY-counter_L", "base_pos": [-1.5, 0.05, 0], "rect": [3.2, 1.0],
            "props": [["SY-counter_M", 0.0, 0.05, 0, 0], ["SY-basket-of-pastries", -0.9, 0.0, 1.16, 0], ["SY-food-bread03", -0.2, -0.1, 1.16, 10], ["SY-food-bread01", 0.35, 0.05, 1.16, 0],
                      ["AV-mdvl_food_scales_01", 1.0, 0.0, 1.16, 0], ["SY-keg01", 2.0, 0.2, 0, 0]]},
    "S05": {"base": "SY-table03", "rect": [2.4, 1.2], "props": [["SY-table-cloth03", 0, 0, 0.76, 0], ["FP-Vase_2", -0.7, 0.0, 0.78, 0], ["FP-Chalice", -0.2, 0.05, 0.78, 0], ["FP-Coin_Pile", 0.25, 0.0, 0.78, 0],
                                                                 ["FP-Scroll_1", 0.7, 0.05, 0.78, 30], ["FP-Crate_Wooden", 1.6, 0.1, 0, 12]]},
}
# Four free stalls plus four 8 m awning rows (16 bays) lining the central market street.
STALLS = list(LY.STALLS)
ROWS = list(LY.ROWS)
STALL_KITS_EXTRA = {}

BRICK, RED, COBBLE = "MV-Floor_Brick", "MV-Floor_RedBrick", "MV-Floor_UnevenBrick"
PAVING = list(LY.PAVE_D)
YARDS = list(LY.YARDS_D)
RESERVED = list(LY.RESERVED)
CLEAR = [  # corridors that must stay free of nominal building, stall and awning-row footprints
    ("Merchant street clear width 8 m", -4, 4, 10.6, 36), ("Market street west of the cross", -4.3, -1.2, 36, 59), ("Market street east of the cross", 1.2, 4.3, 36, 59),
    ("Artisan lane 4 m", -18, -14.2, 6, 36), ("Warehouse lane 4 m", 14, 18, 6, 36), ("Cross street west", -14, -5, 19, 22), ("Cross street east 4 m", 5, 14, 18, 22),
    ("Terrace steps and hall approach", -6, 6, 60, 72), ("Cross-passage west of the cross", -8.9, -1.2, 48.1, 49.9), ("Cross-passage east of the cross", 1.2, 8.9, 48.1, 49.9),
    ("Gateway centre lane 4 m", -2, 2, 2.5, 7.5), ("Tea lane 4 m", 22, 30, 56, 60), ("Service court centre", 18, 32, 18, 22), ("Market west side lane", -20.4, -18, 40, 60), ("Market east side lane", 18, 21.5, 40, 60),
]
NODES, EDGES = dict(LY.ND), list(LY.ED)


def lamp(x, n, rz):
    """Street lamp: a 3 m timber post stretched 1.3x in height (disclosed non-uniform scale) with a bracket lantern at 2.45 m."""
    return [["MV-Corner_Exterior_Wood", x, n, 0, 0, [1, 1, 1.3]], ["FP-Lantern_Wall", x, n, 2.45, rz, 1]]


def standard(x, n, rz, cloth):
    """District standard: 4.8 m post (1.6x height) with one hanging banner; marks the entrance to a lane."""
    return [["MV-Corner_Exterior_Wood", x, n, 0, 0, [1, 1, 1.6]], [cloth, x, n, 3.9, rz, 1]]


# Street dressing and vegetation: [asset, x, n, z, rz, scale]
F = "MV-Prop_WoodenFence_Single"


def tlamp(x, n, rz, z=1.0):
    """Lamp standing on the raised terrace."""
    return [["MV-Corner_Exterior_Wood", x, n, z, 0, [1, 1, 1.3]], ["FP-Lantern_Wall", x, n, z + 2.45, rz, 1]]


DRESSING = (
    # merchant street: lamps beside the two gate arches; a line of pennants runs between them across the street
    sum([lamp(x, n, 180) for x, n in ((-4.7, 31), (4.7, 29))], []) + lamp(13.2, 16.7, 180)
    + [["MV-Wall_Arch", -5.3, 31.2, 0, 90, 1], ["MV-Wall_Arch", 5.3, 29.3, 0, 90, 1], ["MV-Prop_Vine1", -5.15, 31.2, 3.25, 90, 1],
       ["CUS-Bunting_10", 0, 30.0, 3.86, -12.0, [0.961, 1, 1]], ["CUS-PavingSeal", 0, 20, 0, 0, 1]]
    + sum([lamp(x, n, rz) for x, n, rz in ((-21.3, 37.2, 90), (21.3, 37.2, -90), (-9.4, -7.4, 180), (9.4, -7.4, 180), (31, 23.3, 180), (28.6, 60.7, 180), (30.6, 51.4, 0))], [])
    + sum([lamp(-13.6, n, -90) for n in (24, 29, 35)], []) + sum([lamp(13.6, n, 90) for n in (23.2, 27.6)], [])
    + standard(-18.3, 6.7, 90, "FP-Banner_1@cream") + standard(18.3, 6.7, -90, "FP-Banner_2@burgundy")
    # bazaar: two lines of pennants from hall gable to hall gable over the market street
    + [["CUS-Bunting_18", 0, 44.25, 6.6, 0, 1], ["CUS-Bunting_18", 0, 55.75, 6.6, 0, 1]]
    # civic terrace (+1.0 m): guild standards and lamps at the head of the steps, benches, planting, the seal in the paving
    + [["MV-Corner_Exterior_Wood", x, 62.6, 1.0, 0, [1, 1, 1.6]] for x in (-6.9, 6.9)] + [["FP-Banner_2@burgundy", x, 62.6, 4.9, rz, 1] for x, rz in ((-6.9, 90), (6.9, -90))]
    + tlamp(-12.6, 73.2, 0) + tlamp(12.6, 73.2, 0)
    + [["FP-Bench", -9.5, 70.4, 1.0, 0, 1], ["FP-Bench", 9.5, 70.4, 1.0, 0, 1], ["CUS-PavingSeal", 0, 66.6, 1.0, 0, 1]]
    + [["SN-Bush_Common_Flowers", x, n, 1.0, rz, s] for x, n, rz, s in ((-12.4, 72.6, 0, 0.9), (12.4, 72.6, 30, 0.9), (-12.6, 67.0, 80, 0.8), (12.6, 67.0, 10, 0.8))]
    # yard fences along the lanes, terrace rails
    + [[F, -13.85, n, 0, 90, 1] for n in (23, 25, 27, 33)] + [[F, 13.85, n, 0, 90, 1] for n in (25, 27)]
    + [[F, 18.15, n, 0, 90, 1] for n in (33, 35)] + [[F, x, 36.15, 0, 0, 1] for x in (19.2, 21.2, 23.2, 25.2)]
    + [[F, 42, n, 0, 90, 1] for n in (53, 55, 57, 59, 61)] + [[F, x, 52, 0, 0, 1] for x in (31, 33, 35, 37, 39, 41)]
    + [["FP-Bench", -8.6, -5.6, 0, 90, 1], ["FP-Bench", 33, 53, 0, 0, 1], ["FP-Bench", 39.5, 53, 0, 0, 1],
       # tea terrace (cafe furniture): two laid tables beside the route across the terrace
       ["SY-table02", 40.0, 55.6, 0, 0, 1], ["SY-table-cloth02", 40.0, 55.6, 0.82, 0, 1], ["SY-chair01", 38.8, 55.6, 0.46, 90, 1], ["SY-chair01", 41.2, 55.6, 0.46, -90, 1],
       ["SY-stool", 40.0, 54.4, 0, 0, 1], ["SY-mug01", 39.7, 55.5, 0.84, 0, 1], ["SY-mug02", 40.3, 55.75, 0.84, 40, 1], ["SY-pitcher", 40.05, 55.4, 0.84, 0, 1],
       ["SY-table01", 33.0, 54.8, 0, 0, 1], ["SY-table-cloth01", 33.0, 54.8, 0.82, 0, 1], ["SY-stool", 32.1, 54.8, 0, 0, 1], ["SY-stool", 33.9, 54.8, 0, 0, 1],
       ["SY-mug03", 32.9, 54.7, 0.84, 0, 1], ["SY-platter-of-pie", 33.2, 54.95, 0.84, 0, 1], ["SY-keg02", 41.3, 60.4, 0, 0, 1],
       # arrival court
       ["MV-Prop_Wagon", 6.2, -5.2, 0, 110, 1], ["FP-Crate_Wooden", 4.4, -6.3, 0, 10, 1], ["FP-Barrel", -6.8, -6.6, 0, 0, 1], ["FP-Bag", -6.0, -6.8, 0, 30, 1],
       # shopfront staging inside the 1 m frontage strip, junction pocket court
       ["FP-Barrel", -4.6, 23.4, 0, 0, 1], ["MV-Prop_Crate", -4.6, 28.2, 0, 8, 1], ["FP-Bag", -4.5, 34.9, 0, 0, 1],
       ["FP-Barrel", 4.6, 11.2, 0, 0, 1], ["FP-Bench", 4.45, 25, 0, 90, 1], ["MV-Prop_Crate", 4.5, 31.6, 0, 20, 1], ["FP-Bench", 9.0, 16.7, 0, 0, 1], ["FP-Barrel", 11.2, 16.7, 0, 0, 1],
       # artisan workyard at the lane's bazaar end: well, bench and anvil
       ["AV-mdvl_village_well_01", -22.6, 34.7, 0, 0, 1], ["FP-Workbench", -22.7, 32.9, 0, 0, 1], ["FP-Anvil_Log", -20.9, 32.8, 0, 0, 1], ["FP-Barrel", -23.5, 33.7, 0, 0, 1],
       # west yards and east service yard
       ["MV-Prop_Crate", -12.4, 23.4, 0, 0, 1], ["FP-Bucket_Wooden_1", -12.6, 28.4, 0, 0, 1], ["FP-Barrel", -12.5, 33.4, 0, 0, 1],
       ["MV-Prop_Wagon", 11.5, 24.6, 0, 80, 1], ["MV-Prop_Crate", 12.6, 27.2, 0, 15, 1], ["FP-Barrel", 10.3, 27.4, 0, 0, 1],
       # service court (Pelataran Gudang)
       ["MV-Prop_Crate", 27.0, 17.3, 0, 0, 1], ["MV-Prop_Crate", 28.2, 17.4, 0, 25, 1], ["MV-Prop_Crate", 27.5, 17.35, 1.06, 40, 1], ["FP-Barrel", 29.5, 17.3, 0, 0, 1],
       ["FP-Barrel", 30.4, 17.5, 0, 0, 1], ["MV-Prop_Wagon", 29.6, 22.2, 0, 15, 1], ["FP-Bag", 27.4, 22.9, 0, 0, 1], ["FP-Bag", 27.9, 23.3, 0, 60, 1], ["FP-Crate_Wooden", 20.0, 23.2, 0, 5, 1]]
    + [[f"SN-CommonTree_{k}", x, n, 0, rz, s] for k, x, n, rz, s in (
        (3, -12.5, -6.5, 0, 0.95), (3, 19, -7, 40, 0.9), (3, -22, -9, 0, 1.0), (3, 22, -10, 90, 1.0), (3, -27.5, 3, 45, 1.05), (3, -28.8, 19, 0, 1.0), (3, -28.4, 25.5, 50, 0.95),
        (3, -33.5, 36.5, 90, 1.05), (1, -34, 53.5, 10, 1.1), (3, -29, 64, 130, 1.0), (3, -27, 76, 30, 1.1), (3, -19, 88, 20, 1.05), (1, 19, 88, 200, 1.05), (3, -10, 95, 70, 1.1),
        (3, 10, 95.5, 110, 1.1), (1, 0, 96, 0, 1.15), (3, 27.5, 78, 170, 1.05), (3, 36, 5, 0, 1.05), (3, 35.5, 21, 60, 1.0), (3, 30.5, 31.5, 100, 0.95), (3, 31.5, 41.5, 20, 0.95),
        (3, 22.3, 34.2, 300, 0.75), (3, -12.4, 26.2, 80, 0.7), (3, 30, 5, 210, 0.9))]
    + [["SN-TwistedTree_2", 44.5, 68, 0, 30, 0.75]]
    + [["SN-Bush_Common_Flowers", x, n, 0, rz, s] for x, n, rz, s in ((31.0, 64.6, 0, 0.9), (42.2, 63.6, 60, 0.9), (-15.5, 0.9, 0, 0.8), (-32.5, 44, 0, 0.9), (20.5, 33.2, 0, 0.7))]
    + [["SN-Flower_3_Group", x, n, 0, rz, 0.55] for x, n, rz in ((31.5, 51.3, 0), (40.5, 51.3, 50))]
    + [["SN-Fern_1", x, n, 0, rz, 0.8] for x, n, rz in ((-12.3, 34.8, 0), (10.6, 22.8, 90), (-24.6, 36.6, 0), (43.2, 55, 0), (25.4, 33.0, 30))]
    + [["SN-Rock_Medium_1", 44, 51, 0, 20, 0.6], ["SN-Rock_Medium_2", -30.5, 31, 0, 0, 0.7]]
)
VIEWS = {  # name: camera position (x, n, z), look-at, vertical fov, explorer position (x, n[, z]) or None.  A-F use the P1.3 cameras.
    "view-a-aerial": ((52, -66, 70), (5, 42, 2), 33, None),
    "view-b-merchant-street": ((0, 12.2, 6.6), (0, 24, 1.25), 60, (0, 24)),
    "view-b2-merchant-street-eye": ((0.9, 10.4, 1.65), (-0.2, 40, 4.6), 64, (-1.4, 16.5)),
    "view-c-central-bazaar": ((-2.5, 35.4, 8.0), (1.5, 56, 2.5), 62, (1.6, 44.6)),
    "view-c2-bazaar-eye": ((1.6, 37.2, 1.65), (-0.6, 62, 5.4), 66, (-2.0, 43.0)),
    "view-d-exchange-court": ((-1.8, 57.6, 1.65), (0.4, 80, 9.2), 64, (2.6, 63.5, 1.0)),
    "view-e-service-court": ((3.2, 19.4, 1.65), (27, 20.3, 3.6), 64, (9.5, 20.7)),
    "view-e2-artisan-lane": ((-16, 4.2, 6.6), (-16, 16, 1.25), 60, (-16, 16)),
    "view-f-tea-route": ((20.4, 57.6, 1.65), (37, 60.5, 3.2), 64, (27.2, 57.4)),
    "view-g-bazaar-from-terrace": ((0, 66.4, 2.75), (0, 40, 1.6), 62, (-2.2, 57.4)),
}


def rect_of(b):
    """Axis-aligned bound of the building's nominal footprint (the footprint itself is LY.corners(b); it may be turned)."""
    return LY.bbox(b)


def door_point(b, out=1.5):
    return LY.door_point(b, out)


def box_poly(x0, x1, n0, n1):
    return [(x0, n0), (x1, n0), (x1, n1), (x0, n1)]


def placed_rect(x, n, rz, w, d):
    a = math.radians(rz); c, sn = math.cos(a), math.sin(a)
    return [(x + px * c - py * sn, n + px * sn + py * c) for px, py in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]


def stall_poly(st):
    _, kit, x, n, rz = st
    w, d = STALL_KITS[kit]["rect"]
    return placed_rect(x, n, rz, w, d)


def row_poly(r):
    return placed_rect(r[2], r[3], r[4], 8.2, 1.9)


def on_paving(px, pn):
    return any(p[1] <= px <= p[2] and p[3] <= pn <= p[4] for p in PAVING)


def checks():
    out, ok = [], True
    polys = {b[0]: LY.corners(b) for b in BUILDINGS}
    polys["G01w"] = box_poly(-4, -2, 3, 7); polys["G01e"] = box_poly(2, 4, 3, 7); polys["M01"] = box_poly(-1, 1, 48, 50)
    ids = list(polys)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if LY.overlap(polys[a], polys[b]):
                ok = False; out.append(f"FAIL overlap {a} {b}")
    movable = [(s[0], stall_poly(s)) for s in STALLS] + [(r[0], row_poly(r)) for r in ROWS]
    for name, *c in CLEAR:
        for k, pl in list(polys.items()) + movable:
            if LY.overlap(box_poly(*c), pl):
                ok = False; out.append(f"FAIL {k} blocks '{name}'")
    for k, pl in movable:
        for kb, pb in polys.items():
            if LY.overlap(pl, pb):
                ok = False; out.append(f"FAIL {k} overlaps {kb}")
    for b in BUILDINGS:
        px, pn = door_point(b)
        if not on_paving(px, pn):
            ok = False; out.append(f"FAIL {b[0]} entrance approach ({px},{pn}) is not on paving")
    for s in list(STALLS) + list(ROWS):
        if not on_paving(s[2], s[3]):
            ok = False; out.append(f"FAIL {s[0]} not on paving")
    adj = {k: set() for k in NODES}
    for a, b, _ in EDGES:
        adj[a].add(b); adj[b].add(a)
    seen, todo = {"N01"}, ["N01"]
    while todo:
        for nb in adj[todo.pop()]:
            if nb not in seen:
                seen.add(nb); todo.append(nb)
    if seen != set(NODES):
        ok = False; out.append(f"FAIL unreachable nodes {sorted(set(NODES) - seen)}")
    out.append(f"INFO walking graph: {len(NODES)} nodes, {len(EDGES)} edges, independent loops = {len(EDGES) - len(NODES) + 1}")
    xs = [v for pl in polys.values() for v, _ in pl] + [v for p in PAVING for v in p[1:3]]
    ns = [v for pl in polys.values() for _, v in pl] + [v for p in PAVING for v in p[3:5]]
    env = (round(min(xs), 2), round(max(xs), 2), round(min(ns), 2), round(max(ns), 2))
    out.append(f"INFO developed envelope (nominal) x {env[0]}..{env[1]} ({env[1] - env[0]:.1f} m), n {env[2]}..{env[3]} ({env[3] - env[2]:.1f} m)")
    return ok, out, env


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    ok, msgs, env = checks()
    print("\n".join(msgs)); print("NOMINAL SPATIAL CHECKS:", "PASS" if ok else "FAIL")
    arch = dict(ARCHETYPES); arch["GATE"] = GATE; arch["CROSS"] = CROSS; arch["A10p"] = ROW_KITS["provisions"]; arch["A10c"] = ROW_KITS["crafts"]; arch["TERRACE"] = TERRACE
    json.dump(arch, open(os.path.join(out, "archetypes.json"), "w"), indent=1)
    layout = {"revision": REVISION,
              "buildings": [dict(id=b[0], archetype=b[1], district=b[2], x=b[3], n=b[4], rz=b[5], label=b[6], opts=b[7] or {}, status=b[8], rect=rect_of(b),
                                 corners=[[round(v, 2) for v in c] for c in LY.corners(b)], door=door_point(b)) for b in BUILDINGS],
              "gate": GATE_POS, "cross": CROSS_POS, "terrace": TERRACE_POS, "stall_kits": STALL_KITS,
              "stalls": [dict(id=s[0], kit=s[1], x=s[2], n=s[3], rz=s[4], corners=[[round(v, 2) for v in c] for c in stall_poly(s)]) for s in STALLS],
              "rows": [dict(id=r[0], kit=r[1], x=r[2], n=r[3], rz=r[4], corners=[[round(v, 2) for v in c] for c in row_poly(r)]) for r in ROWS],
              "paving": PAVING, "yards": YARDS, "reserved": RESERVED, "clear": CLEAR, "dressing": DRESSING, "views": VIEWS, "nodes": NODES, "edges": EDGES,
              "envelope": env, "checks": msgs, "checks_pass": ok}
    json.dump(layout, open(os.path.join(out, "layout.json"), "w"), indent=1)
    print("wrote", out)
