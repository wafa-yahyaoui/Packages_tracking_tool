$(function () {
  $("#content").load("store.html"); //initially loads email
  $('#user-link').addClass("active");
});


$(document).ready(function () {

  //on nav click, lods corresponding page

  $('.nav-link.store-link').click(function () {
    var href = $(this).attr('href');
    $('.nav-link.store-link').removeClass("active");
    $(this).addClass("active");
    $('#content').load(href, function () {
    });
    return false;

  });

});


//store JS
$(document).on("change", "#file_logo", function () {
  readURLForLogo(this);
});

$(document).on("click", "#add_web_links", function () {
  add_web_links();
});

$(document).on("click", "#add_social_links", function () {
  add_social_links();
});

$(document).on("click", ".close", function () {
  close_row(this);
});


function readURLForLogo(input) {

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $('#logo').attr('src', e.target.result);
      $('#logo_name').text(input.files[0].name);

    }

    reader.readAsDataURL(input.files[0]);
  }
}


function add_web_links() {
  var text = "<div class='form-group row web'><label class='col-1 col-form-label'>Text</label><div class='col-2'><input class='form-control' type='text' name='links.1.text'></div> <label class='col-1 col-form-label'>URL</label>  <div class='col-4'><input class='form-control' type='url' name='links.1.url'> </div>	<div class='col-1'>	<button type='button' class='close' aria-label='Close'>	  <span aria-hidden='true'>&times;</span></button></div></div>";

  $('.web').last().after(text);

}


function add_social_links() {
  var text2 = "<div class='form-group row social'><div class='col-2'><select class='form-control'><option selected>Twitter</option><option value='1'>Facebook</option>  <option value='2'>LinkenIn</option></select></div>	  <label class='col-1 col-form-label'>Text</label> <div class='col-2'><input class='form-control' type='text'>  </div> <label for='example-password-input' class='col-1 col-form-label'>URL</label><div class='col-4'>   <input class='form-control' type='url'> </div><div class='col-1'><button type='button' class='close' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div>";

  $('.social').last().after(text2);
}


function close_row(e) {

  e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
}


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
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

// *******************************************************************************************************


// *************************** Load Instance Values *******************************************************


$(document).ready(function () {
  console.log("Document Ready!");
  var current_location = window.location.pathname.split("/");
  var action_url = "/".concat("tracking/api/store/", current_location[3], "/");
  console.log(action_url);

  $.ajax({
    type: 'GET',
    url: action_url,
    dataType: "json",
    success: function (data) {
      console.log("Get instance values is working");
      console.log(data);
      document.getElementById("logo").src = data["logo"];
      document.getElementById("color_menu").value = data["color_menu"];
      document.getElementById("color_text").value = data["color_text"];
      data['links'].forEach(function (link) {
        var web_link_text_id = "web_link_text_".concat(link["id"].toString());
        var web_link_url_id = "web_link_url_".concat(link["id"].toString());
        var text = "<div class='form-group row web'><label class='col-1 col-form-label'>Text</label><div class='col-2'><input class='form-control' type='text' name='links.1.text' id='".concat(web_link_text_id, "'></div> <label class='col-1 col-form-label'>URL</label>  <div class='col-4'><input class='form-control' type='url' name='links.1.url' id ='", web_link_url_id, "'> </div>	<div class='col-1'>	<button type='button' class='close' aria-label='Close'>	  <span aria-hidden='true'>&times;</span></button></div></div>");

        $('.web').last().after(text);
        document.getElementById(web_link_text_id).value = link["text"];
        document.getElementById(web_link_url_id).value = link["url"];

      });

      // change colors of color picker
      // TODO : fix the color picker when changing instances
        $('#cp2').colorpicker();
        $('#cp3').colorpicker();

      //font select menu
      $("#font option").each(function () {

        console.log($(this).val());
        if ($(this).val() == data["font"]) {
          $(this).attr("selected", "selected");
        }
        ;
      });
    },

    error: function () {
      console.log("Get instance values is not working ! ");
    }
  });


});
//********************************************************************************************************


//******************************************** Change store design **************************************

$('#StoreDesignFormID').on('submit', function (event) {
  event.preventDefault();
  console.log("StoreDesignForm sanity check!")  // sanity check
  change_store_design();
});

function change_store_design() {
  console.log(" change_store_design function is working!"); // sanity check
  var form = document.forms.namedItem("StoreDesignFormName");
  // var formData = $(form).serializeArray();
  var formData = new FormData(form);
  var store = window.location.pathname.split("/")[3];

  console.log(formData);
  var url_action = "/tracking/api/store/".concat(store,"/");

console.log("************FORM DATA************")
      console.log(formData);
      console.log("************************")
  $.ajax({
    url: url_action,
    type: "PATCH",
    data: formData,
    processData: false, // Don't process the files
    contentType: false, // Set content type to false as jQuery will tell the server its a query string request
    cache: false,

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
