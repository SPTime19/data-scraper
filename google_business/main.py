from fire import Fire
from googlemaps import GoogleMapsScraper
import json
import utils.util as sc
from pathlib import Path
from datetime import datetime
from companies import STORES


class GmapParse:

    def __init__(self, debug: bool = False):
        self.scraper = GoogleMapsScraper(debug=debug)
        pass

    def parseStore(self, company, n_reviews: int = 10):
        if company in STORES:
            print(f"[*] Scraping '{company}'...")
            output_folder = Path(sc.check_folder("output"))
            for idx, store_url in enumerate(STORES[company]):
                print(f"[*] Scraping now from '{store_url}'!")
                print(f"{idx+1} out of {len(STORES[company])} links...")
                error = self.scraper.sort_by_date(store_url)
                if error == 0:
                    n = 0
                    file = output_folder / f"gbusiness_{company}_{datetime.utcnow().strftime('%Y-%m-%d-T%H-%M-%SZ')}.jl"
                    while n < n_reviews:
                        reviews = self.scraper.enrich_reviews(self.scraper.get_reviews(n), store_url, company)
                        with file.open("a", encoding="utf-8") as js:
                            for r in reviews:
                                js.write(json.dumps(r) + "\n")
                        if len(reviews) == 0:
                            n += 100
                        else:
                            n += len(reviews)
                else:
                    print(f"[*] Could not scrape link '{store_url}'. Link will be stored @error.log for further retries.")
                    with Path("error.log").open("a", encoding="utf-8") as js:
                        js.write(str(store_url) + "\n")
        else:
            raise Exception(f"Company '{company}' not found!")




if __name__ == '__main__':
    Fire(GmapParse)
