#!/usr/bin/env python3
"""Asset provenance records for the production kit: every downloaded model that the kit instantiates, resolved to its exact source file.

For each asset id (as recorded by the kit export in kit-report.json "usage") this resolves the pack, the file inside the extracted archive, its SHA-256 and size, and the licence
evidence that ships with that pack (file hash and first licence line). Items authored for this project (CUS-*) are listed separately and are not downloaded geometry.
Usage: python3 p2a_provenance.py <inspection_dir> <kit-report.json> <out_dir> [batch2_assets.json]
"""
import csv, hashlib, json, os, sys
from collections import Counter

INSPECT, KIT, OUT = sys.argv[1:4]
B2 = set(json.load(open(sys.argv[4]))) if len(sys.argv) > 4 else set()
PREV = {r["asset_id"] for r in json.load(open(sys.argv[5]))["downloaded"]} if len(sys.argv) > 5 else set()   # P2-B batch 2 register: anything not in it is new in this batch (batch 4: previous register = batch 3)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p2a_bazaar import load_dims                                   # noqa: E402

PACKS = {
    "quaternius-medieval-village": ("Quaternius Medieval Village MegaKit [Standard]", "Quaternius", "CC0 1.0", "Medieval Village MegaKit[Standard]/License_Standard.txt", "licence file inside the archive"),
    "quaternius-fantasy-props": ("Quaternius Fantasy Props MegaKit [Standard]", "Quaternius", "CC0 1.0", "License_Standard.txt", "licence file inside the archive"),
    "quaternius-stylized-nature": ("Quaternius Stylized Nature MegaKit [Standard]", "Quaternius", "CC0 1.0", "License_Standard.txt", "licence file inside the archive"),
    "avramania-free-collection": ("Avramania Free Low-Poly Medieval Collection", "Avramania", "CC0 1.0", "Avramania_Free_Collection/License.txt", "License.txt in the archive and the creator's page; ReadMe states the models were built by scripts written with an AI coding assistant (not AI 3D generation)"),
    "synofplay-medieval-cafe": ("Syntaxes of Play Medieval Cafe Asset Pack", "Syntaxes of Play", "CC0 1.0 (stated on the creator's page only)", None, "NO licence file in the archive: keep a dated copy of the creator's page with the P2 assets (P1.2 register 04)"),
}
dims = load_dims(INSPECT); kit = json.load(open(KIT)); usage = kit.get("usage", {})


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


lic_cache = {}
rows, custom, missing = [], [], []
for aid, n in sorted(usage.items()):
    base = aid.split("@")[0]; variant = aid.split("@")[1] if "@" in aid else ""
    if base.startswith("CUS-"):
        custom.append({"asset": aid, "placed": n, "note": "authored for this project (flat-colour materials, no third-party geometry)"}); continue
    d = dims.get(base)
    if not d:
        missing.append(aid); continue
    pack = d["pack"]; name, pub, lic, licfile, cond = PACKS.get(pack, (pack, "?", "?", None, "unknown pack"))
    src = os.path.join(INSPECT, "extracted", pack, d["file"])
    lic_path = os.path.join(INSPECT, "extracted", pack, licfile) if licfile else None
    if lic_path and lic_path not in lic_cache:
        lic_cache[lic_path] = (sha(lic_path), open(lic_path, errors="ignore").read().strip().splitlines()) if os.path.exists(lic_path) else (None, [])
    lh, ltxt = lic_cache.get(lic_path, (None, []))
    rows.append({"asset_id": aid, "base_asset": base, "colour_variant": variant, "placements_in_kit": n, "batch2_extra": base in B2 or aid in B2, "new_in_batch4": bool(PREV) and aid not in PREV, "pack": name, "publisher": pub, "pack_id": pack,
                 "source_file": d["file"], "source_exists": os.path.exists(src), "source_bytes": os.path.getsize(src) if os.path.exists(src) else None, "source_sha256": sha(src) if os.path.exists(src) else None,
                 "triangles_source": d["tris"], "licence": lic, "licence_file": licfile or "(none in archive)", "licence_file_sha256": lh, "licence_condition": cond})
os.makedirs(OUT, exist_ok=True)
cols = list(rows[0].keys())
with open(os.path.join(OUT, "asset-provenance.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
summary = {"downloaded_assets": len(rows), "by_pack": dict(Counter(r["pack"] for r in rows)), "custom_assets": len(custom), "unresolved": missing, "source_files_found": sum(1 for r in rows if r["source_exists"]),
           "licence_files": {k.split("extracted/")[1]: v[0] for k, v in lic_cache.items()}, "packs": {k: {"name": v[0], "licence": v[2], "condition": v[4]} for k, v in PACKS.items() if any(r["pack_id"] == k for r in rows)}}
json.dump({"summary": summary, "custom": custom, "downloaded": rows}, open(os.path.join(OUT, "asset-provenance.json"), "w"), indent=1)
print(json.dumps(summary, indent=1)[:1500])
