var DiscoverPage = function(args) {
  var that = this;
  this.campaign_data = args.campaign_data;
  this.ndisplayed = 0;
  var DISPLAY_PER_CLICK = 6;
  this.start = function(args) {
    this.display_data = this.campaign_data;
    this.filter_with_args(args.filters.states, 
                          args.filters.languages, 
                          args.filters.types_string);
    $('#scroll').click(this.show_next_campaigns);
    // $('#filter-btn').click(this.filter);
    $('input[type="checkbox"]').on('change',this.filter);
    $('.row-fluid a').click(function(e) {
      $(this).find('.collapseSign').html(
        $(this).find('.collapseSign').html() == '−' ? '+' : '−'
      );
    });
  };
  this.show_campaigns = function(data, start, end) {
    var $campaigns = $('#campaigns');
    for (i = start; i < end && i < data.length; i++) {
      var campaign = data[i];
      var $div_md_3 = $('<div/>').addClass('col-md-3').appendTo($campaigns);
      $div_md_3.click(function (campaign) {
        return function() {
          window.location.replace('/campaign/' + campaign.id);
        }
      }(campaign));
      var $h1 = $('<h1/>').appendTo($div_md_3);
      var $img = $('<img/>').
        attr('src', '/static/uploads/uploads/' + campaign.image).
        attr('alt', 'campaign image').
        appendTo($h1);
      if (campaign.target <= campaign.total_donations) {
        $('<span/>').addClass('champion').html('Fully<br> Funded').appendTo($div_md_3);
      }
      var $title = $('<h2/>').html(campaign.title).appendTo($div_md_3);
      var $campaignInfo = $('<div/>').addClass('campaignInfo').appendTo($div_md_3);
      var $description = $('<p/>').html(campaign.description).appendTo($campaignInfo);
      var $ul = $('<ul/>').appendTo($campaignInfo);
      var $impact = $('<li/>').html("Impact: " + campaign.impact).appendTo($ul);
      var $langs = $('<li/>').html("Languages: " + campaign.languages).appendTo($ul);
      var $type = $('<li/>').html("Beneficiary Type: " + campaign.type).appendTo($ul);
      var $location = $('<li/>').html("Location: " + campaign.city + ', ' + campaign.state).appendTo($ul);
      $campaignInfo.append($('<hr/>'));
      $campaignInfo.append($('<h6/>').html("Funding Details"));
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
        append($('<span/>').addClass('days').html('Active')).
        append($('<span/>').addClass('funders').html(campaign.num_donors)).
        appendTo($campaignInfo);
      var $donate_link = $('<a/>').attr('href', '/donate/'+campaign.id).
        addClass('btn browse-btn').
        html('Donate').
        appendTo($div_md_3);
    }
  };
  this.show_next_campaigns = function() {
    var start = that.ndisplayed;
    var end = that.ndisplayed + DISPLAY_PER_CLICK < that.campaign_data.length ?
      that.ndisplayed + DISPLAY_PER_CLICK : 
      that.campaign_data.length;
    that.show_campaigns(that.display_data, start, end);
    that.ndisplayed = end;
    if (that.ndisplayed == that.display_data.length) {
      $('#scroll').hide();
    }
  };
  this.clear_campaigns = function() {
    that.ndisplayed = 0;
    $('#campaigns').html('');
  };

  this.filter_with_args = function(states, languages, types) {
    var filtered_data = that.campaign_data;;

    if (states && states.length > 0) {
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
    if (languages && languages.length > 0) {
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
    if (types.length > 0) {
      filtered_data = filtered_data.filter(function(c) {
        return types.indexOf(c.type) != -1;
      });
    }
    that.display_data = filtered_data;
    that.clear_campaigns();
    if (that.display_data.length == 0) {
      that.no_campaigns();
      that.display_data = that.campaign_data;
    }
    that.show_next_campaigns();
  };

  this.no_campaigns = function() {
    $('.modal').modal('show');
    $('#states').val('');
    $('#languages').val('');
    $('#types').val('');
  };

  this.filter = function(e) {
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

    that.filter_with_args(states, languages, types);
  };
};
