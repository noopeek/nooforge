import json
import os
import sys
from pathlib import Path

from nooforge.core.constants import MCP_SCRIPTS_DIR
from nooforge.core.utils import ensure_dir, write_text

def create_mcp_script(name: str, body: str, slug: str) -> Path:
    ensure_dir(MCP_SCRIPTS_DIR)
    script_path = MCP_SCRIPTS_DIR / f"{slug}.py"
    code = f'print({json.dumps(f"Skill: {name}\n{body}")})\n'
    write_text(script_path, code)
    if sys.platform != "win32":
        os.chmod(script_path, 0o755)
    return script_path
