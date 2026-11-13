#!/usr/bin/env python3
"""Reproducible download of the additional FREE candidate archives examined in the P1.2 targeted asset expansion.

Only free uploads on the creators' own itch.io pages are requested (the "No thanks, just take me to the
downloads" path of a name-your-own-price page with a zero minimum). Nothing is purchased, no account or key is
used and nothing is executed from the archives.  A page that refuses the free path is recorded as an error.

Usage:  python3 fetch_expansion.py <dest_dir> [pack_id ...]
Writes: <dest_dir>/<pack_id>/<archive> and appends to <dest_dir>/archive-manifest.json
"""
import hashlib, html, json, os, re, sys, time, urllib.parse, urllib.request
from fetch_archives import opener, save

ITCH = [  # pack_id, publisher, creator page, upload-name filter (regex) or None for every listed upload
    ("synofplay-medieval-cafe", "Syntaxes of Play", "https://synofplay.itch.io/medieval-caf-asset-pack-free", None),
    ("avramania-free-collection", "Avramania", "https://avramania.itch.io/free-collection", None),
    ("kaykit-medieval-builder", "Kay Lousberg (KayKit)", "https://kaylousberg.itch.io/kaykit-medieval-builder-pack", None),
]


POLY = [  # individual Poly Pizza models: pack_id, model page. Licence and file URL are read from the model page itself.
    ("polypizza-quaternius-market-stalls", "https://poly.pizza/m/jSqGy8V0MQ"),
    ("polypizza-quaternius-market-stand", "https://poly.pizza/m/DGIM5HGISb"),
    ("polypizza-quaternius-sign", "https://poly.pizza/m/4MSsNFk5fc"),
    ("polypizza-quaternius-town-sign", "https://poly.pizza/m/VSZubp0ru3"),
    ("polypizza-ipoly3d-wooden-sign", "https://poly.pizza/m/SpRHK36gNl"),
]


def poly(pack_id, page, dest):
    op, jar = opener()
    t = op.open(page).read().decode("utf8", "ignore")
    url = re.search(r'https://static\.poly\.pizza/[0-9a-f-]+\.glb', t).group(0)
    lic = re.search(r'creativecommons\.org/[a-z]+/[a-z-]+/[0-9.]+', t)
    title = ("iPoly3D" if "ipoly3d" in pack_id else "Quaternius") + " (via Poly Pizza)"
    os.makedirs(os.path.join(dest, pack_id), exist_ok=True)
    name = pack_id.replace("polypizza-", "") + ".glb"
    size, sha = save(op, url, os.path.join(dest, pack_id, name), referer=page)
    return [dict(pack_id=pack_id, publisher=title, edition="single model, free download", source_page=page, file_url=url,
                 licence_link_on_page=("https://" + lic.group(0)) if lic else "NOT FOUND", distribution="Poly Pizza static file",
                 archive_filename=name, bytes=size, sha256=sha, downloaded_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))]


def itch(pack_id, publisher, page, flt, dest):
    op, jar = opener()
    t = op.open(page).read().decode("utf8", "ignore")
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', t).group(1)
    post = lambda u: json.loads(op.open(urllib.request.Request(
        u, data=urllib.parse.urlencode({"csrf_token": csrf}).encode(),
        headers={"X-Requested-With": "XMLHttpRequest", "Referer": page})).read())
    resp = post(page + "/download_url")
    if "url" not in resp:
        raise RuntimeError(f"free download path refused: {resp}")
    dl_page = resp["url"]
    d = op.open(dl_page).read().decode("utf8", "ignore")
    ups = [(i, html.unescape(n)) for i, n in re.findall(r'data-upload_id="([0-9]+)".*?<strong title="([^"]+)"', d, re.S)]
    want = [(i, n) for i, n in ups if not flt or re.search(flt, n)]
    if not want:
        raise RuntimeError(f"no matching upload among {ups}")
    out = []
    os.makedirs(os.path.join(dest, pack_id), exist_ok=True)
    for uid, name in want:
        resp = post(f"{page}/file/{uid}?source=game_download")
        if "url" not in resp:
            raise RuntimeError(f"file link refused for {name}: {resp}")
        size, sha = save(op, resp["url"], os.path.join(dest, pack_id, name), referer=dl_page)
        out.append(dict(pack_id=pack_id, publisher=publisher, edition="free download (name-your-own-price page, zero minimum)",
                        source_page=page, distribution="official itch.io upload", upload_id=uid, archive_filename=name,
                        bytes=size, sha256=sha, listed_uploads=[n for _, n in ups],
                        downloaded_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
    return out


if __name__ == "__main__":
    dest = sys.argv[1]
    only = set(sys.argv[2:])
    recs = []
    for pack_id, publisher, page, flt in ITCH:
        if only and pack_id not in only:
            continue
        try:
            r = itch(pack_id, publisher, page, flt, dest)
            for x in r:
                print("OK ", pack_id, x["archive_filename"], x["bytes"], x["sha256"][:16])
            recs += r
        except Exception as e:
            recs.append(dict(pack_id=pack_id, publisher=publisher, source_page=page, error=repr(e)))
            print("ERR", pack_id, repr(e))
    for pack_id, page in POLY:
        if only and pack_id not in only:
            continue
        try:
            r = poly(pack_id, page, dest)
            print("OK ", pack_id, r[0]["publisher"], r[0]["bytes"], r[0]["licence_link_on_page"])
            recs += r
        except Exception as e:
            recs.append(dict(pack_id=pack_id, source_page=page, error=repr(e)))
            print("ERR", pack_id, repr(e))
    mpath = os.path.join(dest, "archive-manifest.json")
    prev = json.load(open(mpath)) if os.path.exists(mpath) else []
    keep = [r for r in prev if r["pack_id"] not in {o["pack_id"] for o in recs}]
    json.dump(keep + recs, open(mpath, "w"), indent=2)
