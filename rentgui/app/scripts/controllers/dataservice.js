(function () {


    angular.module('rentguiApp')
        .factory('dataservice', ['$http', function ($http, $log) {
            var baseURL = '/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=PAGESIZE&page=PAGE';

            return {
                //getLatest: getLatest,
                getAll: getAll
            };


            function getAll(options) {
                var options = options || {};
                var pageSize = options.pageSize || 1000;
                var page = options.page || 1;
                var maxPrice = options.maxPrice || 0;
                var minPrice = options.minPrice || 0;
                var city = options.city || "";

                var url = baseURL.replace("PAGESIZE", pageSize).replace("PAGE", page);

                if (city.length > 0) {
                    url += '&filter={\"place\":{ \"$regex\":\".*' + city + '\", "$options": "i" }}';
                }

                if (maxPrice > 0 && minPrice > 0) {
                    url  += '&filter={\"price\":{ \"$gte\":' + minPrice + ', \"$lte\":' + maxPrice + '}}';
                } else {
                    if (maxPrice > 0) {
                        url += '&filter={\"price\":{ \"$lte\":' + maxPrice + '}}';
                    }

                    if (minPrice > 0) {
                        url += '&filter={\"price\":{ \"$gte\":' + minPrice + '}}';
                    }
                }

                return $http.get(url).then(function (response) {
                    var ads = [];
                    var data = response.data;
                    angular.forEach(data._embedded['rh:doc'], function (value, key) {
                        var fields = ["street", "price", "source", "place"];
                        var ad = {};
                        angular.forEach(fields, function (field) {
                            ad[field] = value[field];
                        });
                        ads.push(ad);

                    });
                    var result =  {data: ads, pages: data._total_pages, page: page}
                    return result;
                })
                    .catch(function (data) {
                        $log.error(data)
                    });
            }

        }])
}());