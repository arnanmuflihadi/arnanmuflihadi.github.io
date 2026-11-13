#!/usr/bin/env python3
"""P1.4 targeted asset research: download the FREE uploads of two further candidate packs for inspection.
Only the creators' own itch.io pages, free path (name-your-own-price with a zero minimum). Nothing is purchased.
Usage: python3 fetch_p14.py <archives_dir>     (appends to <archives_dir>/archive-manifest.json)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "p1", "blender-inspection"))
from fetch_expansion import itch

PACKS = [("wizp-stylized-medieval-village", "WizP", "https://wizp.itch.io/stylized-medieval-village", None),
         ("alefran-medieval-stylized-free", "Alefran", "https://alefrandev.itch.io/medieval-stylized-assets-pack-free", None)]
if __name__ == "__main__":
    dest = sys.argv[1]; recs = []
    for pack_id, publisher, page, flt in PACKS:
        try:
            r = itch(pack_id, publisher, page, flt, dest)
            for x in r:
                print("OK ", pack_id, x["archive_filename"], x["bytes"], x["sha256"][:16])
            recs += r
        except Exception as e:
            recs.append(dict(pack_id=pack_id, publisher=publisher, source_page=page, error=repr(e))); print("ERR", pack_id, repr(e))
    mpath = os.path.join(dest, "archive-manifest.json")
    prev = json.load(open(mpath)) if os.path.exists(mpath) else []
    json.dump([r for r in prev if r["pack_id"] not in {o["pack_id"] for o in recs}] + recs, open(mpath, "w"), indent=2)
