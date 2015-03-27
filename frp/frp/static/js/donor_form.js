var DonorForm = function() {
  var that = this;
  this.start = function() {
    $('form .btn').click(function(e) {
      if ($('[name="amount_choice"]:checked').length == 0 &&
          !parseInt($('[name="customize_amount"]').val())
         ) {
        $('[name="amount_choice"]').attr('required','');
      }
      else {
        $('[name="amount_choice"]').removeAttr('required');
      }
      if ($(':invalid').length > 0) {
        $('form').find(':invalid').first().focus();
        highlightInvalidFields($('form'));
        e.preventDefault();
      }
    });
  }
};
