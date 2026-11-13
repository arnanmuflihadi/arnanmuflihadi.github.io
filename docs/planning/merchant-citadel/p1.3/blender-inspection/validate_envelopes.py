"""P1.1 validation on ACTUAL assembled geometry (not nominal footprints). Headless Blender, read-only.

Run: Blender --background --factory-startup --python validate_envelopes.py -- <blockout.blend> <data_dir> <out.json>

Checks
  A  measured envelope of every structure (walls + roofs; and with signs / lanterns / props) vs its nominal footprint
  B  real gaps between neighbouring structure envelopes (roof overhangs included)
  C  height of every lantern and banner above the walking surface beneath it
  D  every walking edge sampled each 0.25 m: paved surface, step height, 0.34 m body clearance, headroom
  E  Exchange Hall stair profile
  F  clear opening of the timber arch module
  G  follow-camera line of sight along every edge, both directions, using the documented camera rig
Player and camera constants are copied from the project configuration; the production controller is not modified or run.
"""
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

blend, data_dir, out_path = sys.argv[sys.argv.index("--") + 1:][:3]
L = json.load(open(os.path.join(data_dir, "layout.json")))
RADIUS, HEIGHT, MAX_STEP = 0.34, 1.9, 0.42             # floating-atlas/collision.js, player-controller.js
CAM_DIST, CAM_UP, CAM_LOOK, CAM_PAD, CAM_MIN = 11.8, 6.6, 1.25, 0.28, 0.8   # urban-atlas/camera.js
HEADROOM_MIN, HANG_MIN = 2.0, 2.1

bpy.ops.wm.open_mainfile(filepath=blend)
town = bpy.data.collections["TOWN"]


def root_of(o):
    while o.parent:
        o = o.parent
    return o.name


cache = {}


def tris_of(o):
    me = o.data
    if me.name not in cache:
        me.calc_loop_triangles()
        v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", v)
        t = np.empty(len(me.loop_triangles) * 3, dtype=np.int32); me.loop_triangles.foreach_get("vertices", t)
        cache[me.name] = (v.reshape(-1, 3), t.reshape(-1, 3))
    v, t = cache[me.name]
    m = np.array(o.matrix_world)
    return v @ m[:3, :3].T + m[:3, 3], t


WALK_PREFIX = ("MV-Floor_", "MV-Stairs_Exterior_Straight")
objs = [o for o in town.objects if o.type == "MESH" and not o.name.startswith(("TMP_explorer", "TMP_yard"))]
allv, allt, owner, kind = [], [], [], []
env = {}
hang = []
nv = 0
for o in objs:
    v, t = tris_of(o)
    r = root_of(o)
    base = o.name.split(".")[0]
    walk = base.startswith(WALK_PREFIX) or base == "TMP_ground"
    allv.append(v); allt.append(t + nv); nv += len(v)
    owner += [(r, base)] * len(t); kind += [walk] * len(t)
    lo, hi = v.min(0), v.max(0)
    if r not in ("PAVING", "DRESSING") and not base.startswith("TMP_"):
        e = env.setdefault(r, {"struct": None, "full": None})
        structural = base.startswith("MV-") and not base.startswith(("MV-Prop_Wagon", "MV-Prop_Crate", "MV-Floor_", "MV-Stairs_"))
        for key in ("full",) + (("struct",) if structural else ()):
            e[key] = [lo.copy(), hi.copy()] if e[key] is None else [np.minimum(e[key][0], lo), np.maximum(e[key][1], hi)]
    if base.startswith(("FP-Lantern_Wall", "FP-Banner_", "CUS-Sign_", "AV-mdvl_village_sign_inn", "AV-mdvl_village_window_box")):   # wall vines protrude under 0.2 m: tested as obstacles on the walking edges instead
        hang.append((base, r, lo, hi))
V = np.vstack(allv); T = np.vstack(allt)
kind = np.array(kind)
verts = [Vector(p) for p in V.tolist()]
walk_idx = np.nonzero(kind)[0]; obst_idx = np.nonzero(~kind)[0]
bvh_walk = BVHTree.FromPolygons(verts, T[walk_idx].tolist())
bvh_obst = BVHTree.FromPolygons(verts, T[obst_idx].tolist())
print(f"[validate] {len(objs)} mesh objects, {len(T):,} triangles ({len(obst_idx):,} obstacle, {len(walk_idx):,} walkable)", flush=True)
r3 = lambda a: [round(float(x), 2) for x in a]
res = {"constants": {"capsule_radius": RADIUS, "player_height": HEIGHT, "max_step": MAX_STEP, "camera_distance": CAM_DIST, "camera_up": CAM_UP,
                     "headroom_min": HEADROOM_MIN, "hanging_min": HANG_MIN}, "triangles_tested": int(len(T))}

# ---- A envelopes ------------------------------------------------------------------------------------
nominal = {b["id"]: b for b in L["buildings"]}
A = []
for r, e in sorted(env.items()):
    if e["struct"] is None:
        continue
    bid = r.split("_")[0]
    s0, s1 = e["struct"]; f0, f1 = e["full"]
    row = {"root": r, "id": bid, "struct_x": r3([s0[0], s1[0]]), "struct_n": r3([s0[1], s1[1]]), "struct_size": r3(s1 - s0),
           "full_x": r3([f0[0], f1[0]]), "full_n": r3([f0[1], f1[1]]), "full_size": r3(f1 - f0)}
    if bid in nominal:
        x0, x1, n0, n1 = nominal[bid]["rect"]
        row.update(nominal_rect=[x0, x1, n0, n1], nominal_size=[x1 - x0, n1 - n0],
                   overhang_w_e_s_n=r3([x0 - s0[0], s1[0] - x1, n0 - s0[1], s1[1] - n1]))
    A.append(row)
res["A_envelopes"] = A

# ---- B gaps between real structure envelopes ----------------------------------------------------------
B = []
S = [(a["id"], a["struct_x"], a["struct_n"]) for a in A if not a["root"].startswith("S")]
for i in range(len(S)):
    for j in range(i + 1, len(S)):
        (ia, xa, na), (ib, xb, nb) = S[i], S[j]
        dx = max(xb[0] - xa[1], xa[0] - xb[1]); dn = max(nb[0] - na[1], na[0] - nb[1])
        gap = max(dx, dn)
        if gap < 3.0:
            B.append({"a": ia, "b": ib, "gap_m": round(gap, 2), "status": "FAIL" if gap < 0.3 else "NARROW" if gap < 1.0 else "OK"})
res["B_roof_gaps_under_3m"] = sorted(B, key=lambda g: g["gap_m"])

# ---- helpers ------------------------------------------------------------------------------------------
DOWN, UP = Vector((0, 0, -1)), Vector((0, 0, 1))


def ground(x, y, zfrom):
    loc, nrm, idx, dist = bvh_walk.ray_cast(Vector((x, y, zfrom)), DOWN, 30)
    if loc is None:
        return None, None
    return loc.z, owner[int(walk_idx[idx])]

# ---- C hanging objects ---------------------------------------------------------------------------------
C = []
for base, r, lo, hi in hang:
    cx, cy = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
    g, own = ground(cx, cy, lo[2] - 0.05)
    paved = bool(own and own[1].startswith(WALK_PREFIX))
    clr = None if g is None else round(float(lo[2] - g), 2)
    C.append({"asset": base, "on": r, "x": round(float(cx), 2), "n": round(float(cy), 2), "lowest_z": round(float(lo[2]), 2), "ground_z": None if g is None else round(g, 2),
              "clearance_m": clr, "over_paving": paved, "status": "FAIL" if (paved and clr is not None and clr < HANG_MIN) else "OK"})
res["C_hanging"] = sorted(C, key=lambda c: (c["clearance_m"] is None, c["clearance_m"]))

# ---- D / E walking edges -------------------------------------------------------------------------------
D = []
profile = []
for a, b, kindname in L["edges"]:
    (xa, na, _), (xb, nb, _) = L["nodes"][a], L["nodes"][b]
    length = math.hypot(xb - xa, nb - na); n = max(2, int(length / 0.25) + 1)
    zprev, _ = ground(xa, na, 3.0)
    zprev = 0.0 if zprev is None else zprev
    issues, unpaved, max_step, min_head, min_side = [], 0, 0.0, 99.0, 99.0
    for i in range(n):
        t = i / (n - 1); x, y = xa + (xb - xa) * t, na + (nb - na) * t
        g, own = ground(x, y, zprev + 1.9)
        if g is None:
            issues.append({"at": r3([x, y]), "issue": "no walkable surface"}); continue
        if not own[1].startswith(WALK_PREFIX):
            unpaved += 1
        step = abs(g - zprev); max_step = max(max_step, step)
        if step > MAX_STEP:
            issues.append({"at": r3([x, y]), "issue": f"step {step:.2f} m exceeds {MAX_STEP}"})
        for h in (0.5, 1.0, 1.5, 1.85):
            hit = bvh_obst.find_nearest(Vector((x, y, g + h)), RADIUS)
            if hit[0] is not None:
                issues.append({"at": r3([x, y]), "issue": f"body blocked at {h} m by {owner[int(obst_idx[hit[2]])]}"}); break
        near = bvh_obst.find_nearest(Vector((x, y, g + 1.0)), 4.0)
        if near[0] is not None:
            min_side = min(min_side, near[3])
        up = bvh_obst.ray_cast(Vector((x, y, g + 0.3)), UP, 20)
        if up[0] is not None:
            head = up[3] + 0.3; min_head = min(min_head, head)
            if head < HEADROOM_MIN:
                issues.append({"at": r3([x, y]), "issue": f"headroom {head:.2f} m under {owner[int(obst_idx[up[2]])]}"})
        if (a, b) == ("N07", "N08"):
            profile.append([round(y, 2), round(g, 3)])
        zprev = g
    uniq = []
    for it in issues:
        if not uniq or uniq[-1]["issue"] != it["issue"]:
            uniq.append(it)
    D.append({"edge": f"{a}-{b}", "type": kindname, "length_m": round(length, 1), "samples": n, "unpaved_samples": unpaved, "max_step_m": round(max_step, 2),
              "min_headroom_m": None if min_head > 90 else round(min_head, 2), "min_side_clearance_m": None if min_side > 90 else round(min_side, 2),
              "status": "RESERVED (not built in P1-P3)" if kindname.startswith("reserved") else "FAIL" if (uniq or unpaved) else "PASS", "issues": uniq[:6]})
res["D_edges"] = D
risers = []
for (y0, z0), (y1, z1) in zip(profile, profile[1:]):
    if z1 - z0 > 0.02:
        risers.append(round(z1 - z0, 3))
res["E_stairs"] = {"edge": "N07-N08", "risers_m": risers, "riser_count": len(risers), "max_riser_m": max(risers) if risers else None,
                   "total_rise_m": round(sum(risers), 3), "limit_m": MAX_STEP}

# ---- F arch opening --------------------------------------------------------------------------------------
arch = next(o for o in town.objects if o.name.split(".")[0] == "MV-Wall_Arch")
me = arch.data; me.calc_loop_triangles()
av = [v.co.copy() for v in me.vertices]
ab = BVHTree.FromPolygons(av, [tuple(t.vertices) for t in me.loop_triangles])
ymid = (min(v.y for v in av) + max(v.y for v in av)) / 2
F = {"module": "MV-Wall_Arch", "module_width_m": 2.0}
for h in (0.5, 1.0, 1.5, 1.9, 2.2):
    r_ = ab.ray_cast(Vector((0, ymid, h)), Vector((1, 0, 0)), 3); l_ = ab.ray_cast(Vector((0, ymid, h)), Vector((-1, 0, 0)), 3)
    F[f"clear_width_at_{h}m"] = None if (r_[0] is None or l_[0] is None) else round(r_[3] + l_[3], 2)
u = ab.ray_cast(Vector((0, ymid, 0.05)), UP, 5)
F["clear_height_centre_m"] = None if u[0] is None else round(u[3] + 0.05, 2)
F["passable_for_capsule"] = bool(F.get("clear_width_at_1.0m") and F["clear_width_at_1.0m"] >= 2 * RADIUS + 0.2 and F["clear_height_centre_m"] and F["clear_height_centre_m"] >= HEIGHT + 0.1)
res["F_arch"] = F

# ---- G follow camera ---------------------------------------------------------------------------------------
G = []
for a, b, kindname in L["edges"]:
    if kindname.startswith("reserved"):
        continue
    for p, q in ((a, b), (b, a)):
        (xa, na, _), (xb, nb, _) = L["nodes"][p], L["nodes"][q]
        length = math.hypot(xb - xa, nb - na)
        if length < 1e-6:
            continue
        dx, dy = (xb - xa) / length, (nb - na) / length
        n = max(2, int(length / 0.5) + 1)
        clear_n, mins, blockers = 0, 99.0, {}
        for i in range(n):
            t = i / (n - 1); x, y = xa + (xb - xa) * t, na + (nb - na) * t
            g, _ = ground(x, y, 3.0)
            g = 0.0 if g is None else g
            origin = Vector((x, y, g + CAM_LOOK)); desired = Vector((x - dx * CAM_DIST, y - dy * CAM_DIST, g + CAM_UP))
            d = desired - origin; full = d.length
            hit = bvh_obst.ray_cast(origin, d.normalized(), full)
            if hit[0] is None:
                clear_n += 1; avail = full
            else:
                avail = max(CAM_MIN, hit[3] - CAM_PAD)
                o_ = owner[int(obst_idx[hit[2]])]; blockers[o_[0]] = blockers.get(o_[0], 0) + 1
            mins = min(mins, avail)
        G.append({"travel": f"{p}->{q}", "type": kindname, "samples": n, "unobstructed_pct": round(100 * clear_n / n), "min_camera_distance_m": round(mins, 2),
                  "full_distance_m": round(math.hypot(CAM_DIST, CAM_UP - CAM_LOOK), 2), "main_blockers": sorted(blockers, key=blockers.get, reverse=True)[:3]})
res["G_camera"] = G

fails = {"B": [g for g in B if g["status"] == "FAIL"], "C": [c for c in C if c["status"] == "FAIL"], "D": [d for d in D if d["status"] == "FAIL"]}
res["summary"] = {"roof_gaps_fail": len(fails["B"]), "roof_gaps_narrow": len([g for g in B if g["status"] == "NARROW"]), "hanging_fail": len(fails["C"]),
                  "edges_total": len(D), "edges_fail": len(fails["D"]), "stairs_ok": bool(risers) and max(risers) <= MAX_STEP, "arch_passable": F["passable_for_capsule"],
                  "camera_edges_fully_clear": len([g for g in G if g["unobstructed_pct"] == 100]), "camera_travel_directions": len(G),
                  "camera_min_distance_m": min(g["min_camera_distance_m"] for g in G)}
json.dump(res, open(out_path, "w"), indent=1)
print("[validate] summary", json.dumps(res["summary"]))
for g in sorted(B, key=lambda g: g["gap_m"])[:10]:
    print("[validate] gap", g)
for c in [c for c in res["C_hanging"] if c["clearance_m"] is not None][:8]:
    print("[validate] hang", c["asset"], c["on"], c["clearance_m"], c["over_paving"], c["status"])
for d in fails["D"]:
    print("[validate] edge FAIL", d["edge"], "unpaved", d["unpaved_samples"], d["issues"][:3])
print("[validate] stairs", res["E_stairs"]); print("[validate] arch", F)
for g in [g for g in G if g["type"].startswith("primary")]:
    print("[validate] cam-primary", g["travel"], g["unobstructed_pct"], g["min_camera_distance_m"], g["main_blockers"])
for g in sorted(G, key=lambda g: g["min_camera_distance_m"])[:6]:
    print("[validate] cam", g["travel"], g["unobstructed_pct"], g["min_camera_distance_m"], g["main_blockers"])
