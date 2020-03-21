from fire import Fire
from googlemaps import GoogleMapsScraper
import json
import utils.util as sc
from pathlib import Path
from datetime import datetime
from companies import STORES


def get_cep(location):
    locs = location.split(" - ")
    cep = locs[-1].split()[-1]
    return cep


class GmapParse:

    def __init__(self, debug: bool = False):
        self.scraper = GoogleMapsScraper(debug=debug)
        pass

    def parseStore(self, company, n_reviews: int = 10):
        if company in STORES:
            output_folder = Path(sc.check_folder("output"))
            for store in STORES[company]:
                error = self.scraper.sort_by_date(store["url"])
                if error == 0:
                    n = 0
                    file = output_folder / f"gbusiness_{company}_{get_cep(store['location'])}_{datetime.utcnow().strftime('%Y-%m-%d-T%H-%M-%SZ')}.jl"
                    while n < n_reviews:
                        reviews = self.scraper.get_reviews(n)
                        with file.open("a", encoding="utf-8") as js:
                            for r in reviews:
                                js.write(json.dumps(r) + "\n")
                        n += len(reviews)
        else:
            raise Exception(f"Company '{company}' not found!")


if __name__ == '__main__':
    Fire(GmapParse)
