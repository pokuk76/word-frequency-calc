(function() {
    'use strict';

    angular.module('WordcountApp', [])

    .controller('WordcountController', ['$scope', '$log', '$http', '$timeout',
        function($scope, $log, $http, $timeout) {

            // Dependency Injection and whatnot
            $scope.submitButtonText = 'Submit'; // Ok so string do have to be in single quotes?
            $scope.loading = false;
            $scope.urlerror = false;
            $scope.getResults = function() {
                // Get the URL from the input
                var userInput = $scope.url;

                // Fire the API request
                // Is this an ES6 promise?
                $http.post('/start', {"url": userInput})
                    .success(function(results) {
                        $log.log("Results from /start endpoint:", results);
                        // Successful HTTP request results in calling getWordCount
                        getWordCount(results);
                        $scope.urlerror = false;
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

                                $log.log("Data from 202: ", data, status);
                            } else if (status === 200) {
                                $log.log("Data from 200: ", data);
                                if (data['error_status']) {
                                    // If the data doesn't have an error,
                                    // the value for that key will be undefined, which evaluates to false
                                    $scope.urlerror = true;
                                    $scope.loading = false;
                                    $scope.submitButtonText = "Submit";
                                    $scope.wordcounts = {}; // Wordcounts should just be an empty JSON
                                    $timeout.cancel(timeout);
                                    return false;
                                }
                                $scope.loading = false;
                                $scope.submitButtonText = "Submit";
                                // Add the results to the $scope object so it's available in the View
                                $scope.wordcounts = data; // For some reason, data is coming back as an array instead of a JSON object

                                // When the page is available w/ data, cancel the timeout
                                $timeout.cancel(timeout);
                                return false;
                            }
                            /* Continue to call the poller() function every 2 seconds
                                until the timeout is cancelled */
                            timeout = $timeout(poller, 2000); // Poll every 2 seconds until timeout is cancelled (w/ a 200 response)
                        })
                        .error(function(error) {
                            $log.log(error);
                            $scope.loading = false;
                            $scope.submitButtonText = 'Submit';
                            $scope.urlerror = true;
                        });
                };
                poller();
            };
        }
    ])

    .directive('wordCountChart', ['$parse', '$log', function($parse, $log)  {
        return {
            restrict: 'E', // Creates a Directive that is restricted to an HTML element
            replace: true, // Replaces the HTML Directive with the HTML in the template below
            template: '<div id="chart"></div>',
            link: function(scope) {  // Allows access to the variables in the scope defined in the controller
                scope.$watch('wordcounts', function() {
                    // Clear out chart each time $scope.watch is called
                    d3.select('#chart').selectAll('*').remove();

                    var data = scope.wordcounts;
                    for (var word_index in data) {
                        $log.log("Word in Data: ", word_index);

                        var key = data[word_index][0];
                        var value = data[word_index][1];
                        d3.select('#chart')
                          .append('div')
                          .selectAll('div')
                          .data(word_index) //  Not sure about this line
                          .enter()
                          .append('div')
                          .style('width', function() {
                            return (value * 3) + 'px';
                          })
                          .text(function(d) {
                            return key;
                          });
                    }
                }, true);
            },
        };
    }]);
}());
