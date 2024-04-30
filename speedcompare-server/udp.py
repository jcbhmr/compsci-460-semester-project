import socketserver
from rich import print

def func(args):
    host: str = args.bind
    hostname = host.split(':')[0]
    port = int(host.split(':')[1])

    print(f"UDP listening on {host}")
    