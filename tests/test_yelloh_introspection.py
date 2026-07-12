import json
import requests

headers = {
    "Content-Type": "application/json",
    "gql-locale": "nl",
    "gql-market-site": "1",
    "Origin": "https://www.yellohvillage.nl",
    "Referer": "https://www.yellohvillage.nl/",
    "User-Agent": "Mozilla/5.0",
}

introspection = """
query IntrospectionQuery {
  __schema {
    types {
      name
      kind
      fields {
        name
      }
    }
  }
}
"""

r = requests.post(
    "https://api.sitepriv.prod.yellohvillage.fr/graphql",
    headers=headers,
    json={"query": introspection},
    timeout=60,
)
print("status", r.status_code)
data = r.json()
print(json.dumps(data, indent=2)[:3000])
