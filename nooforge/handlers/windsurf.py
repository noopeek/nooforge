from pathlib import Path

from nooforge.core.constants import WINDSURF_RULES_DIR
from nooforge.handlers.base import register_handler

@register_handler("windsurf")
def render_windsurf(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    content = f"# {name}\n\n{description}\n\n{body}\n"
    dest = WINDSURF_RULES_DIR / f"{slug}.md"
    return content, dest, f"Salvar em {dest}"
