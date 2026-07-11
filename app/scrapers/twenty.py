from app.constants.accommodation_mapping import TWENTY_MAPPING
from app.scrapers.base import BaseScraper
from app.models.deal import Deal

class TwentyScraper(BaseScraper):

    BASE_URL = None
    TENANT = None
    LOCALE = None
    ACCOMMODATION_MAPPING = {}

    def scrape(self):

        deals = []

        for arrival in self.departure_dates:

            self.logger.info(
                "Searching %s sites for %s",
                self.provider.capitalize(),
                arrival,
            )

            sites = self.search_sites(arrival)

            self.logger.info(
                "Found %d sites",
                len(sites),
            )

            for site in sites:

                deals.extend(
                    self.search_accommodations(
                        site=site,
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
                "funnel": None,
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
            "Origin": self.BASE_URL,
            "Referer": (
                f"{self.BASE_URL}/"
            ),
        }

        response = self.post(
            self.url_sites,
            headers=headers,
            json=payload,
        )

        result = response.json()

        data = result.get("data", {})
        sites = data.get("sites", [])

        self.logger.info(
            "Found %d sites",
            len(sites),
        )

        return sites

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
                "limit": 100,
                "order": "desc",
                "orderBy": "popular",
                "orderSettingsLabel": "popular-desc",
                "page": 1,
            },
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": self.BASE_URL,
            "Referer": (
                f"{self.BASE_URL}/camping/"
                f"{site['meta']['country']['slug']}/"
                f"{site['meta']['area']['slug']}/"
                f"{site['slug']}"
            ),
        }

        response = self.post(
            self.url_accommodations,
            headers=headers,
            json=payload,
        )

        result = response.json()

        data = result.get("data", {})
        accommodations = data.get("accommodations", [])

        self.logger.info(
            "%s: %d accommodations",
            site["name"],
            len(accommodations),
        )

        deals = []

        for accommodation in accommodations:

            accommodation_type = self.ACCOMMODATION_MAPPING.get(
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


    def _build_deal(self, site, accommodation, arrival):

        return Deal(
            source=self.provider.capitalize(),

            title=f"{site['name']} - {accommodation['name']}",

            location=site["meta"].get("city", {}).get("name"),

            region=site["meta"]["area"]["name"],

            countrycode=site["meta"]["country"]["code"],

            url=self._site_url(
                site,
                accommodation,
            ),

            arrival_date=arrival,

            price=accommodation.get("priceAfterDiscount"),

            accommodation_type=self.ACCOMMODATION_MAPPING.get(
                accommodation.get("categorySlug")
            ),

            bedrooms=accommodation.get("bedrooms"),

            capacity=accommodation.get("maxPersons"),

            comfort_level=None,

            airconditioning=accommodation.get("aircondition"),

            pets_allowed=accommodation.get("dogAllowed"),
        )

    def _site_url(self, site, accommodation):

        return (
            f"{self.BASE_URL}/camping/"
            f"{site['meta']['country']['slug']}/"
            f"{site['meta']['area']['slug']}/"
            f"{site['slug']}"
            f"?accommodation={accommodation['id']}"
        )
        
        
    @property
    def url_sites(self):
        return (
            f"{self.BASE_URL}/api/twenty/v2/"
            f"{self.TENANT}/{self.LOCALE}/search/sites"
        )


    @property
    def url_accommodations(self):
        return (
            f"{self.BASE_URL}/api/twenty/v2/"
            f"{self.TENANT}/{self.LOCALE}/search/accommodations"
        )
        
        
    