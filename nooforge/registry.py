import contextlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nooforge.core.constants import REGISTRY_FILE, MCP_SCRIPTS_DIR
from nooforge.core.utils import read_json, write_json, slugify

def read_registry() -> dict:
    return read_json(REGISTRY_FILE, {"skills": {}})

def write_registry(data: dict) -> None:
    write_json(REGISTRY_FILE, data)

def register_skill(name: str, platform: str, dest: Path, slug: str) -> None:
    data = read_registry()
    data.setdefault("skills", {})
    data["skills"][slug] = {
        "name": name,
        "platform": platform,
        "dest": str(dest),
        "installed_at": datetime.now(timezone.utc).isoformat(),
    }
    write_registry(data)

def remove_skill(slug_or_name: str, force: bool = False) -> bool:
    data = read_registry()
    skills = data.get("skills", {})
    slug = slugify(slug_or_name)
    entry = skills.get(slug)
    if not entry and force:
        for k, v in skills.items():
            if str(v.get("name", "")).lower() == slug_or_name.lower():
                slug = k
                entry = v
                break
    if not entry:
        return False
    dest = Path(entry.get("dest", ""))
    with contextlib.suppress(Exception):
        if dest.exists():
            dest.unlink()
    with contextlib.suppress(Exception):
        script_path = MCP_SCRIPTS_DIR / f"{slug}.py"
        if script_path.exists():
            script_path.unlink()
    skills.pop(slug, None)
    data["skills"] = skills
    write_registry(data)
    return True
