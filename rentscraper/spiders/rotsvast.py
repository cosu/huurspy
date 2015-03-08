from scrapy import Selector, Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot
from rentscraper.util import has_pp

__author__ = 'cdumitru'


def _extract_street_from_description(description):
    return description.split(",")[1].strip()


def _extract_place_from_description(description):
    return description.split(",")[2].strip()


def _extract_type_from_description(description):
    return description.split(",")[0].strip()


def _extract_surface_from_description(description):
    return description.split("-")[0].split(":")[1]


def _extract_rooms_from_description(description):
    return description.split("-")[1].split()[0]


class RotsvastLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_dot, default_input_processor)
    parking_in = MapCompose(has_pp, default_input_processor)
    street_in = MapCompose(_extract_street_from_description, default_input_processor)
    place_in = MapCompose(_extract_place_from_description, default_input_processor)
    rooms_in = MapCompose(_extract_rooms_from_description, default_input_processor)
    surface_in = MapCompose(_extract_surface_from_description, default_input_processor)


class RotsvastSpider(CrawlSpider):
    name, start_urls = 'rotsvast', ['http://www.rotsvast.nl/nl/zoeken/rotterdam']
    rules = (
    Rule(SgmlLinkExtractor(allow=('http://www.rotsvast.nl/nl/huuraanbod/page-')), callback='parse_page', follow=True),)

    def parse_page(self, response):
        selector = Selector(response)
        # yes that's a space in the class name ...
        for listed_ad in selector.xpath("//div[@class='objectsummary ']"):
            l = RotsvastLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_value("source", self.name)
            l.add_xpath("link", ".//a/@href")
            l.add_xpath("price", ".//div[@class='prijs']", re="(\d+\.*\d+)")
            l.add_xpath("place", ".//h4")
            l.add_xpath("availability", ".//div[@class='ingangsdatum']")
            l.add_xpath("street", ".//h4")
            l.add_xpath("parking", ".//p[2]")
            l.add_xpath("postcode", ".//p[1]")
            l.add_xpath("surface", ".//p[3]")
            l.add_xpath("rooms", ".//p[3]")

            yield l.load_item()