import asyncio
import logging

from app.config.settings import settings
from app.core.deal_service import DealService
from app.database.db import initialize_database
from app.notifier.telegram import TelegramNotifier
from app.scheduler import scheduler
from app.scrapers.manager import run_scrapers
from app.config.config_loader import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)
config = load_config()

async def holiday_job(deal_service: DealService):
    logger.info("Zoeken naar vakanties...")

    await run_scrapers(
        config,
        deal_service.process,
    )


async def main():

    logger.info("HolidayHunter starting...")

    initialize_database()
    logger.info("Database initialized")

    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN ontbreekt")

    if not settings.telegram_chat_id:
        raise RuntimeError("TELEGRAM_CHAT_ID ontbreekt")

    notifier = TelegramNotifier()
    deal_service = DealService(notifier)

    logger.info("Telegram initialized")

    await notifier.send_message("🚀 HolidayHunter gestart")

    # Meteen één keer uitvoeren
    await holiday_job(deal_service)


    # Iedere XX seconden
    scheduler.add_job(
        holiday_job,
        "interval",
        seconds=config.get('scheduler').get('interval_seconds'),
        args=[deal_service],
        id="holiday_search",
        replace_existing=True,
    )

    scheduler.start()

    logger.info("Scheduler gestart")

    # Applicatie actief houden
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("HolidayHunter gestopt")


if __name__ == "__main__":
    asyncio.run(main())