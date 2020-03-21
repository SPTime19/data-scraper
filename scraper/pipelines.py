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

    def try_parse_RA_date(self, date: str):
        try:
            # date parsing "20/03/20 às 13h35"
            date = datetime.strptime(date, "%d/%m/%y às %Hh%M")
            return date.strftime(self.utc_format)
        except:
            return None

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
                else:
                    date = self.try_parse_RA_date(data)
                    if date:
                        item["datetime"] = date
            item.pop(field)

    def add_timeCaptured(self, item):
        item["timeCaptured"] = datetime.utcnow().strftime(self.utc_format)

    def parse_reply(self, html_section, reply_class):
        b_replies = [i for i in html_section.find_all("div", {"class": reply_class})]
        formatted_replies = []
        for b_reply in b_replies:
            formatted_reply = dict()

            date = [i for i in b_reply.find_all("p", {"class": "date"})]  # 11/03/20 às 14h47
            if len(date) > 0:
                dt = self.try_parse_RA_date(date[0].text.strip())
                if dt:
                    formatted_reply["datetime"] = dt

            content = [i for i in b_reply.find_all("div", {"class": "reply-content"})]
            if len(content) > 0:
                formatted_reply["content"] = content[0].text.strip()

            formatted_replies.append(formatted_reply)
        return formatted_replies

    def parse_response(self, item):
        field = "company_response"
        if field in item:
            doc = BeautifulSoup(self.unpack_field(item, field), "html.parser")

            responses = {"business":[], "customer":[], "final": dict()}

            # Parse replies
            responses["business"] = self.parse_reply(doc, "business-reply")
            responses["customer"] = self.parse_reply(doc, "user-reply")

            # Parse final response
            # try 2 find a positive final answ
            final_class = None
            if len([i for i in doc.find_all("div", {"class": "user-upshot-green"})]) > 0:
                final_class = "user-upshot-green"
                responses["final"]["result"] = "positive"
            elif len([i for i in doc.find_all("div", {"class": "user-upshot-purple"})]) > 0:
                final_class = "user-upshot-purple"
                responses["final"]["result"] = "negative"

            if final_class:
                responses["final"]["reply"] = self.parse_reply(doc, final_class)

                score_seals = [i for i in doc.find_all("div", {"class": "score-seal"})]
                seals = []
                if len(score_seals) > 0:
                    for seal in score_seals:
                        split_seal = [o.strip() for o in seal.text.split("  ") if o != ""]
                        if len(split_seal) == 2:
                            seals.append({"seal": split_seal[0], "value": split_seal[-1]})

                responses["final"]["seals"] = seals

            item.pop("company_response")
            item["responses"] = responses


    def process_item(self, item, spider):
        self.parse_text_field(item, "description")
        self.parse_text_field(item, "title")
        self.parse_text_field(item, "business_name")
        self.parse_tags(item)
        self.parse_answered(item)
        self.parse_locale(item)
        self.parse_response(item)
        self.add_timeCaptured(item)

        return item
