from dataclasses import dataclass
from datetime import date

@dataclass
class Deal:
    source: str
    title: str
    location: str
    region: str
    countrycode: str
    price: float
    url: str
    arrival_date: date
    accommodation_type: str | None = None
    bedrooms: int | None = None
    capacity: int | None = None
    airconditioning: bool | None = None
    pets_allowed: bool | None = None
    comfort_level: str | None = None