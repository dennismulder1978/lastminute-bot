from app.core.logging import logger
from app.database.manager import DatabaseManager


class DealService:

    def __init__(self, notifier):
        self.notifier = notifier
        self.db = DatabaseManager()

    async def process(self, deals):

        for deal in deals:

            logger.info(
                "%s | %s | €%s",
                deal.source,
                deal.title,
                deal.price,
            )

            existing = self.db.get_deal(deal)

            # Nieuwe deal
            if existing is None:

                self.db.insert_deal(deal)

                await self.notifier.send_message(
                    f"""🏖️ Nieuwe deal!

Bron: {deal.source}
Bestemming: {deal.title}
Prijs: €{deal.price}
"""
                )

                continue

            # Bestaande deal
            _, old_price = existing

            if old_price != deal.price:

                self.db.update_price(deal)

                await self.notifier.send_message(
                    f"""💰 Prijs gewijzigd!

Bron: {deal.source}
Bestemming: {deal.title}

€{old_price} ➜ €{deal.price}
"""
                )