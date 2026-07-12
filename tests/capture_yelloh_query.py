"""Capture searchCampings GraphQL query from Yelloh website."""

import json
import sys

from playwright.sync_api import sync_playwright

captured = []
all_ops = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        locale="nl-NL",
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1440, "height": 900},
        extra_http_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
        },
    )
    page = context.new_page()

    def on_request(request):
        if "graphql" not in request.url.lower():
            return
        post = request.post_data
        if not post:
            return
        try:
            payload = json.loads(post)
            query = payload.get("query", "")
            op = payload.get("operationName", "")
            label = op or query[:80].replace("\n", " ")
            all_ops.append(label)
            if "searchCampings" in query:
                captured.append(query)
        except Exception:
            pass

    page.on("request", on_request)

    urls = [
        "https://www.yellohvillage.nl/",
        "https://www.yellohvillage.nl/camping/vergelijker_van_campings",
        "https://www.yellohvillage.fr/camping/comparateur_de_camping",
    ]

    for url in urls:
        print(f"visiting {url}", file=sys.stderr)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
        except Exception as exc:
            print(f"goto error: {exc}", file=sys.stderr)
        page.wait_for_timeout(3000)

        for selector in [
            "#onetrust-accept-btn-handler",
            "button:has-text('Accepteren')",
            "button:has-text('Tout accepter')",
        ]:
            try:
                page.locator(selector).first.click(timeout=2000)
                page.wait_for_timeout(1000)
                break
            except Exception:
                pass

        for selector in [
            "text=Zoeken",
            "text=Rechercher",
            "button:has-text('Zoeken')",
            "button:has-text('Rechercher')",
            "a:has-text('Zoeken')",
            "[class*='search']",
        ]:
            try:
                loc = page.locator(selector).first
                if loc.is_visible(timeout=2000):
                    loc.click(timeout=5000)
                    page.wait_for_timeout(8000)
            except Exception:
                pass

        if captured:
            break

    # Try filling search form if present
    try:
        page.goto(
            "https://www.yellohvillage.nl/",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        page.evaluate(
            """
            () => {
              const forms = document.querySelectorAll('form');
              forms.forEach(f => f.dispatchEvent(new Event('submit', {bubbles:true})));
            }
            """
        )
        page.wait_for_timeout(10000)
    except Exception:
        pass

    browser.close()

print("OPS:", sorted(set(all_ops))[:40], file=sys.stderr)

if captured:
    print(max(captured, key=len))
else:
    print("NO_QUERY", file=sys.stderr)
    sys.exit(1)
