from urllib import quote
from pymongo import ReadPreference
from pymongo.mongo_client import MongoClient
from scrapy.conf import settings
from scrapy import log
from pushbullet import Pushbullet
import urlparse
from scrapy.exceptions import DropItem


class InvalidItemPipeline(object):
    def process_item(self, item, spider):
        if 'price' not in item.keys():
            raise DropItem("Invalid item found: %s" % item)
        else:
            return item

class PushbulletPipeline(object):
    def __init__(self):
        if settings[settings['PUSHBULLET_KEY']]:
            self.pb = Pushbullet(settings['PUSHBULLET_KEY'])
        self.ads_to_send = []

        connection = MongoClient(
            settings['MONGODB_HOST'],
            read_preference=ReadPreference.PRIMARY)

        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if int(item['price']) < settings['MAX_PRICE'] and item['place'].lower() in settings['PLACES']:

            # the item is not in mongo
            if self.collection.find({"link": item['link']}).count() == 0:
                self.debug(spider, item['link'])
                self.ads_to_send.append(item)
        return item

    def close_spider(self, spider):
        links = []
        for item in self.ads_to_send:
            log.msg(" %s " % item['link'], level=log.DEBUG, spider=spider)
            links.append(urlparse.urljoin(item['base_address'], quote(item['link'])))
            log.msg(" %s " % item, level=log.DEBUG, spider=spider)

        if len(links) and self.pb:
            self.pb.push_note("New ads", "\n".join(links))

    def debug(self, spider, msg):
        log.msg(msg, level=log.DEBUG, spider=spider)
