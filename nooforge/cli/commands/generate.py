import sys
from pathlib import Path
import argparse

from nooforge.core.utils import read_text, write_text
from nooforge.core.extract import extract_skill_info
from nooforge.core.lint import lint_skill
from nooforge.handlers import get_handler, list_handlers
from nooforge.registry import read_registry
from nooforge.cli.interactive import pick_platform_interactive, show_issues, get_input_text
from nooforge.cli.utils import install_skill, find_render_target

def do_generate(args: argparse.Namespace) -> int:
    text = get_input_text(args)
    if not text.strip():
        return 1
    name, desc, body = extract_skill_info(text)
    platform = args.platform
    if platform is None:
        if sys.stdin.isatty():
            platform = pick_platform_interactive()
        else:
            platform = "universal"
    if platform not in list_handlers():
        print(f"Plataforma inválida: {platform}")
        return 1
    registry = read_registry()
    content, dest, instr, slug = find_render_target(platform, name, desc, body, args, registry)
    issues = lint_skill(content, platform)
    if issues:
        show_issues(issues)
    if args.dry_run:
        print(content)
        return 0
    if args.output:
        out = Path(args.output)
        write_text(out, content)
        print(str(out))
        return 0
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.prompt import Confirm
        from rich.syntax import Syntax
        console = Console()
        syntax_lang = "json" if dest.suffix == ".json" else "yaml" if dest.suffix in {".yaml", ".yml"} else "markdown"
        console.print(Panel(Syntax(content, syntax_lang, theme="monokai"), title="Conteúdo gerado"))
        console.print(f"[blue]{instr}[/blue]")
        install_now = args.install or Confirm.ask("Instalar automaticamente?", default=False)
    except ImportError:
        print(content)
        print(instr)
        install_now = args.install
    if install_now:
        ok = install_skill(content, dest, platform, name, slug, force=args.force)
        return 0 if ok else 1
    return 0
