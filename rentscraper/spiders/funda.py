from scrapy import Selector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.spiders import Rule, CrawlSpider
import unicodedata
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot
from rentscraper.util import has_pp
from re import sub

__author__ = 'cdumitru'


def _clean(description):
    result = {
        'age': None,
        'rooms': None
    }
    clean = sub(r'[^\x00-\x7F]+', ',', description)
    clean = sub('\s+', ' ', clean)
    clean = " ".join(clean.split()).split(",")
    clean = [t.strip() for t in clean]


    if "sinds" in clean[-1]:
        result['age'] = clean[-1]
        result['availability'] = clean[-2]
    else:
        result['age'] = None
        result['availability'] = clean[-1]

    if "m" in clean[0]:
        result['surface'] = clean[0]

    if "kamers" in clean[2]:
        result['rooms'] = clean[2].split()[0]


    return result

def _extract_place(description):
    tokens = sub('\s+', ',', description.strip()).strip().split(",")
    return tokens[2]


def _extract_postcode(description):
    tokens = sub('\s+', ',', description.strip()).strip().split(",")
    return " ".join(tokens[1:3])


def _extract_surface(description):
    return _clean(description)['surface']


def _extract_rooms(description):
    return _clean(description)['rooms']


def _extract_availability(description):
    return _clean(description)['availability']

def _extract_age(description):
    return _clean(description)['age']

# def _extract_availability(description):
#     clean = sub(r'[^\x00-\x7F]+', '', description).strip()
#     tokens = sub('\s+', ',', clean).strip().split(",")
#     return " ".join(tokens[7:10])


class FundaLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_dot, default_input_processor)
    parking_in = MapCompose(has_pp, default_input_processor)
    place_in = MapCompose(default_input_processor, _extract_place)
    postcode_in = MapCompose(_extract_postcode, default_input_processor)
    surface_in = MapCompose(default_input_processor, _extract_surface)
    rooms_in = MapCompose(default_input_processor, _extract_rooms)
    availability_in = MapCompose(default_input_processor, _extract_availability)
    age_in = MapCompose(default_input_processor, _extract_age)


class FundaSpider(CrawlSpider):
    name, start_urls = 'funda', ['http://www.funda.nl/huur/%s/sorteer-datum-af/p1']
    rules = (
        Rule(LxmlLinkExtractor(allow=('http://www.funda.nl/huur/'), restrict_xpaths=('//div[@id="pagerContainer"]')), callback='parse_page',
             follow=True),)

    def __init__(self, city=None, *args, **kwargs):
        super(FundaSpider, self).__init__(*args, **kwargs)
        self.start_urls[0] = self.start_urls[0] % city

    def parse_page(self, response):
        selector = Selector(response)

        # yes that's a space in the class name ...
        for listed_ad in selector.xpath("//li[contains(concat(' ', normalize-space(@class), ' '), ' nvm ')]"):
            l = FundaLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_value("source", self.name)
            l.add_value("base_address", response.url)
            l.add_css("link", ".object-media-wrapper::attr(href)")
            l.add_xpath("price", ".//span[@class='price']", re="(\d+\.*\d+)")
            l.add_css("street", ".object-street ")
            l.add_xpath("place", ".//li[1]")
            l.add_xpath("postcode", ".//li[1]")
            l.add_xpath("surface", ".//li[2]")
            l.add_xpath("rooms", ".//li[2]")
            l.add_xpath("age", ".//li[2]")
            l.add_xpath("availability", ".//li[2]")

            yield l.load_item()

    parse_start_url = parse_page