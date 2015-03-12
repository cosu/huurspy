# -*- coding: utf-8 -*-

from scrapy import Spider, Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot


def _extract_place(text):
    return text.split()[1]


class InterhouseLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, remove_dot)
    place_in = MapCompose(default_input_processor, _extract_place)
    # hood_in = MapCompose(default_input_processor, _extract_hood)
    # street_in = MapCompose(default_input_processor, _extract_street)

class InterhouseSpider(Spider):
    name = "interhouse"
    allowed_domains = ["http://www.interhouse.nl"]
    start_urls = (
        'http://amsterdam.interhouse.nl/nl/woningaanbod',
    )


    def parse(self, response):
        selector = Selector(response)


        for listed_ad in selector.css(".item"):
            l = InterhouseLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_xpath("link", ".//a/@href")
            l.add_xpath("street", ".//td[1]")
            l.add_xpath("place", ".//h1")
            l.add_xpath("price", './/td[@class="bold"]', re="(\d+\.*\d+)")
            l.add_value("base_address", response.url)
            l.add_value("source", self.name)

            yield l.load_item()
