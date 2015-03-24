var DiscoverPage = function(campaign_data) {
  var that = this;
  this.campaign_data = campaign_data;
  this.display_data = campaign_data;
  this.ndisplayed = 0;
  var DISPLAY_PER_CLICK = 6;
  this.start = function() {
    this.display_data = this.campaign_data;
    this.show_next_campaigns();
    $('#scroll').click(this.show_next_campaigns);
    $('#filter-btn').click(this.filter);
  };
  this.show_campaigns = function(data, start, end) {
    var $campaigns = $('#campaigns');
    for (i = start; i < end && i < data.length; i++) {
      var campaign = data[i];
      var $div_md_3 = $('<div/>').addClass('col-md-3').appendTo($campaigns);
      $div_md_3.click(function() {
        window.location.replace('/campaign/' + campaign.id);
      });
      var $img = $('<h1/>').html(campaign.title).appendTo($div_md_3);
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
      var $percentFunded = $('<span/>').
        addClass('percentFunded').
        html(Math.round((campaign.total_donations/campaign.target) * 100)).
        appendTo($target);
      $target.appendTo($campaignInfo);
      var $progress = $('<div/>').addClass('progress progress-warning').appendTo($campaignInfo);
      var $bar = $('<div/>').addClass('bar').css('width', '20%').appendTo($progress);
      var $days = $('<h5/>').
        append($('<span/>').addClass('days').html('Active')).
        append($('<span/>').addClass('funders').html(campaign.nfunders)).
        appendTo($campaignInfo);
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

  this.filter = function(e) {
    e.preventDefault();
    var states = $('#states').val();
    var languages = $('#languages').val();
    var types_string = $('#types option:selected').text();
    var filtered_data = that.campaign_data;;
    if (states && states.length > 0) {
      filtered_data = filtered_data.filter(function(c) {
        var found = false;
        _.each(states, function(state) {
          if (c.state.indexOf(state) != -1) {
            found = true;
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
          }
        });
        return found;
      });
    }
    // There is only one type on a campaign so it is easier to search
    // for the campaign.type in the selected types
    if (types_string.length > 0) {
      filtered_data = filtered_data.filter(function(c) {
        return (types_string.indexOf(c.type) != -1);
      });
    }
    that.display_data = filtered_data;
    that.clear_campaigns();
    that.show_next_campaigns();
  };
};
