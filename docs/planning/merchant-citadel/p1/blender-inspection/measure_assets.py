"""Headless Blender inspection: import every glTF/GLB of the freshly downloaded packs and measure it.

Run:  Blender --background --factory-startup --python measure_assets.py -- <extracted_dir> <out.json>

Inspection only. Nothing is exported and no source file is modified.
Dimensions are reported in glTF space (X = width, Y = up, Z = depth), metres as authored (no rescale).
"""
import bpy, bmesh, json, os, sys, time
from mathutils import Vector

extracted, out_path = sys.argv[sys.argv.index("--") + 1:][:2]

PACKS = {
    "quaternius-medieval-village": ("Quaternius", "Medieval Village MegaKit", "Standard (free)", ".gltf"),
    "quaternius-fantasy-props": ("Quaternius", "Fantasy Props MegaKit", "Standard (free)", ".gltf"),
    "quaternius-stylized-nature": ("Quaternius", "Stylized Nature MegaKit", "Standard (free)", ".gltf"),
    "kenney-fantasy-town-kit": ("Kenney", "Fantasy Town Kit", "2.0 (free)", ".glb"),
    "kenney-modular-buildings": ("Kenney", "Modular Buildings", "free", ".glb"),
}


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def measure(path):
    clear()
    try:
        bpy.ops.import_scene.gltf(filepath=path)
    except Exception as e:  # record import failures instead of hiding them
        return {"blender_import_status": "FAILED", "error": repr(e)[:200]}
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        return {"blender_import_status": "IMPORTED_NO_MESH"}
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    tris = verts = nonmanifold = 0
    has_uv = True
    has_vcol = False
    mats, images = {}, {}
    dg = bpy.context.evaluated_depsgraph_get()
    for o in meshes:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
        me.calc_loop_triangles()
        tris += len(me.loop_triangles); verts += len(me.vertices)
        has_uv = has_uv and bool(me.uv_layers)
        has_vcol = has_vcol or bool(me.color_attributes)
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
    # Blender Z-up -> glTF Y-up: width=X, height=Z, depth=Y
    r = lambda v: round(float(v), 3)
    return {
        "blender_import_status": "IMPORTED",
        "dimensions_m": [r(hi.x - lo.x), r(hi.z - lo.z), r(hi.y - lo.y)],
        "bbox_min_xyz_gltf": [r(lo.x), r(lo.z), r(-hi.y)],
        "bbox_max_xyz_gltf": [r(hi.x), r(hi.z), r(-lo.y)],
        "triangle_count": tris, "vertex_count": verts, "mesh_objects": len(meshes),
        "materials": sorted(mats), "textures": images,
        "textures_loaded": all(v[2] for v in images.values()) if images else None,
        "has_uv": has_uv, "has_vertex_color": has_vcol, "non_manifold_edges": nonmanifold,
    }


rows, t0 = [], time.time()
for pack_id, (publisher, pack, edition, ext) in PACKS.items():
    base = os.path.join(extracted, pack_id)
    files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(base) for f in fs if f.lower().endswith(ext))
    for p in files:
        rec = {"pack_id": pack_id, "publisher": publisher, "pack": pack, "edition": edition,
               "internal_filepath": os.path.relpath(p, base), "format": ext.lstrip("."),
               "asset_name": os.path.splitext(os.path.basename(p))[0]}
        rec.update(measure(p))
        rows.append(rec)
    print(f"[measure] {pack_id}: {len(files)} files, {time.time() - t0:.0f}s elapsed", flush=True)
json.dump(rows, open(out_path, "w"), indent=1)
print("[measure] wrote", out_path, len(rows))
