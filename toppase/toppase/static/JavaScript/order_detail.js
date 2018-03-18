$(function(){

  $('#tracking-link').addClass("active");
  $(".alert").hide();
});


$(document).ready(function(){


  $('#print_button').click( function() {

    $('#printable_area').print();


  });



  $('#refresh_button').click( function() {

    //to be changed with this template URL
    $('#refresh_area').load('/home/mouna/coreUI/detailShipment.html' +  ' #refresh_area');
    $(".alert").show();

    //Uncomment this line if you want alert to fade after 2s => Alert won"t be printed if user   			clicks print after he clicks refresh

    //$('.alert').delay(2000).fadeOut();

  });


});


//******************************** COOKIES  ********************************************


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

// *******************************************************************************************************


// *************************** Load Instance Values *******************************************************


$( document ).ready(function() {
  console.log("Document Ready!");
  var current_location = window.location.pathname.split("/");
  var action_url = "/".concat("tracking/api/store/",current_location[3], "/order/", current_location[5],"/");
  console.log(action_url)

  $.ajax({
    type: 'GET',
    url: action_url,
    dataType: "json",
    success: function (data) {
      console.log("Get instance values is working");
      console.log(data)
      document.getElementById("order_id").value = data["id"];
      document.getElementById("order_tracking_id").value = data["tracking_id"];
      document.getElementById("order_origin").value = data["origin"];
      document.getElementById("order_destination").value = data["destination"];
      document.getElementById("order_date_created").value = data["date_created"];
      document.getElementById("order_rate").value = data["rate"];
      document.getElementById("order_reason").value = data["reason"];
      document.getElementById("order_note").value = data["note"];
      document.getElementById("order_client_email").value = data["client"]["email"];
      document.getElementById("order_client_first_name").value = data["client"]["first_name"];
      document.getElementById("order_client_last_name").value = data["client"]["last_name"];
      document.getElementById("order_client_phone").value = data["client"]["phone"];
      document.getElementById("order_client_country").value = data["client"]["country"];
      document.getElementById("order_client_city").value = data["client"]["city"];
      document.getElementById("order_client_address_line").value = data["client"]["address_line"];
      document.getElementById("order_client_zip_code").value = data["client"]["zip_code"];
      document.getElementById("order_client_ip_address").value = data["client"]["ip_address"];
      data['products'].forEach(function(product) {
        $("#order_products").append("<option value='".concat(product['sku'],"' selected=''>",product['name'] ,"</option>"))
      });
      $("#order_courier").append("<option value='".concat(data['courier'],"' selected=''>",data['courier'],"</option>"))
    },

    error: function () {
      console.log("Get instance values is not working ! ");
    }
  });



});
//********************************************************************************************************
//******************************************** Change Order Details **************************************

$('#OrderDetailFormID').on('submit', function (event) {
  event.preventDefault();
  console.log("OrderDetailForm sanity check!")  // sanity check
  change_order_detail();
});

function change_order_detail() {
  console.log(" change_order_detail function is working!"); // sanity check
  var form = document.forms.namedItem("OrderDetailFormName");
  var formData = $(form).serializeArray();
  var store = window.location.pathname.split("/")[3]
  var order = window.location.pathname.split("/")[5]

  console.log(formData);
  var url_action = "/tracking/api/store/".concat(store,"/order/",order,"/")

console.log("************************")
      console.log(formData);
      console.log("************************")
  $.ajax({
    url: url_action,
    type: "PATCH",
    data: formData,
    // contentType: 'application/json; charset=UTF-8',

    success: function (json) {
      console.log("************************")
      console.log(json);
      console.log("************************")
      console.log("Update succeeded !");
      // $(".alert_zone").html("<div class=\"alert alert-success alert-dismissable\"><a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a> <strong>Update succeeded!</strong> </div>");

    },
    error: function (xhr, errmsg, err) {
      console.log("************************")
      console.log(formData)
      console.log("************************")
      console.log("Oops! We have encountered an error: " + errmsg);
      console.log(xhr.status + ": " + xhr.responseText);

      console.log(xhr.responseText.split("\""));



      console.log("***************");
      console.log(errmsg);
      console.log(err);
    }
  });
}
;
//********************************************************************************************************





