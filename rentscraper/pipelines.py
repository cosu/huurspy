import datetime
from pymongo import ReadPreference
from pymongo.mongo_client import MongoClient
from scrapy.conf import settings
from scrapy import log
from pushbullet import Pushbullet
from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import BaseItemExporter


class InvalidItemPipeline(BaseItemExporter):
    def __init__(self):
        super(InvalidItemPipeline, self).__init__()

        connection = MongoClient(
            settings['MONGODB_HOST'],
            read_preference=ReadPreference.PRIMARY)
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION_INVALID']]

    def process_item(self, item, spider):
        dict_item = dict(self._get_serialized_fields(item))
        keys = item.keys()
        if 'price' not in keys or 'place' not in keys or 'link' not in keys:

            dict_item['rentscraper'] = {'ts': datetime.datetime.utcnow()}
            dict_item['url'] = item.get_url()

            if self.collection.find({"url": dict_item['url']}).count() == 0:
                self.collection.insert(dict_item)

            raise DropItem("Invalid item (missing price or place) %s" % item)
        else:
            item.pop("html", None)
            item['price'] = int(item['price'])
            item['url'] = item.get_url()
            return item


class PushbulletPipeline(object):
    use_pushbullet = False

    def __init__(self):
        if settings['PUSHBULLET_KEY']:
            log.msg("Pushbullet enabled", level=log.INFO)
            self.pb = Pushbullet(settings['PUSHBULLET_KEY'])
            self.use_pushbullet = True
        else:
            log.msg("Pushbullet key missing", level=log.INFO)
        self.ads_to_send = []

        connection = MongoClient(
            settings['MONGODB_HOST'],
            read_preference=ReadPreference.PRIMARY)

        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if int(item['price']) <= settings['MAX_PRICE'] and item['place'].lower() in settings['PLACES']:
            # the item is not in mongo
            if self.collection.find({"link": item['link']}).count() == 0:
                self.ads_to_send.append(item)
        return item

    def close_spider(self, spider):
        links = []
        for item in self.ads_to_send:
            log.msg("[NEW] link:  %s " % item['link'], level=log.INFO, spider=spider)
            links.append(item.get_url())
            log.msg("[NEW] item %s " % item, level=log.INFO, spider=spider)

        if len(links) and self.use_pushbullet:
            log.msg("Sending %d new items " % len(links), level=log.INFO, spider=spider)
            self.pb.push_note("New ads (%s)" % len(links), "\n".join(links))


