# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from bs4 import BeautifulSoup
from datetime import datetime


class ScraperPipeline(object):
    utc_format = "%Y-%m-%dT%H:%M:%SZ"

    def unpack_field(self, item, field: str):
        if field in item and type(item[field]) is list and len(item[field]) > 0:
            return item[field][0]

    def parse_text_field(self, item, field):
        if field in item:
            desc = self.unpack_field(item, field)
            item[field] = BeautifulSoup(desc, "html.parser").text

    def parse_answered(self, item):
        field = "img_response"
        if field in item:
            doc = BeautifulSoup(self.unpack_field(item, field))
            if len(doc.contents) > 0 and "title" in doc.contents[0].attrs:
                if doc.contents[0].attrs["title"] == 'Não Respondida':
                    item["review_answered"] = False
                else:
                    item["review_answered"] = True
            item.pop(field)

    def parse_tags(self, item):
        field = "tags"
        if field in item:
            doc = self.unpack_field(item, field)
            item[field] = [i.text for i in BeautifulSoup(doc).find_all("li")]

    def parse_locale(self, item):
        field = "location_ate"
        if field in item:
            doc = self.unpack_field(item, field)
            locales = [i.text.strip() for i in BeautifulSoup(doc).find_all("li")]
            for data in locales:
                if len(data.split("-")) == 2:  # Try parse location ex ' Recife - PE'
                    location = data.split("-")
                    item["uf"] = location[-1].strip()
                    item["city"] = location[0].strip()
                elif "ID" in data:  # ex 'ID: 101788939'
                    item["review_ID"] = data.split(":")[-1].strip()
                else:  # date parsing "20/03/20 às 13h35"
                    try:
                        date = datetime.strptime(data, "%d/%m/%y às %Hh%M")
                        item["datetime"] = date.strftime(self.utc_format)
                    except:
                        pass
            item.pop(field)

    def add_timeCaptured(self, item):
        item["timeCaptured"] = datetime.utcnow().strftime(self.utc_format)

    def process_item(self, item, spider):
        self.parse_text_field(item, "description")
        self.parse_text_field(item, "title")
        self.parse_tags(item)
        self.parse_answered(item)
        self.parse_locale(item)
        self.add_timeCaptured(item)

        return item
