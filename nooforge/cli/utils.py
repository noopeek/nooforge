import json
import logging
from pathlib import Path
from typing import Any

from nooforge.core.utils import ensure_dir, read_json, write_json, write_text
from nooforge.registry import register_skill
from nooforge.handlers import get_handler

logger = logging.getLogger("nooforge")

def install_skill(content: str, dest: Path, platform: str, name: str, slug: str, force: bool = False) -> bool:
    try:
        ensure_dir(dest.parent)
        if dest.exists() and not force:
            logger.error("Arquivo já existe: %s", dest)
            return False
        if platform in {"claude-desktop", "continue"} and dest.exists() and dest.suffix == ".json":
            try:
                existing = read_json(dest, {})
            except json.JSONDecodeError:
                logger.error("JSON inválido em %s", dest)
                return False
            new = json.loads(content)
            if platform == "claude-desktop":
                existing.setdefault("mcpServers", {})
                existing["mcpServers"].update(new.get("mcpServers", {}))
            else:
                existing.setdefault("tools", [])
                incoming = new.get("tools", [])
                names = {t.get("name") for t in existing["tools"] if isinstance(t, dict)}
                for item in incoming:
                    if isinstance(item, dict) and item.get("name") not in names:
                        existing["tools"].append(item)
            write_json(dest, existing)
        else:
            write_text(dest, content)
        register_skill(name, platform, dest, slug)
        return True
    except json.JSONDecodeError:
        logger.error("Falha de JSON ao instalar skill em %s", dest)
        return False
    except Exception as e:
        logger.error("Erro ao instalar skill: %s", e)
        return False

def find_render_target(platform: str, name: str, description: str, body: str, args: Any, registry: dict) -> tuple[str, Path, str, str]:
    from nooforge.core.utils import unique_slug
    slug = unique_slug(name, registry)
    handler = get_handler(platform)
    content, dest, instr = handler(name, description, body, slug=slug, ollama_model=getattr(args, "ollama_model", None))
    return content, dest, instr, slug
