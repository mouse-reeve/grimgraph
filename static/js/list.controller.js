angular.module('app').controller('ListCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.type = $routeParams.type || 'grimoires';
    $scope.sortField = 'properties.title';
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

    $scope.edit = function (node) {
        node.editMode = !node.editMode;
    };

    $scope.updateNode = function (node) {
        Grimoire.updateNode(node).then(function (data) {
            node.editMode = false;
        });
    };

    $scope.addNode = function () {
        Grimoire.addNode($scope.newItem, $scope.type).then(function (data) {
            $scope.newItem.properties = {};
            loadData();
        });
    };

    loadData();
}]);
