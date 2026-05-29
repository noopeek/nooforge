from pathlib import Path

from nooforge.core.constants import ZED_CONFIG_DIR
from nooforge.handlers.base import register_handler

@register_handler("zed")
def render_zed(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    content = f"# {name}\n\n{description}\n\n{body}\n"
    dest = ZED_CONFIG_DIR / "prompts" / f"{slug}.md"
    return content, dest, f"Salvar em {dest}"
