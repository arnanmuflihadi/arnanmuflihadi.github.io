"""Headless Blender inspection of the P1.2 expansion candidates: import, measure, and render one tile each.

Run:  Blender --background --factory-startup --disable-autoexec --python inspect_expansion.py -- <extracted_dir> <out.json> <tiles_dir> [px]

Every tile shows the candidate AS AUTHORED (no rescale, no material change) beside two references:
the 1.9 m explorer stand-in and the already-adopted Quaternius Fantasy Props barrel (style and scale reference).
Inspection only. Nothing is exported and no source file is modified.
"""
import bpy, bmesh, json, math, os, sys, time
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
extracted, out_path, tiles = argv[:3]
PX = int(argv[3]) if len(argv) > 3 else 300
ONLY = argv[4] if len(argv) > 4 else None      # optional: inspect a single pack_id
SYN_BLEND = os.path.join(extracted, "synofplay-medieval-cafe", "all-merged.blend")


def remap_from_blend(objs, blend):
    """The cafe pack's FBX files carry geometry but their texture paths do not resolve; the creator's own
    all-merged.blend holds the same-named materials with the textures in ./tex. Swap them in by name."""
    names = sorted({s.material.name.split(".")[0] for o in objs for s in o.material_slots if s.material})
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        dst.materials = [n for n in names if n in src.materials and n not in bpy.data.materials or n in src.materials]
    got = {m.name.split(".")[0]: m for m in dst.materials if m}
    for o in objs:
        for s in o.material_slots:
            if s.material and s.material.name.split(".")[0] in got and s.material is not got[s.material.name.split(".")[0]]:
                s.material = got[s.material.name.split(".")[0]]
    return sorted(got)
os.makedirs(tiles, exist_ok=True)
REF = os.path.join(extracted, "quaternius-fantasy-props")

# pack_id: (publisher, pack, edition, sub-directory, extension, tile filter or None = every model)
PACKS = {
    "synofplay-medieval-cafe": ("Syntaxes of Play", "Medieval Cafe Asset Pack", "free (CC0 stated on the creator's page)", "fbx", ".fbx", None),
    "avramania-free-collection": ("Avramania", "Free Low-Poly Medieval Collection", "free collection 2026-10-28 (CC0, License.txt)", "", ".glb",
                                  ("Food_Market", "Village_Builder", "Props_Tools_Fencing", "Interiors_Furniture")),
    "kaykit-medieval-builder": ("Kay Lousberg (KayKit)", "Medieval Builder Pack (Legacy)", "1.0 free (CC0, License.txt)", "Models/objects/gltf", ".glb",
                                ("market", "house", "well", "castle", "mill")),
    "polypizza-quaternius-market-stalls": ("Quaternius via Poly Pizza", "Market Stalls", "single model (CC0 on page)", "", ".glb", None),
    "polypizza-quaternius-market-stand": ("Quaternius via Poly Pizza", "Market Stand", "single model (CC0 on page)", "", ".glb", None),
    "polypizza-quaternius-sign": ("Quaternius via Poly Pizza", "Sign", "single model (CC0 on page)", "", ".glb", None),
    "polypizza-quaternius-town-sign": ("Quaternius via Poly Pizza", "Town Sign", "single model (CC0 on page)", "", ".glb", None),
    "polypizza-ipoly3d-wooden-sign": ("iPoly3D via Poly Pizza", "Wooden Sign", "single model (CC0 on page)", "", ".glb", None),
}


def load(path):
    before = set(bpy.data.objects)
    if path.lower().endswith(".fbx"):
        bpy.ops.import_scene.fbx(filepath=path)
    else:
        bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def bounds(objs):
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    return lo, hi


def measure(meshes):
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    tris = verts = nonmanifold = 0
    has_uv, has_vcol, mats, images = True, False, {}, {}
    dg = bpy.context.evaluated_depsgraph_get()
    for o in meshes:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
        me.calc_loop_triangles()
        tris += len(me.loop_triangles); verts += len(me.vertices)
        has_uv = has_uv and bool(me.uv_layers); has_vcol = has_vcol or bool(me.color_attributes)
        bm = bmesh.new(); bm.from_mesh(me)
        nonmanifold += sum(1 for e in bm.edges if not e.is_manifold)
        bm.free(); ev.to_mesh_clear()
        for s in o.material_slots:
            m = s.material
            if not m:
                continue
            mats[m.name] = True
            if m.node_tree:
                for n in m.node_tree.nodes:
                    if n.type == "TEX_IMAGE" and n.image:
                        im = n.image
                        images[im.name] = [im.size[0], im.size[1], bool(im.has_data or im.size[0] > 0)]
    r = lambda v: round(float(v), 3)
    return {"blender_import_status": "IMPORTED", "dimensions_m": [r(hi.x - lo.x), r(hi.z - lo.z), r(hi.y - lo.y)],
            "bbox_min_xyz_gltf": [r(lo.x), r(lo.z), r(-hi.y)], "bbox_max_xyz_gltf": [r(hi.x), r(hi.z), r(-lo.y)],
            "triangle_count": tris, "vertex_count": verts, "mesh_objects": len(meshes), "materials": sorted(mats), "textures": images,
            "textures_loaded": all(v[2] for v in images.values()) if images else None,
            "has_uv": has_uv, "has_vertex_color": has_vcol, "non_manifold_edges": nonmanifold}


def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "BLENDER_WORKBENCH"):
        try:
            sc.render.engine = eng; break
        except TypeError:
            continue
    sc.render.resolution_x = sc.render.resolution_y = PX
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("neutral"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.82, 0.84, 0.88, 1); bg.inputs[1].default_value = 0.9
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.2; sun.data.angle = math.radians(6)
    sun.rotation_euler = (math.radians(52), 0, math.radians(-38))
    sc.collection.objects.link(sun)
    return sc


def figure(x, y):
    m = bpy.data.materials.new("scale_fig"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.05, 0.42, 0.45, 1); b.inputs["Roughness"].default_value = 0.9
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.56, location=(x, y, 0.78)); body = bpy.context.object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(x, y, 1.73)); head = bpy.context.object
    for o in (body, head):
        o.data.materials.append(m)
    return [body, head]


def frame(sc, lo, hi, direction=(0.95, -1.55, 0.95)):
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"
    d = Vector(direction).normalized()
    cam.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    bpy.context.view_layer.update()
    inv = cam.rotation_euler.to_matrix().inverted()
    pts = [inv @ Vector((x, y, z)) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
    xs, ys = [p.x for p in pts], [p.y for p in pts]
    cam.data.ortho_scale = max(max(xs) - min(xs), max(ys) - min(ys)) * 1.12
    cam.location = cam.rotation_euler.to_matrix() @ Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, 0)) + d * 200
    cam.data.clip_start, cam.data.clip_end = 1, 600


rows, t0 = [], time.time()
for pack_id, (publisher, pack, edition, sub, ext, flt) in PACKS.items():
    if ONLY and pack_id != ONLY:
        continue
    base = os.path.join(extracted, pack_id)
    files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(base, sub)) for f in fs if f.lower().endswith(ext))
    for p in files:
        name = os.path.splitext(os.path.basename(p))[0]
        rec = {"pack_id": pack_id, "publisher": publisher, "pack": pack, "edition": edition,
               "internal_filepath": os.path.relpath(p, base), "format": ext.lstrip("."), "asset_name": name}
        sc = setup_scene()
        try:
            new = load(p)
        except Exception as e:
            rec.update({"blender_import_status": "FAILED", "error": repr(e)[:200]}); rows.append(rec); continue
        meshes = [o for o in new if o.type == "MESH"]
        if not meshes:
            rec["blender_import_status"] = "IMPORTED_NO_MESH"; rows.append(rec); continue
        bpy.context.view_layer.update()
        if pack_id == "synofplay-medieval-cafe":
            rec["materials_remapped_from_blend"] = remap_from_blend(meshes, SYN_BLEND)
        rec.update(measure(meshes))
        rows.append(rec)
        want = flt is None or any(k in rec["internal_filepath"] or k == name for k in flt)
        if not want:
            continue
        lo, hi = bounds(meshes); lo.z = min(lo.z, 0.0)
        refs = []
        small = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z) < 1.3
        for o in load(os.path.join(REF, "Exports", "glTF", "Barrel.gltf")) if os.path.exists(os.path.join(REF, "Exports", "glTF", "Barrel.gltf")) else []:
            if o.parent is None:
                o.location.x += hi.x + 0.75; o.location.y += lo.y + 0.3
            if o.type == "MESH":
                refs.append(o)
        if not small:
            refs += figure(hi.x + 1.7, lo.y + 0.2)
        bpy.context.view_layer.update()
        lo2, hi2 = bounds(meshes + refs); lo2.z = min(lo2.z, 0.0)
        frame(sc, lo2, hi2)
        sc.render.filepath = os.path.join(tiles, f"{pack_id}__{name}.png")
        bpy.ops.render.render(write_still=True)
    print(f"[inspect] {pack_id}: {len(files)} files, {time.time() - t0:.0f}s", flush=True)
json.dump(rows, open(out_path, "w"), indent=1)
print("[inspect] wrote", out_path, len(rows))
