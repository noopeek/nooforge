from pathlib import Path

from nooforge.handlers.base import register_handler

@register_handler("universal")
def render_universal(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    content = f"---\nname: {slug}\ndescription: {description}\nversion: 1.0.0\n---\n\n# {name}\n\n{body}\n"
    dest = Path.cwd() / f"{slug}.skill.md"
    return content, dest, f"Skill universal em {dest}"
