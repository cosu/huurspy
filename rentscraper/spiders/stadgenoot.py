# -*- coding: utf-8 -*-
import scrapy


class StadgenootSpider(scrapy.Spider):
    name = "stadgenoot"
    allowed_domains = ["http://www.stadgenoot.nl"]
    start_urls = (
        'http://www.http://www.stadgenoot.nl/',
    )

    def parse(self, response):
        pass
