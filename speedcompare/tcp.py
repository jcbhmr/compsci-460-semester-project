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

    def client_thread(socket_id, host, port, data, response_data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(data)
            response = client_socket.recv(len(data))
            response_data[socket_id] = response

    data = bytearray(random.getrandbits(8) for _ in range(size))
    expected_response = data

    sockets = []
    response_data = [None] * sockets

    start_time = time.time()

    for i in range(sockets):
        socket_id = i
        thread = threading.Thread(target=client_thread, args=(socket_id, hostname, port, data, response_data))
        sockets.append(thread)
        thread.start()

    for socket in sockets:
        socket.join()

    end_time = time.time()
    total_time = end_time - start_time

    # https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
    total_accuracy = 0
    for response in response_data:
        accuracy = SequenceMatcher(None, response, expected_response).ratio()
        total_accuracy += accuracy

    avg_accuracy = total_accuracy / sockets

    print(f"Test results:")
    print(f"Number of sockets: {sockets}")
    print(f"Number of bytes sent per socket: {size}")
    print(f"Total time taken: {total_time} seconds")
    print(f"Average accuracy: {avg_accuracy * 100:.2f}%")

    print(f"[bold][green]Time:[/green][/bold] {total_time:.2f} seconds")
    print(f"[bold][green]Size:[/green][/bold] {pretty_bytes(size)} or {pretty_bits(size * 8)}")
    print(f"[bold][green]Speed:[/green][/bold] {pretty_bytes(size / total_time)}/s or {pretty_bits((size / total_time) * 8)}/s")

