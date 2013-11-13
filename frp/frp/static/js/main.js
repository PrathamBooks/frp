var ajaxify_category_form = function() {
    var form_success = function(responseText, statusText, xhr, el) { 
        var data = $.parseJSON(xhr.responseText);
        $("div#message").text(data['message']).show().fadeOut(1000);
    };
    
    var form_error = function(xhr, status, error) { 
        var data = $.parseJSON(xhr.responseText);
        $("div#message").text(data['message']).show().fadeOut(1000);
    };

    
    $("#create_category").submit(function(event) {
        var options = { "success" : form_success,
                        "error" : form_error,
                        "url" : $("button[form='create_category']").attr("data-async-submit")
                      };
        $(this).ajaxSubmit(options);
        return false;
    });
};

$(function() {
    $("input.datepicker").datepicker({dateFormat : "yy-mm-dd"});
    ajaxify_category_form();
});

