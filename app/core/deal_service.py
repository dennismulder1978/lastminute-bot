from app.core.logging import logger
from app.database.manager import DatabaseManager


class DealService:

    def __init__(self, notifier):
        self.notifier = notifier
        self.db = DatabaseManager()

    async def process(self, deals):

        for deal in deals:

            existing = self.db.get_deal(deal)

            # Nieuwe deal
            if existing is None:

                self.db.insert_deal(deal)

                await self.notifier.send_message(
                    f"""🏖️ Nieuwe deal

                Bron: {deal.source}
                Bestemming: {deal.title}
                Regio: {deal.region}
                Aankomst: {deal.arrival_date:%d-%m-%Y}
                Prijs: €{deal.price:.2f}

                {deal.url}
                """
                )

                logger.info(
                    "%s | %s | %s | %s | €%.2f",
                    deal.source,
                    deal.arrival_date,
                    deal.title,
                    deal.region,
                    deal.price,
                )

                logger.info("%s", deal.url)

                continue

            # Bestaande deal
            _, old_price = existing

            if old_price != deal.price:

                self.db.update_price(deal)

            if abs(old_price - deal.price) >= 5:
                await self.notifier.send_message(
                    f"""💰 Prijs gewijzigd

                Bron: {deal.source}
                Bestemming: {deal.title}
                Regio: {deal.region}
                Aankomst: {deal.arrival_date:%d-%m-%Y}

                €{old_price:.2f} → €{deal.price:.2f}

                {deal.url}
                """
                )

                logger.info(
                    "%s | %s | %s | %s | €%.2f",
                    deal.source,
                    deal.arrival_date,
                    deal.title,
                    deal.region,
                    deal.price,
                )

                logger.info("%s", deal.url)