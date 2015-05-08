$(function ($){
  $('.form-control').each(function(){
    var max = parseInt( $(this).attr('maxwords'));
    if (!max){
      return;
    }
    var $btn = $('<button/>');
    $(this).after($btn);
    $(this).keyup(function () {
      var str = $(this).val().trim();
      if (!str) {
        $btn.hide();
        return;
      }else {
        str = str.split(/\s+/);
        var words = str.length;
      }
      if (words >= max) {
        alert('You have reached the word limit'+max);
        $btn.html('You have reached the word limit');
      }else {
        $btn.html(max- words + 'Words left');
      }
      $btn.show();
    });
  });
});
