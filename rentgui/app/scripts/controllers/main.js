'use strict';

angular.module('rentguiApp')
    .controller('MainCtrl', function ($scope, $log, $http, $q) {
        var baseURL = 'http://localhost:8080/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=50&page=';


        $scope.setCurrentPage = function (num) {
            $scope.currentPage = num;
            var pageURL  = baseURL + $scope.currentPage;

            if (!$scope.city== '') {
                //{"name":{"$regex":".*k"}}
                pageURL += '&filter={\"place\":{ \"$regex\":\".*' + $scope.city + '\", "$options": "i" }}';

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
                    ad['link1'] = base_address + value['link'];
                    //ad['link1'] = angular.element("<div></div>");
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
