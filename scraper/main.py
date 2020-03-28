import fire
from pathlib import Path
from typing import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import shutil
from utils import util as sc
from datetime import datetime
import uuid


class DS4AScrap:

    def __init__(self, store_name: str, page_start: int = 1, page_end: int = 2):
        self.settings = get_project_settings()
        self.page_start = int(page_start)
        self.page_end = int(page_end)
        self.store_name = store_name
        self.utc_format = '%Y-%m-%dT%H-%M-%SZ'

    def start_crawl(self, spider_name, allowed_domains: List[str], start_urls: List[str]):
        process = CrawlerProcess(settings=self.settings)
        process.crawl(spider_name, p_allowed_domains=allowed_domains, p_start_urls=start_urls)
        process.start()  # the script will block here until the crawling is finished

    def clear_job_folder(self):
        if "JOBDIR" in self.settings and Path(self.settings["JOBDIR"]).exists():
            shutil.rmtree(self.settings["JOBDIR"])

    def format_output_file(self, website_name):
        if "FEED_URI" in self.settings:
            file_name = f"listing_{website_name}_{datetime.utcnow().strftime(self.utc_format)}.jl"
            output_folder = sc.check_folder(
                str(Path(self.settings["FEED_URI"]).parent) + "_" + datetime.utcnow().strftime("%Y-%m-%d"))
            self.settings["FEED_URI"] = str(Path(output_folder) / file_name)

    def scrapeReclameAqui(self):
        self.clear_job_folder()
        self.format_output_file(website_name="ReclameAqui")
        START_URL = [
            f"https://www.reclameaqui.com.br/empresa/{self.store_name}/lista-reclamacoes/?pagina={page}" for
            page in range(self.page_start, self.page_end + 1)]
        self.start_crawl("ReclameAqui", ["reclameaqui.com.br"], START_URL)


if __name__ == '__main__':
    fire.Fire(DS4AScrap)
