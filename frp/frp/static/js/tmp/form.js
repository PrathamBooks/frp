/*****      Declaration of global variables     *****/
var eachStagePostDataURL = '/api/v1/campaign';
var wholeFormPostDataURL = '/campaign/add';

function getFileSize(fSize){
    var fSExt = new Array('Bytes', 'KB', 'MB', 'GB');
    i=0;while(fSize>900){fSize/=1024;i++;}

    return ((Math.round(fSize*100)/100)+' '+fSExt[i]);
}
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
$(function() {
    $("#goLive").click(function(event){
    	event.preventDefault();
    	if($("input:invalid, textarea:invalid, checkbox:invalid, radio:invalid").length > 0){
    		$(this).parent().find('.alert').removeClass('hide').delay(5000).fadeOut(2000,function(){ 
                $(this).addClass('hide');
                $(this).removeAttr('style'); 
            });
            $("input:invalid, textarea:invalid, checkbox:invalid, radio:invalid").css('border-color','#FF0004');
            $("input:valid, textarea:valid, checkbox:valid, radio:valid").css('border-color','#CCCCCC');
    	}
    	else {
            $("input:valid, textarea:valid, checkbox:valid, radio:valid").css('border-color','#CCCCCC');
    		$.post(wholeFormPostDataURL, $("form.col-sm-9").serializeArray(), function(data){
    			//console.log(data);
    		});
    	}
    });
    $("a#showLeft").click(function(event){
        event.preventDefault();
        $("section").addClass('hide');
        $(":invalid").eq(1).parents('section').removeClass('hide');
    });
    $("input[name=imageUpload]").change(function(){        
        var ext = this.files[0].type;
        if(ext=='image/jpeg' || ext=='image/png' || ext=='image/gif'){
            $(this).parent().find('.alert').addClass('hide');
        } else {
            $(this).parent().find('.alert').removeClass('hide');
        }
    });
    $("input[name=addVideo]").change(function(){
        var fileSize = getFileSize(this.files[0].size);
        var ext = this.files[0].type;
        if(ext=='video/mpeg'){
            $(this).parent().find('.alert').addClass('hide');
            /*  For setting video source we need to upload it.
            $(this).parent().find('video').attr('src',this.files[0].name);
            */
            // Check fileSize here...
        } else {
            $(this).parent().find('.alert').removeClass('hide');
        }
    });

    $('.percentageSlider').slider();
    showBottomNavigation();

	$('div.list-group a, .nav li a, #previous, #next').click(function (e) {
        e.preventDefault();
        var id = $('section:visible').attr('id');
        if($('section#' + id + ' :invalid').length > 0){
            $('section#' + id + ' :invalid').css('border-color','#FF0004');
            $('section#' + id + ' :valid').css('border-color','#CCCCCC');
        }
        else {
            $('section#' + id + ' :valid').css('border-color','#CCCCCC');
            $.post(eachStagePostDataURL, $('form').serializeArray());
            //, function(data){
            //     //console.log(data);
            // });
            $('div.list-group a, .nav li a').removeClass('active');
            $("a[href="+$(this).attr('href')+"]").addClass('active');
            $('section').addClass('hide');
            $('section' + $(this).attr('href')).removeClass('hide');
            showBottomNavigation();
        }        
    });

	$("#addLanguage").click(function(){
		$("#addLanguage").before('<div class="form-group row">'
                            +'<div class="col-xs-4">'
                                +'<select class="form-control" name="language1[]">'
                                    +'<option value="Hindi">Hindi</option>'
                                    +'<option value="English">English</option>'
                                    +'<option value="Marathi">Marathi</option>'
                                    +'<option value="Telugu">Telugu</option>'
                                    +'<option value="Gujarati">Gujarati</option>'
                                    +'<option value="Malayalam">Malayalam</option>'
                                +'</select>'
                            +'</div>'
                            +'<div class="col-xs-4">'
                                +'Number of books in this language (<span id="booksLeft"></span> left)'
                            +'</div>'
                            +'<div class="col-xs-2">'
                                +'<input type="text" class="form-control" name="library[]" placeholder="No. of books" />'
                            +'</div>'
                        +'</div>'
                        
                        +'<table class="table">'
                        +'<tr>'
                          +'<th>Level</th>'
                          +'<th>Percentage</th>'
                          +'<th>Number of Books</th>'
                        +'</tr>'
                        +'<tr>'
                          +'<td>1</td>'
                          +'<td><input type="text" class="percentageSlider" name="percentageSlider1[]" value="" style="width: 300px;" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="0" data-slider-selection="none" data-slider-tooltip="show"></td>'
                          +'<td><span class="level1"></span></td>'
                        +'</tr>'
                        +'<tr>'
                          +'<td>2</td>'
                          +'<td><input type="text" class="percentageSlider" name="percentageSlider2[]" value="" style="width: 300px;" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="0" data-slider-selection="none" data-slider-tooltip="show"></td>'
                          +'<td><span class="level2"></span></td>'
                        +'</tr>'
                        +'<tr>'
                          +'<td>3</td>'
                          +'<td><input type="text" class="percentageSlider" name="percentageSlider3[]" value="" style="width: 300px;" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="0" data-slider-selection="none" data-slider-tooltip="show"></td>'
                          +'<td><span class="level3"></span></td>'
                        +'</tr>'
                        +'<tr>'
                          +'<td>4</td>'
                          +'<td><input type="text" class="percentageSlider" name="percentageSlider4[]" value="" style="width: 300px;" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="0" data-slider-selection="none" data-slider-tooltip="show"></td>'
                          +'<td><span class="level4"></span></td>'
                        +'</tr>'
                        +'<tr>'
                          +'<td>Total</td>'
                          +'<td><input type="text" class="percentageSlider" name="percentageSlider5[]" value="" style="width: 300px;" data-slider-min="0" data-slider-max="100" data-slider-step="1" data-slider-value="0" data-slider-selection="none" data-slider-tooltip="show"></td>'
                          +'<td><span class="level5"></span></td>'
                        +'</tr>'
                        +'</table>');
        $('.table').eq($('.table').length-1).find('.percentageSlider').slider();
	});
	
    $('#bookCounts input').keyup(function(e) {
        var count = 0;
        $('#bookCounts input').each(function(i, e) {
            if (i==1) {
                if (parseInt(e.value)) count += parseInt(e.value) * 125;
            } else {
                if (parseInt(e.value)) count += parseInt(e.value);
            }
        });

        $('#bookAmount').html(count * 30);
        $('#noOfBooks').html(count);
        $('#booksLeft').html(count);
    });
});
