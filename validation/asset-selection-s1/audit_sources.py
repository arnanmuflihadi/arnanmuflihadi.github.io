"""Bounded audit of supplied discovery URLs. Does not download model archives."""
import concurrent.futures, datetime, hashlib, json, re, urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.text=[]; self.links=[]; self.images=[]; self.hidden=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('script','style'): self.hidden+=1
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='img' and a.get('src'): self.images.append(a['src'])
        if tag=='meta' and a.get('property')=='og:image': self.images.insert(0,a.get('content',''))
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
    def handle_data(self, data):
        if not self.hidden: self.text.append(data.strip())
def fetch(url):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AR(N)AN asset license audit; Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=22) as r: raw=r.read(4000000); status=r.status; final=r.url
        html=raw.decode('utf-8','replace'); p=Page();p.feed(html)
        text=' '.join(t for t in p.text if t)
        key=hashlib.sha256(url.encode()).hexdigest()[:12]
        (ROOT/'pages'/f'{key}.txt').write_text(text)
        return {'url':url,'final_url':final,'status':status,'title':re.findall(r'<title[^>]*>(.*?)</title>',html,re.S)[:1],'page_text':f'pages/{key}.txt','links':[urljoin(final,l) for l in p.links], 'images':list(dict.fromkeys(urljoin(final,i) for i in p.images))[:14]}
    except Exception as e: return {'url':url,'status':'blocked-or-unavailable','error':str(e)}
if __name__=='__main__':
    rows=[dict(zip(['id','category','title','url'],l.split('\t'))) for l in (ROOT/'sources.tsv').read_text().splitlines()]
    (ROOT/'pages').mkdir(exist_ok=True)
    urls=list(dict.fromkeys(r['url'] for r in rows))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: pages=list(pool.map(fetch,urls))
    (ROOT/'source-audit.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows,'pages':pages},indent=2))
    print(json.dumps({'supplied_entries':len(rows),'unique_pages':len(pages),'accessible':sum(p['status']==200 for p in pages),'blocked':sum(p['status']!=200 for p in pages)}))
