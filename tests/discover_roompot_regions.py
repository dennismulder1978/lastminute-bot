import json
from datetime import timedelta

from app.config.config_loader import load_config
from app.scrapers.roompot import RoompotScraper


def main():
    config = load_config()
    scraper = RoompotScraper(config)

    adults = config["family"]["adults"]
    children = config["family"]["children"]

    arrival = config["trip"]["departure_dates"][0]
    departure = arrival + timedelta(days=config["trip"]["nights"])

    data = {
        "arrivalDate": arrival.strftime("%d-%m-%Y"),
        "departureDate": departure.strftime("%d-%m-%Y"),
        "parkInfoLevel": 0,
        "promotedProductId": "{3F1C8CB8-055E-4AA7-8F36-489E9A3B9A30}",
        "campaignInventoryEnabled": "false",
        "stayType": 968,
        "searchType": 1,
        "paginationOffset": 0,
        "travelGroup[0][Id]": "18-120",
        "travelGroup[0][Amount]": adults,
        "travelGroup[1][Id]": "3-17",
        "travelGroup[1][Amount]": len(children),
        "travelGroup[2][Id]": "0-2",
        "travelGroup[2][Amount]": 0,
        "travelGroup[3][Id]": "pets",
        "travelGroup[3][Amount]": 0,
        "travelGroupCombiEnabled": "false",
        "defaultArrivalDay": "",
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.roompot.com",
        "Referer": "https://www.roompot.com/resorts/parks",
    }

    result = scraper.post(
        scraper.URL,
        headers=headers,
        data=data,
    ).json()

    # facets = result["searchResult"]["countryRegionFacets"]
    facets2 = result["searchResult"]

    # print(json.dumps(facets, indent=2, ensure_ascii=False))
    print(json.dumps(facets2, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
