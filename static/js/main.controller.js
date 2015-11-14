angular.module('app').controller('MainCtrl', [
        '$scope', 'Grimoire', function($scope, Grimoire) {

    Grimoire.grimoires().then(function (data) {
        $scope.grimoires = data;
    });

}]);
