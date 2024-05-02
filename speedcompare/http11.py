import socket
import urllib.request
from rich import print
from .utils import pretty_bits, pretty_bytes
import time
import threading

def func(args):
    host = args.host
    hostname = host.split(":")[0]
    port = int(host.split(":")[1])
    sockets = args.sockets
    no_compression = args.no_compression

    print(f"HTTP 1.1 GET {host} with {sockets} sockets")

    worker_sizes = [0] * sockets

    def worker(i: int):
        url = f"http://{hostname}:{port}/"
        req = urllib.request.Request(url)
        if no_compression:
            req.remove_header("Accept-Encoding")
            req.add_header("Accept-Encoding", "identity")
        contents = urllib.request.urlopen(req).read()
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
    print(f"Total size: {pretty_bytes(total_size)} bytes")
    print(f"Total time: {total_time} seconds")
    print(f"Speed: {pretty_bits(speed * 8)}ps")
