import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Dict

from nooforge.core.constants import (
    CLAUDE_CODE_DIR, GEMINI_SKILLS_DIR, CURSOR_RULES_DIR,
    WINDSURF_RULES_DIR, ZED_CONFIG_DIR, CONTINUE_CONFIG_DIR,
    VALID_EXTENSIONS, CACHE_TTL
)

_cache = {"ts": 0.0, "data": []}

def collect_skills() -> List[Dict[str, str]]:
    now = time.time()
    if now - _cache["ts"] < CACHE_TTL:
        return list(_cache["data"])
    skills = []
    roots = [
        CLAUDE_CODE_DIR,
        GEMINI_SKILLS_DIR,
        CURSOR_RULES_DIR,
        WINDSURF_RULES_DIR,
        ZED_CONFIG_DIR / "prompts",
        CONTINUE_CONFIG_DIR,
    ]
    for root in roots:
        if not root.exists():
            continue
        for f in root.rglob("*"):
            if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS:
                skills.append({"id": f.stem, "name": f.stem, "path": str(f)})
    _cache["ts"] = now
    _cache["data"] = skills
    return skills

class NooForgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/mcp":
            payload = {"skills": collect_skills(), "count": len(collect_skills())}
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, fmt, *args):
        return

def serve(port: int) -> None:
    server = HTTPServer(("127.0.0.1", port), NooForgeHandler)
    print(f"Servidor MCP rodando em http://127.0.0.1:{port}/mcp")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
