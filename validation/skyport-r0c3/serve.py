from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
class ReviewHandler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(Path(__file__).resolve().parents[2]),**kw)
 def end_headers(self):self.send_header('Cache-Control','no-store');super().end_headers()
 def log_message(self,*a):pass
print('Skyport review: http://127.0.0.1:4176 (local only, no stale module cache)',flush=True)
ThreadingHTTPServer(('127.0.0.1',4176),ReviewHandler).serve_forever()
