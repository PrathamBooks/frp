/******     Angular Starts here     ******/
var signupApp = angular.module('signupApp',['ui.bootstrap']);
signupApp.directive('showtab',
    function () {
        return {
            link: function (scope, element, attrs) {
                element.click(function(e) {
                    e.preventDefault();
                    $(element).tab('show');
                    $("section").addClass('hide');
                    //console.log("section"+$(element)[0].hash);
                    $("section"+$(element)[0].hash).removeClass('hide');
					showBottomNavigation();
                });
            }
        };
    });

signupApp.controller('signupController', ['$scope', function($scope) {
    $scope.signup = {};
	
	$scope.signup.imageUploadStatus=false;
	$scope.signup.imageUpload='';
	$scope.$watch('signup.imageUpload', function() {
       
	   if(document.getElementById('imageUpload').files[0]!=undefined){
		   console.log(document.getElementById('imageUpload').files[0]);
		   var ext = document.getElementById('imageUpload').files[0].type;
		   if(ext=='image/jpeg' || ext=='image/png' || ext=='image/gif'){
				$(this).css('border-color','#CCCCCC');
				$scope.signup.imageUploadStatus=false;
				$(this).parent().find('.alert').addClass('hide');
			} else {
				$(this).css('border-color','#FF0004');
				$scope.signup.imageUploadStatus=false;
				$(this).parent().find('.alert').removeClass('hide');
			}
	   }
	});
}]);

function signupController($scope, $http) {
    $scope.signup = {};
}

function signupTabs($scope, $http) {
    $scope.signup = {};
	
    $scope.createTabs = [
        { title:"Step1", anchor:"#step1", content:"Step1", active:true },
        { title:"Step2", anchor:"#step2", content:"Step2", active:false },
        { title:"Step3", anchor:"#step3", content:"Step3", active:false },
        { title:"Step4", anchor:"#step4", content:"Step4", active:false }
    ];
    
    $scope.tabs = function(){
        this.tab('show');
    };	
}

/*******		General Functions		*********/
$(function(){
    //$("section").removeClass('hide');
	showBottomNavigation();
});

function showBottomNavigation(){
    if($("section:visible").prev().attr('id')!== undefined && $("section:visible").prev().attr('id').indexOf('step')!== -1) {
        $("#previous").removeClass('hide');
        $("#previous").attr('href','#'+$("section:visible").prev().attr('id'));
    }else $("#previous").addClass('hide');
    if($("section:visible").next().attr('id')!== undefined && $("section:visible").next().attr('id').indexOf('step')!== -1) {
        $("#next").removeClass('hide');
        $("#next").attr('href','#'+$("section:visible").next().attr('id'));
    }else $("#next").addClass('hide');
}