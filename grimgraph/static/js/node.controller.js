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

            if (!$scope.addItem) {
                $scope.addItem = data['common']
            }
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

    $scope.addRelationship = function (relatedNode, relationship) {
        Grimoire.addRelationship($scope.item.id, relatedNode, relationship).then(function () {
            loadData();
        });
    };

    $scope.removeRelationship = function (relId) {
        Grimoire.removeRelationship(relId).then(function () {
            loadData();
        });
    };

    $scope.showAddItem = function (item) {
        Grimoire.loadList(item.label).then(function (data) {
            item.show = true;
            item.options = data.nodes;
            item.props = data.properties;
        });
    };

    $scope.saveAddItem = function (item) {
        if (item.isNew) {
            Grimoire.addNode(item.newItem, item.label).then(function (data) {
                var startId = item.start ? data.nodes[0].id : $scope.item.id;
                var endId = item.start ? $scope.item.id : data.nodes[0].id;

                Grimoire.addRelationship(startId, endId, item.rel).then(loadData);
            });
        } else {
            var startId = item.start ? item.existingItem : $scope.item.id;
            var endId = item.start ? $scope.item.id : item.existingItem;
            Grimoire.addRelationship(startId, endId, item.rel).then(loadData);
        }
    };

    $scope.loadList = function (label) {
        Grimoire.loadList(label).then(function (data) {
            $scope.connectList = data.nodes;
        });
    };

    $scope.setUID = function (node) {
        node.properties.uid = node.properties.identifier.replace(' ', '-').toLowerCase();
    };

    loadData();
}]);

