from scrapy.crawler import Crawler
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from scrapy import Spider, Item, Field
from scrapy.settings import Settings
from twisted.internet import reactor


__author__ = 'cosmin'


class AdvertisedItem(Item):
    street = Field()


class HuurSpider(Spider):
    name, start_urls = 'jacobusrecourt', ['http://jacobusrecourt.nl/MenuID/3566/Woning/Verhuur/Chapter/Huurwoningen/']

    def parse(self, response):

        item = AdvertisedItem()

        hxs = HtmlXPathSelector(response)

        item['street'] = hxs.select("//span[@class='straat']/text()").extract()[0]

        return item






if __name__ == '__main__':
    spider = HuurSpider()
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()
