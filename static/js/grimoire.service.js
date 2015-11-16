angular.module('grimoireService', []).service('Grimoire', function ($http) {
    return {
        loadList: function (label) {
            label = label ? label : 'grimoires';
            return $http.get('/api/' + label).then(function (response) {
                return response.data;
            });
        },

        loadNode: function (id) {
            return $http.get('/api/item/' + id).then(function (response) {
                return response.data;
            });
        },
        updateNode: function (item) {
            return $http.put('/api/item/' + item.id, item).then(function (response) {
                return response.data;
            });
        }
    };
});
