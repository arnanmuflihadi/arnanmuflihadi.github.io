#!/usr/bin/env python3
"""Reproducible download of the FREE archives inspected in Merchant Citadel P1.

Only free uploads are requested:
  * Quaternius itch.io pages -> the upload whose name ends in "[Standard].zip" (no price).
  * Kenney.nl -> the site's own "Continue without donating" signed link.
Paid Pro/Source uploads are never requested. Nothing is executed from the archives.

Usage:  python3 fetch_archives.py <dest_dir> [pack_id ...]
Writes: <dest_dir>/<pack_id>/<archive>.zip and <dest_dir>/archive-manifest.json
"""
import hashlib, html, http.cookiejar, json, os, re, sys, time, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
ITCH = [
    ("quaternius-medieval-village", "https://quaternius.itch.io/medieval-village-megakit"),
    ("quaternius-fantasy-props", "https://quaternius.itch.io/fantasy-props-megakit"),
    ("quaternius-stylized-nature", "https://quaternius.itch.io/stylized-nature-megakit"),
]
KENNEY = [
    ("kenney-fantasy-town-kit", "https://kenney.nl/assets/fantasy-town-kit"),
    ("kenney-modular-buildings", "https://kenney.nl/assets/modular-buildings"),
]


def opener():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders = [("User-Agent", UA)]
    return op, jar


def save(op, url, path, referer=None):
    req = urllib.request.Request(url, headers={"Referer": referer} if referer else {})
    h = hashlib.sha256()
    n = 0
    with op.open(req) as r, open(path, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
            h.update(b)
            n += len(b)
    return n, h.hexdigest()


def itch(pack_id, page, dest):
    op, jar = opener()
    t = op.open(page).read().decode("utf8", "ignore")
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', t).group(1)
    post = lambda u: json.loads(op.open(urllib.request.Request(
        u, data=urllib.parse.urlencode({"csrf_token": csrf}).encode(),
        headers={"X-Requested-With": "XMLHttpRequest", "Referer": page})).read())
    resp = post(page + "/download_url")
    if "url" not in resp:
        raise RuntimeError(f"download page refused: {resp}")
    dl_page = resp["url"]
    d = op.open(dl_page).read().decode("utf8", "ignore")
    # each upload block: data-upload_id="..." ... <strong title="<file name>" class="name">
    ups = re.findall(r'data-upload_id="([0-9]+)".*?<strong title="([^"]+)"', d, re.S)
    free = [(i, html.unescape(n)) for i, n in ups if "[Standard]" in n]
    if len(free) != 1:
        raise RuntimeError(f"expected exactly one free [Standard] upload, found {ups}")
    uid, name = free[0]
    resp = post(f"{page}/file/{uid}?source=game_download")  # free uploads need no key
    if "url" not in resp:
        raise RuntimeError(f"file link refused: {resp}")
    url = resp["url"]
    os.makedirs(os.path.join(dest, pack_id), exist_ok=True)
    path = os.path.join(dest, pack_id, name)
    size, sha = save(op, url, path, referer=dl_page)
    return dict(pack_id=pack_id, publisher="Quaternius", edition="Standard (free)", source_page=page,
                distribution="official itch.io upload", upload_id=uid, archive_filename=name,
                bytes=size, sha256=sha, listed_uploads=[n for _, n in ups])


def kenney(pack_id, page, dest):
    op, jar = opener()
    t = op.open(page).read().decode("utf8", "ignore")
    did = re.search(r"data-download-id='([0-9a-f]+)'", t).group(1)
    version = (re.search(r"Version</[^>]+>\s*<[^>]+>\s*([0-9.]+)", t) or [None, "UNKNOWN"])[1]
    info = json.loads(op.open(urllib.request.Request(
        "https://kenney.nl/download-link/" + did, headers={"Referer": page})).read())
    url = info["url"]
    name = os.path.basename(urllib.parse.urlparse(url).path)
    os.makedirs(os.path.join(dest, pack_id), exist_ok=True)
    path = os.path.join(dest, pack_id, name)
    size, sha = save(op, url, path, referer=page)
    return dict(pack_id=pack_id, publisher="Kenney", edition=f"free download (page version {version})",
                source_page=page, distribution="official kenney.nl signed link", archive_filename=name,
                bytes=size, sha256=sha)


if __name__ == "__main__":
    dest = sys.argv[1]
    os.makedirs(dest, exist_ok=True)
    out = []
    only = set(sys.argv[2:])
    for fn, items in ((itch, ITCH), (kenney, KENNEY)):
        for pack_id, page in items:
            if only and pack_id not in only:
                continue
            try:
                rec = fn(pack_id, page, dest)
                rec["downloaded_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                print("OK ", pack_id, rec["archive_filename"], rec["bytes"], rec["sha256"][:16])
            except Exception as e:  # record the failure honestly, keep going
                rec = dict(pack_id=pack_id, source_page=page, error=repr(e))
                print("ERR", pack_id, repr(e))
            out.append(rec)
    mpath = os.path.join(dest, "archive-manifest.json")
    prev = json.load(open(mpath)) if os.path.exists(mpath) else []
    keep = [r for r in prev if r["pack_id"] not in {o["pack_id"] for o in out}]
    json.dump(keep + out, open(mpath, "w"), indent=2)
