import argparse
import socket
import threading
import time
from .pretty_bytes import pretty_bytes, pretty_bits
from rich import print

def func(args):
    host: str = args.host
    hostname = host.split(':')[0]
    port = int(host.split(':')[1])
    sockets: int = args.sockets
    size: int = args.size

    print(f"[bold][blue]Host:[/blue][/bold] {host}")
    print(f"[bold][blue]Sockets:[/blue][/bold] {sockets}")
    print(f"[bold][blue]Size:[/blue][/bold] {pretty_bytes(size)} or {pretty_bits(size * 8)}")

    # Send only MY PART of the data and let other threads fill in the rest.
    # Use 1000 byte chunks to avoid errno 90 message too long
    def send_data(sock: socket.socket, i: int):
        my_nbytes = size // sockets
        print(f"Socket {i} sending {pretty_bytes(my_nbytes)}")
        for _ in range(my_nbytes // 1000):
            sock.sendto(b"x" * 1000, (hostname, port))
        sock.sendto(b"x" * (my_nbytes % 1000), (hostname, port))

    start = time.time()
    threads = []
    socket_list = []
    for i in range(sockets):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        thread = threading.Thread(target=send_data, args=(sock, i))
        thread.start()
        threads.append(thread)
        socket_list.append(sock)
    for thread in threads:
        thread.join()
    for sock in socket_list:
        sock.close()
    end = time.time()

    speed_bytes = size / (end - start)

    print(f"[bold][green]Time:[/green][/bold] {end - start:.2f} seconds")
    print(f"[bold][green]Size:[/green][/bold] {pretty_bytes(size)} or {pretty_bits(size * 8)}")
    print(f"[bold][green]Speed:[/green][/bold] {pretty_bytes(speed_bytes)}/s or {pretty_bits(speed_bytes * 8)}/s")
