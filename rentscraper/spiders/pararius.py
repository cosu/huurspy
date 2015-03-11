# -*- coding: utf-8 -*-
from scrapy import Selector, Spider
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.exceptions import CloseSpider
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot


def parse_location(text):
    result = {
        'place': None,
        'street': None,
        'hood': None,
        'type': None
    }

    tokens = text.split("-")

    tokens = [t.strip() for t in tokens]

    if len(tokens) == 3:
        result['place'] = tokens[1]
        result['hood'] = tokens[2]

        type_place = tokens[0].split()
        if len(type_place) == 2:
            result['type'] = type_place[0].strip()
            result['street'] = type_place[1].strip()
        else:
            result['street'] = tokens[0].strip()

    return result


def _extract_place(text):
    return parse_location(text)['place']


def _extract_street(text):
    return parse_location(text)['street']


def _extract_hood(text):
    return parse_location(text)['hood']


def _extract_price(text):
    return text.split(" ")[1].split(",")[0].strip()


class ParariusLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, _extract_price, remove_dot)
    place_in = MapCompose(default_input_processor, _extract_place)
    hood_in = MapCompose(default_input_processor, _extract_hood)
    street_in = MapCompose(default_input_processor, _extract_street)


class ParariusSpider(CrawlSpider):
    name = "pararius"
    allowed_domains = ["pararius.nl"]
    start_urls = [
        'http://www.pararius.nl/huurwoningen/%s/0-2000',
    ]

    rules = (
        Rule(LxmlLinkExtractor(allow=('http://www.pararius.nl/huurwoningen/amsterdam/0-2000/'),
                               restrict_xpaths=('//ul[@id="pagination-digg"]'), ),
             callback='parse_page',
             follow=True),)

    def __init__(self, city=None, *args, **kwargs):
        super(ParariusSpider, self).__init__(*args, **kwargs)
        if not city:
            raise CloseSpider('Must provide city for pararius')
        self.start_urls[0] = self.start_urls[0] % city


    def parse_page(self, response):
        "resultset > hproduct"
        '<a class="photo" href="/appartement-te-huur/amsterdam/PR0001196935/banstraat">'
        '<div class="addressTitle"><a href="/appartement-te-huur/amsterdam/PR0001196935/banstraat">Appartement Banstraat 28 2 - Amsterdam - Museumkwartier</a><div>'
        '<strong class="price"><b>€ 1.650,-</b>per maand (exclusief)</strong>'

        """
        <div class="deform">
            <strong class="price"><b>€ 1.650,-</b> per maand(exclusief)</strong>
            - 2 slaapkamers - 70 m²  - Gestoffeerd
        </div>
        """
        selector = Selector(response)

        for listed_ad in selector.css(".hproduct"):
            l = ParariusLoader(item=AdvertisedItem(), selector=listed_ad)

            l.add_css("link", ".photo::attr(href)")
            l.add_xpath("place", './/div[@class="addressTitle"]/a/text()')
            l.add_xpath("street", './/div[@class="addressTitle"]/a/text()')
            l.add_xpath("hood", './/div[@class="addressTitle"]/a/text()')
            l.add_xpath("price", './/strong[@class="price"]/b')
            l.add_value("base_address", response.url)
            l.add_value("source", self.name)

            yield l.load_item()

    parse_start_url = parse_page