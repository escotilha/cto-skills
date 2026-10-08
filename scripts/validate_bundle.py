#!/usr/bin/env python3
"""Validate the portable package, not runtime behavior or comprehensive privacy."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "README.md", "LICENSE", "scripts/validate_bundle.py",
    "skills/cto/SKILL.md", "skills/cto-fable/SKILL.md",
    "skills/cto-evolution/SKILL.md",
    "skills/cto-evolution/references/evaluation-contract.md",
    *(f"skills/cto/references/{name}.md" for name in (
        "architecture-quality", "decision-discriminators", "discovery",
        "infra-security", "intended-vs-implemented", "ledger", "performance",
        "report-templates", "security", "synthesis")),
}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FOOTPRINT = (
    ("absolute personal path", re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/")),
    ("email address", re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")),
    ("private key material", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("credential assignment", re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[\"']?[A-Za-z0-9_+/=-]{20,}")),
)


def main():
    errors = []
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_symlink():
            errors.append(f"symlink not allowed: {relative}")
        elif path.is_file():
            files.append(path)
    actual = {str(path.relative_to(ROOT)) for path in files}
    for missing in sorted(EXPECTED - actual):
        errors.append(f"missing resource: {missing}")
    for extra in sorted(actual - EXPECTED):
        errors.append(f"unexpected publishable file: {extra}")
    for path in files:
        relative = path.relative_to(ROOT)
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            errors.append(f"unreadable text: {relative}: {exc}")
            continue
        if path.name == "SKILL.md":
            match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
            if not match:
                errors.append(f"missing frontmatter: {relative}")
            else:
                fields = dict(re.findall(r"^([a-z_-]+):\s*(.+)$", match[1], re.M))
                if set(fields) != {"name", "description"}:
                    errors.append(f"unsupported frontmatter fields: {relative}")
                if fields.get("name") != path.parent.name:
                    errors.append(f"name differs from directory: {relative}")
                if not fields.get("description", "").strip():
                    errors.append(f"empty description: {relative}")
        if path.suffix == ".md":
            for raw in LINK.findall(content):
                target = raw.strip().strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                resolved = (path.parent / unquote(target)).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                    errors.append(f"broken/escaping link: {relative}: {raw}")
        for label, pattern in FOOTPRINT:
            if pattern.search(content):
                errors.append(f"public-footprint flag ({label}): {relative}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(files)} files; inventory, frontmatter, local resources, footprint screen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
