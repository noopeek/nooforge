from pathlib import Path

from nooforge.handlers.base import register_handler

@register_handler("open-interpreter")
def render_open_interpreter(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    content = f"{description}\n\n{body}\n"
    return content, Path.cwd() / f"{slug}.txt", "Salvar como texto para Open Interpreter"
