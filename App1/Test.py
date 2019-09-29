from django.http import HttpResponse
import datetime
from modelling import HTMLLoader
import App1.settings as meta
import time

def login():
    dct = {
        "body$b1": "<div id=header name=header><h2 style=\"width:98%;padding:1%;text-align:left;\">"
                   "Robotframework Front End</h2></div>",
        "body$b2": "<div id=login_div name=login_div><table><tr><th colspan=2>Enter your credential</th></tr>"
                   "<tr><td colspan=2 id=err_msg>&nbsp;</td></tr>"
                   "<tr><td>Username</td><td><input type=text id=username /></td></tr>"
                   "<tr><td>Password</td><td><input type=password id=password /></td></tr>"
                   "<tr><td colspan=2 id=err_msg>&nbsp;</td></tr>"
                   "<tr><td colspan=2 style='text-align:center;'><button name=plz id=plz>Submit</button></td></tr>"
                   "</table></div>",
        "script$s1": "../static/jquery.min.js",
        "script$s2": "../static/home.js",
        "style$t1": "../static/home.css",
        "headrawmeta$m1": "<title>home</title>"
        }
    return HTMLLoader.htmlstructure(**dct)
    

def home(request):
    try:
        if request.method == "GET":
            return HttpResponse(login())
        elif request.method == "POST":
            print(request.POST)
            if request.POST["action"] == "check_in":
                if request.POST["username"] in meta.user_list:
                    if request.POST["password"] == meta.user_list[request.POST["username"]]["password"]:
                        request.session["username"] = request.POST["username"]
                        request.session["last_login"] = str(time.time() * 1000)
                        Msg = "Authenticated"
                        status = 200
                    else:
                        Msg = "Authorized"
                        status = 401
            elif request.POST["action"] == "check_out":
                if request.session.get("username") is not None:
                    del request.session["username"]
                    Msg = "Logout"
                    status = 401
                else:
                    Msg = "Unauthorize"
                    status = 403
            elif request.POST["action"] == "check":
                if request.session.get("username") is not None:
                    Msg = "Authorized"
                    status = 200
                else:
                    Msg = "Unauthorize"
                    status = 403
            else:
                Msg = "unknown request"
                status = 500
        else:
            Msg = "Forbidden"
            status = 403
        print(Msg, status)
        return HttpResponse(Msg, status=status)
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

