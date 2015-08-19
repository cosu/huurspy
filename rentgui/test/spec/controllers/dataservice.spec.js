'use strict';

describe('dataservice', function () {


    var data = {
        "_embedded": {
            "rh:doc": [{
                "_embedded": {}
                , "_links": {
                    "self": {"href": "/scrapy/rentscraper/55d406adbd618f0899e6397c"},
                    "rh:coll": {"href": "/scrapy"},
                    "curies": [{
                        "href": "http://www.restheart.org/docs/v0.10/#api-doc-{rel}",
                        "name": "rh"
                    }]
                },
                "_type": "DOCUMENT",
                "_id": {"$oid": "55d406adbd618f0899e6397c"},
                "hood": "West", "url": "http://www.rooftrack.nl/EenheidDetails/150046056",
                "price": 825,
                "surface": "69m",
                "source": "rooftrack",
                "street": "Jacob van Lennepstraat 94 A",
                "place": "Amsterdam",
                "rooms": "3",
                "link": "/EenheidDetails/150046056",
                "scrapy-mongodb": {"ts": {"$date": 1439958701033}},
                "type": "Eengezinswoning",
                "base_address": "http://www.rooftrack.nl/Zoeken/geo-52;3651323157895,4;88880105263158,0,Amsterdam/huur-0-9999/page-3,10"
                , "_created_on": "2015-08-19T04:31:41Z"
            }
                , {"_embedded": {},
                    "_links": {
                        "self": {"href": "/scrapy/rentscraper/55ce6bedbd618f71ccca96d4"},
                        "rh:coll": {"href": "/scrapy"},
                        "curies": [{"href": "http://www.restheart.org/docs/v0.10/#api-doc-{rel}", "name": "rh"}]
                    },
                    "_type": "DOCUMENT",
                    "_id": {"$oid": "55ce6bedbd618f71ccca96d4"},
                    "scrapy-mongodb": {"ts": {"$date": 1439591405068}},
                    "url": "http://www.funda.nl/huur/amsterdam/huis-49560714-gerrit-van-erkelstraat-6/",
                    "price": 1275,
                    "surface": "96 m",
                    "source": "funda",
                    "street": "Gerrit van Erkelstraat 6",
                    "link": "/huur/amsterdam/huis-49560714-gerrit-van-erkelstraat-6/",
                    "postcode": "1019 JW",
                    "place": "Amsterdam",
                    "age": "sinds vandaag",
                    "availability": "Per direct beschikbaar",
                    "base_address": "http://www.funda.nl",
                    "rooms": "3",
                    "_created_on": "2015-08-14T22:30:05Z"
                }]
        },
        "_links": {
            "self": {"href": "/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=20&page=1&filter={\"place\":{ \"$regex\":\".*amsterdam\", \"$options\": \"i\" }}&filter={\"price\":{ \"$gte\":500, \"$lte\":1500}}"},
            "first": {"href": "/scrapy/rentscraper?pagesize=20&sort_by=-scrapy-mongodb.ts&count&filter={\"place\":{ \"$regex\":\".*amsterdam\", \"$options\": \"i\" }}&filter={\"price\":{ \"$gte\":500, \"$lte\":1500}}"},
            "last": {"href": "/scrapy/rentscraper?page=121&pagesize=20&sort_by=-scrapy-mongodb.ts&count&filter={\"place\":{ \"$regex\":\".*amsterdam\", \"$options\": \"i\" }}&filter={\"price\":{ \"$gte\":500, \"$lte\":1500}}"},
            "next": {"href": "/scrapy/rentscraper?page=2&pagesize=20&sort_by=-scrapy-mongodb.ts&count&filter={\"place\":{ \"$regex\":\".*amsterdam\", \"$options\": \"i\" }}&filter={\"price\":{ \"$gte\":500, \"$lte\":1500}}"},
            "rh:db": {"href": "/scrapy"},
            "rh:filter": {"href": "/scrapy/rentscraper/{?filter}", "templated": true},
            "rh:sort": {"href": "/scrapy/rentscraper/{?sort_by}", "templated": true},
            "rh:paging": {"href": "/scrapy/rentscraper/{?page}{&pagesize}", "templated": true},
            "rh:countandpaging": {"href": "/scrapy/rentscraper/{?page}{&pagesize}&count", "templated": true},
            "rh:indexes": {"href": "/scrapy/rentscraper/_indexes"},
            "curies": [{"href": "http://www.restheart.org/docs/v0.10/#api-coll-{rel}", "templated": true, "name": "rh"}]
        },
        "_type": "COLLECTION",
        "_id": "rentscraper",
        "_created_on": "2015-03-16T20:57:11Z",
        "_etag": {"$oid": "550743a70364bbd296dfd168"},
        "_lastupdated_on": "2015-03-16T20:57:11Z",
        "_collection-props-cached": false,
        "_size": 2410,
        "_total_pages": 1,
        "_returned": 2
    };


    // load the controller's module
    beforeEach(module('rentguiApp'));

    var ds;
    var $httpBackend;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($injector) {
        $httpBackend = $injector.get('$httpBackend');
        ds = $injector.get('dataservice');
    }));

    it('should call the right url to get a page', function () {
        $httpBackend.expectGET("/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=1000&page=1")
            .respond({_embedded: {"rh:doc": []}});
        ds.getAll();
        $httpBackend.flush();
    });

    it('should call the right url to get a page with minimum price', function () {
        $httpBackend.expectGET("/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=1000&page=1&filter={\"price\":{ \"$gte\":100}}")
            .respond({_embedded: {"rh:doc": []}});
        ds.getAll({minPrice: 100});
        $httpBackend.flush();
    });

    it('should call the right url to get a page with maximum price', function () {
        $httpBackend.expectGET("/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=1000&page=1&filter={\"price\":{ \"$lte\":100}}")
            .respond({_embedded: {"rh:doc": []}});
        ds.getAll({maxPrice: 100});
        $httpBackend.flush();
    });

    it('should call the right url to get a page with minimum and maximum price', function () {
        $httpBackend.expectGET("/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=1000&page=1&filter={\"price\":{ \"$gte\":100, \"$lte\":100}}")
            .respond({_embedded: {"rh:doc": []}});
        ds.getAll({minPrice: 100, maxPrice: 100});
        $httpBackend.flush();
    });

    it('should call the right url and return a list of valid ads', function () {
        $httpBackend.expectGET("/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=1000&page=1")
            .respond(data);
        ds.getAll().then(function(ads){
            expect(ads.data.length).toEqual(2);
            angular.forEach(ads.data, function(ad){
                expect(ad.price).toBeDefined();
                expect(ad.street).toBeDefined();
                expect(ad.place).toBeDefined();
                expect(ad.source).toBeDefined();
            })
        });
        $httpBackend.flush();
    });
});
