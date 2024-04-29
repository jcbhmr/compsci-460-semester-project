from socketserver import ThreadingTCPServer, StreamRequestHandler

class MyTCPHandler(StreamRequestHandler):
    def handle(self):
        print(f"Connection from {self.client_address}")
        while True:
            data = self.rfile.read(1024)
            if not data:
                break
            self.wfile.write(data)

def func(args):
    host: str = args.bind
    hostname = host.split(':')[0]
    port = int(host.split(':')[1])

    print(f"Listening on {host}")
    with ThreadingTCPServer((hostname, port), MyTCPHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("interrupted")
