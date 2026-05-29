from pathlib import Path
import sys

HOME = Path.home()
NOOFORGE_DIR = HOME / ".nooforge"
REGISTRY_FILE = NOOFORGE_DIR / "registry.json"
MCP_SCRIPTS_DIR = NOOFORGE_DIR / "mcp_scripts"
DEFAULT_PORT = 8765

if sys.platform == "win32":
    CLAUDE_DESKTOP_CONFIG = HOME / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    CLAUDE_CODE_DIR = HOME / ".claude" / "skills"
elif sys.platform == "darwin":
    CLAUDE_DESKTOP_CONFIG = HOME / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    CLAUDE_CODE_DIR = HOME / ".claude" / "skills"
else:
    CLAUDE_DESKTOP_CONFIG = HOME / ".config" / "Claude" / "claude_desktop_config.json"
    CLAUDE_CODE_DIR = HOME / ".claude" / "skills"

CURSOR_RULES_DIR = HOME / ".cursor" / "rules"
GEMINI_SKILLS_DIR = HOME / ".gemini" / "skills"
WINDSURF_RULES_DIR = HOME / ".windsurf" / "rules"
ZED_CONFIG_DIR = HOME / ".config" / "zed"
CONTINUE_CONFIG_DIR = HOME / ".continue"

VALID_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".nooforge", ".cursorrules", ".windsurfrules", ".txt", ".modelfile"}
CACHE_TTL = 5.0

DANGEROUS_PATTERNS = [
    ("rm -rf", "error"),
    ("sudo ", "warning"),
    ("format c:", "error"),
    ("del /f", "error"),
    ("del /s /q", "error"),
    ("mkfs", "error"),
    (":(){ :|:& };:", "error"),
    ("> /dev/sda", "error"),
    ("dd if=", "error"),
    ("chmod 777 /", "warning"),
    ("curl ", "warning"),
    ("wget ", "warning"),
    (" sh", "warning"),
    ("eval(", "error"),
    ("exec(", "error"),
    ("subprocess.call", "error"),
    ("os.system", "error"),
    ("__import__", "warning"),
]
