"""Build bounded S1 research outputs from saved source evidence; no production writes."""
import csv, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V = ROOT / 'validation/asset-selection-s1'
OUT = ROOT / 'docs/urban-atlas/asset-selection-s1'
OUT.mkdir(parents=True, exist_ok=True)
d = json.loads((V/'source-audit.json').read_text())
pages = {p['url']: p for p in d['pages']}
CC0 = 'https://creativecommons.org/publicdomain/zero/1.0/'
catalog_ids = {16,22,28,34,35,36,37,39,40,51,52,53,54,*range(55,64)}
local = {1:'assets/game/scenery/architecture-library.glb',3:'source-assets/r0b1/kenney_modular-buildings.zip',4:'source-assets/r0b1/kenney_building-kit.zip',20:'assets/game/scenery/canopy-tree.glb'}
notes = {
1:'Already local Standard subset; Boston/NYC style. Reuse street props, reject complete buildings as tropical default.',
2:'NEW: four FBX buildings + 32px original atlas acquired through official public Drive. Parts only; full buildings fail concept fit.',
3:'Already local: 108 GLBs; current page advertises 100 files. Component reservoir, not finished town architecture.',
4:'Already local: 79 GLBs; current page advertises 80 files. Roof/opening complement; no redownload.',
5:'Preview inspected: generic towers and rectangular blocks; reject finished town use.',
6:'Defer: suburban typology; not needed after local audit.',
7:'Preview inspected: industrial/grunge texture vocabulary conflicts with warm tropical concept; reject.',
8:'Defer: no car-road network needed; existing paving sufficient.',
9:'Defer: use pedestrian ground treatment; no road-system acquisition.',
10:'Preview inspected: Tudor/gabled village. CC0 Blend + original textures; reject medieval primary architecture.',
11:'Preview inspected: emissive night-city blocks. Blend + individual glTF; reject generic block façades.',
12:'Preview inspected: roofs/stalls may supply fantasy accent, not core architecture. Official ZIP request returned HTTP403; NOT acquired.',
13:'Medieval primary style unsuitable; not acquired.',14:'Retro fantasy style not shortlisted; not acquired.',15:'RTS-scale fantasy architecture not shortlisted.',
19:'Andrew Jepson; CC BY4.0 linked on page. 10.7k tris/5.8k vertices. Composition reference only; no download or derivative made.',
20:'Already local Standard subset, tree and fern reused. No replacement nature pack needed.',
21:'Alternative nature deferred; keep working local vegetation.',23:'Alternative nature deferred; avoid incompatible stylization.',
24:'Kay Lousberg: free CC0 models distinct from paid EXTRA and SOURCE/Blend tiers. No purchase or download; existing nature adequate.',
29:'CC0 Standard free subset; source Blender tier paid. Props candidate deferred; existing local planter used.',
30:'Preview inspected: indoor shelving/counters, not an outdoor café/market-frontage solution.',
41:'Sci-fi components deferred: not an architecture baseline for this town.',
54:'Supplied blendkit.com resolves as Blendkit; no per-asset identity/license clearance. NOT acquired; do not assume catalog-wide rights.',
}

def metadata(s):
    i=int(s['id']);p=pages[s['url']];t=(V/p['page_text']).read_text();u=s['url']
    formats=[]
    for fmt in ['FBX','OBJ','Blend','glTF','GLB']:
        if re.search(r'\b'+fmt+r'\b',t,re.I): formats.append(fmt)
    count=re.search(r'(?:Models\s+(\d+)|Files\s+(\d+)×)',t)
    size=re.findall(r'\b\d+(?:\.\d+)?\s*(?:kB|MB)\b',t)
    license='Unverified per asset';creator='Catalog / individual creator';access='Catalog only; no file downloaded';licenseurl='Per-asset clearance required'
    if 'reodesuxz.itch.io' in u:
        creator='reodesuxz';license='Custom: commercial use, no attribution; source redistribution prohibited';licenseurl=u+' (LICENSE section)'
        access='Name-your-price/free option advertised; download not exercised'
        assert 'Please do not resell or redistribute the files' in t
    elif i not in catalog_ids and ('kenney.nl' in u or 'quaternius.com/packs/' in u):
        creator='Kenney' if 'kenney.nl' in u else 'Quaternius';license='CC0-1.0' if 'CC0' in t else 'Unverified';licenseurl=CC0 if 'CC0' in t else u
        access='Free download advertised; not acquired'
        if '60-70%' in t: access='Free Standard subset (60–70%); paid Pro/Source; no paid content acquired'
    elif i in [10,11]:
        creator='humble squirrel' if i==10 else 'leonkin';license='CC0-1.0';licenseurl=CC0;access='Free attachment advertised; not acquired'
        formats=['Blend'] if i==10 else ['Blend','glTF']
    elif i==19:
        creator='Andrew Jepson';license='CC-BY-4.0';licenseurl='https://creativecommons.org/licenses/by/4.0/';access='Download button present; authentication/file download not tested'
    elif i in [24,47,49]:
        creator='Kay Lousberg';license='CC0-1.0 (free models); paid tiers separate';licenseurl=u+' (license/tier sections)';access='Free tier advertised; paid EXTRA/SOURCE not acquired'
    if i in local: access='ALREADY LOCAL; no redownload'
    if i==2: access='ACQUIRED four individual FBX files + atlas; free original public download'
    if i==12: access='Free advertised; direct ZIP returned HTTP403; manual download required'
    note=notes.get(i,'Future candidate only; no download.' if 45<=i<=50 else 'Not shortlisted; no download.')
    if i in catalog_ids and i!=54: note='Discovery catalog/homepage only; exact pack/file and per-asset rights not cleared. No broad catalog downloads.'
    if i in [28,36,51,52]:
        creator='Poly Haven';license='CC0-1.0 assets; catalog only';licenseurl='https://polyhaven.com/license';note='Official asset-license page verified CC0; no particular model/material selected or downloaded.'
    if i==53:
        creator='ambientCG';license='CC0-1.0 assets; catalog only';licenseurl='https://docs.ambientcg.com/license/';note='Official asset-license page verified CC0; no particular material selected or downloaded.'
    if 'reodesuxz.itch.io' in u: note='No acquisition: source-redistribution prohibition conflicts with publishing raw files on public GitHub. Embedded game delivery rights need clarification before use.'
    return creator,license,licenseurl,access,','.join(formats) or 'Not verified',','.join(size) or 'Not measured',count.group(1) or count.group(2) if count else 'Not counted',note

lines=['# S1 asset catalog','',f'Checked {d["checked_utc"]}. All 63 supplied entries / 54 unique pages responded HTTP200. This verifies page access, not a working archive, license for every marketplace item, or visual suitability. Raw bounded page evidence is in `validation/asset-selection-s1/source-audit.json` and `pages/`.','',
'No paid content acquired. Only one new architecture pack sampled: four individual FBX models and its original atlas. Existing archives, source licenses, island, blockout and website were preserved. Exact model provenance and file hashes: `validation/asset-selection-s1/acquisition-manifest.json`.','',
'Sizes below are page-advertised attachment sizes when shown, not measured full-pack sizes. Counts are advertised pack file/model totals, not useful architectural component counts. Formats absent from a page remain unverified. Source Blender files in paid tiers are not treated as free.','']
seen={}
for category in ['A1','A2','A3','A4','A5','A6','A7','A8']:
    lines += ['## '+category,'','| # / source | Creator / license | Formats / advertised count / size | Availability and relevance |','|---|---|---|---|']
    for s in d['sources']:
        if s['category']!=category:continue
        i=int(s['id']);creator,lic,lu,access,fmt,size,count,note=metadata(s)
        dup=' Duplicate URL of #'+str(seen[s['url']])+'.' if s['url'] in seen else ''
        seen.setdefault(s['url'],i)
        evidence='../../../validation/asset-selection-s1/'+pages[s['url']]['page_text']
        lines.append(f'| {i}. [{s["title"]}]({s["url"]}) | {creator}; [{lic}]({lu.split(" (")[0] if lu.startswith("http") else s["url"]}) | {fmt}; {count}; {size} | {access}. {note}{dup} [Evidence]({evidence}) |')
    lines.append('')
lines += ['## Download/access limits','',
'Kenney Fantasy Town: open the official page → Download → Continue without donating. The actual download link returned HTTP403 in this run. If it persists, use the creator’s official itch.io link from their page. No alternate guessed mirror or bypass was used. File formats and archive size remain unverified for this pack.','',
'Quaternius Ultimate Buildings: official page links to the public [original folder](https://drive.google.com/drive/folders/1RE3qXhbE5yGS3t-xGFJ8GmOtTgCUF3LQ). Only four finished-building FBXs and Texture_Light.png were fetched. Original license inspected in that folder; no paid Source tier used.','',
'CC0 permits adaptation and raw public redistribution without required attribution; credits are retained. CC BY4.0 requires creator/source/license attribution and change indication. Marketplace catalogs do not confer uniform rights. Every reodesuxz pack was individually checked for its redistribution restriction; none was downloaded. Preview images retained locally for evaluation are creator promotional references, not game assets cleared for redistribution. Do not publish those preview images as project-owned assets.','',
'Original generated concept boards were found in the supplied image attachments and copied into `validation/asset-selection-s1/references/`. Embedded old instructions are historical image content, not authorization to build. No missing-reference claim is needed.']
(OUT/'ASSET-CATALOG.md').write_text('\n'.join(lines)+'\n')

# Six separate scores: concept fit, richness, coherence, editability, realtime, license.
rows=[
('A1',2,'2Story_Balcony.fbx',[2,3,3,4,5,5],'CONDITIONAL PARTS','Balcony/cornice source only; black diagonal at balcony needs repair; poor storefront'),
('A2',2,'2Story_Columns.fbx',[3,3,3,4,5,5],'CONDITIONAL PARTS','Columns/porch vocabulary; rebuild glazing and thresholds later'),
('A3',2,'1Story_GableRoof.fbx',[2,2,3,4,5,5],'REJECT COMPLETE BUILDING','Gable geometry reference only; small windows and oversized closed door'),
('A4',2,'2Story_RoundRoof.fbx',[2,2,3,4,5,5],'REJECT COMPLETE BUILDING','Barrel roof reference only; blank upper frontage'),
('K1',3,'',[3,2,4,5,5,5],'REUSE COMPONENTS','Best primary component pack already local; not an approved ready-made facade'),
('K2',4,'',[3,3,4,5,5,5],'REUSE COMPLEMENT','Existing roof/opening parts; no new download'),
('Q0',1,'',[2,3,2,4,4,5],'REJECT BUILDINGS / REUSE PROPS','Planter/street-detail sample only; Western full buildings unsuitable'),
('N1',20,'',[4,4,4,4,4,5],'KEEP LOCAL NATURE','Existing tree/fern; no new nature pack'),
('P5',5,'',[1,2,2,3,5,5],'REJECT','Generic towers / block facades'),
('P7',7,'',[2,3,2,4,5,5],'REJECT','Industrial texture style incompatible'),
('P10',10,'',[1,3,2,4,4,5],'REJECT','Tudor village; not modern tropical'),
('P11',11,'',[2,2,2,4,4,5],'REJECT','Night-emissive boxes; unsuitable primary architecture'),
('P12',12,'',[3,3,3,4,5,5],'DEFER / DOWNLOAD BLOCKED','Fantasy roof/prop reference; advertised modularity not actual imported-mesh verification'),
('P17',17,'',[2,2,3,4,5,1],'REJECT','Plain hut style and source redistribution restriction'),
('P30',30,'',[2,2,3,3,5,5],'DEFER','Interior mini-market; not streetside frontage')]
with (OUT/'ASSET-SHORTLIST.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['candidate_id','asset_name','source_url','local_file_path','license','format','concept_fit','architectural_richness','style_coherence','blender_editability','realtime_suitability','license_suitability','visual_quality_score','technical_suitability','recommended_use','status'])
    for cid,sid,filename,scores,status,note in rows:
        s=next(s for s in d['sources'] if int(s['id'])==sid);meta=metadata(s)
        path='validation/asset-selection-s1/acquired/quaternius-ultimate-buildings/'+filename if filename else local.get(sid,'')
        w.writerow([cid,filename or s['title'],s['url'],path,meta[1],'FBX' if filename else meta[4],*scores,round(sum(scores[:3])/3,2),'Actual Blender import' if filename else 'Local verified assets' if sid in local else 'Preview/page only',note,status])

ids={'2Story_Columns.fbx':'1FVcUDiQ9DpnLFT5lxWEs1N7Yodzs7go-','2Story_RoundRoof.fbx':'1qMZUknI8ztZ2TolsMysWsfSyDyfj-_J1','1Story_GableRoof.fbx':'12NomxtrKA2m9C8_YQBvcYla_7cDkBCPA','Texture_Light.png':'1mhju4DYyluV21jtQh-LUWnaEpT5lN_GX'}
folder='https://drive.google.com/drive/folders/1X3vM9MO2XvGEbM7pmA0LwsOz9PUW1Jrl'
files=[]
for p in sorted((V/'acquired/quaternius-ultimate-buildings').iterdir()):
    files.append({'file':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':'https://drive.google.com/file/d/'+ids[p.name]+'/view' if p.name in ids else folder+' (exact filename)' if p.suffix=='.fbx' else 'https://drive.google.com/file/d/1tSk6QjHVGJtpPSDuggR02LyNgO0bBG7g/view'})
(V/'acquisition-manifest.json').write_text(json.dumps({'phase':'S1','creator':'Quaternius','source_page':'https://quaternius.com/packs/ultimatetexturedbuildings.html','license':'CC0-1.0','license_url':CC0,'attribution_required':False,'files':files,'new_model_files':4,'new_pack_count':1,'full_pack_downloaded':False,'public_raw_redistribution':'Permitted for these CC0 files; not blanket clearance for catalog candidates'},indent=2)+'\n')
print('Wrote catalog, shortlist and exact acquisition manifest')
