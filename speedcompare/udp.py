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
    expected_size = args.expected_size

    print(f"UDP {host} x{sockets} sockets")

    each_size = [0] * sockets

    def do_thing(i: int):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(b"hi", (hostname, port))

        contents = b""
        while True:
            if len(contents) < (expected_size * 0.8):
                client_socket.settimeout(1)
            else:
                client_socket.settimeout(0.3)
            try:
                data, _ = client_socket.recvfrom(60000)
                if not data:
                    break
                contents += data
            except socket.timeout:
                break
        client_socket.close()

        each_size[i] = len(contents)

    start_time = time.time()

    threads = []
    for i in range(sockets):
        thread = threading.Thread(target=do_thing, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()

    total_size = sum(each_size)
    total_time = end_time - start_time
    speed = total_size / total_time
    print("For UDP:")
    print(f"Total size: {pretty_bytes(total_size)}")
    print(f"Total time: {total_time} seconds")
    print(f"Speed: {pretty_bits(speed * 8)}ps")

    percent = (total_size / (expected_size * sockets)) * 100

    print(f"The original expected size was {pretty_bytes(expected_size)} PER SOCKET")
    print(f"Which is {pretty_bytes(expected_size * sockets)} total")
    print(f"The actual size was {pretty_bytes(total_size)} bytes")
    print(f"That means we got {percent:.2f}% of the expected size")
    if percent < 50:
        print("UH OH: The actual size was less than 50% of the expected size")


