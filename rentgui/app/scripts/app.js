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
                    controller: 'MainCtrl'
                })
                .otherwise({
                    redirectTo: '/'
                });

            $httpProvider.defaults.headers.common["Content-Type"] = "application/json";

        });

})();
