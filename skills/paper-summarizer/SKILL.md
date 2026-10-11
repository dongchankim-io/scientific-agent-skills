---
name: paper-summarizer
description: >-
  Read, analyze, critique, and synthesize scientific papers from PDFs, preprints,
  or full text. Produces structured technical reading notes, methodological critiques,
  and multi-paper synthesis matrices. Use whenever summarizing a paper, reviewing a
  manuscript, extracting experimental results, or comparing multiple papers.
---

# Scientific Paper Reading, Critique & Synthesis Skill

Use this skill when the user provides a scientific paper (PDF path, arXiv ID, DOI, or URL) and asks for a summary, deep dive, peer review, or multi-paper comparison.

---

## Step 1: Retrieve Full Metadata & Read Beyond the Abstract

1. Verify the paper's bibliographic record and add it to `references.bib` using `literature-search` (`bib_tool.py`).
2. Read the **full document** (including methodology equations, main result tables, ablation studies, and limitation sections). If reading a PDF, inspect the figures and tables directly.

---

## Step 2: Generate a Structured Reading Note

Save individual paper notes to `papers/notes/<citekey>.md` following `templates/paper_note_template.md`:

1. **Citation Header**: Full title, authors, venue/year, persistent identifiers (`DOI` / `arXiv ID`), and code/dataset links.
2. **TL;DR (2–3 sentences)**:
   - Sentence 1: The specific bottleneck or open question addressed.
   - Sentence 2: The core technical mechanism, theorem, or experimental design introduced.
   - Sentence 3: The primary quantitative result (with numbers and benchmark names).
3. **Core Contributions**: 3–5 bullet points isolating what is genuinely new vs. inherited from prior work.
4. **Methodology & Formulation**:
   - Explicitly write out the core objective function, algorithm steps, or experimental protocol using LaTeX math (`$...$` / `$$...$$`).
   - State key theoretical or modeling assumptions.
5. **Empirical Results & Ablations**:
   - Summarize primary benchmark comparisons in a clean Markdown table.
   - Highlight which component drove the largest performance gain in the ablation study.
6. **Methodological Critique & Limitations**:
   - Consult [review_rubric.md](./references/review_rubric.md) to evaluate internal/external validity, baseline fairness, statistical significance, and reproducibility.

---

## Step 3: Update the Multi-Paper Synthesis Matrix

Whenever summarizing 2 or more related papers (or conducting a literature review):
1. Open `papers/synthesis_matrix.md` (initialize from `templates/synthesis_matrix.md` if missing).
2. Add a row for each paper with its `@citekey`, problem formulation, core method, datasets/scale, headline metric, and primary limitation.
3. Group the literature into a coherent taxonomy (by mechanism or assumption) rather than listing papers chronologically as "Author A did X. Author B did Y."
