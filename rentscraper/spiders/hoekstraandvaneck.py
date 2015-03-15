from scrapy import Selector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot

# http://hoekstraenvaneck.nl/MenuID/2890/Woning/Verhuur/

class HoekstraenvaneckLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()


class HoekstraenvaneckSpider(CrawlSpider):
    name = "hoekstraenvaneck"
    allowed_domains = ["hoekstraenvaneck.nl"]

    start_urls = (
        'http://hoekstraenvaneck.nl/MenuID/2890/Woning/Verhuur/',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'Woning/MenuID/2890/Verhuur/1/Pagina/',),
                               restrict_xpaths=('//span[@id="Main_ctl00_PageNumbers"]'),
                               ),
             callback='parse_page',
             follow=True),
    )

    def parse_page(self, response):
        selector = Selector(response)
        for listed_ad in selector.css(".woning"):
            l = HoekstraenvaneckLoader(item=AdvertisedItem(), selector=listed_ad)

            l.add_css("street", ".straat::text")
            l.add_css("place", ".plaats::text")
            l.add_css("link", ".woninglink::attr(onclick)", re="='(.+)'")
            l.add_css("price", ".detailsrechts", MapCompose(remove_dot), re="(\d+\.*\d+)")

            l.add_value("source", self.name)
            l.add_value("html", listed_ad.extract())

            yield l.load_item()

    parse_start_url = parse_page