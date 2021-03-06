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

        loadTypes: function () {
            return $http.get('/api/types').then(function (response) {
                return response.data;
            });
        },

        updateNode: function (item) {
            return $http.put('/api/item/' + item.id, item).then(function (response) {
                return response.data;
            });
        },

        addNode: function (item, label) {
            return $http.post('/api/' + label, item).then(function (response) {
                return response.data;
            });
        },

        deleteNode: function(item_id) {
            return $http.delete('/api/item/' + item_id);
        },

        addRelationship: function (node1, node2, relName) {
            return $http.post('/api/item/' + node1 + '/' + node2, {'relationship': relName}).then(function (response) {
                return response.data;
            });
        },

        removeRelationship: function (relId) {
            return $http.delete('/api/rel/' + relId).then(function (response) {
                return response.data;
            });
        },

        query: function (q) {
            return $http.post('/api/query', {'query': q}).then(function (response) {
                return response.data;
            });
        },

        loadLabels: function () {
            return $http.get('/api/types').then(function (response) {
                return response.data;
            });
        },

        editLabel: function (label, updated) {
            return $http.put('/api/types/' + label, {'updated': updated}).then(function (response) {
                return response.data;
            });
        }
    };
});
