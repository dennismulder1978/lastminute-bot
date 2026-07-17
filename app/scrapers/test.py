from app.scrapers.eurocamps import EurocampScraper
from app.config.config_loader import load_config

def main():
    scraper = EurocampScraper(config=load_config())
    result = list()
    for i in range(5):
        try:
            result = scraper.scrape()
            if type(result) == list:
                continue
        except Exception:
            print(f"{i}: {Exception}")

    for each in result:
        print(each)

if __name__ == "__main__":
    main()