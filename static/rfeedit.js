content = null
last_content_modify = null
td = null

$(document).ready(function(){
	console.log("loaded")

	var ajx = $.ajax({
				url:"/GETNOW",
				method:"POST"
				});
		ajx.done(function(msg){
                if(msg.toLowerCase() != "fail")
                {
                    d = new Date()
                    td = Number(message) - d.getTime();
                }
                else{
                    console.log("Unable to fetch time failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			});

/*
    setInterval(function(){
        if(current_feature != "")
            get_suite_tree(current_feature)
        }, 5000);
        */
})


function sync_edit(){
    if(content == null)
    {
        content = fetch_content()
        $("#editor").text(content.data)
    }
    else{
            x = fetch_content()
            content = $("#editor").text()
            if(x.data == content.data)
            {
                //do nothing
            }
            else{
                if(x.time > content.time)
                {
                   content = x
                   $("#editor").text(content.data)
                }
                else{
                    content = update_content()
                }
            }
    }
}

function fetch_content(){

}

function update_content(){
}