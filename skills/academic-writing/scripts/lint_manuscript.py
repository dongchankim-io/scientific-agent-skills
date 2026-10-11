#!/usr/bin/env python3
"""Zero-dependency manuscript linter for LaTeX (.tex), Markdown (.md), and Typst (.typ).

Checks:
1. Citation keys used in manuscript vs. keys defined in a .bib file (missing & unused keys).
2. Unresolved placeholders (TODO, FIXME, TBD, [?], empty \\cite{}).
3. Academic prose hygiene (promotional hype / AI cliches).
4. LaTeX typographic anti-patterns (\\hline instead of booktabs, vertical table bars).
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Set

BANNED_WORDS = [
    "delve",
    "delves",
    "delving",
    "tapestry",
    "testament",
    "groundbreaking",
    "revolutionary",
    "paradigm shift",
    "seamlessly",
    "meticulously",
    "game-changer",
    "skyrocketed",
]


def parse_bib_keys(bib_path: str) -> Set[str]:
    if not os.path.exists(bib_path):
        return set()
    with open(bib_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return set(re.findall(r"@\w+\{\s*([^,\s]+)\s*,", content))


def extract_cited_keys(text: str, ext: str) -> Set[str]:
    keys: Set[str] = set()
    # LaTeX \cite, \citet, \citep, \citeauthor, \citeyear, \autocite
    for match in re.finditer(r"\\(?:cite[a-zA-Z]*|autocite)\s*(?:\[[^\]]*\])*\s*\{([^}]*)\}", text):
        raw = match.group(1)
        for k in raw.split(","):
            k = k.strip()
            if k:
                keys.add(k)

    # Pandoc / Markdown / Typst [@key] or @key
    if ext in {".md", ".typ", ".qmd"}:
        for match in re.finditer(r"(?<![a-zA-Z0-9_])@([a-zA-Z0-9_:-]+)", text):
            keys.add(match.group(1))
    return keys


def lint_file(manuscript_path: str, bib_path: str | None) -> Dict[str, object]:
    with open(manuscript_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    full_text = "".join(lines)
    ext = os.path.splitext(manuscript_path)[1].lower()

    issues: List[Dict[str, object]] = []

    for idx, line in enumerate(lines, start=1):
        # Skip LaTeX comments
        stripped = line.split("%")[0] if ext == ".tex" else line

        # 1. Placeholders
        if re.search(r"\b(TODO|FIXME|TBD|XXX)\b|\[\?+\]|\\cite\{\s*\}", stripped):
            issues.append({
                "line": idx,
                "severity": "error",
                "category": "placeholder",
                "message": f"Unresolved placeholder or empty citation: {stripped.strip()[:80]}",
            })

        # 2. Promotional / AI cliche words
        lower = stripped.lower()
        for word in BANNED_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", lower):
                issues.append({
                    "line": idx,
                    "severity": "warning",
                    "category": "style",
                    "message": f"Avoid promotional/cliche term '{word}' in academic prose.",
                })

        # 3. LaTeX-specific checks
        if ext == ".tex":
            if r"\hline" in stripped:
                issues.append({
                    "line": idx,
                    "severity": "warning",
                    "category": "latex-typography",
                    "message": r"Use booktabs (\toprule, \midrule, \bottomrule) instead of \hline.",
                })
            if re.search(r"\\begin\{tabular\}\{[^}]*\|[^}]*\}", stripped):
                issues.append({
                    "line": idx,
                    "severity": "warning",
                    "category": "latex-typography",
                    "message": "Avoid vertical lines '|' in LaTeX tabular environments (booktabs standard).",
                })

    cited_keys = extract_cited_keys(full_text, ext)
    missing_keys: List[str] = []
    unused_keys: List[str] = []

    if bib_path and os.path.exists(bib_path):
        bib_keys = parse_bib_keys(bib_path)
        missing_keys = sorted(cited_keys - bib_keys)
        unused_keys = sorted(bib_keys - cited_keys)
        for mk in missing_keys:
            issues.append({
                "line": 0,
                "severity": "error",
                "category": "missing-citation",
                "message": f"Citation key '{mk}' is cited in manuscript but missing from {bib_path}.",
            })

    return {
        "manuscript": manuscript_path,
        "bibliography": bib_path,
        "cited_count": len(cited_keys),
        "missing_citations": missing_keys,
        "unused_bib_entries": unused_keys,
        "issue_count": len(issues),
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit academic manuscript for citation integrity and style.")
    parser.add_argument("manuscript", help="Path to .tex, .md, or .typ manuscript file")
    parser.add_argument("--bib", default="references.bib", help="Path to BibTeX file (default: references.bib)")
    parser.add_argument("--json", action="store_true", help="Output report as JSON")
    args = parser.parse_args()

    if not os.path.exists(args.manuscript):
        print(f"Error: Manuscript file not found: {args.manuscript}", file=sys.stderr)
        sys.exit(1)

    report = lint_file(args.manuscript, args.bib)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"=== Manuscript Audit: {report['manuscript']} ===")
        print(f"Citations found in text: {report['cited_count']}")
        if report["missing_citations"]:
            print(f"[ERROR] Missing from {args.bib}: {', '.join(report['missing_citations'])}")
        if report["unused_bib_entries"]:
            print(f"[INFO]  Unused in {args.bib}: {', '.join(report['unused_bib_entries'])}")
        for issue in report["issues"]:
            loc = f"Line {issue['line']}" if issue["line"] else "Global"
            print(f"[{issue['severity'].upper()}] ({issue['category']}) {loc}: {issue['message']}")
        if report["issue_count"] == 0:
            print("[OK] No citation or style issues detected!")

    has_errors = any(i["severity"] == "error" for i in report["issues"])
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
