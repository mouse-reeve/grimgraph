angular.module('app').controller('MainCtrl', [
        '$scope', 'Grimoire', function($scope, Grimoire) {
    $scope.test = 'hi';
    Grimoire.grimoires(function (data) {
        debugger;
    });
}]);
