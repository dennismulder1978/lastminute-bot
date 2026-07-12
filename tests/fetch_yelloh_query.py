import json
import re
import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}

r = requests.get("https://www.yellohvillage.nl/", headers=headers, timeout=30)
print("status", r.status_code, "len", len(r.text))

for term in [
    "searchCampings",
    "CampingAccommodationDetailFragment",
    "campingContentIds",
    "graphql",
]:
    print(term, term in r.text)

# Find escaped graphql in scripts
patterns = [
    r'"query"\s*:\s*"((?:\\.|[^"\\])*)"',
    r'query\\n[^"]{50,5000}',
    r'searchCampings\\n',
]
for pat in patterns:
    matches = re.findall(pat, r.text)
    if matches:
        print("pattern", pat, "matches", len(matches))
        for m in matches[:2]:
            s = m if isinstance(m, str) else m[0]
            print(s[:500])

# Save html for inspection
open("tests/yelloh_home.html", "w", encoding="utf-8").write(r.text)

# Download all linked js and search
js_urls = re.findall(r'src="([^"]+\.js[^"]*)"', r.text)
print("js urls", js_urls)
for url in js_urls:
    if not url.startswith("http"):
        url = "https://www.yellohvillage.nl" + url
    if "yellohvillage" not in url and "yelloh" not in url:
        continue
    t = requests.get(url, headers=headers, timeout=120).text
    if "searchCampings" in t or "CampingAccommodation" in t:
        print("FOUND in", url)
        idx = t.find("searchCampings") if "searchCampings" in t else t.find("CampingAccommodation")
        print(t[max(0, idx - 200): idx + 12000])
