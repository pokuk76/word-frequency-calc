(function(){
    'use strict';

    angular.module('WordcountApp', [])

    .controller('WordcountController', ['$scope', '$log', '$http',
        function($scope, $log, $http) {
            // Dependency Injection and whatnot
            $scope.getResults = function() {
                $log.log("test");

                // Get the URL from the input
                var userInput = $scope.url;

                // Fire the API request
                // Is this an ES6 promise?
                $http.post('/start', {"url": userInput}).
                    success(function(results) {
                        $log.log(results);
                    }).
                    error(function(error){
                        $log.log(error);
                    });

            };
        }
    ]);

}());
