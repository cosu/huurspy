# -*- coding: utf-8 -*-
from scrapy import Spider, Selector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem


class PerfectHousingLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    place_in = MapCompose(default_input_processor, lambda x: x.split(",")[-1].strip())
    street_in = MapCompose(default_input_processor, lambda x: x.split(",")[0].strip())


class PerfecthousingSpider(CrawlSpider):
    name = "perfecthousing"
    allowed_domains = ["www.perfecthousing.com"]
    start_urls = (
        'http://www.perfecthousing.com/rental-apartments&rpp=50',
    )

    rules = (
        Rule(
            LxmlLinkExtractor(
                allow=("http://www.perfecthousing.com/rental-apartments",),
                restrict_xpaths=('//span[@class="pagingItems"]',),
            ),
            callback='parse_page', follow=True, ),)

    def parse_page(self, response):
        selector = Selector(response)
        for listed_ad in selector.css(".property"):
            l = PerfectHousingLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_xpath("surface", ".//td[3]/strong", re="\d+")
            l.add_xpath("rooms", ".//td[2]/strong", re="\d+")
            l.add_xpath("price", ".//td[1]/strong", re="(\d+\.*\d+)")
            l.add_xpath("street", ".//h3/a/text()", re="(.*),")
            l.add_xpath("place", ".//h3/a/text()")
            l.add_value("base_address", response.url)
            l.add_value("source", self.name)
            l.add_xpath("link", ".//h3/a/@href")
            l.add_xpath("hood", ".//h3/a/text()", re=",(.+),")
            l.add_value("html", listed_ad.extract())


            yield l.load_item()

    parse_start_url = parse_page



