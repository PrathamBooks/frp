'use strict';

/* Controllers */

angular.module('frp.controllers', []).
  controller('baseCtrl', ['$scope', function($scope) {
	$scope.path = window.location.pathname;
  }]);