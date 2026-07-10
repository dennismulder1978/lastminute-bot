from pprint import pprint
import requests

from app.config.config_loader import load_config


URL_SITES = (
    "https://www.allcamps.nl/api/twenty/v2/allcamps/nl/search/sites"
)
URL_ACCOMMODATIONS = (
    "https://www.allcamps.nl/api/twenty/v2/allcamps/nl/search/accommodations"
)

def main():
    config = load_config()

    arrival = config["trip"]["departure_dates"][0]

    payload = {
        "filters": {
            "site": {
                "facilities": [],
                "countries": [],
                "areas": [],
                "funnels": [],
                "reviewScores": [],
            },
            "accommodation": {
                "categories": [],
                "bedrooms": [],
                "bathrooms": [],
            },
        },
        "parameters": {
            "includeTopFacilities": True,
            "product": None,
            "funnel": "camping",
            "date": arrival.isoformat(),
            "duration": config["trip"]["nights"],
            "country": None,
            "area": None,
            "recentlySeenSiteDomainId": None,
            "persons": {
                "adults": config["family"]["adults"],
                "children": [
                    {"age": age}
                    for age in config["family"]["children"]
                ],
            },
            "site": None,
            "filter": None,
        },
        "meta": {
            "limit": 10,
            "order": "desc",
            "orderBy": "popular",
            "orderSettingsLabel": "popular-desc",
            "page": 1,
        },
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.allcamps.nl",
        "Referer": (
            "https://www.allcamps.nl/zoek-en-boek"
            f"?date={arrival.isoformat()}"
            f"&duration={config['trip']['nights']}"
            f"&adults={config['family']['adults']}"
        ),
        "User-Agent": (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:152.0) "
            "Gecko/20100101 Firefox/152.0"
        ),
    }

    response = requests.post(
        URL_SITES,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print("=" * 80)
    print("STATUS:", response.status_code)
    print("=" * 80)
    result = response.json()
    sites = result["data"]["sites"]

    site = sites[0]
    pprint(site)
    # if accommodations:
    #     from pprint import pprint
    #
    #     pprint(accommodations[0], width=140, sort_dicts=False)
    #     raise SystemExit

    # for key in sorted(site.keys()):
    #     if key in ("meta", "description"):
    #         print(f"\n=== {key} ===")
    #         pprint(site[key])
    #
    # pprint(site["location"])

    payload2 = {
        "filters": {
            "site": {
                "facilities": [],
                "countries": [],
                "areas": [],
                "funnels": [],
                "reviewScores": [],
            },
            "accommodation": {
                "categories": [],
                "bedrooms": [],
                "bathrooms": [],
            },
        },
        "parameters": {
            "includeTopFacilities": True,
            "product": None,
            "funnel": "camping",
            "date": arrival.isoformat(),
            "duration": config["trip"]["nights"],
            "country": None,
            "area": None,
            "recentlySeenSiteDomainId": None,
            "persons": {
                "adults": config["family"]["adults"],
                "children": [
                    {"age": age}
                    for age in config["family"]["children"]
                ],
            },
            "site": site["slug"],
            "filter": None,
        },
        "meta": {
            "limit": 10,
            "order": "desc",
            "orderBy": "popular",
            "orderSettingsLabel": "popular-desc",
            "page": 1,
        },
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.allcamps.nl",
        "Referer": (
            "https://www.allcamps.nl/zoek-en-boek"
            f"?date={arrival.isoformat()}"
            f"&duration={config['trip']['nights']}"
            f"&adults={config['family']['adults']}"
        ),
        "User-Agent": (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:152.0) "
            "Gecko/20100101 Firefox/152.0"
        ),
    }

    response2 = requests.post(
        URL_ACCOMMODATIONS,
        headers=headers,
        json=payload2,
        timeout=30,
    )


    print(response2.status_code)

    result2 = response2.json()
    pprint(result2)





if __name__ == "__main__":
    main()