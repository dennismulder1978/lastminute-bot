import logging


class DealFilter:

    def __init__(self, config):
        self.filters = config.get("filters", {})
        self.logger = logging.getLogger("deal_filter")

    def matches(self, deal):

        # max price
        max_price = self.filters.get("max_price")
        if (
            max_price is not None
            and deal.price is not None
            and deal.price > max_price
        ):
            return False

        #country
        countries = self.filters.get("countries")
        if countries and deal.countrycode not in countries:
            return False

        #bedrooms
        bedrooms = self.filters.get("bedrooms")

        if bedrooms is not None and deal.bedrooms is not None:
            if deal.bedrooms != bedrooms:
                self.logger.info(
                    "Filtered: %s (bedrooms %s != %s)",
                    deal.title,
                    deal.bedrooms,
                    bedrooms,
                )
                return False

        # min cap
        min_capacity = self.filters.get("min_capacity")

        if min_capacity is not None and deal.capacity is not None:
            if deal.capacity < min_capacity:
                self.logger.info(
                    "Filtered: %s (capacity %s < %s)",
                    deal.title,
                    deal.capacity,
                    min_capacity,
                )
                return False


        return True