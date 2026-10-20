# Backend integration (forms)

The sample is front-end only. Submitting a valid form shows an explicit **"This is a preview… nothing has been sent"** notice. To connect a server, set `data-endpoint="/api/…"` on the `<form>`; `main.js` will then POST `FormData` and show success / failure messages (strings in the `#i18n` JSON block).

| Form | Page(s) | Endpoint (suggested) | Origin of feature |
|---|---|---|---|
| Careers / application | `/careers/`, `/ar/careers/` | `POST /api/careers` (multipart) | Existing in old site (without file upload) |
| Contact enquiry | `/contact/`, `/ar/contact/` | `POST /api/contact` | **New** — old Contact page had no form |

**Careers fields:** `name*, email*, mobile*, qualification, gender*, nationality*, education*, job_type*, applying_for, portfolio (url), message, cv (file, optional — new)`.
**Contact fields:** `name*, email*, phone, project_type, message*`.
**Both:** hidden honeypot `company_website` (reject if non-empty).

Server requirements: validate and sanitise all input; limit `cv` to PDF/DOC/DOCX ≤ 5 MB and store outside the web root; rate-limit / add CAPTCHA (e.g. Cloudflare Turnstile); send mail via authenticated SMTP to `info@noraengineers.com`; return `2xx` on success. No CORS needed when served from the same origin. On Hostinger a small PHP handler or a headless-CMS form endpoint both work.

**Search:** the original site exposed none, so none was built.
**CMS readiness:** all copy lives in `build.py` dictionaries (EN/AR) and project images in one list — easy to swap for a CMS/JSON source.
