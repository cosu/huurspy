(function () {
    'use strict';

    angular
        .module('rentguiApp', [
            'ngSanitize',
            'ngRoute',
            'ui.grid'
        ])
        .config(function ($routeProvider, $httpProvider) {
            $routeProvider

                .when('/', {
                    templateUrl: 'views/main.html',
                    controller: 'MainCtrl',
                     controllerAs: 'vm'
                })

                .when('/stats', {
                    templateUrl: 'views/stats.html',
                    controller: 'StatsCtrl',
                     controllerAs: 'vm'
                })

                .otherwise({
                    redirectTo: '/'
                });

            $httpProvider.defaults.headers.common["Content-Type"] = "application/json";

        });

})();
