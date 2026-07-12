import json
import sys

from playwright.sync_api import sync_playwright

payloads = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(locale="nl-NL")

    def on_request(request):
        if "graphql" not in request.url.lower():
            return
        post = request.post_data
        if post:
            try:
                payloads.append(json.loads(post))
            except Exception:
                payloads.append({"raw": post[:500]})

    page.on("request", on_request)

    page.goto("https://www.yellohvillage.nl/", wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(5000)

    for selector in ["#onetrust-accept-btn-handler", "button:has-text('Accepteren')"]:
        try:
            page.locator(selector).first.click(timeout=2000)
            break
        except Exception:
            pass

    page.wait_for_timeout(10000)
    browser.close()

print(json.dumps(payloads, indent=2)[:8000], file=sys.stderr)
for p in payloads:
    q = p.get("query", "")
    if "searchCampings" in q:
        print(q)
        sys.exit(0)

print("NO searchCampings in", len(payloads), "requests", file=sys.stderr)
