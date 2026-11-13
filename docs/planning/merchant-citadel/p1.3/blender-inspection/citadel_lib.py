"""Shared Blender helpers for the Merchant Citadel P1 / P1.1 / P1.2 inspection scenes (concept only, no exports).

Conventions (Blender, Z up):  X = east, Y = north, Z = up.  Project/Three.js: x = X, y = Z, z = -Y.
Medieval Village modules as measured in P1: 2 m wide, 3 m storey pitch, origin bottom-centre on the
grid line, front face towards Blender -Y (glTF +Z).  Roof_RoundTiles_<span>x<length>: ridge along Y.

Asset id forms handled by Lib.inst():
  MV-/FP-/SN-<name>            real downloaded Quaternius model, instanced as authored
  SY-<name>                    real downloaded Syntaxes of Play "Medieval Cafe" model (FBX geometry + the pack's own materials)
  AV-<name>                    real downloaded Avramania model (Food & Market and Village Builder packs only)
  <real id>@<variant>          MATERIAL VARIANT: same downloaded geometry, cloth or roof-tile colour changed (see VARIANTS)
  CUS-<name>                   CUSTOM concept geometry built here (NOT a downloaded asset; see CUSTOM)

P1.2 colour grade: GRADE lists a hue / saturation / value correction per downloaded material, applied once to
the shared material (a material normalisation, disclosed in the documents; geometry and textures are untouched).
"""
import bpy, bmesh, colorsys, json, math, os
from mathutils import Vector

PREFIX = {"MV": "quaternius-medieval-village", "FP": "quaternius-fantasy-props",
          "SN": "quaternius-stylized-nature", "KFT": "kenney-fantasy-town-kit", "KMB": "kenney-modular-buildings",
          "SY": "synofplay-medieval-cafe", "AV": "avramania-free-collection"}

# facade code -> (wall module, insert)   insert "door:<id>" is hung on the hinge side of the opening
CODES = {
    "P": ("MV-Wall_Plaster_Straight", None),
    "G": ("MV-Wall_Plaster_WoodGrid", None),
    "F": ("MV-Wall_Plaster_Window_Wide_Flat", "MV-Window_Wide_Flat1"),
    "R": ("MV-Wall_Plaster_Window_Wide_Round", "MV-Window_Wide_Round1"),
    "T": ("MV-Wall_Plaster_Window_Thin_Round", "MV-Window_Thin_Round1"),
    "D": ("MV-Wall_Plaster_Door_Flat", "door:MV-Door_1_Flat"),
    "O": ("MV-Wall_Plaster_Door_Round", "door:MV-Door_8_Round"),
    "I": ("MV-Wall_Plaster_Door_RoundInset", "doorin:MV-Door_8_Round"),
    "S": ("MV-Wall_UnevenBrick_Straight", None),
    "s": ("MV-Wall_UnevenBrick_Window_Wide_Flat", "MV-Window_Wide_Flat1"),
    "r": ("MV-Wall_UnevenBrick_Window_Wide_Round", "MV-Window_Wide_Round1"),
    "o": ("MV-Wall_UnevenBrick_Door_Round", "door:MV-Door_8_Round"),
    "d": ("MV-Wall_UnevenBrick_Door_Flat", "door:MV-Door_4_Flat"),
    "A": ("MV-Wall_Arch", None),
    "X": (None, None),
}
STOREY = 3.0
POST = {"wood": "MV-Corner_ExteriorWide_Wood", "brick": "MV-Corner_Exterior_Brick", None: None}

def srgb(hexcode):
    """'#RRGGBB' -> linear RGB tuple."""
    c = [int(hexcode[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


# P1.2 art-direction palette (owner brief, section 3.2).
PALETTE = {"plaster": "#E8D9BC", "timber": "#75543B", "roof": "#BB6345", "roof_dark": "#9F523D", "stone": "#858078",
           "cobble": "#A69E8E", "burgundy": "#8C3E45", "blue": "#345D80", "gold": "#C8A15A", "cream": "#E6D8B8"}
# Material grade: base material name -> (hue offset, saturation multiplier, value multiplier), derived from the measured
# average texture colour of each downloaded material against the palette target.
GRADE = {"MI_RoundTiles": (0.012, 0.90, 0.94), "MI_WoodTrim": (0.0, 0.82, 0.76), "MI_WoodTrim_Wear": (0.0, 0.82, 0.76),
         "MI_Plaster": (0.0, 0.80, 1.14), "MI_UnevenBrick": (0.0, 0.50, 0.98), "MI_Brick": (0.0, 0.70, 1.10),
         "MI_RockTrim": (0.0, 0.65, 1.0), "MI_Trim_Furniture": (0.0, 0.95, 0.90), "MI_RedBrick": (0.0, 0.78, 0.98),
         "Leaves_NormalTree": (0.0, 0.70, 0.90), "Leaves": (0.0, 0.75, 0.92), "Flowers": (0.0, 0.85, 1.0)}
# Variants. Cloth variants replace the vertex-colour mix of the downloaded cloth material with texture x colour
# (reproducible in Three.js as material.color). "dark" is the civic roof tile value (extra grade on MI_RoundTiles).
CLOTH_MATERIALS = ("MI_Banner",)
VARIANTS = {"burgundy": ("cloth", PALETTE["burgundy"], 1.2), "blue": ("cloth", PALETTE["blue"], 1.9), "gold": ("cloth", PALETTE["gold"], 1.6),
            "cream": ("cloth", PALETTE["cream"], 1.7), "dark": ("grade", "MI_RoundTiles", (0.004, 0.84, 0.72))}


def flat_material(name, rgb, rough=0.9, metallic=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return m


def _prism(bm, pts, y0, y1, mat_index):
    """Extrude a 2D outline (x, z) between y0 (back) and y1 (front, more negative)."""
    back = [bm.verts.new((x, y0, z)) for x, z in pts]
    front = [bm.verts.new((x, y1, z)) for x, z in pts]
    n = len(pts)
    faces = [bm.faces.new(front[::-1]), bm.faces.new(back)]
    for i in range(n):
        faces.append(bm.faces.new((back[i], back[(i + 1) % n], front[(i + 1) % n], front[i])))
    for f in faces:
        f.material_index = mat_index


def _circle(r, n=28):
    return [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _rect(cx, cz, w, h, ang=0.0):
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + x * c - z * sn, cz + x * sn + z * c) for x, z in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]


def _finish(bm, name, mats):
    me = bpy.data.meshes.new(name)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me); bm.free()
    for m in mats:
        me.materials.append(m)
    return bpy.data.objects.new("TPL_" + name, me)


def make_seal():
    """CUS-Seal_NiagaAwan: original guild seal, 1.0 m diameter, faces -Y, back on the wall plane.
    Gold rim, burgundy field, two crossing trade routes with a way-station disc at each end, central diamond."""
    bm = bmesh.new()
    _prism(bm, _circle(0.50), 0.0, -0.05, 0)                       # gold rim disc
    _prism(bm, _circle(0.43), -0.05, -0.07, 1)                     # burgundy field
    for ang in (math.radians(32), math.radians(148)):
        _prism(bm, _rect(0, 0, 0.74, 0.065, ang), -0.07, -0.092, 0)        # trade route
        for sgn in (-1, 1):
            cx, cz = sgn * 0.37 * math.cos(ang), sgn * 0.37 * math.sin(ang)
            _prism(bm, [(cx + x, cz + z) for x, z in _circle(0.058, 12)], -0.07, -0.10, 0)   # way station
    _prism(bm, [(0, 0.25), (0.19, 0), (0, -0.25), (-0.19, 0)], -0.092, -0.118, 0)           # gold diamond
    _prism(bm, [(0, 0.15), (0.115, 0), (0, -0.15), (-0.115, 0)], -0.118, -0.132, 2)         # blue heart of the diamond
    return _finish(bm, "CUS-Seal_NiagaAwan", [flat_material("CUS_guild_gold", srgb(PALETTE["gold"]), 0.42, 0.45),
                                              flat_material("CUS_guild_burgundy", srgb(PALETTE["burgundy"]), 0.75),
                                              flat_material("CUS_guild_blue", srgb(PALETTE["blue"]), 0.7)])


GLYPHS = {  # trade pictograms, drawn in the 0.5 x 0.4 m board plane (y = along the board, z = up)
    "Loaf": [(-0.17, -0.06), (-0.12, -0.10), (0.12, -0.10), (0.17, -0.06), (0.16, 0.03), (0.08, 0.09), (-0.08, 0.09), (-0.16, 0.03)],
    "Jar": [(-0.07, -0.12), (0.07, -0.12), (0.12, -0.04), (0.11, 0.04), (0.05, 0.08), (0.05, 0.11), (0.08, 0.13), (-0.08, 0.13), (-0.05, 0.11), (-0.05, 0.08), (-0.11, 0.04), (-0.12, -0.04)],
    "Hammer": [(-0.025, -0.13), (0.025, -0.13), (0.025, 0.05), (0.13, 0.05), (0.13, 0.13), (-0.13, 0.13), (-0.13, 0.05), (-0.025, 0.05)],
    "Crate": [(-0.12, -0.11), (0.12, -0.11), (0.12, 0.11), (-0.12, 0.11)],
    "Coin": None,   # disc
    "Cup": [(-0.09, -0.11), (0.07, -0.11), (0.09, -0.02), (0.15, -0.02), (0.15, 0.07), (0.10, 0.07), (0.10, 0.11), (-0.11, 0.11)],
    "Scroll": [(-0.15, -0.10), (0.11, -0.10), (0.15, -0.06), (0.15, 0.10), (-0.11, 0.10), (-0.15, 0.06)],
}


def make_sign(glyph, field):
    """CUS-Sign_<glyph>: hanging trade sign. Origin = where the iron arm meets the wall; the arm runs 0.95 m along -Y and
    the 0.5 x 0.4 m timber board hangs under it in the Y-Z plane, so it is read by people walking along the wall.
    The top of the arm is at z = 0; the board spans z -0.56 .. -0.16."""
    bm = bmesh.new()
    box = lambda x0, x1, y0, y1, z0, z1, mi: _prism(bm, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], y1, y0, mi)
    box(-0.025, 0.025, -0.95, 0.0, -0.05, 0.0, 0)                  # arm
    box(-0.02, 0.02, -0.30, -0.26, -0.30, -0.05, 0)                # wall-side strut
    box(-0.012, 0.012, -0.80, -0.78, -0.16, -0.05, 0); box(-0.012, 0.012, -0.44, -0.42, -0.16, -0.05, 0)   # two hangers
    box(-0.03, 0.03, -0.86, -0.36, -0.56, -0.16, 1)                # board frame (timber)
    box(-0.036, 0.036, -0.83, -0.39, -0.53, -0.19, 2)              # painted field, both faces
    cy, cz = -0.61, -0.36
    pts = GLYPHS[glyph] or _circle(0.11, 16)
    for face in (-1, 1):                                           # pictogram on both faces (outline lies in the Y-Z plane)
        vs0 = [bm.verts.new((face * 0.036, cy + py * 0.9, cz + pz * 0.9)) for py, pz in pts]
        vs1 = [bm.verts.new((face * 0.046, cy + py * 0.9, cz + pz * 0.9)) for py, pz in pts]
        fs = [bm.faces.new(vs1)]
        for i in range(len(pts)):
            fs.append(bm.faces.new((vs0[i], vs0[(i + 1) % len(pts)], vs1[(i + 1) % len(pts)], vs1[i])))
        for f in fs:
            f.material_index = 3
    fields = {"wood": ("CUS_sign_field_wood", (0.30, 0.19, 0.11)), "burgundy": ("CUS_guild_burgundy", srgb(PALETTE["burgundy"])),
              "blue": ("CUS_guild_blue", srgb(PALETTE["blue"]))}
    fname, fcol = fields[field]
    return _finish(bm, f"CUS-Sign_{glyph}_{field}", [flat_material("CUS_sign_iron", (0.035, 0.035, 0.04), 0.5, 0.6),
                                                      flat_material("CUS_sign_timber", srgb(PALETTE["timber"]), 0.8),
                                                      flat_material(fname, fcol, 0.75),
                                                      flat_material("CUS_sign_paint", srgb(PALETTE["cream"]) if field != "wood" else srgb(PALETTE["gold"]), 0.6)])


CUSTOM = {"CUS-Seal_NiagaAwan": make_seal}
for _g in GLYPHS:
    for _f in ("wood", "burgundy", "blue"):
        CUSTOM[f"CUS-Sign_{_g}_{_f}"] = (lambda g=_g, f=_f: make_sign(g, f))


class Lib:
    """Imports each real asset once (joined, transforms applied in memory) and hands out linked copies."""

    def __init__(self, extracted, measurements_json):
        self.paths, self.tris = {}, {}
        inv = {v: k for k, v in PREFIX.items()}
        rows = json.load(open(measurements_json))
        extra = os.path.join(os.path.dirname(measurements_json), "measurements-expansion.json")
        if os.path.exists(extra):
            rows += json.load(open(extra))
        for r in rows:
            if r["pack_id"] not in inv:
                continue                      # inspected and rejected packs are never loadable
            aid = f"{inv[r['pack_id']]}-{r['asset_name']}"
            self.paths[aid] = os.path.join(extracted, r["pack_id"], r["internal_filepath"])
            self.tris[aid] = r.get("triangle_count", 0)
        self.extracted = extracted
        self.tpl, self.usage, self.tinted, self.canon = {}, {}, {}, {}
        self.libcol = bpy.data.collections.new("LIB_templates")
        bpy.context.scene.collection.children.link(self.libcol)

    def _stash(self, obj, aid):
        obj.name = "TPL_" + aid
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        self.libcol.objects.link(obj)
        obj.hide_render = True; obj.hide_viewport = True
        self.tpl[aid] = obj
        return obj

    @staticmethod
    def _hsv(mat, dh, sat, val):
        nt = mat.node_tree
        bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if not bsdf or not bsdf.inputs["Base Color"].links:
            return
        inp = bsdf.inputs["Base Color"]
        src = inp.links[0].from_socket
        hsv = nt.nodes.new("ShaderNodeHueSaturation")
        hsv.inputs["Hue"].default_value = 0.5 + dh
        hsv.inputs["Saturation"].default_value = sat
        hsv.inputs["Value"].default_value = val
        nt.links.new(src, hsv.inputs["Color"]); nt.links.new(hsv.outputs["Color"], inp)

    def _canon(self, obj, pack):
        """Apply the colour grade (GRADE) once to every imported material. Materials are NOT merged across files: the glTF
        importer builds a vertex-colour multiply only for meshes that carry vertex colours, so two materials with the same
        name are not interchangeable (merging them turned the lantern metal black). P2 must keep that distinction too."""
        for m in obj.data.materials:
            if m and m.node_tree and m.name.split(".")[0] in GRADE and not m.get("graded"):
                self._hsv(m, *GRADE[m.name.split(".")[0]]); m["graded"] = 1

    def _tint(self, mat, variant):
        key = (mat.name, variant)
        if key in self.tinted:
            return self.tinted[key]
        spec = VARIANTS[variant]
        m = mat.copy(); m.name = f"{mat.name.split('.')[0]}@{variant}"
        nt = m.node_tree
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        inp = bsdf.inputs["Base Color"]
        if spec[0] == "grade":
            self._hsv(m, *spec[2])
        else:
            col = srgb(spec[1])
            tex = next((n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image), None)
            if tex:
                mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"
                mix.inputs["Factor"].default_value = 1.0
                mix.inputs["B"].default_value = (*[c * spec[2] for c in col], 1)
                nt.links.new(tex.outputs["Color"], mix.inputs["A"]); nt.links.new(mix.outputs["Result"], inp)
            else:
                inp.default_value = (*col, 1)
        self.tinted[key] = m
        return m

    def _load(self, aid):
        if aid in CUSTOM:
            obj = CUSTOM[aid]()
            obj.data.calc_loop_triangles(); self.tris[aid] = len(obj.data.loop_triangles)
            return self._stash(obj, aid)
        if "@" in aid:
            base_id, variant = aid.split("@")
            base = self.tpl.get(base_id) or self._load(base_id)
            o = base.copy(); o.data = base.data.copy()
            targets = CLOTH_MATERIALS if VARIANTS[variant][0] == "cloth" else (VARIANTS[variant][1],)
            for i, m in enumerate(o.data.materials):
                if m and m.name.split(".")[0] in targets:
                    o.data.materials[i] = self._tint(m, variant)
            self.tris[aid] = self.tris[base_id]
            return self._stash(o, aid)
        before = set(bpy.data.objects)
        if self.paths[aid].lower().endswith(".fbx"):
            bpy.ops.import_scene.fbx(filepath=self.paths[aid])
        else:
            bpy.ops.import_scene.gltf(filepath=self.paths[aid])
        new = [o for o in bpy.data.objects if o not in before]
        meshes = [o for o in new if o.type == "MESH"]
        bpy.context.view_layer.update()
        for o in meshes:
            mw = o.matrix_world.copy()
            if o.data.users > 1:
                o.data = o.data.copy()
            o.parent = None
            o.data.transform(mw)
            o.matrix_world.identity()
        if aid.startswith("SY-"):
            self._syn_materials(meshes)
        base = meshes[0]
        other_names = [o.name for o in new if o.type != "MESH"]
        if len(meshes) > 1:
            with bpy.context.temp_override(active_object=base, selected_editable_objects=meshes, selected_objects=meshes):
                bpy.ops.object.join()
        for n in other_names:  # empties left over from the import
            o = bpy.data.objects.get(n)
            if o is not None:
                bpy.data.objects.remove(o, do_unlink=True)
        self._canon(base, aid.split("-")[0])
        return self._stash(base, aid)

    def _syn_materials(self, objs):
        """The cafe pack's FBX texture paths do not resolve; its own all-merged.blend holds the same-named materials."""
        blend = os.path.join(self.extracted, PREFIX["SY"], "all-merged.blend")
        need = sorted({s.material.name.split(".")[0] for o in objs for s in o.material_slots if s.material} - {k[3:] for k in self.canon if k.startswith("SY:")})
        if need:
            with bpy.data.libraries.load(blend, link=False) as (src, dst):
                dst.materials = [n for n in need if n in src.materials]
            for m in dst.materials:
                if m:
                    self.canon["SY:" + m.name.split(".")[0]] = m
        for o in objs:
            for s in o.material_slots:
                if s.material and "SY:" + s.material.name.split(".")[0] in self.canon:
                    s.material = self.canon["SY:" + s.material.name.split(".")[0]]

    def inst(self, aid, loc=(0, 0, 0), rz=0.0, parent=None, coll=None, scale=1.0):
        tpl = self.tpl.get(aid) or self._load(aid)
        o = tpl.copy()
        (coll or bpy.context.scene.collection).objects.link(o)
        o.hide_render = False; o.hide_viewport = False
        o.name = aid
        o.parent = parent
        o.location = loc
        o.rotation_mode = "XYZ"  # the glTF importer leaves objects in quaternion mode
        o.rotation_euler = (0, 0, math.radians(rz))
        o.scale = tuple(scale) if isinstance(scale, (list, tuple)) else (scale, scale, scale)
        self.usage[aid] = self.usage.get(aid, 0) + 1
        return o

    def stats(self):
        var = {a: n for a, n in self.usage.items() if "@" in a}
        cus = {a: n for a, n in self.usage.items() if a.startswith("CUS-")}
        return {"instances": sum(self.usage.values()), "unique_assets": len(self.usage),
                "unique_downloaded_models": len({a.split("@")[0] for a in self.usage if not a.startswith("CUS-")}),
                "material_variant_ids": len(var), "custom_ids": len(cus),
                "triangles": sum(self.tris[a] * n for a, n in self.usage.items()),
                "triangles_custom": sum(self.tris[a] * n for a, n in cus.items()),
                "usage": dict(sorted(self.usage.items())), "tris_each": {a: self.tris[a] for a in self.usage}}


def ground_material(name="TMP_ground_grass"):
    """Temporary ground: two muted greens mixed by a large soft noise, so the support plane does not read as one flat colour."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.95
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 0.035; noise.inputs["Detail"].default_value = 4.0
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.38; ramp.color_ramp.elements[0].color = (0.115, 0.165, 0.075, 1)
    ramp.color_ramp.elements[1].position = 0.66; ramp.color_ramp.elements[1].color = (0.185, 0.225, 0.105, 1)
    nt.links.new(geo.outputs["Position"], noise.inputs["Vector"]); nt.links.new(noise.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


def box(name, lo, hi, mat, parent=None, coll=None):
    """Temporary concept geometry (always disclosed as such in the docs)."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object; o.name = name
    o.scale = (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
    o.location = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
    o.data.materials.append(mat)
    if coll:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
    o.parent = parent
    return o


def figure(loc, rz=0.0, coll=None):
    """1.9 m explorer stand-in (temporary geometry)."""
    m = flat_material("TMP_explorer", (0.05, 0.42, 0.45))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.56, location=(loc[0], loc[1], loc[2] + 0.78)); a = bpy.context.object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(loc[0], loc[1], loc[2] + 1.73)); b = bpy.context.object
    for o in (a, b):
        o.data.materials.append(m); o.name = "TMP_explorer"
        if coll:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            coll.objects.link(o)
    return [a, b]


def side_slots(W, D, side):
    """Module centres (x, y, rz) for one facade, listed left-to-right as seen from outside."""
    if side == "front":
        return [(-W / 2 + 1 + 2 * i, -D / 2, 0) for i in range(int(W // 2))]
    if side == "right":
        return [(W / 2, -D / 2 + 1 + 2 * i, 90) for i in range(int(D // 2))]
    if side == "back":
        return [(W / 2 - 1 - 2 * i, D / 2, 180) for i in range(int(W // 2))]
    return [(-W / 2, D / 2 - 1 - 2 * i, -90) for i in range(int(D // 2))]


def build_part(lib, part, parent, coll):
    """Assemble one rectangular block: walls per floor, inserts, corner posts, gables, roof, dark core."""
    W, D, floors = part["W"], part["D"], part["floors"]
    ox, oy, oz = part.get("offset", (0, 0, 0))
    ridge = part.get("ridge", "y")
    f_from = part.get("floor_from", 0)          # walls and posts start at this floor (tower rising through a roof)
    jet = part.get("jetty")                     # P1.2: front facade jettied 1.12 m from this floor up (Overhang modules; ridge "y" only)
    JET = 1.123
    for side, per_floor in part["facades"].items():
        slots = side_slots(W, D, side)
        for f, codes in enumerate(per_floor):
            assert len(codes) == len(slots), (part.get("id"), side, f, codes, len(slots))
            for code, (x, y, rz) in zip(codes, slots):
                wall, insert = CODES[code]
                if not wall or f < f_from:
                    continue
                z = oz + f * STOREY
                a = math.radians(rz)
                if jet is not None and side == "front" and f >= jet:
                    lib.inst("MV-Overhang_Plaster_Short", (ox + x, oy + y, z), 0, parent, coll)
                    if insert and ":" not in insert:   # window frame and glass mounted on the jetty face
                        lib.inst(insert, (ox + x, oy + y - JET, z), 0, parent, coll)
                    continue
                lib.inst(wall, (ox + x, oy + y, z), rz, parent, coll)
                if insert and insert.startswith("doorin:"):  # leaf at the back of the 1 m deep portal
                    lib.inst(insert[7:], (ox + x - 0.535 * math.cos(a) - 0.93 * math.sin(a), oy + y - 0.535 * math.sin(a) + 0.93 * math.cos(a), z), rz, parent, coll)
                elif insert and insert.startswith("door:"):
                    lib.inst(insert[5:], (ox + x - 0.535 * math.cos(a), oy + y - 0.535 * math.sin(a), z), rz, parent, coll)
                elif insert:
                    lib.inst(insert, (ox + x, oy + y, z), rz, parent, coll)
                if part.get("shutters") and side == "front" and code in "Fs":
                    lib.inst("MV-WindowShutters_Wide_Flat_Open", (ox + x, oy + y, z), rz, parent, coll)
    corner = part.get("corner", "wood")
    skip = [tuple(c) for c in part.get("skip_corners", [])]
    for f in range(f_from, floors):
        post = POST[corner[min(f, len(corner) - 1)] if isinstance(corner, list) else corner]
        if not post:
            continue
        for sx, sy, rz in ((-1, -1, 0), (1, -1, 90), (1, 1, 180), (-1, 1, -90)):
            if (sx, sy) not in skip and not (jet is not None and f >= jet and sy == -1):
                lib.inst(post, (ox + sx * W / 2, oy + sy * D / 2, oz + f * STOREY), rz, parent, coll)
    for extra_post in part.get("posts", []):  # free-standing timber posts [x, y]
        lib.inst("MV-Corner_ExteriorWide_Wood", (ox + extra_post[0], oy + extra_post[1], oz), 0, parent, coll)
    top = oz + floors * STOREY
    rv = ("@" + part["roof_variant"]) if part.get("roof_variant") else ""
    gy = 0.0
    if jet is not None:                         # side closures (two storeys tall: bracket below, cheek above)
        zj = oz + (jet - 1) * STOREY
        lib.inst("MV-Overhang_Side_Plaster_Short_L", (ox - W / 2 + 1, oy - D / 2, zj), 0, parent, coll)
        lib.inst("MV-Overhang_Side_Plaster_Short_R", (ox + W / 2 - 1, oy - D / 2, zj), 0, parent, coll)
        gy = -JET
    if part.get("roof"):
        span, length = part["roof"].split("x")
        rrz = 0 if ridge == "y" else 90
        rname, rsx, rsy = part["roof"], *part.get("roof_shift", (0, 0))
        if jet is not None:                     # a roof 2 m longer, shifted 1 m forward, covers the jetty
            rname, rsy = f"{span}x{int(length) + 2}", rsy - 1.0
        lib.inst(part.get("roof_asset", f"MV-Roof_RoundTiles_{rname}") + rv, (ox + rsx, oy + rsy, top), rrz, parent, coll)
        gable = part.get("gable_asset", f"MV-Roof_Front_Brick{span}")
        ends = part.get("gables", ["a", "b"])
        if ridge == "y":
            if "a" in ends: lib.inst(gable, (ox, oy - D / 2 + gy, top), 0, parent, coll)
            if "b" in ends: lib.inst(gable, (ox, oy + D / 2, top), 180, parent, coll)
        else:
            if "a" in ends: lib.inst(gable, (ox + W / 2, oy, top), 90, parent, coll)
            if "b" in ends: lib.inst(gable, (ox - W / 2, oy, top), -90, parent, coll)
    if part.get("tower_roof"):
        lib.inst("MV-Roof_Tower_RoundTiles" + rv, (ox, oy, top), 0, parent, coll)
    if part.get("core", True):
        m = flat_material("TMP_interior_core", (0.035, 0.03, 0.028))
        i = part.get("core_inset", 0.34)
        box("TMP_core", (ox - W / 2 + i, oy - D / 2 + i, oz + f_from * STOREY + 0.02), (ox + W / 2 - i, oy + D / 2 - i, top + 0.3), m, parent, coll)


def build_archetype(lib, arch, name, loc=(0, 0, 0), rz=0.0, coll=None, opts=None):
    """opts: {"sign": asset id replacing every extra tagged role == 'sign', "kit": dressing kit to include}.
    Extras tagged with a kit are placed only when it matches; with no kit chosen the first kit found is used."""
    opts = opts or {}
    sign = opts.get("sign")
    kit = opts.get("kit") or next((e["kit"] for e in arch.get("extras", []) if e.get("kit")), None)
    root = bpy.data.objects.new(name, None)
    (coll or bpy.context.scene.collection).objects.link(root)
    root.location = loc; root.rotation_euler = (0, 0, math.radians(rz))
    for part in arch["parts"]:
        build_part(lib, part, root, coll)
    for e in list(arch.get("extras", [])) + list(opts.get("add", [])):   # opts["add"]: per-building extras (P1.3)
        if e.get("kit") and e["kit"] != kit:
            continue
        asset = sign if (sign and e.get("role") == "sign") else e["asset"]
        lib.inst(asset, e["pos"], e.get("rz", 0), root, coll, e.get("scale", 1.0))
    return root


def setup_render(px=(1600, 900), sky=(0.60, 0.74, 0.92), sun_energy=4.0, sun_rot=(50, 0, -35), transparent=False, afternoon=False):
    """afternoon=True is the P1.2 presentation light: warm low sun, blue sky fill from a horizon-to-zenith gradient,
    screen-space ambient occlusion where the engine offers it, and the Khronos PBR Neutral view transform
    (the tone mapping three.js ships as NeutralToneMapping). It changes how the scene is lit, not what is in it."""
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            sc.render.engine = eng; break
        except TypeError:
            continue
    sc.render.resolution_x, sc.render.resolution_y = px
    sc.render.film_transparent = transparent
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.get("citadel_world") or bpy.data.worlds.new("citadel_world")
    sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*sky, 1); bg.inputs[1].default_value = 1.0
    sun = bpy.data.objects.get("SUN")
    if not sun:
        sun = bpy.data.objects.new("SUN", bpy.data.lights.new("SUN", "SUN")); sc.collection.objects.link(sun)
    sun.data.energy = sun_energy; sun.data.angle = math.radians(4); sun.data.color = (1.0, 0.95, 0.86)
    sun.rotation_euler = tuple(math.radians(a) for a in sun_rot)
    if afternoon:
        sun.data.color = (1.0, 0.86, 0.68); sun.data.angle = math.radians(2.5)
        nt = w.node_tree
        tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
        half = nt.nodes.new("ShaderNodeMath"); half.operation = "MULTIPLY_ADD"; half.inputs[1].default_value = 0.5; half.inputs[2].default_value = 0.5
        nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], half.inputs[0]); nt.links.new(half.outputs[0], ramp.inputs[0])
        e = ramp.color_ramp.elements
        e[0].position = 0.40; e[0].color = (0.60, 0.66, 0.60, 1)      # below the horizon: soft green-grey bounce
        e[1].position = 0.50; e[1].color = (0.95, 0.86, 0.74, 1)      # warm horizon haze
        for pos, col in ((0.58, (0.60, 0.76, 0.92, 1)), (1.0, (0.24, 0.46, 0.82, 1))):
            el = e.new(pos); el.color = col
        nt.links.new(ramp.outputs["Color"], bg.inputs[0]); bg.inputs[1].default_value = 0.85
        for attr, val in (("use_raytracing", False), ("use_gtao", True), ("gtao_distance", 1.2), ("use_soft_shadows", True),
                          ("taa_render_samples", 48), ("use_shadows", True)):
            try:
                setattr(sc.eevee, attr, val)
            except Exception:
                pass
        for vt in ("Khronos PBR Neutral", "Filmic", "Standard"):
            try:
                sc.view_settings.view_transform = vt; break
            except TypeError:
                continue
        try:
            sc.view_settings.look = "None"
        except TypeError:
            pass
    return sc


def camera(name, loc, look_at, fov_v=None, ortho=None, clip=(0.2, 1500)):
    sc = bpy.context.scene
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name)); sc.collection.objects.link(cam)
    cam.location = loc
    d = Vector(loc) - Vector(look_at)
    cam.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    if ortho:
        cam.data.type = "ORTHO"; cam.data.ortho_scale = ortho
    else:
        cam.data.sensor_fit = "VERTICAL"; cam.data.angle_y = math.radians(fov_v or 60)
    cam.data.clip_start, cam.data.clip_end = clip
    return cam


def render(cam, path):
    sc = bpy.context.scene
    sc.camera = cam; sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("[render]", path, flush=True)
