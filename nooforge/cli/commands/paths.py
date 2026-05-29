import argparse
from nooforge.core.constants import (
    CLAUDE_CODE_DIR, CLAUDE_DESKTOP_CONFIG, CURSOR_RULES_DIR,
    GEMINI_SKILLS_DIR, WINDSURF_RULES_DIR, ZED_CONFIG_DIR,
    CONTINUE_CONFIG_DIR, REGISTRY_FILE, MCP_SCRIPTS_DIR
)

def cmd_paths(args: argparse.Namespace) -> int:
    paths = {
        "claude_code": CLAUDE_CODE_DIR,
        "claude_desktop": CLAUDE_DESKTOP_CONFIG,
        "cursor": CURSOR_RULES_DIR,
        "gemini": GEMINI_SKILLS_DIR,
        "windsurf": WINDSURF_RULES_DIR,
        "zed": ZED_CONFIG_DIR,
        "continue": CONTINUE_CONFIG_DIR,
        "registry": REGISTRY_FILE,
        "mcp_scripts": MCP_SCRIPTS_DIR,
    }
    for k, v in paths.items():
        print(f"{k}: {v}")
    return 0
