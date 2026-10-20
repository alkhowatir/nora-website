# Phase 1 — Capture audit (internal)

Source: `noraengineers-mirror.zip` (treated as read-only; never modified). The live site was **not** accessed during this work — everything below comes from the capture and its own README / source audit / download log.

## Verdict
**The capture is sufficient for the redesign.** All user-facing content, both languages, the usable imagery, the logo mark and the corporate video are present.

## Available and verified locally
| Item | Status |
|---|---|
| Pages | 6 English + 6 Arabic (Home, About, Services, Projects, Join Us, Contact) with rendered content in `api_dump/pages.json` and static HTML in `site_mirror/` |
| Media library | ~80 items; full-size originals present alongside WordPress thumbnails |
| Project imagery | 8 residential interior renders (also duplicated under a second upload folder), 10 café interior renders |
| Office imagery | 5 photographs of the office (reception/logo wall, meeting rooms, open plan) |
| Branding | Gold "n" mark (transparent PNG, 3543 px). No vector logo, no brand guidelines |
| Video | `Noras-Office.mp4` — 848×480, ~61 s, handheld office walkthrough |
| Metadata | Yoast SEO fields present for pages (titles / descriptions / OG) |
| Forms | Join Us (careers) form structure captured; Contact page has contact details only |
| Environment (detectable) | WordPress, OceanWP theme, Elementor, Yoast SEO, form plugin with honeypot (WPForms-style markup) |

## Missing / uncertain (and why it matters)
- **No project names, clients, locations, dates or descriptions.** Images are unlabeled. The redesign therefore uses neutral captions ("Bedroom — view 1", "Café — evening view") and labels everything as *design visualisation*. **Ask the client** which projects are built, and for names/credits.
- **Images are 3D renders**, not photographs of built work. Café renders are small (≈760–988 px wide), so they are never shown full-bleed.
- **Video is low quality** (480p handheld, audio present, no captions/transcript). It is used as a contained inline player with a photo poster, `preload="none"`. A professional re-shoot would lift the brand most.
- **No statistics, years in business, team, certifications, awards, clients or partners** exist in the content, so none are shown. The "facts" bar uses only derivable values (6 services, 2 project categories, location, working hours).
- **English and Arabic copy disagree** in places: EN says projects cover "residential, commercial, hospitality"; AR says "residential, commercial, industrial" (architecture) and "health" (interiors). EN says "considerable experience"; AR also calls the office "emerging" in one place. The redesign uses the common denominator ("residential, commercial and other") — **client to confirm**.
- **No search, no map embed, no social links** were found in the capture; none were added. Contact page has **no contact form** and the careers form has **no file upload** — the redesign adds both as *proposal improvements* (flagged in BACKEND.md).
- A few capture-log entries are marked failed in `download_log.json`; none are used by the redesign.
- Backend behaviour (form email routing, anti-spam, WordPress admin) is not inspectable and not reproduced.

## Decisions for the redesign
- Original brand colour (bronze) kept as the single accent; palette otherwise new (warm limestone / graphite).
- Arabic slugs replaced with clean ASCII paths (`/ar/about/`), with 301 mapping in `.htaccess`.
- Office name in UI: "Nora AlSaud Architects & Engineers" / "نورة السعود معماريون ومهندسون" (from the capture's titles).
