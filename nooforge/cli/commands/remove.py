import argparse
from nooforge.registry import remove_skill

def cmd_remove(args: argparse.Namespace) -> int:
    ok = remove_skill(args.name, force=args.force)
    print("Removido." if ok else "Skill não encontrada.")
    return 0 if ok else 1
