"""Registro local de skills do NooForge."""
from __future__ import annotations

import contextlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nooforge.core.constants import REGISTRY_FILE, MCP_SCRIPTS_DIR
from nooforge.core.utils import read_json, write_json, slugify


def read_registry() -> dict:
    return read_json(REGISTRY_FILE, {"skills": {}, "meta": {"version": 1}})


def write_registry(data: dict) -> None:
    data.setdefault("meta", {})
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(REGISTRY_FILE, data)


def register_skill(
    name: str,
    platform: str,
    dest: Path,
    slug: str,
    description: str = "",
) -> None:
    data = read_registry()
    data.setdefault("skills", {})
    existing = data["skills"].get(slug, {})
    data["skills"][slug] = {
        "name": name,
        "platform": platform,
        "dest": str(dest),
        "description": description or name,
        "installed_at": existing.get("installed_at") or datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "version": existing.get("version", 1) + (1 if existing else 0),
    }
    write_registry(data)


def get_skill(slug_or_name: str) -> dict[str, Any] | None:
    data = read_registry()
    skills = data.get("skills", {})
    slug = slugify(slug_or_name)

    if slug in skills:
        return {"slug": slug, **skills[slug]}

    for k, v in skills.items():
        if str(v.get("name", "")).lower() == slug_or_name.lower():
            return {"slug": k, **v}

    query = slug_or_name.lower()
    for k, v in skills.items():
        if query in str(v.get("name", "")).lower() or query in k.lower():
            return {"slug": k, **v}

    return None


def list_skills(platform: str | None = None) -> list[dict[str, Any]]:
    data = read_registry()
    skills = data.get("skills", {})
    result = [{"slug": k, **v} for k, v in skills.items()]
    if platform:
        result = [s for s in result if s.get("platform") == platform]
    return sorted(result, key=lambda s: s.get("installed_at", ""), reverse=True)


def remove_skill(slug_or_name: str, force: bool = False) -> tuple[bool, str]:
    data = read_registry()
    skills = data.get("skills", {})

    entry = get_skill(slug_or_name)
    if not entry:
        return False, f"skill '{slug_or_name}' nao encontrada no registro."

    slug = entry["slug"]
    dest = Path(entry.get("dest", ""))

    # Usa OSError em vez de Exception para não suprimir bugs inesperados
    with contextlib.suppress(OSError):
        if dest.exists():
            dest.unlink()

    with contextlib.suppress(OSError):
        script_path = MCP_SCRIPTS_DIR / f"{slug}.py"
        if script_path.exists():
            script_path.unlink()

    skills.pop(slug, None)
    data["skills"] = skills
    write_registry(data)
    return True, f"skill '{slug}' removida com sucesso."


def skill_exists(slug_or_name: str) -> bool:
    return get_skill(slug_or_name) is not None
