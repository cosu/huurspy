from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot
from rentscraper.util import has_pp


__author__ = 'cosmin'


class JacobusLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, remove_dot)
    parking_in = MapCompose(default_input_processor, has_pp)


class JacobusSpider(CrawlSpider):
    name = 'jacobus'
    start_urls = ['http://jacobusrecourt.nl/MenuID/3566/Woning/Verhuur/Chapter/Huurwoningen/']
    allowed_domains = ["jacobusrecourt.nl"]
    rules = (Rule(SgmlLinkExtractor(allow=('Huurwoningen/Verhuur/1/Pagina/')), callback='parse_page', follow=True),)

    def parse_page(self, response):
        selector = Selector(response)
        for listed_ad in selector.xpath("//div[@class='woning']"):
            l = JacobusLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_xpath("link", ".//a[@class='detaillink']/@href")
            l.add_xpath("price", ".//span[@class='prijs right']", re="(\d+\.*\d+)")
            l.add_xpath("place", ".//span[@class='plaats']")
            l.add_xpath("street", ".//span[@class='straat']", re="(([A-Za-z]+\s*)+\d+)")
            l.add_xpath("parking", ".//span[@class='straat']")
            l.add_xpath("availability", ".//div[@class='beschikbaarper']//span")
            l.add_xpath("rooms", ".//div[@class='slaapkamers']//span")
            l.add_xpath("type", ".//div[@class='soortobject']//span")
            l.add_value("base_address", response.url)
            l.add_value("source", self.name)

            yield l.load_item()

    # this is to also parse the start page. There might be a better way I guess.
    parse_start_url = parse_page