var ajaxify_category_form = function() {
    $("#create_category").submit(function(event) {
        var url = $("button[form='create_category']").attr("data-async-submit");
        var data = $("#create_category").serializeArray();
        $.post(url, data).done(
            function(data, textStatus, jqXHR) {
                $("div#message").text(data['message']).show().fadeOut(1000);
            }).fail(function(jqXHR, textStatus, errorThrown) {
                var resp = $.parseJSON(jqXHR.responseText);
                var message = resp['errors'][0]['message'];
                $("div#message").text(message).show().fadeOut(2000);
            });
        event.preventDefault();
    });
};

$(function() {
    $("input.datepicker").datepicker({dateFormat : "yy-mm-dd"});
    ajaxify_category_form();
});

