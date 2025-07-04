#!/usr/bin/env python3
"""generate_previews.py

Generate placeholder thumbnail images (first page PNG) for every BibTeX entry in
`_bibliography/papers.bib` that is missing a `preview` field.

For each qualifying entry the script will:
1. Locate the associated PDF file (using the `pdf` field first, otherwise the
   filename portion of the `file` field).
2. Convert the first page of that PDF to a PNG named
      "<entry_id>_preview.png".
3. Save the image to `assets/img/publication_preview/`.
4. Insert `preview = {<entry_id>_preview.png}` into the BibTeX entry.

The script is designed to be idempotent: running it multiple times will only
act on entries that still lack a preview image and will *not* regenerate images
that already exist.

Dependencies
------------
• Python ≥ 3.8
• `bibtexparser` for BibTeX I/O
• `pdf2image`  (and the Poppler tool-chain) for PDF→PNG conversion
• `Pillow` (pulled in automatically by `pdf2image`)

Install example (inside your virtualenv):

    pip install bibtexparser pdf2image pillow
    brew install poppler  # macOS

Usage
-----
    python bin/generate_previews.py [options]

Run with `-h` to see all CLI switches.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from pdf2image import convert_from_path

# ---------------------------------------------------------------------------
# Configuration defaults
# ---------------------------------------------------------------------------
DEFAULT_BIB_PATH = Path("_bibliography/papers.bib")
DEFAULT_PDF_DIRS: List[Path] = [
    Path("assets/pdf"),           # primary location in the repo
    Path("."),                   # fallback: root of repo (rare)
]
DEFAULT_PREVIEW_DIR = Path("assets/img/publication_preview")

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def locate_pdf(filename: str, search_dirs: List[Path]) -> Optional[Path]:
    """Return the path to the first existing PDF that matches *filename*.

    The *filename* may contain directory components (e.g. "files/123/foo.pdf").
    In that case we treat the right-most component as the actual file name.
    """
    # Normalise path and take basename only (strip any container dirs)
    candidate_name = Path(filename).name

    # 1. If filename is an absolute or relative path that already exists, use it
    p = Path(filename)
    if p.is_file():
        return p.resolve()

    # 2. Search within provided directories
    for d in search_dirs:
        candidate = d / candidate_name
        if candidate.is_file():
            return candidate.resolve()

    return None  # not found


def pdf_to_png_first_page(pdf_path: Path, out_path: Path, dpi: int = 150, poppler_path: Optional[str] = None) -> None:
    """Convert only the first page of *pdf_path* to *out_path* (PNG)."""
    logger.debug("Converting %s → %s", pdf_path, out_path)
    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        first_page=1,
        last_page=1,
        fmt="png",
        poppler_path=poppler_path,
    )
    if not images:
        raise RuntimeError(f"Failed to convert PDF (no pages returned): {pdf_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(out_path, "PNG")


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def generate_previews(
    bib_path: Path = DEFAULT_BIB_PATH,
    pdf_dirs: List[Path] = DEFAULT_PDF_DIRS,
    preview_dir: Path = DEFAULT_PREVIEW_DIR,
    dpi: int = 150,
    poppler_path: Optional[str] = None,
    overwrite_existing_image: bool = False,
) -> None:
    """Main routine that reads *bib_path* and updates it in-place."""

    if not bib_path.is_file():
        raise FileNotFoundError(f"BibTeX file not found: {bib_path}")

    logger.info("Loading %s", bib_path)
    with bib_path.open(encoding="utf-8") as fh:
        bib_db = bibtexparser.load(fh)

    # Track whether we changed anything so we only rewrite when necessary.
    modified = False

    for entry in bib_db.entries:
        entry_id = entry.get("ID")
        if not entry_id:
            logger.warning("Encountered BibTeX entry with no ID; skipping: %s", entry)
            continue

        if "preview" in entry:
            logger.debug("%s already has a preview; skipping", entry_id)
            continue  # respect existing previews

        # Locate a PDF for this entry
        pdf_field = entry.get("pdf")
        file_field = entry.get("file")

        pdf_path: Optional[Path] = None
        if pdf_field:
            pdf_path = locate_pdf(pdf_field, pdf_dirs)
        if not pdf_path and file_field:
            pdf_path = locate_pdf(file_field, pdf_dirs)

        if not pdf_path:
            logger.warning("%s: No PDF found (pdf/file fields were %s / %s)", entry_id, pdf_field, file_field)
            continue  # cannot generate preview

        # Determine output image path
        preview_filename = f"{entry_id}_preview.png"
        preview_path = preview_dir / preview_filename

        if preview_path.exists() and not overwrite_existing_image:
            logger.debug("%s: Preview image already exists; linking without regeneration", entry_id)
        else:
            try:
                pdf_to_png_first_page(pdf_path, preview_path, dpi=dpi, poppler_path=poppler_path)
                logger.info("%s: Generated preview %s", entry_id, preview_filename)
            except Exception as exc:  # noqa: BLE001
                logger.error("%s: Failed to generate preview: %s", entry_id, exc)
                continue  # Leave entry unchanged

        # Update BibTeX entry
        entry["preview"] = preview_filename
        modified = True

    # Write back to disk only if something changed
    if modified:
        writer = BibTexWriter()
        writer.order_entries_by = None  # preserve original ordering as much as possible
        writer.indent = "    "  # 4-space indent to be close to original style

        logger.info("Writing updated BibTeX to %s", bib_path)
        with bib_path.open("w", encoding="utf-8") as fh:
            bibtexparser.dump(bib_db, fh, writer=writer)
    else:
        logger.info("No changes made – all entries already have previews.")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate placeholder preview images for BibTeX entries.")
    p.add_argument("--bib", "-b", type=Path, default=DEFAULT_BIB_PATH, help="Path to the BibTeX file to process.")
    p.add_argument("--pdf-dirs", "-p", type=Path, nargs="*", default=DEFAULT_PDF_DIRS, help="Directories to search for PDFs (first match wins).")
    p.add_argument("--preview-dir", "-o", type=Path, default=DEFAULT_PREVIEW_DIR, help="Output directory for generated PNG previews.")
    p.add_argument("--dpi", type=int, default=150, help="DPI to use when rasterising PDFs.")
    p.add_argument("--poppler-path", type=str, default=None, help="Path to the Poppler binaries (if not in $PATH).")
    p.add_argument("--overwrite", action="store_true", help="Re-create preview images even if they already exist.")
    p.add_argument("--verbose", "-v", action="count", default=0, help="Increase verbosity (can be passed multiple times).")
    return p


def configure_logging(verbosity_level: int) -> None:
    level = logging.WARNING  # default
    if verbosity_level == 1:
        level = logging.INFO
    elif verbosity_level >= 2:
        level = logging.DEBUG

    logging.basicConfig(format="%(levelname)s: %(message)s", level=level)


def main(argv: List[str] | None = None) -> None:  # pragma: no cover
    args = build_arg_parser().parse_args(argv)
    configure_logging(args.verbose)

    try:
        generate_previews(
            bib_path=args.bib,
            pdf_dirs=list(args.pdf_dirs),
            preview_dir=args.preview_dir,
            dpi=args.dpi,
            poppler_path=args.poppler_path,
            overwrite_existing_image=args.overwrite,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main() 