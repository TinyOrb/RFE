td = null
lag = null

ts = null
tc = null
ms = null
mc = null
_ts = null
_ms = null

fetch_fail = 0
update_fail = 0

$(document).ready(function(){
	console.log("loaded")
    get_time()
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

async function sync(){
    if(ts == null){
            var {tx, mx} = fetch_sync_content();
            ts = tx;
            ms = mx;
            tc = tx;
            mc = mx;
            $("#editor").text(mx);
     } else{
        if(tc == null || tc == ts){
            if(ms == mc){
            // Do nothing
            }
            else{
            var {tx, mx} = fetch_sync_content();
                if(tx >= tc){
                     ts = tx
                     tc = tx
                     ms = mx
                     mc = mx
                     $("#editor").text(mx);
                    }
                    else{
                        if(update_sync_content() == 2){
                            ts = tc
                            ms = mc
                        }
                    }
            }
        }
        else{
         if(tc != null && tc != ts){
            var {tx, mx} = fetch_sync_content();
            if(tx >= tc){
                 ts = tx
                 tc = tx
                 ms = mx
                 mc = mx
                 $("#editor").text(mx);
                }
                else{
                    if(update_sync_content() == 2){
                        ts = tc
                        ms = mc
                    }
                }
         }
        }
    }
}

function client_gather(){
  if(mc != $("#editor").text()){
      tc = new Date().getTime();
      mc = $("#editor").text();
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
                 }
                else{
                    fetch_fail = 1
                    console.log("Unable to fetch time failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
		        fail = 1
				console.log(jqXHR, textStatus);
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
                    if(msg == "success"){
                       update_content = 2
                       console.log("write succeed");
                   }
                   else{
                   update_fail = 1
                   }
                });
            ajx.fail(function(jqXHR, textStatus){
                    update_fail = 1
                    console.log(jqXHR, textStatus);
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