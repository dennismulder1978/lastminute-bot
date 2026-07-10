from app.constants.accommodation_mapping import TWENTY_MAPPING
from app.scrapers.twenty import TwentyScraper


class VacanceSelectScraper(TwentyScraper):

    provider = "vacanceselect"

    BASE_URL = "https://www.vacanceselect.com"

    URL_SITES = (
        "https://www.vacanceselect.com/api/twenty/v2/"
        "vacanceselect/couk/search/sites"
    )

    URL_ACCOMMODATIONS = (
        "https://www.vacanceselect.com/api/twenty/v2/"
        "vacanceselect/couk/search/accommodations"
    )

    ACCOMMODATION_MAPPING = TWENTY_MAPPING