from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if not self.path.startswith('/__capture/'):
            self.send_error(404); return
        name=self.path.rsplit('/',1)[-1]
        if name not in {'site-on.png','scale-on.png','compare-on.png','overhead-on.png','rider-on.png','rear-on.png'}:
            self.send_error(400); return
        length=int(self.headers.get('Content-Length','0'))
        if length<1 or length>5000000:
            self.send_error(400); return
        data=self.rfile.read(length)
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            self.send_error(400); return
        (Path('validation/dragon-mount-d1b')/name).write_bytes(data)
        self.send_response(200); self.end_headers(); self.wfile.write(b'saved')

ThreadingHTTPServer(('127.0.0.1',4177),Handler).serve_forever()
