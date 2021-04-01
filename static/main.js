(function() {
    'use strict';

    angular.module('WordcountApp', [])

    .controller('WordcountController', ['$scope', '$log', '$http', '$timeout',
        function($scope, $log, $http, $timeout) {

            // Dependency Injection and whatnot
            $scope.submitButtonText = 'Submit'; // Ok so string do have to be in single quotes?
            $scope.loading = false;
            $scope.getResults = function() {
                $log.log("test");

                // Get the URL from the input
                var userInput = $scope.url;

                // Fire the API request
                // Is this an ES6 promise?
                $http.post('/start', {"url": userInput})
                    .success(function(results) {
                        $log.log(results);
                        // Successful HTTP request results in calling getWordCount
                        getWordCount(results);
                        // Set wordcounts to null so that "the old values get cleared out" -> Not sure where that happens
                        $scope.wordcounts = null;
                        // Set loading to true so that submit button will be disabled via ng-disabled directive
                        $scope.loading = true;
                        $scope.submitButtonText = "Loading...";
                    })
                    .error(function(error){
                        $log.log(error);
                    });

            };
            function getWordCount(jobID) {
                var timeout = "";   // Okay, let's stick to var instead of let from now on

                var poller = function() {
                    // Fire another request
                    $http.get('/results/'+jobID)
                        /* Okay so we send a GET request to that page until the job is executed and we get data
                            back from the page
                        */
                        .success(function(data, status, headers, config) {
                            if(status === 202) {
                                $log.log(data, status);
                            } else if (status === 200) {
                                $log.log(data);
                                $scope.loading = false;
                                $scope.submitButtonText = "Submit";
                                // Add the results to the $scope object so it's available in the View
                                $scope.wordcounts = data;
                                // When the page is available w/ data, cancel the timeout
                                $timeout.cancel(timeout);
                                return false;
                            }
                            /* Continue to call the poller() function every 2 seconds
                                until the timeout is cancelled */
                            timeout = $timeout(poller, 2000); // Poll every 2 seconds until timeout is cancelled (w/ a 200 response)
                        });
                };
                poller();
            }

        }
    ]);
}());
