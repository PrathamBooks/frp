var AdminPage = function(campaign_data) 
{
  var that = this;
  this.campaign_data = campaign_data;
  this.start = function() {
    this.show_campaigns(this. campaign_data);
    $('#campaigns').on('change', 'select', function(e) {
      var id = parseInt($(this).parents('tr').attr('id').replace ( /[^\d.]/g, '' ),10);
      var status = $(this).val();
      $.ajax({
        type: "POST",
        url: "/change_status",
        data: {
          campaign_id: id,
          updated_status: status
        },
        success: function(data) {
          that.replace_campaign_data(data);
          alert("Status of campaign [ " + data.title + " ] changed to: " + status);
        },
        error: function(errMsg) {
          alert(errMsg);
        }
      });
    });

    $('#campaigns').on('click', '.glyphicon', function(e) {
      var id = parseInt($(this).parents('tr').attr('id').replace ( /[^\d.]/g, '' ),10);
      $.ajax({
        type: "POST",
        url: "/change_featured",
        data: {
          campaign_id: id,
        },
        success: function(data) {
          that.replace_campaign_data(data);
          alert("Campaign [ " + data.title + " ] is now " + (data.featured ? "featured" : "not featured"));
        },
        error: function(errMsg) {
          alert(errMsg);
        }
      });
     });

    $('#campaigns').on('click','.btn.btn-comment',function(e) {
      var id = parseInt($(this).parents('tr').attr('id').replace(/[^\d.]/g, ''),10);
      $('#CommentsModal').find(".modal-content").attr('id',"modal"+id);
      $('#CommentsModal').find('.comments').html('');
    });

    $('#CommentsModal').on('click','#comment-submit-btn',function(e) {
      var comment = $('#CommentsModal').find('#comments').val()
      var id = parseInt($(this).parents('.modal-content').attr('id').replace ( /[^\d.]/g, '' ),10);
      $.ajax({
        type: "POST",
        url: "/comment",
        data: { 
          campaign_id: id,
          comment: comment
        },
        success: function(data) {
          // Remove old comments if present and then show all comments
          var comments = data.comments;
          that.show_comments(comments,id);
        },
        error: function(errMsg) 
        {
          alert("Update failed");
        }
      });
    });

    $('#CommentsModal').on('click','#comment-show-btn',function(e){
      $('#CommentsModal').find('.form-group').find("tr").remove();
      var id = parseInt($(this).parent().attr('id').replace ( /[^\d.]/g, '' ),10);
      $.ajax({
        type: "GET",
        url: "/comment",
        data: { 
          "campaign_id": id
        },
        success: function(data){
          var comments = data.comments;
          if (comments.length != 0) {
            that.show_comments(comments,id);
          }
          else {
            alert("There are no comments for this campaign");
          }
        },
        failure: function(errMsg){
          alert("Get Failed");
        }
      });
    });

  };// start function 

  this.replace_campaign_data = function(campaign)
  {
    var $row = this.get_campaign(campaign);
    $('#row'+campaign.id).replaceWith($row);
  };

  this.get_campaign = function(data) 
  {
    var $row = $('<tr/>').attr('id',"row"+data.id)
    var $title = $('<td/>').html("<a href=/campaign/"+data.id+ ">"+data.title+"</a>").addClass('title').appendTo($row);
    var $who = $('<td/>').html(data.who).appendTo($row);
    var $city= $('<td/>').html(data.city).appendTo($row);
    var $target = $('<td/>').html(data.target).appendTo($row);
    var $start_date = $('<td/>').html(data.start_date).appendTo($row);
    var $end_date = $('<td/>').html(data.end_date).appendTo($row);
    var $span = $('<span/>').addClass('label label-info').html(data.status);
    var $status = $('<td>').append($span).appendTo($row);
    var $featured_span = $('<span/>').addClass('glyphicon');
    if (data.featured) {
      $featured_span.addClass('glyphicon-ok');
    }
    else {
      $featured_span.addClass('glyphicon-remove');
    }

    var $featured = $('<td>').append($featured_span).appendTo($row);

    var arr = [
      {val : '', text: 'Select State'},
      {val : 'Approved', text: 'Approved'},
      {val : 'Rejected', text: 'Rejected'},
      {val : 'Pending Approval', text: 'Pending Approval'},
      {val : 'Closed', text: 'Closed'}
    ];

    var $sel = $('<select/>').addClass('label label-info');
    $(arr).each(function() {
      $sel.append($("<option>").attr('value',this.val).text(this.text));
    });
    $('<td/>').append($sel).appendTo($row);
    $('<td/>').html(data.num_donors).appendTo($row);
    var $butn = $('<button type="button"/>').attr("data-toggle","modal").attr("data-target","#CommentsModal").attr("id",'butn'+data.id).addClass("btn btn-comment");
    $('<td/>').append($butn).appendTo($row);
    return $row;
  };

  this.show_campaigns = function(campaigndata) 
  {
    var $campaigns = $('#campaigns');
    var $tbody = $('<tbody/>')
    for (i = 0; i < campaigndata.length; i++) 
    {
      var $row=this.get_campaign(campaigndata[i])
      $row.appendTo($tbody);
    }
    $tbody.appendTo($campaigns);
    $('#campaigns').tablesorter({
      headers: {
        6: {
          sorter: false
        },
        7: {
          sorter: false
        },
        9: {
          sorter: false
        }
      },
      cssAsc: "arrUp",
      cssDesc: "arrDown"
    });
  };
  this.show_comments = function(comments,id)
  {
    var $modal_comments_section = $('#CommentsModal').find('.comments');
    $modal_comments_section.html('');
    /* Load comments*/
    for (i=0; i<comments.length;i++) {
      var $comment_header = $('<div/>').addClass('comment-header').appendTo($modal_comments_section);
      var $user = $('<div/>').addClass('user').appendTo($comment_header);
      var $user_icon = $('<i/>').addClass('icon-user').appendTo($user);
      $user.append(comments[i].by);
      var $datetime = $('<div/>').addClass('datetime').appendTo($comment_header);
      var $time_icon = $('<i/>').addClass('icon-time').appendTo($datetime);
      $datetime.append(comments[i].date);
      var $comment_content = $('<div/>').addClass('comment-content').appendTo($modal_comments_section);
      var $comment = $('<p/>').text(comments[i].comment).appendTo($comment_content);
    }
  };
};

