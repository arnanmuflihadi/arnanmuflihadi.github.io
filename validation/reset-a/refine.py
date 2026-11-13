from pathlib import Path
import json
exec(Path('validation/reset-a/study.py').read_text().split('A=[];B=[]')[0])
search=json.loads(Path('validation/reset-a/search.json').read_text());out={}
for name in ['A','B']:
 best=search[name][0];setup(best['template']);rows=[]
 for x in range(best['centre'][0]-2,best['centre'][0]+3):
  for z in range(best['centre'][1]-2,best['centre'][1]+3):
   if name=='A'and math.hypot(x-36,z-27)>12:continue
   if name=='B'and math.hypot(x-36,z-27)<22:continue
   for angle in range(best['angle']-10,best['angle']+11,5):
    r=evaluate([x,z],angle)
    if r:r['template']=best['template'];rows.append(r)
 rows.sort(key=lambda r:r['score']);out[name]=rows[0]
Path('validation/reset-a/selected.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
