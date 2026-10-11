# Scientific Agent Skills (`scientific-agent-skills`)

**Turn any AI coding agent into a rigorous scientific research & academic writing co-pilot in one prompt.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standard: AGENTS.md](https://img.shields.io/badge/Standard-AGENTS.md-success.svg)](AGENTS.md)
[![Skills: .agents/skills](https://img.shields.io/badge/Agent_Skills-4_Included-orange.svg)](.agents/skills/)
[![Dependencies: Zero](https://img.shields.io/badge/Python_Dependencies-Zero_(Stdlib_Only)-brightgreen.svg)](.agents/skills/)

Out of the box, general-purpose AI agents hallucinate BibTeX citations, skim only paper abstracts, write fluffy promotional prose (*"delve into this groundbreaking paradigm"*), and hand-format brittle LaTeX tables.

**`scientific-agent-skills`** fixes this across **Google Antigravity / Gemini**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Windsurf**, and **GitHub Copilot** using the open `AGENTS.md` and `.agents/skills/` standard—bundled with **zero-dependency Python 3 CLI tools** that work inside any sandboxed environment.

---

## Why Use `scientific-agent-skills`?

| Common AI Research Failure | How `scientific-agent-skills` Solves It |
| :--- | :--- |
| **Hallucinated DOIs & fake BibTeX** | Enforces a strict verification protocol backed by [`bib_tool.py`](.agents/skills/literature-search/scripts/bib_tool.py), which queries **Crossref, OpenAlex, arXiv, and PubMed** live APIs to fetch and deduplicate real BibTeX entries. |
| **Shallow abstract-only summaries** | Provides the [`paper-summarizer`](.agents/skills/paper-summarizer/SKILL.md) skill + [peer-review rubric](.agents/skills/paper-summarizer/references/review_rubric.md) + [synthesis matrix](templates/synthesis_matrix.md) to extract math formulations, ablation tables, and methodological flaws. |
| **AI clichés & broken LaTeX citations** | Includes [`lint_manuscript.py`](.agents/skills/academic-writing/scripts/lint_manuscript.py) to audit `.tex`/`.md`/`.typ` drafts against `references.bib` for missing/unused keys, unresolved `TODO`s, banned fluff words, and non-`booktabs` tables. |
| **Manual copy-pasting into LaTeX tables** | Includes [`csv_to_table.py`](.agents/skills/scientific-figures-tables/scripts/csv_to_table.py) to convert raw `.csv`/`.tsv` results into publication-ready LaTeX `booktabs` or Markdown tables with automatic **bold best** and <u>underlined second-best</u> metrics, plus an Okabe-Ito colorblind-safe [Matplotlib style sheet](.agents/skills/scientific-figures-tables/scripts/pub_style.mplstyle). |

---

## Quick Start (30 Seconds)

### Option A: One-Prompt Agent Self-Setup (Zero-Click)

Copy and paste this single prompt into **any** AI agent (Antigravity, Claude Code, Cursor, Codex, etc.):

```text
Read https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/BOOTSTRAP.md and follow the instructions to configure my workspace for scientific research.
```

The agent will read [`BOOTSTRAP.md`](BOOTSTRAP.md), install the rules and skills into your project, scaffold your `papers/`, `manuscripts/`, and `references.bib` structure, and verify all CLI tools automatically.

### Option B: One-Line Terminal Installer

```bash
# Install into your current research project workspace
curl -fsSL https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/install.sh | bash -s -- --target .

# Or install globally across your machine (~/.gemini/config, ~/.claude, ~/.agents)
curl -fsSL https://raw.githubusercontent.com/dongchankim-io/scientific-agent-skills/main/install.sh | bash -s -- --global
```

*(If you cloned the repo locally, run `./install.sh --target .` or `./install.sh --global`.)*

---

## What's Inside

```text
scientific-agent-skills/
├── AGENTS.md                                 # Universal always-on scientific rules & citation integrity protocol
├── BOOTSTRAP.md                              # Deterministic self-setup instructions for AI agents reading via URL
├── install.sh                                # Cross-agent installer (workspace or global)
├── templates/
│   ├── references.bib                        # Central verified BibTeX bibliography
│   ├── paper_note_template.md                # Structured single-paper deep reading note template
│   └── synthesis_matrix.md                   # Multi-paper literature comparison & taxonomy matrix
└── .agents/
    └── skills/
        ├── literature-search/
        │   ├── SKILL.md                      # Literature search, DOI verification & BibTeX workflow
        │   └── scripts/
        │       └── bib_tool.py               # Zero-dep CLI for Crossref, arXiv, OpenAlex & PubMed APIs
        ├── paper-summarizer/
        │   ├── SKILL.md                      # Deep paper reading, equation/figure analysis & synthesis
        │   └── references/
        │       └── review_rubric.md          # Peer-review & methodological critique checklist
        ├── academic-writing/
        │   ├── SKILL.md                      # LaTeX/Typst/Markdown academic writing & style enforcement
        │   └── scripts/
        │       └── lint_manuscript.py        # Audits .tex/.md/.typ citations against .bib & checks style flaws
        └── scientific-figures-tables/
            ├── SKILL.md                      # Publication figure design & reproducible data-to-table workflow
            └── scripts/
                ├── csv_to_table.py           # Converts CSV/TSV to LaTeX booktabs or Markdown with bold best
                └── pub_style.mplstyle        # Publication-ready Matplotlib style sheet (Okabe-Ito palette)
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

## Cross-Agent Compatibility

| AI Agent / IDE | Rules File Loaded | Skills Directory Loaded | Supported by `install.sh` |
| :--- | :--- | :--- | :--- |
| **Google Antigravity / Gemini CLI** | `AGENTS.md` / `GEMINI.md` | `.agents/skills/` or `~/.gemini/config/skills/` | Yes |
| **Claude Code** | `CLAUDE.md` | `.claude/skills/` or `~/.claude/skills/` | Yes |
| **OpenAI Codex / Jules / Amp** | `AGENTS.md` | `.agents/skills/` | Yes |
| **Cursor** | `AGENTS.md` | `.agents/skills/` | Yes |
| **Windsurf / GitHub Copilot** | `AGENTS.md` | `.agents/skills/` | Yes |

---

## Contributing & License

Contributions of new scientific skills (e.g., statistical hypothesis testing, grant writing, rebuttal drafting, domain-specific bio/physics/ML pipelines) are welcome! Released under the [MIT License](LICENSE).
