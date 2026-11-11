#!/usr/bin/env python3
"""Verify the selected glTF sources and their dependencies inside official Standard archives."""
import argparse
import datetime
import hashlib
import json
import pathlib
import posixpath
import urllib.parse
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--city', required=True, type=pathlib.Path)
parser.add_argument('--nature', required=True, type=pathlib.Path)
parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('assets/game/scenery/verification.json'))
args = parser.parse_args()
sha = lambda data: hashlib.sha256(data).hexdigest()
architecture = json.loads(pathlib.Path('assets/game/scenery/architecture-source.json').read_text())
scenery = json.loads(pathlib.Path('assets/game/scenery/source.json').read_text())
records = [dict(m, pack='downtown-city-megakit', sourceFile='Exports/glTF (Godot)/'+m['sourceFile']) for m in architecture['models']]
records += [m for m in scenery['models'] if m['id'] != 'city-building']
archives = {}
for pack, path in [('downtown-city-megakit', args.city), ('stylized-nature-megakit', args.nature)]:
    with zipfile.ZipFile(path) as archive:
        license_bytes = archive.read('License_Standard.txt')
        retained = pathlib.Path('assets/game/scenery', pack+'-LICENSE.txt').read_bytes()
        assert license_bytes == retained, pack+' license differs'
        assert b'CC0 1.0 Universal' in license_bytes
        selected = []
        for record in records:
            if record['pack'] != pack:
                continue
            source = archive.read(record['sourceFile'])
            assert sha(source) == record['sourceSha256'], record['sourceFile']+' source differs'
            document = json.loads(source)
            dependencies = []
            for item in document.get('buffers', [])+document.get('images', []):
                uri = item.get('uri', '')
                if not uri or uri.startswith('data:'):
                    continue
                assert not urllib.parse.urlparse(uri).scheme, 'Unexpected remote dependency'
                file = posixpath.normpath(posixpath.join(posixpath.dirname(record['sourceFile']), urllib.parse.unquote(uri)))
                data = archive.read(file)
                dependencies.append(dict(file=file, bytes=len(data), sha256=sha(data)))
            selected.append(dict(id=record['id'], file=record['sourceFile'], sha256=sha(source), dependencies=dependencies))
        archives[pack] = dict(archiveFilename='Downtown City MegaKit[Standard].zip' if args.city == path else 'Stylized Nature MegaKit[Standard].zip', archiveSha256=sha(path.read_bytes()), archiveBytes=path.stat().st_size, licenseFile='License_Standard.txt', licenseSha256=sha(license_bytes), licenseMatchesRetained=True, selected=selected)
result = dict(verifiedOn=str(datetime.date.today()), method='Official creator itch.io free Standard downloads; exact glTF hashes, archive dependencies and included CC0 notices checked', archives=archives)
args.output.write_text(json.dumps(result, indent=2)+'\n')
print('Verified', sum(len(p['selected']) for p in archives.values()), 'source models and all referenced buffers/textures; wrote', args.output)
