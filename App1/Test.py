from django.http import HttpResponse
import datetime
from modelling import HTMLLoader

def login():
    dct = {
        "body$b1": "<div id=header name=header><h2 style=\"width:98%;padding:1%;text-align:left;\">"
                   "Robotframework Front End</h2></div>",
        "body$b2": "<div id=login_div name=login_div><table><tr><th colspan=2>Enter your credential</th></tr>"
                   "<tr><td colspan=2 id=err_msg>&nbsp;</td></tr>"
                   "<tr><td>Username</td><td><input type=text id=username/></td></tr>"
                   "<tr><td>Password</td><td><input type=password id=password/></td></tr>"
                   "<tr><td colspan=2 id=err_msg>&nbsp;</td></tr>"
                   "<tr><td colspan=2 style='text-align:center;'><button name=plz id=plz>Submit</button></td></tr>"
                   "</table></div>",
        "script$s2": "../static/home.js",
        "style$t1": "../static/home.css"
        }
    return HTMLLoader.htmlstructure(**dct)
    

def home(request):
    return HttpResponse(login())
