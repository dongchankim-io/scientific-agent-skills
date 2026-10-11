---
name: academic-writing
description: >-
  Draft, edit, refine, and lint academic manuscripts in LaTeX (.tex), Typst (.typ),
  or Markdown (.md). Enforces clear academic prose, removes promotional hype/weasel words,
  ensures mathematical and typographic consistency, and audits citation keys against
  references.bib. Use whenever writing or editing paper sections, abstracts, rebuttals,
  or checking manuscript readiness.
---

# Academic Writing & Manuscript Linting Skill

Use this skill when drafting, revising, or auditing scientific manuscripts (`.tex`, `.typ`, `.md`), abstracts, cover letters, or peer-review rebuttals.

---

## 1. Structural & Rhetorical Guidelines by Section

- **Abstract (4-Part Structure)**:
  1. *Context & Gap*: 1–2 sentences defining the domain and why current approaches fall short.
  2. *Proposal*: 1–2 sentences stating what this paper introduces ("We propose/introduce...").
  3. *Results*: 1–2 sentences with concrete quantitative findings across specific benchmarks.
  4. *Impact*: 1 concluding sentence on broader scientific or practical implications.
- **Introduction**:
  - End with a clear, itemized **Summary of Contributions** where every claim is forward-referenced to a specific section, theorem, or table (e.g., `\cref{sec:method}`, `\cref{tab:main}`).
- **Related Work**:
  - Organize by **thematic taxonomy** (e.g., problem setting or mechanism), never as a disconnected laundry list ("X did A. Y did B."). Conclude each paragraph by contrasting how your work differs.
- **Methodology**:
  - Define every symbol upon first use. Keep notation consistent across text, equations, and figures.

---

## 2. Prose Hygiene & De-Fluffing Rules

- **Banned Promotional / AI-Cliche Words**: Remove words like *"groundbreaking"*, *"revolutionary"*, *"novel"* (as a bare adjective without explaining what is new), *"seamlessly"*, *"delve"*, *"tapestry"*, *"testament"*, *"paradigm shift"*, *"meticulously"*.
- **Quantify Comparisons**: Replace vague claims (*"significantly better"*, *"much faster"*, *"vastly superior"*) with specific metrics (*"improves F1 by $4.2\%$ ($p < 0.01$)"*, *"reduces latency by $2.8\times$"*).

---

## 3. LaTeX Typographic Standards

- **Tables**: Always use `\usepackage{booktabs}` with `\toprule`, `\midrule`, and `\bottomrule`. Never use vertical lines (`|`) or `\hline`.
- **Citations & Cross-References**:
  - Precede `\cite{}` / `\citep{}` and `\ref{}` / `\cref{}` with a non-breaking space (`~`), e.g., `Transformer~\cite{vaswani2017attention}`, `as shown in~\cref{fig:overview}`.
- **Math Punctuation**: Equations are part of sentences; punctuate display equations with commas or periods as appropriate.
- **Delimiters**: Use `\left( ... \right)` or `\bigl( ... \bigr)` for tall expressions; use `\text{...}` or `\mathrm{...}` for multi-letter operators and subscripts (e.g., $\mathcal{L}_{\mathrm{train}}$ instead of $\mathcal{L}_{train}$).

---

## 4. Automated Manuscript & Citation Audit

Always run [lint_manuscript.py](./scripts/lint_manuscript.py) after drafting or editing a manuscript:

```bash
python3 .agents/skills/academic-writing/scripts/lint_manuscript.py manuscripts/main.tex --bib references.bib
```

### What `lint_manuscript.py` verifies:
1. **Missing Citations**: Every `\cite{key}`, `\citet{key}`, `\citep{key}`, or `[@key]` in the manuscript exists in `references.bib`.
2. **Uncited Bibliography Entries**: Identifies entries in `references.bib` that are never cited in the manuscript.
3. **Placeholder / TODO Markers**: Flags unresolved `TODO`, `FIXME`, `???`, or `\cite{}` with empty keys.
4. **LaTeX & Prose Hygiene**: Flags banned promotional words, `\hline` / vertical table borders, and unescaped `%` or missing `~` before `\ref`/`\cite`.
