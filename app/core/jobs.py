from app.scrapers.manager import ScraperManager
from app.scrapers.centerparcs import CenterParcsScraper


def run_scrapers():

    manager = ScraperManager()

    manager.register(CenterParcsScraper())

    return manager.run()