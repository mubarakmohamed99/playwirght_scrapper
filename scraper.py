#!/usr/bin/env python3
"""
Playwright Web Automation — core engine
=======================================
Demonstrates the exact skills in the job description:
  • Playwright-based browser automation
  • Extracting and structuring data from websites
  • Handling pagination
  • Handling login flows

It runs against public sandbox sites built for scraping practice
(books.toscrape.com, quotes.toscrape.com) — so it's 100% legal to demo and
always available. The same code patterns apply to any real site.

Author: Mubarak Mohamud
"""

from playwright.sync_api import sync_playwright


# ---------------------------------------------------------------------------
# 1) PAGINATION + STRUCTURED DATA
#    Walk through N catalogue pages and pull clean, structured rows.
# ---------------------------------------------------------------------------
def scrape_catalog(max_pages=3, headless=True, progress=None):
    """Scrape books across paginated pages into structured rows."""
    base = "https://books.toscrape.com/catalogue/page-{}.html"
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        for i in range(1, max_pages + 1):
            page.goto(base.format(i), timeout=30000)
            cards = page.query_selector_all("article.product_pod")
            if not cards:
                break  # ran past the last page
            for c in cards:
                a = c.query_selector("h3 a")
                star = c.query_selector("p.star-rating")
                star_cls = (star.get_attribute("class") or "").replace(
                    "star-rating", "").strip()
                rows.append({
                    "Title": a.get_attribute("title"),
                    "Price": c.query_selector("p.price_color").inner_text(),
                    "Rating": rating_map.get(star_cls, ""),
                    "Availability": c.query_selector(
                        "p.instock.availability").inner_text().strip(),
                })
            if progress:
                progress(i, max_pages, len(rows))
        browser.close()
    return rows


# ---------------------------------------------------------------------------
# 2) JAVASCRIPT-RENDERED PAGES
#    quotes.toscrape.com/js/ builds its content with JavaScript. A plain
#    requests scrape sees nothing; Playwright renders it like a real browser.
# ---------------------------------------------------------------------------
def scrape_js_page(headless=True):
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/js/", timeout=30000)
        page.wait_for_selector(".quote", timeout=10000)
        for q in page.query_selector_all(".quote"):
            rows.append({
                "Quote": q.query_selector(".text").inner_text().strip('“”"'),
                "Author": q.query_selector(".author").inner_text(),
                "Tags": ", ".join(t.inner_text()
                                   for t in q.query_selector_all(".tag")),
            })
        browser.close()
    return rows


# ---------------------------------------------------------------------------
# 3) LOGIN FLOW
#    Fill a login form, submit, and confirm an authenticated session — the
#    pattern for any site that hides data behind a login.
# ---------------------------------------------------------------------------
def demo_login(username="demo", password="demo", headless=True):
    """Returns (logged_in: bool, detail: str)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/login", timeout=30000)
        page.fill("input#username", username)
        page.fill("input#password", password)
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")
        # On this sandbox, a successful session shows a "Logout" link.
        logged_in = page.query_selector("a[href='/logout']") is not None
        detail = ("Session authenticated — 'Logout' link present, so we're in."
                  if logged_in else
                  "Login submitted but no authenticated session detected.")
        browser.close()
    return logged_in, detail


# ---------------------------------------------------------------------------
# Generic helper: scrape any URL the user supplies, pulling a structured
# table of links/headings as a starting point (tuned per-site in real work).
# ---------------------------------------------------------------------------
def scrape_custom(url, headless=True):
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle")
        title = page.title()
        for h in page.query_selector_all("h1, h2, h3"):
            txt = h.inner_text().strip()
            if txt:
                rows.append({"Page": title, "Heading": txt})
        browser.close()
    return rows


if __name__ == "__main__":
    print("Scraping 2 catalogue pages with Playwright...")
    data = scrape_catalog(max_pages=2)
    print(f"Got {len(data)} rows. First: {data[0] if data else 'none'}")
    print("\nLogin flow test:")
    ok, msg = demo_login()
    print(" ", msg)
