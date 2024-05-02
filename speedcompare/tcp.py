import socket
from rich import print
from .utils import pretty_bits, pretty_bytes
import time
import threading


def func(args):
    host = args.host
    hostname = host.split(":")[0]
    port = int(host.split(":")[1])
    sockets = args.sockets

    print(f"TCP {host} with {sockets} sockets")

    worker_sizes = [0] * sockets

    def worker(i: int):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))
        contents = b""
        while True:
            data = client_socket.recv(60000)
            if not data:
                break
            contents += data
        client_socket.close()
        worker_sizes[i] = len(contents)

    start_time = time.time()

    threads = []
    for i in range(sockets):
        thread = threading.Thread(target=worker, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()

    total_size = sum(worker_sizes)
    total_time = end_time - start_time
    speed = total_size / total_time
    print("Summary:")
    print(f"Total size: {pretty_bytes(total_size)} bytes")
    print(f"Total time: {total_time} seconds")
    print(f"Speed: {pretty_bits(speed * 8)}ps")
