from datetime import timedelta
import re
from app.models.deal import Deal
from app.scrapers.base import BaseScraper


class LandalScraper(BaseScraper):

    provider = "landal"

    URL_PARKS = (
        "https://www.landal.com/en/api/destinations/parksAvailabilities/search"
    )

    URL_ACCOMMODATIONS = (
        "https://www.landal.com/en/api/destinations/accommodationsAvailabilities/search"
    )

    def scrape(self):

        deals = []

        for arrival in self.departure_dates:

            self.logger.info(
                "Searching Landal parks for %s",
                arrival,
            )

            parks = self.search_parks(arrival)

            self.logger.info(
                "Found %d parks",
                len(parks),
            )

            for park in parks:

                park_info = park.get("ParkInfo", {})
                park_code = park_info.get("ParkCode")

                if not park_code:
                    continue

                deals.extend(
                    self.search_accommodations(
                        park_info=park_info,
                        arrival=arrival,
                    )
                )

        return deals

    def search_parks(self, arrival):

        departure = arrival + timedelta(days=self.nights)

        data = {
            "arrivalDate": arrival.strftime("%d-%m-%Y"),
            "departureDate": departure.strftime("%d-%m-%Y"),
            "parkInfoLevel": 0,
            "promotedProductId": "{AF34FA23-0C46-495A-A4A1-11F359E40DC1}",
            # "regions[]": self.regions,
            "campaignInventoryEnabled": "false",
            "stayType": 947,
            "searchType": 1,
            "paginationOffset": 0,
            "travelGroup[0][Id]": "18-120",
            "travelGroup[0][Amount]": self.adults,
            "travelGroup[1][Id]": "3-17",
            "travelGroup[1][Amount]": len(self.children),
            "travelGroup[2][Id]": "0-2",
            "travelGroup[2][Amount]": 0,
            "travelGroup[3][Id]": "pets",
            "travelGroup[3][Amount]": 0,
            "travelGroupCombiEnabled": "false",
            "defaultArrivalDay": "",
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.landal.com",
            "Referer": "https://www.landal.com/destinations/parks",
        }

        response = self.post(
            self.URL_PARKS,
            headers=headers,
            data=data,
        )

        response.raise_for_status()

        result = response.json()

        search_result = result.get("searchResult", {})
        parks = search_result.get("parks", [])

        self.logger.info(
            "Found %d Landal parks for %s",
            len(parks),
            arrival,
        )

        return parks

    def search_accommodations(self, park_info, arrival):

        departure = arrival + timedelta(days=self.nights)

        data = {
            "arrivalDate": arrival.strftime("%d-%m-%Y"),
            "arrivalDaysAfter": 0,
            "arrivalDaysBefore": 0,
            "departureDate": departure.strftime("%d-%m-%Y"),
            "numberOfNights": self.nights,
            "campaignInventoryEnabled": "false",
            "selectedParkCode": park_info["ParkCode"],
            "sortOption": 16,
            "stayType": 947,
            "searchType": 3,
            "paginationOffset": 0,
            "travelGroup[0][Id]": "18-120",
            "travelGroup[0][Amount]": self.adults,
            "travelGroup[1][Id]": "3-17",
            "travelGroup[1][Amount]": len(self.children),
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
            "Origin": "https://www.landal.com",
            "Referer": park_info["ParkDetailPageLink"]["Url"],
        }

        response = self.post(
            self.URL_ACCOMMODATIONS,
            headers=headers,
            data=data,
        )

        result = response.json()

        search_result = result.get("searchResult", {})
        accommodations = search_result.get("accommodations", [])

        self.logger.info(
            "%s: %d accommodations",
            park_info["ParkName"],
            len(accommodations),
        )

        deals = []

        for accommodation in accommodations:

            info = accommodation.get("AccommodationInfo", {})
            price_info = accommodation.get("PriceInfo", {})

            price = price_info.get("bestTotalPriceInCents")

            # accommodatie type
            name = info.get("Name", "").lower()

            accommodation_type = None

            if "bungalow" in name:
                accommodation_type = "bungalow"
            elif "villa" in name:
                accommodation_type = "villa"
            elif "apartment" in name:
                accommodation_type = "apartment"
            elif "tent" in name:
                accommodation_type = "tent"

            if (
                    self.accommodation_types
                    and accommodation_type not in self.accommodation_types
            ):
                continue

            bedrooms = info.get("BedroomUspAmount")

            if (
                    self.min_bedrooms is not None
                    and bedrooms is not None
                    and bedrooms < self.min_bedrooms
            ):
                continue

            deals.append(
                self._build_deal(
                    park_info=park_info,
                    accommodation=accommodation,
                    arrival=arrival,
                )
            )

        return deals



    def _build_deal(self, park_info, accommodation, arrival):

        info = accommodation.get("AccommodationInfo", {})
        price_info = accommodation.get("PriceInfo", {})

        price = price_info.get("bestTotalPriceInCents")

        return Deal(
            source="Landal",
            title = f"{info['ParkName']} - {info['Name']}",
            location=info.get("City", ""),
            region=info.get("RegionCode", ""),
            countrycode=info.get("CountryCode", ""),
            url=info.get("DetailPageLink", {}).get("Url", ""),
            arrival_date=arrival,

            price=price,

            accommodation_type=self._extract_accommodation_type(
                info.get("Name", "")
            ),
            comfort_level=info.get("Label", {}).get("Title"),
            bedrooms=info.get("BedroomUspAmount"),
            capacity=self._extract_capacity(
                info.get("Name", "")
            ),

            airconditioning=None,
            pets_allowed=None,
        )

    def _extract_capacity(self, name):

        match = re.match(r"(\\d+)-person", name)

        if match:
            return int(match.group(1))

        return None

    def _extract_accommodation_type(self, name):

        name = name.lower()

        if "bungalow" in name:
            return "bungalow"

        if "villa" in name:
            return "villa"

        if "apartment" in name:
            return "apartment"

        if "tent" in name:
            return "tent"

        return None