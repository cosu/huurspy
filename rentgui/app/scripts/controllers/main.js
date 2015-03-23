'use strict';

angular.module('rentguiApp')
    .controller('MainCtrl', function ($scope, $log, $http, $q) {
        var baseURL = '/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=20&page=';
        $scope.minPrice = 500;
        $scope.maxPrice = 1500;
        $scope.city = "amsterdam";

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
                console.log('GET ' + pageURL);
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

                $scope.grid = ads;


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
    });
