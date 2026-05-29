from dataclasses import dataclass
from typing import List

from nooforge.core.constants import DANGEROUS_PATTERNS

@dataclass
class LintIssue:
    severity: str
    message: str

def lint_skill(content: str, platform: str) -> List[LintIssue]:
    issues = []
    lower = content.lower()
    if platform in {"claude-code", "universal"}:
        if not content.lstrip().startswith("---"):
            issues.append(LintIssue("error", "Frontmatter YAML ausente"))
        if "name:" not in lower:
            issues.append(LintIssue("error", "Campo name ausente"))
        if "description:" not in lower:
            issues.append(LintIssue("warning", "Campo description ausente"))
    if len(content.strip()) < 20:
        issues.append(LintIssue("warning", "Conteúdo muito curto"))
    if len(content) > 50000:
        issues.append(LintIssue("warning", "Conteúdo muito grande"))
    for pat, severity in DANGEROUS_PATTERNS:
        if pat in lower:
            issues.append(LintIssue(severity, f"Padrão potencialmente perigoso detectado: {pat}"))
    return issues
