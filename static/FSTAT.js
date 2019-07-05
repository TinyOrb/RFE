tc_head = ""
start_time = ""
url = ""
feat = ""
suite = ""
tc = ""

$(document).ready(function(){
	console.log("loaded")
	tc_head = $("#testcase").html();
	start_time = $(".stat_list")[0].innerHTML;
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
    $(".stat_list").click(function(){
		start_time = this.innerHTML;
		load_run_stat(start_time)
	});

    load_run_stat(start_time)

    setInterval(function(){
        if(start_time != "")
            load_run_stat(start_time)
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

	var ajx = $.ajax({
	url:"/RFELOADSTATUS",
    method:"POST",
	data:data
	});

	ajx.done(function(msg){
	});

	ajx.fail(function(jqXHR, textStatus){
		console.log(jqXHR, textStatus);
	});
}