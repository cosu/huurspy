(function () {

    'use strict';

    angular.module('rentguiApp')
        .controller('MainCtrl', function ($scope, $log, $http, $q, dataservice) {
            $scope.minPrice = 500;
            $scope.maxPrice = 1500;
            $scope.place = "amsterdam";
            $scope.gridOptions = {
                columnDefs: [
                    {field: 'place'},
                    {field: 'price'},
                    {
                        field: 'scrapy-mongodb.ts',
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

                var options = {
                    place: $scope.place,
                    maxPrice: $scope.maxPrice,
                    minPrice: $scope.minPrice,
                    page: $scope.currentPage
                };
                dataservice.getPage(options).then(function (ads) {
                    $scope.nextPage = ads.page + 1;
                    $scope.pages = ads.pages;
                    console.log($scope.pages);
                    $scope.ads = ads.items;
                })

            };

            $scope.setCurrentPage(1);
        });
})();
