# Managing Publications in this Website

This document explains **how the publications list on this site is generated and kept in sync** with the canonical reference library in Zotero.

> TL;DR — All editing happens in Zotero. Export once, run one copy command, commit & push. The site rebuilds automatically.

---

## 1. Source of truth: Zotero + Better BibTeX

1. Every publication lives in Zotero (attached PDF, metadata, notes, …).
2. The add-on **Better BibTeX** (BBT) provides an _auto-export_ feature:

   - Right-click the Zotero collection → **Export Collection…** → Better BibTeX.
   - **Tick "Keep updated"** so the export file is rewritten whenever items change.
   - Choose a folder on disk, e.g. `~/Documents/papers/`.
   - Tick **"Export Files"** so PDFs are copied into `files/<itemID>/…` next to the `.bib`.

This yields the following layout on your laptop:

```
~/Documents/papers/
├── papers.bib              ← auto-exported
└── files/
    ├── 12345/Some-paper.pdf
    ├── 67890/Other.pdf
    └── …
```

## 2. Moving the artefacts into the web repo

After Zotero finishes exporting you run a single command (copy–paste-safe):

```bash
find ~/Documents/papers/files -name "*.pdf" -type f -exec cp {} \
  ~/Development/richarddavis.github.io/assets/pdf/ \;
```

Then copy the bibliography file itself:

```bash
cp ~/Documents/papers/papers.bib \
   ~/Development/richarddavis.github.io/_bibliography/
```

_(Feel free to automate both steps with a tiny shell script.)_

## 3. Commit & push

```
git add _bibliography/papers.bib assets/pdf/*.pdf
git commit -m "Update publications (auto-export)"
git push
```

GitHub Pages rebuilds and the new entries (and their PDF buttons) appear automatically under `/publications`.

## 4. Optional richness you can add later

The site already renders several custom BibTeX fields; you just drop them into Zotero's **Extra** field using Better BibTeX's `tex.<field>:` syntax. Examples:

| Field                  | Effect on the site                                         |
| ---------------------- | ---------------------------------------------------------- |
| `tex.abbr: CHI`        | Venue badge "CHI" (colour set in `_data/venues.yml`)       |
| `tex.pdf:`             | Relative PDF filename (set automatically by the AT script) |
| `tex.slides:`          | Button linking to slides                                   |
| `tex.code:`            | Button linking to source code repo                         |
| `tex.preview:`         | Thumbnail/GIF next to citation                             |
| `tex.additional_info:` | Inline note (e.g. _Best Paper Award_)                      |

See `docs/publications-goodies.md` for the full cheat-sheet.

## 5. Known limits / future work

- **Git LFS not used** — PDFs are small (< 20 MB) so plain Git is fine. If the repo size balloons past ~1 GB we can migrate `assets/pdf` to LFS and add a build step.
- **Preview images** — Planned: store in `assets/img/publication_preview/` and add `tex.preview:` accordingly.
- **Video embeds** — Enable `enable_video_embedding: true` in `_config.yml` and add `tex.video:` fields.

---

_Last updated: 2025-07-03_
