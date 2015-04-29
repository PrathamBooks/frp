$(document).ready(function() {
  utils = new Utils();
});

var Utils = function() {
  this.fb_share = function(href) {
    FB.ui({
      method: 'share',
      href: href,
    }, function(response){});
  };
  this.popup = function(href) {
    var newwindow=window.open(href,'name','height=300,width=400,top=200,left=400');
    if (window.focus) {newwindow.focus()}
    return false;
  }
  this.twitter_share = function(href, text) {
    var tw_url = "http://twitter.com/share?";
    var args = {
      url: href,
      text: text};
    var args_string = $.param(args);
    var final_url = tw_url + args_string;
    this.popup(final_url);
  }
};

