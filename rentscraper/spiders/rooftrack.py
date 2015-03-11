from scrapy import Selector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from re import sub
from rentscraper.util import remove_dot


def _clean_description(text):
    clean = sub(r'[^\x00-\x7F]+', '', text)
    clean = sub('\s+', ' ', clean)
    clean = clean.split()

    result = {
        "rooms": None,
        "type": None,
        "surface": None
    }

    if len(clean) == 4:
        result["rooms"] = clean[1]
        result["type"] = clean[0]
        result["surface"] = clean[-1]

    if len(clean) == 2:
        result['surface'] = clean[1]

    if len(clean) != 2 and len(clean) != 4:
        result["rooms"] = str(clean)
        result["type"] = clean
        result["surface"] = clean

    return result


def _extract_price(text):
    return text.split(" ")[1].split(",")[0].strip()


def _extract_place(text):
    tokens = text.split("-")
    return tokens[0].strip()


def _extract_hood(text):
    tokens = text.split("-")
    return "-".join(tokens[1:]).strip()


def _extract_rooms(text):
    return _clean_description(text)['rooms']


def _extract_surface(text):
    return _clean_description(text)['surface']


def _extract_type(text):
    return _clean_description(text)['type']


class RooftrackLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, _extract_price, remove_dot)
    place_in = MapCompose(default_input_processor, _extract_place)
    hood_in = MapCompose(default_input_processor, _extract_hood)
    rooms_in = MapCompose(default_input_processor, _extract_rooms)
    surface_in = MapCompose(default_input_processor, _extract_surface)
    type_in = MapCompose(default_input_processor, _extract_type)


class RooftrackSpider(CrawlSpider):
    name = "rooftrack"
    allowed_domains = ["rooftrack.nl"]
    start_urls = (
        'http://www.rooftrack.nl/Zoeken/geo-52;3651323157895,4;88880105263158,0,Amsterdam/huur-0-9999',
    )

    rules = (
        Rule(LxmlLinkExtractor(allow=('http://www.rooftrack.nl/Zoeken'),
                               restrict_xpaths=('//ul[@class="pagination"]'), ),
             callback='parse_page',
             follow=True),)

    def parse_page(self, response):
        selector = Selector(response)

        for listed_ad in selector.css(".ResultBox"):
            l = RooftrackLoader(item=AdvertisedItem(), selector=listed_ad)
            l.add_css("price", "strong")
            l.add_css("street", "h6")
            l.add_css("place", ".plaatswijk")
            l.add_css("hood", ".plaatswijk")
            l.add_css("surface", ".eigenschappen")
            l.add_css("rooms", ".eigenschappen")
            l.add_css("type", ".eigenschappen")
            l.add_css("link", ".react::attr(href)")
            l.add_value("base_address", response.url)
            l.add_value("source", self.name)

            yield l.load_item()

    parse_start_url = parse_page