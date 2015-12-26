from bson import ObjectId, Code
from flask import Flask, g, request, Response
from pymongo import DESCENDING
from pymongo.mongo_client import MongoClient
from scrapy.conf import settings
from pymongo.read_preferences import ReadPreference
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
import datetime
from flask_cors import CORS


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')


app = Flask(__name__)
cors = CORS(app)


def get_collection():
    if not hasattr(g, 'mongo_db'):
        connection = MongoClient(settings['MONGODB_HOST'], read_preference=ReadPreference.PRIMARY)
        db = connection[settings['MONGODB_DATABASE']]
        g.mongo_db = db[settings['MONGODB_COLLECTION']]
    return g.mongo_db


@app.route("/ads")
def ads():
    page_size = int(request.args.get('page_size', 20))
    page = int(request.args.get('page', 1))
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 999999))
    fields = request.args.get('fields', '').split(",")
    place = request.args.get('place', "")

    query_options = {
        "place": {
            "$regex": ".*" + place,
            "$options": "i"
        },
        "price": {
            "$gte": min_price,
            "$lte": max_price
        }
    }

    skip = (page-1) * page_size
    total = get_collection().find(query_options).count()
    if len(fields) > 1:
        items_cursor = get_collection().find(query_options, fields=fields)
    else:
        items_cursor = get_collection().find(query_options)

    items = items_cursor.sort("scrapy-mongodb.ts", DESCENDING).skip(skip).limit(page_size)
    data = {
        "total": total,
        "items": list(items),
        "page": page,
        "page_size": page_size,
        "pages": int(total / page_size)
    }
    return jsonify(data)


@app.route("/prices")
def prices():
    reducer = Code("""
        function(obj, prev){
            if (!Array.isArray(prev[obj.place]))
                prev[obj.place] = [];
            prev[obj.place].push(obj.price);

        }
    """)
    prices = get_collection().group(key={"place"}, condition={}, initial={}, reduce=reducer)

    return jsonify({"ads": prices})


@app.route("/fix")
def fix():
    items = get_collection().find(projection=["place"])
    fixed = []
    for item in items:
        if 'place' in item:
            place = item['place']
            if place != "Amsterdam" and "amsterdam" in place.lower():
                get_collection().update_one({'_id': item['_id']}, {'$set': {'place': 'Amsterdam'}})
                fixed.append(item)

    return jsonify({"ok": fixed})

if __name__ == '__main__':
    app.run(debug=True)
