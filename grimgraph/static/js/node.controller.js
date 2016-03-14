angular.module('app').controller('NodeCtrl', ['$routeParams', '$scope', 'Grimoire',
        function($routeParams, $scope, Grimoire) {

    $scope.edit = false;

    var customAdd = {
        grimoire: {
            edition: {
                label: 'edition', show: false, relationship: 'has', start: false
            },
            language: {
                label: 'language', show: false, relationship: 'was_written_in', start: false
            }
        },
        edition: {
            publisher: {
                label: 'publisher', show: false, relationship: 'published', start: true
            },
            editor: {
                label: 'editor', show: false, relationship: 'edited', start: true
            }
        },
        demon: {
            outcome: {label: 'outcome', show:false, relationship:'for', start:false}
        }
    };

    customAdd.book = customAdd.grimoire;

    angular.forEach(['spell', 'demon', 'angel', 'olympian_spirit', 'fairy', 'aerial_spirit'], function (entity) {
        customAdd.grimoire[entity] = {
            label: entity,
            show: false,
            relationship: 'lists',
            start: false
        };
    });

    $scope.addItem = customAdd[$routeParams.type] || {};

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

    $scope.showAddItem = function (type) {
        Grimoire.loadList(type).then(function (data) {
            $scope.addItem[type].show = true;
            $scope.addItem[type].options = data.nodes;
            $scope.addItem[type].props = data.properties;
        });
    };

    $scope.saveAddItem = function (item) {
        if (item.isNew) {
            Grimoire.addNode(item.newItem, item.label).then(function (data) {
                console.log(data);
                var startId = item.start ? data.nodes[0].id : $scope.item.id;
                var endId = item.start ? $scope.item.id : data.nodes[0].id;

                Grimoire.addRelationship(startId, endId, item.relationship).then(loadData);
            });
        } else {
            var startId = item.start ? item.existingItem : $scope.item.id;
            var endId = item.start ? $scope.item.id : item.existingItem;
            Grimoire.addRelationship(startId, endId, item.relationship).then(loadData);
        }
    };

    $scope.loadList = function (label) {
        Grimoire.loadList(label).then(function (data) {
            $scope.connectList = data.nodes;
        });
    };

    loadData();
}]);

