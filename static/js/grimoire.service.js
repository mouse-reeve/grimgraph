angular.module('grimoireService', []).service('Grimoire', function ($http) {
    return {
        loadList: function (label) {
            label = label ? label : 'grimoire';
            return $http.get('/api/' + label).then(function (response) {
                return response.data;
            });
        },
        loadNode: function (id) {
            return $http.get('/api/item/' + id).then(function (response) {
                return response.data;
            });
        }
    };
});
