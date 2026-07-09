# 1st Class Plumbing & Gas LLC — Website

Single-page marketing site for 1st Class Plumbing & Gas LLC, West Columbia, SC.
Zero-dependency static HTML/CSS (one file, no JS, no build step) for maximum speed.

## Live
https://1st-class-plumbing-gas.netlify.app — deployed via Netlify MCP import
(single self-contained index.html; logo is inlined as base64).

## SEO / AIEO
- JSON-LD graph: Plumber (NAP, geo, areaServed, service catalog, sameAs profiles),
  WebSite, FAQPage — mirrors the visible FAQ.
- Canonical, OG/Twitter cards (`img/og.png`), descriptive title/meta.
- `robots.txt` (AI crawlers explicitly allowed), `sitemap.xml`, `llms.txt`.
  These three deploy only when the Netlify site is git-linked ("Import from
  Git" in Netlify UI) since the MCP import ships a single HTML file.

## Content sources
- Business facts (phone, services, license status, 24/7 hours) and review quotes were
  pulled from the company's public Google/Nextdoor/Yelp/BBB listings.
- The Google Maps embed in the Service Area section renders the live Google Business
  Profile card (photo, rating, pin) directly from Google.

## Adding real job photos
Photos from the Google Business Profile couldn't be exported from this build environment.
To add them: download from the GMB dashboard (or ask the owner), drop them in `img/`,
and add `<img>` tags inside the relevant service `.card` elements or a gallery section.

## Deploy
Hosted on Netlify. Any push re-deploys via `netlify.toml` (publish dir = repo root).
