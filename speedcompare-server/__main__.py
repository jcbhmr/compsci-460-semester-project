import argparse
from . import tcp, udp

parser = argparse.ArgumentParser(description='SpeedCompare server')
subparser = parser.add_subparsers()

parser_tcp = subparser.add_parser('tcp')
parser_tcp.add_argument('--bind', type=str, help='Hostname & port to bind to', default='localhost:8000')
parser_tcp.set_defaults(func=tcp.func)

parser_udp = subparser.add_parser('udp')
parser_udp.add_argument('--bind', type=str, help='Hostname & port to bind to', default='localhost:8001')
parser_udp.set_defaults(func=udp.func)

args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.print_help()
    exit(1)
