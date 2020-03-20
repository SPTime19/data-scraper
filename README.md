# Scraper

## Setup

Install dependencies
> pip install -r requirements

Also, you need to download chromium driver to run
https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/

Then change SELENIUM_DRIVER_EXECUTABLE_PATH @ scraper/settings.py to bin path.

## Run

Will run reclameAqui spider for the first two pages.

> python main.py --store_name=magazine-luiza-loja-online --page_start=1 --page_end=2 scrapeReclameAqui

## Roadmap

[ ] Google business/map scrap