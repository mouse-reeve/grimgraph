angular.module('app').controller('LabelsCtrl', ['$scope', 'Grimoire', function($scope, Grimoire) {

    $scope.labels = {};

    Grimoire.loadLabels().then(function (data) {
        $scope.labels = setLabels(data);
    });

    $scope.edit = function (label) {
        label.editMode = true;
    };

    $scope.updateLabel = function (label) {
        Grimoire.editLabel(label.label, label.updated).then(function (data) {
            $scope.labels = setLabels(data);
            label.editMode = false;
        });
    };

    var setLabels = function(data) {
        var labels = {}
        angular.forEach(data, function (label) {
            labels[label] = {
                'label': label[0],
                'updated': label[0],
                'editMode': false,
                'count': label[1]
            };
        });
        return labels
    };
}]);
