import json
import os

from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from modelling import HTMLLoader
from Robot_loader import Al_robot
from Robot_loader import Al_robot_parser
from robot_runner.invoke import invoke as invoke
import App1.settings as meta

runner = invoke(track='App1/robot_runner/track.json', result_dir=os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT"))

def initial():
    Suite = Al_robot.fetch_All_suite().keys()
    initial_loading = {
        "body$b1":"<div id=header name=header><h2 style=\"padding:1%;text-align:left;\">Robotframework Front End</h2></div>",
        "body$b2":"<div id=suite name=suite><h2>Features</h2></div>",
        "body$b3":"<div id=testcase name=testcase><h2>Test Case</h2></div>",
        "body$b4":"<div id=ControlReport name=ControlReport>",
        "body$b5":"<div id=control name=control><h2>Controls</h2></div><br>",
        "body$b6":"<div id=log name=log><h2>Logs and Reports</h2></div>",
        "body$b7":"</div>",
        "script$s1":"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",
        "script$s2": "static/he.js",
        "bscript$s1":"static/RFE.js",
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


def fetchSuite(feature):
    TC = Al_robot_parser.get_testcases_list(feature, Al_robot.fetch_All_suite()[feature])
    return TC


@ensure_csrf_cookie
def InitialLoad(request):
    try:
        return HttpResponse(initial())
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")


@ensure_csrf_cookie
def LoadTestSuite(request):
    global runner
    try:
        if request.method == "POST":
            feature = request.POST["feature"]
            return HttpResponse(json.dumps(runner.get_run_state(fetchSuite(feature))))
    except Exception as e:
        # raise e
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

@ensure_csrf_cookie
def Run_instance(request):
    global runner
    try:
        if request.method == "POST":
            feature = request.POST["feature"]
            try:
                suite = request.POST["suite"]
            except KeyError as k:
                suite = None
            try:
                tc = request.POST["tc"]
            except KeyError as k:
                tc = None
            return HttpResponse(runner.trigger(feature=feature, suite=suite, tc=tc))
    except Exception as e:
        # raise e
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

@ensure_csrf_cookie
def Abort_instance(request):
    global runner
    try:
        if request.method == "POST":
            feature = request.POST["feature"]
            try:
                suite = request.POST["suite"]
            except KeyError as k:
                suite = None
            try:
                tc = request.POST["tc"]
            except KeyError as k:
                tc = None
            return HttpResponse(runner.get_run_state(feature=feature, suite=suite, tc=tc))
    except Exception as e:
        # raise e
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")