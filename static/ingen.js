function prompt_msg(msg){
    $("#load_message").html(msg);
    $("#load_message").css({"position":"fixed", "top":"10%", "left":"40%", "display":"block", "z-index":"10", "background": "#cbc3c1", "border-width":"0px", "padding":"15px 25px", "border-radius": "5px", "text-size":"36px"})
    $("#load_message").fadeIn("fast");
    $("#load_message").delay(3000).fadeOut("slow");
}

function check(){
}

function check_up(a,ap){
    $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                 }
        });

        var ajx = $.ajax({
         url:"/MANAGEFEAT",
         method:"POST",
         data:{action:"template"}
         });

        ajx.done(function(msg){
        });

        ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
          });
}

function check_down(){
        $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                 }
        });

        var ajx = $.ajax({
         url:"/MANAGEFEAT",
         method:"POST",
         data:{action:"template"}
         });

        ajx.done(function(msg){
        });

        ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
          });
}