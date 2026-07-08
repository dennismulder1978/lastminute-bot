from datetime import timedelta

from app.config.config_loader import load_config
from app.scrapers.roan import RoanScraper


def main():
    config = load_config()
    scraper = RoanScraper(config)

    departure_dates = config["trip"]["departure_dates"]
    nights = config["trip"]["nights"]

    accommodation_types = set()

    for arrival in departure_dates:

        departure = arrival + timedelta(days=nights)

        page = 1

        while True:

            params = {
                "page": page,
                "itemsPerPage": 20,
                # "sort": "relevance:asc",
                # "arrivalDate": arrival.strftime("%Y-%m-%d"),
                # "departureDate": departure.strftime("%Y-%m-%d"),
                # "dateOffset": 3,
                # "regions[]": config["providers"]["roan"]["regions"],
            }

            response = scraper.get(
                scraper.URL,
                params=params,
            )

            result = response.json()

            campings = result.get("campingResults", [])

            if not campings:
                break

            for camping in campings:
                for accommodation in camping.get("accommodationKindResults", []):

                    accommodation_types.add(
                        accommodation.get("title", "").strip()
                    )

            page += 1

    print("\n=== Accommodation types ===\n")

    for accommodation_type in sorted(accommodation_types):
        print(accommodation_type)

    print(f"\nFound {len(accommodation_types)} unique accommodation types.")


if __name__ == "__main__":
    main()