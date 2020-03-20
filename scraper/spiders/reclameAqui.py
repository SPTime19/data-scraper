import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import Rule

from ..items import ScraperItem
from ..utils.processor import Item, Field

log = logging.getLogger(__name__)
from scrapy_selenium import SeleniumRequest
from scrapy.utils.response import get_base_url


class RequiredFieldMissing(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class DS4AItemLoader(ItemLoader):
    def get_value(self, value, *processors, **kw):
        required = kw.pop('required', False)
        val = super(DS4AItemLoader, self).get_value(value, *processors, **kw)
        if required and not val:
            raise RequiredFieldMissing(
                'Missing required field "{value}" for "{item}"'.format(
                    value=value, item=self.item.__class__.__name__))
        return val


class QuotesSpider(scrapy.Spider):
    name = "ReclameAqui"

    def __init__(self, p_allowed_domains, p_start_urls, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [*p_allowed_domains]
        self.start_urls = [*p_start_urls]
        self.market = "ReclameAqui"
        self.rules = [
            Rule(
                LinkExtractor(
                    allow=('.*'),
                    restrict_css=("ul.complain-list:nth-child(1)"),
                    unique=True
                ),
                callback='parse',
                process_links="filter_links",
                follow=True
            )
        ]

    items = [
        [
            Item(
                ScraperItem,
                None,
                u'html.ng-scope body ui-view.ng-scope div#complain-detail.ng-scope',
                [
                    Field(
                        u'title',
                        'h1.ng-binding',
                        []),
                    Field(
                        u'location_ate',
                        '.local-date',
                        []),
                    Field(
                        u'tags',
                        '.tags',
                        []),
                    Field(
                        u'description',
                        '.complain-body > p:nth-child(2)',
                        []),
                    Field(
                        u'img_response',
                        '.upshot-seal > span:nth-child(1) > img:nth-child(1)',
                        []),
                ])
        ]
    ]

    def load_item(self, definition, response):
        logging.debug("##Load_item")
        selectors = response.css(definition.selector)
        for selector in selectors:
            selector = selector if selector else None
            ld = DS4AItemLoader(
                item=definition.item(),
                selector=selector,
                response=response,
                baseurl=get_base_url(response)
            )
            for field in definition.fields:
                if hasattr(field, 'fields'):
                    if field.name is not None:
                        ld.add_value(field.name,
                                     self.load_item(field, selector))
                else:
                    if field.name is 'url':
                        ld.add_value(field.name, response._url)
                    else:
                        ld.add_css(field.name, field.selector, *field.processors, required=field.required)

            yield ld.load_item()

    def start_requests(self):
        log.debug("## Starting requests")
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=50)

    def parse(self, response):
        logging.debug("##Parsering")
        links = self.rules[0].link_extractor.extract_links(response=response)
        for href in links:
            yield SeleniumRequest(url=response.urljoin(href.url), callback=self.parse_my_item)

    def parse_my_item(self, response):
        logging.debug("##Parse_item")
        for sample in self.items:
            items = []
            try:
                for definition in sample:
                    items.extend(
                        [i for i in self.load_item(definition, response)]
                    )
            except RequiredFieldMissing as exc:
                self.logger.warning(str(exc))
            if items:
                for item in items:
                    yield item
                break
