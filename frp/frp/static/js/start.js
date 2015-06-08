var Start = function() {
  var that = this;
  this.start = function(arg) {
    if (!arg.logged_in) {
      $('input').attr('disabled','');
      $("#goLive").click(function(e) {
        alert('You need to sign-up and login to start a campaign');
        e.preventDefault();
      });
      return;
    }
    $("#accordion").accordion();
    this.attachErrorUpdateCallbacks();
    this.attachPreviewCallback();
    this.attachOrgCheckboxCallback();
    $('input[name="total_impact_on_children"]').attr('required','');
    $('input[name="project_title"]').attr('required','');
    $('#bookCounts input').change(this.booksCallback);
    $("#goLive").click(this.checkErrorsOnSubmit);
    $("#step8 button").click(this.step8GetStartedCallback);
    // Need to call in the beginning to so that required attribute is
    // set. Not setting in form because we want to avoind printing the
    // '*'
    this.booksCallback(); 
    $(window).on('beforeunload', function(){
        return 'Are you sure you want to leave before saving the form? The form will not be saved.';
    });
  };

  // At the end of step 8 in Introduction, need to go to get started
  this.step8GetStartedCallback = function(e) {
    $('#get-started-tab a').tab('show');
    showBottomNavigation();
  };

  this.checkErrorsOnSubmit = function(e) {
    var active_tab = $('section:visible');
    if (hasInvalidFields(active_tab)) {
      highlightInvalidFieldsAndFocusOnFirst(active_tab);
      e.preventDefault();
    }
    $(window).off('beforeunload');
  };

  this.booksCallback = function(e) {
    var foundOneVal = false;
    $('#bookCounts input').each(function(i, e) {
      if (parseInt(e.value)) {
        foundOneVal = true;
      }
    });
    if (foundOneVal) {
      $('#bookCounts input').removeAttr('required');
      $('#bookCounts input').css('border-color','#CCCCCC');
    }
    else {
      $('#bookCounts input').attr('required', '');
    }

    var count = 0;
    $('#bookCounts input').each(function(i, e) {
      if (i==1) {
        if (parseInt(e.value)) count += parseInt(e.value) * 125;
      } else {
        if (parseInt(e.value)) count += parseInt(e.value);
      }
    });

    var COST_PER_BOOK = 36.75;
    $('#bookAmount').html('Rs. ' + count * COST_PER_BOOK);
    $("input[name='fundingGoal']").attr('value', (count * COST_PER_BOOK));
    $('#noOfBooks').html(count);
    $('#booksLeft').html(count);
  };

  this.attachOrgCheckboxCallback = function() {
    $('input[name="org_work"]').change(function(e) {
      // At least one checked
      if ($('input[name="org_work"]:checked').length > 0) {
        $('input[name="org_work"]').removeAttr('required');
      }
      else {
        $('input[name="org_work"]').attr('required', '');
      }
    });
  };

  this.get_chosen_languages = function() {
    var languages = [];
    if ($('select[name="language1"]').val()) { languages.push($('select[name="language1"]').val()) };
    if ($('select[name="language2"]').val()) { languages.push($('select[name="language2"]').val()) };
    if ($('select[name="language3"]').val()) { languages.push($('select[name="language3"]').val()) };
    return languages;
  };

  // Preview btn populates the modal with the values from the form before 
  // showing the modal
  this.attachPreviewCallback = function() {
    $('.modal').on('show.bs.modal', function (event) {
      var $modal = $(this); 
      $modal.find("#title").text($('input[name="title"]').val());
      var languages = that.get_chosen_languages().join(',');
      if (languages) {
        $modal.find("#languages").text(languages);
      }
      if ($('input[name="total_impact_on_children"]').val()) {
        $modal.find("#total_impact_on_children").text($('input[name="total_impact_on_children"]').val());
      }
      $modal.find("#category").text($('input[name="category"][checked="checked"]').parent().text());
      $modal.find("#status").text($('input[name="organization_status"][checked="checked"]').parent().text());
      if ($('input[name="project_city"]').val() && $('select[name="project_state"]').val()) {
        $modal.find("#location").text($('input[name="project_city"]').val() + ', ' + 
                                      $('select[name="project_state"]').val());
      }
      $modal.find("#website").text($('input[name="website"]').val());
      $modal.find("#facebook").text($('input[name="facebook"]').val());
      $modal.find("#blog").text($('input[name="blog"]').val());
      $modal.find("#target").text($("input[name='fundingGoal']").val());
      $modal.find("#who").text($("textarea[name='project_who_are_you']").val());
      $modal.find("#story").text($("textarea[name='project_description']").val());
      $modal.find("#impact").text($("textarea[name='project_impact']").val());
      $modal.find("#fund_utilization").text($("textarea[name='fund_utilization']").val());
    });
  };

  // Attach callbacks to all inputs so that when they get valid values
  // we can remove the "What's left" link
  this.attachErrorUpdateCallbacks = function() {
    $('input, textarea, select').change(function() {
      if ($(':invalid').length == 0) {
        $('#whatsleft').hide();
      }
    });
  };
};
