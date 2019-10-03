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
current_feature = ""
$(document).ready(function(){

   $.getScript( "static/ingen.js", function( data, textStatus, jqxhr ) {
//      console.log( data ); // Data returned
//      console.log( textStatus ); // Success
//      console.log( jqxhr.status ); // 200
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
	tc_head = $("#testcase").html();
	current_feature = $(".suite_list")[0].innerHTML;

        $(".suite_list").click(function(){
		current_feature = this.innerHTML;
		get_suite_tree(current_feature)
	});

	$("#edit_suite_btn").click(function(){
		get_all_suite();
	});

    get_suite_tree(current_feature)


    $("#add_feat").click(function(){
        add_feat("template");
    });

    $("#del_feat").click(function(){
    });

    setInterval(function(){
        if(current_feature != "")
            get_suite_tree(current_feature)
        }, 5000);
})


function add_feat(action){
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
		if(msg != "" || msg.toLowerCase() != null){
            var data = JSON.parse(msg);

            htmlTable="<table>"
			htmlTable+="<tr><td>Project Type: </td><td><select id=type_feat name=type_feat>"
			for(var f in data.template){
				htmlTable+="<option>"+f+"</option>"
			}
			htmlTable+="</select></td></tr>"
            }
            htmlTable+="<tr><td>Project name: </td><td id=feat_name><input type=text id=feat_name></td></tr>"
            htmlTable += "<tr><td><button id='cancel_run_with'>Cancel</button></td><td style='text-align:right'><button id='post_run_with' name='post_run_with'>Create Project</button></td></tr>";
			htmlTable += "<tr><td colspan=2 id='form_msg'></td></tr>"
			htmlTable+="</table>"

			$("#post_run_with").click(function(){
                template = $("#type_feat option:selected").text()
                feat_name = $("#feat_name").val();
                var data = {}
                data["name"] = feat_name
                data["template"] = template
                if(feat_name != ""){
                    manage_feat("add", data)
                    $("#load_message").html("");
                    $("#load_message").css({"display":"none", "z-index":"0"});
                }
                else{
                    $("#feat_name").css({"border-color":"red"});
                    $("#form_msg").html("Invalid field value");
                }
			});

			$("#cancel_run_with").click(function(){
                $("#load_message").html("");
                $("#load_message").css({"display":"none", "z-index":"0"});
            });
         });

         ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
          });

}

function del_feat(){
}

function get_all_suite(){
	$.ajaxSetup({
                beforeSend: function(xhr, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                 }
        });

        var ajx = $.ajax({
                     url:"/GETALLSUITES",
                     method:"POST",
                     });

	ajx.done(function(msg){
		if(msg != "" && msg.toLowerCase() != "none"){
                    	var data = JSON.parse(msg);
			htmlTable="<table>"
			htmlTable+="<tr><td>Feature: </td><td><select id=pedit_feat name=pedit_feat>"
			for(var f in data){
				htmlTable+="<option>"+f+"</option>"
			}
			htmlTable+="</select></td></tr>"
			htmlTable+="<tr><td>File: <td><td><select id=pedit_action name=pedit_action>"
			htmlTable+="<option 'selected'>select</option><option>add</option><option>edit</option><option>delete</option>"
			htmlTable+="</select></td></tr>"
			htmlTable+="<tr><td>File: </td><td id=pedit_file_td><input type=text id=pedit_file></td></tr>"
			htmlTable += "<tr><td><button id='cancel_run_with'>Cancel</button></td><td style='text-align:right'><button id='post_run_with' name='post_run_with'>Action</button></td></tr>";
			htmlTable+="</table>"
			$("#load_message").html(htmlTable);
            $("#load_message").css({"position":"fixed", "top":"30%", "left":"40%", "display":"block", "z-index":"10", "background": "lightgrey", "border-width":"2px", "border-color":"#2F4F4F", "border-style": "solid"})
			$("#pedit_action").change(function(){
				switch($("#pedit_action option:selected").text()){
					case "select":
						$("#pedit_file_td").html("<input type=text id=pedit_file>")
						break;
					case "add":
						$("#pedit_file_td").html("<input type=text id=pedit_file>")
						break;
					case "edit":
						htmlTemp="<select id=pedit_sel_file>"
						for(var s in data[$("#pedit_feat option:selected").text()]){
							htmlTemp+="<option>"+data[$("#pedit_feat option:selected").text()][s]+"</option>"
						}
						htmlTemp+="</select>"
						$("#pedit_file_td").html(htmlTemp);
						break;
					case "delete":
						htmlTemp="<select id=pedit_sel_file>"
                                                for(var s in data[$("#pedit_feat option:selected").text()]){
                                                        htmlTemp+="<option>"+data[$("#pedit_feat option:selected").text()][s]+"</option>"
                                                }
                                                htmlTemp+="</select>"
                                                $("#pedit_file_td").html(htmlTemp);
						break;
				}
			});

            		$("#post_run_with").click(function(){
                		    feat = $("#pedit_feat option:selected").text();
				            //action=$("#pedit_action option:selected").text();
				            switch($("#pedit_action option:selected").text()){
                                case "select":
                                    break;
                                case "add":
                                    suite = $("#pedit_file").val();
                                    f_action(feat, suite, "add_fl");
                                    break;
                                case "edit":
                                    suite = $("#pedit_sel_file option:selected").text();
                                    var win = window.open("RFEEDITOR?feat="+feat+"&suite="+suite, '_blank');
                                    win.focus();
                                    break;
                                case "delete":
                                    suite = $("#pedit_sel_file option:selected").text();
                                    f_action(feat, suite, "delete_fl");
						            break;
                                }

                		$("#load_message").html("");
                		$("#load_message").css({"display":"none", "z-index":"0"});
            		});
            		$("#cancel_run_with").click(function(){
                		$("#load_message").html("");
                		$("#load_message").css({"display":"none", "z-index":"0"});
            		});

		}
	});

	ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
          });
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
				if( !msg.includes("Some error occurred") && msg != "" && msg.toLowerCase() != "none"){
					var data = JSON.parse(msg);
					//console.log(data);
					//console.log(msg);
					htmlTable = "";
					for(i = 0; i < data.suites.length; i++){
						htmlTable += "<table style=\"width:100%;margin:auto;background:#2F4F4F;color:white;\"><tr>"
						htmlTable += "<td style=\"width:70%;\"><h3>" + he.escape(data.suites[i].name.toUpperCase()) + "</h3></td>"
						htmlTable += "<td><h5 class=runnable feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">"+(typeof(data.suites[i].status) != "undefined" ? data.suites[i].status : "Wait")+"</h5></td>"
						if(typeof(data.suites[i].status) != "undefined" && data.suites[i].status != "Running")
						    htmlTable += "<td><h5 class=runnable_2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">Run with</h5></td>"
						if(data.suites[i].status == "Running")
						    htmlTable += "<td><h5 class=abort_handle feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">Abort</h5></td>"
						htmlTable += "<td><h5 class=stat_viewer feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">"+"View"+"</h5></td>"
						htmlTable += "<td><a target=_blank style=\" text-decoration: none; color: inherit\" href=\"/RFEEDITOR?feat="+data.feature+"&suite="+data.suites[i].name+"\"><h5 style=\"text-align:right; cursor:pointer; "+ (data.suites[i].status != "Running"? "" :"color:#E39FF6;") +"\">"+"Edit"+"</h5></td>"
						htmlTable += "</tr></table>" ;
						for(j = 0; j < data.suites[i].tcs.length; j++){
							htmlTable += "<table style=\"width:100%;margin:auto;background:lightgrey;\"><tr>"
							htmlTable += "<td style=\"width:70%;\"><h4>" + he.escape(data.suites[i].tcs[j].name) + "</h4></td>"
							htmlTable += "<td><h6 class=runnable2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" tc=\""+he.escape(data.suites[i].tcs[j].name) +"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].tcs[j].status != "Running"? "" : "color:#67032F;" )+ "\">"+(typeof(data.suites[i].tcs[j].status) != "undefined" ? data.suites[i].tcs[j].status : "Wait")+"</h6></td>"
							if(typeof(data.suites[i].tcs[j].status) != "undefined" && data.suites[i].tcs[j].status != "Running")
							    htmlTable += "<td><h6 class=runnable2_2 feat=\""+data.feature+"\" suite=\""+data.suites[i].name+"\" tc=\""+he.escape(data.suites[i].tcs[j].name) +"\" style=\"text-align:right; cursor:pointer; "+ (data.suites[i].tcs[j].status != "Running"? "" : "color:#67032F;" )+ "\">Run with</h6></td>"
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
                        if(this.innerHTML.toLowerCase() == "run"){
                        invoke("run", this.getAttribute("feat"), this.getAttribute("suite"), null);
                        this.innerHTML = "wait"
                        }
                    });

                    $(".runnable2").click(function(){
                        console.log(this);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        console.log(this.getAttribute("tc"));
                        if(this.innerHTML.toLowerCase() == "run"){
                        invoke("run", this.getAttribute("feat"), this.getAttribute("suite"), this.getAttribute("tc"));
                        this.innerHTML = "wait"
                        }
                    });

                    $(".runnable_2").click(function(){
                        console.log(this.innerHTML);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        if(this.innerHTML.toLowerCase() == "run with"){
                        select_message("run_with", this.getAttribute("feat"), this.getAttribute("suite"), null);
                        this.innerHTML = "wait"
                        }
                    });

                    $(".runnable2_2").click(function(){
                        console.log(this);
                        console.log(this.getAttribute("feat"));
                        console.log(this.getAttribute("suite"));
                        console.log(this.getAttribute("tc"));
                        if(this.innerHTML.toLowerCase() == "run with"){
                        select_message("run_with", this.getAttribute("feat"), this.getAttribute("suite"), this.getAttribute("tc"));
                        this.innerHTML = "wait"
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
                    console.log(msg)
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			if(jqXHR["status"] == 401){
                window.location = "/expire"
            }
			});
}

function select_message(action, feat, suite, tc){
    console.log(action, feat, suite, tc)
    data = {"feature": feat, "suite":suite, "tc": tc}
    f_data = ""
    var ajx = $.ajax({
				url:"/RFERUNWITHMETA",
				method:"POST",
				data:data
				});
    ajx.done(function(msg){
        //console.log(msg)
        if(msg.toLowerCase() != "fail" && !msg.toLowerCase().includes("some error occurred"))
        {
            f_data = JSON.parse(msg);
            //console.log(f_data);

            htmlTable = "<table>";
            htmlTable += "<tr><td colspan='2' style='text-align:center;background:#2F4F4F;color:white'>Run with form</td></tr>";
            htmlTable += "<tr><td>Variable</td><td><input type='text' id='variable_text'></td></tr>";
            htmlTable += "<tr><td>Variable file</td><td><select id='selected_variable_file'>"
            htmlTable += "<option 'selected'>--select--</option>"
            for(i = 0; i < f_data.vf.length; i++){
                htmlTable += "<option>" + f_data.vf[i] + "</option>"
            }
            htmlTable += "</select></td></tr>";
            htmlTable += "<tr><td>Include tag</td><td><select id='selected_include_tag'>"
            htmlTable += "<option 'selected'>--select--</option>"
            for(i = 0; i< f_data.tags.length; i++){
            htmlTable += "<option>" + f_data.tags[i] + "</option>"
            }
            htmlTable += "</select></td></tr>";
            htmlTable += "<tr><td>Exclude tag</td><td><select id='selected_exclude_tag'>"
            htmlTable += "<option 'selected'>--select--</option>"
            for(i = 0; i< f_data.tags.length; i++){
            htmlTable += "<option>" + f_data.tags[i] + "</option>"
            }
            htmlTable += "</select></td></tr>";
            if(tc != null)
            {
                htmlTable += "<tr><td><button id='cancel_run_with'>Cancel</button></td><td id='run_with_td_info' feat='"+feat+"' suite='"+suite+"' tc='"+tc+"'><button id='post_run_with' name='post_run_with'>Run</button></td></tr>";
            }
            else{
                htmlTable += "<tr><td><button id='cancel_run_with'>Cancel</button></td><td id='run_with_td_info' feat='"+feat+"' suite='"+suite+"' style='text-align:right'><button id='post_run_with' name='post_run_with'>Run</button></td></tr>";
            }
            htmlTable += "</table>";

            $("#load_message").html(htmlTable);
            $("#load_message").css({"position":"fixed", "top":"30%", "left":"40%", "display":"block", "z-index":"10", "background": "lightgrey", "border-width":"2px", "border-color":"#2F4F4F", "border-style": "solid"})

            $("#post_run_with").click(function(){
                variable_file = $( "#selected_variable_file option:selected" ).text();
                variable = $("#variable_text").val();
                include_tag = $( "#selected_include_tag option:selected" ).text();
                exclude_tag = $( "#selected_exclude_tag option:selected" ).text();
                feat = $("#run_with_td_info").attr("feat");
                suite = $("#run_with_td_info").attr("suite");
                try{
                    tc = $("#run_with_td_info").attr("tc");
                }
                catch(err){
                    tc = null;
                }
                invoke_run_with(feat, suite, tc, variable_file, variable, include_tag, exclude_tag);
                $("#load_message").html("");
                $("#load_message").css({"display":"none", "z-index":"0"});
            });
            $("#cancel_run_with").click(function(){
                $("#load_message").html("");
                $("#load_message").css({"display":"none", "z-index":"0"});
            });
        }
        else{
            console.log("Fetch: failed")
        }
    });
	ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
            if(jqXHR["status"] == 401){
                window.location = "/expire"
            }
        });
}

function invoke_run_with(feat, suite, tc, variable_file, variable, include_tag, exclude_tag){
    var data = {};
    console.log("invoke_run_with")
    data["feature"] = feat;
    data["suite"] = suite
    if(tc != null)
        data["tc"] = tc
    if(variable_file != "--select--")
        data["variableFile"] = variable_file
    if(variable != "")
        data["variable"] = variable
    if(include_tag != "--select--")
        data["include_tag"] = include_tag
    if(exclude_tag != "--select--")
        data["exclude_tag"] = exclude_tag

    var ajx = $.ajax({
				url:"/RFERUN",
				method:"POST",
				data:data
				});
		ajx.done(function(msg){
                if(msg.toLowerCase() == "success")
                {
                    console.log("Run with: successful")
                }
                else{
                    console.log("Run with: failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			if(jqXHR["status"] == 401){
                window.location = "/expire"
            }
			});
    //console.log(data)

}

function f_action(feat, fl, action){
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
				data:{"feature":feat, "action":action, "suite":fl}
				});
		ajx.done(function(msg){
		    if(msg == "success"){
		        prompt_msg(msg);
		    }
		    else{
		        prompt_msg(msg);
		    }
		});
	ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			});
}

function manage_feat(action, data){
    $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                 }
        });
        var ajx = $.ajax({
         url:"/MANAGEFEAT",
         method:"POST",
         data : data
         });

        ajx.done(function(msg){
            if(msg == "success"){
                prompt_msg("Operation success");
            }
            else{
                prompt_msg("Operation failed!");
            }
        });

         ajx.fail(function(jqXHR, textStatus){
            console.log(jqXHR, textStatus);
          });
}