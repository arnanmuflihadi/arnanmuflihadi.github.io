"""Merchant Citadel P2-A: build the production kit from the P1.4 assemblies and export one game-ready GLB.

Run:  Blender --background --factory-startup --disable-autoexec --python p2a_kit_export.py -- <inspection_dir> <out_dir> <scene.json>

Pipeline (the P2 construction rules of P1.4, applied):
 1. Build each archetype of the slice at the origin from the verified models (citadel_lib / town_data of P1.4).
 2. Merge materials that have an identical node set-up and the same source images (never by name alone: same-named
    Quaternius materials differ by whether the mesh has vertex colours).
 3. Bake the colour grade and cloth tints into copies of the base-colour textures (the grade is a Hue/Saturation node and a
    constant multiply in Blender; glTF has neither), and reduce every texture to the sizes in TEX_POLICY. Normal and ORM maps are
    resized only. All baked images are written to <out_dir>/tex.
 4. Join every archetype into ONE mesh with one primitive per material, origin at the world origin.
 5. Export kit.glb (textures embedded once for the whole kit), a texture/material report and a .blend of the kit.
Nothing outside <out_dir> is written.
"""
import bpy, json, math, os, sys, hashlib
import numpy as np
from collections import OrderedDict
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
INSPECT, OUT, SCENE = args[:3]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "p1.4", "blender-inspection"))
import citadel_lib as cl                                         # noqa: E402
sys.path.insert(0, HERE)
from p2a_hall import hall_modules                                # noqa: E402
from p2a_bazaar import hall_archetype, HALL_VARIANTS, register_custom   # noqa: E402
register_custom(cl)                                              # batch 4: CUS-Hoist, CUS-Sign_Leaf_*, CUS-Awning_tea

TEXDIR = os.path.join(OUT, "tex"); os.makedirs(TEXDIR, exist_ok=True)
SC = json.load(open(SCENE))
ARCH = json.load(open(os.path.join(INSPECT, "p1.4", "data", "archetypes.json")))
TIER1 = ("MI_RoundTiles", "MI_Plaster", "MI_WoodTrim", "MI_WoodTrim_Wear", "MI_UnevenBrick", "MI_Brick", "MI_RedBrick", "MI_RockTrim")
TEX_POLICY = {"tier1": {"base": 1024, "orm": 512, "normal": 512}, "tier2": {"base": 512, "orm": 256, "normal": 256}}   # long side, pixels
QUALITY = {"base": 88, "orm": 86, "normal": 88}
NORMAL_1024 = ("MI_Brick", "MI_UnevenBrick", "MI_RedBrick")      # the ground and the stone ground floors are seen close and at grazing angles: keep their relief
PAVING_WARM = {"MI_UnevenBrick": (1.06, 0.97, 0.78), "MI_Brick": (1.12, 1.00, 0.92)}   # linear albedo multipliers = (Blender reference colour) / (browser colour) measured on the same views: sunlit cobble 157,150,143 vs 150,153,160; hall floor 101,106,111 vs 83,106,129; second pass after the first tint (1.05,.98,.89 / 1.22,1,.86) left cobble 160,153,151 and hall floor 94,106,120
METALS = ("Metal013", "Metal042B", "brushed_iron_03", "Metal013-2", "MI_Trim_Metal", "MI_MetalOrnaments", "CUS_sign_iron", "CUS_guild_gold")


# ---------------------------------------------------------------------------------------------------- colour maths
def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def hsv_apply(rgb, dh, sat, val):
    """Blender's Hue/Saturation/Value node (factor 1) on linear rgb."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b); d = mx - mn; dd = np.maximum(d, 1e-12)
    s = np.where(mx > 0, d / np.maximum(mx, 1e-12), 0.0)
    h = np.where(r == mx, (mx - b) / dd - (mx - g) / dd, np.where(g == mx, 2 + (mx - r) / dd - (mx - b) / dd, 4 + (mx - g) / dd - (mx - r) / dd))
    h = np.where(d > 1e-12, (h / 6.0) % 1.0, 0.0)
    h = (h + dh) % 1.0; s = np.clip(s * sat, 0, 1); v = mx * val
    i = np.floor(h * 6).astype(int) % 6; f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.stack([np.choose(i, [v, q, p, p, t, v]), np.choose(i, [t, v, v, q, p, p]), np.choose(i, [p, p, t, v, v, q])], axis=-1)
    return np.maximum(out, 0)


# ---------------------------------------------------------------------------------------------------- build
bpy.ops.wm.read_factory_settings(use_empty=True)
lib = cl.Lib(os.path.join(INSPECT, "extracted"), os.path.join(INSPECT, "measurements.json"))
nodes = OrderedDict()                       # node name -> list of mesh objects
col = bpy.data.collections.new("KIT"); bpy.context.scene.collection.children.link(col)


def meshes_under(root):
    return [o for o in root.children_recursive if o.type == "MESH"]


def build(name, arch):
    root = cl.build_archetype(lib, arch, name, (0, 0, 0), 0, col)
    root.name = "ROOT_" + name                                  # keep the plain name free for the joined mesh
    nodes[name] = meshes_under(root)


# P1.4 doc 10 proposed substituting the two heaviest repeated modules (corner bricks 3,102 triangles x 51, wall lanterns 2,822 x 46). Collapse-decimate the
# templates before any archetype is built from them; the effect is measured in 05 and judged by eye in 04. `--no-lod` exports the unreduced kit.
LOD_TARGETS = {"MV-Corner_Exterior_Brick": 400, "FP-Lantern_Wall": 700,
               # P2-B batch 3: small props that repeat in the new district and cost 1.4-3.8k triangles each for something under 1 m across and seen from 3 m or more
               "AV-mdvl_props_barrel_01": 800, "AV-mdvl_props_basket_01": 800, "AV-mdvl_props_sack_01": 600, "AV-mdvl_props_rope_coil_01": 600, "FP-Rope_1": 700,
               "FP-Anvil_Log": 1400, "AV-mdvl_farm_fruit_basket_01": 1300, "AV-mdvl_props_wheelbarrow_01": 900, "AV-mdvl_interiors_woodpile_01": 800,
               # P2-B batch 4: window boxes (two per A05c, plus A09 and A03c: 1.3k triangles each for a 1 m planter seen from 4 m or more), chest and basket of jars in the tea house
               "AV-mdvl_village_window_box_01": 700, "AV-mdvl_interiors_chest_01": 500}
LOD_REPORT = {}
if "--no-lod" not in sys.argv:
    _orig_stash = lib._stash

    def _stash_lod(obj, aid):
        t = LOD_TARGETS.get(aid)
        if t and obj.type == "MESH":
            obj.data.calc_loop_triangles(); n = len(obj.data.loop_triangles)
            if n > t:
                bpy.context.view_layer.objects.active = obj
                md = obj.modifiers.new("LOD", "DECIMATE"); md.ratio = t / n
                with bpy.context.temp_override(active_object=obj, object=obj):
                    bpy.ops.object.modifier_apply(modifier=md.name)
                obj.data.calc_loop_triangles(); LOD_REPORT[aid] = {"before": n, "after": len(obj.data.loop_triangles)}
        return _orig_stash(obj, aid)
    lib._stash = _stash_lod
HALL = hall_modules(ARCH["A01"])
def strip_signs(a):
    """Signs and banners are separate placed objects (SIGN_ nodes), so one building node serves every building of its archetype."""
    b = dict(a); b["extras"] = [e for e in a.get("extras", []) if e.get("role") != "sign"]
    return b


kit = [n for n in SC["kit_nodes"] if not n.startswith("TILE_") and n not in ("PODIUM", "ARCH")]
for n in kit:
    if n.startswith("SIGN_"):
        sg = SC["signs"][n]; o = lib.inst(sg["asset"], (0, 0, 0), 0, None, col, sg["scale"]); nodes[n] = [o]
    elif n in HALL_VARIANTS:
        build(n, strip_signs(hall_archetype(n, ARCH)))
    else:
        build(n, strip_signs(HALL[n] if n in HALL else ARCH[n]))
a01 = ARCH["A01"]
build("PODIUM", {"parts": [], "extras": [e for e in a01["extras"] if e["asset"].startswith(("MV-Floor_Brick", "MV-Stairs_"))]})
build("ARCH", {"parts": [], "extras": [{"asset": "MV-Wall_Arch", "pos": [0, 0, 0]}]})
for k, a in (("cobble", "MV-Floor_UnevenBrick"), ("brick", "MV-Floor_Brick"), ("red", "MV-Floor_RedBrick")):
    nodes["TILE_" + k] = [lib.inst(a, (0, 0, 0), 0, None, col)]
# static dressing: every prop of the slice merged by material into one mesh at world placement
dr = {}
for (a, x, n, z, rz, sc), dist in zip(SC["dressing"], SC["dressing_district"]):          # per-district dressing so each district can be merged and culled on its own
    dr.setdefault(dist, []).append(lib.inst(a, (x, n, z), rz, None, col, sc))
for dist, objs in dr.items():
    nodes["DRESSING_" + dist] = objs
for o in bpy.data.objects:
    if o.name.startswith("TPL_"):
        o.hide_viewport = True


# ---------------------------------------------------------------------------------------------------- materials
def abspath(img):
    p = bpy.path.abspath(img.filepath, library=img.library)
    if os.path.exists(p):
        return p
    cand = os.path.join(INSPECT, "extracted", "synofplay-medieval-cafe", "tex", os.path.basename(img.filepath))
    return cand if os.path.exists(cand) else p


def signature(m):
    nt = m.node_tree
    if not nt:
        return ("nonodes", m.name)
    b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    tex = tuple(sorted(os.path.basename(n.image.filepath) or n.image.name for n in nt.nodes if n.type == "TEX_IMAGE" and n.image))
    types = tuple(sorted(n.type for n in nt.nodes))
    par = []
    for n in nt.nodes:
        if n.type == "HUE_SAT":
            par.append(tuple(round(n.inputs[i].default_value, 4) for i in ("Hue", "Saturation", "Value")))
        if n.type == "MIX":
            par.append(tuple(round(v, 3) for i in n.inputs if i.enabled and i.name == "B" and not i.links for v in i.default_value))
    flat = tuple(round(v, 3) for v in b.inputs["Base Color"].default_value) + (round(b.inputs["Roughness"].default_value, 2), round(b.inputs["Metallic"].default_value, 2), round(b.inputs["Alpha"].default_value, 2))
    return (m.name.split(".")[0], types, tex, tuple(sorted(par)), flat if not tex else None)


canon, remap = {}, {}
for m in list(bpy.data.materials):
    if m.users == 0:
        continue
    sig = signature(m)
    if sig in canon:
        remap[m] = canon[sig]
    else:
        canon[sig] = m
before = len([m for m in bpy.data.materials if m.users])
for me in bpy.data.meshes:
    for i, m in enumerate(me.materials):
        if m in remap:
            me.materials[i] = remap[m]
for m in remap:
    m.user_clear()
mats = [m for m in canon.values()]
print("[kit] materials by signature:", before, "->", len(mats))

CACHE, REPORT = {}, {"materials": [], "textures": []}


def load_scaled(src, long_side):
    """src = the Blender image. File-backed images are re-read from disk; embedded ones (glb imports) are copied in memory."""
    p = abspath(src)
    if src.filepath and os.path.isfile(p):
        img = bpy.data.images.load(p, check_existing=False)
    else:
        img = src.copy()
    w, h = img.size
    if w == 0:
        img.reload(); w, h = img.size
    if w == 0:
        raise RuntimeError("texture did not load: " + src.name)
    k = min(1.0, long_side / max(w, h)); nw, nh = max(4, int(round(w * k))), max(4, int(round(h * k)))
    if (nw, nh) != (w, h):
        img.scale(nw, nh)
    return img, (w, h), (nw, nh)


def save_img(arr, w, h, name, fmt, quality, alpha):
    img = bpy.data.images.new(name, w, h, alpha=alpha, float_buffer=False)
    img.colorspace_settings.name = "Non-Color"
    img.pixels.foreach_set(arr.astype(np.float32).ravel())
    ext = ".jpg" if fmt == "JPEG" else ".png"; path = os.path.join(TEXDIR, name + ext)
    img.file_format = fmt; img.filepath_raw = path
    try:
        img.save(quality=quality)
    except TypeError:
        img.save()
    bpy.data.images.remove(img)
    return path


def process(src_img, role, ops, side, name):
    key = (abspath(src_img) or src_img.name, src_img.name, role, tuple(ops), side)
    if key in CACHE:
        return CACHE[key]
    img, (w0, h0), (w, h) = load_scaled(src_img, side)
    a = np.empty(w * h * 4, dtype=np.float32); img.pixels.foreach_get(a); a = a.reshape(h, w, 4); has_alpha = float(a[..., 3].min()) < 0.999
    over = 0.0
    if role == "base" and ops:
        lin = srgb_to_lin(a[..., :3])
        for op in ops:
            if op[0] == "hsv":
                lin = hsv_apply(lin, op[1], op[2], op[3])
            else:
                lin = lin * np.array(op[1])[None, None, :]
        over = float((lin.max(axis=-1) > 1.0).mean()); a = np.concatenate([lin_to_srgb(lin), a[..., 3:4]], axis=-1)
    fmt = "PNG" if (has_alpha and role == "base") else "JPEG"
    out = a if fmt == "PNG" else np.concatenate([a[..., :3], np.ones_like(a[..., 3:4])], axis=-1)
    path = save_img(out, w, h, name, fmt, QUALITY[role], fmt == "PNG")
    bpy.data.images.remove(img)
    rec = {"name": os.path.basename(path), "role": role, "source": os.path.basename(src_img.filepath) or src_img.name, "source_px": [w0, h0], "px": [w, h], "bytes": os.path.getsize(path), "format": fmt, "clamped_share": round(over, 4)}
    CACHE[key] = (path, rec); REPORT["textures"].append(rec)
    return CACHE[key]


def input_chain(sock):
    """Walk back from a socket through baked-in colour operations. Returns (ops, killable [(node, colour_input)], texture node, vcol mix)."""
    ops, kill, vcol = [], [], None
    cur = sock
    while cur.links:
        n = cur.links[0].from_node
        if n.type == "HUE_SAT":
            ops.append(("hsv", n.inputs["Hue"].default_value - 0.5, n.inputs["Saturation"].default_value, n.inputs["Value"].default_value)); kill.append((n, n.inputs["Color"])); cur = n.inputs["Color"]; continue
        if n.type == "MIX":
            ins = {i.name: i for i in n.inputs if i.enabled and i.name in ("A", "B")}
            linked = [k for k, i in ins.items() if i.links]
            vc = [k for k in linked if ins[k].links[0].from_node.type in ("VERTEX_COLOR", "ATTRIBUTE")]
            if vc:
                vcol = n; cur = ins["A" if vc[0] == "B" else "B"]; continue
            if len(linked) == 1:
                other = ins["B" if linked[0] == "A" else "A"].default_value
                ops.append(("mul", tuple(other[:3]))); kill.append((n, ins[linked[0]])); cur = ins[linked[0]]; continue
        break
    tex = cur.links[0].from_node if cur.links and cur.links[0].from_node.type == "TEX_IMAGE" else None
    return list(reversed(ops)), kill, tex, vcol


def bypass(node, colour_input):
    src = colour_input.links[0].from_socket
    for out in node.outputs:                                    # ShaderNodeMix has three Result sockets (float, vector, colour): the linked one is not outputs[0]
        for o in list(out.links):
            node.id_data.links.new(src, o.to_socket)
    node.id_data.nodes.remove(node)


def tier(m):
    return "tier1" if m.name.split(".")[0] in TIER1 else "tier2"


IMG_CACHE = {}
DEDUPED = [0]


def load_unique(path, colorspace):
    """Texture reuse: byte-identical baked images (the 15 Avramania palette copies, the two Metal013 normal maps) share one image datablock, hence one embedded GLB image."""
    key = (hashlib.md5(open(path, "rb").read()).hexdigest(), colorspace)
    if key in IMG_CACHE:
        DEDUPED[0] += 1; return IMG_CACHE[key]
    im = bpy.data.images.load(path, check_existing=False); im.colorspace_settings.name = colorspace; IMG_CACHE[key] = im
    return im


for m in mats:
    nt = m.node_tree
    if not nt:
        continue
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    safe = m.name.replace("@", "_").replace(".", "_")
    info = {"name": m.name, "tier": tier(m), "textures": []}
    ops, kill, tex, vcol = input_chain(bsdf.inputs["Base Color"])
    if m.name.split(".")[0] in PAVING_WARM:               # P2-B batch 3: the browser read the stone paving blue-grey (blue sky ambient on a neutral grey); warm the albedo toward the palette's cobble #A69E8E
        ops = list(ops) + [("mul", PAVING_WARM[m.name.split(".")[0]])]
    if tex is not None and tex.image is not None:
        path, rec = process(tex.image, "base", ops, TEX_POLICY[tier(m)]["base"], safe + "_base")
        for node, ci in kill:
            bypass(node, ci)
        new = load_unique(path, "sRGB"); tex.image = new
        info["textures"].append(rec); info["baked_ops"] = [o[0] for o in ops]
        if not (bsdf.inputs["Base Color"].links or vcol):
            raise RuntimeError("base colour unlinked after baking: " + m.name)
    # glTF has one metallic-roughness texture (G roughness, B metallic). Other packs' specular / metal maps do not map onto it: use constants.
    has_orm = bsdf.inputs["Roughness"].links and bsdf.inputs["Roughness"].links[0].from_node.type == "SEPARATE_COLOR"
    if not has_orm and not m.name.startswith("MI_"):
        base = m.name.split(".")[0]
        metal = bsdf.inputs["Metallic"]
        keep = 0.5 if (base in METALS or base.startswith(("Metal", "brushed"))) else 0.0
        for sock in (metal, bsdf.inputs["Roughness"]):
            for l in list(sock.links):
                nt.links.remove(l)
        metal.default_value = min(metal.default_value, keep) if keep else 0.0
        if bsdf.inputs["Roughness"].default_value < 0.2:
            bsdf.inputs["Roughness"].default_value = 0.6
        info["sanitised"] = {"metallic": round(metal.default_value, 2), "roughness": round(bsdf.inputs["Roughness"].default_value, 2)}
    for socket, node_type, role in ((bsdf.inputs["Roughness"], "SEPARATE_COLOR", "orm"), (bsdf.inputs["Normal"], "NORMAL_MAP", "normal")):
        if socket.links and socket.links[0].from_node.type in (node_type, "TEX_IMAGE"):
            inp = socket.links[0].from_node.inputs["Color"] if socket.links[0].from_node.type == node_type else socket
            if inp.links and inp.links[0].from_node.type == "TEX_IMAGE" and inp.links[0].from_node.image:
                t = inp.links[0].from_node
                side = 1024 if (role == "normal" and m.name.split(".")[0] in NORMAL_1024) else TEX_POLICY[tier(m)][role]
                path, rec = process(t.image, role, [], side, safe + "_" + role)
                new = load_unique(path, "Non-Color"); t.image = new
                info["textures"].append(rec)
    REPORT["materials"].append(info)


# ---------------------------------------------------------------------------------------------------- join and export
exp = []
for name, objs in nodes.items():
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.make_single_user(object=True, obdata=True)
    for o in objs:                                              # one UV set and one colour attribute only: the extras were 60 % of the file
        me = o.data
        while len(me.uv_layers) > 1:
            me.uv_layers.remove(me.uv_layers[len(me.uv_layers) - 1])
        cas = list(me.color_attributes)
        for ca in cas[1:]:
            me.color_attributes.remove(ca)
        if cas:
            me.color_attributes[0].name = "Color"
    bpy.ops.object.join()
    j = bpy.context.view_layer.objects.active
    j.name = name; j.data.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)    # the active part's own transform must not survive as a node transform
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    for i in range(len(j.material_slots) - 1, -1, -1):        # drop unused slots
        pass
    bpy.ops.object.material_slot_remove_unused()
    exp.append(j)

# ---------------------------------------------------------------------------------------------------- baked vertex ambient occlusion
# The vendored three build has no post-processing, so contact darkening is baked: one float per vertex (custom glTF attribute _AO) from
# cosine-weighted rays against the node itself plus a ground plane at its lowest point. The preview applies it to the INDIRECT light only.
AO_SAMPLES, AO_DIST, AO_STRENGTH = 40, 2.6, 0.4
for _a in sys.argv:                                              # --ao-strength=0.6 : lighter bake (P2-B A/B test), --ao-floor=0.2
    if _a.startswith("--ao-strength="):
        AO_STRENGTH = float(_a.split("=")[1])
AO_FLOOR = next((float(_a.split("=")[1]) for _a in sys.argv if _a.startswith("--ao-floor=")), 0.3)


def hemisphere_dirs(n):
    i = np.arange(n) + 0.5
    r = np.sqrt(i / n); phi = i * 2.399963229728653                      # Vogel disc -> cosine-weighted hemisphere (z up)
    return np.stack([r * np.cos(phi), r * np.sin(phi), np.sqrt(1 - r * r)], axis=1)


def bake_ao(obj):
    from mathutils.bvhtree import BVHTree
    from mathutils import Matrix
    me = obj.data; dg = bpy.context.evaluated_depsgraph_get()
    bvh = BVHTree.FromObject(obj, dg)
    zmin = min(v.co.z for v in me.vertices); g = zmin - 0.002
    ground = BVHTree.FromPolygons([(-300, -300, g), (300, -300, g), (300, 300, g), (-300, 300, g)], [(0, 1, 2, 3)])
    dirs = hemisphere_dirs(AO_SAMPLES); vals = np.ones(len(me.vertices), dtype=np.float32)
    for vi, v in enumerate(me.vertices):
        nrm = v.normal.normalized() if v.normal.length > 1e-6 else Vector((0, 0, 1))
        t = Vector((1, 0, 0)) if abs(nrm.x) < 0.9 else Vector((0, 1, 0)); b = nrm.cross(t).normalized(); t = b.cross(nrm)
        org = v.co + nrm * 0.03; occ = 0.0
        for d in dirs:
            w = t * d[0] + b * d[1] + nrm * d[2]
            best = AO_DIST
            for tree in (bvh, ground):
                h = tree.ray_cast(org, w, AO_DIST)
                if h[0] is not None and h[3] < best:
                    best = h[3]
            if best < AO_DIST:
                occ += 1.0 - best / AO_DIST
        vals[vi] = max(AO_FLOOR, 1.0 - AO_STRENGTH * occ / len(dirs) * 1.6)
    if "_AO" in me.attributes:
        me.attributes.remove(me.attributes["_AO"])
    a = me.attributes.new(name="_AO", type="FLOAT", domain="POINT"); a.data.foreach_set("value", vals)
    return float(vals.mean()), float(vals.min())


AO_REPORT = {}
if "--no-ao" not in sys.argv:
    for j in exp:
        if j.name.startswith("TILE_"):
            continue
        AO_REPORT[j.name] = bake_ao(j); print("[ao]", j.name, len(j.data.vertices), "vertices, mean/min", AO_REPORT[j.name])

for _m in bpy.data.materials:                                    # the colour attribute of every mesh was renamed "Color" above: the Color Attribute nodes must point at it, or the
    if _m.node_tree:                                              # exporter drops COLOR_0 and the vertex-coloured materials (pottery, coins, bottles) come out white
        for _n in _m.node_tree.nodes:
            if _n.type == "VERTEX_COLOR":
                _n.layer_name = "Color"
bpy.context.view_layer.update()
stats = {}
for j in exp:
    j.data.calc_loop_triangles()
    bb = [Vector(c) for c in j.bound_box]
    stats[j.name] = {"bbox_gltf": [round(min(v.x for v in bb), 4), round(min(v.z for v in bb), 4), round(-max(v.y for v in bb), 4), round(max(v.x for v in bb), 4), round(max(v.z for v in bb), 4), round(-min(v.y for v in bb), 4)],
                     "triangles": len(j.data.loop_triangles), "vertices": len(j.data.vertices), "primitives": len([s for s in j.material_slots if s.material]),
                     "materials": sorted({s.material.name for s in j.material_slots if s.material})}
bpy.ops.object.select_all(action="DESELECT")
for j in exp:
    j.select_set(True)
glb = os.path.join(OUT, "merchant-citadel-p2a-kit.glb")
bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_yup=True, export_texcoords=True, export_normals=True, export_tangents=False,
                          export_vertex_color="MATERIAL", export_all_vertex_colors=False, export_image_format="AUTO", export_cameras=False, export_lights=False, export_extras=False, export_animations=False,
                          export_skins=False, export_morph=False, export_materials="EXPORT", export_apply=False, export_attributes=True)
REPORT["texture_dedupe"] = {"images_reused": DEDUPED[0]}; REPORT["usage"] = dict(sorted(lib.usage.items())); REPORT["lod"] = LOD_REPORT; REPORT["ao"] = {"samples": AO_SAMPLES, "distance_m": AO_DIST, "strength": AO_STRENGTH, "nodes": AO_REPORT}; REPORT["nodes"] = stats; REPORT["glb_bytes"] = os.path.getsize(glb)
REPORT["policy"] = TEX_POLICY; REPORT["material_count"] = {"before_signature_merge": before, "after": len(mats)}
tot = {"textures": len(REPORT["textures"]), "bytes": sum(t["bytes"] for t in REPORT["textures"]), "gpu_bytes_mip": int(sum(t["px"][0] * t["px"][1] * 4 * 4 / 3 for t in REPORT["textures"])),
       "gpu_bytes_source_res": int(sum(t["source_px"][0] * t["source_px"][1] * 4 * 4 / 3 for t in REPORT["textures"]))}
REPORT["texture_totals"] = tot
json.dump(REPORT, open(os.path.join(OUT, "kit-report.json"), "w"), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "merchant-citadel-p2a-kit-source.blend"), compress=True)
print("[kit] glb", REPORT["glb_bytes"], "bytes;", tot, "; nodes", {k: (v["triangles"], v["primitives"]) for k, v in stats.items()})
