from pathlib import Path

from nooforge.core.constants import GEMINI_SKILLS_DIR
from nooforge.handlers.base import register_handler

HAS_YAML = False
try:
    import yaml
    HAS_YAML = True
except ImportError:
    yaml = None

@register_handler("gemini-cli")
def render_gemini(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    if HAS_YAML:
        content = yaml.safe_dump({"name": slug, "description": description, "prompt": body}, allow_unicode=True, sort_keys=False)
    else:
        lines = body.splitlines()
        indented = "\n".join(f"  {line}" for line in lines)
        content = f"name: {slug}\ndescription: {description}\nprompt: |\n{indented}\n"
    dest = GEMINI_SKILLS_DIR / f"{slug}.yaml"
    return content, dest, f"Salvar em {dest}"
