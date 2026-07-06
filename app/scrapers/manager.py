from app.models.deal import Deal


class ScraperManager:

    def __init__(self):
        self.scrapers = []

    def register(self, scraper):
        self.scrapers.append(scraper)

    def run(self) -> list[Deal]:

        deals = []

        for scraper in self.scrapers:
            deals.extend(scraper.search())

        return deals