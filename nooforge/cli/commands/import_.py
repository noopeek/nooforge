import json
import argparse
from pathlib import Path

from nooforge.core.utils import slugify, read_text, unique_slug
from nooforge.core.extract import extract_skill_info
from nooforge.registry import read_registry
from nooforge.handlers import list_handlers
from nooforge.cli.utils import install_skill, find_render_target

def cmd_import(args: argparse.Namespace) -> int:
    try:
        payload = json.loads(read_text(Path(args.file)))
    except Exception:
        print("Arquivo inválido ou não encontrado.")
        return 1
    skills = payload.get("skills", [])
    if not isinstance(skills, list):
        print("Arquivo inválido.")
        return 1
    for item in skills:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", item.get("slug", "skill")))
        platform = str(item.get("platform", "universal"))
        content = str(item.get("content", ""))
        if platform not in list_handlers():
            platform = "universal"
        registry = read_registry()
        imported_name, imported_desc, imported_body = extract_skill_info(content)
        slug = slugify(imported_name) if args.force else unique_slug(imported_name, registry)
        _, dest, _, _ = find_render_target(platform, imported_name, imported_desc, imported_body, args, registry)
        ok = install_skill(content, dest, platform, imported_name, slug, force=args.force)
        if not ok:
            return 1
    print("Importação concluída.")
    return 0
