from pprint import pprint
from collections import Counter
from app.config.config_loader import load_config
from app.scrapers.eurocamps import EurocampScraper


def main():
    config = load_config()
    scraper = EurocampScraper(config)

    adults = scraper.adults
    ages = [30] * adults + scraper.children

    for arrival in scraper.departure_dates:

        payload = {
            "operationName": "AccommodationSearch",
            "variables": {
                "startDate": arrival.strftime("%Y-%m-%d"),
                "nights": scraper.nights,
                "ages": ages,
                "pets": 0,
                "filters": [],
                "siteCode": "PA012",  # tijdelijk hardcoded
                "alternatives": True,
                "alternativesExcludeWorse": True,
                "alternativesMaxFlex": 7,
                "alternativesThreshold": 200,
                "sortBy": [],
            },
            "query": """
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
                        capacity
                        bedrooms
                        bathrooms
                        beds
                        brand
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

                ... on ApiError {
                  code
                  source
                }
              }
            }
            """
        }

        headers = {
            "Content-Type": "application/json",
            "x-market": "eurocamp-nl",
            "x-requested-by": "/reserveren/camping-zoeken",
        }

        response = scraper.post(
            scraper.URL,
            json=payload,
            headers=headers,
        )

        data = response.json()
        results = (
            data["data"]["accommodationSearch"]["results"]
        )
        pprint(data)
        for result in results:


            if "parc" in result:
                print(
                    "PARC:",
                    result["parc"]["code"],
                    result["parc"]["name"],
                )

            if "siteCode" in result:
                print(
                    "SITE:",
                    result["siteCode"],
                )



if __name__ == "__main__":
    main()