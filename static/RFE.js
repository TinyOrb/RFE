tc_head = ""
current_feature = ""
$(document).ready(function(){
	console.log("loaded")
	tc_head = $("#testcase").html()
	current_feature = $(".suite_list")[0].innerHTML

        $(".suite_list").click(function(){
		current_feature = this.innerHTML;
		get_suite_tree(current_feature)
	});

    get_suite_tree(current_feature)

    setInterval(function(){
        if(current_feature != "")
            get_suite_tree(current_feature)
        }, 5000);
})


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


function get_suite_tree(feature_name){
	//console.log(feature_name)

	$.ajaxSetup({
    		beforeSend: function(xhr, settings) {
        		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            		// Only send the token to relative URLs i.e. locally.
            		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
   		 }		
	});

	var ajx = $.ajax({
				url:"/RFETS",
				method:"POST",
				data:{feature:feature_name}
				});
			ajx.done(function(msg){
				if(msg != "" && msg.toLowerCase() != "none"){
					var data = JSON.parse(msg);
					//console.log(data);
					//console.log(msg);
					htmlTable = "";
					for(i = 0; i < data.suites.length; i++){
						htmlTable += "<table style=\"width:100%;margin:auto;background:#2F4F4F;color:white;\"><tr>"
						htmlTable += "<td style=\"width:70%;\"><h3>" + he.escape(data.suites[i].name.toUpperCase()) + "</h3></td>"
						htmlTable += "<td><h5 class=runnable feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">"+data.suites[i].status+"</h5></td>"
						if(data.suites[i].status == "Running")
						    htmlTable += "<td><h5 class=abort_handle feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">Abort</h5></td>"
						htmlTable += "<td><h5 class=stat_viewer feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">"+"View"+"</h5></td>"
						htmlTable += "</tr></table>" ;
						for(j = 0; j < data.suites[i].tcs.length; j++){
							htmlTable += "<table style=\"width:100%;margin:auto;background:lightgrey;\"><tr>"
							htmlTable += "<td style=\"width:70%;\"><h4>" + he.escape(data.suites[i].tcs[j].name) + "</h4></td>"
							htmlTable += "<td><h6 class=runnable2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" tc=\""+he.escape(data.suites[i].tcs[j].name) +"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].tcs[j].status != "Running"? "" : "color:#67032F;" )+ "\">"+data.suites[i].tcs[j].status+"</h6></td>"
							if(data.suites[i].tcs[j].status == "Running")
							    htmlTable += "<td><h6 class=abort_handle2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" tc=\""+he.escape(data.suites[i].tcs[j].name) +"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].tcs[j].status != "Running"? "" : "color:#67032F;" )+ "\">Abort</h6></td>"
							htmlTable += "<td><h6 class=stat_viewer2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" tc=\""+he.escape(data.suites[i].tcs[j].name) +"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].tcs[j].status != "Running"? "" : "color:#67032F;" )+ "\">"+"View"+"</h6></td>"
							htmlTable += "</tr></table>";
						}
					}
					$("#testcase").html(tc_head + htmlTable);
                    $("#testcase").css({"overflow":"auto"});

                    $(".runnable").hover(function(){
                    $(this).css({"color":"lightgrey"});
                    }, function(){
                    if(this.innerHTML == "Run")
                        $(this).css({"color":"white"})
                    else
                        $(this).css({"color":"#E39FF6"})
                    });

                    $(".runnable2").hover(function(){
                    $(this).css({"color":"darkgrey"});
                    }, function(){
                    if(this.innerHTML == "Run")
                        $(this).css({"color":"#090909"})
                    else
                        $(this).css({"color":"#67032F"})
                    });

                    $(".runnable").click(function(){
                        console.log(this.innerHTML);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        if(this.innerHTML.toLowerCase() != "running"){
                        invoke("run", this.getAttribute("feat"), this.getAttribute("suite"), null);
                        }
                    });

                    $(".runnable2").click(function(){
                        console.log(this);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        console.log(this.getAttribute("tc"));
                        if(this.innerHTML.toLowerCase() != "running"){
                        invoke("run", this.getAttribute("feat"), this.getAttribute("suite"), this.getAttribute("tc"));
                        }
                    });

                    $(".abort_handle").click(function(){
                        console.log(this.innerHTML);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        invoke("abort", this.getAttribute("feat"), this.getAttribute("suite"), null);
                    });

                    $(".abort_handle2").click(function(){
                        console.log(this);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        console.log(this.getAttribute("tc"));
                        invoke("abort", this.getAttribute("feat"), this.getAttribute("suite"), this.getAttribute("tc"));
                    });

                    $(".stat_viewer").click(function(){
                        console.log(this.innerHTML);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        window.open("/RFERUNSTATUS?feat="+this.getAttribute("feat")+"&suite="+this.getAttribute("suite"));
                    });

                    $(".stat_viewer2").click(function(){
                        console.log(this);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        console.log(this.getAttribute("tc"));
                        window.open("/RFERUNSTATUS?feat="+this.getAttribute("feat")+"&suite="+this.getAttribute("suite")+"&tc="+this.getAttribute("tc"));
                    });
				}
				else{
					$("#errormsg2").text("No data received");
				}
			});

			ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			});
}

function f1(){
	name = $("#x1").val()
	if(name != "")
	{	
		if(name.length <2)
		{
			$("#div1").html("Hello, "+ name +". One letter name is very rare!")	
		}
		else
		{
			$("#div1").html("<h2>Hello, "+name+"</h2>")	
		}
	}
	else{
		$("#div1").html("Oops, you forget to mention names.")	
	}
}

function invoke(action, feature, suite, tc){
    if(feature != null && suite != null && tc != null)
    {
    data = {feature:feature, suite:suite, tc:tc}
    }
    else{
        if(feature != null && suite != null)
        {
            data = {feature:feature, suite:suite}
        }
        else{
            if(feature != null)
            {
                data = {feature:feature}
            }
            else{
                console.log("Inappropriate data")
                return
            }
        }
    }
    if(action == "run")
    {
    url = "/RFERUN"
    }
    else{
            if(action == "abort")
            {
                url = "/RFEABORT"
            }
            else {
                console.log("Unknown error")
                return
            }
        }
    var ajx = $.ajax({
				url:url,
				method:"POST",
				data:data
				});
		ajx.done(function(msg){
                if(msg.toLowerCase() == "success")
                {
                    console.log(action + ": successful")
                }
                else{
                    console.log(action + ": failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			});
}