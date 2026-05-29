from __future__ import annotations

import sys
import argparse
from pathlib import Path
from typing import List

from nooforge.core.utils import read_text, slugify
from nooforge.core.extract import extract_skill_info
from nooforge.core.lint import lint_skill
from nooforge.registry import read_registry
from nooforge.handlers import list_handlers, get_handler
from nooforge.cli.utils import install_skill, find_render_target

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

def get_input_text(args: argparse.Namespace) -> str:
    if getattr(args, "input", None):
        return read_text(Path(args.input))
    if getattr(args, "text", None):
        return args.text
    if getattr(args, "stdin", False) or not sys.stdin.isatty():
        data = sys.stdin.read()
        if data.strip():
            return data
    if HAS_RICH:
        return Prompt.ask("Cole o texto da skill", multiline=True)
    print("Cole o texto da skill. Finalize com uma linha contendo apenas FIM ou use Ctrl+D/Ctrl+Z+Enter:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "FIM":
            break
        lines.append(line)
    return "\n".join(lines)

def show_issues(issues: List) -> None:
    for issue in issues:
        if HAS_RICH:
            color = "red" if issue.severity == "error" else "yellow"
            console.print(f"[{color}]{issue.severity.upper()}: {issue.message}[/{color}]")
        else:
            print(f"{issue.severity.upper()}: {issue.message}")

def pick_platform_interactive() -> str:
    items = list_handlers()
    if HAS_RICH:
        table = Table(title="Plataformas")
        table.add_column("#", style="cyan")
        table.add_column("Plataforma", style="green")
        for i, p in enumerate(items, 1):
            table.add_row(str(i), p)
        console.print(table)
        choice = Prompt.ask("Escolha", choices=[str(i) for i in range(1, len(items) + 1)])
        return items[int(choice) - 1]
    for i, p in enumerate(items, 1):
        print(f"{i}. {p}")
    choice = input("Escolha: ").strip()
    return items[int(choice) - 1]

def get_installed_count() -> int:
    data = read_registry()
    return len(data.get("skills", {}))

def show_header() -> None:
    if not HAS_RICH:
        print("NooForge - Forje skills para IA")
        return
    logo = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  @@@ @@@ @@@@@@ @@@@@@ @@@@@@@@ @@@@@@ @@@@@@@ @@@@@@@@ @@@@@@@@            ║
║  @@@@ @@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@@@ @@@@@@@@  ║
║  @@!@!@@@ @@!  @@@ @@!  @@@ @@!      @@!  @@@ @@!  @@@ !@@       @@!       ║
║  !@!!@!@! !@!  @!@ !@!  @!@ !@!      !@!  @!@ !@!  @!@ !@!       !@!       ║
║  @!@ !!@! @!@ !@!  @!@ !@!  @!!!:!   @!@!!@!  !@! !@!  !@! @!@!@ @!!!:!   ║
║  !@!  !!! !@! !!!  !@! !!!  !!!!!:   !!@!@!   !!! !!@!  !!! !!@!! !!!!!:   ║
║  !!:  !!! !!:  !!! !!:  !!! !!:      !!: :!!   !!: :!!   :!!  !!:  !!:      ║
║  :!:  !:! :!:  !:! :!:  !:! :!:      :!:  !:!  :!:  !:!  :!: !::  :!:      ║
║   ::  ::  ::::: ::  ::::: ::  ::      ::   :::   ::  :::  :::: ::   ::       ║
║   :   :    : :  :    : :  :   :        :   : :   :    ::  :: ::  :   ::      ║
║                                                                              ║
║  ╔═══════════════════════════════════════════════════════════════════════╗   ║
║  ║            🔥 FORJE SKILLS PARA IA 🔥                                ║   ║
║  ╚═══════════════════════════════════════════════════════════════════════╝   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    console.print(Panel(logo, style="bold cyan", border_style="cyan"))
    count = get_installed_count()
    console.print(f"[dim]📦 Skills forjadas: {count}[/dim]\n")

def show_menu() -> str:
    if HAS_RICH:
        console.print("[bold yellow]⚡ Menu principal[/bold yellow]")
        table = Table(show_header=False, box=None)
        table.add_column("Opção", style="cyan", no_wrap=True)
        table.add_column("Ação", style="green")
        items = [
            ("1", "✨ Forjar nova skill"),
            ("2", "📋 Listar skills forjadas"),
            ("3", "ℹ️  Ver detalhes de uma skill"),
            ("4", "🗑️  Remover skill"),
            ("5", "💾 Exportar skill(s)"),
            ("6", "📥 Importar skill(s)"),
            ("7", "🌐 Iniciar servidor MCP"),
            ("8", "🚪 Sair"),
        ]
        for num, desc in items:
            table.add_row(num, desc)
        console.print(table)
        return Prompt.ask("Escolha", choices=[str(i) for i in range(1, 9)], default="1")
    else:
        print("\nMenu principal:")
        print("1 - Forjar nova skill")
        print("2 - Listar skills forjadas")
        print("3 - Ver detalhes de uma skill")
        print("4 - Remover skill")
        print("5 - Exportar skill(s)")
        print("6 - Importar skill(s)")
        print("7 - Iniciar servidor MCP")
        print("8 - Sair")
        return input("Escolha: ").strip()

def interactive_generate():
    text = get_input_text(argparse.Namespace(input=None, text=None, stdin=False))
    if not text.strip():
        if HAS_RICH:
            console.print("[red]Nenhum texto fornecido.[/red]")
        else:
            print("Nenhum texto.")
        return
    name, desc, body = extract_skill_info(text)
    platform = pick_platform_interactive()
    registry = read_registry()
    args = argparse.Namespace(ollama_model=None, force=False)
    content, dest, instr, slug = find_render_target(platform, name, desc, body, args, registry)
    issues = lint_skill(content, platform)
    if issues:
        show_issues(issues)
        if HAS_RICH and not Confirm.ask("A skill tem avisos/erros. Continuar mesmo assim?", default=False):
            return
    if HAS_RICH:
        syntax_lang = "json" if dest.suffix == ".json" else "yaml" if dest.suffix in {".yaml", ".yml"} else "markdown"
        console.print(Panel(Syntax(content, syntax_lang, theme="monokai"), title="Conteúdo gerado"))
        console.print(f"[blue]{instr}[/blue]")
        if Confirm.ask("Instalar automaticamente?", default=False):
            ok = install_skill(content, dest, platform, name, slug, force=False)
            console.print("[green]✅ Instalado com sucesso[/green]" if ok else "[red]❌ Falha na instalação[/red]")
        else:
            if Confirm.ask("Salvar em arquivo?", default=False):
                out_file = Prompt.ask("Nome do arquivo", default=f"{slug}.skill")
                from nooforge.core.utils import write_text
                write_text(Path(out_file), content)
                console.print(f"[green]✅ Salvo em {out_file}[/green]")
    else:
        print(content)
        print(instr)
        if input("Instalar? (s/N): ").lower() in ['s', 'sim']:
            install_skill(content, dest, platform, name, slug, force=False)

def interactive_list():
    from nooforge.cli.commands.list import cmd_list
    cmd_list(argparse.Namespace())
    if HAS_RICH:
        input("\nPressione Enter para continuar...")
    else:
        input()

def interactive_info():
    if HAS_RICH:
        name = Prompt.ask("Nome ou slug da skill")
    else:
        name = input("Nome ou slug: ")
    from nooforge.cli.commands.info import cmd_info
    cmd_info(argparse.Namespace(name=name))
    if HAS_RICH:
        input("\nPressione Enter para continuar...")
    else:
        input()

def interactive_remove():
    if HAS_RICH:
        name = Prompt.ask("Nome ou slug da skill a remover")
        if not Confirm.ask(f"Tem certeza que deseja remover '{name}'?", default=False):
            return
    else:
        name = input("Skill: ")
    from nooforge.cli.commands.remove import cmd_remove
    cmd_remove(argparse.Namespace(name=name, force=False))
    if HAS_RICH:
        input("\nPressione Enter para continuar...")
    else:
        input()

def interactive_export():
    if HAS_RICH:
        name = Prompt.ask("Nome ou slug da skill (deixe vazio para todas)", default="")
    else:
        name = input("Skill (vazio para todas): ")
    from nooforge.cli.commands.export import cmd_export
    if name.strip():
        args = argparse.Namespace(name=name.strip(), output=None)
    else:
        args = argparse.Namespace(name=None, output=None)
    cmd_export(args)
    if HAS_RICH:
        input("\nPressione Enter para continuar...")
    else:
        input()

def interactive_import():
    if HAS_RICH:
        file_path = Prompt.ask("Caminho do arquivo .nooforge")
    else:
        file_path = input("Arquivo: ")
    from nooforge.cli.commands.import_ import cmd_import
    cmd_import(argparse.Namespace(file=Path(file_path), force=False))
    if HAS_RICH:
        input("\nPressione Enter para continuar...")
    else:
        input()

def interactive_serve():
    from nooforge.cli.commands.serve import cmd_serve
    from nooforge.core.constants import DEFAULT_PORT
    port = DEFAULT_PORT
    if HAS_RICH:
        port = int(Prompt.ask("Porta", default=str(DEFAULT_PORT)))
    if HAS_RICH:
        console.print("[green]Iniciando servidor MCP. Pressione Ctrl+C para parar.[/green]")
    else:
        print("Iniciando servidor MCP...")
    cmd_serve(argparse.Namespace(port=port))

def interactive_fallback() -> int:
    if HAS_RICH:
        show_header()
    else:
        print("NooForge - Forje skills para IA\n")
    while True:
        choice = show_menu()
        if choice == "1":
            interactive_generate()
        elif choice == "2":
            interactive_list()
        elif choice == "3":
            interactive_info()
        elif choice == "4":
            interactive_remove()
        elif choice == "5":
            interactive_export()
        elif choice == "6":
            interactive_import()
        elif choice == "7":
            interactive_serve()
        elif choice == "8":
            if HAS_RICH:
                console.print("[bold cyan]Até logo! ⚡[/bold cyan]")
            else:
                print("Até logo!")
            return 0
