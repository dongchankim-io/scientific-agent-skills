#!/usr/bin/env python3
"""Zero-dependency CLI tool for searching scientific literature and fetching verified BibTeX.

Supports Crossref, OpenAlex, arXiv, and PubMed using only the Python standard library.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

USER_AGENT = "ScientificAgentSkills/1.0 (https://github.com/dongchankim-io/scientific-agent-skills)"


def http_get(url: str, accept: str = "application/json") -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def make_cite_key(first_author_family: str, year: str, title: str) -> str:
    author_clean = re.sub(r"[^a-zA-Z]", "", first_author_family or "anon").lower()
    stopwords = {"a", "an", "the", "of", "in", "on", "for", "with", "to", "and", " via ", "by", "from"}
    words = [
        re.sub(r"[^a-zA-Z0-9]", "", w).lower()
        for w in (title or "paper").split()
    ]
    words = [w for w in words if w and w not in stopwords]
    first_word = words[0] if words else "work"
    year_clean = re.sub(r"[^0-9]", "", str(year or "0000"))[:4] or "0000"
    return f"{author_clean}{year_clean}{first_word}"


def append_bibtex(bib_entry: str, bib_file: str) -> None:
    key_match = re.search(r"@\w+\{\s*([^,\s]+)\s*,", bib_entry)
    key = key_match.group(1) if key_match else None

    if os.path.exists(bib_file) and key:
        with open(bib_file, "r", encoding="utf-8") as f:
            existing = f.read()
        if re.search(rf"@\w+\{{\s*{re.escape(key)}\s*,", existing):
            print(f"[bib_tool] Entry '{key}' already exists in {bib_file}; skipping duplicate.", file=sys.stderr)
            return

    with open(bib_file, "a", encoding="utf-8") as f:
        if os.path.exists(bib_file) and os.path.getsize(bib_file) > 0:
            f.write("\n")
        f.write(bib_entry.strip() + "\n")
    print(f"[bib_tool] Appended '{key or 'entry'}' to {bib_file}", file=sys.stderr)


def fetch_doi_bibtex(doi: str) -> str:
    doi_clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip())
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    data = json.loads(http_get(url))["message"]

    title = (data.get("title") or ["Untitled"])[0]
    authors = data.get("author") or []
    author_strs = []
    first_family = "author"
    for idx, a in enumerate(authors):
        family = a.get("family", "")
        given = a.get("given", "")
        if idx == 0 and family:
            first_family = family
        author_strs.append(f"{family}, {given}".strip(", "))

    issued = data.get("issued", {}).get("date-parts", [[None]])[0]
    year = str(issued[0]) if issued and issued[0] else "0000"
    container = (data.get("container-title") or [""])[0]
    work_type = data.get("type", "journal-article")
    bib_type = "inproceedings" if "proceedings" in work_type else "article"
    venue_field = "booktitle" if bib_type == "inproceedings" else "journal"
    key = make_cite_key(first_family, year, title)

    lines = [
        f"@{bib_type}{{{key},",
        f"  title = {{{title}}},",
        f"  author = {{{' and '.join(author_strs) or 'Unknown'}}},",
        f"  year = {{{year}}},",
    ]
    if container:
        lines.append(f"  {venue_field} = {{{container}}},")
    if data.get("volume"):
        lines.append(f"  volume = {{{data['volume']}}},")
    if data.get("issue"):
        lines.append(f"  number = {{{data['issue']}}},")
    if data.get("page"):
        lines.append(f"  pages = {{{data['page']}}},")
    lines.append(f"  doi = {{{doi_clean}}},")
    lines.append(f"  url = {{https://doi.org/{doi_clean}}}")
    lines.append("}")
    return "\n".join(lines)


def fetch_arxiv_bibtex(arxiv_id: str) -> str:
    clean_id = re.sub(r"^arxiv:", "", arxiv_id.strip(), flags=re.IGNORECASE)
    url = f"https://export.arxiv.org/api/query?id_list={urllib.parse.quote(clean_id)}"
    xml_text = http_get(url, accept="application/atom+xml")
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    entry = root.find("atom:entry", ns)
    if entry is None:
        raise ValueError(f"No arXiv entry found for {clean_id}")

    title = re.sub(r"\s+", " ", (entry.findtext("atom:title", "", ns) or "").strip())
    published = (entry.findtext("atom:published", "", ns) or "")[:4] or "0000"
    authors = [
        (a.findtext("atom:name", "", ns) or "").strip()
        for a in entry.findall("atom:author", ns)
    ]
    first_family = authors[0].split()[-1] if authors and authors[0] else "author"
    primary_cat_el = entry.find("arxiv:primary_category", ns)
    primary_cat = primary_cat_el.attrib.get("term", "cs.LG") if primary_cat_el is not None else "cs.LG"
    key = make_cite_key(first_family, published, title)

    return "\n".join([
        f"@article{{{key},",
        f"  title = {{{title}}},",
        f"  author = {{{' and '.join(authors)}}},",
        f"  year = {{{published}}},",
        f"  journal = {{arXiv preprint arXiv:{clean_id}}},",
        f"  eprint = {{{clean_id}}},",
        "  archivePrefix = {arXiv},",
        f"  primaryClass = {{{primary_cat}}},",
        f"  url = {{https://arxiv.org/abs/{clean_id}}}",
        "}",
    ])


def fetch_pmid_bibtex(pmid: str) -> str:
    clean_id = re.sub(r"[^0-9]", "", pmid.strip())
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={clean_id}&retmode=json"
    data = json.loads(http_get(url))
    doc = data.get("result", {}).get(clean_id)
    if not doc:
        raise ValueError(f"No PubMed record found for PMID {clean_id}")

    title = doc.get("title", "Untitled").rstrip(".")
    pubdate = doc.get("pubdate", "0000")
    year_match = re.search(r"\b(19|20)\d{2}\b", pubdate)
    year = year_match.group(0) if year_match else "0000"
    authors = [a.get("name", "") for a in doc.get("authors", []) if a.get("name")]
    first_family = authors[0].split()[0] if authors else "author"
    journal = doc.get("fulljournalname") or doc.get("source") or ""
    doi = ""
    for aid in doc.get("articleids", []):
        if aid.get("idtype") == "doi":
            doi = aid.get("value", "")
            break

    key = make_cite_key(first_family, year, title)
    lines = [
        f"@article{{{key},",
        f"  title = {{{title}}},",
        f"  author = {{{' and '.join(authors)}}},",
        f"  year = {{{year}}},",
    ]
    if journal:
        lines.append(f"  journal = {{{journal}}},")
    if doc.get("volume"):
        lines.append(f"  volume = {{{doc['volume']}}},")
    if doc.get("issue"):
        lines.append(f"  number = {{{doc['issue']}}},")
    if doc.get("pages"):
        lines.append(f"  pages = {{{doc['pages']}}},")
    if doi:
        lines.append(f"  doi = {{{doi}}},")
    lines.append(f"  pmid = {{{clean_id}}},")
    lines.append(f"  url = {{https://pubmed.ncbi.nlm.nih.gov/{clean_id}/}}")
    lines.append("}")
    return "\n".join(lines)


def search_literature(query: str, source: str, limit: int) -> None:
    q = urllib.parse.quote(query)
    results = []

    if source == "crossref":
        url = f"https://api.crossref.org/works?query={q}&rows={limit}"
        items = json.loads(http_get(url)).get("message", {}).get("items", [])
        for it in items:
            title = (it.get("title") or ["Untitled"])[0]
            authors = [a.get("family", "") for a in (it.get("author") or [])[:3] if a.get("family")]
            issued = it.get("issued", {}).get("date-parts", [[None]])[0]
            year = issued[0] if issued else "?"
            venue = (it.get("container-title") or [""])[0]
            results.append({
                "title": title,
                "authors": ", ".join(authors),
                "year": year,
                "venue": venue,
                "doi": it.get("DOI", ""),
            })
    elif source == "openalex":
        url = f"https://api.openalex.org/works?search={q}&per-page={limit}"
        items = json.loads(http_get(url)).get("results", [])
        for it in items:
            authors = [
                a.get("author", {}).get("display_name", "")
                for a in (it.get("authorships") or [])[:3]
            ]
            loc = it.get("primary_location") or {}
            src = loc.get("source") or {}
            results.append({
                "title": it.get("title", "Untitled"),
                "authors": ", ".join(filter(None, authors)),
                "year": it.get("publication_year", "?"),
                "venue": src.get("display_name", ""),
                "cited_by_count": it.get("cited_by_count", 0),
                "doi": (it.get("doi") or "").replace("https://doi.org/", ""),
                "oa_url": (it.get("open_access") or {}).get("oa_url", ""),
            })
    elif source == "arxiv":
        url = f"https://export.arxiv.org/api/query?search_query=all:{q}&max_results={limit}"
        root = ET.fromstring(http_get(url, accept="application/atom+xml"))
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            raw_id = entry.findtext("atom:id", "", ns)
            arxiv_id = raw_id.split("/abs/")[-1] if "/abs/" in raw_id else raw_id
            title = re.sub(r"\s+", " ", (entry.findtext("atom:title", "", ns) or "").strip())
            authors = [
                (a.findtext("atom:name", "", ns) or "").strip()
                for a in entry.findall("atom:author", ns)[:3]
            ]
            year = (entry.findtext("atom:published", "", ns) or "")[:4]
            results.append({
                "title": title,
                "authors": ", ".join(authors),
                "year": year,
                "arxiv_id": arxiv_id,
                "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            })
    elif source == "pubmed":
        esearch = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={q}&retmax={limit}&retmode=json"
        ids = json.loads(http_get(esearch)).get("esearchresult", {}).get("idlist", [])
        if ids:
            id_str = ",".join(ids)
            esum = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={id_str}&retmode=json"
            sum_data = json.loads(http_get(esum)).get("result", {})
            for pid in ids:
                doc = sum_data.get(pid, {})
                authors = [a.get("name", "") for a in (doc.get("authors") or [])[:3]]
                results.append({
                    "title": doc.get("title", "Untitled"),
                    "authors": ", ".join(authors),
                    "year": (doc.get("pubdate") or "")[:4],
                    "venue": doc.get("source", ""),
                    "pmid": pid,
                })

    print(json.dumps(results, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Search literature and fetch verified BibTeX entries.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Search Crossref, OpenAlex, arXiv, or PubMed")
    p_search.add_argument("query", help="Search query string")
    p_search.add_argument("--source", choices=["crossref", "openalex", "arxiv", "pubmed"], default="crossref")
    p_search.add_argument("--limit", type=int, default=5)

    for id_cmd, help_text in [
        ("doi", "Fetch BibTeX for a DOI"),
        ("arxiv", "Fetch BibTeX for an arXiv ID"),
        ("pmid", "Fetch BibTeX for a PubMed ID"),
    ]:
        p = sub.add_parser(id_cmd, help=help_text)
        p.add_argument("identifier", help="Identifier value")
        p.add_argument("--append", metavar="BIB_FILE", help="Append verified BibTeX entry to file")

    args = parser.parse_args()

    if args.cmd == "search":
        search_literature(args.query, args.source, args.limit)
    else:
        if args.cmd == "doi":
            bib = fetch_doi_bibtex(args.identifier)
        elif args.cmd == "arxiv":
            bib = fetch_arxiv_bibtex(args.identifier)
        elif args.cmd == "pmid":
            bib = fetch_pmid_bibtex(args.identifier)
        print(bib)
        if args.append:
            append_bibtex(bib, args.append)


if __name__ == "__main__":
    main()
