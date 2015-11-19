angular.module('app').controller('ListCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.type = $routeParams.type || 'grimoires';
    $scope.sortField = 'properties.identifier';
    $scope.reverse = false;

    var loadData = function () {
        Grimoire.loadList($scope.type).then(function (data) {
            $scope.nodes = data.nodes;
            $scope.properties = data.properties;
        });
    };

    $scope.setSort = function (field) {
        if ($scope.sortField == 'properties.' + field) {
            $scope.reverse = !$scope.reverse;
        } else {
            $scope.sortField = 'properties.' + field;
            $scope.reverse = false;
        }
    };

    $scope.isSort = function (field) {
        if ($scope.sortField == 'properties.' + field) {
            return 'sort-field';
        }
    };

    loadData();
}]);
