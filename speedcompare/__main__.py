import argparse
from . import tcp, udp, http11

parser = argparse.ArgumentParser(description="SpeedCompare client")
subparser = parser.add_subparsers()

parser_tcp = subparser.add_parser("tcp")
parser_tcp.add_argument(
    "--host", type=str, help="Hostname & port to connect to", default="localhost:8000"
)
parser_tcp.add_argument(
    "--sockets", type=int, help="Number of sockets to use", default=1
)
parser_tcp.set_defaults(func=tcp.func)

parser_udp = subparser.add_parser("udp")
parser_udp.add_argument(
    "--host", type=str, help="Hostname & port to connect to", default="localhost:8001"
)
parser_udp.add_argument(
    "--sockets", type=int, help="Number of sockets to use", default=1
)
parser_udp.add_argument(
    "--expected-size",
    type=int,
    help="Expected size of the response",
    default=10_000_000,
)
parser_udp.set_defaults(func=udp.func)

parser_http11 = subparser.add_parser("http11")
parser_http11.add_argument(
    "--host", type=str, help="Hostname & port to connect to", default="localhost:8002"
)
parser_http11.add_argument(
    "--sockets", type=int, help="Number of sockets to use", default=1
)
parser_http11.add_argument(
    "--no-compression", type=bool, help="Disable HTTP compression", default=False
)
parser_http11.set_defaults(func=http11.func)

args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
    exit(1)
