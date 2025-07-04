#!/usr/bin/env python3
"""Generate or update the publications section in assets/json/resume.json
from the entries stored in _bibliography/papers.bib.

Run this script whenever papers.bib changes::

    python _scripts/generate_resume_publications.py

It requires the ``bibtexparser`` Python package (listed in requirements.txt).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

# -----------------------------------------------------------------------------
# Helpers for cleaning / transforming BibTeX fields
# -----------------------------------------------------------------------------

_latex_converter = LatexNodes2Text()


MONTH_MAP = {
    "jan": "01",
    "january": "01",
    "feb": "02",
    "february": "02",
    "mar": "03",
    "march": "03",
    "apr": "04",
    "april": "04",
    "may": "05",
    "jun": "06",
    "june": "06",
    "jul": "07",
    "july": "07",
    "aug": "08",
    "august": "08",
    "sep": "09",
    "september": "09",
    "oct": "10",
    "october": "10",
    "nov": "11",
    "november": "11",
    "dec": "12",
    "december": "12",
}


def _latex_to_plain(text: str | None) -> str:
    """Convert LaTeX-formatted text to plain Unicode using pylatexenc."""

    if not text:
        return ""
    return _latex_converter.latex_to_text(text).strip()


def _month_to_number(month: str | None) -> str | None:
    if not month:
        return None
    month = month.strip().lower()
    if month.isdigit():
        return month.zfill(2)
    return MONTH_MAP.get(month)


# -----------------------------------------------------------------------------
# Conversion logic
# -----------------------------------------------------------------------------

def bib_entry_to_publication(entry: Dict[str, str]) -> Dict[str, str]:
    """Convert a single BibTeX entry to the JSON-Resume publication dict."""
    title = _latex_to_plain(entry.get("title", ""))

    publisher = _latex_to_plain(
        entry.get("journal")
        or entry.get("booktitle")
        or entry.get("publisher", "")
    )

    # Build ISO-like date string
    year = entry.get("year", "").strip()
    month_raw = entry.get("month")
    day_raw = entry.get("day")
    date_str = ""
    if year:
        month_num = _month_to_number(month_raw)
        day_num = day_raw.zfill(2) if day_raw and day_raw.isdigit() else None
        if month_num:
            date_str = f"{year}-{month_num}-{day_num or '01'}"
        else:
            date_str = year  # fall back to year only

    # Best-effort URL discovery
    url = (entry.get("url") or "").strip()
    if not url:
        doi = (entry.get("doi") or "").strip()
        if doi:
            url = f"https://doi.org/{doi}"
        else:
            eprint = (entry.get("eprint") or "").strip()
            if eprint:
                url = f"https://arxiv.org/abs/{eprint}"

    summary = _latex_to_plain(entry.get("abstract", ""))

    publication = {
        "name": title,
        "publisher": publisher,
        "releaseDate": date_str,
        "url": url,
        "summary": summary,
    }

    return publication


# -----------------------------------------------------------------------------
# Main routine
# -----------------------------------------------------------------------------

def generate_publications() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    bib_path = repo_root / "_bibliography" / "papers.bib"
    resume_json_path = repo_root / "assets" / "json" / "resume.json"

    if not bib_path.exists():
        raise FileNotFoundError(f"BibTeX file not found: {bib_path}")

    # Parse BibTeX
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    with bib_path.open(encoding="utf-8") as bib_file:
        bib_database = bibtexparser.load(bib_file, parser=parser)

    # Convert entries → publications
    publications: List[Dict[str, str]] = [
        bib_entry_to_publication(entry) for entry in bib_database.entries
    ]

    # Sort by releaseDate descending (newest first)
    def _date_key(pub: Dict[str, str]):
        date_str: str = pub.get("releaseDate") or ""
        for fmt in ("%Y-%m-%d", "%Y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return datetime.min

    publications.sort(key=_date_key, reverse=True)

    # Load existing resume JSON (if any)
    if resume_json_path.exists():
        with resume_json_path.open(encoding="utf-8") as f:
            resume_data = json.load(f)
    else:
        resume_data = {}

    # Update / overwrite publications section
    resume_data["publications"] = publications

    # Pretty-print JSON with 2-space indent (to match the template style)
    resume_json_path.parent.mkdir(parents=True, exist_ok=True)
    with resume_json_path.open("w", encoding="utf-8") as f:
        json.dump(resume_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(
        f"[generate_resume_publications] Wrote {len(publications)} publication(s) to {resume_json_path}"
    )


if __name__ == "__main__":
    generate_publications()