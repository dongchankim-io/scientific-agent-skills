---
name: literature-search
description: >-
  Search scientific literature across Crossref, arXiv, OpenAlex, and PubMed;
  verify DOIs, arXiv IDs, and PMIDs; and generate or append verified BibTeX entries
  to references.bib without hallucinating citations. Use whenever searching for papers,
  verifying references, resolving DOIs, or building a bibliography.
---

# Literature Search & Verified Citation Workflow

Use this skill whenever the user asks to find papers, verify a citation, look up a DOI/arXiv ID/PMID, or add entries to a `.bib` file.

---

## Core Rule: Zero Unverified Citations

Never write a BibTeX entry from memory alone. Always verify metadata using either:
1. Built-in platform literature tools (if available in your environment), **OR**
2. The bundled zero-dependency CLI script:
   [bib_tool.py](./scripts/bib_tool.py)

---

## Step-by-Step Usage of `bib_tool.py`

### 1. Search by Title, Author, or Keywords
Query Crossref, OpenAlex, arXiv, or PubMed directly from the terminal:

```bash
# Search Crossref (general journal/conference papers with DOIs)
python3 .agents/skills/literature-search/scripts/bib_tool.py search "Attention Is All You Need" --source crossref --limit 5

# Search OpenAlex (includes citation counts and open-access PDF links)
python3 .agents/skills/literature-search/scripts/bib_tool.py search "protein structure prediction" --source openalex --limit 5

# Search arXiv preprints
python3 .agents/skills/literature-search/scripts/bib_tool.py search "direct preference optimization" --source arxiv --limit 5

# Search PubMed biomedical literature
python3 .agents/skills/literature-search/scripts/bib_tool.py search "CRISPR base editing" --source pubmed --limit 5
```

### 2. Fetch Verified BibTeX by Identifier and Append to `references.bib`
Once you identify the exact `DOI`, `arXiv ID`, or `PMID`, fetch its canonical BibTeX entry and append it (with automatic duplicate-key prevention):

```bash
# By DOI (via Crossref content negotiation / API)
python3 .agents/skills/literature-search/scripts/bib_tool.py doi "10.1038/s41586-021-03819-2" --append references.bib

# By arXiv ID
python3 .agents/skills/literature-search/scripts/bib_tool.py arxiv "1706.03762" --append references.bib

# By PubMed ID (PMID)
python3 .agents/skills/literature-search/scripts/bib_tool.py pmid "34265844" --append references.bib
```

---

## Verification Checklist
1. Confirm the fetched paper's **title**, **first author**, and **year** match the intended claim in the manuscript.
2. When a paper exists both as an arXiv preprint and a peer-reviewed conference/journal publication, prefer the **peer-reviewed DOI entry** unless citing a preprint-exclusive version.
3. Check `references.bib` to confirm the citation key is clean (`authorYearKeyword` format) and contains no malformed characters.
