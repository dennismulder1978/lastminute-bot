import asyncio

from app.core.logging import logger
from app.filters.deal_filter import DealFilter
from app.scrapers import SCRAPERS


async def run_scrapers(config, process_callback):

    providers = config.get("providers", {})
    deal_filter = DealFilter(config)

    delay = config.get("scrapers", {}).get(
        "delay_between_providers",
        60,
    )

    for provider_name, scraper_class in SCRAPERS.items():

        provider_config = providers.get(provider_name, {})

        if not provider_config.get("enabled", False):
            logger.info("%s is disabled", provider_name)
            continue

        scraper = scraper_class(config)

        try:
            logger.info("Starting %s", scraper.__class__.__name__)

            scraper_deals = scraper.scrape()

            filtered_deals = []

            for deal in scraper_deals:
                if deal_filter.matches(deal):
                    filtered_deals.append(deal)

            logger.info(
                "%s: %d/%d deals accepted",
                scraper.__class__.__name__,
                len(filtered_deals),
                len(scraper_deals),
            )

            # Verwerk direct de deals van deze provider
            if filtered_deals:
                await process_callback(filtered_deals)

                logger.info(
                    "Wachten %d seconden voor volgende provider...",
                    delay,
                )

                await asyncio.sleep(delay)

        except Exception:
            logger.exception("%s failed", scraper.__class__.__name__)