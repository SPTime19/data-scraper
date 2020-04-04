# Scraper

## Setup

Install dependencies
> pip install -r requirements

Also, you need to download chromium driver to run
https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/

Then change SELENIUM_DRIVER_EXECUTABLE_PATH @ scraper/settings.py to bin path.

## Run

> python main.py --store_name=[RA STORE NAME] --page_start=[PAGE START (int)] --page_end=[PAGE END (int)] scrapeReclameAqui

Will run reclameAqui spider for the first two pages.
Ex:
> python main.py --store_name=magazine-luiza-loja-online --page_start=1 --page_end=2 scrapeReclameAqui


## Windows powershell script
* Download and install powershell (if not yet installed)
* Open powershell and execute (may ask for adm privileges)
> Set-ExecutionPolicy Unrestricted
* Open script file ("win_auto_scrape.ps1"") with text editor
* Edit script variable "storesIds" adding ReclameAqui stores ids
* Using anaconda powershell, run with:

> .\win_auto_scrape -pageStart=1 -pageMax=200 -step=20


