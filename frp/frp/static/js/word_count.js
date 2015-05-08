$(function ($){
  $('.form-control').each(function(){
    var max = parseInt($(this).attr('maxwords'));
    if (!max) {
      return;
    }
    var $btn = $('<button/>');
    $(this).after($btn);
    $(this).keyup(function () {
      var str = $(this).val().trim();
      if (!str) {
        $btn.hide();
        return;
      } 
      str = str.split(/\s+/);
      var nwords = str.length;
      if (nwords >= max) {
        alert('You have reached the word limit'+max);
        $btn.html('You have reached the word limit');
      } else {
        $btn.html(max - nwords + 'Words left');
      }
      $btn.show();
    });
  });
});
