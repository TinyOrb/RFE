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

tc_head = ""
start_time = ""
url = ""
feat = ""
suite = ""
tc = ""
isOnDiv=false
old_msg = null

$(document).ready(function(){
   tc_head = $("#testcase").html();
   try{
   start_time = $(".stat_list")[0].innerHTML;
   }catch(err){
	   console.log(err);
   }
    url = window.location.href
    feat = url.split("RFERUNSTATUS")[1].replace("/?", "").split("&")[0].split("=")[1]
    try{
        suite = url.split("RFERUNSTATUS")[1].replace("/?", "").split("&")[1].split("=")[1]
    }
    catch(e){
        suite = null;
    }
    try {
         tc = url.split("RFERUNSTATUS")[1].replace("/?", "").split("&")[2].split("=")[1]
      }
      catch ( e ) {
         tc = null;
      }
     //console.log(start_time, feat, suite, tc)
    $(".stat_list").click(function(){
		start_time = this.innerHTML;
		load_run_stat(feat, suite, tc, start_time)
	});

    load_run_stat(feat, suite, tc, start_time)

    setInterval(function(){
        if(start_time != "")
            load_run_stat(feat, suite, tc, start_time)
        }, 5000);

    $("#testcase").mouseenter(function(){isOnDiv=true;});
    $("#testcase").mouseleave(function(){isOnDiv=false;});

    $("#suite").css({"margin":"0 1% 0 1%", "width":"15%", "padding":"1%", "background":"#E3E3E3", "height":"86%", "float":"left", "overflow":"auto"});
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


function load_run_stat(feature, suite, tc, start_time){
    $.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            		// Only send the token to relative URLs i.e. locally.
            		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
   		 }
	});

	if(suite == null)
	{
	    data = {feature: feature, time: start_time}
	}else{
	 if(tc == null){
	    data = {feature:feature, suite:suite, time: start_time}
	 }
	 else{
	    data = {feature:feature, suite:suite, tc:tc, time: start_time}
	 }
	}
	//console.log(data)

	var ajx = $.ajax({
	url:"/RFELOADSTATUS",
    method:"POST",
	data:data
	});

	ajx.done(function(msg){
	 if(msg != "")
	 {
	    if(old_msg != msg){
            $("#testcase").html(tc_head + msg);
            if(isOnDiv==false)
            $("#testcase").scrollTop($("#testcase")[0].scrollHeight-10);
            old_msg = msg
	    }
	 }
	 else{
	    console.log("No log")
	 }
	});

	ajx.fail(function(jqXHR, textStatus){
		console.log(jqXHR, textStatus);
	});
}
