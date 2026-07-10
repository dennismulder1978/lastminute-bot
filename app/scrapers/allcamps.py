from app.constants.accommodation_mapping import TWENTY_MAPPING
from app.scrapers.twenty import TwentyScraper


class AllcampsScraper(TwentyScraper):

    provider = "allcamps"

    BASE_URL = "https://www.allcamps.nl"

    URL_SITES = (
        "https://www.allcamps.nl/api/twenty/v2/"
        "allcamps/nl/search/sites"
    )

    URL_ACCOMMODATIONS = (
        "https://www.allcamps.nl/api/twenty/v2/"
        "allcamps/nl/search/accommodations"
    )

    ACCOMMODATION_MAPPING = TWENTY_MAPPING