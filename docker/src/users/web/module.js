app = angular.module('MainApp', ['ngRoute', 'ngResource'])

app.config(['$routeProvider', function($routeProvider) {

  $routeProvider
    .when('/perfil/:usuario', {templateUrl: '/componentes/perfil/index.html', controller:'PerfilCtrl'})
    .otherwise({ redirectTo: '/perfil/' });

}]);

app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
