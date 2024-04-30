import socket
import threading
import argparse
import time

def func(args):
    host = args.bind
    hostname = host.split(":")[0]
    port = int(host.split(":")[1])
    size = args.size
    loop_delay = args.loop_delay

    def handle_client(data, client_address):
        n = 0
        while n < size:
            server_socket.sendto(b"X" * 4096, client_address)
            n += 4096
            if loop_delay:
                time.sleep(loop_delay * 0.001)
        print(f"sent all {n} bytes to {client_address}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((hostname, port))

    print(f"[*] Listening on {hostname}:{port}")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"[*] Received connection from {client_address}")
        
        client_handler = threading.Thread(target=handle_client, args=(data, client_address))
        client_handler.start()