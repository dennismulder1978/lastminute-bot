class LuxCampScraper(TwentyScraper):

    provider = "luxcamp"

    BASE_URL = "https://lux-camp.nl"

    URL_SITES = (
        "https://lux-camp.nl/api/twenty/v2/luxcamp/nl/search/sites"
    )

    URL_ACCOMMODATIONS = (
        "https://lux-camp.nl/api/twenty/v2/luxcamp/nl/search/accommodations"
    )

    ACCOMMODATION_MAPPING = ALLCAMPS_MAPPING