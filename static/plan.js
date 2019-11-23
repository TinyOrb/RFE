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
                prompt_msg("successfully add suite")
            }
            break
            case "case_form":
                load_form(p_msg.form);
                $("#cancel_form").click(function(){
                    clr_msg();
                });
                $("#submit_case").click(function(){
                });
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