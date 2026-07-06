import asyncio

from app.core.logging import logger
from app.database.db import initialize_database
from app.scrapers.manager import ScraperManager
from app.scrapers.centerparcs import CenterParcsScraper
from app.config.settings import settings
from app.notifier.telegram import TelegramNotifier


async def main():

    logger.info("HolidayHunter starting...")

    initialize_database()

    logger.info("Configuration loaded")
    logger.info("Database initialized")

    notifier = TelegramNotifier()

    logger.info("Telegram initialized")

    await notifier.send_message(
        "🚀 HolidayHunter is gestart!"
    )

    logger.info("Telegram test message sent")

    logger.info("HolidayHunter ready")

    manager = ScraperManager()

    manager.register(CenterParcsScraper())

    deals = manager.run()

    for deal in deals:
        logger.info("%s €%s", deal.title, deal.price)


if __name__ == "__main__":
    asyncio.run(main())