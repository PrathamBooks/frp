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
    $("#previous").removeClass('hide');
    $("#previous").attr('href','#'+$("section:visible").prev().attr('id'));
  } else $("#previous").addClass('hide');
  if($("section:visible").next().attr('id')!== undefined && $("section:visible").next().attr('id').indexOf('step')!== -1) {
    $("#next").removeClass('hide');
    $("#next").attr('href','#'+$("section:visible").next().attr('id'));
  } else $("#next").addClass('hide');
};

$(function() {
  $("input[name=imageUpload]").change(function(){
    var ext = this.files[0].type;
    if(ext=='image/jpeg' || ext=='image/png' || ext=='image/gif'){
      $(this).css('border-color','#CCCCCC');
      $(this).parent().find('.alert').addClass('hide');
    } else {
      $(this).css('border-color','#FF0004');
      $(this).parent().find('.alert').removeClass('hide');
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

  $('div.sidebar a, #previous, #next').click(function (e) {
    e.preventDefault();
    var id = $('section:visible').attr('id');
    var active_tab = $('section:visible');
    var clicked_tab = $($(this).attr('href'));
    if (isClickedTabEarlier(active_tab, clicked_tab) || $('section#' + id + ' :invalid').length == 0) {
      $('div.sidebar a').removeClass('active');
      $("a[href="+$(this).attr('href')+"]").addClass('active');
      $('section').removeClass('show').addClass('hide');
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
