from abc import ABC, abstractmethod
import logging
import requests


class BaseScraper(ABC):

    provider = "unknown"

    def __init__(self, config):
        self.config = config

        self.logger = logging.getLogger(
            f"scraper.{self.provider}"
        )

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "HolidayHunter/1.0 (+https://github.com/...)"
        })

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