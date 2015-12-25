(function () {

  'use strict';

  angular.module('rentguiApp')
    .controller('MainCtrl', function ($log, $http, $q, dataservice) {
      var vm = this;
      vm.minPrice = 500;
      vm.maxPrice = 1500;
      vm.place = 'amsterdam';
      vm.gridOptions = {
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

      };

      vm.setCurrentPage = function setCurrentPage(num) {
        vm.currentPage = num;

        var options = {
          place: vm.place,
          maxPrice: vm.maxPrice,
          minPrice: vm.minPrice,
          page: vm.currentPage
        };
        dataservice.getPage(options).then(function (ads) {
          vm.nextPage = ads.page + 1;
          vm.pages = ads.pages;
          vm.gridOptions.data = ads.items;
        });

      };

      vm.setCurrentPage(1);
    });
})();
