---
name: scientific-figures-tables
description: >-
  Generate publication-grade scientific figures and convert experimental CSV/TSV/JSON
  data into reproducible LaTeX booktabs or Markdown tables with automatic best/second-best
  highlighting. Use whenever creating plots, formatting benchmark tables, or designing
  data visualizations for a paper.
---

# Reproducible Scientific Figures & Tables Skill

Use this skill whenever generating charts/figures or formatting quantitative tables for a scientific paper.

---

## 1. Publication-Grade Figure Standards

1. **Use the Bundled Matplotlib Style Sheet**:
   When writing Python plotting scripts, load [pub_style.mplstyle](./scripts/pub_style.mplstyle):
   ```python
   import matplotlib.pyplot as plt
   plt.style.use(".agents/skills/scientific-figures-tables/scripts/pub_style.mplstyle")
   ```
2. **Colorblind-Safe Palette (Okabe-Ito)**:
   - Use the Okabe-Ito palette (`#0072B2`, `#D55E00`, `#009E73`, `#CC79A7`, `#F0E442`, `#56B4E9`, `#E69F00`, `#000000`) and pair colors with distinct line styles (`-`, `--`, `-.`, `:`) or marker shapes (`o`, `s`, `^`, `D`) so figures remain legible in grayscale print.
3. **Sizing & Export**:
   - Single-column width: `3.5 in` (`89 mm`); Double-column width: `7.0 in` (`178 mm`).
   - Always export both a **vector PDF** (`fig.savefig("figures/fig1.pdf")`) for LaTeX inclusion and a **300 DPI PNG** (`fig.savefig("figures/fig1.png", dpi=300)`) for quick previewing.
   - Always include error bars / confidence bands (`plt.fill_between` or `plt.errorbar`) and physical units on axis labels.

---

## 2. Automated Data-to-Table Pipeline (`csv_to_table.py`)

Never hand-copy numbers from logs into LaTeX tables. Store experimental results in a structured `.csv` or `.tsv` file and run [csv_to_table.py](./scripts/csv_to_table.py) to generate publication-ready LaTeX `booktabs` or Markdown tables:

```bash
# Generate a LaTeX booktabs table with bold best & underlined second-best values
python3 .agents/skills/scientific-figures-tables/scripts/csv_to_table.py results.csv \
  --format latex \
  --caption "Comparison on main benchmarks (mean $\pm$ std over 5 seeds)." \
  --label "tab:main_results" \
  --highlight-max "Accuracy,F1" \
  --highlight-min "RMSE,Latency"

# Generate a clean Markdown table for notes or READMEs
python3 .agents/skills/scientific-figures-tables/scripts/csv_to_table.py results.csv \
  --format markdown \
  --highlight-max "Accuracy,F1" \
  --highlight-min "RMSE,Latency"
```
