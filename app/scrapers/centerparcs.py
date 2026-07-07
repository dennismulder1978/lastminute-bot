from app.models.deal import Deal
from app.scrapers.base import BaseScraper


class CenterParcsScraper(BaseScraper):

    def __init__(self, config):
        self.config = config

    def scrape(self):

        adults = self.config["family"]["adults"]
        children = self.config["family"]["children"]

        departure_dates = self.config["trip"]["departure_dates"]
        nights = self.config["trip"]["nights"]

        # Voor nu alleen even loggen zodat we zien dat de YAML wordt gebruikt.
        print(
            f"CenterParcs: {adults} volwassenen, "
            f"{len(children)} kinderen, "
            f"{departure_dates}, "
            f"{nights} nachten"
        )

        deals = [
            Deal(
                source="Center Parcs",
                title="De Vossemeren",
                location="Lommel",
                price=699,
                url="https://www.centerparcs.nl/",
            )
        ]

        return deals