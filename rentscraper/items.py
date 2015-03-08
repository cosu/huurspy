# -*- coding: utf-8 -*-


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
    postcode = Field()

