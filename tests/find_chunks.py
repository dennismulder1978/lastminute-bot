import re
import requests

headers = {"User-Agent": "Mozilla/5.0"}
base = "https://img.yellohvillage.fr/js/"
main = requests.get(
    base + "app_main_isolated_desktop.min.js?9.160.0",
    headers=headers,
    timeout=120,
).text

chunks = set(re.findall(r'["\']([^"\']+\.js[^"\']*)["\']', main))
print("chunks", len(chunks))

needles = [
    "searchCampings",
    "CampingAccommodationDetailFragment",
    "CampingRentalTechnicalInformationFragment",
    "CampingSlotTechnicalInformationFragment",
]

for chunk in sorted(chunks):
    if not chunk.endswith(".js") and ".js?" not in chunk:
        continue
    url = chunk if chunk.startswith("http") else base + chunk.lstrip("/")
    try:
        text = requests.get(url, headers=headers, timeout=30).text
    except Exception as exc:
        continue
    for n in needles:
        if n in text:
            print("FOUND", n, "in", url)
            idx = text.index(n)
            # extract full query - look backward for query start and forward for end
            start = text.rfind("query", 0, idx)
            if start == -1:
                start = text.rfind("fragment", 0, idx)
            snippet = text[start : start + 15000]
            print(snippet)
            open("tests/yelloh_query_snippet.txt", "w", encoding="utf-8").write(snippet)
            raise SystemExit(0)

print("not found in chunks")
