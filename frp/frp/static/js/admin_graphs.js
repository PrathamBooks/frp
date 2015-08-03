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
    this.donations_per_user_graph(this.donation_data, $('#donation-per-user-graph'));
  };

  this.get_dates = function(data, init_func, add_func) {
    var first = data[0];
    var start_date = new Date(first.year, first.month, first.day, 0, 0, 0);

    var last = data[data.length - 1];
    var end_date = new Date(last.year, last.month, last.day, 0, 0, 0);

    // Find all the dates from first to last user
    var dates = [];
    for (var d = start_date; d <= end_date; d.setDate(d.getDate() + 1)) {
      dates.push(init_func(d));
    }
    var cur_data_date;
    var cur_date_index;
    var i;
    for (i = 0, cur_date_index = 0; i < data.length; i++) {
      var cur_data = data[i];
      cur_data_date = new Date(cur_data.year, cur_data.month, cur_data.day, 0, 0, 0);
      while (dates[cur_date_index][0] < cur_data_date) {
        cur_date_index += 1;
      }
      add_func(dates[cur_date_index], cur_data); // [1] += 1;
    }

    var j;
    dates[0][0] = dates[0][0].getDate() + '/' + dates[0][0].getMonth();
    for (i = 1; i < dates.length; i++) {
      dates[i][0] = dates[i][0].getDate() + '/' + dates[i][0].getMonth();
      for (j = 1; j < dates[1].length; j++) {
        dates[i][j] += dates[i - 1][j];
      }
    }

    return dates;
  };

  this.base_init = function(d) {
    return [new Date(d), 0];
  };

  this.base_add = function(entry) {
    entry[1] += 1;
  };
  this.user_graph = function(user_data, $div) {
    dates = that.get_dates(user_data, that.base_init, that.base_add);
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
      var user_chart = new google.charts.Bar($div.get(0));
      user_chart.draw(user_chart_data, user_options);
  };

  this.campaign_graph = function(campaign_data, $div) {
    dates = that.get_dates(campaign_data, that.base_init, that.base_add);
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
      var user_chart = new google.charts.Bar($div.get(0));
      user_chart.draw(user_chart_data, user_options);
   };

   this.donation_graph = function(donation_data, $div) {
     var init = function(d) {
       return [new Date(d), 0, 0];
     };

     var add = function(entry, cur_data) {
       entry[1] += 1;
       entry[2] += cur_data.amount;
     }

     dates = that.get_dates(donation_data, init, add);
     // dates will contain tuples with date and the number of users who signed up
     // on that day
     // Create the data table.
     var user_chart_data = new google.visualization.DataTable();
     user_chart_data.addColumn('string', 'Date');
     user_chart_data.addColumn('number', 'Number of Donations');
     user_chart_data.addColumn('number', 'Sum Donations');
     user_chart_data.addRows(dates);

     // Set chart options
     var user_options = {
       'width':1200,
       'height':300,
       chart: {
         'title':'Donations'
       },
       series: {
         0: {axis: 'nDonations'},
         1: {axis: 'Donations'}
       },
       axes: {
         nDonations: {label: "Number of Donations"},
         Donations: {side: 'right', label: "Amount of Donations"}
       },
       'colors' : ['#ffc600', '#dd2300']
     };
     // Instantiate and draw our chart, passing in some options.
     var user_chart = new google.charts.Bar($div.get(0));
     user_chart.draw(user_chart_data, user_options);
   };

   this.donations_per_user_graph = function(donation_data, $div) {
     var donors = {};
     var i;
     _.each(donation_data, function(donation) {
       if (!donors[donation.donor]) {
         donors[donation.donor] = {number : 0,
                                   amount : 0};
       }
       donors[donation.donor].number += 1;
       donors[donation.donor].amount += donation.amount;
     });

     var max_num_donations = 0;
     _.each(donors, function(data) {
       max_num_donations = data.number > max_num_donations ? data.number : max_num_donations;
     });

     var chart_data = [];
     for (i = 0; i <= max_num_donations; i++) {
       chart_data.push([i, 0]);
     };
     _.each(donors, function(data) {
       chart_data[data.number][1] += 1;
     });

     var user_chart_data = new google.visualization.DataTable();
     user_chart_data.addColumn('number', '#Donations');
     user_chart_data.addColumn('number', '#Users');
     user_chart_data.addRows(chart_data);
     var user_options = {
       'width':1200,
       'height':300,
       chart: {
         'title':'Donation Stats Per User'
       },
       'colors' : ['#ffc600', '#dd2300']
     };
     // Instantiate and draw our chart, passing in some options.
     var user_chart = new google.charts.Bar($div.get(0));
     user_chart.draw(user_chart_data, user_options);
    }
};

