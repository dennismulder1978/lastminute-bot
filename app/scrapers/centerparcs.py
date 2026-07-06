from app.models.deal import Deal
from app.scrapers.base import BaseScraper


class CenterParcsScraper(BaseScraper):

    def search(self):

        return [

            Deal(
                source="Center Parcs",
                title="De Vossemeren",
                location="België",
                price=799,
                url="https://www.centerparcs.nl"
            )

        ]