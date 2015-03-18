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


def _extract_street(description):
    return description.split(",")[1].strip()


def _extract_place(description):
    return description.split(",")[2].strip()


def _extract_type(description):
    return description.split(",")[0].strip()


class RotsvastLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, remove_dot)
    parking_in = MapCompose(default_input_processor, has_pp)
    street_in = MapCompose(default_input_processor, _extract_street)
    place_in = MapCompose(default_input_processor, _extract_place)


class RotsvastSpider(CrawlSpider):
    name = 'rotsvast'

    allowed_domains = ["rotsvast.nl"]
    start_urls = ['http://www.rotsvast.nl/nl/zoeken/']
    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www.rotsvast.nl/nl/huuraanbod/page-')), callback='parse_page',
             follow=True),)

    def __init__(self, city=None, *args, **kwargs):
        super(RotsvastSpider, self).__init__(*args, **kwargs)
        self.start_urls[0] = self.start_urls[0]+city

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
            l.add_xpath("surface", ".//p[3]", re="(\d{2,})m")
            l.add_xpath("rooms", ".//p[3]", re="(\d) kamer")
            l.add_value("base_address", response.url)
            l.add_value("html", listed_ad.extract())


            yield l.load_item()

    # this is to alo parse the start page. There might be a better way I guess.
    parse_start_url = parse_page