(function () {


    angular.module('rentguiApp')
        .factory('dataservice', ['$http', function ($http, $log) {
            var baseURL = '/ads?page_size=PAGESIZE&page=PAGE';

            return {
                //getLatest: getLatest,
                getAll: getAll
            };


            function getAll(queryOptions) {
                var options = queryOptions || {};
                var pageSize = options.pageSize || 1000;
                var page = options.page || 1;
                var maxPrice = options.maxPrice || 0;
                var minPrice = options.minPrice || 0;
                var city = options.city || "";

                var url = baseURL.replace("PAGESIZE", pageSize).replace("PAGE", page);

                if (city.length > 0) {
                    url += '&city=' + city;
                }
                if (minPrice > 0) {
                    url += '&min_price=' + minPrice;
                }
                if (maxPrice > 0) {
                    url += '&max_price=' + maxPrice;
                }

                return $http.get(url).then(function (response) {
                    console.log(response.data);
                    return response.data;
                })
                    .catch(function (data) {
                        $log.error(data)
                    });
            }

        }])
}());