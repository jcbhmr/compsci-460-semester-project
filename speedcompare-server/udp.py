from socketserver import ThreadingUDPServer, DatagramRequestHandler

class MyUDPHandler(DatagramRequestHandler):
    def handle(self):
        pass

def func(args):
    host: str = args.bind
    hostname = host.split(':')[0]
    port = int(host.split(':')[1])

    print(f"Listening on {host}")
    with ThreadingUDPServer((hostname, port), MyUDPHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("interrupted")