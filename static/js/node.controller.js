angular.module('app').controller('NodeCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.edit = false;
    Grimoire.loadNode($routeParams.id).then(function (data) {
        $scope.item = data;
        $scope.itemCopy = angular.copy($scope.item);
    });

    $scope.addField = function () {
        if ($scope.newField) {
            $scope.itemCopy.properties[$scope.newField] = "";
        }
    };

    $scope.updateNode = function () {
        Grimoire.updateNode($scope.itemCopy).then(function (data) {
            $scope.item = $scope.itemCopy;
            $scope.edit = false;
        });
    };

}]);

