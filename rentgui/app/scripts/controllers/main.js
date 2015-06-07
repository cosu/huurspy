'use strict';

angular.module('rentguiApp')
    .controller('MainCtrl', function ($scope, $log, $http, $q) {
        var baseURL = '/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=20&page=';
        $scope.minPrice = 500;
        $scope.maxPrice = 1500;
        $scope.city = "amsterdam";
        $scope.gridOptions = {
            columnDefs: [
                {field: 'place'},
                {field: 'price'},
                {
                    field: 'ts',
                    cellTemplate: '<div class="ui-grid-cell-contents">{{COL_FIELD|date: "yyyy-MM-dd HH:mm"}}</div>',
                    name: 'Date'
                },
                {
                    field: 'url',
                    cellTemplate: '<div class="ui-grid-cell-contents"><a target="_blank" href="{{ COL_FIELD}}">link</a></div>'
                },
                {field: 'street'},
                {field: 'source'}
            ],

            data: 'ads'
        };

        $scope.setCurrentPage = function (num) {
            $scope.currentPage = num;
            var pageURL = baseURL + $scope.currentPage;

            if (!$scope.city == '') {
                pageURL += '&filter={\"place\":{ \"$regex\":\".*' + $scope.city + '\", "$options": "i" }}';

            }

            if (!$scope.maxPrice == '' && !$scope.minPrice == '') {
                pageURL += '&filter={\"price\":{ \"$gte\":' + $scope.minPrice + ', \"$lte\":' + $scope.maxPrice + '}}';
            } else {
                if (!$scope.maxPrice == '') {
                    pageURL += '&filter={\"price\":{ \"$lte\":' + $scope.maxPrice + '}}';
                }

                if (!$scope.minPrice == '') {
                    pageURL += '&filter={\"price\":{ \"$gte\":' + $scope.minPrice + '}}';
                }
            }


            //promise to return
            var deferred = $q.defer();

            var request = $http.get(pageURL, {});

            request.success(function (data) {
                $scope.posts = data;
                $scope.pages = data['_total_pages'];

                var ads = [];
                $scope.posts = data;
                angular.forEach(data._embedded['rh:doc'], function (value, key) {

                    var fields = ["street", "price", "source", "place"];
                    var ad = {};
                    angular.forEach(fields, function (field) {
                        ad[field] = value[field];
                    });
                    ad['ts'] = new Date(value['scrapy-mongodb']['ts']['$date']);
                    var base_address = value['base_address'] || "";
                    ad['url'] = value['url'];
                    ads.push(ad);

                });

                $scope.ads = ads;

                //resolve promise
                deferred.resolve();

            });

            request.error(function (data, status) {
                if (status === 404) {
                    $scope.errorNotFound = true;
                    //resolve promise
                    deferred.resolve();
                }
            });
        };

        $scope.setCurrentPage(1);
    })
    .controller('StatsCtrl', function ($scope, $log, $http, $q) {
        var baseURL = '/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=1000&page=';
        var deferred = $q.defer();
        var pageNum = 1;
        var request = $http.get(baseURL + pageNum, {});
        var ads = [];
        $scope.loading = true;

        request.success(function (data) {
            var pages = data._total_pages;
            //pages = 2;

            angular.forEach(data._embedded['rh:doc'], function (value, key) {
                var fields = ["street", "price", "source", "place"];
                var ad = {};
                angular.forEach(fields, function (field) {
                    ad[field] = value[field];
                });
                ads.push(ad);
            });

            for (var i = 2; i < pages + 1; i++) {
                $http.get(baseURL + i, {}).success(function (data) {
                    angular.forEach(data._embedded['rh:doc'], function (value, key) {
                        var fields = ["street", "price", "source", "place"];
                        var ad = {};
                        angular.forEach(fields, function (field) {
                            ad[field] = value[field];
                        });
                        ads.push(ad);
                    });
                    if (ads.length == pages * 1000) deferred.resolve();
                });

            }
        });

        deferred.promise.then(function () {
            $scope.binSize = 50;
            var priceChart = dc.barChart('#price');
            var placeChart = dc.rowChart('#place');
            var ndx = crossfilter(ads);
            var all = ndx.groupAll();
            var priceDimension = ndx.dimension(function (d) {return d.price;});
            var placeDimension = ndx.dimension(function (d) {return d.place;});

            var priceGroup  = priceDimension.group(function(d) { return Math.floor(d.x/$scope.binSize); });




            priceChart.width(420)
                .height(400)
                .dimension(priceDimension)
                .group(priceDimension.group().reduceCount())
                .x(d3.scale.linear().domain([500, 3000]))
                .xUnits(dc.units.fp.precision($scope.binSize))
                .elasticY(true)
                .render();

            placeChart.width(420)
                .height(400)
                .dimension(placeDimension)
                .group(placeDimension.group())
                .rowsCap(10)
                .render()

            $scope.loading = false;


        })


    });
