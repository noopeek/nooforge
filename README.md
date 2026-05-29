# NooForge

Forje skills para assistentes de IA com um comando.

## Instalação

```bash
pip install nooforge
```

## Uso rápido

```bash
# Modo interativo
nooforge

# Gerar skill para Claude Code
nooforge generate -p claude-code -t "Minha skill"

# Gerar a partir de arquivo
nooforge generate -p cursor -i minha_skill.md

# Listar skills instaladas
nooforge list

# Ver detalhes de uma skill
nooforge info <nome>

# Remover skill
nooforge remove <nome>

# Exportar skill(s)
nooforge export [nome] -o arquivo.nooforge

# Importar skill(s)
nooforge import arquivo.nooforge

# Iniciar servidor MCP
nooforge serve --port 8765

# Ver caminhos de instalação
nooforge paths
```

## Plataformas suportadas

- `claude-code` — Claude Code (skills em `.claude/skills/`)
- `claude-desktop` — Claude Desktop (config MCP)
- `claude-web` — Claude Web (markdown)
- `cursor` — Cursor Rules
- `gemini-cli` — Gemini CLI (YAML)
- `windsurf` — Windsurf Rules
- `zed` — Zed Editor
- `continue` — Continue.dev
- `cline` — Cline (.clinerules)
- `open-interpreter` — Open Interpreter
- `ollama` — Ollama (Modelfile)
- `universal` — Formato universal

## Dependências opcionais

```bash
pip install nooforge[rich]   # UI bonita no terminal
pip install nooforge[yaml]   # Suporte a YAML
pip install nooforge[rich,yaml]  # Tudo
```

## Licença

MIT — noopeek
