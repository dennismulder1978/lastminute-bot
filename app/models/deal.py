from dataclasses import dataclass


@dataclass
class Deal:
    source: str
    title: str
    location: str
    price: float
    url: str