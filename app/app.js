<<<<<<< HEAD
angular
    .module('app', [
        /*
         * Angular modules
         */
        'ngResource', 'ui.router'

        /*
         * 3rd Party modules
         */
    ])
    .config(routeConfig)
    .run(run);

function routeConfig($urlRouterProvider, $httpProvider, $resourceProvider) {
    // Enable cors in client side
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $urlRouterProvider.otherwise("/");
    $resourceProvider.defaults.stripTrailingSlashes = false;
}

function run($rootScope, $state, $stateParams) {
    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
}
=======
'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'myApp.view1',
  'myApp.view2',
  'myApp.version'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);
>>>>>>> b5f2b2ab985cd3bf34e403ddece257a9ee3d0024
