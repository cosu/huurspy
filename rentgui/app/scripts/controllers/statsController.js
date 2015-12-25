(function () {
  'use strict';
  angular.module('rentguiApp')
    .controller('StatsCtrl', function ($log, $q, dataservice) {
      var vm = this;
      var deferred = $q.defer();
      vm.loading = true;
      var options = {pageSize: 5000, page: 1};
      vm.data = [];
      dataservice.getPage(options).then(function (data) {
        var pages = data.pages;
        vm.data = data.items;
        if (pages >= 2) {
          vm.receiveCount = pages - 1;
          for (var i = 2; i < pages + 1; i++) {
            options.page = i;
            dataservice.getPage(options).then(function (data) {
              vm.receiveCount--;
              angular.forEach(data.items, function (item) {
                vm.data.push(item)
              });

              if (vm.receiveCount === 0) {
                deferred.resolve();
              }
            });
          }
        }
        else {
          deferred.resolve();
        }

      });


      deferred.promise.then(function () {
        vm.binSize = 50;
        var priceChart = dc.barChart('#price');
        var placeChart = dc.rowChart('#place');
        var ndx = crossfilter(vm.data);
        var all = ndx.groupAll();
        var priceDimension = ndx.dimension(function (d) {
          return d.price;
        });
        var placeDimension = ndx.dimension(function (d) {
          return d.place;
        });

        var priceGroup = priceDimension.group(function (d) {
          return Math.floor(d.x / vm.binSize);
        });


        priceChart.width(420)
          .height(400)
          .dimension(priceDimension)
          .group(priceDimension.group().reduceCount())
          .x(d3.scale.linear().domain([500, 3000]))
          .xUnits(dc.units.fp.precision(vm.binSize))
          .elasticY(true)
          .render();

        placeChart.width(420)
          .height(400)
          .dimension(placeDimension)
          .group(placeDimension.group())
          .rowsCap(10)
          .render()

        vm.loading = false;


      })


    });

}());
