angular.module('app').controller('ListCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.type = $routeParams.type || 'grimoires';
    Grimoire.loadList($scope.type).then(function (data) {
        $scope.grimoires = data.nodes;
    });

}]);
