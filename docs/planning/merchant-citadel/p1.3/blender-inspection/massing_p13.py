"""Headless Blender: MASSING comparison of the P1.3 layout alternatives (and the P1.2 baseline).

Run: Blender --background --factory-startup --python massing_p13.py -- <p1.2 data dir> <out_dir> <p1.3 archetypes.json>

Simplified massing only: wall boxes and gable-roof prisms built from the real module dimensions of each archetype
(2 m bays, 3 m storeys, measured roof rise / eave drop / half width). No downloaded model is used here; this is a
measuring and comparison tool, not a visual concept. Gold roofs = buildings that do not exist in P1.2.
Outputs: massing-<alt>.png (one consistent aerial camera) and massing-metrics.json (hall sightlines, follow-camera ray test).
"""
import bpy, json, math, os, sys
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layouts_p13 as LY

data_dir, out_dir, arch_json = sys.argv[sys.argv.index("--") + 1:][:3]
ARCH = json.load(open(arch_json))            # P1.3 archetypes (P1.2 set plus the shallow house A03c)
L12 = json.load(open(os.path.join(data_dir, "layout.json")))
os.makedirs(out_dir, exist_ok=True)
ROOF = {2: (1.9, 0.3, 1.5), 4: (3.73, 0.52, 2.757), 6: (4.89, 0.78, 4.125), 8: (6.0, 0.78, 4.976)}
CAM_DIST, CAM_UP, CAM_LOOK = 11.8, 6.6, 1.25
TARGETS = {"tower seal": (0, 81.6, 11.5), "porch gable": (0, 76.6, 6.0)}
SIGHT = ["N01", "N02", "N03", "N04", "N05", "N27", "N06", "N07", "N10", "N13", "N11", "N14", "N23", "N24", "N16"]


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
    rise, drop, hw = ROOF[span]
    hl = length / 2 + 0.45
    sec = [(-hw, top - drop), (hw, top - drop), (0, top + rise)]
    v = []
    for e in (-hl, hl):
        for a, z in sec:
            lx, ly = (a, e) if ridge == "y" else (e, a)
            v.append((*tf(cx + lx, cy + ly, rz, ox, on), z))
    return mesh(name, v, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], material)


def building(bid, arch, x, n, rz, new, objs):
    A = ARCH[arch]
    wall, stone = mat("wall", (0.83, 0.76, 0.62)), mat("stone", (0.45, 0.44, 0.42))
    for p in A["parts"]:
        W, D, fl = p["W"], p["D"], p["floors"]; ox, oy, oz = p.get("offset", (0, 0, 0)); f0 = p.get("floor_from", 0)
        civic = bool(p.get("roof_variant"))
        rm = mat("roof_new", (0.86, 0.62, 0.10)) if new else mat("roof_civic", (0.34, 0.14, 0.09)) if civic else mat("roof", (0.52, 0.22, 0.12))
        top = oz + fl * 3
        if p.get("core", True):
            objs.append(box(bid + "_w", ox, oy, W, D, oz + f0 * 3, top, rz, x, n, stone if arch in ("A01", "A06", "A07") and f0 == 0 and fl <= 2 and arch != "A01" else wall))
        else:
            for sx in (-1, 1):
                for sy in (-1, 1):
                    objs.append(box(bid + "_p", ox + sx * (W / 2 - 0.15), oy + sy * (D / 2 - 0.15), 0.3, 0.3, oz, top, rz, x, n, mat("post", (0.30, 0.20, 0.13))))
        if p.get("roof"):
            span, length = (int(v) for v in p["roof"].split("x"))
            sx, sy = p.get("roof_shift", (0, 0))
            if p.get("jetty") is not None:
                length += 2; sy -= 1
            objs.append(prism(bid + "_r", ox + sx, oy + sy, span, length, p.get("ridge", "y"), top, rz, x, n, rm))
        if p.get("tower_roof"):
            v = [(*tf(ox + a, oy + b_, rz, x, n), top - 0.5) for a, b_ in ((-2.8, -2.8), (2.8, -2.8), (2.8, 2.8), (-2.8, 2.8))] + [(*tf(ox, oy, rz, x, n), top + 6.8)]
            objs.append(mesh(bid + "_t", v, [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (3, 2, 1, 0)], rm))
    if arch == "A01":
        objs.append(box(bid + "_pod", 0, -2, 28, 16, 0, 1.0, rz, x, n, stone))
    if arch == "A08":
        objs.append(box(bid + "_ver", 0, -4, 6, 2, 2.85, 3.0, rz, x, n, mat("post", (0.30, 0.20, 0.13))))


def scene(key, title, buildings, paving, yards, stalls):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            sc.render.engine = eng; break
        except TypeError:
            continue
    sc.render.resolution_x, sc.render.resolution_y = 1400, 900
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.80, 0.84, 0.88, 1)
    sun = bpy.data.objects.new("SUN", bpy.data.lights.new("SUN", "SUN")); sc.collection.objects.link(sun)
    sun.data.energy = 2.4; sun.data.angle = math.radians(3); sun.rotation_euler = (math.radians(52), 0, math.radians(-34))
    box("ground", 0, 40, 600, 600, -0.3, -0.02, 0, 0, 0, mat("ground", (0.36, 0.43, 0.27)))
    PV = {"MV-Floor_UnevenBrick": (0.55, 0.53, 0.49), "MV-Floor_Brick": (0.66, 0.60, 0.52), "MV-Floor_RedBrick": (0.62, 0.42, 0.32)}
    for i, pv in enumerate(paving):
        _, x0, x1, n0, n1, tile = pv[:6]
        box("pave", (x0 + x1) / 2, (n0 + n1) / 2, x1 - x0, n1 - n0, -0.02, 0.0 + 0.001 * i, 0, 0, 0, mat(tile, PV[tile]))
    for _, x0, x1, n0, n1 in yards:
        box("yard", (x0 + x1) / 2, (n0 + n1) / 2, x1 - x0, n1 - n0, -0.02, -0.005, 0, 0, 0, mat("earth", (0.52, 0.43, 0.30)))
    objs = []
    for b in buildings:
        building(b[0], b[1], b[3], b[4], b[5], b[8] == "new", objs)
    for gx in (-3, 3):   # gate lodges and market cross (unchanged structures)
        for sx in (-1, 1):
            for sy in (-1, 1):
                objs.append(box("gate_p", gx + sx * 0.85, 5 + sy * 1.85, 0.3, 0.3, 0, 3, 0, 0, 0, mat("post", (0.30, 0.20, 0.13))))
        objs.append(prism("gate_r", gx, 5, 2, 4, "y", 3, 0, 0, 0, mat("roof_civic", (0.34, 0.14, 0.09))))
    objs.append(box("cross", 0, 49, 0.4, 0.4, 0, 4, 0, 0, 0, mat("post", (0.30, 0.20, 0.13))))
    for s in stalls:
        w_, d_ = (1.0, 2.0) if s[4] in (90, -90) else (2.0, 1.0)
        box("stall", s[2], s[3], w_, d_, 0, 2.3, 0, 0, 0, mat("stall", (0.30, 0.40, 0.55)))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (52, -66, 70); cam.rotation_euler = (Vector(cam.location) - Vector((2, 40, 2))).to_track_quat("Z", "Y").to_euler()
    cam.data.sensor_fit = "VERTICAL"; cam.data.angle_y = math.radians(36); cam.data.clip_end = 1500
    sc.render.filepath = os.path.join(out_dir, f"massing-{key}.png"); bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.update()
    verts, polys = [], []
    for o in objs:
        base = len(verts); verts += [o.matrix_world @ v.co for v in o.data.vertices]; polys += [tuple(base + i for i in p.vertices) for p in o.data.polygons]
    return BVHTree.FromPolygons(verts, polys)


def measure(bvh, nodes, edges):
    vis = {}
    for k in SIGHT:
        if k not in nodes:
            continue
        x, n = nodes[k][:2]; eye = Vector((x, n, 1.65)); row = {}
        for tn, t in TARGETS.items():
            d = Vector(t) - eye; hit = bvh.ray_cast(eye, d.normalized(), d.length - 0.3)
            row[tn] = hit[0] is None
        vis[k] = row
    cam = []
    for a, b, kind in edges:
        if kind.startswith("reserved"):
            continue
        for p, q in ((a, b), (b, a)):
            pa, pb = Vector(nodes[p][:2]), Vector(nodes[q][:2]); L = (pb - pa).length; u = (pb - pa) / L
            n_s = max(2, int(L)); clear = 0; mind = 99.0
            for i in range(n_s + 1):
                pos = pa + u * (L * i / n_s)
                look = Vector((pos.x, pos.y, CAM_LOOK)); c = Vector((pos.x - u.x * CAM_DIST, pos.y - u.y * CAM_DIST, CAM_UP))
                d = c - look; hit = bvh.ray_cast(look, d.normalized(), d.length)
                if hit[0] is None:
                    clear += 1
                else:
                    mind = min(mind, (hit[0] - look).length)
            cam.append({"travel": f"{p}->{q}", "type": kind.split(",")[0], "clear_pct": round(100 * clear / (n_s + 1)), "min_dist": round(mind, 1) if mind < 99 else None})
    return {"hall_visibility": vis, "camera": cam}


res = {}
b12 = [(k, v[0], "", v[1], v[2], v[3], k, None, "kept") for k, v in LY.P12.items()]
res["P12"] = measure(scene("P12", "P1.2 baseline", b12, L12["paving"], L12.get("yards", []), [(s["id"], s["kit"], s["x"], s["n"], s["rz"]) for s in L12["stalls"]]),
                     {k: tuple(v) for k, v in L12["nodes"].items()}, [tuple(e) for e in L12["edges"]])
for key, alt in LY.ALTS.items():
    res[key] = measure(scene(key, alt["title"], alt["buildings"], alt["paving"], alt["yards"], alt["stalls"]), alt["nodes"], alt["edges"])
    print("[massing]", key, len(alt["buildings"]), "buildings", flush=True)
json.dump(res, open(os.path.join(out_dir, "massing-metrics.json"), "w"), indent=1)
print("[massing] done")
