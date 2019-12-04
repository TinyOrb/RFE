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

    $("#add_suite").click(function(){
        data = {"action":"suite_form"}
        suite_plan(data)
    });

    $("#add_case").click(function(){
        data = {"action":"case_form"}
        suite_plan(data)
    });

    $(".edit_suite").click(function(){
        data = {}
        data["suite"] = $(this).attr("suite_id")
        data["action"] = "edit_suite_form"
        suite_plan(data)
    });

    $(".edit_case").click(function(){
        data = {}
        data["suite"] = $(this).attr("suite_id")
        data["case"] = $(this).attr("case_id")
        data["action"] = "edit_case_form"
        suite_plan(data)
    });

    $(".del_suite").click(function(){
        data = {}
        data["suite"] = $(this).attr("suite_id")
        data["action"] = "del_suite"
        suite_plan(data)
    });

    $(".del_case").click(function(){
        data = {}
        data["suite"] = $(this).attr("suite_id")
        data["case"] = $(this).attr("case_id")
        data["action"] = "del_case"
        suite_plan(data)
    });

    $("#exec_suite").click(function(){
        data = {}
        data["suite"] = $(this).attr("suite_id")
        data["action"] = "instantiate_suite"
        suite_plan(data)
    });


	console.log("loaded")

});

function suite_plan(data){

    var ajx = $.ajax({
          url:"/PLAN",
          method:"POST",
          data : data
    });

	ajx.done(function(msg){
	    p_msg = JSON.parse(msg);

	    switch(data.action){
            case "suite_form":
                load_form(p_msg.form);

                project = $("#selected_project option:selected").text();
                $("#select_suite").html("")
                p_msg.projects[project].forEach(select_html)

                $("#selected_project").change(function(){
                    project = $("#selected_project option:selected").val();
                    $("#select_suite").html("");
                    p_msg.projects[project].forEach(select_html);
                });
                $("#cancel_form").click(function(){
                    clr_msg();
                });
                $("#submit_suite").click(function(){
                    data = {}
                    data["name"] = $("#suite_name").val()
                    data["project"] = project
                    data["action"] = "submit_suite_form"
                    data["suite_list"] = $("#select_suite option:selected").toArray().map(item => item.value).join();
                    console.log(data["suite_list"])
                    suite_plan(data)
                })
            break
            case "submit_suite_form":
                if(msg == 0){
                    prompt_msg("successfully add suite");
                    location.reload();
                }
            break
            case "case_form":
                load_form(p_msg.form);
                $("#cancel_form").click(function(){
                    clr_msg();
                });
                $("#submit_case").click(function(){
                    data = {}
                    data["name"] = $("#case_name").val();
                    data["desc"] = $("#case_desc").val();
                    data["steps"] = $("#case_step").val();
                    data["suite"] = window.location.href.split("=")[1]
                    data["action"] = "submit_case_form"
                    suite_plan(data)
                });
            break
            case "submit_case_form":
            if(msg == 0){
                prompt_msg("successfully add case");
                location.reload();
            }
            break
            case "edit_suite_form":
                load_form(p_msg.form);

                project = $("#selected_project option:selected").text();
                $("#select_suite").html("")
                p_msg.projects[project].forEach(select_html)

                $("#selected_project").change(function(){
                    project = $("#selected_project option:selected").val();
                    $("#select_suite").html("");
                    p_msg.projects[project].forEach(select_html);
                });

                $("#update_suite").click(function(){
                    data = {}
                    data["suite"] = $("#update_suite").attr("suite_id");
                    data["name"] = $("#suite_name").val();
                    data["project"] = project
                    data["action"] = "update_suite"
                    data["suite_list"] = $("#select_suite option:selected").toArray().map(item => item.value).join();
                    suite_plan(data)
                });

                $("#cancel_form").click(function(){
                    clr_msg();
                });
            break
            case "update_suite":
                if(msg == 0){
                    prompt_msg("Suite successfully updated");
                    location.reload();
                }
            break
            case "edit_case_form":
                load_form(p_msg.form);
                $("#cancel_form").click(function(){
                    clr_msg();
                });
                $("#update_case").click(function(){
                    data = {}
                    data["suite"] = $("#update_case").attr("suite_id")
                    data["case"] = $("#update_case").attr("case_id")
                    data["name"] = $("#case_name").val();
                    data["desc"] = $("#case_desc").val();
                    data["steps"] = $("#case_step").val();
                    data["suite"] = window.location.href.split("=")[1]
                    data["action"] = "update_case"
                    suite_plan(data)
                });
            break
            case "update_case":
                if(msg == 0){
                    prompt_msg("Case successfully updated");
                    location.reload();
                }
            break
            case "del_suite":
                if(msg == 0){
                    prompt_msg("successfully suite deleted");
                    location.reload();
                }
            break
            case "del_case":
                if(msg == 0){
                    prompt_msg("successfully case deleted");
                    location.reload();
                }
            break
            case "instantiate_suite":
                if(msg == 0){
                    prompt_msg("successfully suite instantiated");
                }
            break
        }
	})

	ajx.fail(function(jqXHR, textStatus){
	    console.log(jqXHR, textStatus);
    });
}

function select_html(item){
    $("#select_suite").append("<option value="+item+">"+item+"</option>")
}