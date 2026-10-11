# GitHub Copilot Scientific Research Instructions

Always adhere to the protocols in [`AGENTS.md`](../AGENTS.md) and the modular skills in [`skills/`](../skills/):

1. **Citation Integrity**: Never guess or hallucinate BibTeX entries, DOIs, or arXiv IDs. Always run `python3 .agents/skills/literature-search/scripts/bib_tool.py` to verify metadata from Crossref, OpenAlex, arXiv, or PubMed before adding entries to `references.bib`.
2. **Paper Reading & Synthesis**: Follow `.agents/skills/paper-summarizer/SKILL.md` to inspect equations, figures, and ablations, and update `papers/synthesis_matrix.md` when comparing multiple works.
3. **Academic Writing**: Follow `.agents/skills/academic-writing/SKILL.md` (objective prose, no promotional clichés, `booktabs` tables, `\cref{}` cross-references) and validate drafts with `python3 .agents/skills/academic-writing/scripts/lint_manuscript.py`.
4. **Figures & Tables**: Follow `.agents/skills/scientific-figures-tables/SKILL.md` and generate tables from raw CSV/TSV files using `python3 .agents/skills/scientific-figures-tables/scripts/csv_to_table.py`.
