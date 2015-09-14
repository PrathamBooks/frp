var DiscoverPage = function(args) {
  var that = this;
  this.campaign_data = args.campaign_data;
  this.ndisplayed = 0;
  var DISPLAY_PER_CLICK = 6;
  this.start = function(args) {
    this.display_data = this.campaign_data;
    this.show_after_filter_or_sort(this.campaign_data);
    $('#scroll').click(this.show_next_campaigns);
    $('.row-fluid a').click(function(e) {
      $(this).find('.collapseSign').html(
        $(this).find('.collapseSign').html() == '−' ? '+' : '−'
      );
    });
    $('input[type="checkbox"]').on('change',this.filter_and_sort);
    $('input[name=sort-by]').on('change', this.filter_and_sort);
    $(':radio[value="' + args.category + '"]').click();
    $('.modal').on('hidden.bs.modal', this.on_modal_hide);
  };
  this.filter_and_sort = function(e) {
    e.preventDefault();

    var states = [];
    $states = $('#state').find('input[type=checkbox]:checked');
    $states.each(function() {
      states.push($(this).val());
    });

    var languages = [];
    $languages = $('#language').find('input[type=checkbox]:checked');
    $languages.each(function() {
      languages.push($(this).val());
    });

    var types = [];
    $types = $('#type').find('input[type=checkbox]:checked');
    $types.each(function() {
      types.push($(this).val());
    });

    var filtered_data = that.filter_with_args(states, languages, types);

    var sort_by = $('input[name=sort-by]:checked').val();
    var sorted_data = filtered_data;
    if (sort_by === 'Featured') {
      sorted_data = filtered_data.sort(function(a, b) {
        if (a.status != b.status) {
          if (a.status == 'Active') {
            return -1;
          }
          if (a.status == 'Closed') {
            return 1;
          }
        }
        return (b.featured - a.featured);
      });
    }
    else if (sort_by === 'Popular') {
      sorted_data = filtered_data.sort(function(a, b) {
        if (a.status != b.status) {
          if (a.status == 'Active') {
            return -1;
          }
          if (a.status == 'Closed') {
            return 1;
          }
        }
        return (b.num_donors - a.num_donors);
      });
    }
    else if (sort_by === 'Recently Launched') {
      sorted_data = filtered_data.sort(function(a, b) {
        if (a.status != b.status) {
          if (a.status == 'Active') {
            return -1;
          }
          if (a.status == 'Closed') {
            return 1;
          }
        }
        return (b.days_remaining - a.days_remaining);
      });
    }
    else if (sort_by == 'Ending Soon') {
      sorted_data = filtered_data.sort(function(a, b) {
        if (a.status != b.status) {
          if (a.status == 'Active') {
            return -1;
          }
          if (a.status == 'Closed') {
            return 1;
          }
        }
        return (a.days_remaining - b.days_remaining);
      });
    }
    else if (sort_by == 'Most Funded') {
      sorted_data = filtered_data.sort(function(a, b) {
        if (a.status != b.status) {
          if (a.status == 'Active') {
            return -1;
          }
          if (a.status == 'Closed') {
            return 1;
          }
        }
        return (b.total_donations - a.total_donations);
      });
    }
    that.show_after_filter_or_sort(sorted_data);
  }

  this.show_campaigns = function(data, start, end) {
    var $campaigns = $('#campaigns');
    for (i = start; i < end && i < data.length; i++) {
      var campaign = data[i];
      var $div_md_3 = $('<div/>').addClass('col-md-3').appendTo($campaigns);
      $div_md_3.click(function (campaign) {
        return function() {
          window.location.href = '/campaign/' + campaign.url;
        }
      }(campaign));
      $div_md_3.popover({
        title: campaign.title,
        container: 'body',
        placement: function() { return $(window).width() < 786 ? 'top' : 'left'; },
        content: campaign.description
      });
      $div_md_3.hover(
        function() {
          $(this).popover('show'); 
        },
        function() {
          $(this).popover('hide'); 
        }
      );
      var $h1 = $('<h1/>').appendTo($div_md_3);
      var $img = $('<img/>').
        attr('src', '/static/uploads/size_2/' + campaign.image).
        attr('alt', 'campaign image').
        appendTo($h1);
      var $icons = $('<div/>').addClass('campaign-icons').appendTo($div_md_3);
      if (campaign.target <= campaign.total_donations) {
        $('<span/>').addClass('champion').html('Fully<br> Funded').appendTo($icons);
      }
      if (campaign.featured) {
        $('<span/>').addClass('featured-campaign').html('Featured').appendTo($icons);
      }
      var $title = $('<h2/>').html('<strong>' + campaign.title + '</strong>').appendTo($div_md_3);
      var $campaignInfo = $('<div/>').addClass('campaignInfo').appendTo($div_md_3);
      // var $description = $('<p/>').html(campaign.description).appendTo($campaignInfo);
      var $ul = $('<ul/>').appendTo($campaignInfo);
      var $impact = $('<li/>').html("Children Impacted: " + campaign.impact).appendTo($ul);
      var $langs = $('<li/>').html("Languages: " + campaign.languages).appendTo($ul);
      var $type = $('<li/>').html("Beneficiary Type: " + campaign.type).appendTo($ul);
      var $location = $('<li/>').html("Location: " + campaign.city + ', ' + campaign.state).appendTo($ul);
      $campaignInfo.append($('<hr/>'));
      $campaignInfo.append($('<h6/>').html("Funding Details"));
      var $time_left = $('<time/>').append($('<span/>').text(campaign.days_remaining + ' Days Left'));
      $campaignInfo.append($time_left);

      var $target = $('<h4/>').html(campaign.target);
      var percent_funded = Math.round((campaign.total_donations/campaign.target) * 100);
      var $percentFunded = $('<span/>').
        addClass('percentFunded').
        html(percent_funded).
        appendTo($target);
      $target.appendTo($campaignInfo);
      if (percent_funded > 100){
        percent_funded = 100;
      }
      var $progress_bar = $('<div/>').
        addClass('progress progress-warning').
        css('width', percent_funded + '%').
        css('min-width', '0.2em').
        appendTo($campaignInfo);
      var $progress_span = $('<span/>').
        addClass("sr-only").
        html(percent_funded + '% Complete').
        appendTo($target);
      var $days = $('<h5/>').
        append($('<span/>').addClass('days').html(campaign.status)).
        append($('<span/>').addClass('funders').html(campaign.num_donors)).
        appendTo($campaignInfo);
      if (percent_funded < 100.0 && campaign.status == 'Active') {
        var $donate_link = $('<a/>').attr('href', '/donate/'+campaign.url).
          addClass('btn browse-btn').
          html('Donate').
          appendTo($div_md_3);
      }
      else {
        var $donate_link = $('<a/>').attr('href', '/donate/'+campaign.url).
          addClass('btn browse-btn browse-btn-disabled').
          html('Donate').
          appendTo($div_md_3);
        $donate_link.tooltip({
          title: "We are thankful to donors like you who helped this campaign reach its funding goal. You can help other campaigns similar to this one!."
        });
        $donate_link.click(function(e) {
          e.preventDefault();
          e.stopPropagation(); // Stop the click event propagating to the parent div
        });
      }
    }
  };
  this.show_next_campaigns = function() {
    var start = that.ndisplayed;
    var end = that.ndisplayed + DISPLAY_PER_CLICK < that.display_data.length ?
      that.ndisplayed + DISPLAY_PER_CLICK : 
      that.display_data.length;
    that.show_campaigns(that.display_data, start, end);
    that.ndisplayed = end;
    if (that.ndisplayed == that.display_data.length) {
      $('#scroll').hide();
    }
    else {
      $('#scroll').show();
    }
  };
  this.clear_campaigns = function() {
    that.ndisplayed = 0;
    $('#campaigns').html('');
  };

  this.filter_with_args = function(states, languages, types) {
    var filtered_data = that.campaign_data;;

    if (states && states.length > 0 && states.indexOf('All') == -1) {
      filtered_data = filtered_data.filter(function(c) {
        var found = false;
        _.each(states, function(state) {
          if (c.state.indexOf(state) != -1) {
            found = true;
            return;
          }
        });
        return found;
      });
    }
    if (languages && languages.length > 0 && languages.indexOf('All') == -1) {
      filtered_data = filtered_data.filter(function(c) {
        var found = false;
        _.each(languages, function(language) {
          if (c.languages.indexOf(language) != -1) {
            found = true;
            return;
          }
        });
        return found;
      });
    }
    // There is only one type on a campaign so it is easier to search
    // for the campaign.type in the selected types
    if (types && types.length > 0 && types.indexOf('All') == -1) {
      filtered_data = filtered_data.filter(function(c) {
        return types.indexOf(c.type) != -1;
      });
    }
    return filtered_data;
  };

  this.show_after_filter_or_sort = function(data) {
    that.display_data = data;
    that.clear_campaigns();
    if (that.display_data.length == 0) {
      that.no_campaigns();
      that.display_data = that.campaign_data;
    }
    that.show_next_campaigns();
  };

  this.no_campaigns = function() {
    $('.modal').modal('show');
  }

  this.on_modal_hide = function() {
    $('#state input').prop('checked', false);
    $('#state input[value="All"]').prop('checked', true);
    $('#language input').prop('checked', false);
    $('#language input[value="All"]').prop('checked', true);
    $('#type input').prop('checked', false);
    $('#type input[value="All"]').prop('checked', true);
    $(':radio[value="Featured"]').click();
  };
};
