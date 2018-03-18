$(function(){
    $("#content").load("user.html"); //initially loads email
    $('#user-link').addClass("active");
});



$(document).ready(function(){

    //on nav click, lods corresponding page

    $('.nav-link.account-link').click( function() {
        var href = $(this).attr('href');
        $('.nav-link.account-link').removeClass("active");
        $(this).addClass("active");
        $('#content').load( href, function() {});
        return false;

    });

});


//store JS
$(document).on("change","#file_logo",function(){
    readURLForLogo(this);
});

$(document).on("click","#add_web_links",function(){
    add_web_links();
});

$(document).on("click","#add_social_links",function(){
    add_social_links();
});

$(document).on("click",".close",function(){
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


function add_web_links()
{
    var text="<div class='form-group row web'><label class='col-1 col-form-label'>Text</label><div class='col-2'><input class='form-control' type='text'></div> <label class='col-1 col-form-label'>URL</label>  <div class='col-4'><input class='form-control' type='url'> </div>	<div class='col-1'>	<button type='button' class='close' aria-label='Close'>	  <span aria-hidden='true'>&times;</span></button></div></div>";

    $('.web').last().after(text);

}





function add_social_links()
{
    var text2="<div class='form-group row social'><div class='col-2'><select class='form-control'><option selected>Twitter</option><option value='1'>Facebook</option>  <option value='2'>LinkenIn</option></select></div>	  <label class='col-1 col-form-label'>Text</label> <div class='col-2'><input class='form-control' type='text'>  </div> <label for='example-password-input' class='col-1 col-form-label'>URL</label><div class='col-4'>   <input class='form-control' type='url'> </div><div class='col-1'><button type='button' class='close' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div>";

    $('.social').last().after(text2);
}




function close_row(e)
{

    e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
}



