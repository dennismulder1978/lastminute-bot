import asyncio

from telegram import Bot
from telegram.error import TimedOut

from app.config.settings import settings
from app.core.logging import logger


class TelegramNotifier:

    def __init__(self):
        self.bot = Bot(token=settings.telegram_bot_token)

    async def send_message(self, text: str):
        max_attempts = 5

        for attempt in range(1, max_attempts + 1):
            try:
                await self.bot.send_message(
                    chat_id=settings.telegram_chat_id,
                    text=text,
                )
                return

            except TimedOut:
                if attempt == max_attempts:
                    logger.exception(
                        "Telegram timeout na %d pogingen.",
                        max_attempts,
                    )
                    return

                wait = 2 ** (attempt - 1)
                logger.warning(
                    "Telegram timeout (poging %d/%d). Opnieuw proberen over %d seconden...",
                    attempt,
                    max_attempts,
                    wait,
                )

                await asyncio.sleep(wait)

            except Exception as e:
                logger.exception("Telegram versturen mislukt: %s", e)
                return