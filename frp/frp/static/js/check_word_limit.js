$(function() {
    $('.form-control').each(function() {
      var max = parseInt($(this).attr('maxlength'))
      if (!max) {
        return;
      }
      $(this).keyup(word_cnt_fn(max));
    }
    var word_cnt_fn = function(max) {
      var state = {created_btn: false, max: max};
      return function() {
      }
    } 


      
    $('.form-control').keyup(function () {
      max = Math.round(max/12);
      var str = $(this).val().split(' ')
      str = jQuery.grep(str, function(value) {
        return value != '';
      });
      var words = str.length
      if ($(this).next().attr('type') == 'temp'){
        var $btn = $(this).next();
      }
      else{
        var $btn = $('<button/>').attr('type','temp');
      }

      if (words >= max) {
        $btn.html('you have reached the limit');
      } else {
        $btn.html(max-words + 'Words left');
      }
      $(this).after($btn);
    });

