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
};

