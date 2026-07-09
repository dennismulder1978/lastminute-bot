from datetime import timedelta

from app.config.config_loader import load_config
from app.scrapers.landal import LandalScraper

from pprint import pprint
def main():
    config = load_config()
    scraper = LandalScraper(config)

    adults = config["family"]["adults"]
    children = config["family"]["children"]

    departure_dates = config["trip"]["departure_dates"]
    nights = config["trip"]["nights"]

    accommodation_types = set()

    for arrival in departure_dates:

        departure = arrival + timedelta(days=nights)

        data = {
            "arrivalDate": arrival.strftime("%d-%m-%Y"),
            "departureDate": departure.strftime("%d-%m-%Y"),
            "parkInfoLevel": 0,
            "promotedProductId": "{3F1C8CB8-055E-4AA7-8F36-489E9A3B9A30}",
            "regions[]": [
                "9295.18635",
                "9295.18637",
            ],
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

        # data = {
        #     "arrivalDate": arrival.strftime("%d-%m-%Y"),
        #     "arrivalDaysAfter": 0,
        #     "arrivalDaysBefore": 0,
        #     "departureDate": departure.strftime("%d-%m-%Y"),
        #     "numberOfNights": nights,
        #
        #     "campaignInventoryEnabled": "false",
        #
        #     "selectedParkCode": "DSD",  # <-- verplicht
        #     "sortOption": 16,
        #
        #     "stayType": 947,
        #     "searchType": 3,
        #
        #     "paginationOffset": 0,
        #
        #     "travelGroup[0][Id]": "18-120",
        #     "travelGroup[0][Amount]": adults,
        #     "travelGroup[1][Id]": "3-17",
        #     "travelGroup[1][Amount]": len(children),
        #     "travelGroup[2][Id]": "0-2",
        #     "travelGroup[2][Amount]": 0,
        #     "travelGroup[3][Id]": "pets",
        #     "travelGroup[3][Amount]": 0,
        #
        #     "travelGroupCombiEnabled": "false",
        #     "defaultArrivalDay": "",
        # }

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.roompot.com",
            "Referer": "https://www.roompot.com/resorts/parks",
        }
        response = scraper.post(
            "https://www.landal.com/en/api/destinations/parksAvailabilities/search",
            headers=headers,
            data=data,
        )

        result = response.json()
        # pprint(result.keys())
        # pprint(result["searchResult"].keys())
        # accommodations = result["searchResult"]["accommodations"]

        # print(len(accommodations))
        # pprint(accommodations[0])

        from pprint import pprint

        pprint(result["searchResult"]["parks"][0]["ParkInfo"])
if __name__ == "__main__":
    main()