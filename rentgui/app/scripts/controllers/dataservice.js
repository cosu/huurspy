(function () {


    angular.module('rentguiApp')
        .factory('dataservice', ['$http','$log','$location', function ($http, $log, $location) {
            var baseURL = '/ads?page_size=PAGESIZE&page=PAGE';
            if ($location.host() === '127.0.0.1')
                baseURL =  'http://localhost:5000' + baseURL;

            return {
                getPage: getPage
            };


            function getPage(queryOptions) {
                var options = queryOptions || {};
                var pageSize = options.pageSize || 20;
                var page = options.page || 1;
                var maxPrice = options.maxPrice || 9999;
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