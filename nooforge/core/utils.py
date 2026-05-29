import json
import re
import logging
from pathlib import Path
from typing import Any

from nooforge.core.constants import REGISTRY_FILE, NOOFORGE_DIR

logger = logging.getLogger("nooforge")

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write_text(path: Path, content: str) -> None:
    content = content.replace("\\n", "\n")
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8", newline="\n")

def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as e:
        logger.error("JSON inválido em %s: %s", path, e)
        return default
    except Exception as e:
        logger.error("Erro ao ler JSON %s: %s", path, e)
        return default

def write_json(path: Path, data: Any) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False))

def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "skill"

def unique_slug(name: str, registry: dict[str, Any] | None = None) -> str:
    base = slugify(name)
    if registry is None:
        from nooforge.registry import read_registry
        registry = read_registry()
    skills = registry.get("skills", {})
    if base not in skills:
        return base
    i = 2
    while True:
        candidate = f"{base}-{i}"
        if candidate not in skills:
            return candidate
        i += 1
