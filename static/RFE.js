tc_head = ""
$(document).ready(function(){
	console.log("loaded")
	tc_head = $("#testcase").html()
        $(".suite_list").click(function(){
		// console.log(this.innerHTML);
		get_suite_tree(this.innerHTML)
	});

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
	console.log(feature_name)

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
					console.log(msg);
					htmlTable = "";
					for(i = 0; i < data.suites.length; i++){
						htmlTable = htmlTable + "<table style=\"width:100%;margin:auto;background:#2F4F4F;color:white;\"><tr><td><h3>" + he.escape(data.suites[i].name.toUpperCase()) + "</h3></td><td><h6 class=runnable feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer;\">Run</h6><td></tr></table>" ;
						for(j = 0; j < data.suites[i].tcs.length; j++){
							htmlTable = htmlTable + "<table style=\"width:100%;margin:auto;background:lightgrey;\"><tr><td><h4>" + he.escape(data.suites[i].tcs[j]) + "</h4></td><td><h6 class=runnable2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" tc=\""+he.escape(data.suites[i].tcs[j]) +"\" style=\"text-align:right; cursor:pointer;\">Run</h6><td></tr></table>";
						}
					}
					$("#testcase").html(tc_head + htmlTable);
                    $("#testcase").css({"overflow":"auto"});

                    $(".runnable").hover(function(){
                    $(this).css({"color":"lightgrey"});
                    }, function(){
                    $(this).css({"color":"white"})
                    });

                    $(".runnable2").hover(function(){
                    $(this).css({"color":"darkgrey"});
                    }, function(){
                    $(this).css({"color":"#090909"})
                    });

                    $(".runnable").click(function(){
                        console.log(this.innerHTML);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                    });

                    $(".runnable2").click(function(){
                        console.log(this);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        console.log(this.getAttribute("tc"));
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