# -*- coding: utf-8 -*-
import urlparse

from scrapy import Item, Field


class AdvertisedItem(Item):
    price = Field()
    street = Field()
    postcode = Field()
    place = Field()
    link = Field()
    parking = Field()
    availability = Field()
    rooms = Field()
    surface = Field()
    furnished = Field()
    source = Field()
    type = Field()
    base_address = Field()
    age = Field()
    hood = Field()
    html = Field()
    url = Field()

    def get_url(self):

        link_parts = ['base_address', 'link']
        clean_parts = []
        for link_part in link_parts:
            if self.has_key(link_part): clean_parts.append(self[link_part])

        if not len(clean_parts):
            return "http://nolink"

        if len (clean_parts) > 1:
            return urlparse.urljoin(*clean_parts)
        else:
            return clean_parts[0]



