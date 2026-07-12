from datetime import timedelta
from time import sleep
from app.models.deal import Deal
from app.scrapers.base import BaseScraper
from app.constants.accommodation_mapping import YELLOH_MAPPING
import requests

class YellohScraper(BaseScraper):

    provider = "yelloh"

    GRAPHQL_URL = "https://api.sitepriv.prod.yellohvillage.fr/graphql"

    AVAILABILITY_URL = (
        "https://www.yellohvillage.nl/camping/"
        "availability_price_categ"
    )

    ACCOMMODATION_MAPPING = YELLOH_MAPPING

    AVAILABILITY_QUERY = """
            query (
                $campingCode: Int!,
                $startDate: Date!,
                $endDate: Date!,
                $accommodationType: String!,
                $peopleCount: Int!,
                $filters: [FilterInput!],
                $fidelityId: ID
            ) {
            campingAvailability(
                campingCode: $campingCode
                peopleCount: $peopleCount
                accommodationType: $accommodationType
                startDate: $startDate
                endDate: $endDate
                filters: $filters
                fidelityId: $fidelityId
            ) {
                statusCode
                accommodationId
                info {
                arrivalDate
                departureDate
                stock
                priceInfo {
                    title
                    fullPrice
                    discountedPrice
                    discount
                }
                }
            }
            }
            """

    SEARCH_QUERY = """
            query ($startDate: Date, $endDate: Date, $accommodationType: String!, $peopleCount: Int!, $campingContentIds: [Int], $filters: [FilterInput!]) {
            searchCampings(
                peopleCount: $peopleCount
                accommodationType: $accommodationType
                startDate: $startDate
                endDate: $endDate
                campingContentIds: $campingContentIds
                filters: $filters
            ) {
                campings {
                campingCode
                isNew
                spotlighted
                isResidence
                contentId
                countryId
                name
                starCount
                city
                department
                campingUrl
                image
                note
                openingDates {
                    start
                    end
                }
                coordinates {
                    latitude
                    longitude
                }
                accommodationsUrl {
                    slot
                    rental
                }
                map {
                    type
                    xPosition
                    yPosition
                }
                availabilityStatus
                filterCategories {
                    categoryId
                    filters {
                    id
                    title
                    key
                    }
                }
                accommodations {
                    ...CampingAccommodationDetailFragment

                    ... on Rental {
                    technicalInfos {
                        ...CampingRentalTechnicalInformationFragment
                    }
                    }

                    ... on Slot {
                    technicalInfos {
                        ...CampingSlotTechnicalInformationFragment
                    }
                    }
                }

                specialOffer {
                    imageUrl
                    imageAlt
                    description
                }
                }

                filterCategories {
                categoryId
                type
                priority

                filters {
                    id
                    title
                    count
                    key
                    priority
                }
                }

                tiles {
                imageUrl
                position
                url
                tooltipContent
                gaId
                }

                POIs {
                contentId

                coordinates {
                    latitude
                    longitude
                }

                description
                detailUrl

                image {
                    src: url
                }

                title
                type
                }
            }
            }

            fragment CampingAccommodationDetailFragment on Accommodation {
            code
            accommodationType
            title

            badge {
                type
                count
                color
            }

            filters

            technicalInfos {
                pmr {
                value
                label
                }

                surface {
                label
                }

                animalsAllowed {
                value
                label
                }
            }
            }

            fragment CampingRentalTechnicalInformationFragment on RentalTechnicalInformation {
            capacity {
                value
                label
            }

            airConditioning {
                value
                label
            }

            television {
                value
                label
            }

            exteriorPlug {
                value
                label
            }

            bathroom {
                value
                label
            }

            bedroom {
                value
                label
            }
            }

            fragment CampingSlotTechnicalInformationFragment on SlotTechnicalInformation {
            electricity {
                value
                label
            }

            waterDisposal {
                value
                label
            }

            waterSupply {
                value
                label
            }

            privateSanitary {
                value
                label
            }

            capacity {
                value
                label
            }
            }
            """
        
        

    def graphql(self, query, variables):

        headers = {
            "Content-Type": "application/json",
            "gql-locale": "nl",
            "gql-market-site": "1",
            "Accept": "*/*",
            "Origin": "https://www.yellohvillage.nl",
            "Referer": "https://www.yellohvillage.nl",
            "X-Requested-With": "XMLHttpRequest",
        }

        for attempt in range(3):

            try:

                response = self.post(
                    self.GRAPHQL_URL,
                    headers=headers,
                    json={
                        "query": query,
                        "variables": variables,
                    },
                )

                sleep(0.25)

                return response.json()["data"]

            except requests.HTTPError as exc:

                if exc.response is not None and exc.response.status_code == 502:
                    self.logger.warning(
                        "Yelloh API gaf 502, retry %d/3",
                        attempt + 1,
                    )
                    sleep(2)
                    continue

                raise

        raise RuntimeError("Yelloh GraphQL bleef 502 retourneren.")

    def scrape(self):

        deals = []

        for arrival in self.departure_dates:

            self.logger.info(
                "Searching Yelloh villages for %s",
                arrival,
            )

            campings = self.search_campings(arrival)

            self.logger.info(
                "Found %d campings",
                len(campings),
            )

            for camping in campings:

                try:
                    deals.extend(
                        self.search_availability(
                            camping=camping,
                            arrival=arrival,
                        )
                    )
                except Exception as exc:
                    self.logger.warning(
                        "Camping %s overgeslagen: %s",
                        camping["name"],
                        exc,
                    )
        self.logger.info("Yelloh returned %d deals", len(deals))

        return deals
    
    def search_campings(self, arrival):

        departure = arrival + timedelta(days=self.nights)

        variables = {
            "accommodationType": "rental",
            "peopleCount": self.adults + len(self.children),
            "startDate": arrival.strftime("%Y-%m-%dT00:00:00.000Z"),
            "endDate": departure.strftime("%Y-%m-%dT00:00:00.000Z"),
            "campingContentIds": [],
            "filters": [],
        }

        data = self.graphql(
            self.SEARCH_QUERY,
            variables,
        )

        campings = data["searchCampings"]["campings"]

        self.logger.info(
            "Found %d Yelloh campings",
            len(campings),
        )

        return campings

    def search_availability(self, camping, arrival):

        departure = arrival + timedelta(days=self.nights)

        variables = {
            "campingCode": camping["campingCode"],
            "accommodationType": "rental",
            "peopleCount": self.adults + len(self.children),
            "startDate": arrival.strftime("%Y-%m-%dT00:00:00.000Z"),
            "endDate": departure.strftime("%Y-%m-%dT00:00:00.000Z"),
            "filters": [],
            "fidelityId": None,
        }

        data = self.graphql(
            self.AVAILABILITY_QUERY,
            variables,
        )

        availability = data["campingAvailability"]

        if availability["statusCode"] != "available":
            return []

        price = availability["info"]["priceInfo"]["discountedPrice"]

        self.logger.info(
            "%s: €%s",
            camping["name"],
            price,
        )

        accommodation = camping["accommodations"][0]

        deal = self._build_deal(
            camping=camping,
            accommodation=accommodation,
            stay={
                "price": price,
                "step3Url": (
                    "https://www.yellohvillage.nl"
                    + camping["campingUrl"]
                ),
            },
            availability=availability,
            arrival=arrival,
        )
        
        return [deal]
    
    def _build_deal(
        self,
        camping,
        accommodation,
        stay,
        availability,
        arrival,
    ):

        technical = accommodation.get("technicalInfos", {})

        price = stay.get("price")

        if price is None:
            self.logger.warning(
                "No price for %s (%s)",
                camping["name"],
                accommodation["title"],
            )
            return None

        title = accommodation.get("title", "").lower()

        accommodation_type = None

        for key, value in YELLOH_MAPPING.items():
            if key in title:
                accommodation_type = value
                break

        return Deal(

            source="Yelloh",

            title=f"{camping['name']} - {accommodation['title']}",

            location=camping.get("city", "").strip(),

            region=camping.get("department", ""),

            countrycode=camping.get("countryId"),

            url=(
                stay.get("step3UrlWithoutTracking")
                or stay.get("step3Url")
                or (
                    "https://www.yellohvillage.nl"
                    + camping.get("campingUrl", "")
                )
            ),

            arrival_date=arrival,

            price=price,

            accommodation_type=accommodation_type,

            comfort_level=accommodation.get(
                "badge",
                {},
            ).get("count"),

            bedrooms=technical.get(
                "bedroom",
                {},
            ).get("value"),

            capacity=self._extract_capacity(
                technical.get(
                    "capacity",
                    {},
                ).get("value")
            ),

            airconditioning=technical.get(
                "airConditioning",
                {},
            ).get("value"),

            pets_allowed=technical.get(
                "animalsAllowed",
                {},
            ).get("value"),
        )

    def _extract_accommodation_type(self, title):

        title = title.lower()

        for key, value in self.ACCOMMODATION_MAPPING.items():

            if key in title:
                return value

        return None
    
    def _extract_capacity(self, value):

        if value is None:
            return None

        value = str(value)

        if "/" in value:
            value = value.split("/")[-1]

        try:
            return int(value)
        except ValueError:
            return None
    