$(function(){ 
      $("#content").load("email.html"); //initially loads email
	$('#email-link').addClass("active");
	$('#loyalty-link').addClass("active");
    });



$(document).ready(function(){

		//on nav clikc, lods corresponding page

	     $('.nav-link.loyalty-link').click( function() {
		var href = $(this).attr('href');
		$('.nav-link.loyalty-link').removeClass("active");
		$(this).addClass("active");
		$('#content').load( href, function() {});
		return false;

	     });

	     $('.list-group-item.list-group-item-action').click( function() {
		$('.list-group-item.list-group-item-action').removeClass("active");
		$(this).addClass("active");
		});



});

//landingPage JS 

$(document).on("change","#background_image_file",function(){
		readURLForBackground(this);
		});

$(document).on("click","#add_adverts",function(){
		add_adverts();
		});

$(document).on("click",".close",function(){
		close_row(this);
		});




function add_adverts()
{
 var text="<div class='form-group row adverts'><label class='col-2 col-form-label'>Ad image</label><div class='col-4.5'> <label for='file-upload' class='custom-file-upload'> Upload Image</label><input id='file-upload' type='file' style='display:none;'/></div> <label class='col-1 col-form-label'>URL</label><div class='col-5'>	 <input class='form-control' type='url'> </div> <div class='col-0.5'><button type='button' class='close' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div></div>";

  $('.adverts').last().after(text); 

}



function close_row(e)
{

    e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
}



function readURLForBackground(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
	    $('#background_name').text(input.files[0].name);

        }

        reader.readAsDataURL(input.files[0]);
    }
}




