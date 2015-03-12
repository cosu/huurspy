from re import sub, search
from scrapy import Spider, Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import TakeFirst
from w3lib.html import remove_tags
from rentscraper.items import AdvertisedItem
from rentscraper.util import remove_dot, collapse_whitespace



class StadgenootLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, unicode.strip, collapse_whitespace)
    default_output_processor = TakeFirst()
    price_in = MapCompose(default_input_processor, remove_dot)
    place_in = MapCompose(default_input_processor, lambda x: search('\d{4} \w{2} (\w+) \(.*\)', x).group(1))
    hood_in = MapCompose(default_input_processor, lambda x: sub("[\(\)]", '', x))
    # street_in = MapCompose(default_input_processor, _extract_street)


class StadgenootSpider(Spider):
    name = "stadgenoot"
    allowed_domains = ["stadgenoot.nl"]
    start_urls = [
        'http://www.stadgenoot.nl/zoeken?q=&sort=updatedate&priceRange_use=on&priceRange_valuefrom=650&priceRange_valueto='+
        '1500&district=on&type_wonen=on&type_parkeren=&type_ondernemen=&soort_huur=on&city_2588=on&q-wonen=&q-parkeren=&q-ondernemen=',
    ]

    def parse(self, response):

        selector = Selector(response)

        for listed_ad in selector.css(".object-listitem-search"):
            l = StadgenootLoader(item=AdvertisedItem(), selector=listed_ad)

            l.add_xpath("link", ".//a/@href")
            l.add_xpath("place", './/li[1]')
            l.add_xpath("street", './/h3')
            l.add_xpath("hood", './/li[1]', re=".*(\(.*\))")
            l.add_xpath("price", './/div[@class="object-price"]', re="(\d+\.*\d+)")
            l.add_xpath("surface", './/li[2]', re="\d+")
            l.add_xpath("rooms", './/li[2]', re="(\d+).*kamer")
            l.add_value("base_address", response.url)
            l.add_value("source", self.name)

            yield l.load_item()

    # parse_start_url = parse_page
