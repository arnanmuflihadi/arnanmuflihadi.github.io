#!/usr/bin/env python3
"""Shared architecture / asset registry for the Merchant Citadel kit: one row per production GLB node.

Reads: kit-report.json (Blender export), scene.json (instances, collision), the P1.4 archetype table (provenance, readiness) and the
building schedule. Writes asset-registry.csv and asset-registry.json next to the P2-A closeout documents.
Usage: python3 p2a_registry.py <kit-report.json> <scene.json> <p1.4 dir> <out dir>
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

KIT, SCENE, P14, OUT = sys.argv[1:5]
kit = json.load(open(KIT)); sc = json.load(open(SCENE))
LICENCE = {"Q. Medieval Village": "CC0 (Quaternius Medieval Village MegaKit), P1.2 register", "Q. Fantasy Props": "CC0 (Quaternius Fantasy Props MegaKit), P1.2 register",
           "SoP Medieval Cafe": "CC0 stated on the page only (Syntaxes of Play); FBX materials re-linked", "Avramania": "CC0 (Avramania Food & Market / Village Builder); ReadMe checked, AI-built packs rejected",
           "custom": "authored for this project (no third-party licence)"}
prov = {}
for line in open(os.path.join(P14, "07-archetype-construction-specifications.md"), encoding="utf-8"):
    m = re.match(r"\|\s*(A\d+[a-z]?m?)\s*\|(.*)\|", line)
    if m:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 10:
            prov[cells[0]] = {"purpose": cells[1].replace("**", ""), "sources": cells[8], "readiness": cells[9]}
parts_of = {"A01_main": "A01", "A01_wing_w": "A01", "A01_wing_e": "A01", "A01_porch": "A01", "A01_tower": "A01", "A02p": "A02", "A02c": "A02", "A06s": "A06", "A06j": "A06", "A04bP": "A04b", "A04bO": "A04b", "A03cC": "A03c", "A07w": "A07", "A05c": "A05", "A03cT": "A03c"}
inst = defaultdict(list)
for i in sc["instances"]:
    inst[i["node"]].append(i["id"])
coll = defaultdict(Counter)
for o in sc["collision"]:
    coll[o["src"]][o["group"]] += 1
STATUS = {"P2-A": ["A03", "A03b", "A04", "A04b", "A08", "A09", "A10c", "A10p", "A11", "CROSS", "TERRACE", "PODIUM", "ARCH", "TILE_cobble", "TILE_brick", "TILE_red", "DRESSING"],
          "P2-B batch 1": ["A01_main", "A01_wing_w", "A01_wing_e", "A01_porch", "A01_tower"]}
STATUS["P2-B batch 2"] = ["A02p", "A02c"]
STATUS["P2-B batch 3"] = ["A06s", "A06j", "A04bP", "A04bO", "A03cC", "DRESSING_D1", "DRESSING_D6"]
STATUS["P2-B batch 4"] = ["A07w", "A05c", "A03cT", "DRESSING_D7"]
STATUS["P2-B batch 5"] = ["A11a", "A11c", "SIGN_CUS-Sign_Compass_wood_x1p4"]   # B15, B16 and the compass sign; modified earlier nodes (A07w, A05c, roof grades, terrace dressing) keep the status of the batch that created them
status_of = {n: s for s, ns in STATUS.items() for n in ns}
status_of.update({n: "P2-B batch 2" for n in kit["nodes"] if n.startswith(("SIGN_", "DRESSING_D")) and n not in ("DRESSING_D1", "DRESSING_D6", "DRESSING_D7")})
status_of.update({n: "P2-B batch 5" for n in STATUS["P2-B batch 5"]})   # after the generic SIGN_/DRESSING_ rule above
rows = []
for name, st in kit["nodes"].items():
    base = parts_of.get(name, name); p = prov.get(base, {})
    srcs = [s.strip() for s in p.get("sources", "custom, Q. Medieval Village").split(",")]
    if name.startswith("SIGN_"):
        srcs = ["Q. Fantasy Props"] if "FP-" in name else ["custom"]
    elif name.startswith("DRESSING_"):
        srcs = ["Q. Medieval Village", "Q. Fantasy Props", "SoP Medieval Cafe", "Avramania", "custom"]
    mats = st["materials"]
    rows.append({
        "node": name, "archetype": base, "purpose": p.get("purpose", {"CROSS": "Market cross, guild emblem on a stone base", "TERRACE": "Civic terrace steps, skirt, balustrade", "PODIUM": "Hall podium deck and steps",
                     "ARCH": "Gate arch closing a street gap"}.get(name, "paving tile" if name.startswith("TILE_") else ("Trade sign or banner placed on a building front" if name.startswith("SIGN_") else ("Static dressing of one district (benches, barrels, lamps, bunting)" if name.startswith("DRESSING_") else "")))),
        "status": status_of.get(name, "P2-A"), "instances_in_slice": ";".join(inst.get(name, [])), "triangles": st["triangles"], "vertices": st["vertices"], "primitives": st["primitives"],
        "material_names": len(mats), "baked_vertex_ao": name in kit.get("ao", {}).get("nodes", {}), "bbox_gltf_m": st["bbox_gltf"],
        "sources": "; ".join(srcs), "licence_notes": " | ".join(LICENCE.get(s, "see P1.2 register") for s in srcs), "p1_4_readiness": p.get("readiness", ""),
        "collision_groups": {} if name.startswith(("SIGN_", "DRESSING_")) else (dict(coll["B01"]) if name == "A01_main" else {}) if name.startswith("A01_") else (dict(sum((coll[i.split("_")[0]] if i.split("_")[0] in coll else coll[i] for i in inst.get(name, [])), Counter())) if inst.get(name) else {}),
    })
json.dump({"revision": "P2-B batch 5", "glb_bytes": kit["glb_bytes"], "texture_totals": kit["texture_totals"], "ao": kit.get("ao", {}), "nodes": rows}, open(os.path.join(OUT, "asset-registry.json"), "w"), indent=1)
with open(os.path.join(OUT, "asset-registry.csv"), "w", newline="") as f:
    w = csv.writer(f); cols = ["node", "archetype", "purpose", "status", "instances_in_slice", "triangles", "vertices", "primitives", "material_names", "baked_vertex_ao", "sources", "licence_notes", "p1_4_readiness", "collision_groups"]
    w.writerow(cols)
    for r in rows:
        w.writerow([json.dumps(r[c]) if isinstance(r[c], (dict, list)) else r[c] for c in cols])
print("registry rows", len(rows), "triangles", sum(r["triangles"] for r in rows))
