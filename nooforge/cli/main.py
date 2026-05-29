import argparse
import sys
import logging
from pathlib import Path

from nooforge.cli.commands import (
    do_generate, cmd_list, cmd_info, cmd_lint, cmd_remove,
    cmd_export, cmd_import, cmd_serve, cmd_paths
)
from nooforge.cli.interactive import interactive_fallback
from nooforge.core.constants import DEFAULT_PORT
from nooforge.handlers import list_handlers

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nooforge")
    parser.add_argument("--log-level", default="INFO")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", aliases=["gen"])
    gen.add_argument("-p", "--platform", choices=list_handlers())
    gen.add_argument("-i", "--input", type=Path)
    gen.add_argument("-t", "--text")
    gen.add_argument("--output", type=Path)
    gen.add_argument("--install", action="store_true")
    gen.add_argument("--force", action="store_true")
    gen.add_argument("--dry-run", action="store_true")
    gen.add_argument("--ollama-model")
    gen.add_argument("--stdin", action="store_true")
    gen.set_defaults(func=do_generate)

    sub.add_parser("list").set_defaults(func=cmd_list)
    info = sub.add_parser("info")
    info.add_argument("name")
    info.set_defaults(func=cmd_info)

    lint = sub.add_parser("lint")
    lint.add_argument("file", type=Path)
    lint.add_argument("-p", "--platform", choices=list_handlers(), default="universal")
    lint.set_defaults(func=cmd_lint)

    rm = sub.add_parser("remove")
    rm.add_argument("name")
    rm.add_argument("--force", action="store_true")
    rm.set_defaults(func=cmd_remove)

    exp = sub.add_parser("export")
    exp.add_argument("name", nargs="?")
    exp.add_argument("-o", "--output", type=Path)
    exp.set_defaults(func=cmd_export)

    imp = sub.add_parser("import")
    imp.add_argument("file", type=Path)
    imp.add_argument("--force", action="store_true")
    imp.set_defaults(func=cmd_import)

    srv = sub.add_parser("serve")
    srv.add_argument("--port", type=int, default=DEFAULT_PORT)
    srv.set_defaults(func=cmd_serve)

    sub.add_parser("paths").set_defaults(func=cmd_paths)

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    level = getattr(args, "log_level", "INFO")
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(levelname)s %(message)s")
    if hasattr(args, "func"):
        sys.exit(args.func(args))
    sys.exit(interactive_fallback())
