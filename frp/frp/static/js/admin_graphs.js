var AdminGraphs = function(user_data, campaign_data, donation_data) {
  var that = this;
  this.user_data = user_data;
  this.campaign_data = campaign_data;
  this.donation_data = donation_data;

  this.start = function() {
    $graph_div = $('#graph');
    this.user_graph(this.user_data, $('#user-graph'));
    this.campaign_graph(this.campaign_data, $('#campaign-graph'));
    this.donation_graph(this.donation_data, $('#donation-graph'));
  };

  this.get_dates = function(data) {
    var first_user = data[0];
    var start_date = new Date(first_user.year, first_user.month, first_user.day, 0, 0, 0);

    var last_user = data[data.length - 1];
    var end_date = new Date(last_user.year, last_user.month, last_user.day, 0, 0, 0);

    // Find all the dates from first user to last user
    var dates = [];
    for (var d = start_date; d <= end_date; d.setDate(d.getDate() + 1)) {
      dates.push([new Date(d), 0]);
    }
    var cur_user_date;
    var cur_date_index;
    var i;
    for (i = 0, cur_date_index = 0; i < data.length; i++) {
      var cur_user = data[i];
      cur_user_date = new Date(cur_user.year, cur_user.month, cur_user.day, 0, 0, 0);
      while (dates[cur_date_index][0] < cur_user_date) {
        cur_date_index += 1;
      } 
      dates[cur_date_index][1] += 1;
    }

    dates[0][0] = dates[0][0].getDate() + '/' + dates[0][0].getMonth();
    for (i = 1; i < dates.length; i++) {
      dates[i][0] = dates[i][0].getDate() + '/' + dates[i][0].getMonth();
      dates[i][1] += dates[i - 1][1];
    }

    return dates;
  };

  this.user_graph = function(user_data, $div) {
    dates = that.get_dates(user_data);
    // dates will contain tuples with date and the number of users who signed up
    // on that day
    // Create the data table.
    var user_chart_data = new google.visualization.DataTable();
    user_chart_data.addColumn('string', 'Date');
    user_chart_data.addColumn('number', 'Users');
    user_chart_data.addRows(dates);

    // Set chart options
    var user_options = {'title':'Users',
      'width':1200,
      'height':300,
      'colors' : ['#ffc600']};
      // Instantiate and draw our chart, passing in some options.
      var user_chart = new google.visualization.ColumnChart($div.get(0));
      user_chart.draw(user_chart_data, user_options);
  };

  this.campaign_graph = function(campaign_data, $div) {
    dates = that.get_dates(campaign_data);
    // dates will contain tuples with date and the number of users who signed up
    // on that day
    // Create the data table.
    var user_chart_data = new google.visualization.DataTable();
    user_chart_data.addColumn('string', 'Date');
    user_chart_data.addColumn('number', 'Campaigns');
    user_chart_data.addRows(dates);

    // Set chart options
    var user_options = {'title':'Campaigns',
      'width':1200,
      'height':300,
      'colors' : ['#ffc600']};
      // Instantiate and draw our chart, passing in some options.
      var user_chart = new google.visualization.ColumnChart($div.get(0));
      user_chart.draw(user_chart_data, user_options);
   };

  this.donation_graph = function(donation_data, $div) {
    dates = that.get_dates(donation_data);
    // dates will contain tuples with date and the number of users who signed up
    // on that day
    // Create the data table.
    var user_chart_data = new google.visualization.DataTable();
    user_chart_data.addColumn('string', 'Date');
    user_chart_data.addColumn('number', 'Donations');
    user_chart_data.addRows(dates);

    // Set chart options
    var user_options = {'title':'Donations',
      'width':1200,
      'height':300,
      'colors' : ['#ffc600']};
      // Instantiate and draw our chart, passing in some options.
      var user_chart = new google.visualization.ColumnChart($div.get(0));
      user_chart.draw(user_chart_data, user_options);
   };
}

