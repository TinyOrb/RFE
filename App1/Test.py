from django.http import HttpResponse
import datetime
from modelling import HTMLLoader

def temp():
    dct = {
        "body$b1":"<label for=x1>Enter your name</label>",
        "body$b2":"<input type=text id=x1 name=x1 /> <br> <button id=sub name=sub>Greeting</button>",
        "body$b3":"<div id=div1 name=div1></div>",
        "script$s1":"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",
        "script$s2":"static/RFE.js",
        "style$t1":"static/test.css"
        }
    return HTMLLoader.htmlstructure(**dct)

def test1(request):
    try:
        xid = request.GET["id"]
        return HttpResponse(temp())
    except Exception as e:
        return HttpResponse("Some error occurred" + str(e))
        print e
    

def home(request):
    return HttpResponse("<h2>Welcome to Application 1</h2>")
