import socket
import threading

def func(args):
    host = args.bind
    hostname = host.split(":")[0]
    port = int(host.split(":")[1])
    size = args.size

    def handle_client(client_socket):
        client_socket.send(b"X" * size)
        client_socket.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)

    print(f"[*] Listening on {hostname}:{port}")

    while True:
        client, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()