import requests

url = (
    "https://www.centerparcs.nl/nl-nl/belgie/"
    "fp_VM_vakantiepark-de-vossemeren/cottages"
)

params = {
    "market": "nl",
    "language": "nl",
    "facet[DATE]": "2026-07-17",
    "facet[DATEEND]": "2026-07-24",
    "facet[MULTIPARTICIPANTS][0][adult]": "2",
    "facet[MULTIPARTICIPANTS][0][ages][]": ["11", "14"],
}

headers = {
    "User-Agent": "Mozilla/5.0",
}

response = requests.get(url, params=params, headers=headers)

print(response.status_code)
print(response.url)
print(response.text[:3000])