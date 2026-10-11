#!/usr/bin/env python3
"""Zero-dependency CLI to convert CSV/TSV experimental results into LaTeX booktabs or Markdown tables.

Features:
- Automatic detection of numeric values (including 'mean +/- std' or '84.2 ± 0.3' strings).
- Automatic bolding of the best value and underlining of the second-best value per column
  (--highlight-max for higher-is-better metrics, --highlight-min for lower-is-better metrics).
"""

import argparse
import csv
import re
import sys
from typing import Dict, List, Optional, Set, Tuple

NUM_RE = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)\s*(?:(?:\+/-|±|\\pm)\s*([+-]?\d+(?:\.\d+)?))?\s*$")


def parse_numeric(cell: str) -> Optional[float]:
    m = NUM_RE.match(cell or "")
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def format_cell_latex(cell: str, is_best: bool, is_second: bool) -> str:
    formatted = re.sub(r"\+/-|±", r"$\\pm$", cell.strip())
    if is_best:
        return f"\\textbf{{{formatted}}}"
    if is_second:
        return f"\\underline{{{formatted}}}"
    return formatted


def format_cell_md(cell: str, is_best: bool, is_second: bool) -> str:
    formatted = re.sub(r"\+/-", "±", cell.strip())
    if is_best:
        return f"**{formatted}**"
    if is_second:
        return f"<u>{formatted}</u>"
    return formatted


def compute_ranks(
    rows: List[List[str]],
    headers: List[str],
    max_cols: Set[str],
    min_cols: Set[str],
) -> Dict[Tuple[int, int], str]:
    ranks: Dict[Tuple[int, int], str] = {}
    for col_idx, col_name in enumerate(headers):
        if col_name not in max_cols and col_name not in min_cols:
            continue
        reverse = col_name in max_cols
        vals: List[Tuple[float, int]] = []
        for row_idx, row in enumerate(rows):
            if col_idx < len(row):
                val = parse_numeric(row[col_idx])
                if val is not None:
                    vals.append((val, row_idx))
        if not vals:
            continue
        unique_sorted = sorted({v for v, _ in vals}, reverse=reverse)
        best_val = unique_sorted[0]
        second_val = unique_sorted[1] if len(unique_sorted) > 1 else None
        for val, row_idx in vals:
            if val == best_val:
                ranks[(row_idx, col_idx)] = "best"
            elif second_val is not None and val == second_val:
                ranks[(row_idx, col_idx)] = "second"
    return ranks


def to_latex(
    headers: List[str],
    rows: List[List[str]],
    ranks: Dict[Tuple[int, int], str],
    caption: str,
    label: str,
) -> str:
    col_spec = "l" + "c" * (len(headers) - 1)
    lines = [
        r"\begin{table}[t]",
        r"  \centering",
        f"  \\caption{{{caption}}}",
        f"  \\label{{{label}}}",
        f"  \\begin{{tabular}}{{{col_spec}}}",
        r"    \toprule",
        "    " + " & ".join(f"\\textbf{{{h}}}" for h in headers) + r" \\",
        r"    \midrule",
    ]
    for r_idx, row in enumerate(rows):
        cells = []
        for c_idx in range(len(headers)):
            raw = row[c_idx] if c_idx < len(row) else ""
            rk = ranks.get((r_idx, c_idx), "")
            cells.append(format_cell_latex(raw, rk == "best", rk == "second"))
        lines.append("    " + " & ".join(cells) + r" \\")
    lines.extend([
        r"    \bottomrule",
        r"  \end{tabular}",
        r"\end{table}",
    ])
    return "\n".join(lines)


def to_markdown(
    headers: List[str],
    rows: List[List[str]],
    ranks: Dict[Tuple[int, int], str],
) -> str:
    sep = [":---"] + [":---:"] * (len(headers) - 1)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for r_idx, row in enumerate(rows):
        cells = []
        for c_idx in range(len(headers)):
            raw = row[c_idx] if c_idx < len(row) else ""
            rk = ranks.get((r_idx, c_idx), "")
            cells.append(format_cell_md(raw, rk == "best", rk == "second"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert CSV/TSV into LaTeX booktabs or Markdown table.")
    parser.add_argument("input_file", help="Path to CSV or TSV file")
    parser.add_argument("--format", choices=["latex", "markdown"], default="latex")
    parser.add_argument("--caption", default="Experimental results.")
    parser.add_argument("--label", default="tab:results")
    parser.add_argument("--highlight-max", default="", help="Comma-separated column names where higher is better")
    parser.add_argument("--highlight-min", default="", help="Comma-separated column names where lower is better")
    args = parser.parse_args()

    delimiter = "\t" if args.input_file.endswith(".tsv") else ","
    with open(args.input_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f, delimiter=delimiter))

    if not reader:
        print("Error: Empty input file.", file=sys.stderr)
        sys.exit(1)

    headers = [h.strip() for h in reader[0]]
    rows = [r for r in reader[1:] if any(c.strip() for c in r)]

    max_cols = {c.strip() for c in args.highlight_max.split(",") if c.strip()}
    min_cols = {c.strip() for c in args.highlight_min.split(",") if c.strip()}
    ranks = compute_ranks(rows, headers, max_cols, min_cols)

    if args.format == "latex":
        print(to_latex(headers, rows, ranks, args.caption, args.label))
    else:
        print(to_markdown(headers, rows, ranks))


if __name__ == "__main__":
    main()
