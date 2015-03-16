'use strict';

angular
    .module('rentguiApp', [
        'ngResource',
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

        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common["X-Requested-With"];
        $httpProvider.defaults.withCredentials = true;
        $httpProvider.defaults.headers.common["Accept"] = "application/hal+json";
        $httpProvider.defaults.headers.common["Content-Type"] = "application/json";
        $httpProvider.defaults.headers.common["No-Auth-Challenge"] = "true";
    });
