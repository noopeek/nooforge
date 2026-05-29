import argparse
from nooforge.server import serve

def cmd_serve(args: argparse.Namespace) -> int:
    serve(args.port)
    return 0
