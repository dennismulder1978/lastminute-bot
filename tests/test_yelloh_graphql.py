import json
import requests
from datetime import date, timedelta
from pathlib import Path

query_file = Path("app/scrapers/yelloh.py").read_text(encoding="utf-8")
start = query_file.index('SEARCH_QUERY = """') + len('SEARCH_QUERY = """')
end = query_file.index('"""', start)
search_query = query_file[start:end]

headers = {
    "Content-Type": "application/json",
    "gql-locale": "nl",
    "gql-market-site": "1",
    "Origin": "https://www.yellohvillage.nl",
    "Referer": "https://www.yellohvillage.nl/",
    "User-Agent": "Mozilla/5.0",
}
arrival = date(2026, 7, 18)
departure = arrival + timedelta(days=7)
variables = {
    "accommodationType": "rental",
    "peopleCount": 2,
    "startDate": arrival.strftime("%Y-%m-%dT00:00:00.000Z"),
    "endDate": departure.strftime("%Y-%m-%dT00:00:00.000Z"),
    "campingContentIds": [],
    "filters": [],
}
r = requests.post(
    "https://api.sitepriv.prod.yellohvillage.fr/graphql",
    headers=headers,
    json={"query": search_query, "variables": variables},
    timeout=60,
)
print("status", r.status_code)
print(json.dumps(r.json(), indent=2)[:5000])
