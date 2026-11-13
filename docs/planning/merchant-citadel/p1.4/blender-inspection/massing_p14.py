"""Headless Blender: MASSING comparison and measurement of the P1.4 layout alternatives (B = P1.3 selected, D, E).

Run: Blender --background --factory-startup --python massing_p14.py -- <p1.4 archetypes.json> <out_dir>

Boxes and roof prisms at the real module dimensions of each archetype; no downloaded model. Gold roofs = buildings that the
P1.3 layout does not have (or has as a different type). Writes massing-<alt>.png (one aerial camera) and alternatives.json:
enclosure of street and court edges, hall sightlines at eye height, follow-camera ray test, counts, envelope, triangle estimate.
"""
import bpy, json, math, os, sys, collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layouts_p14 as LY

arch_json, out_dir = sys.argv[sys.argv.index("--") + 1:][:2]
ARCH = json.load(open(arch_json)); os.makedirs(out_dir, exist_ok=True)
AREP = json.load(open(os.path.join(os.path.dirname(arch_json), "..", "archetypes", "archetype-report.json")))
ROOF = {2: (1.9, 0.3, 1.5), 4: (3.73, 0.52, 2.757), 6: (4.89, 0.78, 4.125), 8: (6.0, 0.78, 4.976)}
CAM_DIST, CAM_UP, CAM_LOOK = 11.8, 6.6, 1.25
SIGHT = ["N01", "N02", "N03", "N04", "N05", "N27", "N06", "N07", "N10", "N13", "N11", "N14", "N23", "N24", "N16"]
PRIM = ["N01", "N02", "N03", "N04", "N05", "N29", "N27", "N06", "N07", "N08"]


def mat(name, rgb):
    m = bpy.data.materials.get(name)
    if not m:
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = 0.9
    return m


def mesh(name, verts, faces, material):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); me.materials.append(material)
    return o


def tf(x, y, rz, ox, on):
    a = math.radians(rz); c, s = math.cos(a), math.sin(a)
    return (ox + x * c - y * s, on + x * s + y * c)


def box(name, cx, cy, w, d, z0, z1, rz, ox, on, material):
    pts = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    v = [(*tf(cx + px, cy + py, rz, ox, on), z) for z in (z0, z1) for px, py in pts]
    return mesh(name, v, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], material)


def prism(name, cx, cy, span, length, ridge, top, rz, ox, on, material):
    rise, drop, hw = ROOF[span]; hl = length / 2 + 0.45
    sec = [(-hw, top - drop), (hw, top - drop), (0, top + rise)]; v = []
    for e in (-hl, hl):
        for a, z in sec:
            lx, ly = (a, e) if ridge == "y" else (e, a)
            v.append((*tf(cx + lx, cy + ly, rz, ox, on), z))
    return mesh(name, v, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], material)


def building(b, new, objs):
    bid, arch, _, x, n, rz = b[:6]; A = ARCH[arch]; ez = ((b[7] or {}).get("elev", 0.0)) if len(b) > 7 else 0.0
    wall, stone, post = mat("wall", (0.83, 0.76, 0.62)), mat("stone", (0.45, 0.44, 0.42)), mat("post", (0.30, 0.20, 0.13))
    for p in A["parts"]:
        W, D, fl = p["W"], p["D"], p["floors"]; ox, oy, oz = p.get("offset", (0, 0, 0)); oz += ez; f0 = p.get("floor_from", 0)
        rm = mat("roof_new", (0.86, 0.62, 0.10)) if new else mat("roof_civic", (0.34, 0.14, 0.09)) if p.get("roof_variant") else mat("roof", (0.52, 0.22, 0.12))
        top = oz + fl * 3
        if p.get("core", True):
            objs.append(box(bid + "_w", ox, oy, W, D, oz + f0 * 3, top, rz, x, n, wall))
        else:
            for sx in (-1, 1):
                for sy in (-1, 1):
                    objs.append(box(bid + "_p", ox + sx * (W / 2 - 0.15), oy + sy * (D / 2 - 0.15), 0.3, 0.3, oz, top, rz, x, n, post))
        if p.get("roof"):
            span, length = (int(v) for v in p["roof"].split("x")); sx, sy = p.get("roof_shift", (0, 0))
            if p.get("jetty") is not None:
                length += 2; sy -= 1
            objs.append(prism(bid + "_r", ox + sx, oy + sy, span, length, p.get("ridge", "y"), top, rz, x, n, rm))
        if p.get("tower_roof"):
            v = [(*tf(ox + a, oy + c, rz, x, n), top - 0.5) for a, c in ((-2.8, -2.8), (2.8, -2.8), (2.8, 2.8), (-2.8, 2.8))] + [(*tf(ox, oy, rz, x, n), top + 6.8)]
            objs.append(mesh(bid + "_t", v, [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (3, 2, 1, 0)], rm))
    if arch == "A01":
        objs.append(box(bid + "_pod", 0, -2, 28, 16, 0, 1.0 + ez, rz, x, n, stone))
    if arch in ("A08", "A09"):
        d2 = ARCH[arch]["footprint"][1] / 2
        objs.append(box(bid + "_ver", 0, -d2 - 1, 6, 2, 2.85, 3.0, rz, x, n, post))


def scene(key, alt):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            sc.render.engine = eng; break
        except TypeError:
            continue
    sc.render.resolution_x, sc.render.resolution_y = 1400, 900; sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.80, 0.84, 0.88, 1)
    sun = bpy.data.objects.new("SUN", bpy.data.lights.new("SUN", "SUN")); sc.collection.objects.link(sun)
    sun.data.energy = 2.4; sun.data.angle = math.radians(3); sun.rotation_euler = (math.radians(52), 0, math.radians(-34))
    box("ground", 0, 40, 600, 600, -0.3, -0.02, 0, 0, 0, mat("ground", (0.36, 0.43, 0.27)))
    PV = {"MV-Floor_UnevenBrick": (0.55, 0.53, 0.49), "MV-Floor_Brick": (0.66, 0.60, 0.52), "MV-Floor_RedBrick": (0.62, 0.42, 0.32)}
    objs = []
    for i, pv in enumerate(alt["paving"]):
        x0, x1, n0, n1, tile = pv[1:6]; z = pv[6] if len(pv) > 6 else 0.0
        parts = [(x0, x1, n0, n1, False)]
        if alt["swing"] and n0 < 18:
            parts = [(x0, x1, n0, min(n1, 18), True)] + ([(x0, x1, 18, n1, False)] if n1 > 18 else [])
        for a, b_, c, d, sw in parts:
            px, pn = LY.PIVOT
            o = box("pave", (a + b_) / 2 - (px if sw else 0), (c + d) / 2 - (pn if sw else 0), b_ - a, d - c, -0.02, z + 0.001 * i, LY.THETA if sw else 0, px if sw else 0, pn if sw else 0, mat(tile, PV[tile]))
            if z > 0:
                objs.append(o)
    for y in alt["yards"]:
        box("yard", (y[1] + y[2]) / 2, (y[3] + y[4]) / 2, y[2] - y[1], y[4] - y[3], -0.02, -0.005, 0, 0, 0, mat("earth", (0.52, 0.43, 0.30)))
    base = {b[0]: b[1] for b in LY.ALTS["B"]["buildings"]}
    for b in alt["buildings"]:
        building(b, key != "B" and base.get(b[0]) != b[1], objs)
    gx, gn = (0, 5)
    for sx in (-3, 3):
        cx, cn = LY.swing(sx, 5) if alt["swing"] else (sx, 5); r = LY.THETA if alt["swing"] else 0
        objs.append(prism("gate_r", 0, 0, 2, 4, "y", 3, r, cx, cn, mat("roof_civic", (0.34, 0.14, 0.09))))
        for a in (-0.85, 0.85):
            for c in (-1.85, 1.85):
                objs.append(box("gate_p", a, c, 0.3, 0.3, 0, 3, r, cx, cn, mat("post", (0.30, 0.20, 0.13))))
    objs.append(box("cross", 0, 49, 0.4, 0.4, 0, 4, 0, 0, 0, mat("post", (0.30, 0.20, 0.13))))
    for s in alt["stalls"]:
        w_, d_ = (1.0, 2.0) if abs(s[4]) == 90 else (2.0, 1.0)
        box("stall", s[2], s[3], w_, d_, 0, 2.3, 0, 0, 0, mat("stall", (0.30, 0.40, 0.55)))
    for r in alt["rows"]:
        objs.append(box("row", 0, 0, 8, 1.6, 2.5, 3.2, r[4], r[2], r[3], mat("stall", (0.30, 0.40, 0.55) if r[1] == "provisions" else (0.50, 0.22, 0.25))))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (52, -66, 70); cam.rotation_euler = (Vector(cam.location) - Vector((2, 40, 2))).to_track_quat("Z", "Y").to_euler()
    cam.data.sensor_fit = "VERTICAL"; cam.data.angle_y = math.radians(36); cam.data.clip_end = 1500
    sc.render.filepath = os.path.join(out_dir, f"massing-{key}.png"); bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.update()
    verts, polys = [], []
    for o in objs:
        b0 = len(verts); verts += [o.matrix_world @ v.co for v in o.data.vertices]; polys += [tuple(b0 + i for i in p.vertices) for p in o.data.polygons]
    return BVHTree.FromPolygons(verts, polys)


def evaluate(key, alt, bvh):
    N, E, bs = alt["nodes"], alt["edges"], alt["buildings"]
    ez = 1.0 if key != "B" else 0.0
    targets = {"tower seal": (0, 81.6, 11.5 + (4.0 if key != "B" else 0)), "porch gable": (0, 76.6, 6.0 + ez)}
    zof = lambda k: (1.0 if (key != "B" and k in ("N07", "N21", "N22")) else 0.0)
    vis = {}
    for k in SIGHT:
        if k in N:
            eye = Vector((N[k][0], N[k][1], 1.65 + zof(k)))
            vis[k] = {tn: bvh.ray_cast(eye, (Vector(t) - eye).normalized(), (Vector(t) - eye).length - 0.3)[0] is None for tn, t in targets.items()}
    cam = []
    for a, b, kind in E:
        if kind.startswith("reserved"):
            continue
        for p, q in ((a, b), (b, a)):
            pa, pb = Vector(N[p][:2]), Vector(N[q][:2]); Lg = (pb - pa).length; u = (pb - pa) / Lg; n_s = max(2, int(Lg)); clear = 0
            for i in range(n_s + 1):
                pos = pa + u * (Lg * i / n_s); z = max(zof(p), zof(q)) if key != "B" and min(N[p][1], N[q][1]) > 61 else 0
                look = Vector((pos.x, pos.y, CAM_LOOK + z)); c = Vector((pos.x - u.x * CAM_DIST, pos.y - u.y * CAM_DIST, CAM_UP + z)); d = c - look
                clear += bvh.ray_cast(look, d.normalized(), d.length)[0] is None
            cam.append({"travel": f"{p}->{q}", "type": kind.split(",")[0], "clear_pct": round(100 * clear / (n_s + 1))})
    polys = [LY.corners(b) for b in bs]
    xs = [v for pl in polys for v, _ in pl] + [v for p in alt["paving"] for v in p[1:3]]; ns = [v for pl in polys for _, v in pl] + [v for p in alt["paving"] for v in p[3:5]]
    env = (min(xs), max(xs), min(ns), max(ns)); area = sum(LY.FOOT[b[1]][0] * LY.FOOT[b[1]][1] for b in bs)
    ln = lambda p, q: math.hypot(N[p][0] - N[q][0], N[p][1] - N[q][1])
    enc = {l[0]: LY.enclosure(bs, l) for l in alt["lines"]}
    grp = collections.OrderedDict()
    for g in ("Merchant street", "Artisan lane", "Warehouse lane", "Bazaar", "Arrival court", "Civic"):
        ks = [k for k in enc if k.startswith(g)]
        grp[g] = [round(sum(enc[k][0] * enc[k][i] for k in ks) / sum(enc[k][0] for k in ks)) for i in (1, 2)]
    tot = sum(v[0] for v in enc.values())
    base = {b[0]: b for b in LY.ALTS["B"]["buildings"]}
    tri = sum(AREP[b[1]]["triangles"] for b in bs) + (len(alt["rows"]) * AREP.get("A10p", {"triangles": 11000})["triangles"])
    sec = [c for c in cam if c["type"] != "primary"]
    return {"title": alt["title"], "buildings": len(bs), "new_buildings": sum(b[0] not in base for b in bs), "re_typed": sum(b[0] in base and base[b[0]][1] != b[1] for b in bs),
            "turned_or_moved": sum(b[0] in base and (base[b[0]][3:6] != b[3:6]) for b in bs), "archetypes": dict(sorted(collections.Counter(b[1] for b in bs).items())),
            "free_stalls": len(alt["stalls"]), "awning_rows": len(alt["rows"]), "envelope": [round(v, 1) for v in env], "envelope_size": [round(env[1] - env[0], 1), round(env[3] - env[2], 1)],
            "coverage_pct": round(100 * area / ((env[1] - env[0]) * (env[3] - env[2])), 1), "nodes": len(N), "edges": len(E), "loops": len(E) - len(N) + 1,
            "network_m": round(sum(ln(p, q) for p, q, k in E if not k.startswith("reserved")), 1), "primary_route_m": round(sum(ln(p, q) for p, q in zip(PRIM, PRIM[1:])), 1),
            "enclosure_lines": enc, "enclosure_groups": grp, "overall_wall_pct": round(sum(v[0] * v[1] for v in enc.values()) / tot), "overall_active_pct": round(sum(v[0] * v[2] for v in enc.values()) / tot),
            "building_triangles": tri, "camera_directions": len(cam), "camera_fully_clear": sum(c["clear_pct"] == 100 for c in cam),
            "camera_secondary_mean_clear_pct": round(sum(c["clear_pct"] for c in sec) / len(sec)), "camera_primary_northbound": [c for c in cam if c["travel"] in [f"{p}->{q}" for p, q in zip(PRIM, PRIM[1:])]],
            "tower_visible_from": [k for k, v in vis.items() if v["tower seal"]], "porch_visible_from": [k for k, v in vis.items() if v["porch gable"]], "points_tested": list(vis)}


RES = {}
for key, alt in LY.ALTS.items():
    RES[key] = evaluate(key, alt, scene(key, alt))
    r = RES[key]
    print("[massing]", key, r["buildings"], "bld", "env", r["envelope_size"], "wall/active", r["overall_wall_pct"], r["overall_active_pct"], dict(r["enclosure_groups"]), "cam", r["camera_fully_clear"], "/", r["camera_directions"],
          "sec", r["camera_secondary_mean_clear_pct"], "tower", len(r["tower_visible_from"]), r["tower_visible_from"], "porch", r["porch_visible_from"], "tris", r["building_triangles"], flush=True)
json.dump(RES, open(os.path.join(out_dir, "alternatives.json"), "w"), indent=1)
