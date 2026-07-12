import re
import requests

headers = {"User-Agent": "Mozilla/5.0"}
base = "https://img.yellohvillage.fr/js/"
main = requests.get(
    base + "app_bottom_desktop.js?9.160.0",
    headers=headers,
    timeout=120,
).text

chunks = set(re.findall(r'["\']([^"\']+\.js[^"\']*)["\']', main))
print("chunks", len(chunks))

needles = [
    "searchCampings",
    "CampingAccommodationDetailFragment",
    "campingContentIds",
]

for chunk in sorted(chunks):
    if ".js" not in chunk:
        continue
    url = chunk if chunk.startswith("http") else base + chunk.lstrip("/")
    try:
        text = requests.get(url, headers=headers, timeout=30).text
    except Exception:
        continue
    for n in needles:
        if n in text:
            print("FOUND", n, "in", url)
            idx = text.index(n)
            start = max(0, idx - 500)
            print(text[start : idx + 10000])
