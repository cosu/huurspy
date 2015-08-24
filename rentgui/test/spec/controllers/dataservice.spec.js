'use strict';

describe('dataservice', function () {


    var data = {
        "items": [
            {
                "scrapy-mongodb": {
                    "ts": "2015-07-08T01:30:04.365000"
                },
                "url": "http://www.funda.nl/huur/amsterdam/appartement-49439862-poeldijkstraat-173/",
                "price": 530,
                "surface": "25 m",
                "availability": "In overleg",
                "source": "funda",
                "street": "Poeldijkstraat 173",
                "link": "/huur/amsterdam/appartement-49439862-poeldijkstraat-173/",
                "postcode": "1059 VK",
                "place": "Amsterdam",
                "_id": "559c7d1ca8282f2d221cb5b2",
                "age": "sinds vandaag",
                "base_address": "http://www.funda.nl"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-06-10T01:30:05.804000"
                },
                "url": "http://www.funda.nl/huur/amsterdam/appartement-49409432-poeldijkstraat-47/",
                "price": 530,
                "surface": "25 m",
                "availability": "In overleg",
                "source": "funda",
                "street": "Poeldijkstraat 47",
                "link": "/huur/amsterdam/appartement-49409432-poeldijkstraat-47/",
                "postcode": "1059 VG",
                "place": "Amsterdam",
                "_id": "5577931da8282f626d7e41f8",
                "age": "sinds vandaag",
                "base_address": "http://www.funda.nl"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-29T16:35:20.442000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam/PR0001218156/marco-polostraat",
                "price": 550,
                "surface": "17",
                "source": "pararius",
                "street": "Kamer Marco Polostraat",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam/PR0001218156/marco-polostraat",
                "_id": "55689548a8282f0cc6793a7a",
                "hood": "Hoofdweg en omgeving",
                "rooms": "1"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-27T20:30:24.474000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam/PR0001217456/prinseneiland",
                "price": 575,
                "surface": "16",
                "source": "pararius",
                "street": "Prinseneiland",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam/PR0001217456/prinseneiland",
                "_id": "55662960a8282f7f0ee8ec92",
                "hood": "Haarlemmerbuurt",
                "rooms": "1"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-26T16:01:58.897000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam/PR0001217092/het-hoogt",
                "price": 550,
                "surface": "12",
                "source": "pararius",
                "street": "Kamer Het Hoogt",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam/PR0001217092/het-hoogt",
                "_id": "556498f6a8282f7b5c082155",
                "hood": "Buikslotermeer",
                "rooms": "1"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-25T08:50:32.259000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam/PR0001215477/dijkgraafplein",
                "price": 600,
                "surface": "15",
                "source": "pararius",
                "street": "Dijkgraafplein",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam/PR0001215477/dijkgraafplein",
                "_id": "5562e258a8282f079adbae46",
                "hood": "De Punt",
                "rooms": "4"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-20T19:10:58.645000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam-zuidoost/PR0001209572/leerdamhof",
                "price": 600,
                "surface": "15",
                "source": "pararius",
                "street": "Leerdamhof",
                "place": "Amsterdam Zuidoost",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam-zuidoost/PR0001209572/leerdamhof",
                "_id": "555cdc42a8282f18610fcace",
                "hood": "Nellestein",
                "rooms": "4"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-20T19:10:49.558000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam/PR0001215476/dijkgraafplein",
                "price": 600,
                "surface": "15",
                "source": "pararius",
                "street": "Dijkgraafplein",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam/PR0001215476/dijkgraafplein",
                "_id": "555cdc39a8282f18610fc9a1",
                "hood": "De Punt",
                "rooms": "4"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-20T19:10:49.555000"
                },
                "url": "http://www.pararius.nl/appartement-te-huur/amsterdam/PR0001215477/dijkgraafplein",
                "price": 600,
                "surface": "15",
                "source": "pararius",
                "street": "Dijkgraafplein",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/appartement-te-huur/amsterdam/PR0001215477/dijkgraafplein",
                "_id": "555cdc39a8282f18610fc9a0",
                "hood": "De Punt",
                "rooms": "4"
            },
            {
                "scrapy-mongodb": {
                    "ts": "2015-05-20T19:10:39.228000"
                },
                "url": "http://www.pararius.nl/kamer-te-huur/amsterdam/PR0001212115/polijsterweg",
                "price": 500,
                "surface": "14",
                "source": "pararius",
                "street": "Polijsterweg",
                "place": "Amsterdam",
                "base_address": "http://www.pararius.nl",
                "link": "/kamer-te-huur/amsterdam/PR0001212115/polijsterweg",
                "_id": "555cdc2fa8282f18610fc84a",
                "hood": "Buiksloterham",
                "rooms": "3"
            }
        ],
        "total": 22,
        "page": 1,
        "page_size": 10
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
        $httpBackend.expectGET("/ads?page_size=1000&page=1")
            .respond({items: []});
        ds.getAll();
        $httpBackend.flush();
    });

    it('should call the right url to get a page with minimum price', function () {
        $httpBackend.expectGET("/ads?page_size=1000&page=1&min_price=100")
            .respond({items: []});
        ds.getAll({minPrice: 100});
        $httpBackend.flush();
    });

    it('should call the right url to get a page with maximum price', function () {
        $httpBackend.expectGET("/ads?page_size=1000&page=1&max_price=100")
            .respond({items: []});
        ds.getAll({maxPrice: 100});
        $httpBackend.flush();
    });

    it('should call the right url to get a page with minimum and maximum price', function () {
        $httpBackend.expectGET("/ads?page_size=1000&page=1&min_price=100&max_price=100")
            .respond({items: []});
        ds.getAll({minPrice: 100, maxPrice: 100});
        $httpBackend.flush();
    });

    it('should call the right url and return a list of valid ads', function () {
        $httpBackend.expectGET("/ads?page_size=1000&page=1")
            .respond(data);
        ds.getAll().then(function (ads) {
            expect(ads.items).toBeDefined();
            expect(ads.items.length).toEqual(10);
            angular.forEach(ads.items, function (ad) {
                expect(ad.price).toBeDefined();
                expect(ad.street).toBeDefined();
                expect(ad.place).toBeDefined();
                expect(ad.source).toBeDefined();
            })
        });
        $httpBackend.flush();
    });
});
