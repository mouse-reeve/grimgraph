angular.module('grimoireService', []).service('Grimoire', function ($http) {
    return {
        load: function (label) {
            label = label ? label : 'grimoires';
            return $http.get('/api/' + label).then(function (response) {
                return response.data;
            });
        }
    };
});
