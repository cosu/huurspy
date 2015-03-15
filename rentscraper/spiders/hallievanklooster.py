# -*- coding: utf-8 -*-
from scrapy import Spider, Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot


class HallievankloosterLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()


class HallievankloosterSpider(Spider):
    name = "hallievanklooster"
    allowed_domains = ["www.hallie-vanklooster.nl"]
    start_urls = (
        'http://www.hallie-vanklooster.nl/huizen/smartselect.aspx?prefilter=Huuraanbod',
        'http://www.hallie-vanklooster.nl/huizen/smartselect.aspx?prefilter=Huuraanbod&pageNum=1'
    )



    def parse(self, response):

        selector = Selector(response)
        for listed_ad in selector.css(".ElementContainer"):
            l = HallievankloosterLoader(item=AdvertisedItem(), selector=listed_ad)

            l.add_css("street", ".adres")
            l.add_css("place", ".plaatsnaam::text",  re="(\w+\s*)+")
            l.add_xpath("surface", ".//tr[3]/td[4]/text()", re="\d+")
            l.add_xpath("rooms", ".//tr[6]/td[4]/text()", re="\d+")
            l.add_xpath("link", ".//h3/a/@href")
            l.add_css("price", ".element_prijs2.prijs_aktief", MapCompose(remove_dot), re="(\d+\.*\d+)")
            l.add_value("source", self.name)
            l.add_value("html", listed_ad.extract())

            yield l.load_item()


