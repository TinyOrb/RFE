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
td = null
lag = null

ts = null
tc = null
ms = null
mc = null

fetch_fail = 0
do_update = 0

$(document).ready(function(){
    $.getScript( "static/ingen.js", function( data, textStatus, jqxhr ) {
//        console.log( data ); // Data returned
//        console.log( textStatus ); // Success
//        console.log( jqxhr.status ); // 200
        data = {}
        data["action"] = "check"
        check_up(data)
        console.log( "Load was performed." );
    });

    $("#logout").click(function(){
        data = {}
        data["action"] = "check_out"
        check_up(data)
    });

	console.log("loaded")

    get_time()
    run_sync()



    setInterval(function(){
            run_sync()
        }, 5000);
});

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

function run_sync(){
    client_gather()
    sync()
}

function sync(){
    console.log(ts, tc, ms, mc)
    if(ts == null){
            console.log("updating client");
            fetch_content();
            do_update = 1
     } else{
        if(tc == null || tc == ts){
            fetch_content();
            if(ms == mc){
            // Do nothing
            }
            else{
                if(ts >= tc){
                    do_update = 1
                    }
                    else{
                        do_update = 0
                        update_content();
                    }
            }
        }
        else{

         if(tc != null && tc != ts){
            fetch_content();
            if(ts >= tc){
                 do_update = 1
                }
                else{
                    do_update = 0
                    update_content();
                }
         }
        }
    }
}

function client_gather(){
  console.log("getting client state change");
  var valu = $("#editor").val();
  if(mc != valu){
      tc = new Date().getTime();
      console.log(tc)
      mc = valu;
  }else{
    // Do nothing
  }
}

async function fetch_sync_content(){
  fetch_content();
  while(_ts == null && fetch_fail == 0){
    console.log(_ts, fetch_fail)
    var y = await 20;
   /*if(_ts != null || fetch_fail == 1){
    break;
   }*/
  }
  fetch_fail = 0
  var tx = _ts
  var mx = _ms
  _ts = null
  _ms = null
  return {tx, mx};
}

function nobody(){
}

async function update_sync_content(){
    update_content();
    while(update_content == 0){
    var y = await 20;
    /*
     if(update_content != 0)
      break;
      */
    }
    temp = update_content
    update_content = 0
    return temp;
}

function fetch_content(){
    var data = {};
    data["feature"] = window.location.href.split("?")[1].split('&')[0].split("=")[1];
    data["suite"] = window.location.href.split("?")[1].split('&')[1].split("=")[1];
    data["action"] = "read";

    $.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            		// Only send the token to relative URLs i.e. locally.
            		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
   		 }
	});
    var ajx = $.ajax({
				url:"/RFEEDITOR",
				method:"POST",
				data:data
				});
		ajx.done(function(msg){
                if(msg != "fail")
                {
                    f_data = JSON.parse(msg);
                    _ts = parseFloat(f_data.mtime) - lag
                    _ms = f_data.data
                    ts = _ts;
                    ms = _ms;
                    if(do_update == 1){
                        tc = _ts;
                        mc = _ms;
                        $("#editor").val(_ms);
                        console.log("read success");
                    }
                    {
                        ts = _ts;
                        ms = _ms;
                    }
                    do_update = 0;
                    setTimeout(function() { clr_msg(); }, 3000);
                 }
                else{
                    fetch_fail = 1
                    console.log("Unable to fetch time failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
				per_msg("unable to connect");
			});
}

function update_content(){
    var data = {};
    data["feature"] = window.location.href.split("?")[1].split('&')[0].split("=")[1]
    data["suite"] = window.location.href.split("?")[1].split('&')[1].split("=")[1]
    data["action"] = "write"
    data["content"] = mc

    $.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            		// Only send the token to relative URLs i.e. locally.
            		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
   		 }
	});

        var ajx = $.ajax({
                    url:"/RFEEDITOR",
                    method:"POST",
                    data:data
                 });
            ajx.done(function(msg){
                    console.log(msg);
                    if(msg == "success"){
                            ts = tc
                            ms = mc
                       prompt_msg("Saved successfully");
                       setTimeout(function() { clr_msg(); }, 3000);

                       //console.log("write succeed");
                       update_fail = 2
                   }
                   else{
                   update_fail = 1
                   }
                });
            ajx.fail(function(jqXHR, textStatus){
                    update_fail = 1
                    console.log(jqXHR, textStatus);
                    if(jqXHR["status"] == 403){
                        per_msg("Session expire");
                    }else{
                        per_msg("unable to connect");
                    }
                });
}

function get_time(){
    $.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            		// Only send the token to relative URLs i.e. locally.
            		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
   		 }
	});
    var ajx = $.ajax({
				url:"/GETSERVERNOW",
				method:"POST"
				});
		ajx.done(function(msg){
                if(msg != "fail")
                {
                    server_time = parseFloat(msg);
                    client_time = new Date().getTime();
                    lag = server_time - client_time;
                }
                else{
                    console.log("Unable to fetch time failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			});
}

