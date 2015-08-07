(function() {
	'use strict';
	angular.module('rentguiApp')
	.controller('StatsCtrl', function ($scope, $log, $http, $q, dataservice {
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

}()); 