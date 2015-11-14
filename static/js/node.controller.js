angular.module('app').controller('NodeCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    Grimoire.loadNode($routeParams.id).then(function (data) {
        $scope.item = data;
    });

}]);

