# Playwright Web Automation Demo

A live demo of Playwright browser automation that does exactly what the job asks:

- **Browser automation** with Playwright (real Chromium)
- **Extracting & structuring data** from websites into clean tables
- **Pagination** — walking through multiple pages
- **Login flows** — filling a form and confirming an authenticated session

It runs against public scraping-practice sites (books.toscrape.com,
quotes.toscrape.com), so it's safe and always available. The same patterns
apply to any real website.

Built by **Mubarak Mohamud** · Python · Playwright · Streamlit.

## Run it locally

```bash
pip install -r requirements.txt
python -m playwright install chromium    # one-time browser download (~150 MB)
python -m streamlit run app.py
```

Then open http://localhost:8501.

- **Tab 1 — Pagination + Structured Data:** pick how many pages, scrape a clean
  table of title/price/rating/availability, download as Excel.
- **Tab 2 — JavaScript-Rendered Page:** scrapes a JS-built page that a plain
  `requests` scrape can't see — proving why a real browser (Playwright) is needed.
- **Tab 3 — Login Flow:** fills a login form, submits, and confirms the session.

## Files

| File | Purpose |
|------|---------|
| `scraper.py` | Playwright engine: pagination, JS rendering, login |
| `app.py` | Streamlit dashboard |
| `requirements.txt` | Python deps |
| `packages.txt` | System libs Chromium needs (for cloud hosting) |

## Quick command-line test

```bash
python scraper.py
```
Prints scraped rows and runs the login-flow check.
