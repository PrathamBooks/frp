var DiscoverPage = function(campaign_data) {
  this.campaign_data = campaign_data;
  this.start = function() {
    this.show_campaigns(this.campaign_data);
  };
  this.show_campaigns = function(data) {
    var $campaigns = $('#campaigns');
    for (i = 0; i < data.length; i++) {
      var campaign = data[i];
      var $div_md_3 = $('<div/>').addClass('col-md-3').appendTo($campaigns);
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
      var $percentFunded = $('<span/>').addClass('percentFunded').html(110).appendTo($target);
      $target.appendTo($campaignInfo);
      var $progress = $('<div/>').addClass('progress progress-warning').appendTo($campaignInfo);
      var $bar = $('<div/>').addClass('bar').css('width', '20%').appendTo($progress);
      var $days = $('<h5/>').
        append($('<span/>').addClass('days').html('Active')).
        append($('<span/>').addClass('funders').html(110)).
        appendTo($campaignInfo);
    }
  };
};
