(function () {


    angular.module('rentguiApp')
        .factory('dataservice', ['$http', function ($http, $log) {
            var baseURL = 'http://localhost:5000/ads?page_size=PAGESIZE&page=PAGE';

            return {
                getPage: getPage
            };


            function getPage(queryOptions) {
                var options = queryOptions || {};
                var pageSize = options.pageSize || 20;
                var page = options.page || 1;
                var maxPrice = options.maxPrice || 0;
                var minPrice = options.minPrice || 0;
                var place = options.place|| "";

                var url = baseURL.replace("PAGESIZE", pageSize).replace("PAGE", page);

                if (place.length > 0) {
                    url += '&place=' + place;
                }
                if (minPrice > 0) {
                    url += '&min_price=' + minPrice;
                }
                if (maxPrice > 0) {
                    url += '&max_price=' + maxPrice;
                }

                return $http.get(url).then(function (response) {
                    return response.data;
                })
                    .catch(function (data) {
                        $log.error(data)
                    });
            }

        }])
}());