/***************************************************************************
Copyright 2019, TinyOrb.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Shad Hasan, Tinyorb.Org
***************************************************************************/
function prompt_msg(msg){
    $("#load_message").html(msg);
    $("#load_message").css({"position":"fixed", "top":"10%", "left":"40%", "display":"block", "z-index":"10", "background": "#cbc3c1", "border-width":"0px", "padding":"15px 25px", "border-radius": "5px", "text-size":"36px"})
    //Below are not supported in chrome and chrome is literally turning into shit for developer
    //$("#load_message").fadeIn("fast");
    //$("#load_message").delay(3000).fadeOut("slow");
}

function per_msg(msg){
    $("#load_message").html(msg);
    $("#load_message").css({"position":"fixed", "top":"10%", "left":"40%", "display":"block", "z-index":"10", "background": "#cbc3c1", "border-width":"0px", "padding":"15px 25px", "border-radius": "5px", "text-size":"36px"})
}

function clr_msg(){
    $("#load_message").css({"display":"none"})
}

function load_form(msg){
    $("#load_message").html(msg);
    $("#load_message").css({"position":"fixed", "top":"25%", "left":"40%", "display":"block", "z-index":"10", "background": "#cbc3c1", "border-width":"0px", "padding":"15px 25px", "border-radius": "5px", "text-size":"36px"});
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function check_up(ac){
    $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                 }
        });

        var ajx = $.ajax({
         url:"/",
         method:"POST",
         data:ac
         });

        ajx.done(function(msg){
            switch(ac["action"]){
                case "check_in":
                    if( msg == "Authenticated"){
                        window.location = "/RFE"
                    }
                    else{
                        $("#err_msg_2").html("<span style='color:red;'> Incorrect username and password! </span>")
                    }
                break;
                case "check_out":
                    if( msg == "Logout"){
                        window.location = "/"
                    }
                    else{
                    }
                break;
                case "check":
                    if( msg == "Authorized"){
                        console.log(window.location)
                    }
                    else{
                    }
                break;
                default:
                 console.log("unknown action")
                break
            }
        });

        ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
            if(jqXHR["status"] == 401){
            if(ac["action"] == "check_in")
            $("#err_msg_2").html("<span style='color:red;'> *Incorrect username and password </span>")
            }
          });
}
