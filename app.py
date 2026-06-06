#!/usr/bin/env python3
"""
Playwright Web Automation — Streamlit Dashboard
===============================================
A clickable demo of the four skills the job asks for:
  Playwright automation · structured data extraction · pagination · login flows.

Run locally:
    python -m streamlit run app.py

Author: Mubarak Mohamud
"""

import io
import subprocess
import sys

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Playwright Scraper — Mubarak Mohamud",
                   page_icon="🎭", layout="wide")


@st.cache_resource
def _ensure_chromium():
    """On a fresh host (e.g. Streamlit Cloud) the Chromium binary isn't there.
    Install it once on first boot. Cached so it only runs a single time."""
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"],
                       check=False, capture_output=True)
    except Exception:
        pass
    return True


_ensure_chromium()

import scraper  # noqa: E402  (import after browser bootstrap)

st.title("🎭 Playwright Web Automation Demo")
st.caption("Browser automation · structured data extraction · pagination · "
           "login flows  •  Built by **Mubarak Mohamud**")

st.info("This runs a real Chromium browser via Playwright against public "
        "scraping-practice sites (books.toscrape.com, quotes.toscrape.com). "
        "The same patterns apply to any real website.")


def to_excel(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xl:
        df.to_excel(xl, index=False, sheet_name="Data")
    return buf.getvalue()


tab1, tab2, tab3 = st.tabs([
    "📚 Pagination + Structured Data",
    "⚙️ JavaScript-Rendered Page",
    "🔐 Login Flow",
])

# ---- Tab 1: pagination + structured extraction ----
with tab1:
    st.subheader("Scrape multiple pages into a clean table")
    st.write("Walks through catalogue pages with Playwright and extracts "
             "structured rows (title, price, rating, availability).")
    pages = st.slider("How many pages to scrape", 1, 10, 3)
    if st.button("▶️ Run paginated scrape", type="primary"):
        bar = st.progress(0.0, text="Launching browser…")

        def prog(i, total, n):
            bar.progress(i / total, text=f"Page {i}/{total} — {n} items so far")

        with st.spinner("Scraping with Playwright…"):
            try:
                rows = scraper.scrape_catalog(max_pages=pages, progress=prog)
                bar.empty()
                df = pd.DataFrame(rows)
                st.success(f"Scraped {len(df)} products across {pages} page(s).")
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Excel", to_excel(df),
                                   "books.xlsx", use_container_width=True)
            except Exception as e:
                bar.empty()
                st.error(f"Run failed: {e}\n\nIf this says the browser is "
                         f"missing, run:  python -m playwright install chromium")

# ---- Tab 2: JS-rendered ----
with tab2:
    st.subheader("Scrape a page that builds itself with JavaScript")
    st.write("`quotes.toscrape.com/js/` renders content via JS — a plain "
             "`requests` scrape sees an empty page. Playwright renders it like "
             "a real browser, so the data is there.")
    if st.button("▶️ Scrape the JS page", type="primary"):
        with st.spinner("Rendering with Playwright…"):
            try:
                df = pd.DataFrame(scraper.scrape_js_page())
                st.success(f"Extracted {len(df)} quotes from the JS-rendered page.")
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.download_button("⬇️ Download Excel", to_excel(df),
                                   "quotes.xlsx", use_container_width=True)
            except Exception as e:
                st.error(f"Run failed: {e}")

# ---- Tab 3: login flow ----
with tab3:
    st.subheader("Handle a login form and confirm the session")
    st.write("Fills a login form, submits it, and verifies we reached an "
             "authenticated state — the pattern for any site that hides data "
             "behind a login. (This sandbox accepts any username/password.)")
    c1, c2 = st.columns(2)
    user = c1.text_input("Username", value="demo")
    pw = c2.text_input("Password", value="demo", type="password")
    if st.button("🔐 Run login flow", type="primary"):
        with st.spinner("Logging in with Playwright…"):
            try:
                ok, msg = scraper.demo_login(user, pw)
                (st.success if ok else st.warning)(msg)
            except Exception as e:
                st.error(f"Run failed: {e}")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.85em;'>"
    "Playwright Web Automation — browser automation & data extraction<br>"
    "Built by <b>Mubarak Mohamud</b> · Python · Playwright · Streamlit · "
    "<a href='https://github.com/mubarakmohamed99'>github.com/mubarakmohamed99</a>"
    "</div>", unsafe_allow_html=True)
