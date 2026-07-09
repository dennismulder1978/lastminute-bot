from abc import ABC, abstractmethod
import logging
import requests


class BaseScraper(ABC):

    provider = "unknown"


    def __init__(self, config):
        self.config = config

        self.logger = logging.getLogger(f"scraper.{self.provider}")

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HolidayHunter/1.0 (+https://github.com/...)"
        })

        # Gedeelde configuratie
        self.family = config["family"]
        self.trip = config["trip"]
        self.provider_config = config["providers"].get(self.provider, {})

    @property
    def adults(self):
        return self.family["adults"]

    @property
    def children(self):
        return self.family["children"]

    @property
    def departure_dates(self):
        return self.trip["departure_dates"]

    @property
    def nights(self):
        return self.trip["nights"]

    @property
    def accommodation_types(self):
        return self.provider_config.get("accommodation_types", [])

    @property
    def regions(self):
        return self.provider_config.get("regions", [])

    @property
    def min_capacity(self):
        return self.provider_config.get("min_capacity")

    @property
    def min_bedrooms(self):
        return self.provider_config.get("min_bedrooms")

    @abstractmethod
    def scrape(self):
        pass

    def get(self, url, **kwargs):
        timeout = kwargs.pop("timeout", 15)

        try:
            self.logger.debug("GET %s", url)

            response = self.session.get(
                url,
                timeout=timeout,
                **kwargs
            )

            response.raise_for_status()
            return response

        except requests.RequestException as exc:
            self.logger.error(
                "HTTP request mislukt voor %s: %s",
                url,
                exc
            )
            raise

    def post(self, url, **kwargs):
        timeout = kwargs.pop("timeout", 15)

        try:
            self.logger.debug("POST %s", url)

            response = self.session.post(
                url,
                timeout=timeout,
                **kwargs
            )

            response.raise_for_status()
            return response

        except requests.RequestException as exc:
            self.logger.error(
                "HTTP POST mislukt voor %s: %s",
                url,
                exc
            )
            raise