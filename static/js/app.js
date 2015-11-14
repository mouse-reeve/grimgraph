angular.module('app', ['grimoireService', 'ngRoute'])
.config(function ($httpProvider, $locationProvider, $routeProvider) {
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });

    $routeProvider
        .when('/', {
            controller: 'ListCtrl',
            templateUrl: '/static/partials/list.html'
        })
        .when('/:type', {
            controller: 'ListCtrl',
            templateUrl: 'static/partials/list.html'
        })
        .when('/:type/:id', {
            controller: 'NodeCtrl',
            templateUrl: 'static/partials/node.html'
        })
        .otherwise({
            redirectTo: '/'
        });

    $httpProvider.interceptors.push(function($q) {
        return {
            'response': function(response) {
                var deferred = $q.defer();

                if (response.config.url.startsWith('/api/')) {
                    if (response.data.success) {
                        deferred.resolve(response.data);
                    } else {
                        deferred.reject(response.data);
                    }
                    return deferred.promise;
                }
                return response;
            }
        };
    });
});
