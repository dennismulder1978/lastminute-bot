from app.scrapers.centerparcs import CenterParcsScraper
from app.scrapers.landal import LandalScraper
from app.scrapers.roompot import RoompotScraper
from app.scrapers.roan import RoanScraper
from app.scrapers.eurocamps import EurocampScraper
from app.scrapers.twenty_scrapers import AllcampsScraper, VacanceSelectScraper, LuxCampScraper, FriferieScraper, DanskBilferieScraper
from app.scrapers.yelloh import YellohScraper

SCRAPERS = {
    "centerparcs": CenterParcsScraper,
    "landal": LandalScraper,
    "roompot": RoompotScraper,
    "roan": RoanScraper,
    "eurocamp": EurocampScraper,
    "allcamps": AllcampsScraper,
    "vacanceselect": VacanceSelectScraper,
    "luxcamp": LuxCampScraper,
    "friferie": FriferieScraper,
    "danskbilferie": DanskBilferieScraper,
    "yelloh": YellohScraper,
}