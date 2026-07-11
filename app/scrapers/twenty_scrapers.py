from app.constants.accommodation_mapping import TWENTY_MAPPING
from app.scrapers.twenty import TwentyScraper


class AllcampsScraper(TwentyScraper):

    provider = "allcamps"
    BASE_URL = "https://www.allcamps.nl"
    TENANT = "allcamps"
    LOCALE = "nl"

    ACCOMMODATION_MAPPING = TWENTY_MAPPING


class VacanceSelectScraper(TwentyScraper):

    provider = "vacanceselect"
    BASE_URL = "https://www.vacanceselect.com"
    TENANT = "vacanceselect"
    LOCALE = "couk"

    ACCOMMODATION_MAPPING = TWENTY_MAPPING


class LuxCampScraper(TwentyScraper):

    provider = "luxcamp"
    BASE_URL = "https://lux-camp.nl"
    TENANT = "luxcamp"
    LOCALE = "nl"

    ACCOMMODATION_MAPPING = TWENTY_MAPPING
    

class FriferieScraper(TwentyScraper):

    provider = "friferie"
    BASE_URL = "https://www.friferie.dk"
    TENANT = "friferie"
    LOCALE = "dk"

    ACCOMMODATION_MAPPING = TWENTY_MAPPING
    
class DanskBilferieScraper(TwentyScraper):

    provider = "danskbilferie"

    BASE_URL = "https://danskbilferie.dk"
    TENANT = "danskbilferie"
    LOCALE = "dk"

    ACCOMMODATION_MAPPING = TWENTY_MAPPING