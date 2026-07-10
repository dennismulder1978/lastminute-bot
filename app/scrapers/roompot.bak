from app.models.deal import Deal
from app.scrapers.base import BaseScraper
from datetime import timedelta
from app.constants.accommodation_mapping import ROOMPOT_MAPPING
from pprint import pprint
class RoompotScraper(BaseScraper):

    provider = "roompot"

    URL = "https://www.roompot.com/en/api/destinations/parksAvailabilities/search"

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

            data = {
                "arrivalDate": arrival.strftime("%d-%m-%Y"),
                "departureDate": departure.strftime("%d-%m-%Y"),
                "parkInfoLevel": 0,
                "promotedProductId": "{3F1C8CB8-055E-4AA7-8F36-489E9A3B9A30}",
                # "regions[]": regions,
                "campaignInventoryEnabled": "false",
                "stayType": 968,
                "searchType": 1,
                "paginationOffset": 0,
                "travelGroup[0][Id]": "18-120",
                "travelGroup[0][Amount]": adults,
                "travelGroup[1][Id]": "3-17",
                "travelGroup[1][Amount]": children,
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

            response = self.session.post(
                self.URL,
                headers=headers,
                data=data,
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

            search_result = result.get("searchResult", {})

            parks = search_result.get("parks", [])

            self.logger.info(
                "RoompotScraper: %s: %d parks",
                arrival,
                len(parks)
            )

            for park in parks:

                park_info = park.get("ParkInfo", {})

                url = (
                    park_info
                    .get("AccommodationsForParkPageLink", {})
                    .get("Url", "")
                )

                price_info = park.get("PriceInfo")

                if not price_info:
                    continue


                code = price_info.get("accommodationCode", "").lower()

                accommodation_type = ROOMPOT_MAPPING.get(code)
                if accommodation_type is None:
                    self.logger.warning("Unknown Roompot accommodation code: %s", code)
                    continue

                if (
                        self.accommodation_types
                        and accommodation_type not in self.accommodation_types
                ):
                    continue

                price = price_info.get("bestRentalPriceInCents")

                if price is not None:
                    price /= 100

                deals.append(
                    Deal(
                        source="Roompot",
                        title=park_info.get("ParkName", ""),
                        location=park_info.get("City", ""),
                        region=park_info.get("Region", ""),
                        countrycode=park_info.get("CountryCode", ""),
                        price=price,
                        url=url,
                        arrival_date=arrival,

                        accommodation_type=accommodation_type,
                        comfort_level=None,
                        bedrooms=None,
                        capacity=None,
                        airconditioning=None,
                        pets_allowed=None,
                    )
                )
        return deals