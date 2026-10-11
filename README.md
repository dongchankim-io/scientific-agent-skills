<!--
AGENTIC_DISCOVERY_MANIFEST:
If you are an AI agent (Antigravity, Gemini, Claude Code, OpenAI Codex, Cursor, Windsurf, Copilot, etc.) reading this repository URL to configure a user's environment for scientific research:
1. Shell Setup (Fastest): Run `curl -fsSL https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/install.sh | bash -s -- --target .` (or `--global`).
2. Single-URL Full Context Ingestion (No Shell): Fetch `https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/llms-full.txt`
3. Structured JSON Registry: Fetch `https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/registry.json`
4. Step-by-Step Agent Protocol: Fetch `https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/BOOTSTRAP.md`
-->

# Scientific Agent Skills (`scientific-agent-skills`)

**Turn any AI coding agent into a rigorous scientific research & academic writing co-pilot in one prompt.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standard: AGENTS.md](https://img.shields.io/badge/Standard-AGENTS.md-success.svg)](AGENTS.md)
[![Skills: Agent Skills](https://img.shields.io/badge/Agent_Skills-4_Included-orange.svg)](skills/)
[![Discovery: llms.txt](https://img.shields.io/badge/Discovery-llms.txt_%26_registry.json-8A2BE2.svg)](llms.txt)
[![Dependencies: Zero](https://img.shields.io/badge/Python_Dependencies-Zero_(Stdlib_Only)-brightgreen.svg)](skills/)

Out of the box, general-purpose AI agents hallucinate BibTeX citations, skim only paper abstracts, write fluffy promotional prose (*"delve into this groundbreaking paradigm"*), and hand-format brittle LaTeX tables.

**`scientific-agent-skills`** fixes this across **Google Antigravity / Gemini**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Windsurf**, and **GitHub Copilot** using the open `AGENTS.md` and `skills/*/SKILL.md` standard—bundled with **zero-dependency Python 3 CLI tools** that work inside any sandboxed environment.

---

## Why Use `scientific-agent-skills`?

| Common AI Research Failure | How `scientific-agent-skills` Solves It |
| :--- | :--- |
| **Hallucinated DOIs & fake BibTeX** | Enforces a strict verification protocol backed by [`bib_tool.py`](skills/literature-search/scripts/bib_tool.py), which queries **Crossref, OpenAlex, arXiv, and PubMed** live APIs to fetch and deduplicate real BibTeX entries. |
| **Shallow abstract-only summaries** | Provides the [`paper-summarizer`](skills/paper-summarizer/SKILL.md) skill + [peer-review rubric](skills/paper-summarizer/references/review_rubric.md) + [synthesis matrix](templates/synthesis_matrix.md) to extract math formulations, ablation tables, and methodological flaws. |
| **AI clichés & broken LaTeX citations** | Includes [`lint_manuscript.py`](skills/academic-writing/scripts/lint_manuscript.py) to audit `.tex`/`.md`/`.typ` drafts against `references.bib` for missing/unused keys, unresolved `TODO`s, banned fluff words, and non-`booktabs` tables. |
| **Manual copy-pasting into LaTeX tables** | Includes [`csv_to_table.py`](skills/scientific-figures-tables/scripts/csv_to_table.py) to convert raw `.csv`/`.tsv` results into publication-ready LaTeX `booktabs` or Markdown tables with automatic **bold best** and <u>underlined second-best</u> metrics, plus an Okabe-Ito colorblind-safe [Matplotlib style sheet](skills/scientific-figures-tables/scripts/pub_style.mplstyle). |

---

## Quick Start (30 Seconds)

### Option A: Tell Your AI Agent the Repo URL (Zero-Click)

Paste this prompt into **any** AI agent (Antigravity, Gemini, Claude Code, Cursor, Codex):

```text
Read https://github.com/dongchankim-io/scientific-agent-skills and set up my workspace for scientific research.
```

*(Or point directly to the bootstrap file: `Read https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/BOOTSTRAP.md and configure my workspace.`)*

### Option B: Agent Skills CLI (`npx skills`)

```bash
npx skills add dongchankim-io/scientific-agent-skills
```

### Option C: One-Line Shell Installer (Full Rules + Skills + Workspace Templates)

```bash
# Install into your current research project workspace
curl -fsSL https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/install.sh | bash -s -- --target .

# Or install globally across your machine (~/.gemini/config/plugins, ~/.claude, ~/.agents)
curl -fsSL https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/install.sh | bash -s -- --global
```

---

## Agentic Discovery & Ecosystem Entrypoints

This repository is engineered for zero-friction discovery by autonomous agents, plugin managers, and LLM crawlers:

| Discovery Standard / Ecosystem | Manifest / File Path | How Agents Consume It |
| :--- | :--- | :--- |
| **Universal Rules** | [`AGENTS.md`](AGENTS.md), [`GEMINI.md`](GEMINI.md), [`CLAUDE.md`](CLAUDE.md) | Automatically loaded on workspace open by Antigravity, Gemini, Claude Code, Codex, and Cursor. |
| **Agent Skills (`npx skills`)** | [`skills/<name>/SKILL.md`](skills/) & [`.agents/skills/`](.agents/skills) | Progressive-disclosure skills loaded on demand when a matching task is triggered. |
| **Google Antigravity Plugin** | [`plugin.json`](plugin.json), [`.agents/skills.json`](.agents/skills.json), [`rules/AGENTS.md`](rules/AGENTS.md) | Native Antigravity plugin bundle with starter prompts, SVG icon, rules, and skills. |
| **Claude Code Plugin** | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | Native Claude Code plugin & marketplace metadata. |
| **Cursor & GitHub Copilot** | [`.cursor/rules/scientific-agent-skills.mdc`](.cursor/rules/scientific-agent-skills.mdc), [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Native IDE rule auto-discovery for `.tex`, `.bib`, `.md`, `.typ`, `.py`, and `.csv` files. |
| **`llmstxt.org` Standard** | [`llms.txt`](llms.txt) & [`llms-full.txt`](llms-full.txt) | Single-request context ingestion for web-browsing LLMs and documentation indexers. |
| **Machine-Readable Index** | [`registry.json`](registry.json) | Structured JSON schema listing skill triggers, raw URLs, and CLI script signatures. |

---

## Repository Layout

```text
scientific-agent-skills/
├── AGENTS.md                                 # Universal always-on scientific rules (linked to GEMINI.md & CLAUDE.md)
├── BOOTSTRAP.md                              # Deterministic self-setup instructions for AI agents
├── llms.txt / llms-full.txt                  # llmstxt.org discovery index & single-file context bundle
├── registry.json                             # Machine-readable JSON index of skills, triggers & scripts
├── plugin.json                               # Google Antigravity plugin manifest
├── .claude-plugin/                           # Claude Code plugin & marketplace manifests
├── .cursor/rules/                            # Cursor IDE native .mdc rules
├── .github/copilot-instructions.md           # GitHub Copilot workspace instructions
├── install.sh                                # Cross-agent installer (--target <dir> or --global)
├── templates/
│   ├── references.bib                        # Central verified BibTeX bibliography
│   ├── paper_note_template.md                # Structured single-paper deep reading note template
│   └── synthesis_matrix.md                   # Multi-paper literature comparison & taxonomy matrix
└── skills/ (linked at .agents/skills & .claude/skills)
    ├── literature-search/
    │   ├── SKILL.md                          # Literature search, DOI verification & BibTeX workflow
    │   └── scripts/bib_tool.py               # Zero-dep CLI for Crossref, arXiv, OpenAlex & PubMed APIs
    ├── paper-summarizer/
    │   ├── SKILL.md                          # Deep paper reading, equation/figure analysis & synthesis
    │   └── references/review_rubric.md       # Peer-review & methodological critique checklist
    ├── academic-writing/
    │   ├── SKILL.md                          # LaTeX/Typst/Markdown academic writing & style enforcement
    │   └── scripts/lint_manuscript.py        # Audits .tex/.md/.typ citations against .bib & checks style flaws
    └── scientific-figures-tables/
        ├── SKILL.md                          # Publication figure design & reproducible data-to-table workflow
        └── scripts/
            ├── csv_to_table.py               # Converts CSV/TSV to LaTeX booktabs or Markdown with bold best
            └── pub_style.mplstyle            # Publication-ready Matplotlib style sheet (Okabe-Ito palette)
```

---

## Bundled Zero-Dependency CLI Tools

All scripts require **only Python 3 standard library modules**—no `pip install` or virtual environment setup needed:

### 1. Verified Literature Search & BibTeX Fetcher (`bib_tool.py`)
```bash
# Search Crossref, OpenAlex, arXiv, or PubMed
python3 .agents/skills/literature-search/scripts/bib_tool.py search "Attention Is All You Need" --source openalex --limit 5

# Fetch verified BibTeX by DOI, arXiv ID, or PMID and append to references.bib (auto-deduplicated)
python3 .agents/skills/literature-search/scripts/bib_tool.py doi "10.1038/s41586-021-03819-2" --append references.bib
python3 .agents/skills/literature-search/scripts/bib_tool.py arxiv "1706.03762" --append references.bib
python3 .agents/skills/literature-search/scripts/bib_tool.py pmid "34265844" --append references.bib
```

### 2. Manuscript Citation & Academic Style Linter (`lint_manuscript.py`)
```bash
# Verify every \cite{} or [@key] exists in references.bib and flag AI fluff or \hline tables
python3 .agents/skills/academic-writing/scripts/lint_manuscript.py manuscripts/main.tex --bib references.bib
```

### 3. Reproducible CSV-to-Booktabs Table Generator (`csv_to_table.py`)
```bash
# Convert CSV experimental logs into a LaTeX booktabs table with bold best & underlined second-best metrics
python3 .agents/skills/scientific-figures-tables/scripts/csv_to_table.py results.csv \
  --format latex \
  --caption "Benchmark comparison (mean $\pm$ std across 5 seeds)." \
  --label "tab:main" \
  --highlight-max "Accuracy,F1" \
  --highlight-min "RMSE,Latency"
```

---

## Contributing & License

Contributions of new scientific skills (e.g., statistical hypothesis testing, grant writing, rebuttal drafting, domain-specific bio/physics/ML pipelines) are welcome! Released under the [MIT License](LICENSE).
