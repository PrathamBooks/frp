function getFileSize(fSize){
  var fSExt = new Array('Bytes', 'KB', 'MB', 'GB');
  var i=0;
  while(fSize>900) {
    fSize/=1024;
    i++;
  }
  return ((Math.round(fSize*100)/100)+' '+fSExt[i]);
}

function isClickedTabEarlier(active_tab, clicked_tab) {
  var cur_tab = active_tab;
  while (cur_tab.prev().length > 0) {
    cur_tab = cur_tab.prev().first();
    if (cur_tab.is(clicked_tab)) return true;
  }
  return false;
}

function highlightInvalidFields($tab) {
  $tab.find(':valid').css('border-color','#CCCCCC');
  $tab.find(':valid').each(function(){
    if($(this).is(":radio") || $(this).is(":checkbox")){
      $(this).parents('.form-group').find('.alert').addClass('hide');
    }
    else{
      $(this).parent().find('.alert').addClass('hide');
    }
  });
  $tab.find(':invalid').css('border-color','#ffc600');
  $tab.find(':invalid').each(function(){
    if($(this).is(":radio") || $(this).is(":checkbox")){
      $(this).parents('.form-group').find('.alert').removeClass('hide');
    }
    else{
      $(this).parent().find('.alert').removeClass('hide');
    }
  });
}

function showBottomNavigation() {
  if($("section:visible").prev().attr('id')!== undefined && $("section:visible").prev().attr('id').indexOf('step')!== -1) {
    $(".btn-pre").removeClass('hide');
    $(".btn-pre").attr('href','#'+$("section:visible").prev().attr('id'));
  } else $(".btn-pre").addClass('hide');
  if($("section:visible").next().attr('id')!== undefined && $("section:visible").next().attr('id').indexOf('step')!== -1) {
    $(".btn-next").removeClass('hide');
    $(".btn-next").attr('href','#'+$("section:visible").next().attr('id'));
  } else $(".btn-next").addClass('hide');
};

$(function() {
  $("input[name=imageUpload]").change(function(){
    $(this).parent().find('.alert').addClass('hide');
    var ext = this.files[0].type;
    var imageSize = this.files[0].size;
    if (imageSize < MAX_FILE_SIZE) {
      $(this).css('border-color','#FF0004');
      $(this).parent().find('.alert-size').addClass('hide');
    }
    else {
      $(this).css('border-color','#FF0004');
      $(this).parent().find('.alert-size').removeClass('hide');
    }

    if(ext=='image/jpeg' || ext=='image/png' || ext=='image/gif'){
      $(this).css('border-color','#CCCCCC');
      $(this).parent().find('.alert-type').addClass('hide');
    } else {
      $(this).css('border-color','#FF0004');
      $(this).parent().find('.alert-type').removeClass('hide');
    }
  });
  $("input[name=addVideo]").change(function(){
    var fileSize = getFileSize(this.files[0].size);
    var ext = this.files[0].type;
    if(ext=='video/mpeg'){
      $(this).parent().find('.alert').addClass('hide');
      // For setting video source we need to upload it.
      // $(this).parent().find('video').attr('src',this.files[0].name);
      // Check fileSize here...
    } else {
      $(this).parent().find('.alert').removeClass('hide');
    }
  });

  $('.percentageSlider').slider();
  showBottomNavigation();

  $('div.sidebar a, .btn-pre, .btn-next').click(function (e) {
    e.preventDefault();
    var id = $('section:visible').attr('id');
    var active_tab = $('section:visible');
    var clicked_tab = $($(this).attr('href'));
    if (isClickedTabEarlier(active_tab, clicked_tab) || $('section#' + id + ' :invalid').length == 0) {
      clicked_tab.parent().parent().find('div.sidebar a').removeClass('active');
      $("a[href="+$(this).attr('href')+"]").addClass('active');
      clicked_tab.parent().find('section').removeClass('show').addClass('hide');
      $('section' + $(this).attr('href')).removeClass('hide').addClass('show');
      showBottomNavigation();
      window.scrollTo($('section:visible').position().left,
                      $('section:visible').position().top);
    }
    else {
      $('section#' + id + ' :invalid').first().focus();
      highlightInvalidFields(active_tab);
      return false;
    } 
  });
});
