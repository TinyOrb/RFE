last_client_edit = null
td = null
lag = null
snapshot_editor = null
snapshot_time = null

$(document).ready(function(){
	console.log("loaded")
    get_time()
/*
    setInterval(function(){
        if(current_feature != "")
            get_suite_tree(current_feature)
        }, 5000);
        */
});



function sync_edit(){
    fetch_content()
}

function fetch_content(){
    var data = {};
    data["feature"] = window.location.href.split("?")[1].split('&')[0].split("=")[1]
    data["suite"] = window.location.href.split("?")[1].split('&')[1].split("=")[1]
    data["action"] = "read"
    var ajx = $.ajax({
				url:"/RFEEDITOR",
				method:"POST"
				data:data
				});
		ajx.done(function(msg){
                if(msg != "fail")
                {
                    f_data = JSON.parse(msg);
                    server_modify_time = parseFloat(f_data.mtime) - lag
                    if(snapshot_time != null && last_client_edit != null &&last_client_edit > server_modify_time){
                        update_content()
                        }
                    }
                    else{
                        if(snapshot_time == null){
                            snapshot_time = server_modify_time
                            if(snapshot_editor != null && f_data.data != snapshot_editor){
                                snapshot_editor = f_data.data
                                $("#editor").text(snapshot_editor)
                                }
                                else{
                                    if(snapshot_editor != null){
                                        snapshot_editor = f_data.data
                                        $("#editor").text(snapshot_editor)
                                    }
                                }
                            }
                            else{
                                if(last_client_edit == null){
                                    last_client_edit = new Date().getTime();
                                    if(f_data.data != $("#editor").text()){
                                        update_content()
                                    }
                                }
                            }
                        }
                else{
                    console.log("Unable to fetch time failed")
                }
			});
		ajx.fail(function(jqXHR, textStatus){
				console.log(jqXHR, textStatus);
			});
}

function update_content(){
    var data = {};
    data["feature"] = window.location.href.split("?")[1].split('&')[0].split("=")[1]
    data["suite"] = window.location.href.split("?")[1].split('&')[1].split("=")[1]
    data["action"] = "write"
    data["content"] = $("#editor").text()

        var ajx = $.ajax({
                    url:"/RFEEDITOR",
                    method:"POST"
                    data:data
                 });
            ajx.done(function(msg){
                    if(msg != "fail")
                    {
                        fetch_content()
                    }
                    else{
                        console.log("Unable to fetch time failed")
                    }
                });
            ajx.fail(function(jqXHR, textStatus){
                    console.log(jqXHR, textStatus);
                });
}

function get_time(){
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