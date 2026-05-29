from pathlib import Path

from nooforge.handlers.base import register_handler

@register_handler("cline")
def render_cline(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    content = f"# {name}\n\n> {description}\n\n{body}\n"
    return content, Path.cwd() / ".clinerules", "Salvar em .clinerules"
