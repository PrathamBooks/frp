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
  };
  //  super(Email, self).__init__(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE, message)

  // At the end of step 8 in Introduction, need to go to get started
  this.step8GetStartedCallback = function(e) {
    $('#get-started-tab a').tab('show');
    showBottomNavigation();
  };

  this.checkErrorsOnSubmit = function(e) {
    var active_tab = $('section:visible');
    if (active_tab.find(':invalid').length > 0) {
      active_tab.find(':invalid').first().focus();
      highlightInvalidFields(active_tab);
      e.preventDefault();
    }
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

    $('#bookAmount').html(count * 50);
    $("input[name='fundingGoal']").attr('value', (count * 50));
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

  // Preview btn populates the modal with the values from the form before 
  // showing the modal
  this.attachPreviewCallback = function() {
    $('.modal').on('show.bs.modal', function (event) {
      var $modal = $(this); 
      $modal.find("#category").text($('input[name="category"][checked="checked"]').parent().text());
      $modal.find("#title").text($('input[name="title"]').val());
      $modal.find("#status").text($('input[name="organization_status"][checked="checked"]').parent().text());
      $modal.find("#address").text($('input[name="address"]').val());
      $modal.find("#contact_number").text($('input[name="contact_number"]').val());
      $modal.find("#email").text($('input[name="email"]').val());
      $modal.find("#has_80g_certificate").text($('input[name="has_80g_certificate"][checked="checked"]').parent().text());
      $modal.find("#person1_name").text($('input[name="person1_name"]').val());
      $modal.find("#person1_position").text($('input[name="person1_position"]').val());
      $modal.find("#person1_email").text($('input[name="person1_email"]').val());
      $modal.find("#person1_phone").text($('input[name="person1_phone"]').val());
      $modal.find("#modal-noOfBooks").text($('#noOfBooks').html());
      $modal.find("#modal-fundingGoal").text($("input[name='fundingGoal']").val());
      $modal.find("#modal-project-title").text($('input[name="project_title"]').val());
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
  this.showErrorModal = function() {
  };
};
