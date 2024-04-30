from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

def func(args):
    host = args.bind
    hostname = host.split(":")[0]
    port = int(host.split(":")[1])
    size = args.size

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"X" * size)

    class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
        pass

    server = ThreadingSimpleServer((hostname, port), Handler)
    server.serve_forever()