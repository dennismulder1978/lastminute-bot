from datetime import timedelta
from app.models.deal import Deal
from app.scrapers.base import BaseScraper
from app.constants.accommodation_mapping import ROAN_MAPPING

class RoanScraper(BaseScraper):

    provider = "roan"

    URL = "https://www.roan.nl/api/v2/camping-search"

    def scrape(self):

        deals = []

        for arrival in self.departure_dates:
            departure = arrival + timedelta(days=self.nights)

            adults = self.adults
            children = len(self.children)
            regions = self.regions
            accommodation_types = self.accommodation_types
            min_capacity = self.min_capacity
            min_bedrooms = self.min_bedrooms

            page = 1

            while True:

                params = {
                    "page": page,
                    "itemsPerPage": 20,
                    "sort": "relevance:asc",
                    "arrivalDate": arrival.strftime("%Y-%m-%d"),
                    "departureDate": departure.strftime("%Y-%m-%d"),
                    "dateOffset": 1,
                    "regions[]": regions,
                }

                response = self.get(
                    self.URL,
                    params=params,
                )

                result = response.json()

                campings = result.get("campingResults", [])

                if not campings:
                    break

                for camping in campings:
                    accommodations = camping.get('accommodationKindResults', [])

                    if not accommodations:
                        continue

                    for accommodation in accommodations:

                        amount = (
                            accommodation
                            .get("lowestPrice", {})
                            .get("amount")
                        )

                        price = None

                        if amount is not None:
                            price = float(amount) / 100

                        title = accommodation.get("title", "")

                        accommodation_type = ROAN_MAPPING.get(title.lower())

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


                                accommodation_type=accommodation_type,
                                comfort_level=None,

                                bedrooms=None,
                                capacity=None,

                                airconditioning=None,
                                pets_allowed=None,
                            )
                        )

                page += 1

        return deals
