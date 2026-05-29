import argparse
from pathlib import Path
from nooforge.core.utils import read_text
from nooforge.core.lint import lint_skill
from nooforge.cli.interactive import show_issues

def cmd_lint(args: argparse.Namespace) -> int:
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Arquivo não encontrado: {file_path}")
        return 1
    content = read_text(file_path)
    issues = lint_skill(content, args.platform)
    if issues:
        show_issues(issues)
        return 1
    print("Nenhum problema encontrado.")
    return 0
