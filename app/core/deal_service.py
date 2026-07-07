from app.core.logging import logger


class DealService:

    def __init__(self, notifier):
        self.notifier = notifier

    async def process(self, deals):

        for deal in deals:

            logger.info(
                "%s | %s | €%s",
                deal.source,
                deal.title,
                deal.price,
            )

            await self.notifier.send_message(
                f"""🏖️ Nieuwe deal!

Bron: {deal.source}
Bestemming: {deal.title}
Prijs: €{deal.price}
"""
            )