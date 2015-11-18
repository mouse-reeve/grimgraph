angular.module('app').controller('ListCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.type = $routeParams.type || 'grimoires';

    var loadData = function () {
        Grimoire.loadList($scope.type).then(function (data) {
            $scope.nodes = data.nodes;
            $scope.properties = data.properties;
        });
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
