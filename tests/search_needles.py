import re
import requests

headers = {"User-Agent": "Mozilla/5.0"}
text = requests.get(
    "https://img.yellohvillage.fr/js/app_bottom_desktop.js?9.160.0",
    headers=headers,
    timeout=120,
).text

# Find contexts around startDate that look like graphql
for m in re.finditer(r"startDate", text):
    snippet = text[max(0, m.start() - 300) : m.start() + 800]
    if "endDate" in snippet and ("query" in snippet.lower() or "peopleCount" in snippet or "accommodation" in snippet.lower()):
        print("---")
        print(snippet)
        print()

# Also look for concatenated query strings
for m in re.finditer(r'(?:query|fragment)[^\n]{0,20}\+', text):
    print("concat", repr(m.group()[:100]))
