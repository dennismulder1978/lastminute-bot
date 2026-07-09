from app.models.deal import Deal
from app.scrapers.base import BaseScraper
from datetime import timedelta

class CenterParcsScraper(BaseScraper):

    provider = "centerparcs"

    def scrape(self):

        for arrival in self.departure_dates:
            departure = arrival + timedelta(days=self.nights)

            adults = self.adults
            children = len(self.children)

            regions = self.regions
            accommodation_types = self.accommodation_types
            min_capacity = self.min_capacity



        # Voor nu alleen even loggen zodat we zien dat de YAML wordt gebruikt.
        print(f"CenterParcs: DUMMY TEST {arrival}")

        deals = [
            Deal(
                source="Center Parcs",
                title="De Vossemeren",
                location="Lommel",
                region="hier",
                countrycode="nl",
                price=696,
                url="https://www.centerparcs.nl/",
                arrival_date=self.departure_dates[0],
            )
        ]

        return deals