import argparse
from pathlib import Path
from nooforge.registry import read_registry
from nooforge.core.utils import slugify, read_text

try:
    from rich.table import Table
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

def cmd_info(args: argparse.Namespace) -> int:
    data = read_registry()
    skills = data.get("skills", {})
    slug = slugify(args.name)
    entry = skills.get(slug)
    if not entry and args.name in skills:
        entry = skills[args.name]
        slug = args.name
    if not entry:
        print("Skill não encontrada.")
        return 1
    dest = Path(entry.get("dest", ""))
    content = read_text(dest) if dest.exists() else ""
    if HAS_RICH:
        table = Table(title=f"Info da skill: {slug}")
        table.add_column("Campo", style="cyan")
        table.add_column("Valor", style="green")
        table.add_row("Slug", slug)
        table.add_row("Nome", str(entry.get("name", "")))
        table.add_row("Plataforma", str(entry.get("platform", "")))
        table.add_row("Destino", str(entry.get("dest", "")))
        table.add_row("Conteúdo existe", "sim" if dest.exists() else "não")
        console.print(table)
        if content:
            console.print(Panel(Syntax(content, "markdown", theme="monokai"), title="Conteúdo"))
    else:
        print(f"Slug: {slug}")
        print(f"Nome: {entry.get('name', '')}")
        print(f"Plataforma: {entry.get('platform', '')}")
        print(f"Destino: {entry.get('dest', '')}")
        print(f"Conteúdo existe: {'sim' if dest.exists() else 'não'}")
        if content:
            print("\n--- CONTEÚDO ---\n")
            print(content)
    return 0
