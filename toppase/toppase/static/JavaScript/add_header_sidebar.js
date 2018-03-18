



$(function(){
	function resizeBroadcast() {

    var timesRun = 0;
    var interval = setInterval(function(){
      timesRun += 1;
      if(timesRun === 5){
        clearInterval(interval);
      }
      window.dispatchEvent(new Event('resize'));
    }, 62.5);
  }
    $("#sidebar").addClass("sidebar");
    $('.navbar-toggler').click(function(){

        if ($(this).hasClass('sidebar-toggler')) {
            $('body').toggleClass('sidebar-hidden');
            resizeBroadcast();
        }

        if ($(this).hasClass('aside-menu-toggler')) {
            $('body').toggleClass('aside-menu-hidden');
            resizeBroadcast();
        }

        if ($(this).hasClass('mobile-sidebar-toggler')) {
            $('body').toggleClass('sidebar-mobile-show');
            resizeBroadcast();
        }

    });

    $('.sidebar-close').click(function(){
        $('body').toggleClass('sidebar-opened').parent().toggleClass('sidebar-opened');
    });

});


$(document).ready(function(){

    //needs to be populated dynamically
    var list_notif=["Notification1","Notification2","Notification3","Notification4"];

    var content = '<div>'
    for (i in list_notif)
    {
        content += '<a href="#" class="list-group-item" style="border:None;">'+ list_notif[i]+'</a>';
    }
    content += '</div>';


    $('[data-toggle="popover"]').popover({
        html: true,
        content:content
    });


    var number_notif=list_notif.length;
    $('#notif').text(number_notif);

    $('#notif-link').focus(
        function(){
            $('#notif').remove();
        });

});
