(function () {
  'use strict';
  angular.module('rentguiApp')
    .controller('StatsCtrl', function ($log, $q, dataservice) {
      var vm = this;
      vm.loading = true;
      vm.binSize = 100;
      vm.data = [];

      var options = {pageSize: 1, page: 1, minPrice: 100, maxPrice: 3000, fields: ["place", "price"]};
      var pageSize = 10000;


      function getData() {
        var deferred = $q.defer();
        dataservice.getPage(options).then(function (data) {
          var pages = Math.ceil(data.total / pageSize);
          options.pageSize = pageSize;
          vm.receiveCount = pages;
          for (var i = 0; i < pages; i++) {
            options.page = i + 1;
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

        });
        return deferred.promise;
      }


      function draw() {
        var priceChart = dc.barChart('#price');
        var placeChart = dc.rowChart('#place');
        var ndx = crossfilter(vm.data);
        var priceDimension = ndx.dimension(function (d) {
          return d.price;
        });
        var placeDimension = ndx.dimension(function (d) {
          return d.place;
        });

        var priceDimensionBin = ndx.dimension(function (d) {
          return Math.floor(d.price / vm.binSize) * vm.binSize;
        });


        var minPrice = priceDimension.bottom(1)[0].price;
        var maxPrice = priceDimension.top(1)[0].price;


        priceChart.width(420)
          .height(400)
          .dimension(priceDimension)
          .group(priceDimensionBin.group().reduceCount())
          .x(d3.scale.linear().domain([minPrice, maxPrice]))
          .xUnits(dc.units.fp.precision(vm.binSize))
          .elasticY(true)
          .render();

        placeChart.width(420)
          .height(400)
          .dimension(placeDimension)
          .group(placeDimension.group())
          .rowsCap(15)
          .render();

        vm.loading = false;

      }

      getData().then(draw);


    });

}());
