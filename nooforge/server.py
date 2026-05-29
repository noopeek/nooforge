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


def _json_response(handler: "NooForgeHandler", status: int, payload: dict) -> None:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


class NooForgeHandler(BaseHTTPRequestHandler):

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------
    def do_GET(self):
        if self.path == "/health":
            _json_response(self, 200, {"status": "ok"})
        elif self.path in ("/skills", "/mcp"):
            skills = collect_skills()
            _json_response(self, 200, {"skills": skills, "count": len(skills)})
        else:
            self.send_response(404)
            self.end_headers()

    # ------------------------------------------------------------------
    # POST — JSON-RPC 2.0 MCP
    # ------------------------------------------------------------------
    def do_POST(self):
        if self.path != "/mcp":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"

        try:
            req = json.loads(body)
        except json.JSONDecodeError:
            _json_response(self, 400, {
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": "parse error"}
            })
            return

        rpc_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params", {})

        # --- list_skills ---
        if method == "list_skills":
            skills = collect_skills()
            _json_response(self, 200, {
                "jsonrpc": "2.0", "id": rpc_id,
                "result": {"skills": skills, "count": len(skills)}
            })

        # --- get_skill ---
        elif method == "get_skill":
            slug = params.get("slug", "") or params.get("id", "")
            skills = collect_skills()
            match = next((s for s in skills if s["id"] == slug), None)
            if match:
                try:
                    content = open(match["path"], encoding="utf-8").read()
                except OSError as exc:
                    _json_response(self, 200, {
                        "jsonrpc": "2.0", "id": rpc_id,
                        "error": {"code": -32603, "message": str(exc)}
                    })
                    return
                _json_response(self, 200, {
                    "jsonrpc": "2.0", "id": rpc_id,
                    "result": {**match, "content": content}
                })
            else:
                _json_response(self, 200, {
                    "jsonrpc": "2.0", "id": rpc_id,
                    "error": {"code": -32602, "message": f"skill '{slug}' not found"}
                })

        # --- method not found ---
        else:
            _json_response(self, 200, {
                "jsonrpc": "2.0", "id": rpc_id,
                "error": {"code": -32601, "message": f"method '{method}' not found"}
            })

    def log_message(self, fmt, *args):
        return


def serve(port: int) -> None:
    server = HTTPServer(("127.0.0.1", port), NooForgeHandler)
    print(f"servidor mcp em http://127.0.0.1:{port}/mcp")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
