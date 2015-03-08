# -*- coding: utf-8 -*-

BOT_NAME = 'rentscraper'

SPIDER_MODULES = ['rentscraper.spiders']
NEWSPIDER_MODULE = 'rentscraper.spiders'


USER_AGNET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.74 Safari/537.36'


ITEM_PIPELINES = {
    # 'rentscraper.pipelines.MongoDBPipeline': 300,
    'scrapy_mongodb.MongoDBPipeline': 200,
}


COOKIES_DEBUG = True



MONGODB_ADD_TIMESTAMP = True
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'my_items'
MONGODB_UNIQUE_KEY = 'link'

#
# MONGODB_SERVER = "localhost"
# MONGODB_PORT = 27017
# MONGODB_DB = "huur"
# MONGODB_COLLECTION = "ads"