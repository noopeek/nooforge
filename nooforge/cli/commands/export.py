import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

from nooforge.core.utils import slugify, read_text, write_text
from nooforge.registry import read_registry

def export_skill_entry(slug: str, info: dict) -> dict:
    dest = Path(info.get("dest", ""))
    content = read_text(dest) if dest.exists() else ""
    return {
        "slug": slug,
        "name": info.get("name", slug),
        "platform": info.get("platform", ""),
        "dest": info.get("dest", ""),
        "content": content,
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }

def cmd_export(args: argparse.Namespace) -> int:
    data = read_registry()
    skills = data.get("skills", {})
    if args.name:
        slug = slugify(args.name)
        if slug not in skills:
            print("Skill não encontrada.")
            return 1
        payload = {"version": 1, "skills": [export_skill_entry(slug, skills[slug])]}
    else:
        payload = {"version": 1, "skills": [export_skill_entry(slug, info) for slug, info in skills.items()]}
    out = Path(args.output or f"{args.name or 'nooforge'}.nooforge")
    write_text(out, json.dumps(payload, indent=2, ensure_ascii=False))
    print(str(out))
    return 0
