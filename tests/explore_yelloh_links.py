"""Explore Yelloh site links and trigger search."""

import json
import re
import sys

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(locale="nl-NL")
    captured = []

    def on_request(request):
        if "graphql" not in request.url.lower():
            return
        post = request.post_data
        if not post:
            return
        try:
            payload = json.loads(post)
            q = payload.get("query", "")
            if "searchCampings" in q:
                captured.append(q)
        except Exception:
            pass

    page.on("request", on_request)

    page.goto("https://www.yellohvillage.nl/", wait_until="networkidle", timeout=90000)
    links = page.eval_on_selector_all(
        "a[href]",
        "els => els.map(e => e.href).filter(h => h.includes('yelloh'))",
    )
    search_links = [u for u in links if re.search(r"zoek|search|compar|result", u, re.I)]
    print("SEARCH_LINKS", search_links[:30], file=sys.stderr)

    for url in search_links[:10]:
        if captured:
            break
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)
        except Exception as e:
            print("fail", url, e, file=sys.stderr)

    browser.close()

if captured:
    print(max(captured, key=len))
else:
    print("NO_QUERY", file=sys.stderr)
    sys.exit(1)
