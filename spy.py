from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.crawler import Crawler
from scrapy.selector import  Selector
from scrapy import log
from scrapy import Spider, Item, Field
from scrapy.settings import Settings
from twisted.internet import reactor
from w3lib.html import remove_tags


__author__ = 'cosmin'


def remove_dot(string):
    return string.replace(".", "")


class AdvertisedLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_dot, default_input_processor)


class AdvertisedItem(Item):
    price = Field()
    street = Field()
    place = Field()
    link = Field()


class JacobusSpider(Spider):
    name, start_urls = 'jacobusrecourt', ['http://jacobusrecourt.nl/MenuID/3566/Woning/Verhuur/Chapter/Huurwoningen/']

    def parse(self, response):

        selector = Selector(response)
        for listed_ad in selector.xpath("//div[@class='woning']"):
            l = AdvertisedLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_xpath("link", ".//a[@class='detaillink']/@href")
            l.add_xpath("price", ".//span[@class='prijs right']", re="(\d+\.*\d+)")
            l.add_xpath("place", ".//span[@class='plaats']")
            l.add_xpath("street", ".//span[@class='straat']", re="(([A-Za-z]+\s*)+\d+)")

            yield l.load_item()



if __name__ == '__main__':

    spider = JacobusSpider()
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()
