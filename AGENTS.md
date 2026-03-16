# Agent Instructions

This is a personal academic website for Richard Lee Davis (Assistant Professor, KTH Royal Institute of Technology, Division of Digital Learning). Built with the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme, hosted on GitHub Pages at https://richarddavis.github.io. Source repo: https://github.com/richarddavis/richarddavis.github.io.

## Site Overview

### Theme & Framework

al-folio is an academic Jekyll theme. Key features enabled on this site:

- Fixed navbar and footer
- Light/dark mode
- Search (posts, socials, bibliography)
- MathJax typesetting
- Publication badges (Altmetric, Dimensions, Google Scholar)
- Responsive images via ImageMagick (WebP, widths: 480/800/1400px)
- Giscus comments
- Masonry layout for projects

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| `_pages/` | Main site pages (about, publications, blog, projects, cv, etc.) |
| `_posts/` | Blog posts (permalink: `/blog/:year/:title/`) |
| `_projects/` | Portfolio projects (categories: "work" and "fun") |
| `_news/` | News announcements shown on homepage |
| `_bibliography/` | `papers.bib` — academic publications rendered via jekyll-scholar |
| `_books/` | Book collection/reviews |
| `_data/` | YAML config: `cv.yml`, `coauthors.yml`, `repositories.yml`, `socials.yml`, `venues.yml` |
| `_layouts/` | Liquid templates (default, about, cv, page, post, bib, book-shelf, etc.) |
| `_includes/` | Reusable components (header, footer, social, figures, resume sections) |
| `_sass/` | SCSS stylesheets (`_base.scss`, `_variables.scss`, `_themes.scss`, etc.) |
| `_plugins/` | Custom Ruby plugins (scholar citations, cache busting, external posts, etc.) |
| `assets/` | Static assets — images, CSS, JS, PDFs, fonts, documents |
| `.github/workflows/` | CI/CD (deploy, Prettier, accessibility, broken links, CodeQL, Lighthouse) |

### Key Pages

- **About** (`_pages/about.md`, permalink: `/`) — Landing page with profile, announcements, latest posts, selected papers.
- **Publications** (`_pages/publications.md`) — Bibliography from `papers.bib` with search.
- **Blog** (`_pages/blog.md`, permalink: `/blog/`) — Paginated (5/page), with tags and categories.
- **Projects** (`_pages/projects.md`) — Grid/horizontal layout, sorted by importance.
- **CV** (`_pages/cv.md`) — Populated from `assets/json/resume.json`.
- **Books** (`_pages/books.md`) — Book shelf layout.

### Configuration

Main config is `_config.yml`. Key settings:
- Site names use `first_name`, `middle_name`, `last_name` fields (title is `blank`).
- Jekyll Scholar: bibliography in `_bibliography/papers.bib`, APA style, max 3 authors displayed.
- Pagination: 5 posts/page, 3 related posts.
- External links open in new tabs with `rel="external nofollow noopener"`.

### Build & Deploy

- **GitHub Actions** (`deploy.yml`): Ruby 3.3.5, Python 3.13, Jekyll build, PurgeCSS, deploy to GitHub Pages.
- **Docker**: `docker-compose.yml` with `amirpourmand/al-folio:v0.14.6`, port 8080 + LiveReload on 35729.
- **Local**: `bundle exec jekyll serve` (or use Docker).

### CI Checks

- **Prettier** (`prettier.yml`) — Code formatting. Config in `.prettierignore`.
- **Accessibility** (`axe.yml`) — Axe-core scanner (manual trigger).
- **Broken links** (`broken-links.yml`, `broken-links-site.yml`) — Link validation.
- **CodeQL** (`codeql.yml`) — Security analysis.
- **Lighthouse** (`lighthouse-badger.yml`) — Performance badges.

---

## Hosting Static Documents

Static HTML pages (e.g., Quarto reports) go in `assets/documents/<name>/`. Jekyll serves these as-is since they have no front matter.

### Adding a new document

1. Create a subdirectory under `assets/documents/` (e.g., `assets/documents/my_report/`).
2. Copy the HTML file as `index.html` and any supporting assets (images, CSS, JS) alongside it.
3. The document will be available at `https://richarddavis.github.io/assets/documents/<name>/`.

### Updating an existing document

1. Re-render the source document (e.g., Quarto report).
2. Copy the updated HTML and assets into the corresponding `assets/documents/<name>/` directory.
3. If the document is password-protected, re-run StatiCrypt (see below).
4. Commit and push.

### Password-protecting a document with StatiCrypt

StatiCrypt encrypts HTML files client-side with AES-256. Visitors see a password prompt; the page decrypts in-browser.

```bash
npm install -g staticrypt  # if not already installed
staticrypt assets/documents/<name>/index.html -p "password" -d assets/documents/<name> --remember 30 -c false --short
```

Key flags:
- `-d` outputs the encrypted file in-place (same directory).
- `--remember 30` adds a "Remember me" checkbox (30-day expiry).
- `-c false` disables the config file.
- `--short` suppresses the short-password warning.

Caveats:
- Only the HTML is encrypted. Supporting assets (images, CSS, JS) in subdirectories are still directly accessible.
- Not suitable for truly sensitive data since encryption is client-side.
- If the unencrypted version was previously pushed, you must rewrite git history (`git reset` + force push) to remove it.

### Prettier

Generated/vendored files under `assets/documents/` are excluded from Prettier checks via `.prettierignore`.
