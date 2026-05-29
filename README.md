<div align="center">

# NooForge

**Forge, manage and distribute AI skills to any platform.**

[![Python](https://img.shields.io/badge/python-3.10%2B-grey?style=flat-square&labelColor=111)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-grey?style=flat-square&labelColor=111)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-grey?style=flat-square&labelColor=111)](https://modelcontextprotocol.io)
[![Status](https://img.shields.io/badge/status-beta-grey?style=flat-square&labelColor=111)](#)

</div>

---

NooForge is an open-source CLI for creating, managing and installing **AI skills** — structured prompts, rules and instruction sets — across any AI coding assistant. Write a skill once, install it everywhere.

It also exposes your local skill library as a **Model Context Protocol (MCP) server**, compatible with any MCP client.

---

## Installation

```bash
git clone https://github.com/noopeek/nooforge.git
cd nooforge
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[rich,yaml]"
```

> NooForge runs on the Python standard library alone. `rich` adds the interactive TUI; `pyyaml` adds YAML frontmatter support.

```bash
# optional extras
pip install nooforge[rich]        # interactive TUI
pip install nooforge[yaml]        # YAML frontmatter
pip install nooforge[rich,yaml]   # both
```

---

## Quick start

```bash
# interactive TUI
nooforge

# forge from a file and install
nooforge generate -p gemini-cli -i my-skill.md --install

# forge from inline text
nooforge generate -p cursor -t "You are a senior code reviewer..." --install

# pipe from stdin
cat my-skill.md | nooforge generate -p windsurf --stdin --install
```

---

## Commands

| Command | Description |
|---|---|
| `generate` / `gen` | Forge and install a skill from a file, text or stdin |
| `list` | List installed skills, optionally filtered by platform |
| `info <slug>` | Show skill metadata and content |
| `edit <slug>` | Open a skill in `$EDITOR`, lint and reinstall |
| `lint <file>` | Validate a skill file against platform rules |
| `remove <slug>` | Uninstall a skill |
| `export [slug]` | Export one or all skills to a `.nooforge` bundle |
| `import <file>` | Import skills from a `.nooforge` bundle |
| `serve` | Start the local MCP server |
| `paths` | Show platform installation directories |

### generate

```bash
nooforge generate -p gemini-cli -i skill.md --install
nooforge generate -p cursor --dry-run          # preview without installing
nooforge generate -p claude-code --output out.md  # write to file only
```

### edit

Opens the installed skill in `$VISUAL` / `$EDITOR` (falls back to `nano` → `vi` → `notepad`). Changes are linted before saving and you are prompted to reinstall.

```bash
nooforge edit my-skill
nooforge edit my-skill --reinstall   # skip prompt, reinstall immediately
nooforge edit my-skill --force       # ignore lint errors
```

### lint

```bash
nooforge lint skill.md
nooforge lint skill.md -p gemini-cli   # platform-specific rules
```

### serve

```bash
nooforge serve              # default port 8765
nooforge serve --port 9000
```

---

## Skill format

Skills are plain Markdown files with an optional YAML frontmatter block.

```markdown
---
name: code-reviewer
description: Senior code reviewer focused on clarity and security
---

# Code Reviewer

## What it does
Reviews code for correctness, style, security and maintainability.

## Rules
- Label every issue with a severity: critical / warning / suggestion.
- Always explain *why* something is a problem.
- Suggest a concrete fix for every issue raised.
```

The parser also accepts raw Markdown without frontmatter, bold titles (`**Name**`) and H1/H2 headings — name and description are inferred automatically.

---

## Supported platforms

| Platform | Format | Install path |
|---|---|---|
| `gemini-cli` | YAML | `~/.gemini/skills/` |
| `cursor` | Markdown | `~/.cursor/rules/` |
| `windsurf` | Markdown | `~/.windsurf/rules/` |
| `claude-code` | Markdown | `~/.claude/skills/` |
| `claude-desktop` | JSON | `~/.config/Claude/claude_desktop_config.json` |
| `zed` | Markdown | `~/.config/zed/prompts/` |
| `cline` | Markdown | `~/.cline/rules/` |
| `continue` | JSON | `~/.continue/` |
| `ollama` | Modelfile | `~/.ollama/` |
| `open-interpreter` | Markdown | `~/.openinterpreter/` |
| `universal` | Markdown | `~/.nooforge/skills/` |

---

## MCP server

NooForge exposes your skills as MCP tools over HTTP (JSON-RPC 2.0).

```bash
nooforge serve
```

On startup the server auto-configures supported clients found on the system:
- `~/.gemini/settings.json` — Gemini CLI
- `~/.config/Claude/claude_desktop_config.json` — Claude Desktop

**Tools exposed**

| Tool | Description |
|---|---|
| `list_skills` | Return all installed skills |
| `get_skill` | Return a skill’s content by slug |
| `install_skill` | Forge and install a skill via MCP |
| `remove_skill` | Remove a skill by slug |

**HTTP endpoints**

| Endpoint | Method | Description |
|---|---|---|
| `/mcp` | `POST` | MCP protocol (JSON-RPC 2.0) |
| `/skills` | `GET` | List skills as JSON |
| `/health` | `GET` | Health check |

**Manual configuration (Gemini CLI)**

```json
{
  "mcpServers": {
    "nooforge": {
      "url": "http://127.0.0.1:8765/mcp"
    }
  }
}
```

---

## Export and import

```bash
# export all skills
nooforge export --output backup.nooforge

# export a single skill
nooforge export my-skill --output my-skill.nooforge

# import on another machine
nooforge import backup.nooforge
nooforge import backup.nooforge --force   # overwrite existing
```

---

## Development

```bash
git clone https://github.com/noopeek/nooforge.git
cd nooforge
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
pytest
```

**Project structure**

```
nooforge/
├── cli/
│   ├── commands/       # one module per command
│   ├── interactive.py  # TUI loop
│   ├── main.py         # argument parser & entrypoint
│   └── utils.py        # install_skill, find_render_target
├── core/
│   ├── extract.py      # name / description / body parser
│   ├── lint.py         # skill validator
│   └── constants.py    # paths, platform dirs
├── handlers/           # one module per platform
└── registry.py         # local skill registry (JSON)
```

---

## License

MIT © 2025 [noopeek](https://github.com/noopeek) — see [LICENSE](LICENSE) for details.
