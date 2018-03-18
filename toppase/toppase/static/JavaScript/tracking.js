$(function(){

  $('#tracking-link').addClass("active");

  $('#datepicker').datepicker();


});

// **************************************** COOKIES *********************************************************
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
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});


// **********************************************************************************************************
// **************************************** show table containing CSV  content ******************************

$(document).ready(function () {

  var table = $('#csvtable').DataTable({
    columns: [{
      "title": "Client_Mail",
      "data": "Client_Mail"
    }, {
      "title": "Client_First_Name",
      "data": "Client_First_Name"
    }, {
      "title": "Client_Last_Name",
      "data": "Client_Last_Name"
    }, {
      "title": "Tracking_ID",
      "data": "Tracking_ID"
    }, {
      "title": "Courier",
      "data": "Courier"
    }, {
      "title": "Source",
      "data": "Source"
    }, {
      "title": "Destination",
      "data": "Destination"
    }]
  });

  $("#fileinput").on("change", function (evt) {
    var f = evt.target.files[0];
    if (f) {
      var r = new FileReader();
      r.onload = function (e) {
        table.rows.add($.csv.toObjects(e.target.result)).draw();
      }
      r.readAsText(f);
    } else {
      alert("Failed to load file");
    }
  });


});


//***********************************************************************************************************

// ************************************* ADD PICKUP *********************************************************

function FormAddPickupSubmit(){

  $("#FormAddPickupSubmitButton").click();

}
$('#PickupForm').on('submit', function (event) {
  event.preventDefault();
  console.log("PickupForm sanity check!")  // sanity check
  add_pickup();
});

function add_pickup() {
  console.log(" add pickup function is working!"); // sanity check
  var form = document.forms.namedItem("PickupFormName");
  var formData = $(form).serializeArray();
  var store = window.location.pathname.split("/")[3]
  formData.push({name: "store", value: store});
  formData.push({name: "status", value: "IT"});
  formData.push({name: "date_estimation", value: "2000-08-08"});
  console.log(formData);
  var url_action = "/tracking/api/store/".concat(store,"/orders/")


  $.ajax({
    url: url_action,
    type: "POST",
    data: formData,

    success: function (json) {
      console.log(json);
      console.log("success");
      $("#CloseAddPickupModal").click();
      $(".alert_zone").html("<div class=\"alert alert-success alert-dismissable\"><a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a> <strong>Upload succeeded!</strong> </div>");

    },
    error: function (xhr, errmsg, err) {
      console.log(formData)
      console.log("Oops! We have encountered an error: " + errmsg);
      console.log(xhr.status + ": " + xhr.responseText);

      console.log(xhr.responseText.split("\""));


      var client_mail_error = xhr.responseText.split("\"")[3];

      var Tracking_id_error = xhr.responseText.split("\"")[7];
      console.log("***************");
      console.log(errmsg);
      console.log(err);

      $("#add_pickup_error").html("<div class=\"alert alert-danger\"><stong>Oops!</strong> We have encountered an error</div>");
      $("#client_mail_error").html("<div class=\"alert alert-danger\">" + client_mail_error + "</div>");
      $("#Tracking_id_error").html("<div class=\"alert alert-danger\">" + Tracking_id_error + "</div>");
    }
  });
}
;


// **********************************************************************************************************
// *********************************************** UPLOAD CSV **********************************************
function FormUploadCSVSubmit(){

  $("#FormUploadCSVSubmitButton").click();

}

$('#UploadCSVFormID').on('submit', function (event) {
  event.preventDefault();
  console.log("UploadCSVForm sanity check!!")  // sanity check
  create_orders_through_order_file();
});


function create_orders_through_order_file() {

  var form = document.forms.namedItem("UploadCSVFormName");
  var formData = new FormData(form);
  console.log(formData);
  console.log("function create_orders_through_order_file is working!"); // sanity check
  $.ajax({
    url: "/tracking/api/order-csv/",
    type: "POST",
    data: formData,
    processData: false, // Don't process the files
    contentType: false, // Set content type to false as jQuery will tell the server its a query string request
    cache: false,
    // handle a successful response
    success: function (json) {
      console.log(json);
      console.log("success");
      $("#CloseUploadCSVModal").click();
      $(".alert_zone").html("<div class=\"alert alert-success alert-dismissable\"><a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a> <strong>Upload succeeded!</strong> </div>");
    },
    //
    error: function (xhr, errmsg, err) {
      //
      console.log(formData)
      console.log("not working");
      console.log("Oops! We have encountered an error: " + errmsg);
      console.log(xhr.status + ": " + xhr.responseText);
      $("#upload_csv_error").html("<div class=\"alert alert-danger\"><stong>Oops!</strong> We have encountered an error</div>");
      $("#csv_file_error").html("<div class=\"alert alert-danger\">" + xhr.responseText.split("\"")[3] + "</div>");
    }
  });
}
;







// **********************************************************************************************************


// ******************************** Display Orders ********************************************************

function DispalyOrders() {

  var store = window.location.pathname.split("/")[3]

  $.ajax({
      type: 'GET',
      url: "/tracking/api/store/".concat(store, "/orders/"),
      dataType: "json",
      success: function (data) {
        console.log("function DisplayOrders is working !"); // sanity check
        console.log(data)
        var existing_orders_cells = $('.order_id').toArray();
        var existing_id = []
        for (i = 0; i < existing_orders_cells.length; i++) {
          existing_id.push($(existing_orders_cells[i]).text())

        }

        for (i = 0; i < data.length; i++) {
          if ($.inArray(data[i]['id'].toString(), existing_id) == -1) {
            var order_id = data[i]['id'].toString();
            var action_url_detail = "/".concat("tracking/store/", store, "/order/", order_id, "/")
            console.log(" *************************** ACTION URL DETAIL *******************")
            console.log(action_url_detail)
            console.log(" ***************************")

            var row_number = "row_".concat(data[i]['id'].toString())
            var order_to_mark_as_delivered_id = "order_number_".concat(data[i]['id'].toString())
            var order_to_check_status_id = "order_status_".concat(data[i]['id'].toString())
            var order_id_cell = "<td class=\"order_id\">".concat(data[i]['id'].toString(), "</td>")
            var tracking_id_cell ="<td class = \"tracking _id\">".concat(data[i]['tracking_id'].toString(),"</td>")
            var client_mail_cell = "<td class=\"client_mail\">".concat(data[i]['client']['email'].toString(), "</td>")
            var courier_cell = "<td class = \"courier\">".concat(data[i]['courier'].toString(), "</td>")
            var recieved_status = data[i]['status'].toString()
            if (recieved_status == "IT") {
              var status_to_display ="<span class =\"badge badge-pill badge-info OrderStatus\" id='".concat(order_to_check_status_id,"'>In transit</span>")
            } else if (recieved_status =="Delivered") {
              var status_to_display ="<span class =\"badge badge-pill badge-success OrderStatus \" id='".concat(order_to_check_status_id,"'>Delivered</span>")
            }else if (recieved_status =="Ready to go") {
              var status_to_display = "<span class =\"badge badge-pill badge-default OrderStatus\" id='".concat(order_to_check_status_id,"'>Ready to go</span>")
            }
            else if (recieved_status =="Out for delivery") {
              var status_to_display ="<span class =\"badge badge-pill badge-warning OrderStatus\" id='".concat(order_to_check_status_id,"'>Out for delivery</span>")
            }
            else if (recieved_status =="Failed attempt") {
              var status_to_display ="<span class = \"badge badge-pill badge-danger OrderStatus\" id='".concat(order_to_check_status_id,"'>Failed attempt</span>")
            }

            else {
              var status_to_display ="<span class = \"badge badge-pill OrderStatus \" id='".concat(order_to_check_status_id,"'>",recieved_status,"</span>")
            }


            var status_cell=   "<td>".concat( status_to_display,"</td>")
            // var destination_cell = "<td class=\"destination\">".concat(data[i]['destination'].toString(), "</td>")
            var destination_cell = "<td class=\"destination\">".concat("destination", "</td>")
            // var date_estimation_cell ="<td class = \"date\">".concat(data[i]['date_estimation'].toString(), "</td>")
            var date_estimation_cell ="<td class = \"date\">".concat("date_estimation", "</td>")
            // var reason_cell= "<td class = \"reason\">".concat(data[i]['reason'].toString(), "</td>")
            var reason_cell= "<td class = \"reason\">".concat("reason", "</td>")
            // var comment_cell="<td class = \"note\">".concat(data[i]['note'].toString(), "</td>")
            var comment_cell="<td class = \"note\">".concat("note", "</td>")
            var action_cell ="<td class=\"action\"><div class='btn-group'><button type='button' class='btn btn-secondary active dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Action</button><div class='dropdown-menu'>".concat("<a class='dropdown-item' href='",action_url_detail,"'>Edit</a>","<a class='dropdown-item' href='#' onclick='delete_order_function()' id='", data[i]['id'].toString(),"'>Delete</a><a class='dropdown-item' href='#' onclick='mark_as_delivered_function()' id='",order_to_mark_as_delivered_id,"'>Mark as delivered</a>","<a class='dropdown-item' href='#'>Retrack</a></div></div></td>")
            $("#table_tracking_body").append("<tr id= '".concat(row_number,"'>",order_id_cell,tracking_id_cell, client_mail_cell, courier_cell, status_cell, destination_cell, date_estimation_cell, reason_cell,comment_cell,action_cell,"</tr>"));
            //
            //
          }
          //
        }
        //

      },

      error: function () {
        console.log("Display Orders is not working");
      }
    }
  );


}
setInterval(DispalyOrders, 2000);



// **********************************************************************************************************


// *********************************************** Delete Order ********************************************

function delete_order_function() {

  var result = confirm("Want to delete?");
  if (result) {


    var x = document.activeElement.id;
    var store = window.location.pathname.split("/")[3]

    console.log("************************    X  **************************")
    console.log(x)
    console.log("*********************************************************")
    console.log("/tracking/api/store/".concat(store, "/order/",x.toString(),"/"))

    console.log("*********************************************************")


    $.ajax({
        type: 'DELETE',
        url: "/tracking/api/store/".concat(store, "/order/",x.toString(),"/"),

        success: function (data) {
          console.log("delete Order is working");
          console.log("***************** ID ELEMENT TO DELETE *************************");
          console.log(x);
          console.log("***************** ROW PARENT *************************");
          var row_to_delete_id = $('#' + x.toString()).closest('tr').attr('id');
          console.log(row_to_delete_id);
          console.log("***************** ROW PARENT *************************");
          $('#' + row_to_delete_id).remove();


        },

        error: function (error) {
          console.log("delete package is not working");
          console.log(error)

        }
      }
    );

  }


}



// **********************************************************************************************************
// ********************************************  Mark as Delivered ******************************************


function mark_as_delivered_function() {



  var result = confirm("Want to mark as delivered ?");
  if (result) {

    var store = window.location.pathname.split("/")[3]

    var form = document.forms.namedItem("mark_delivered");
    var formData = $(form).serializeArray();
    var x = document.activeElement.id;
    console.log(x.toString().split("_")[2])
    action_url = "/tracking/api/store/".concat(store, "/order/", x.toString().split("_")[2], "/");

    console.log(action_url);

    formData.push({name: "status", value: "Delivered manuel"});
    formData.push({name: "accept_test_flag", value: false});
    // formData.push({name: "store", value: "1"});


    // TODO : use jquery DataForm Object

    /* ********************* using formData object *************************

     var formData = new FormData();


     formData.append('accept_test_flag', 'False');
     formData.append('status', 'Delivered');
     formData.append("date_estimation","2017-02-02T23:00");
     formData.append("shipper","Fedex");
     formData.append("client_mail","test@gmail.com");
     formData.append("destination","dest");
     formData.append("store","1");
     formData.append("source","sou");


     for (var pair of formData.entries()) {
     console.log(pair[0] + ', ' + pair[1]);
     };

     var data_to_send = $(formData).serialize();

     ***************************************************** */

    $.ajax({
        type: "PATCH",
        url: action_url,
        data: formData,

        success: function (data) {
          console.log("Mark as delivered is working");
        },

        error: function (error) {
          console.log("Mark as delivered is not working!");
          console.log(error);


        }
      }
    );


  }
}




// **********************************************************************************************************
// ***************************************** Get Order's status *********************************************



//TODO : Gives correct resultes but it's not optimised


function GetOrdersStatus() {

  var store = window.location.pathname.split("/")[3]

  $.ajax({
    type: 'GET',
    url: "/tracking/api/store/".concat(store, "/orders/"),
    dataType: "json",
    success: function (data) {

      console.log("GetOrdersStatus is working!");
      var orders_status = $('.OrderStatus').toArray();
      console.log(orders_status)
      for (i = 0; i < data.length; i++) {

        var test_id = "order_status_".concat(data[i]["id"].toString());


        for (j = 0; j < orders_status.length; j++) {

          if (test_id == orders_status[j].id) {

            $(orders_status[j]).text(data[i]["status"]);

            if (data[i]["status"] == "In transit") {

              $(orders_status[j]).attr('class', 'badge badge-pill badge-info OrderStatus');
            } else if (data[i]["status"] =="Delivered") {
              $(orders_status[j]).attr('class', 'badge badge-pill badge-success OrderStatus');
             }else if (data[i]["status"] =="Ready to go") {
              $(orders_status[j]).attr('class', 'badge badge-pill badge-default OrderStatus');
             }
            else if (data[i]["status"] =="Out for delivery") {
              $(orders_status[j]).attr('class', 'badge badge-pill badge-warning OrderStatus');
             }
            else if (data[i]["status"] =="Failed attempt") {
              $(orders_status[j]).attr('class', 'badge badge-pill badge-danger OrderStatus');
              }
            else {
              $(orders_status[j]).attr('class', 'badge badge-pill OrderStatus');
            }



            break;

          }

        }
      }

      console.log("GetOrdersStatus has finished! ")

    },

    error: function () {
      console.log("GetOrdersStatus is not working! ");
    }
  });


}
setInterval(GetOrdersStatus, 3000);





// **********************************************************************************************************

