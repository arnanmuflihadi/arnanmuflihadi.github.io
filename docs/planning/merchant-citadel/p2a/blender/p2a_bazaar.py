"""Central Bazaar (P2-B batch 2): market-hall variants of the P1.4 archetype A02 and per-asset collision footprints measured on the real models.

A02 is the P1.4 covered market hall (8 x 12 m open timber arcade on four corner posts, 8x12 round-tile roof). Its two dressing kits
(provisions, crafts) become two kit nodes, A02p (west hall, B02) and A02c (east hall, B03), so each hall carries its own merchandise,
signs and entrance dressing. Variants may add or replace extras (see `improve`) without touching the P1.4 data files.
"""
import copy, json, os

PREFIX = {"MV": "quaternius-medieval-village", "FP": "quaternius-fantasy-props", "SN": "quaternius-stylized-nature", "SY": "synofplay-medieval-cafe", "AV": "avramania-free-collection"}
HALL_VARIANTS = {"A02p": {"base": "A02", "kit": "provisions", "sign": "FP-Banner_1@blue"}, "A02c": {"base": "A02", "kit": "crafts", "sign": "FP-Banner_1@burgundy"},
                 # P2-B batch 3: the artisan lane (D6) and the south gateway (D1): one kit node per building so each carries its own trade
                 "A06s": {"base": "A06", "open_roof": False, "bld": "B10"}, "A06j": {"base": "A06", "open_roof": False, "bld": "B12"},
                 "A04bP": {"base": "A04b", "open_roof": False, "bld": "B11"}, "A04bO": {"base": "A04b", "open_roof": False, "bld": "E01"},
                 "A03cC": {"base": "A03c", "open_roof": False, "bld": "E02"},
                 # P2-B batch 4: the Eastern Trade Quarter (warehouse lane D7) and the tea route (D8)
                 "A07w": {"base": "A07", "open_roof": False, "bld": "B13"}, "A05c": {"base": "A05", "open_roof": False, "bld": "E04"}, "A03cT": {"base": "A03c", "open_roof": False, "bld": "E05"},
                 # P2-B batch 5: the Civic Terrace tower houses
                 "A11a": {"base": "A11", "open_roof": False, "bld": "B15"}, "A11c": {"base": "A11m", "open_roof": False, "bld": "B16"}}
NODE_FOR_BLD = {v["bld"]: k for k, v in HALL_VARIANTS.items() if v.get("bld")}
NODE_FOR_KIT = {"provisions": "A02p", "crafts": "A02c"}


def load_dims(inspect_dir):
    """asset id -> {dims, bbox_min, bbox_max} (glTF axes: x right, y up, z toward the viewer) from the P1 measurements."""
    inv = {v: k for k, v in PREFIX.items()}
    out = {}
    for f in ("measurements.json", "measurements-expansion.json"):
        p = os.path.join(inspect_dir, f)
        if not os.path.exists(p):
            continue
        for r in json.load(open(p)):
            if r["pack_id"] in inv and r.get("bbox_min_xyz_gltf"):
                out[f"{inv[r['pack_id']]}-{r['asset_name']}"] = {"min": r["bbox_min_xyz_gltf"], "max": r["bbox_max_xyz_gltf"], "tris": r.get("triangle_count", 0), "file": r["internal_filepath"], "pack": r["pack_id"]}
    return out


def hall_archetype(variant, arch, improve=None):
    improve = improve or globals().get('improve')
    """The A02 archetype for one variant: parts unchanged, extras of the other kit removed, optional per-variant improvements applied."""
    v = HALL_VARIANTS[variant]
    a = copy.deepcopy(arch[v["base"]])
    a["extras"] = [e for e in a["extras"] if not e.get("kit") or e["kit"] == v.get("kit")]
    a["open_roof"] = v.get("open_roof", True)                                            # open arcade: roof proxies are a shell, not a slab (camera can stand under the roof)
    if improve:
        a = improve(variant, a)
    return a



# ----------------------------------------------------------------------------------------------------------- P2-B batch 2: making the two halls different buildings
# Cause found on the first assembly: both halls were the same open arcade with the same banners and seal; only the goods differed, so the pair read as one
# repeated building. The corrections are architectural, not decorative: the crafts hall is a partly closed shop-hall (plaster bays with windows, closed back and
# east side) while the provisions hall stays a fully open produce arcade; each has its own entrance dressing (cloth awnings in its district colour, hanging trade signs),
# its own zoning, and the same shell/roof/posts so the pair is still one family. Hall-local frame: origin = centre, front (entrance, south) at y = -6, north = +y.
def improve(variant, a):
    ex = a["extras"]
    if variant == "A02p":      # PROVISIONS, open produce arcade: blue cloth, loaf and crate signs, hay, herbs, a barrow of fruit at the door
        ex += [
            {"asset": "CUS-Awning_blue", "pos": [-3, -6.03, 3.08], "rz": 0}, {"asset": "CUS-Awning_blue", "pos": [3, -6.03, 3.08], "rz": 0},
            {"asset": "CUS-Sign_Loaf_wood", "pos": [-1.0, -6.08, 3.05], "rz": 0, "scale": 1.4}, {"asset": "CUS-Sign_Crate_wood", "pos": [1.0, -6.08, 3.05], "rz": 0, "scale": 1.4},
            {"asset": "AV-mdvl_props_wheelbarrow_01", "pos": [-3.15, -4.95, 0], "rz": 70}, {"asset": "AV-mdvl_farm_fruit_basket_01", "pos": [3.25, -4.9, 0], "rz": 0}, {"asset": "AV-mdvl_farm_fruit_basket_01", "pos": [3.45, -4.35, 0], "rz": 40},
            {"asset": "AV-mdvl_farm_hay_bale_01", "pos": [-3.3, 5.35, 0], "rz": 10}, {"asset": "AV-mdvl_farm_hay_bale_01", "pos": [-2.55, 5.5, 0], "rz": -8}, {"asset": "AV-mdvl_farm_hay_bale_01", "pos": [-2.95, 5.4, 0.52], "rz": 4},
            {"asset": "SY-herb-drying-hanger", "pos": [-1.95, 0.0, 2.6], "rz": 90}, {"asset": "SY-herb-drying-hanger", "pos": [1.95, -0.9, 2.6], "rz": 90},
            {"asset": "AV-mdvl_props_sack_01", "pos": [2.2, 5.45, 0], "rz": 25},
        ]
        # P2-B batch 3: selective polish of the sparse interior (the north gable was a blank triangle, the aisle ends dim and empty): the guild seal on the inside of both gables,
        # lanterns on the four inner piers, two more herb hangers over the produce tables, scales on the north bench. No new props on the floor: the aisle stays clear.
        ex += [
            {"asset": "CUS-Seal_NiagaAwan", "pos": [0, 5.78, 5.25], "rz": 0, "scale": 1.3}, {"asset": "CUS-Seal_NiagaAwan", "pos": [0, -5.78, 5.25], "rz": 180, "scale": 1.3},
            {"asset": "FP-Lantern_Wall", "pos": [-3.76, 4.0, 2.3], "rz": 90}, {"asset": "FP-Lantern_Wall", "pos": [3.76, 4.0, 2.3], "rz": -90},
            {"asset": "FP-Lantern_Wall", "pos": [-3.76, -2.0, 2.3], "rz": 90}, {"asset": "FP-Lantern_Wall", "pos": [3.76, -2.0, 2.3], "rz": -90},
            {"asset": "SY-herb-drying-hanger", "pos": [-1.95, 3.4, 2.6], "rz": 90}, {"asset": "SY-herb-drying-hanger", "pos": [1.95, 2.8, 2.6], "rz": 90},
            {"asset": "AV-mdvl_food_scales_01", "pos": [0.5, 4.9, 0.53], "rz": 180},
        ]
    elif variant == "A02c":    # CRAFTS AND TEXTILES, partly closed shop-hall: burgundy cloth, coin and scroll signs, cloth wall, rug, chest, book stand
        a["parts"][0]["facades"] = {"front": ["FAAF"], "back": ["RPPR"], "right": ["RPRPRP"], "left": ["AAAAAA"]}
        a["solid_runs"] = [[-4, -6, -2, -6], [2, -6, 4, -6], [-4, 6, 4, 6], [4, -6, 4, 6]]                  # the new closed bays (local plan, height 3 m)
        ex += [
            {"asset": "CUS-Awning_burgundy", "pos": [-1, -6.03, 3.08], "rz": 0}, {"asset": "CUS-Awning_burgundy", "pos": [1, -6.03, 3.08], "rz": 0},
            {"asset": "CUS-Sign_Coin_burgundy", "pos": [-2.05, -6.08, 3.05], "rz": 0, "scale": 1.4}, {"asset": "CUS-Sign_Scroll_burgundy", "pos": [2.05, -6.08, 3.05], "rz": 0, "scale": 1.4},
            {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [-2.4, 5.7, 2.95], "rz": 0}, {"asset": "FP-Banner_2_Cloth@gold", "pos": [-1.2, 5.7, 2.95], "rz": 0}, {"asset": "FP-Banner_2_Cloth@blue", "pos": [0.0, 5.7, 2.95], "rz": 0},
            {"asset": "FP-Banner_2_Cloth@cream", "pos": [1.2, 5.7, 2.95], "rz": 0}, {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [2.4, 5.7, 2.95], "rz": 0},
            {"asset": "AV-mdvl_interiors_rug_01", "pos": [0.0, -3.2, 0.02], "rz": 0}, {"asset": "AV-mdvl_interiors_rug_01", "pos": [0.0, 1.2, 0.02], "rz": 90},
            {"asset": "AV-mdvl_dungeon_chest_01", "pos": [3.4, 0.5, 0], "rz": -90}, {"asset": "FP-BookStand", "pos": [3.3, -1.2, 0], "rz": -90},
        ]
    a["extras"] = ex
    return a


# ----------------------------------------------------------------------------------------------------------- P2-B batch 3: Lorong Lentera (artisan lane) and the south gateway
# Each building of the district is one archetype with ONE added architectural device and a coherent working set, not a repeat of its P1.4 shape:
#   B10 smithy      stone workshop + open forge bay (lean-to roof on posts) on the north side, quench trough, whetstone, coal sacks, tool rack
#   B12 joiner      timber-framed (plaster/half-timber) workshop + open drying shed on the north side with wood piles, ladder, bench, wheelbarrow of offcuts
#   B11 potter      A04b shop closing the cross street + brick kiln with a tall flue beside it, vase rows, jar shelf, clay trough
#   E01 outfitter   A04b with burgundy awnings, hanging rope and tools, barrels and bags, a way-post
#   E02 carrier     A03c with a parked wagon, crates and bales for the carrier's office, hitching fence
# Local frame as before (front at y = -D/2). A pentice-style lean-to is three Roof_Wooden_2x1 modules (L, Center, R); on a side wall it is rotated by 90.
def _side_leanto(x_wall, sgn, z=2.6, length=6, along0=0.0):
    """Lean-to roof on a side wall (sgn +1 right wall, -1 left wall), modules every 2 m along the wall, 1.56 m deep."""
    n = length // 2; out = []
    for i in range(n):
        kind = "L" if i == 0 else "R" if i == n - 1 else "Center"
        y = along0 + (-length / 2 + 1 + 2 * i) * (1 if sgn > 0 else -1)
        out.append({"asset": f"MV-Roof_Wooden_2x1_{kind}", "pos": [x_wall, y, z], "rz": 90 if sgn > 0 else -90})
    return out


def _post(x, y, zs=0.87):
    return {"asset": "MV-Corner_Exterior_Wood", "pos": [x, y, 0], "scale": [1, 1, zs]}


def improve_district(variant, a):
    ex = a["extras"]
    RV = {"A06s": "dark", "A06j": "weathered", "A04bP": "weathered", "A03cC": "weathered"}
    if variant in RV:
        a["parts"][0]["roof_variant"] = RV[variant]
    if variant == "A06s":        # B10 smithy: stone workshop with an open forge bay on its SOUTH side (first test: a bay on the north side narrowed the 3 m party gap to the potter to 1.2 m and blocked the alley)
        ex += _side_leanto(-3.0, -1)                            # roof modules on the south wall (rz -90), L/R ends placed for that side
        bay = [_post(4.45, 0.0), _post(4.45, 2.85)]                # the east end rests on the lane-entrance post of the P1.4 dressing at (-18.3, 6.7), so no post of its own
        bay += [
            {"asset": "AV-mdvl_interiors_anvil_01", "pos": [3.9, 0.35, 0], "rz": 90}, {"asset": "AV-mdvl_props_water_trough_01", "pos": [3.8, -1.7, 0], "rz": 90},
            {"asset": "FP-Whetstone", "pos": [3.8, 2.0, 0], "rz": 90, "scale": 0.7}, {"asset": "AV-mdvl_props_sack_01", "pos": [3.55, -2.5, 0], "rz": 20}, {"asset": "AV-mdvl_props_sack_01", "pos": [3.7, -2.9, 0], "rz": 70},
            {"asset": "FP-Peg_Rack", "pos": [3.07, -0.1, 1.55], "rz": 90}, {"asset": "AV-mdvl_props_hammer_01", "pos": [3.12, -0.45, 1.6], "rz": 90}, {"asset": "FP-Pickaxe_Bronze", "pos": [3.1, 1.15, 1.2], "rz": 90},
            {"asset": "AV-mdvl_props_hammer_01", "pos": [3.2, 0.35, 0.82], "rz": 25},
        ]
        for e in bay:                                          # mirror across the building's centre line: x -> -x, facing -> -facing (an item facing +x, rz 90, now faces -x, rz -90)
            m = dict(e); m["pos"] = [-e["pos"][0], e["pos"][1], e["pos"][2]]; m["rz"] = -e.get("rz", 0)
            ex.append(m)
    elif variant == "A06j":      # B12 joiner: timber-framed shop with an open drying shed for seasoned wood
        a["parts"][0]["facades"] = {"front": ["GDF"], "right": ["PFP"], "back": ["PGP"], "left": ["PPG"]}
        a["parts"][0]["corner"] = "wood"
        a["extras"] = ex = [e for e in ex if e["asset"] not in ("MV-Prop_Vine1", "FP-WeaponStand", "FP-Anvil_Log")]
        ex += _side_leanto(3.0, +1) + [_post(4.45, -2.85), _post(4.45, 0.0), _post(4.45, 2.85)]
        ex += [
            {"asset": "AV-mdvl_interiors_woodpile_01", "pos": [3.95, -1.9, 0], "rz": 90}, {"asset": "AV-mdvl_interiors_woodpile_01", "pos": [3.95, -0.7, 0], "rz": 90}, {"asset": "AV-mdvl_interiors_woodpile_01", "pos": [3.95, 0.5, 0], "rz": 90},
            {"asset": "AV-mdvl_props_cart_wheel_01", "pos": [3.4, 2.1, 0], "rz": 0}, {"asset": "AV-mdvl_village_ladder_01", "pos": [3.07, 1.4, 0], "rz": 90},
            {"asset": "AV-mdvl_props_axe_01", "pos": [-1.7, -4.28, 0.97], "rz": 60}, {"asset": "AV-mdvl_props_wheelbarrow_01", "pos": [2.4, -4.5, 0], "rz": 20},
            {"asset": "AV-mdvl_nature_stump_01", "pos": [-3.6, -3.1, 0], "scale": 0.45},
        ]
    elif variant == "A04bP":     # B11 potter's yard: shop at the end of the cross street, kiln with a flue beside it
        ex[:] = [e for e in ex if not e["asset"].startswith("CUS-Awning")]
        ex += [{"asset": "CUS-Awning_gold", "pos": [x, -2.03, 3.08]} for x in (-2, 0, 2)]
        # kiln behind the shop (open side against the back wall) so the 3 m gap between B11 and B12 stays a clear alley; a 2 x 2 m brick box 1.7 m high with a flue, built from wall modules
        kiln = [{"asset": "MV-Wall_UnevenBrick_Straight", "pos": [1.0, 3.0, 0], "rz": 90, "scale": [1, 1, 0.55]}, {"asset": "MV-Wall_UnevenBrick_Straight", "pos": [0.0, 4.0, 0], "rz": 180, "scale": [1, 1, 0.55]},
                {"asset": "MV-Wall_UnevenBrick_Straight", "pos": [-1.0, 3.0, 0], "rz": 270, "scale": [1, 1, 0.55]}, {"asset": "MV-Floor_UnevenBrick", "pos": [0.0, 3.0, 1.7]},
                {"asset": "MV-Prop_Chimney", "pos": [0.0, 3.0, 1.7]}]
        kiln[0]["solid"] = [2.0, 2.0, 1.7, 0.0, 3.0]
        ex += kiln
        ex += [
            {"asset": "FP-Vase_2", "pos": [-2.3, -2.95, 0]}, {"asset": "FP-Vase_4", "pos": [-1.5, -3.0, 0]}, {"asset": "FP-Vase_2", "pos": [1.55, -3.0, 0], "rz": 40}, {"asset": "FP-Vase_4", "pos": [2.35, -2.95, 0]},
            {"asset": "AV-mdvl_interiors_pot_01", "pos": [-3.45, -2.3, 0], "rz": 20}, {"asset": "AV-mdvl_props_water_trough_01", "pos": [3.8, -2.7, 0], "rz": 0},
            {"asset": "SY-shelf01", "pos": [3.0, -1.0, 0], "rz": -90}, {"asset": "SY-basket-of-jars", "pos": [-3.35, -3.1, 0]}, {"asset": "AV-mdvl_props_pot_01", "pos": [1.1, -3.05, 0]},
        ]
    elif variant == "A04bO":     # E01 traveller's outfitter at the south gateway: ropes, bags, barrels, a way-post
        ex[:] = [e for e in ex if not e["asset"].startswith("CUS-Awning")]
        ex += [{"asset": "CUS-Awning_burgundy", "pos": [x, -2.03, 3.08]} for x in (-2, 0, 2)]
        ex += [
            {"asset": "FP-Peg_Rack", "pos": [-2.0, -2.05, 1.6]}, {"asset": "FP-Rope_1", "pos": [-2.0, -2.2, 1.35], "rz": 0, "scale": 0.8},
            {"asset": "AV-mdvl_props_barrel_01", "pos": [-3.35, -2.55, 0]}, {"asset": "AV-mdvl_props_barrel_01", "pos": [-3.45, -3.3, 0], "rz": 30},
            {"asset": "AV-mdvl_props_basket_01", "pos": [2.9, -2.9, 0]}, {"asset": "FP-Bag", "pos": [3.45, -2.55, 0], "rz": 30}, {"asset": "AV-mdvl_props_sack_01", "pos": [3.1, -3.4, 0], "rz": 70},
            {"asset": "AV-mdvl_props_signpost_01", "pos": [-4.2, -4.2, 0], "rz": 20}, {"asset": "AV-mdvl_props_rope_coil_01", "pos": [1.5, -2.9, 0], "rz": 15},
        ]
    elif variant == "A03cC":     # E02 carrier's office on the arrival court: the cargo wagon and crates of the P1.4 court dressing stand 5 m out, so the office adds only its own load (crates and bales left of the door, a hitching rail right); the door stays clear
        ex += [
            {"asset": "MV-Prop_Crate", "pos": [-3.4, -3.3, 0], "rz": 8}, {"asset": "MV-Prop_Crate", "pos": [-3.35, -3.35, 1.06], "rz": 30},
            {"asset": "AV-mdvl_props_sack_01", "pos": [-3.35, -4.5, 0], "rz": 15}, {"asset": "AV-mdvl_farm_hay_bale_01", "pos": [1.3, -3.2, 0], "rz": 5}, {"asset": "AV-mdvl_farm_hay_bale_01", "pos": [1.95, -3.3, 0], "rz": -20},
            {"asset": "MV-Prop_WoodenFence_Single", "pos": [3.2, -4.4, 0], "rz": 90}, {"asset": "MV-Corner_Exterior_Wood", "pos": [3.2, -3.4, 0], "scale": [1, 1, 0.45]}, {"asset": "MV-Corner_Exterior_Wood", "pos": [3.2, -5.4, 0], "scale": [1, 1, 0.45]},
        ]
    a["extras"] = ex
    return a



# ----------------------------------------------------------------------------------------------------------- P2-B batch 4: custom details and the Eastern Trade Quarter
def register_custom(cl):
    """Reusable custom Blender geometry for details the downloaded modules cannot make (NOT downloaded assets; listed as custom in the registers).
    CUS-Hoist: warehouse loading jib (wall plate, beam, brace, pulley, rope, hook); origin = beam top at the wall face, the beam runs 2.3 m along -Y.
    CUS-Sign_Leaf_<field>: tea-trade pictogram sign. CUS-Awning_tea: sage-green striped awning (the tea route's accent colour; extends the P1.2 palette, disclosed)."""
    import math, bmesh as _bm
    cl.PALETTE.setdefault("tea", "#6F7F55")
    cl.VARIANTS.setdefault("weathered", ("grade", "MI_RoundTiles", (0.0, 0.58, 0.9)))        # batch 5: a weathered, less saturated terracotta to break roof repetition (B11, B12, E02); a material grade like "dark", not new geometry
    cl.GLYPHS["Leaf"] = [(0.0, 0.15), (0.05, 0.10), (0.085, 0.02), (0.08, -0.05), (0.035, -0.10), (0.012, -0.12), (0.012, -0.17), (-0.012, -0.17), (-0.012, -0.12), (-0.035, -0.10), (-0.08, -0.05), (-0.085, 0.02), (-0.05, 0.10)]   # batch 5: one pointed leaf on a stem (the batch 4 two-leaf sprig read as a heart)
    cl.GLYPHS["Compass"] = [(0.0, 0.15), (0.035, 0.035), (0.15, 0.0), (0.035, -0.035), (0.0, -0.15), (-0.035, -0.035), (-0.15, 0.0), (-0.035, 0.035)]           # a four-point compass star (the cartographer's pictogram)

    def prism_yz(bm, pts, x0, x1, mi):                         # outline in the (y, z) plane extruded along x from x0 to x1
        a = [bm.verts.new((x0, y, z)) for y, z in pts]; b = [bm.verts.new((x1, y, z)) for y, z in pts]; n = len(pts)
        fs = [bm.faces.new(a[::-1]), bm.faces.new(b)] + [bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i])) for i in range(n)]
        for f in fs:
            f.material_index = mi

    def make_hoist():
        bm = _bm.new()
        box = lambda x0, x1, y0, y1, z0, z1, mi: cl._prism(bm, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y0, y1, mi)       # y0 = back (larger), y1 = front (more negative)
        box(-0.08, 0.08, 0.15, -2.3, -0.2, 0.0, 0)                                # beam
        box(-0.1, 0.1, 0.15, -0.04, -1.55, 0.06, 0)                               # wall plate
        prism_yz(bm, [(0.1, -1.32), (0.1, -1.14), (-1.25, -0.2), (-1.45, -0.2)], -0.045, 0.045, 0)   # diagonal brace
        box(-0.1, 0.1, -2.12, -2.28, -0.2, -0.02, 1)                              # end cap strap
        prism_yz(bm, [(-2.15 + 0.13 * math.cos(2 * math.pi * i / 14), -0.34 + 0.13 * math.sin(2 * math.pi * i / 14)) for i in range(14)], -0.035, 0.035, 1)   # pulley wheel
        box(-0.012, 0.012, -2.13, -2.17, -2.55, -0.34, 2)                         # rope
        box(-0.03, 0.03, -2.1, -2.2, -2.7, -2.55, 1)                              # hook block
        return cl._finish(bm, "CUS-Hoist", [cl.flat_material("CUS_sign_timber", cl.srgb(cl.PALETTE["timber"]), 0.8), cl.flat_material("CUS_sign_iron", (0.035, 0.035, 0.04), 0.5, 0.6),
                                            cl.flat_material("CUS_rope", cl.srgb("#8A7450"), 0.95)])
    def prism_xy(bm, pts, z0, z1, mi):                         # outline in the (x, y) plane extruded along z (horizontal discs)
        a = [bm.verts.new((x, y, z0)) for x, y in pts]; b = [bm.verts.new((x, y, z1)) for x, y in pts]; n = len(pts)
        fs = [bm.faces.new(a[::-1]), bm.faces.new(b)] + [bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i])) for i in range(n)]
        for f in fs:
            f.material_index = mi

    def make_balance():
        """CUS-AssayBalance: the assay office's hanging sign, a pair of scales (bracket, post, balance beam, two gold pans on rods). Origin = where the arm meets the wall, top of the arm; it runs 0.95 m along -Y."""
        bm = _bm.new(); box = lambda x0, x1, y0, y1, z0, z1, mi: cl._prism(bm, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y0, y1, mi)
        box(-0.03, 0.03, 0.0, -0.95, -0.06, 0.0, 0); box(-0.02, 0.02, -0.02, -0.5, -0.46, -0.06, 0)          # arm and a strut to the wall
        box(-0.012, 0.012, -0.93, -0.97, -0.56, -0.06, 0)                                                  # post carrying the balance
        box(-0.5, 0.5, -0.925, -0.975, -0.60, -0.57, 0)                                                    # balance beam
        for sx in (-0.46, 0.46):
            box(sx - 0.006, sx + 0.006, -0.945, -0.955, -0.86, -0.60, 0)                                    # rod
            prism_xy(bm, [(sx + 0.17 * math.cos(2 * math.pi * k / 16), -0.95 + 0.17 * math.sin(2 * math.pi * k / 16)) for k in range(16)], -0.92, -0.87, 1)   # pan
        return cl._finish(bm, "CUS-AssayBalance", [cl.flat_material("CUS_sign_iron", (0.035, 0.035, 0.04), 0.5, 0.6), cl.flat_material("CUS_guild_gold", cl.srgb(cl.PALETTE["gold"]), 0.42, 0.45)])

    def make_mapboard():
        """CUS-MapBoard: the cartographer's street board, a timber frame on two posts with a parchment chart (two burgundy routes, gold way-stations, a blue compass disc). Origin = ground, centre; faces -Y; 1.4 m wide, top at 1.9 m."""
        bm = _bm.new(); box = lambda x0, x1, y0, y1, z0, z1, mi: cl._prism(bm, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y0, y1, mi)
        box(-0.72, -0.64, -0.05, 0.05, 0.0, 1.9, 0); box(0.64, 0.72, -0.05, 0.05, 0.0, 1.9, 0)              # posts
        box(-0.72, 0.72, -0.07, 0.06, 0.86, 1.9, 0); box(-0.64, 0.64, -0.075, -0.06, 0.94, 1.82, 1)          # frame, parchment
        for cx, cz, w, ang in ((-0.12, 1.38, 0.95, 0.45), (0.2, 1.32, 0.75, -0.55)):
            cl._prism(bm, cl._rect(cx, cz, w, 0.035, ang), -0.076, -0.082, 2)
        for cx, cz in ((-0.45, 1.2), (0.05, 1.5), (0.42, 1.12), (-0.3, 1.62)):
            cl._prism(bm, [(cx + x, cz + z) for x, z in cl._circle(0.045, 10)], -0.076, -0.088, 3)
        cl._prism(bm, [(0.45 + x, 1.62 + z) for x, z in cl._circle(0.11, 18)], -0.076, -0.084, 4)
        return cl._finish(bm, "CUS-MapBoard", [cl.flat_material("CUS_sign_timber", cl.srgb(cl.PALETTE["timber"]), 0.8), cl.flat_material("CUS_parchment", cl.srgb("#E2D2A8"), 0.9), cl.flat_material("CUS_guild_burgundy", cl.srgb(cl.PALETTE["burgundy"]), 0.75),
                                               cl.flat_material("CUS_guild_gold", cl.srgb(cl.PALETTE["gold"]), 0.42, 0.45), cl.flat_material("CUS_guild_blue", cl.srgb(cl.PALETTE["blue"]), 0.7)])
    cl.CUSTOM["CUS-AssayBalance"] = make_balance; cl.CUSTOM["CUS-MapBoard"] = make_mapboard
    for f in ("wood", "burgundy", "blue"):
        cl.CUSTOM[f"CUS-Sign_Compass_{f}"] = (lambda g="Compass", ff=f: cl.make_sign(g, ff))
    cl.CUSTOM["CUS-Hoist"] = make_hoist
    for f in ("wood", "burgundy", "blue"):
        cl.CUSTOM[f"CUS-Sign_Leaf_{f}"] = (lambda g="Leaf", ff=f: cl.make_sign(g, ff))
    cl.CUSTOM["CUS-Awning_tea"] = (lambda: cl.make_awning("tea"))


def _balcony_on_posts(w_tiles, y_tile, y_post, z=3.0):
    """Balcony gallery in the pattern of the inn (P1.4 A09): wood floor tiles, straight rails with end returns, four posts carrying it. Tiles every 2 m, centred on x = 0."""
    xs = [(-(w_tiles - 1) + 2 * i) for i in range(w_tiles)]
    out = [{"asset": "MV-Floor_WoodDark", "pos": [x, y_tile, z]} for x in xs] + [{"asset": "MV-Balcony_Simple_Straight", "pos": [x, y_tile, z]} for x in xs]
    out += [{"asset": "MV-Balcony_Simple_Straight", "pos": [xs[-1], y_tile, z], "rz": 90}, {"asset": "MV-Balcony_Simple_Straight", "pos": [xs[0], y_tile, z], "rz": -90}]
    px = [xs[0] - 0.9, xs[len(xs) // 2 - 1] + 1 if len(xs) > 2 else xs[0] + 1, xs[len(xs) // 2] - 1 if len(xs) > 2 else xs[-1] - 1, xs[-1] + 0.9]
    out += [{"asset": "MV-Corner_Exterior_Wood", "pos": [x, y_post, 0]} for x in px]
    return out


def improve_east(variant, a):
    ex = a["extras"]
    if variant == "A07w":        # B13 guild warehouse. Local: front (lane gable, west) y = -7, north long wall (service court) x = -4, south long wall x = +4.
        P = a["parts"][0]
        # north long wall, listed east -> west (slot i at y = 6 - 2i): double loading doors under the hoist hatch, a pier, a window, a side door, a pier
        P["facades"]["left"] = ["SooSsoS", "PTDTPTP"]
        a["extras"] = ex = [e for e in ex if e["asset"] not in ("MV-Prop_Wagon", "MV-Prop_Crate", "FP-Barrel", "FP-Crate_Wooden", "MV-Prop_Vine5", "MV-Prop_Vine1")]
        ex += _side_leanto(-4.0, -1, z=2.6, length=6, along0=3.0) + [_post(-5.45, 0.0, 0.87), _post(-5.45, 6.0, 0.87)]
        ex += [
            {"asset": "CUS-Hoist", "pos": [-4.05, 2.0, 5.0], "rz": -90}, {"asset": "MV-Prop_Crate", "pos": [-6.0, 2.0, 2.45], "scale": 0.62, "rz": 15},      # the jib with a crate half way up to the hatch
            {"asset": "AV-mdvl_props_sack_01", "pos": [-4.7, 4.8, 0], "rz": 20}, {"asset": "FP-Barrel", "pos": [-4.85, 5.6, 0]}, {"asset": "FP-Barrel", "pos": [-4.75, 0.7, 0]},
            {"asset": "FP-Table_Large", "pos": [-4.85, 2.9, 0], "rz": 90}, {"asset": "AV-mdvl_food_scales_01", "pos": [-4.85, 2.4, 0.83], "rz": 90}, {"asset": "FP-Book_Stack_1", "pos": [-4.8, 3.5, 0.83], "rz": 10},
            {"asset": "FP-Lantern_Wall", "pos": [-4.1, 4.0, 2.2], "rz": 90}, {"asset": "FP-Lantern_Wall", "pos": [-4.1, -1.2, 2.2], "rz": 90},
            # lane gable: the guild's mark, a loading sign, goods at the doors; the south wall carries the wagon of the P1.4 yard
            {"asset": "CUS-Sign_Crate_burgundy", "pos": [-3.55, -7.05, 3.3], "rz": 0, "scale": 1.4, "role": "sign"},
            # batch 5: the south long wall was plain (seen from the open ground and from the cross lane): ivy, open shutters on both ground windows, a rain butt and a ladder, two wall lanterns
            {"asset": "MV-Prop_Vine5", "pos": [4.04, 2.0, 5.4], "rz": 90}, {"asset": "MV-Prop_Vine1", "pos": [4.04, -3.5, 5.6], "rz": 90},
            {"asset": "MV-WindowShutters_Wide_Flat_Open", "pos": [4.0, -2.0, 0.0], "rz": 90}, {"asset": "MV-WindowShutters_Wide_Flat_Open", "pos": [4.0, 2.0, 0.0], "rz": 90},
            {"asset": "AV-mdvl_props_barrel_01", "pos": [4.7, 5.3, 0]}, {"asset": "AV-mdvl_village_ladder_01", "pos": [4.05, 4.2, 0], "rz": 90},
            {"asset": "FP-Lantern_Wall", "pos": [4.1, 0.0, 2.2], "rz": 90}, {"asset": "FP-Lantern_Wall", "pos": [4.1, -5.0, 2.2], "rz": 90},
            {"asset": "MV-Prop_Wagon", "pos": [6.4, -4.2, 0], "rz": 18}, {"asset": "MV-Prop_Crate", "pos": [5.0, -7.6, 0], "rz": 8}, {"asset": "FP-Barrel", "pos": [4.9, -6.6, 0]}, {"asset": "FP-Crate_Wooden", "pos": [-4.9, -7.7, 0], "rz": 12},
            {"asset": "AV-mdvl_props_sack_01", "pos": [-4.6, -6.3, 0], "rz": 60}, {"asset": "MV-Prop_Crate", "pos": [-5.1, -6.4, 0], "rz": 25},
        ]
    elif variant == "A05c":      # E04 counting house. Local: front (lane, west) y = -4, south wall (court) x = +4 with the tally loggia, back (east) y = +4 carries the strongroom wing.
        P = a["parts"][0]; P["roof_variant"] = "dark"
        a["parts"].append({"id": "strongroom", "W": 6, "D": 4, "floors": 1, "roof": "4x6", "ridge": "x", "corner": "brick", "roof_variant": "dark", "offset": (0, 6, 0),
                           "facades": {"front": ["XXX"], "right": ["Ss"], "back": ["SsS"], "left": ["Ss"]}})
        a["extras"] = ex = [e for e in ex if not (e["asset"].startswith("CUS-Sign") and e["pos"][0] > 0)]
        ex += _side_leanto(4.0, +1, z=2.6, length=8, along0=0.0) + [_post(5.45, -4.0, 0.87), _post(5.45, 0.0, 0.87), _post(5.45, 4.0, 0.87)]
        ex += [
            {"asset": "FP-Table_Large", "pos": [4.95, -1.7, 0], "rz": 90}, {"asset": "AV-mdvl_food_scales_01", "pos": [4.95, -2.2, 0.83], "rz": 90}, {"asset": "FP-Book_Stack_1", "pos": [4.9, -1.1, 0.83], "rz": 80},
            {"asset": "FP-Bench", "pos": [4.85, 2.55, 0], "rz": 90}, {"asset": "AV-mdvl_props_sack_01", "pos": [5.0, 3.5, 0], "rz": 20}, {"asset": "AV-mdvl_props_sack_01", "pos": [4.6, 3.55, 0.0], "rz": 70},
            {"asset": "FP-Lantern_Wall", "pos": [4.1, 0.0, 2.3], "rz": 90},
            # batch 5: the north wall (seen from the yard behind) was plain: ivy, shutters on the ground window, a notice board with the guild's tariff
            {"asset": "MV-Prop_Vine5", "pos": [-4.04, 2.0, 5.4], "rz": -90}, {"asset": "MV-WindowShutters_Wide_Flat_Open", "pos": [-4.0, 1.0, 0.0], "rz": -90},
            {"asset": "FP-Lantern_Wall", "pos": [-4.1, -1.0, 2.3], "rz": -90},
            {"asset": "CUS-Seal_NiagaAwan", "pos": [0, -4.12, 8.25], "rz": 0, "scale": 1.2}, {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [2.0, -4.13, 5.6]}, {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [-2.0, -4.13, 5.6]},
        ]
    elif variant == "A03cT":     # E05 tea route merchant house: two floors, ridge east-west, gable to the bazaar, a balcony gallery over the lane
        P = a["parts"][0]
        P["facades"] = {"front": ["FDFF", "RDRG"], "right": ["DF", "PT"], "back": ["PPPP", "PRRP"], "left": ["PD", "PT"]}
        a["extras"] = ex = [e for e in ex if e["asset"] in ("MV-Prop_Chimney2",)]
        ex += _balcony_on_posts(3, -3.0, -3.9)
        ex += [
            {"asset": "CUS-Awning_tea", "pos": [4.03, -1.0, 2.75], "rz": 90}, {"asset": "CUS-Awning_tea", "pos": [4.03, 1.0, 2.75], "rz": 90},
            {"asset": "CUS-Sign_Leaf_wood", "pos": [4.05, -1.6, 3.55], "rz": 90, "scale": 1.4, "role": "sign"},
            {"asset": "SY-herb-drying-hanger", "pos": [-2.0, -2.6, 2.45], "rz": 0}, {"asset": "SY-herb-drying-hanger", "pos": [1.8, -2.6, 2.45], "rz": 0},
            {"asset": "SY-table01", "pos": [2.1, -3.1, 0]}, {"asset": "SY-table-cloth01", "pos": [2.1, -3.1, 0.82]}, {"asset": "SY-stool", "pos": [2.1, -3.95, 0]}, {"asset": "SY-stool", "pos": [3.0, -3.1, 0]},
            {"asset": "SY-mug01", "pos": [1.9, -3.1, 0.84]}, {"asset": "SY-pitcher", "pos": [2.3, -3.2, 0.84]},
            {"asset": "SY-menu-stand01", "pos": [-3.4, -2.8, 0], "rz": 15}, {"asset": "AV-mdvl_interiors_pottedplant_01", "pos": [-3.45, -3.6, 0]},
            {"asset": "SY-basket-of-jars", "pos": [-2.1, -2.35, 0.0], "rz": 0}, {"asset": "AV-mdvl_props_basket_01", "pos": [-1.6, -3.5, 0]},
            {"asset": "FP-Lantern_Wall", "pos": [0.2, -2.1, 2.3], "rz": 0}, {"asset": "FP-Lantern_Wall", "pos": [4.1, 2.0, 2.3], "rz": 90},
            # the east wall (back-path side): the porters' door with tea sacks, chests and a ladder to the loft
            {"asset": "AV-mdvl_props_sack_01", "pos": [-4.7, 0.9, 0], "rz": 20}, {"asset": "AV-mdvl_props_sack_01", "pos": [-4.75, 0.25, 0], "rz": 80}, {"asset": "AV-mdvl_interiors_chest_01", "pos": [-4.55, -1.8, 0], "rz": 90},
            {"asset": "AV-mdvl_village_ladder_01", "pos": [-4.05, 1.7, 0], "rz": -90},
        ]
    a["extras"] = ex
    return a


_improve_halls = improve


def improve_terrace(variant, a):
    """P2-B batch 5: the Civic Terrace tower houses. Both frame the Exchange Hall (their turrets stand on the terrace side, flanking the stairs) and differ in function and articulation.
    B15 assay office (A11a): stone body, dark civic roof, two flues, an assay hatch with scales and a touchstone bench at the door, the hanging balance, burgundy standards.
    B16 chart maker (A11c): timber and plaster upper storey with wide windows, ridge east-west, terracotta roof, a first-floor balcony over the terrace, a map board and a compass sign at the door."""
    ex = a["extras"]; P = a["parts"][0]; T_ = a["parts"][1]
    if variant == "A11a":
        P["facades"] = {"front": ["sosr", "rSSr"], "right": ["rsSs", "rSSr"], "back": ["SSSS", "rSSr"], "left": ["SsSS", "rSSr"]}
        P["roof_variant"] = "dark"; T_["roof_variant"] = "dark"
        a["extras"] = ex = [e for e in ex if e["asset"] not in ("MV-Prop_Chimney2", "AV-mdvl_village_window_box_01")]
        ex += [
            {"asset": "MV-Prop_Chimney2", "pos": [-1.6, 2.0, 8.7]}, {"asset": "MV-Prop_Chimney", "pos": [-3.2, 2.0, 7.3]},
            {"asset": "CUS-AssayBalance", "pos": [-1.0, -4.05, 3.35], "rz": 0},
            {"asset": "AV-mdvl_interiors_workbench_01", "pos": [-3.0, -4.9, 0], "rz": 0}, {"asset": "AV-mdvl_food_scales_01", "pos": [-3.3, -4.9, 0.85], "rz": 0}, {"asset": "AV-mdvl_food_coin_stack_01", "pos": [-2.7, -4.9, 0.85]},
            {"asset": "FP-Book_Stack_1", "pos": [-2.95, -5.1, 0.85], "rz": 20}, {"asset": "AV-mdvl_interiors_chest_01", "pos": [-4.9, -4.5, 0], "rz": 20},
            {"asset": "AV-mdvl_interiors_pottedplant_01", "pos": [0.55, -4.6, 0]}, {"asset": "FP-Lantern_Wall", "pos": [0.6, -4.1, 2.3], "rz": 0},
            {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [1.9, -4.13, 5.7]}, {"asset": "FP-Banner_2_Cloth@burgundy", "pos": [-3.6, -4.13, 5.7]},
            {"asset": "AV-mdvl_village_window_box_01", "pos": [3.0, -4.03, 4.09], "rz": 0},
        ]
    elif variant == "A11c":
        P["ridge"] = "x"
        P["facades"] = {"front": ["ssos", "FGGF"], "right": ["SsSS", "PRRP"], "back": ["SSSS", "PTTP"], "left": ["sSsr", "RDGR"]}
        a["extras"] = ex = [e for e in ex if e["asset"] not in ("MV-Prop_Chimney2", "MV-Roof_Dormer_RoundTile", "AV-mdvl_village_window_box_01")]
        ex += [
            {"asset": "MV-Prop_Chimney2", "pos": [1.0, 2.2, 8.5]},
            {"asset": "MV-Floor_WoodDark", "pos": [-5, 3, 3.0]}, {"asset": "MV-Floor_WoodDark", "pos": [-5, 1, 3.0]},
            {"asset": "MV-Balcony_Simple_Straight", "pos": [-5, 3, 3.0], "rz": 90}, {"asset": "MV-Balcony_Simple_Straight", "pos": [-5, 1, 3.0], "rz": 90},
            {"asset": "MV-Balcony_Simple_Straight", "pos": [-5, 3, 3.0], "rz": 0}, {"asset": "MV-Balcony_Simple_Straight", "pos": [-5, 1, 3.0], "rz": 180},
            {"asset": "CUS-MapBoard", "pos": [3.1, -5.6, 0], "rz": 0},
            {"asset": "FP-BookStand", "pos": [-2.2, -4.9, 0], "rz": 10}, {"asset": "FP-Scroll_2", "pos": [-1.6, -4.95, 0.0], "rz": 40},
            {"asset": "AV-mdvl_village_window_box_01", "pos": [-1.0, -4.03, 4.09], "rz": 0}, {"asset": "AV-mdvl_village_window_box_01", "pos": [1.0, -4.03, 4.09], "rz": 0},
            {"asset": "FP-Lantern_Wall", "pos": [-0.15, -4.1, 2.3], "rz": 0},
        ]
    a["extras"] = ex
    return a


def improve(variant, a):           # noqa: F811  (dispatch: halls as in batch 2, district buildings as in batch 3 and 4)
    if variant in ("A07w", "A05c", "A03cT"):
        return improve_east(variant, a)
    if variant in ("A11a", "A11c"):
        return improve_terrace(variant, a)
    return improve_district(variant, a) if HALL_VARIANTS[variant].get("bld") else _improve_halls(variant, a)
