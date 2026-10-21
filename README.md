# Nora AlSaud Architects & Engineers — Website

Official bilingual website for **Nora AlSaud Architects & Engineers** (Khobar, Saudi Arabia), featuring architectural, interior, landscape, furniture, branding, and supervision services.

- **Production URL**: [https://noraengineers.com](https://noraengineers.com)
- **Repository**: [https://github.com/alkhowatir/nora-website](https://github.com/alkhowatir/nora-website)
- **Languages**: Arabic (`/`, RTL) & English (`/en/`, LTR)
- **Architecture**: Zero-runtime-dependency static site with automated Python generator (`build.py`)

---

## Key Features & Design System

- **Bilingual & Native RTL/LTR**: Full structural parity between Arabic and English using CSS logical properties (`margin-inline`, `padding-block`, etc.) and native bidirectional typography.
- **Continuous Seamless Infinite Marquee**: Pure CSS horizontal infinite carousel for selected projects in the *"من أعمالنا / Selected Work"* section, moving from left-to-right on Arabic and right-to-left on English, with pause on hover/focus and `prefers-reduced-motion` support.
- **Light/Dark Mode**: Curated warm-alabaster light mode as the default theme regardless of system preference, with persistent manual dark-mode toggle (`localStorage` cross-tab sync).
- **Self-Hosted Typography**:
  - Latin: *Instrument Serif* + *Manrope*
  - Arabic: *IBM Plex Sans Arabic* (300, 400, 500)
- **Technical SEO & Structured Data**: Complete JSON-LD schema graphs (`ArchitecturalFirm`, `WebSite`, `BreadcrumbList`, `Service`), bidirectional `hreflang` alternate links, `sitemap.xml`, `robots.txt`, and `llms.txt`.
- **Performance**: High-efficiency modern WebP imagery, asynchronous video loading, zero external framework dependencies, and minimal DOM complexity.

---

## Directory Structure

```
.
├── index.html         # Arabic homepage (default root)
├── en/                # English pages (/en/, /en/about/, /en/services/, etc.)
├── about/             # Arabic About page
├── services/          # Arabic Services hub and 6 discipline detail pages
├── projects/          # Arabic Projects portfolio
├── careers/           # Arabic Careers application page
├── contact/           # Arabic Contact page
├── assets/
│   ├── css/main.css   # Single unified design system stylesheet
│   ├── js/main.js     # Vanilla progressive enhancement scripts
│   ├── fonts/         # Self-hosted WOFF2 fonts
│   ├── img/           # Responsive optimized WebP assets
│   └── video/         # Office walkthrough media
├── sitemap.xml        # XML Sitemap with hreflang alternates
├── robots.txt         # Crawler indexing rules
├── llms.txt           # Machine-readable knowledge file for LLMs
├── .htaccess          # Security headers, gzip/brotli caching, and clean URLs
└── README.md          # Project documentation
```

---

## Local Development & Preview

### Preview the Static Site
Serve the repository root directly using Python's built-in HTTP server:

```bash
python -m http.server 8000
```

Then visit:
- Arabic: `http://localhost:8000/`
- English: `http://localhost:8000/en/`

---

## Production Deployment (Hostinger / Apache / Nginx / GitHub Pages)

The repository root is production-ready and can be deployed directly into your web root (e.g., `public_html/` on Hostinger or via Git deployment).
