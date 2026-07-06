from abc import ABC, abstractmethod
from app.models.deal import Deal


class BaseScraper(ABC):

    @abstractmethod
    def search(self) -> list[Deal]:
        """Zoek deals"""
        raise NotImplementedError