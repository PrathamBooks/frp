'use strict';

// Declare app level module which depends on filters, and services
angular.module('frp', [
  'ngRoute',
  'frp.filters',
  'frp.services',
  'frp.directives',
  'frp.controllers'
]).
config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
  $locationProvider.html5Mode(true);
  $routeProvider.when('/', {templateUrl: 'partials/home.html', controller: 'baseCtrl'});
  $routeProvider.when('/browse', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/browse/:type', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/create', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/create/:sub', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/learn', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/learn/:sub', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/profile', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.when('/logout', {templateUrl: 'partials/base.html', controller: 'baseCtrl'});
  $routeProvider.otherwise({redirectTo: ''});
}]);
