import socketserver
import socket
from rich import print

def func(args):
    host: str = args.bind
    hostname = host.split(':')[0]
    port = int(host.split(':')[1])

    print(f"TCP listening on {host}")

    class MyTCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            print("Connection from:", self.client_address)
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                print("Received:", data.decode().strip())
                self.request.sendall(data)

    with socketserver.TCPServer((host, port), MyTCPHandler) as server:
        # interrupt the program with Ctrl-C
        server.serve_forever()