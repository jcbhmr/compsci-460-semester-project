import argparse
import socket
import threading
import time
from .pretty_bytes import pretty_bytes
from rich import print

def func(args):
    host: str = args.host
    hostname = host.split(':')[0]
    port = int(host.split(':')[1])
    sockets: int = args.sockets
    size: int = args.size
    timeout: int = args.timeout