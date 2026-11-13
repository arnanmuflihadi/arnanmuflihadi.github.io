"""Merchant Citadel P3-B batch 1: build the island meshes from p3b_model and export one GLB.

  Blender --background --python p3b_blender_build.py -- <out_dir> [--scene <scene.json>] [--blend <save.blend>]

Writes <out_dir>/merchant-citadel-p3b-island.glb, island-instances.json (vegetation, rocks, quay props, collision proxies) and island-build-stats.json.
Everything is generated; the only inputs are p3b_model.py, p3b_geo.py, p3b_props.py and the town scene.json (footprints for planting exclusions).
"""
import bpy, bmesh, sys, os, json, math, time
import numpy as np
from mathutils import geometry, Vector

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import p3b_model as M, p3b_geo as G, p3b_props as PR

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else os.path.join(here, "out"); os.makedirs(OUT, exist_ok=True)
SCENE = argv[argv.index("--scene") + 1] if "--scene" in argv else os.path.join(here, "../../../../merchant-citadel-p2a/data/scene.json")
BLEND = argv[argv.index("--blend") + 1] if "--blend" in argv else None
T0 = time.time(); STATS = {}


def log(*a):
    print("[p3b]", *a, flush=True)


# ---------------------------------------------------------------------------------------------------- scene and materials
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = bpy.data.collections.new("P3B_ISLAND"); scene.collection.children.link(col)


def material(name, rough=0.92, metal=0.0, rgb=None, emit=None, alpha=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); nt.links.new(bsdf.outputs[0], out.inputs[0])
    bsdf.inputs["Roughness"].default_value = rough; bsdf.inputs["Metallic"].default_value = metal
    if rgb is None:
        ca = nt.nodes.new("ShaderNodeVertexColor"); ca.layer_name = "Col"; nt.links.new(ca.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1.0); bsdf.inputs["Emission Strength"].default_value = 1.0
    return m


MAT = {"top": material("MI_P3B_Top", 0.96), "rock": material("MI_P3B_Rock", 0.94), "foliage": material("MI_P3B_Foliage", 0.88), "prop": material("MI_P3B_Prop", 0.85),
       "water": material("MI_P3B_Water_stream", 0.15, 0.0, (0.30, 0.55, 0.62)), "fall": material("MI_P3B_Water_fall", 0.2, 0.0, (0.80, 0.90, 0.95))}


def make_object(name, V, F, C=None, mat="top", smooth="smooth", uv=None, parent_col=None, matid=None):
    V = np.asarray(V, float); F = np.asarray(F, int)
    me = bpy.data.meshes.new(name); me.from_pydata(V.tolist(), [], F.tolist()); me.update()
    if C is not None:
        ca = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT"); rgba = np.column_stack([np.clip(C, 0, 1) ** 2.2, np.ones(len(V))]); ca.data.foreach_set("color", rgba.astype(np.float32).ravel())     # palette is authored as display colours; glTF vertex colours are linear
        me.color_attributes.active_color = ca; me.color_attributes.render_color_index = 0
    if matid is not None:
        at = me.attributes.new('_matid', 'FLOAT', 'POINT'); at.data.foreach_set('value', np.asarray(matid, np.float32))
    if uv is not None:
        uvl = me.uv_layers.new(name="UVMap"); loops = np.array([l.vertex_index for l in me.loops]); uvl.data.foreach_set("uv", np.asarray(uv, np.float32)[loops].ravel())
    ob = bpy.data.objects.new(name, me); (parent_col or col).objects.link(ob); ob.data.materials.append(MAT[mat] if isinstance(mat, str) else mat)
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    if smooth == "smooth":
        for p in me.polygons: p.use_smooth = True
    elif smooth == "angle":
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(26))
    ob.select_set(False); return ob


def tri_stats(ob):
    return len(ob.data.polygons)


# ---------------------------------------------------------------------------------------------------- top surfaces (constrained Delaunay inside the rim)
def build_top(c, terrain_fn, name):
    rim, pts = G.top_vertices(c, terrain_fn)
    verts = [tuple(p) for p in rim] + [tuple(p) for p in pts]
    n = len(rim)
    res = geometry.delaunay_2d_cdt([Vector(v) for v in verts], [], [list(range(n))], 1, 1e-4)
    rv, _e, rf = res[0], res[1], res[2]
    V = np.array([(v.x, v.y) for v in rv]); F = np.array(rf, int)
    z = terrain_fn(V[:, 0], V[:, 1]); V3 = np.column_stack([V, z])
    # orientation: make normals face up
    a, b, cc = V3[F[:, 0]], V3[F[:, 1]], V3[F[:, 2]]; flip = np.cross(b - a, cc - a)[:, 2] < 0; F[flip] = F[flip][:, ::-1]
    nrm = G.vertex_normals(V3, F)
    C, cls = G.top_colours(V3[:, 0], V3[:, 1], V3[:, 2], nrm[:, 2])
    return V3, F, C, cls


# ---------------------------------------------------------------------------------------------------- the build
log("model extents", json.dumps(M.extents()))
stats = {}
# main island: top + shell
t = time.time(); Vt, Ft, Ct, Kt = build_top(M.MAIN, M.terrain, "ISL_TOP"); ob = make_object("ISL_TOP", Vt, Ft, Ct, "top", "smooth", matid=Kt); stats["ISL_TOP"] = dict(tris=len(Ft), verts=len(Vt), s=round(time.time() - t, 1)); log("top", stats["ISL_TOP"])
t = time.time(); Vs, Fs, info = G.build_shell(M.MAIN); Cs = G.shell_colours(Vs, Fs, info); ob = make_object("ISL_CLIFF", Vs, Fs, Cs, "rock", "angle", matid=np.full(len(Vs), 3.0)); stats["ISL_CLIFF"] = dict(tris=len(Fs), verts=len(Vs), rings=info["rings"], rim_points=info["N"], s=round(time.time() - t, 1)); log("shell", stats["ISL_CLIFF"])
np.savez(os.path.join(OUT, "top-mesh.npz"), V=Vt, F=Ft)
# Tea Stack
Vt2, Ft2, Ct2, Kt2 = build_top(M.STACK, M.stack_top, "STACK_TOP"); make_object("STACK_TOP", Vt2, Ft2, Ct2, "top", "smooth", matid=Kt2); stats["STACK_TOP"] = dict(tris=len(Ft2))
Vs2, Fs2, info2 = G.build_shell(M.STACK); Cs2 = G.shell_colours(Vs2, Fs2, info2); make_object("STACK_CLIFF", Vs2, Fs2, Cs2, "rock", "angle", matid=np.full(len(Vs2), 3.0)); stats["STACK_CLIFF"] = dict(tris=len(Fs2), rings=info2["rings"])


# hanging roots (anchored on the real underside) and floating debris
def tapered_root(anchor, direction, length, r0, seed, rings=9, sides=7):
    rng = np.random.default_rng(seed); d = np.asarray(direction, float); d /= np.linalg.norm(d)
    a = np.cross(d, [0, 0, 1.0]); a /= np.linalg.norm(a) + 1e-9; b = np.cross(d, a); V = []; Cc = []
    for k in range(rings):
        t = k / (rings - 1); c = np.asarray(anchor, float) + d * (length * t - 2.0) + a * 1.6 * math.sin(t * 3 + seed) * t + b * 1.1 * math.sin(t * 2 + seed * 2) * t
        rad = r0 * ((1 - t) ** 1.2 * (1 + 0.28 * math.sin(t * 9 + seed)) + 0.05)
        for i in range(sides):
            ang = TAU * i / sides + t * 0.7; rr = rad * (1 + 0.22 * rng.uniform(-1, 1)); V.append(c + a * math.cos(ang) * rr + b * math.sin(ang) * rr)
    V = np.array(V); F = []
    for k in range(rings - 1):
        for i in range(sides):
            j = (i + 1) % sides; p, q, r_, s_ = k * sides + i, k * sides + j, (k + 1) * sides + i, (k + 1) * sides + j; F += [(p, q, r_), (q, s_, r_)]
    tip = len(V); V = np.vstack([V, V[-sides:].mean(0) - d * 0.8]); F += [((rings - 1) * sides + (i + 1) % sides, (rings - 1) * sides + i, tip) for i in range(sides)]
    return V, np.array(F)


TAU = M.TAU
rings_arr = None
Nn = info["N"]; nr = info["rings"]; ringV = Vs.reshape(nr, Nn, 3)
rng = np.random.default_rng(77); root_parts = []; roots = []
for k, (deg, ln, r0) in enumerate(((60, 34, 5.0), (95, 40, 5.6), (35, 28, 4.2), (140, 24, 4.0), (200, 20, 3.4), (330, 22, 3.6), (80, 26, 3.0))):
    th = math.radians(deg); i = int(np.argmin(np.abs(np.arctan2(np.sin(info["th"] - th), np.cos(info["th"] - th))))); anc = ringV[info["cliff_rings"] + 7, i]
    dirv = np.array([math.cos(th) * 0.12 + rng.uniform(-0.1, 0.1), math.sin(th) * 0.12 + rng.uniform(-0.1, 0.1), -1.0]); Vr, Fr = tapered_root(anc, dirv, ln, r0, 100 + k)
    root_parts.append((Vr, Fr)); roots.append(dict(bearing=deg, length=ln, anchor=[float(v) for v in anc]))
V0 = []; F0 = []; o = 0
for Vr, Fr in root_parts:
    V0.append(Vr); F0.append(Fr + o); o += len(Vr)
V0 = np.concatenate(V0); F0 = np.concatenate(F0); C0 = G.layer_colour(V0[:, 2], V0[:, 0], V0[:, 1]) * 0.62 + G.BASALT * 0.3
make_object("ISL_ROOTS", V0, F0, C0, "rock", "angle"); stats["ISL_ROOTS"] = dict(tris=len(F0), roots=len(roots))
deb = []; dparts = []
for k, deg in enumerate((12, 18, 154, 160, 238, 232, 100, 290, 330, 60, 200, 262)):
    th = math.radians(deg + rng.uniform(-6, 6)); i = int(np.argmin(np.abs(np.arctan2(np.sin(info["th"] - th), np.cos(info["th"] - th))))); p = info["pts"][i]; u = info["u"][i]; out_d = rng.uniform(9, 28); dz = rng.uniform(8, 44)
    c = (p[0] + u[0] * out_d, p[1] + u[1] * out_d, info["zr"][i] - dz); rad = rng.uniform(1.6, 4.8)
    V, F, _C = PR.ico(c, rad, 2, (1.0, 0.9, 0.6), 0.32, 300 + k)
    dparts.append((V, F)); deb.append(dict(centre=[float(v) for v in c], radius=float(rad)))
Vd = []; Fd = []; o = 0
for V, F in dparts:
    Vd.append(V); Fd.append(F + o); o += len(V)
Vd = np.concatenate(Vd); Fd = np.concatenate(Fd); nd = G.vertex_normals(Vd, Fd); Cd = G.layer_colour(Vd[:, 2], Vd[:, 0], Vd[:, 1]) * (0.8 + 0.2 * np.clip(nd[:, 2], 0, 1))[:, None]
Cd = np.where((nd[:, 2] > 0.6)[:, None], Cd * 0.5 + np.array([0.25, 0.38, 0.14]) * 0.5, Cd)
make_object("ISL_DEBRIS", Vd, Fd, Cd, "rock", "angle"); stats["ISL_DEBRIS"] = dict(tris=len(Fd), rocks=len(deb))

# P3-B batch 3 WP3: hero rock masses. Faceted, terraced, strata-coloured masses half-buried in the cliff face (buttresses, ledges, overhangs) and hanging masses under the island: they break the smooth
# streaked shell silhouette. Everything is outside the walkable surface (below the rim by >= 1.2 m), the walk mask and the physics grid are untouched.
def hero_mass(c, r, scale, seed, sub=2, step=0.34, amp=0.46):
    V, F, _c = PR.ico((0.0, 0.0, 0.0), 1.0, sub, (1, 1, 1), 0.0, seed); rg = np.random.default_rng(seed); ph = rg.uniform(0, 6.28, size=(4, 3)); fq = rg.uniform(1.6, 5.2, size=(4, 3))
    d = np.zeros(len(V))
    for k in range(4):
        d += np.sin(V @ (fq[k] * np.array([1.0, 1.0, 0.8])) + ph[k].sum()) * (0.5 ** (k * 0.5))
    V = V * (1 + amp * d / 3.0 + rg.uniform(-0.07, 0.07, size=len(V)))[:, None] * np.array(scale)                         # per-vertex jitter + flat shading = angular rock facets
    zt = V[:, 2] / step; V[:, 2] = V[:, 2] * 0.55 + 0.45 * (np.round(zt) * step)                                            # horizontal ledges: strata steps
    V = V * r + np.asarray(c, float); return V, np.asarray(F, int)


hv = []; hf = []; ho = 0; heroes = []; hr = np.random.default_rng(2026); nrm_sh = G.vertex_normals(Vs, Fs); cen = np.array([np.mean(info["pts"][:, 0]), np.mean(info["pts"][:, 1])])
fx0, fn0 = M.FALLS[0]
def add_hero(p, nrm, r, scale, seed, kind):
    global ho
    nrm = np.asarray(nrm, float); out_xy = p[:2] - cen
    if np.dot(nrm[:2], out_xy) < 0: nrm = -nrm
    c = p + nrm / (np.linalg.norm(nrm) + 1e-9) * 0.42 * r
    V, F = hero_mass(c, r, scale, seed)
    hv.append(V); hf.append(F + ho); ho += len(V); heroes.append(dict(kind=kind, centre=[round(float(v), 2) for v in c], r=round(float(r), 2)))
for k in range(56):                                                                                                         # cliff-face masses
    i = int((k * Nn / 56 + hr.integers(-5, 6)) % Nn); kr = int(hr.integers(2, info["cliff_rings"] + 6)); p = ringV[kr, i]; r = float(hr.uniform(2.4, 8.0)); sc = [(1.5, 0.9, 0.75), (0.9, 0.9, 1.7), (1.9, 1.1, 0.6), (1.2, 1.2, 1.2)][k % 4]
    if np.hypot(p[0] - fx0, p[1] - fn0) < 21.0: continue                                         # keep the Cloudfall notch clear for the water sheet
    if p[2] + r * sc[2] * 1.15 > info["zr"][i] - 1.2: r = max(1.8, (info["zr"][i] - 1.2 - p[2]) / (sc[2] * 1.15))
    add_hero(p, nrm_sh[kr * Nn + i], r, sc, 5000 + k, "cliff")
for k in range(22):                                                                                                         # hanging masses on the underside
    i = int((k * Nn / 22 + hr.integers(-12, 13)) % Nn); kr = int(hr.integers(info["cliff_rings"] + 3, nr - 3)); p = ringV[kr, i]; r = float(hr.uniform(4.0, 9.5)); sc = [(1.0, 1.0, 1.8), (1.5, 1.2, 1.1), (0.9, 0.9, 2.0)][k % 3]
    if np.hypot(p[0] - fx0, p[1] - fn0) < 21.0: continue
    add_hero(p, nrm_sh[kr * Nn + i], r, sc, 6000 + k, "underside")
Vh = np.concatenate(hv); Fh = np.concatenate(hf); nh = G.vertex_normals(Vh, Fh); Ch = G.layer_colour(Vh[:, 2], Vh[:, 0], Vh[:, 1]) * (0.82 + 0.28 * np.clip(0.5 + 0.5 * nh[:, 2], 0, 1))[:, None] * (1 - 0.30 * np.clip(-nh[:, 2], 0, 1))[:, None]
Ch = np.where((nh[:, 2] > 0.62)[:, None], Ch * 0.55 + np.array([0.26, 0.38, 0.14]) * 0.45, Ch)
Ch = Ch * 0.72 + G.BASALT * 0.28 * (0.8 + 0.4 * np.random.default_rng(3).random(len(Ch)))[:, None]
make_object("ISL_HEROES", Vh, Fh, Ch, "rock", "flat", matid=np.full(len(Vh), 3.0)); stats["ISL_HEROES"] = dict(tris=len(Fh), masses=len(heroes)); json.dump(heroes, open(os.path.join(OUT, "island-heroes.json"), "w"))

# P3-B batch 3 (crag pass): outcrop masses on the steep riser faces of the Counting Crag benches and summit shoulders. Candidates are grid cells that are NOT walkable (slope above the walk limit), at least
# 3.5 m from every path and clear of the flora trunk and boulder proxies; the masses are half-buried in the face. The walk mask, physics grid and every route are untouched.
spec = M.grid_spec(); Xg, Ng, hg = M.sample_grid(spec); edm = M.edge_distance(M.MAIN, Xg, Ng); eds = M.edge_distance(M.STACK, Xg, Ng); brg = M.bridge_height(Xg, Ng)
walk_g, comf_g, slope_g = M.masks(hg, edm, eds, brg)
flora_p = os.path.join(os.path.dirname(os.path.abspath(SCENE)), "island-flora.json"); fl = json.load(open(flora_p)) if os.path.exists(flora_p) else {"trunks": [], "rocks_solid": []}
solids = [(t["x"], t["n"], t["r"] + 1.2) for t in fl["trunks"]] + [(r["x"], r["n"], r["r"] + 1.0) for r in fl["rocks_solid"]]
cand = np.argwhere((~walk_g) & (~np.isnan(hg)) & (slope_g > 0.72) & (Xg > 5) & (Xg < 86) & (Ng > 93) & (Ng < 134))
cr = np.random.default_rng(4242); cr.shuffle(cand); crag_v = []; crag_f = []; co = 0; crag_info = []
for (j, i) in cand:
    if len(crag_info) >= 46: break
    x, n = float(Xg[j, i]), float(Ng[j, i]); r = float(cr.uniform(1.3, 3.4))
    if float(M.path_distance(np.array([x]), np.array([n]))[0]) < 3.0 + r * 0.4 or any(math.hypot(x - sx, n - sn) < sr + r * 0.5 for sx, sn, sr in solids) or any(math.hypot(x - c["x"], n - c["n"]) < 1.8 + 0.6 * (r + c["r"]) for c in crag_info): continue
    z = float(hg[j, i]); gy, gx = np.gradient(np.where(np.isnan(hg), M.NOSUP, hg), M.CELL); nrm = np.array([-gx[j, i], -gy[j, i]]); nrm = nrm / (np.hypot(*nrm) + 1e-9)       # downhill direction = outward from the face
    c = np.array([x + nrm[0] * 0.15 * r, n + nrm[1] * 0.15 * r, z + 0.1 * r]); V, F = hero_mass(c, r, (1.5, 1.0, 0.8) if len(crag_info) % 2 else (1.0, 1.0, 1.4), 7000 + len(crag_info), step=0.3, amp=0.46)
    crag_v.append(V); crag_f.append(F + co); co += len(V); crag_info.append(dict(x=round(x, 2), n=round(n, 2), r=round(r, 2), z=round(z, 2)))
if crag_v:
    Vc = np.concatenate(crag_v); Fc = np.concatenate(crag_f); nc = G.vertex_normals(Vc, Fc); Cc = G.layer_colour(Vc[:, 2], Vc[:, 0], Vc[:, 1]) * (0.8 + 0.3 * np.clip(0.5 + 0.5 * nc[:, 2], 0, 1))[:, None]
    Cc = np.where((nc[:, 2] > 0.62)[:, None], Cc * 0.55 + np.array([0.26, 0.38, 0.14]) * 0.45, Cc); Cc = Cc * 0.55 + G.BASALT * 0.45 * (0.8 + 0.4 * np.random.default_rng(5).random(len(Cc)))[:, None]
    make_object("ISL_CRAG", Vc, Fc, Cc, "rock", "flat", matid=np.full(len(Vc), 3.0)); stats["ISL_CRAG"] = dict(tris=len(Fc), masses=len(crag_info)); json.dump(crag_info, open(os.path.join(OUT, "island-crag-outcrops.json"), "w"))

# water: stream ribbon and the Cloudfall sheet
W = np.array(M.WATER, float); dense, _ = M._dense([tuple(p) for p in M.WATER], 0.8); sd = len(dense)
wid = np.linspace(0.55, 1.2, sd); tang = np.gradient(dense, axis=0); tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9; nor = np.column_stack([-tang[:, 1], tang[:, 0]])
L_ = dense + nor * wid[:, None]; R_ = dense - nor * wid[:, None]
zL = M.terrain(L_[:, 0], L_[:, 1]) + 0.07; zR = M.terrain(R_[:, 0], R_[:, 1]) + 0.07; zc = np.minimum(M.terrain(dense[:, 0], dense[:, 1]) + 0.08, np.minimum(zL, zR) + 0.0)
Vw = np.vstack([np.column_stack([L_, np.minimum(zL, zc + 0.02)]), np.column_stack([R_, np.minimum(zR, zc + 0.02)])]); Fw = []
for i in range(sd - 1):
    Fw += [(i, i + 1, sd + i), (i + 1, sd + i + 1, sd + i)]
sl = np.cumsum(np.r_[0, np.linalg.norm(np.diff(dense, axis=0), axis=1)]); UVw = np.vstack([np.column_stack([np.zeros(sd), sl / 3.0]), np.column_stack([np.ones(sd), sl / 3.0])])
make_object("WATER_STREAM", Vw, np.array(Fw), None, "water", "smooth", uv=UVw); stats["WATER_STREAM"] = dict(tris=len(Fw))
fx, fn = M.FALLS[0]; ri = int(np.argmin(np.hypot(info["pts"][:, 0] - fx, info["pts"][:, 1] - fn))); K = list(range(0, 1 + info["cliff_rings"]))
fl = []; fr = []; fall_rows = []
for k in K:
    c = ringV[k, ri - 1:ri + 2].mean(0); u = info["u"][ri]; w = 1.4 + 0.18 * k; off = u * (0.3 + 0.05 * k); tx = np.array([-u[1], u[0], 0])
    fl.append(c + np.array([off[0], off[1], 0]) + tx * w); fr.append(c + np.array([off[0], off[1], 0]) - tx * w)
Vf = np.vstack([fl, fr]); nk = len(K); Ff = []
for i in range(nk - 1):
    Ff += [(i, i + 1, nk + i), (i + 1, nk + i + 1, nk + i)]
UVf = np.vstack([np.column_stack([np.zeros(nk), np.arange(nk) * 0.25]), np.column_stack([np.ones(nk), np.arange(nk) * 0.25])])
make_object("WATER_FALL", Vf, np.array(Ff), None, "fall", "smooth", uv=UVf); stats["WATER_FALL"] = dict(tris=len(Ff), lip_z=float(Vf[0, 2]), bottom_z=float(Vf[nk - 1, 2]), height_m=float(Vf[0, 2] - Vf[nk - 1, 2]))


# bridge to the Tea Stack (optional exploration): deck, posts, rope rails
def bridge():
    nm, w, a, b, za, zb = M.BRIDGE; a = np.array(a); b = np.array(b); ab = b - a; L = float(np.linalg.norm(ab)); yaw = math.atan2(ab[1], ab[0]); pitch = math.atan2(zb - za, L)
    def xf(V, s, o):  # local (x along the bridge, y across, z up) at arc position s
        cp, sp, cy, sy = math.cos(pitch), math.sin(pitch), math.cos(yaw), math.sin(yaw); x = V[:, 0] * cp - V[:, 2] * sp + s; z = V[:, 0] * sp + V[:, 2] * cp
        X = x * cy - V[:, 1] * sy; Y = x * sy + V[:, 1] * cy; return np.column_stack([X + a[0], Y + a[1], z + za + o])
    parts = []
    for k in range(int(L / 0.55)):
        s = 0.28 + k * 0.55; V, F, C = PR.box((0, 0, 0), (0.5, w, 0.09), PR.WOOD if k % 3 else PR.WOOD_D, 0.008, k); parts.append((xf(V, s, -0.05), F, C))
    for sgn in (-1, 1):
        V, F, C = PR.box((L / 2, sgn * (w / 2 - 0.05), 0.95), (L, 0.06, 0.07), PR.ROPE); parts.append((xf(V, 0, 0) if False else (lambda VV: xf(VV, 0, 0))(V), F, C))
        V, F, C = PR.box((L / 2, sgn * (w / 2 - 0.05), 0.45), (L, 0.05, 0.05), PR.ROPE); parts.append((xf(V, 0, 0), F, C))
        for k in range(int(L / 1.8) + 1):
            s = min(k * 1.8, L - 0.05); V, F, C = PR.box((0, sgn * (w / 2 - 0.05), 0.5), (0.12, 0.12, 1.2), PR.WOOD_D); parts.append((xf(V, s, 0), F, C))
    V, F, C = PR._join(parts); return V, F, C


Vb, Fb, Cb = bridge(); make_object("BRIDGE", Vb, Fb, Cb, "prop", "angle"); stats["BRIDGE"] = dict(tris=len(Fb))

# ---------------------------------------------------------------------------------------------------- prototypes (instanced in the browser)
proto_col = bpy.data.collections.new("P3B_PROTOS"); scene.collection.children.link(proto_col)
for nm, fn in PR.PROTOS.items():
    V, F, C = fn(); mt = "foliage" if nm in ("tree_round", "tree_tall", "palm", "shrub", "tea") else ("rock" if nm.startswith("rock") else "prop")
    make_object("PROTO_" + nm, V, F, C, mt, "angle" if mt != "foliage" else "smooth", parent_col=proto_col); stats["PROTO_" + nm] = dict(tris=len(F))

# ---------------------------------------------------------------------------------------------------- placement lists
solids = M.load_solids(SCENE)
veg = {k: [] for k in ("tree_round", "tree_tall", "palm", "shrub", "rock", "tea")} if "--no-veg" in argv else M.plant(solids)       # batch 2: vegetation comes from p3b2_scatter.py
quay = []; props_solid = []
A = np.array


def edge_x_at(n, side, margin):
    xs = np.arange(-90, 130, 0.25); m = M.edge_distance(M.MAIN, xs, np.full_like(xs, n)) >= margin; xs = xs[m]
    return float(xs.min() if side < 0 else xs.max())


def add_prop(proto, x, n, yaw=0.0, s=1.0, solid=None):
    z = float(M.terrain(np.array(x), np.array(n))); quay.append(dict(proto=proto, x=x, n=n, z=z, yaw=yaw, s=s))
    if solid:
        props_solid.append(dict(src="P3B:" + proto, x=x, n=n, w=solid[0], d=solid[1], h=solid[2]))


rngq = np.random.default_rng(11)
for n in (-44.0, -58.0):
    xw = edge_x_at(n, -1, 4.5) + 1.2; xe = edge_x_at(n, 1, 4.5) - 3.2
    add_prop("crate_stack", xw, n, rngq.uniform(-0.2, 0.2), 1.0, (4.0, 3.0, 1.7)); add_prop("barrel", xw + 0.2, n + 3.0, 0, 1, (0.8, 0.8, 1.1)); add_prop("barrel", xw + 1.0, n + 3.4, 0, 1, (0.8, 0.8, 1.1))
    add_prop("crate_stack", xe, n - 2.0, math.pi + rngq.uniform(-0.2, 0.2), 1.0, (4.0, 3.0, 1.7)); add_prop("barrel", xe - 1.0, n + 1.5, 0, 1, (0.8, 0.8, 1.1))
xc = edge_x_at(-47.0, 1, 3.0) - 2.2; add_prop("crane", xc, -47.0, 0.0, 1.0, (2.0, 2.2, 5.6))
for n in range(-34, -76, -8):
    for side in (-1, 1):
        xe_ = edge_x_at(float(n), side, 1.6)
        if abs(xe_ - 5) > 12:
            add_prop("bollard", xe_ - side * 1.6, float(n), 0, 1, (0.7, 0.7, 0.8))
rim_n = None
for nn in np.arange(-60, -90, -0.25):
    if M.edge_distance(M.MAIN, np.array(5.0), np.array(nn)) < 6.5:
        rim_n = float(nn); break
add_prop("beacon", 5.0, rim_n + 1.0, 0.0, 1.0, (3.6, 3.6, 9.0))
for xx in (-9.2, 9.2):
    add_prop("lamp", xx, -24.5, 0, 1, (0.3, 0.3, 3.8)); add_prop("lamp", xx, -39.5, 0, 1, (0.3, 0.3, 3.8)); add_prop("lamp", xx, -56.0, 0, 1, (0.3, 0.3, 3.8))
for (x, n) in ((-6, -66), (14, -70), (-14, -72), (18, -64)):
    add_prop("sack", x, float(n), rngq.uniform(0, 6), 1.0)
add_prop("pavilion", 111.0, 45.0, 0.0, 1.0)
zst = float(M.stack_top(np.array(111.0), np.array(45.0)))
quay[-1]["z"] = zst + 0.02
for (px, pn) in ((109.0, 43.0), (113.0, 43.0), (113.0, 47.0), (109.0, 47.0)):
    props_solid.append(dict(src="P3B:pavilion-post", x=px, n=pn, w=0.5, d=0.5, h=2.8))
add_prop("counting_stone", 40.0, 116.0, 0.4, 1.0, (1.4, 1.4, 3.2))
for (wx, wn, wy) in ((-57.0, 7.5, 0.5), (-40.0, 26.5, -0.4), (-59.0, 27.0, 0.2)):
    add_prop("wagon", wx, wn, wy, 1.0, (3.6, 2.2, 2.3))
add_prop("campfire", -44.0, 24.0, 0, 1.0, (1.8, 1.8, 0.4))
inst = dict(vegetation={k: [list(map(float, v)) for v in lst] for k, lst in veg.items()}, quay_props=quay, prop_solids=props_solid, debris=deb, roots=roots, extents=M.extents(), bridge=dict(zip(("name", "width", "a", "b", "za", "zb"), M.BRIDGE)),
            water=[list(map(float, p)) for p in M.WATER], falls=dict(lip=list(M.FALLS[0]), height=stats["WATER_FALL"]["height_m"]),
            clearings=[dict(name=nm, x=cx, n=cn, r=r, z=zz) for nm, cx, cn, r, zz in M.CLEARINGS], paths=[dict(name=nm, kind=k, width=w, pts=[list(p) for p in pts]) for nm, k, w, pts in M.PATHS],
            tree_trunks=[dict(x=v[0], n=v[1], r=0.38) for k in ("tree_round", "tree_tall", "palm") for v in veg[k]], big_rocks=[dict(x=v[0], n=v[1], r=1.0 * v[4]) for v in veg["rock"] if v[4] > 1.25])
json.dump(inst, open(os.path.join(OUT, "island-instances.json"), "w"))
stats["instances"] = {k: len(v) for k, v in veg.items()}; stats["quay_props"] = len(quay)
tri_total = sum(s["tris"] for s in stats.values() if isinstance(s, dict) and "tris" in s and not any(k in s for k in ()))

# ---------------------------------------------------------------------------------------------------- export
glb = os.path.join(OUT, "merchant-citadel-p3b-island.glb")
for ob in bpy.data.objects: ob.select_set(True)
kw = dict(filepath=glb, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_normals=True, export_vertex_color="ACTIVE", export_attributes=True, export_materials="EXPORT", export_cameras=False, export_lights=False)
try:
    bpy.ops.export_scene.gltf(**kw)
except TypeError as e:
    log("export kw fallback:", e); kw.pop("export_vertex_color", None); bpy.ops.export_scene.gltf(**kw)
stats["glb_bytes"] = os.path.getsize(glb); stats["seconds"] = round(time.time() - T0, 1)
stats["island_tris_static"] = sum(stats[k]["tris"] for k in ("ISL_TOP", "ISL_CLIFF", "STACK_TOP", "STACK_CLIFF", "ISL_ROOTS", "ISL_DEBRIS", "WATER_STREAM", "WATER_FALL", "BRIDGE"))
json.dump(stats, open(os.path.join(OUT, "island-build-stats.json"), "w"), indent=1)
if BLEND:
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
log("done", json.dumps(stats))
