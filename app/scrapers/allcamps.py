from datetime import timedelta
from app.constants.accommodation_mapping import ALLCAMPS_MAPPING
from app.scrapers.base import BaseScraper
from app.models.deal import Deal

class AllcampsScraper(BaseScraper):

    provider = "allcamps"

    URL_SITES = (
        "https://www.allcamps.nl/api/twenty/v2/allcamps/nl/search/sites"
    )

    URL_ACCOMMODATIONS = (
        "https://www.allcamps.nl/api/twenty/v2/allcamps/nl/search/accommodations"
    )

    def scrape(self):

        deals = []

        for arrival in self.departure_dates:

            self.logger.info(
                "Searching Allcamps sites for %s",
                arrival,
            )

            sites = self.search_sites(arrival)

            self.logger.info(
                "Found %d sites",
                len(sites),
            )

            for site in sites:

                accommodations = self.search_accommodations(
                    site=site,
                    arrival=arrival,
                )

                self.logger.info(
                    "%s: %d accommodations",
                    site["name"],
                    len(accommodations),
                )

               # build deal
                for accommodation in accommodations:

                    # filters
                    accommodation_type = ALLCAMPS_MAPPING.get(
                        accommodation["categorySlug"]
                    )

                    if (
                            self.accommodation_types
                            and accommodation_type not in self.accommodation_types
                    ):
                        continue

                    bedrooms = accommodation.get("bedrooms")

                    if (
                            self.min_bedrooms is not None
                            and bedrooms is not None
                            and bedrooms < self.min_bedrooms
                    ):
                        continue

                    capacity = accommodation.get("maxPersons")

                    if (
                            self.min_capacity is not None
                            and capacity is not None
                            and capacity < self.min_capacity
                    ):
                        continue


                    deals.append(
                        self._build_deal(
                            site=site,
                            accommodation=accommodation,
                            arrival=arrival,
                        )
                    )

        return deals

    def search_sites(self, arrival):

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
                "duration": self.nights,
                "country": None,
                "area": None,
                "recentlySeenSiteDomainId": None,
                "persons": {
                    "adults": self.adults,
                    "children": [
                        {"age": age}
                        for age in self.children
                    ],
                },
                "site": None,
                "filter": None,
            },
            "meta": {
                "limit": 250,
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
            "Referer": "https://www.allcamps.nl/zoek-en-boek",
        }

        response = self.post(
            self.URL_SITES,
            headers=headers,
            json=payload,
        )

        result = response.json()

        return result["data"]["sites"]

    def search_accommodations(self, site, arrival):

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
                "duration": self.nights,
                "country": site["meta"]["country"]["slug"],
                "area": site["meta"]["area"]["slug"],
                "recentlySeenSiteDomainId": None,
                "persons": {
                    "adults": self.adults,
                    "children": [
                        {"age": age}
                        for age in self.children
                    ],
                },
                "site": site["slug"],
                "filter": None,
            },
            "meta": {
                "limit": 250,
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
                f"https://www.allcamps.nl/camping/"
                f"{site['meta']['country']['slug']}/"
                f"{site['meta']['area']['slug']}/"
                f"{site['slug']}"
            ),
        }

        response = self.post(
            self.URL_ACCOMMODATIONS,
            headers=headers,
            json=payload,
        )

        result = response.json()
        accommodations = result["data"]["accommodations"]

        return accommodations

    def _build_deal(
            self,
            site,
            accommodation,
            arrival,
    ):

        return Deal(

            source="Allcamps",

            title=f"{site['name']} - {accommodation['name']}",

            location="",
            region=site["meta"]["area"]["name"],
            countrycode=site["meta"]["country"]["code"],

            url=(
                "https://www.allcamps.nl/camping/"
                f"{site['meta']['country']['slug']}/"
                f"{site['meta']['area']['slug']}/"
                f"{site['slug']}"
                f"?accommodation={accommodation['id']}"
            ),

            arrival_date=arrival,

            price=accommodation["priceAfterDiscount"],

            accommodation_type=ALLCAMPS_MAPPING.get(
                accommodation["categorySlug"]
            ),

            bedrooms=accommodation.get("bedrooms"),

            capacity=accommodation.get("maxPersons"),

            comfort_level=None,

            airconditioning=accommodation.get("aircondition"),

            pets_allowed=accommodation.get("dogAllowed"),
        )
