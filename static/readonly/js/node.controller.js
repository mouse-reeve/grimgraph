angular.module('app').controller('NodeCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {
    Grimoire.loadNode($routeParams.id).then(function (data) {
        $scope.item = data.nodes[0];
        $scope.rels = data.relationships;
        $scope.itemCopy = angular.copy($scope.item);
        $scope.newItem = {
            'properties': {'identifier': ''},
            'relatedNode': $scope.item.id
        };
    });
}]);

