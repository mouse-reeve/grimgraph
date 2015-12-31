angular.module('app').controller('NodeCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.edit = false;

    var loadData = function () {
        Grimoire.loadNode($routeParams.id).then(function (data) {
            $scope.item = data.nodes[0];
            $scope.rels = data.relationships;
            $scope.itemCopy = angular.copy($scope.item);
            $scope.newItem = {
                'properties': {'identifier': ''},
                'relatedNode': $scope.item.id
            };
        });
    };

    Grimoire.loadTypes().then(function (data) {
        $scope.types = data;
    });

    $scope.addField = function (item, fieldName) {
        if (fieldName) {
            item[fieldName] = "";
            fieldName = null;
        }
    };

    $scope.removeField = function (item, key) {
        delete item[key];
    };


    $scope.updateNode = function () {
        Grimoire.updateNode($scope.itemCopy).then(function (data) {
            $scope.item = $scope.itemCopy;
            $scope.edit = false;
        });
    };


    $scope.addNode = function () {
        Grimoire.addNode($scope.newItem, $scope.newItem.label).then(function (data) {
            loadData();
        });
    };

    $scope.addRelationship = function () {
        Grimoire.addRelationship($scope.item.id, $scope.newConnection.relatedNode, $scope.newConnection.relationship).then(function () {
            loadData();
        });
    };

    $scope.removeRelationship = function (relId) {
        Grimoire.removeRelationship(relId).then(function () {
            loadData();
        });
    };

    $scope.loadList = function (label) {
        Grimoire.loadList(label).then(function (data) {
            $scope.connectList = data.nodes;
        });
    };

    loadData();
}]);

