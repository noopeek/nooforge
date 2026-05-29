import json
from pathlib import Path

from nooforge.core.constants import CONTINUE_CONFIG_DIR
from nooforge.core.utils import read_json, write_json
from nooforge.handlers.base import register_handler

@register_handler("continue")
def render_continue(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    config = read_json(CONTINUE_CONFIG_DIR / "config.json", {})
    config.setdefault("tools", [])
    config["tools"] = [t for t in config["tools"] if not (isinstance(t, dict) and t.get("name") == slug)]
    config["tools"].append({"name": slug, "description": description, "userDescription": body, "type": "python"})
    content = json.dumps(config, indent=2, ensure_ascii=False)
    return content, CONTINUE_CONFIG_DIR / "config.json", f"Adicionar ao arquivo {CONTINUE_CONFIG_DIR / 'config.json'}"
