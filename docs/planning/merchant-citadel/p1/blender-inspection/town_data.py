#!/usr/bin/env python3
"""Single source of truth for Merchant Citadel P1.2 (art-direction and asset-expansion revision of the approved P1.1): archetype assemblies and the measured town layout.

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

REVISION = "P1.2"
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
        {"id": "tower", "W": 4, "D": 4, "floors": 5, "floor_from": 3, "tower_roof": True, "roof_variant": "dark", "offset": [0, 0, z0], "corner": "wood",
         "facades": {"front": ["XX", "XX", "XX", "PP", "RR"], "right": ["XX", "XX", "XX", "TT", "RR"],
                     "back": ["XX", "XX", "XX", "PP", "RR"], "left": ["XX", "XX", "XX", "TT", "RR"]}},
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
    extras += [emblem(0, -6.12, z0 + 4.75, 1.45), emblem(0, -2.11, z0 + 10.5, 1.9), emblem(0, 2.11, z0 + 10.5, 1.9, rz=180)]
    extras += [{"asset": "FP-Banner_2_Cloth@burgundy", "pos": [x, -4.13, z0 + 5.95]} for x in (-5, -3, 3, 5)]
    extras += [lantern(-1.0, -4.1, z0 + 2.3), lantern(1.0, -4.1, z0 + 2.3)]
    return {"name": "Exchange Hall (Balai Niaga Awan)", "parts": parts, "extras": extras,
            "footprint": [28, 16], "height_m": 22.8, "floors": "2 storeys + central tower (walls above the roof on levels 4-5), gabled entrance porch, 1 m podium"}


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
    "A04": {"name": "Compact Shop (gable to street)", "footprint": [4, 6], "height_m": 6.7, "floors": "1",
            "parts": [{"id": "body", "W": 4, "D": 6, "floors": 1, "roof": "4x6", "ridge": "y", "corner": "wood", "shutters": True,
                       "facades": {"front": ["DF"], "right": ["PFP"], "back": ["PP"], "left": ["PGP"]}}],
            "extras": pentice(4, 6) + [lantern(0.1, -3.1), tsign(1.45, -3.05, 4.75, "Crate")]},
    "A04b": {"name": "Compact Shop (eaves to street)", "variant_of": "A04", "footprint": [6, 4], "height_m": 6.7, "floors": "1",
             "parts": [{"id": "body", "W": 6, "D": 4, "floors": 1, "roof": "4x6", "ridge": "x", "corner": "wood", "shutters": True,
                        "facades": {"front": ["FDF"], "right": ["PP"], "back": ["PGP"], "left": ["PP"]}}],
             "extras": [tsign(-2.55, -2.05, 3.05, "Jar"), lantern(1.15, -2.1), vine(3.04, 0.3, 2.9, 90)]},
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
}


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
S = lambda glyph, field="wood": {"sign": f"CUS-Sign_{glyph}_{field}"}
BUILDINGS = [
    # id, archetype, district, x, n, rz, label, options: sign = asset for the building's sign role, kit = dressing kit
    ("B01", "A01", "D5 Balai Niaga Awan", 0, 84, 0, "Exchange Hall", None),
    ("B02", "A02", "D3 Pasar Awan", -13, 50, 0, "Market Hall West (provisions)", {"kit": "provisions", "sign": "FP-Banner_1@blue"}),
    ("B03", "A02", "D3 Pasar Awan", 13, 50, 0, "Market Hall East (crafts and general trade)", {"kit": "crafts", "sign": "FP-Banner_1@burgundy"}),
    ("B04", "A05", "D2 Koridor Niaga", -9, 14, 0, "Gate Corner House (money changer)", S("Coin")),
    ("B05", "A03b", "D2 Koridor Niaga", -8, 25, 90, "Shophouse W1, eaves to street (baker)", S("Loaf")),
    ("B06", "A04", "D2 Koridor Niaga", -8, 33.5, 90, "Compact Shop W2 (dry goods)", S("Crate")),
    ("B07", "A03", "D2 Koridor Niaga", 9, 13, -90, "Jettied Shophouse E1 (map and book seller)", S("Scroll")),
    ("B08", "A04b", "D2 Koridor Niaga", 7, 22.5, -90, "Compact Shop E2, eaves to street (potter)", S("Jar")),
    ("B09", "A03", "D2 Koridor Niaga", 9, 32, -90, "Jettied Shophouse E3 (provisioner)", S("Loaf")),
    ("B10", "A06", "D6 Lorong Lentera", -25.5, 13, 90, "Workshop South (smith)", S("Hammer")),
    ("B11", "A04b", "D6 Lorong Lentera", -24.5, 22.5, 90, "Lane Shop, eaves to lane (potter's yard)", S("Jar")),
    ("B12", "A06", "D6 Lorong Lentera", -25.5, 31.5, 90, "Workshop North (joiner)", S("Hammer")),
    ("B13", "A07", "D7 Jalur Gudang", 29.5, 18, -90, "Guild Warehouse", None),
    ("B14", "A04", "D7 Jalur Gudang", 25.5, 29, -90, "Registry Office (guild)", S("Scroll", "burgundy")),
    ("B15", "A05", "D4 Pelataran Bursa", -22, 67, 90, "Court Corner House (assay office, guild)", S("Coin", "burgundy")),
    ("B16", "A03", "D4 Pelataran Bursa", 22, 67, -90, "Court Shophouse (chart maker)", S("Scroll")),
    ("B17", "A08", "D8 Tea Lookout", 40, 58, 0, "Tea House", S("Cup")),
]

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
# Twelve stalls in four quadrants around the market cross (count unchanged from the approved P1.1). West side = provisions
# (blue / cream / striped), east side = crafts (burgundy / cream). The bay at n = 49 is the hall-to-hall cross-passage.
STALLS = [("S%02d" % (i + 1),) + s for i, s in enumerate([
    ("S01b", -5.0, 40.5, 90), ("S03", -5.0, 44.5, 90), ("S04", -5.0, 53.5, 90), ("S01c", -5.0, 57.5, 90),
    ("S01g", 5.0, 40.5, -90), ("S02c", 5.0, 44.5, -90), ("S05", 5.0, 53.5, -90), ("S01g", 5.0, 57.5, -90),
    ("S03", -10.0, 38.5, 0), ("S05", 10.0, 38.5, 0), ("S01b", -12.0, 59.3, 0), ("S02g", 12.0, 59.3, 0)])]

BRICK, RED, COBBLE = "MV-Floor_Brick", "MV-Floor_RedBrick", "MV-Floor_UnevenBrick"
PAVING = [  # name, x0, x1, n0, n1, tile (2 m tiles; later rows overwrite earlier ones)
    ("D1 Arrival court", -10, 10, -8, 8, COBBLE), ("D1 Gate forecourt", -14, 14, 6, 10, COBBLE), ("D2 Merchant street", -6, 6, 8, 36, COBBLE),
    ("South cross lane W", -22, -10, 2, 6, COBBLE), ("South cross lane E", 10, 22, 2, 6, COBBLE),
    ("D6 Artisan lane (red brick)", -22, -18, 6, 36, RED), ("D7 Warehouse lane", 18, 22, 6, 36, COBBLE),
    ("D3 Bazaar plaza", -22, 22, 36, 62, COBBLE), ("Market Hall West floor", -18, -8, 44, 56, BRICK), ("Market Hall East floor", 8, 18, 44, 56, BRICK),
    ("Hall-to-hall cross-passage", -8, 8, 48, 50, BRICK), ("Guild way (axis band)", -2, 2, 0, 62, BRICK),
    ("D4 Civic court", -18, 18, 62, 74, BRICK), ("D8 Lookout path", 22, 34, 48, 52, COBBLE), ("D8 Lookout terrace (red brick)", 34, 46, 44, 54, RED), ("Tea house veranda floor", 36, 44, 54, 56, RED),
]
# Packed-earth back courts (terrain surface treatment, drawn as temporary planes; a P2 terrain material, not geometry).
YARDS = [("West back courts", -18, -10, 10, 36), ("East back courts", 10, 18, 10, 36)]
RESERVED = [("Future transport reservation (no construction in P1-P3)", -10, 10, -24, -8)]
CLEAR = [  # corridors that must stay free of nominal building and stall footprints
    ("Merchant street clear width 8 m", -4, 4, 10.6, 36), ("Guild way west of the cross", -4.3, -1.2, 36, 62), ("Guild way east of the cross", 1.2, 4.3, 36, 62),
    ("Artisan lane 4 m", -22, -18, 6, 36), ("Warehouse lane 4 m", 18, 22, 6, 36), ("Hall approach", -6, 6, 62, 72),
    ("Cross-passage west of the cross", -8.9, -1.2, 48.1, 49.9), ("Cross-passage east of the cross", 1.2, 8.9, 48.1, 49.9), ("Gateway centre lane 4 m", -2, 2, 2.5, 7.5),
]
NODES = {
    "N01": (0, 0, "Arrival court"), "N02": (0, 5.0, "Gateway centre lane"), "N03": (0, 22, "Merchant street mid"),
    "N04": (0, 36, "Bazaar south entrance"), "N05": (0, 45.5, "Bazaar, south of the market cross"), "N29": (2.7, 49, "Cross-passage east of the cross"),
    "N30": (-2.7, 49, "Cross-passage west of the cross"), "N27": (0, 52.5, "Bazaar, north of the market cross"), "N06": (0, 62, "Court south"),
    "N07": (0, 67, "Civic court centre"), "N08": (0, 75, "Exchange Hall podium, top of stairs (+1.0 m)"),
    "N09": (-20, 4, "Artisan lane south"), "N10": (-20, 22, "Artisan lane mid"), "N11": (-20, 38, "Bazaar south-west"),
    "N12": (20, 4, "Warehouse lane south"), "N13": (20, 18, "Warehouse door"), "N14": (20, 38, "Bazaar south-east"),
    "N15": (20, 50, "Bazaar east exit"), "N16": (40, 49, "Lookout terrace"), "N17": (40, 54.2, "Tea house veranda"),
    "N18": (-12, 42.5, "Market Hall West south arch"), "N31": (-12, 49, "Market Hall West interior"),
    "N19": (12, 42.5, "Market Hall East south arch"), "N32": (12, 49, "Market Hall East interior"),
    "N20": (0, -16, "Future transport reservation"), "N21": (-17, 67, "Court west / corner house"), "N22": (17, 67, "Court east / shophouse"),
    "N23": (-19.5, 58.5, "Bazaar north-west"), "N24": (19.5, 58.5, "Bazaar north-east"),
    "N25": (-15, 61.5, "Court south-west entrance"), "N26": (15, 61.5, "Court south-east entrance"),
}
EDGES = [("N20", "N01", "reserved link"), ("N01", "N02", "primary"), ("N02", "N03", "primary"), ("N03", "N04", "primary"), ("N04", "N05", "primary"),
         ("N05", "N29", "primary"), ("N29", "N27", "primary"), ("N05", "N30", "primary"), ("N30", "N27", "primary"),
         ("N27", "N06", "primary"), ("N06", "N07", "primary"), ("N07", "N08", "primary, stairs"),
         ("N01", "N09", "secondary"), ("N09", "N10", "secondary"), ("N10", "N11", "secondary"), ("N11", "N04", "secondary"),
         ("N11", "N18", "market"), ("N18", "N31", "market"), ("N31", "N30", "market"),
         ("N01", "N12", "service"), ("N12", "N13", "service"), ("N13", "N14", "service"), ("N14", "N04", "service"),
         ("N14", "N19", "market"), ("N19", "N32", "market"), ("N32", "N29", "market"),
         ("N14", "N15", "secondary"), ("N15", "N16", "scenic"), ("N16", "N17", "scenic"),
         ("N11", "N23", "secondary"), ("N23", "N25", "secondary"), ("N25", "N21", "secondary"), ("N25", "N06", "secondary"), ("N21", "N07", "secondary"),
         ("N15", "N24", "secondary"), ("N24", "N26", "secondary"), ("N26", "N22", "secondary"), ("N26", "N06", "secondary"), ("N22", "N07", "secondary")]


def lamp(x, n, rz):
    """Street lamp: a 3 m timber post stretched 1.3x in height (disclosed non-uniform scale) with a bracket lantern at 2.45 m."""
    return [["MV-Corner_Exterior_Wood", x, n, 0, 0, [1, 1, 1.3]], ["FP-Lantern_Wall", x, n, 2.45, rz, 1]]


def standard(x, n, rz, cloth):
    """District standard: 4.8 m post (1.6x height) with one hanging banner; marks the entrance to a lane."""
    return [["MV-Corner_Exterior_Wood", x, n, 0, 0, [1, 1, 1.6]], [cloth, x, n, 3.9, rz, 1]]


# Street dressing and vegetation: [asset, x, n, z, rz, scale]
DRESSING = (
    # merchant street lamps stand in the alley mouths, 0.7 m outside the 8 m clear width, arms along the frontage
    sum([lamp(x, n, 180) for x, n in ((-4.7, 19.5), (-4.7, 30.5), (4.7, 17.6), (4.7, 27.2))], [])
    + sum([lamp(x, n, rz) for x, n, rz in ((-21.3, 37, 90), (21.3, 37, -90), (-21.3, 61, 90), (21.3, 61, -90), (-17.4, 62.7, 90), (17.4, 62.7, -90),
                                         (-7.2, 73.2, 0), (7.2, 73.2, 0), (-9.4, -7.4, 180), (9.4, -7.4, 180), (33.5, 47.3, 0))], [])
    # D6 Lorong Lentera = lantern lane: a lamp every 6 m along the yard fence; D7 gets two
    + sum([lamp(-17.6, n, -90) for n in (9, 15, 21, 27, 33)], []) + sum([lamp(17.6, n, 90) for n in (10, 30)], [])
    + standard(-22.3, 6.6, 90, "FP-Banner_1@cream") + standard(-17.7, 35.4, -90, "FP-Banner_1@cream")
    + standard(22.3, 6.6, -90, "FP-Banner_2@burgundy") + standard(17.7, 35.4, 90, "FP-Banner_2@burgundy")
    # yard fences give the lanes a second edge and turn the leftover strips into back courts
    + [["MV-Prop_WoodenFence_Single", -17.85, n, 0, 90, 1] for n in (11, 13, 15, 17, 22, 24, 26, 28, 33)]
    + [["MV-Prop_WoodenFence_Single", 17.85, n, 0, 90, 1] for n in (11, 13, 15, 20.5, 22.5, 24.5, 30, 32, 34)]
    + [["MV-Prop_WoodenFence_Single", x, 9.9, 0, 0, 1] for x in (-16.8, -14.8, 14.8, 16.8)]
    + [["MV-Prop_WoodenFence_Single", 46, n, 0, 90, 1] for n in (45, 47, 49, 51, 53)]
    + [["MV-Prop_WoodenFence_Single", x, 44, 0, 0, 1] for x in (35, 37, 39, 41, 43, 45)]
    + [["FP-Bench", -8.5, -3, 0, 90, 1], ["FP-Bench", 8.5, -3, 0, 90, 1], ["FP-Bench", -11, 64.5, 0, 0, 1], ["FP-Bench", 11, 64.5, 0, 0, 1],
       ["FP-Bench", 38, 45, 0, 0, 1], ["FP-Bench", 43, 45, 0, 0, 1],
       # tea terrace (Syntaxes of Play cafe furniture): two laid tables, a menu stand at the terrace entrance, a keg by the door
       ["SY-table02", 43.2, 47.2, 0, 0, 1], ["SY-table-cloth02", 43.2, 47.2, 0.82, 0, 1], ["SY-chair01", 42.0, 47.2, 0.46, 90, 1], ["SY-chair01", 44.4, 47.2, 0.46, -90, 1],
       ["SY-stool", 43.2, 48.4, 0, 0, 1], ["SY-mug01", 42.9, 47.1, 0.84, 0, 1], ["SY-mug02", 43.5, 47.35, 0.84, 40, 1], ["SY-pitcher", 43.25, 47.0, 0.84, 0, 1],
       ["SY-table01", 37.3, 46.9, 0, 0, 1], ["SY-table-cloth01", 37.3, 46.9, 0.82, 0, 1], ["SY-stool", 36.4, 46.9, 0, 0, 1], ["SY-stool", 38.2, 46.9, 0, 0, 1],
       ["SY-mug03", 37.2, 46.8, 0.84, 0, 1], ["SY-platter-of-pie", 37.5, 47.05, 0.84, 0, 1], ["SY-menu-stand01", 34.7, 51.4, 0, 90, 1], ["SY-keg02", 44.6, 53.2, 0, 0, 1],
       # a well in the west back court and one flower-box planter pair at the court
       ["AV-mdvl_village_well_01", -14.4, 22.6, 0, 0, 1],
       # goods stacked at the four inner corners of the market halls (outside the arcades, clear of every walking edge)
       ["FP-Barrel", -8.3, 43.3, 0, 0, 1], ["AV-mdvl_food_grain_sack_01", -7.6, 43.7, 0, 30, 1], ["AV-mdvl_food_grain_sack_01", -8.1, 44.2, 0, 80, 1], ["SY-crate02", -7.4, 42.9, 0, 10, 1],
       ["SY-keg02", -8.2, 56.6, 0, 0, 1], ["FP-Barrel_Apples", -7.4, 56.9, 0, 0, 1], ["AV-mdvl_food_produce_crate_01", -7.6, 56.1, 0, 20, 1],
       ["MV-Prop_Crate", 8.3, 43.3, 0, 10, 1], ["MV-Prop_Crate", 8.2, 43.35, 1.06, 30, 1], ["FP-Crate_Wooden", 7.4, 43.8, 0, 0, 1], ["FP-Vase_2", 7.5, 42.9, 0, 0, 1.3],
       ["FP-Crate_Metal", 8.2, 56.6, 0, 0, 1], ["FP-Bag", 7.5, 56.9, 0, 20, 1], ["FP-Bag", 7.9, 56.0, 0, 70, 1], ["FP-Pot_1", 7.3, 56.2, 0, 0, 1.3],
       ["MV-Prop_Wagon", 6.5, -4.5, 0, 110, 1], ["FP-Crate_Wooden", 4.6, -5.6, 0, 10, 1], ["FP-Barrel", -6.8, -6.2, 0, 0, 1], ["FP-Bag", -6.0, -6.4, 0, 30, 1],
       # shopfront staging inside the 1 m frontage strip
       ["FP-Barrel", -4.6, 22.2, 0, 0, 1], ["MV-Prop_Crate", -4.6, 27.6, 0, 8, 1], ["FP-Bag", -4.5, 33.2, 0, 0, 1],
       ["FP-Barrel", 4.6, 11.2, 0, 0, 1], ["FP-Bench", 4.45, 22.5, 0, 90, 1], ["MV-Prop_Crate", 4.5, 30.3, 0, 20, 1],
       # back courts and yards
       ["MV-Prop_Crate", -15.2, 12.2, 0, 0, 1], ["FP-Barrel", -14.2, 12.6, 0, 0, 1], ["MV-Prop_Crate", -13.6, 26.6, 0, 30, 1], ["FP-Bucket_Wooden_1", -14.8, 23.2, 0, 0, 1],
       ["MV-Prop_Crate", 15.0, 11.8, 0, 0, 1], ["MV-Prop_Wagon", 13.3, 21.2, 0, 80, 1], ["FP-Barrel", 11.3, 24.3, 0, 0, 1], ["MV-Prop_Crate", 15.2, 31.0, 0, 15, 1],
       ["MV-Prop_Crate", 23.4, 24.6, 0, 0, 1], ["MV-Prop_Crate", 24.6, 24.9, 0, 25, 1], ["FP-Barrel", 23.3, 25.8, 0, 0, 1], ["FP-Crate_Wooden", 23.4, 11.6, 0, 5, 1]]
    + [[f"SN-CommonTree_{k}", x, n, 0, rz, s] for k, x, n, rz, s in (
        (3, -12.5, -6, 0, 1.0), (3, 12.5, -6, 40, 0.9), (3, -15.4, 14.6, 80, 0.8), (3, -14.6, 31.5, 10, 0.8), (3, 15.5, 14.2, 200, 0.8),
        (3, 14.2, 26.6, 60, 0.75), (3, 15.6, 33.2, 300, 0.8), (3, -24.5, 40.5, 0, 0.95), (1, -25, 53, 90, 1.0), (3, 25.5, 41, 30, 0.95),
        (1, 27, 57.5, 150, 1.0), (3, 30.5, 44.5, 20, 0.9), (3, 30, 55.5, 200, 0.9), (3, -19, 86, 20, 1.05), (1, 19, 86, 200, 1.05),
        (3, -10, 94, 70, 1.1), (3, 10, 94.5, 110, 1.1), (1, 0, 95, 0, 1.15), (3, -34, 10, 0, 1.1), (3, -35, 22, 50, 1.0), (3, -34, 33, 90, 1.1),
        (1, -33, 46, 10, 1.15), (3, -32, 58, 130, 1.1), (3, -31, 76, 30, 1.1), (3, 42, 9, 0, 1.1), (3, 43, 27, 60, 1.05), (3, 36, 37, 100, 1.0),
        (3, 36, 71, 40, 1.1), (1, 31, 80, 170, 1.1), (3, -22, -9, 0, 1.0), (3, 22, -9, 90, 1.0), (3, -29, 1, 45, 1.05), (3, 29, 1, 210, 1.05))]
    + [["SN-TwistedTree_2", 49, 64, 0, 30, 0.75]]
    + [["SN-Bush_Common_Flowers", x, n, 0, rz, s] for x, n, rz, s in (
        (-13.9, 19.6, 0, 1), (13.9, 17.6, 60, 1), (-12.4, 30.4, 20, 0.9), (12.4, 27.4, 100, 0.9), (-9.2, 72.8, 0, 1), (9.2, 72.8, 30, 1),
        (-12.6, 72.9, 80, 0.9), (12.6, 72.9, 10, 0.9), (35.2, 55.6, 0, 1), (45.2, 55.8, 60, 1), (-11, 70.4, 0, 1.1), (11, 70.4, 90, 1.1),
        (-15.5, 0.4, 0, 0.9), (15.5, 0.4, 0, 0.9), (-16, 20.5, 0, 0.9), (12, 20.3, 40, 0.8))]
    + [["SN-Flower_3_Group", x, n, 0, rz, 0.55] for x, n, rz in ((-12.4, 71.0, 0), (-9.6, 70.1, 60), (12.4, 71.0, 20), (9.6, 70.1, 100), (36, 43.2, 0), (44.5, 43.3, 50))]
    + [["SN-Fern_1", x, n, 0, rz, 0.8] for x, n, rz in ((-16.3, 16.8, 0), (16.4, 16.6, 90), (-23.5, 36.8, 0), (23.2, 33.2, 30), (47.2, 57, 0), (-15.6, 34.4, 0))]
    + [["SN-Rock_Medium_1", 48, 44, 0, 20, 0.6], ["SN-Rock_Medium_2", -31, 37, 0, 0, 0.7]]
)
VIEWS = {  # name: camera position (x, n, z), look-at, vertical fov, explorer position (x, n) or None.  Same four cameras as P1.0.
    "view-a-aerial": ((52, -66, 70), (5, 42, 2), 33, None),
    "view-b-merchant-street": ((0, 12.2, 6.6), (0, 24, 1.25), 60, (0, 24)),
    "view-c-central-bazaar": ((-2.5, 35.4, 8.0), (1.5, 56, 2.5), 62, (1.6, 44.6)),   # moved 3.9 m north: B06/B09 now stand where the P1.0 camera was
    "view-d-exchange-court": ((-1.8, 57.6, 1.65), (0.4, 80, 9.2), 64, (2.6, 63.5)),
}


def rect_of(b):
    """NOMINAL world footprint rectangle (x0, x1, n0, n1): wall lines, plus podium/stairs (A01) or veranda (A08)."""
    _, aid, _, x, n, rz = b[:6]
    W, D = ARCHETYPES[aid]["footprint"]
    if aid == "A01":
        return (x - 14, x + 14, n - 12, n + 6)
    f = ARCHETYPES[aid].get("front_extra", 0)
    lo = {0: (-W / 2, W / 2, -D / 2 - f, D / 2), 180: (-W / 2, W / 2, -D / 2, D / 2 + f),
          90: (-D / 2, D / 2 + f, -W / 2, W / 2), -90: (-D / 2 - f, D / 2, -W / 2, W / 2)}[rz]
    return (x + lo[0], x + lo[1], n + lo[2], n + lo[3])


def door_point(b, out=1.5):
    _, aid, _, x, n, rz = b[:6]
    W, D = ARCHETYPES[aid]["footprint"]
    d = (12 if aid == "A01" else D / 2 + ARCHETYPES[aid].get("front_extra", 0)) + out
    a = math.radians(rz)
    return (round(x + d * math.sin(a), 2), round(n - d * math.cos(a), 2))


def overlap(a, b, m=0.0):
    return a[0] < b[1] - m and b[0] < a[1] - m and a[2] < b[3] - m and b[2] < a[3] - m


def stall_rect(s):
    _, kit, x, n, rz = s
    w, d = STALL_KITS[kit]["rect"]
    if rz in (90, -90):
        w, d = d, w
    return (x - w / 2, x + w / 2, n - d / 2, n + d / 2)


def checks():
    out, ok = [], True
    rects = {b[0]: rect_of(b) for b in BUILDINGS}
    rects["G01w"] = (-4, -2, 3, 7); rects["G01e"] = (2, 4, 3, 7); rects["M01"] = (-1, 1, 48, 50)
    ids = list(rects)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if overlap(rects[a], rects[b]):
                ok = False; out.append(f"FAIL overlap {a} {b}")
    for name, *c in CLEAR:
        for k, r in list(rects.items()) + [(s[0], stall_rect(s)) for s in STALLS]:
            if overlap(tuple(c), r):
                ok = False; out.append(f"FAIL {k} blocks '{name}'")
    for b in BUILDINGS:
        px, pn = door_point(b)
        if not any(p[1] <= px <= p[2] and p[3] <= pn <= p[4] for p in PAVING):
            ok = False; out.append(f"FAIL {b[0]} entrance approach ({px},{pn}) is not on paving")
    for s in STALLS:
        if not any(p[1] <= s[2] <= p[2] and p[3] <= s[3] <= p[4] for p in PAVING):
            ok = False; out.append(f"FAIL stall {s[0]} not on paving")
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
    xs = [v for k, r in rects.items() for v in r[:2]] + [v for p in PAVING for v in p[1:3]]
    ns = [v for k, r in rects.items() for v in r[2:]] + [v for p in PAVING for v in p[3:5]]
    out.append(f"INFO developed envelope (nominal) x {min(xs)}..{max(xs)} ({max(xs) - min(xs)} m), n {min(ns)}..{max(ns)} ({max(ns) - min(ns)} m)")
    return ok, out, (min(xs), max(xs), min(ns), max(ns))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    ok, msgs, env = checks()
    print("\n".join(msgs)); print("NOMINAL SPATIAL CHECKS:", "PASS" if ok else "FAIL")
    arch = dict(ARCHETYPES); arch["GATE"] = GATE; arch["CROSS"] = CROSS
    json.dump(arch, open(os.path.join(out, "archetypes.json"), "w"), indent=1)
    layout = {"revision": REVISION,
              "buildings": [dict(id=b[0], archetype=b[1], district=b[2], x=b[3], n=b[4], rz=b[5], label=b[6], opts=b[7] or {}, rect=rect_of(b), door=door_point(b)) for b in BUILDINGS],
              "gate": GATE_POS, "cross": CROSS_POS, "stall_kits": STALL_KITS,
              "stalls": [dict(id=s[0], kit=s[1], x=s[2], n=s[3], rz=s[4], rect=stall_rect(s)) for s in STALLS],
              "paving": PAVING, "yards": YARDS, "reserved": RESERVED, "clear": CLEAR, "dressing": DRESSING, "views": VIEWS, "nodes": NODES, "edges": EDGES,
              "envelope": env, "checks": msgs, "checks_pass": ok}
    json.dump(layout, open(os.path.join(out, "layout.json"), "w"), indent=1)
    print("wrote", out)
