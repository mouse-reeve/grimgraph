angular.module('app').controller('ListCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.type = $routeParams.type || 'grimoires';
    Grimoire.load($scope.type).then(function (data) {
        $scope.grimoires = data;
    });

}]);
