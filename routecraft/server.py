import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from solver import solve
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!='/':self.send_error(404);return
        body=Path(__file__).with_name('index.html').read_bytes()
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(body)
    def do_POST(self):
        if self.path!='/solve':self.send_error(404);return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=20000:raise ValueError('Body must be 1 to 20000 bytes')
            payload=json.loads(self.rfile.read(size));result=solve(payload['points'])
            status=200
        except (ValueError,TypeError,KeyError,OverflowError) as error:
            result={'error':str(error) or 'Invalid input'};status=400
        body=json.dumps(result).encode()
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':
    print('RouteCraft demo: http://127.0.0.1:8000')
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
