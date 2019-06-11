from django.http import HttpResponse
import datetime
from modelling import HTMLLoader
from Robot_loader import Al_robot

def initial():
    Suite = Al_robot.fetch_All_suite().keys()
    initial_loading = {
        "body$b1":"<div id=header name=header><h3 style='padding:1%;'>Robotframework Front End</h3></div>",
        "body$b2":"<div id=suite name=suite><h2>Test Suite</h2></div>",
        "body$b3":"<div id=testcase name=testcase><h2>Test Case</h2></div>",
        "body$b4":"<div id=ControlReport name=ControlReport>",
        "body$b5":"<div id=control name=control><h2>Controls</h2></div><br>",
        "body$b6":"<div id=log name=log><h2>Logs and Reports</h2></div>",
        "body$b7":"</div>",
        "script$s1":"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",
        "bscript$s2":"static/RFE.js",
        "style$t1":"static/RFE.css"
        }
    i = 1
    initial_loading["headrawscript$r"+str(i)] = "$(document).ready(function(){"
    i = i+1
    for s in Suite:
        initial_loading["headrawscript$r"+str(i)] = "$('#suite').html($('#suite').html()+'<div class=suite_list>"+s+"</div>');"
        i = i + 1
    initial_loading["headrawscript$r"+str(i)] = "});"
    return HTMLLoader.htmlstructure(**initial_loading)

def InitialLoad(request):
    try:
        return HttpResponse(initial())
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

def LoadTestSuite(request):
    try:
        suite = request.POST.get("suite","")
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")
        
