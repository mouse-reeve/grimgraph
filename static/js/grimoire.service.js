angular.module('grimoireService', []).service('Grimoire', function ($http) {
    return {
        start: function () {
            return $http.get('/api/item').then(function (response) {
                return response.data;
            });
        }
    };
});
