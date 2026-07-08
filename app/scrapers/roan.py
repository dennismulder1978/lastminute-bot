from datetime import timedelta

from app.models.deal import Deal
from app.scrapers.base import BaseScraper


class RoanScraper(BaseScraper):

    provider = "roan"

    URL = "https://www.roan.nl/api/v2/camping-search"

    def scrape(self):

        departure_dates = self.config["trip"]["departure_dates"]
        nights = self.config["trip"]["nights"]
        regions = self.config["providers"]["roan"]["regions"]

        deals = []

        for arrival in departure_dates:

            departure = arrival + timedelta(days=nights)

            page = 1

            while True:

                params = {
                    "page": page,
                    "itemsPerPage": 20,
                    "sort": "relevance:asc",
                    "arrivalDate": arrival.strftime("%Y-%m-%d"),
                    "departureDate": departure.strftime("%Y-%m-%d"),
                    "dateOffset": 3,
                    "regions[]": regions,
                }

                response = self.get(
                    self.URL,
                    params=params,
                )

                result = response.json()

                campings = result.get("campingResults", [])

                self.logger.info(
                    "%s: pagina %d: %d campings",
                    arrival,
                    page,
                    len(campings),
                )

                if not campings:
                    break

                for camping in campings:

                    accommodation = (
                        camping.get("accommodationKindResults") or []
                    )

                    if not accommodation:
                        continue

                    accommodation = accommodation[0]

                    amount = (
                        accommodation
                        .get("lowestPrice", {})
                        .get("amount")
                    )

                    price = None

                    if amount is not None:
                        price = float(amount) / 100

                    deals.append(
                        Deal(
                            source="Roan",
                            title=camping.get("name", ""),
                            location=camping.get("place", ""),
                            region=camping.get("region", ""),
                            countrycode=camping.get("countryCode", ""),
                            url=accommodation.get("campingUrl", ""),
                            arrival_date=arrival,
                            price=price,
                        )
                    )

                page += 1

        return deals
