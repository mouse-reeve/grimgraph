angular.module('grimoireService', []).service('Grimoire', function ($http) {
    return {
        grimoires: function () {
            return $http.get('/api/grimoires').then(function (response) {
                return response.data;
            });
        }
    };
});
