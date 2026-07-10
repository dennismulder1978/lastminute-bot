from app.models.deal import Deal
from app.scrapers.base import BaseScraper
from datetime import timedelta, datetime
from app.constants.accommodation_mapping import EUROCAMP_MAPPING
import re
from pprint import pprint
class EurocampScraper(BaseScraper):
    provider = "eurocamp"

    BASE_URL = "https://www.eurocamp.nl"
    URL = "https://www.eurocamp.nl/api/graphql"

    HEADERS = {
        "Content-Type": "application/json",
        "x-market": "eurocamp-nl",
        "x-requested-by": "/reserveren/camping-zoeken",
    }

    SEARCH_QUERY = """
    query Search(
      $nights: Int!,
      $startDate: LocalDate!,
      $alternatives: Boolean!,
      $ages: [Int!]!,
      $pets: Int!,
      $filters: [Filter!]!,
      $siteCodes: [ID!]!,
      $sortBy: [String!]!,
      $alternativesThreshold: Int,
      $alternativesMaxFlex: Int,
      $includeMissingParcs: Boolean!
    ) {
      search(
        nights: $nights
        startDate: $startDate
        alternatives: $alternatives
        ages: $ages
        pets: $pets
        filters: $filters
        siteCodes: $siteCodes
        sortBy: $sortBy
        alternativesThreshold: $alternativesThreshold
        alternativesMaxFlex: $alternativesMaxFlex
        includeMissingParcs: $includeMissingParcs
      ) {
        results {
          ... on FullSearchResult {
            price
            arrivalDate

            parc {
              code
              name
              slug

              location {
                place
                region
                country
              }
            }
          }

          ... on PartialSearchResult {
            siteCode
          }
        }
      }
    }
    """

    ACCOMMODATION_QUERY = """
    query AccommodationSearch(
      $startDate: LocalDate!,
      $nights: Int!,
      $ages: [Int!]!,
      $pets: Int!,
      $filters: [Filter!]!,
      $siteCode: ID!,
      $alternatives: Boolean,
      $alternativesThreshold: Int,
      $alternativesMaxFlex: Int,
      $alternativesExcludeWorse: Boolean,
      $sortBy: [String!]
    ) {

      accommodationSearch(
        startDate: $startDate
        nights: $nights
        ages: $ages
        pets: $pets
        filters: $filters
        siteCode: $siteCode
        alternatives: $alternatives
        alternativesThreshold: $alternativesThreshold
        alternativesMaxFlex: $alternativesMaxFlex
        alternativesExcludeWorse: $alternativesExcludeWorse
        sortBy: $sortBy
      ) {

        ... on AccommodationSearch {

          results {

            range

            stays {

              proposalKey
              arrivalDate
              price

              accommodation {

                code
                name
                type
                category
                bedrooms
                bathrooms
                beds
                brand
                capacity
                size
                features

                icons {
                  icon
                  text
                }

              }
            }
          }
        }
      }
    }
    """

    def scrape(self):

        deals = []
        seen = set()

        ages = [30] * self.adults + self.children

        for arrival in self.departure_dates:

            camps = self._search(arrival, ages)

            self.logger.info(
                "Eurocamp: %d campings gevonden",
                len(camps),
            )

            for camp in camps:

                accommodation_groups = self._accommodation_search(
                    arrival=arrival,
                    ages=ages,
                    site_code=camp["parc"]["code"],
                )

                # self.logger.info(
                #     "%s -> %d accommodation groups",
                #     camp["parc"]["name"],
                #     len(accommodation_groups),
                # )

                for group in accommodation_groups:

                    for stay in group.get("stays", []):

                        if stay["arrivalDate"] != arrival.isoformat():
                            continue

                        deal = self._build_deal(
                            camp=camp,
                            stay=stay,
                        )

                        if deal is None:
                            continue

                        if not self._accept_deal(deal):
                            continue

                        key = (
                            deal.source,
                            deal.url,
                            deal.arrival_date,
                        )

                        if key in seen:
                            continue

                        seen.add(key)
                        deals.append(deal)

        self.logger.info("Eurocamp: %d deals", len(deals))

        return deals

    def _search(self, arrival, ages):

        payload = {
            "operationName": "Search",
            "variables": {
                "nights": self.nights,
                "startDate": arrival.strftime("%Y-%m-%d"),
                "alternatives": False,
                "ages": ages,
                "pets": 0,
                "filters": [],
                "sortBy": [],
                "siteCodes": [],
                "alternativesThreshold": 200,
                "alternativesMaxFlex": 7,
                "includeMissingParcs": True,
            },
            "query": self.SEARCH_QUERY,
        }

        response = self.post(
            self.URL,
            json=payload,
            headers=self.HEADERS,
        )

        results = (
            response.json()
            .get("data", {})
            .get("search", {})
            .get("results", [])
        )

        camps = []

        for result in results:
            if "parc" in result:
                camps.append({
                    "parc": result["parc"],
                })

        return camps

    def _accommodation_search(
        self,
        arrival,
        ages,
        site_code,
    ):

        payload = {
            "operationName": "AccommodationSearch",
            "variables": {
                "startDate": arrival.strftime("%Y-%m-%d"),
                "nights": self.nights,
                "ages": ages,
                "pets": 0,
                "filters": [],
                "siteCode": site_code,
                "alternatives": True,
                "alternativesExcludeWorse": True,
                "alternativesMaxFlex": 7,
                "alternativesThreshold": 200,
                "sortBy": [],
            },
            "query": self.ACCOMMODATION_QUERY,
        }

        response = self.post(
            self.URL,
            json=payload,
            headers=self.HEADERS,
        )

        return (
            response.json()
            .get("data", {})
            .get("accommodationSearch", {})
            .get("results", [])
        )

    def _parse_bedrooms(self, value):

        if not value:
            return None

        match = re.search(r"\d+", value)

        if match:
            return int(match.group())

        return None

    def _parse_capacity(self, value):

        if not value:
            return None

        numbers = re.findall(r"\d+", value)

        if not numbers:
            return None

        return max(map(int, numbers))

    def _countrycode(self, country):

        mapping = {
            "Nederland": "NL",
            "België": "BE",
            "Frankrijk": "FR",
            "Duitsland": "DE",
            "Spanje": "ES",
            "Italië": "IT",
            "Kroatië": "HR",
            "Oostenrijk": "AT",
            "Luxemburg": "LU",
            "Zwitserland": "CH",
        }

        return mapping.get(country)

    def _build_deal(self, camp, stay):

        accommodation = stay["accommodation"]

        mapping_key = accommodation.get("type", "").lower()
        accommodation_type = EUROCAMP_MAPPING.get(mapping_key)

        bedrooms = self._parse_bedrooms(
            accommodation.get("bedrooms")
        )

        capacity = self._parse_capacity(
            accommodation.get("capacity")
        )

        return Deal(

            source=self.provider,

            title=accommodation.get("name"),

            location=camp["parc"]["location"]["place"],
            region=camp["parc"]["location"]["region"],
            countrycode=self._countrycode(camp["parc"]["location"]["country"]),

            url=(
                f"{self.BASE_URL}"
                f"{camp['parc']['slug']}"
                f"?proposal={stay['proposalKey']}"
            ),

            arrival_date=datetime.strptime(
                stay["arrivalDate"],
                "%Y-%m-%d",
            ).date(),

            price=stay["price"],

            accommodation_type=accommodation_type,
            comfort_level=accommodation.get("category"),

            bedrooms=bedrooms,
            capacity=capacity,

            airconditioning=None,
            pets_allowed=None,
        )

    def _accept_deal(self, deal):

        if (
                self.accommodation_types
                and deal.accommodation_type
                not in self.accommodation_types
        ):
            return False

        if (
                self.min_capacity is not None
                and deal.capacity is not None
                and deal.capacity < self.min_capacity
        ):
            return False

        if (
                self.min_bedrooms is not None
                and deal.bedrooms is not None
                and deal.bedrooms < self.min_bedrooms
        ):
            return False

        return True