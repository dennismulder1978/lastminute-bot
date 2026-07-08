from app.core.logging import logger
from app.scrapers import SCRAPERS
from app.filters.deal_filter import DealFilter


def run_scrapers(config):

    providers = config.get("providers", {})
    deal_filter = DealFilter(config)
    filtered_deals = []

    for provider_name, scraper_class in SCRAPERS.items():

        provider_config = providers.get(provider_name, {})

        if not provider_config.get("enabled", False):
            logger.info("%s is disabled", provider_name)
            continue

        scraper = scraper_class(config)

        try:
            logger.info("Starting %s", scraper.__class__.__name__)

            scraper_deals = scraper.scrape()

            accepted = 0

            for deal in scraper_deals:
                if deal_filter.matches(deal):
                    filtered_deals.append(deal)
                    accepted += 1

            logger.info(
                "%s: %d/%d deals accepted",
                scraper.__class__.__name__,
                accepted,
                len(scraper_deals),
            )

        except Exception:
            logger.exception("%s failed", scraper.__class__.__name__)

    return filtered_deals