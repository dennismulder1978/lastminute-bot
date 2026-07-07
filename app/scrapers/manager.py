from app.scrapers.centerparcs import CenterParcsScraper


def run_scrapers(config):

    scrapers = [
        CenterParcsScraper(config),
    ]

    deals = []

    for scraper in scrapers:
        deals.extend(scraper.scrape())

    return deals