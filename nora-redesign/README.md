# Nora AlSaud Architects & Engineers — redesign sample (local only)

## Preview
```
cd site && python3 -m http.server 8000     # then open http://localhost:8000/  and  /ar/
```
(Root-relative URLs: serve `site/` as the web root; double-clicking the HTML files will not load assets.)

## Layout
- `site/` — deployable static output (EN at `/`, AR at `/ar/`), `.htaccess`, `sitemap.xml`, `robots.txt`, `llms.txt`
- `build.py` — generator (all copy EN/AR, templates, JSON-LD, sitemap). Run `python3 build.py` to regenerate
- `tools/process_assets.py` — derives optimised WebP/favicons from the capture (read-only source path inside)
- `docs/AUDIT.md` — Phase 1 capture audit · `docs/BACKEND.md` — form/back-end requirements

## Design system
Glass surfaces (`.glass`), architectural hairline grid, bronze accent. Instrument Serif + Manrope (EN), IBM Plex Sans Arabic (AR), all self-hosted. Light/dark via `data-theme` set in `<head>` before first paint, persisted in `localStorage('nora-theme')`, defaults to system preference. All layout uses logical properties, so RTL is native.

## Notes
- Canonicals/hreflang/schema point to `https://noraengineers.com` (production origin); change `BASE` in `build.py` if the domain differs.
- Nothing was published, deployed, pushed or sent. The original capture was not modified.
