import argparse
from . import tcp, udp, http11

parser = argparse.ArgumentParser(description="SpeedCompare server")
subparser = parser.add_subparsers()

parser_tcp = subparser.add_parser("tcp")
parser_tcp.add_argument(
    "--bind", type=str, help="Hostname & port to bind to", default="0.0.0.0:8000"
)
parser_tcp.add_argument(
    "--size", type=int, help="Total number of bytes to send", default=10_000_000
)
parser_tcp.set_defaults(func=tcp.func)

parser_udp = subparser.add_parser("udp")
parser_udp.add_argument(
    "--bind", type=str, help="Hostname & port to bind to", default="0.0.0.0:8001"
)
parser_udp.add_argument(
    "--size", type=int, help="Total number of bytes to send", default=10_000_000
)
parser_udp.add_argument(
    "--loop-delay",
    type=int,
    help="milliseconds to wait between each 4096 chunk send",
    default=0,
)
parser_udp.set_defaults(func=udp.func)

parser_http11 = subparser.add_parser("http11")
parser_http11.add_argument(
    "--bind", type=str, help="Hostname & port to bind to", default="0.0.0.0:8002"
)
parser_http11.add_argument(
    "--size", type=int, help="Total number of bytes to send", default=10_000_000
)
parser_http11.set_defaults(func=http11.func)

args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
    exit(1)
