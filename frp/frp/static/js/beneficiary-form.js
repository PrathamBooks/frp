function addNumberOfBooks(col_num) {
    var sum = 0;

    $('.js-no-books-col-' + col_num).each( function ( index,  el ) {
        sum += parseInt(el.value) ? parseInt(el.value) : 0;
    } );
    $('#js-total-books-col-' + col_num).val(sum);
}

function updateGrossTotal() {
    var sum = parseInt($('#js-total-books-col-1').val()) ? parseInt($('#js-total-books-col-1').val()) : 0;

    sum += parseInt($('#js-total-books-col-2').val()) ? parseInt($('#js-total-books-col-2').val()) : 0;

    sum += parseInt($('#js-total-books-col-3').val()) ? parseInt($('#js-total-books-col-3').val()) : 0;

    $("#js-books-gross-total").val(sum);
}

function displayTotalCount() {
    $('.js-no-books-col-1').on('change keyup paste', function () {
        addNumberOfBooks('1'); updateGrossTotal();
    }).change();
    $('.js-no-books-col-2').on('change keyup paste', function () {
        addNumberOfBooks('2'); updateGrossTotal();
    }).change();
    $('.js-no-books-col-3').on('change keyup paste', function () {
        addNumberOfBooks('3'); updateGrossTotal();
    }).change();
}

$(document).ready( displayTotalCount );


function gotoBeneficiaryStep(step) {
    window.location = "/signup/beneficary/" + step + "/";
}
