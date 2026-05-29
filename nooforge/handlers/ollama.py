import os
from pathlib import Path

from nooforge.handlers.base import register_handler

@register_handler("ollama")
def render_ollama(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    model = kwargs.get("ollama_model") or os.getenv("NOOFORGE_OLLAMA_MODEL") or "llama3.2"
    content = f'FROM {model}\n\nSYSTEM """\n{description}\n\n{body}\n"""\n\nPARAMETER temperature 0.7\n'
    dest = Path.cwd() / f"{slug}.Modelfile"
    return content, dest, f"Executar: ollama create {slug} -f {dest}"
