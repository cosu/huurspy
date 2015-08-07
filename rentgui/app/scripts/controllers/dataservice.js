(function(){

}());
angular.module('rentguiApp').
.factory('dataservice', ['$http', function($http, $log){
	return {
		getLatest: getLatest,
		getAll: getAll
	};

    var baseURL = '/scrapy/rentscraper?sort_by=-scrapy-mongodb.ts&count&pagesize=PAGESIZE&page=PAGE';
	
	function getAll (pageNo, pageSize) {
		url = baseURL.replace("PAGESIZE", pageSize);
		url = url.replace("PAGE", page);
	
		return $http.get(url).then(function(data){
			var ads = [];
			angular.forEach(data._embedded['rh:doc'], function (value, key) {
                var fields = ["street", "price", "source", "place"];
                var ad = {};
                angular.forEach(fields, function (field) {
                    ad[field] = value[field];
                });
                ads.push(ad);
                return {data: ads, pages: data._total_pages, page: page}
            });

		})
		.catch(function(data) {$log.error(data)});
	}

}])
