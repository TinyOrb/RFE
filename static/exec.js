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

    $(".result_exec").change(function(){
        data = {}
        data["suite"] = $(this).attr("es_id")
        data["case"] = $(this).attr("case_id")
        data["type"] = $(this).attr("type")
        data["script"] = $(this).attr("script")
        data["status"] = $("option:selected", this).text();
        data["action"] = "update_case"
        suite_plan(data)
    });

    $(".map_log_form").click(function(){
        data = {}
        data["suite"] = $(this).attr("es_id")
        data["script"] = $(this).attr("script")
        data["action"] = "map_log_form"
        suite_plan(data)
    });

});

function suite_plan(data){

    var ajx = $.ajax({
          url:"/EXEC",
          method:"POST",
          data : data
    });

	ajx.done(function(msg){
	    p_msg = JSON.parse(msg);

	    switch(data.action){
	    case "update_case":
	        if(msg == 0){
                    prompt_msg("successfully updated case status");
                }
	    break
	    case "map_log_form":
	        load_form(p_msg.form);
	        $("#cancel").click(function(){
	            clr_msg();
	        });
	        $(".map_log").click(function(){
	            data = {}
                data["suite"] = $(this).attr("es_id")
                data["script"] = $(this).attr("script")
                data["project"] = $(this).attr("proj")
                data["time"] = $(this).attr("time")
                data["action"] = "map_log"
                suite_plan(data)
	        });
	    break
	    case "map_log":
	        if(msg == 0){
                    prompt_msg("Mapping successfully done");
                    location.reload();
                }
	    break
	    }

	 });

}
