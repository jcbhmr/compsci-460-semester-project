import argparse
import socket
import sys
import threading

def handle_client(client_socket):
    print("Connection from:", client_socket.getpeername())
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            client_socket.sendall(data)
    except Exception as e:
        print("Error occurred:", e)
    finally:
        print("Connection closed:", client_socket.getpeername())
        client_socket.close()

def start_server(bind_address, port, mode):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if mode == 'tcp' else socket.SOCK_DGRAM)
        server_socket.bind((bind_address, port))
        server_socket.listen(5)
        print("Server started on", bind_address, "port", port, "mode", mode)
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server stopped.")
    except Exception as e:
        print("Error occurred:", e)
    finally:
        server_socket.close()

def main():
    parser = argparse.ArgumentParser(description='Speed Compare Server')
    parser.add_argument('--port', type=int, help='Port to bind to', default=8000)
    parser.add_argument('--bind', type=str, help='Address to bind to', default='localhost')
    parser.add_argument('--mode', type=str, help='Mode: tcp or udp', default='tcp', choices=['tcp', 'udp'])
    args = parser.parse_args()

    start_server(args.bind, args.port, args.mode)

if __name__ == "__main__":
    main()
