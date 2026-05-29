import re
from typing import Any

HAS_YAML = False
try:
    import yaml
    HAS_YAML = True
except ImportError:
    yaml = None

def extract_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.lstrip().startswith("---"):
        return {}, text
    lines = text.splitlines()
    if len(lines) < 3:
        return {}, text
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}, text
    fm_text = "\n".join(lines[1:end])
    rest = "\n".join(lines[end + 1:]).strip()
    if HAS_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict):
                return data, rest
        except Exception:
            pass
    data: dict[str, Any] = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data, rest

def extract_skill_info(text: str) -> tuple[str, str, str]:
    text = text.strip()
    fm, rest = extract_frontmatter(text)
    if fm:
        name = str(fm.get("name", "")).strip()
        desc = str(fm.get("description", name)).strip() or name
        body = rest.strip() or desc
        if name:
            return name, desc, body
    lines = text.splitlines()
    if not lines:
        return "skill", "skill", ""
    first_line = lines[0].strip()
    m = re.match(r"^(?:KILL|SKILL)\s*:\s*(.+?)\s*[—-]\s*(.+)$", first_line, re.IGNORECASE)
    if m:
        name = m.group(1).strip()
        desc = m.group(2).strip()
        body = "\n".join(lines[1:]).strip() or desc
        return name, desc, body
    h1 = re.match(r"^#\s+(.+)$", first_line)
    if h1:
        name = h1.group(1).strip()
        remaining = "\n".join(lines[1:]).strip()
        desc = next((l.strip() for l in remaining.splitlines() if l.strip()), name)
        return name, desc, remaining or desc
    name = first_line[:60].strip() or "skill"
    desc = first_line[:120].strip() or name
    body = "\n".join(lines).strip()
    return name, desc, body
