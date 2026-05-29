import argparse
from nooforge.registry import read_registry

try:
    from rich.table import Table
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

def cmd_list(args: argparse.Namespace) -> int:
    data = read_registry()
    skills = data.get("skills", {})
    if HAS_RICH:
        table = Table(title="Skills registradas")
        table.add_column("Slug", style="cyan")
        table.add_column("Nome", style="green")
        table.add_column("Plataforma", style="magenta")
        table.add_column("Destino", style="white")
        for slug, info in skills.items():
            table.add_row(slug, str(info.get("name", "?")), str(info.get("platform", "?")), str(info.get("dest", "?")))
        console.print(table)
    else:
        for slug, info in skills.items():
            print(f"{slug} | {info.get('name', '?')} | {info.get('platform', '?')} | {info.get('dest', '?')}")
    return 0
