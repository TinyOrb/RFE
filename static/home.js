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

    $('#plz').click(function(){
        data = {}
        data["username"] = $("#username").val();
        data["password"] = $("#password").val();
        data["action"] = "check_in"
        check_up(data);
    })
});
