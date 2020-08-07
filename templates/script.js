$("#submit").click(function () {
  var ticket_id = $("#ticket_id").val();
  var add_to_ticket=true;
  var url="https://enter_your_flask_endpoint_url_here"
  if($("#add_to_ticket").is(":checked")){
    add_to_ticket=true;
  }
  else{
    add_to_ticket=false;
  }
  if (ticket_id != "") {
    var check_url=url+"check_ticket?"+"ticket_id="+ticket_id
    $.post(check_url, function( data ) {
      if(data["url_status"]=="valid"){
        $.ajax({
          url: url+"calendly?"+"add_to_ticket="+add_to_ticket+"&ticket_id="+ticket_id,
          success: function (result) {
            url = result["url"];
            $("#url_div").html("<h5 id='url'>One Time URL is <a href=" + url + ">" + url + "</a></h5>")
          }
        });
      }
      else{
        $("#url_div").html("<h5 id='url'>Ticket ID is invalid. Please enter a valid Ticket ID</a></h5>")
      }
    });
  }
  else{
    $("#url_div").html("<h5 id='url'>Kindly enter the Ticket ID</a></h5>")
  }
  $("#url_div").show();
  return false;
});