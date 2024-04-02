import argparse
import socket
import threading
import time

def send_data(socket_, data):
    try:
        socket_.sendall(data)
        return True
    except Exception as e:
        print("Error sending data:", e)
        return False

def receive_data(socket_, expected_size):
    try:
        received_data = socket_.recv(expected_size)
        return received_data
    except Exception as e:
        print("Error receiving data:", e)
        return None

def client_worker(host, port, mode, bytes_per_socket, similarity_threshold):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if mode == 'tcp' else socket.SOCK_DGRAM)
        client_socket.connect((host, port))

        data_sent = b'a' * bytes_per_socket
        if send_data(client_socket, data_sent):
            data_received = receive_data(client_socket, bytes_per_socket)
            if data_received is not None:
                similarity = similar(data_sent, data_received)
                print("Data similarity:", similarity)
        client_socket.close()
    except Exception as e:
        print("Error occurred:", e)

def similar(a, b):
    return sum(a[i] == b[i] for i in range(len(a))) / len(a)

def main():
    parser = argparse.ArgumentParser(description='Speed Compare Client')
    parser.add_argument('--host', type=str, help='Server address and port', default='localhost:8000')
    parser.add_argument('--mode', type=str, help='Mode: tcp or udp', default='tcp', choices=['tcp', 'udp'])
    parser.add_argument('--socket-count', type=int, help='Number of sockets to open', default=1)
    parser.add_argument('--bytes-per-socket', type=int, help='Number of bytes to send per socket', default=1000)
    args = parser.parse_args()

    for i in range(args.socket_count):
        client_thread = threading.Thread(target=client_worker, args=(args.host.split(':')[0], int(args.host.split(':')[1]), args.mode, args.bytes_per_socket, 0.9))
        client_thread.start()

if __name__ == "__main__":
    main()
