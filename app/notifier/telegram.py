from telegram import Bot
from app.config.settings import settings
from app.core.logging import logger


class TelegramNotifier:

    def __init__(self):
        self.bot = Bot(token=settings.telegram_bot_token)

    async def send_message(self, text: str):
        try:
            await self.bot.send_message(
                chat_id=settings.telegram_chat_id,
                text=text,
            )
        except Exception as e:
            logger.exception("Telegram versturen mislukt: %s", e)