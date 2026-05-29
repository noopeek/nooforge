from pathlib import Path

from nooforge.core.constants import CURSOR_RULES_DIR
from nooforge.handlers.base import register_handler

@register_handler("cursor")
def render_cursor(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    content = f"# {name}\n\n{description}\n\n{body}\n"
    dest = CURSOR_RULES_DIR / f"{slug}.md"
    return content, dest, f"Salvar em {dest}"
