# -*- coding: utf-8 -*-
from scrapy import Spider, Selector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.spiders import Rule, CrawlSpider
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot


class HousingLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, remove_dot)


class HousingnetSpider(CrawlSpider):
    name = "housingnet"
    start_urls = (
        'http://www.housingnet.nl/woningaanbod/nederland',
    )
    rules = (
        Rule(
            LxmlLinkExtractor(
                              allow=("http://www.housingnet.nl/woningaanbod/nederland",),
                              restrict_xpaths=('//div[@class="browserDiv"]',),
                              ),
            callback='parse_page', follow=True, ),)


    def parse_page(self, response):
        selector = Selector(response)
        for listed_ad in selector.css(".pandList"):
            l = HousingLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_xpath("price", ".//span[4]", re="(\d+\.*\d+)")
            l.add_xpath("place", ".//h3/text()", re="\w+")
            l.add_xpath("street", ".//h3/text()", re="\w+ - \w+ (.*)")
            l.add_xpath("surface", ".//span[6]", re="\d+")
            l.add_xpath("rooms", ".//span[10]")
            l.add_xpath("furnished", ".//span[8]")
            l.add_value("base_address", "")
            l.add_value("source", self.name)
            l.add_css("link", "::attr(onclick)", re="='(.+)'")

            yield l.load_item()


    parse_start_url = parse_page