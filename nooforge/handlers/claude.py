import json
import sys
from pathlib import Path

from nooforge.core.constants import CLAUDE_CODE_DIR, CLAUDE_DESKTOP_CONFIG
from nooforge.core.utils import read_json, write_json
from nooforge.core.mcp_script import create_mcp_script
from nooforge.handlers.base import register_handler

@register_handler("claude-code")
def render_claude_code(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    content = f"---\nname: {slug}\ndescription: {description}\nallowed-tools: Read, Write, Edit, Bash\n---\n\n# {name}\n\n{body}\n"
    dest = CLAUDE_CODE_DIR / f"{slug}.md"
    return content, dest, f"Instalar em {dest}"

@register_handler("claude-desktop")
def render_claude_desktop(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    slug = kwargs["slug"]
    script_path = create_mcp_script(name, body, slug)
    config = read_json(CLAUDE_DESKTOP_CONFIG, {"mcpServers": {}})
    config.setdefault("mcpServers", {})
    config["mcpServers"][slug] = {"command": sys.executable, "args": [str(script_path)]}
    content = json.dumps(config, indent=2, ensure_ascii=False)
    return content, CLAUDE_DESKTOP_CONFIG, f"Mesclar com {CLAUDE_DESKTOP_CONFIG}"

@register_handler("claude-web")
def render_claude_web(name: str, description: str, body: str, **kwargs) -> tuple[str, Path, str]:
    content = f"# {name}\n\n{description}\n\n{body}\n"
    return content, Path("claude_web_skill.md"), "Copiar para o Claude Web"
