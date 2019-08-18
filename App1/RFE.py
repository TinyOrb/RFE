"""
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
"""

import json
import os

from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from modelling import HTMLLoader
from Robot_loader import Al_robot
from Robot_loader import Al_robot_parser
from robot_runner.invoke import invoke as invoke
import App1.settings as meta

import urllib

import time

runner = invoke(track='App1/robot_runner/track.json', result_dir=os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT"))


def initial():
    Suite = Al_robot.fetch_All_suite().keys()
    initial_loading = {
        "body$b1": "<div id=load_message name=load_message></div>",
        "body$b2":"<div id=header name=header><h2 style=\"width:98%;padding:1%;text-align:left;\">Robotframework Front End</h2></div>",
        "body$b3":"<div id=feature name=feature><div id=suite name=suite><h2>Features</h2></div><div id=edit_suite name=edit_suite><button id=edit_suite_btn>Edit Project</button></div></div>",
        "body$b4":"<div id=testcase name=testcase><h2>Test Case</h2></div>",
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


def status_load(current, history):
        initial_loading = {
            "body$b1": "<div id=header name=header><h2 style=\"width:98%;padding:1%;text-align:left;\">"
                       "Robotframework Front End</h2></div>",
            "body$b2": "<div id=suite name=suite><h2>STATS</h2></div>",
            "body$b3": "<div id=testcase name=testcase><h2>Logs</h2></div>",
            "script$s1": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",
            "script$s2": "../static/he.js",
            "style$t1": "../static/RFE.css",
            "bscript$s1": "../static/FSTAT.js",
        }
        if current is None:
            i = 1
            initial_loading["headrawscript$r" + str(i)] = "$(document).ready(function(){ " \
                                                          "tc_head = $(\"#testcase\").html(); " \
                                                          "$(\"#testcase\").html(tc_head + \"No Logs\"); " \
                                                          "});"
            return HTMLLoader.htmlstructure(**initial_loading)
        else:
            initial_loading["headrawscript$r1"] = "$(document).ready(function(){"
            initial_loading["headrawscript$r1"] += "$('#suite').html($('#suite').html()+'<div><h3>Current status</h3></div>');"
            initial_loading["headrawscript$r1"] += "$('#suite').html($('#suite').html()+'<div class=stat_list>" + current["time"] + "</div>');"
            initial_loading["headrawscript$r1"] += "$('#suite').html($('#suite').html()+'<div><h3>History status</h3></div>');"
            for h in history:
                initial_loading["headrawscript$r1"] += "$('#suite').html($('#suite').html()+'<div class=stat_list>" + h["time"] + "</div>');"
            initial_loading["headrawscript$r1"] += "});"
            #print(HTMLLoader.htmlstructure(**initial_loading))
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
def GetAllSuites(request):
    global runner
    try:
        if request.method == "POST":
            all = {}
            features = meta.Test_Suite_Folder
            for feature in features.keys():
                all[feature]=Al_robot.list_non_binary_files(meta.Test_Suite_Folder[feature])
            return HttpResponse(json.dumps(all))
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
            try:
                include_tag = request.POST["include_tag"]
            except KeyError as k:
                include_tag = None
            try:
                exclude_tag = request.POST["exclude_tag"]
            except KeyError as k:
                exclude_tag = None
            try:
                variable_file = os.path.join(meta.Variable_File[feature], request.POST["variableFile"])
            except KeyError as k:
                variable_file = None
            try:
                variable = request.POST["variable"]
            except KeyError as k:
                variable = None
            runner.Python_Path = meta.ENV_Path[feature]
            try:
                runner.cd_path = meta.CWD[feature]
            except:
                runner.cd_path = None
            return HttpResponse(runner.trigger(feature=feature, suite=suite, tc=tc, variable=variable, variablefile=variable_file, include_tags=include_tag, exclude_tags=exclude_tag))
    except Exception as e:
        #raise e
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
            return HttpResponse(runner.abort_run(feature=feature, suite=suite, tc=tc))
    except Exception as e:
        # raise e
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")


@ensure_csrf_cookie
def Run_stat(request):
    global runner
    try:
        if request.method == "GET":
            feature = request.GET["feat"]
            try:
                suite = request.GET["suite"]
            except KeyError as k:
                suite = None
            try:
                tc = request.GET["tc"]
            except KeyError as k:
                tc = None
            #print(feature, suite, tc)
            if tc != None:
                tc = urllib.unquote(tc)
            #print(feature, suite, tc)
            return HttpResponse(status_load(runner.fetch_current(feature, suite, tc),
                                                       runner.fetch_history(feature, suite, tc)))
        else:
            return HttpResponse("No attribute received")
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")


def log_load(current, history, time):
    global runner

    info = {}

    if current is not None:
        if current["time"] == time:
            info = current
        else:
            for h in history:
                if h["time"] == time:
                    info = h
    if len(info) > 0:
        output = ""
        for s in str(runner.script_log(info["script_output"])).splitlines():
            output += "<tr><td>%s</td></tr>" % s
        initial_loading = {
            "body$b1": "<br><br><table><tr><td><a href=\"%s\">Log</a></td></tr></table><br>" % ("static"+info["log"].replace(meta.STATICFILES_DIRS[0], "")),
            "body$b2": "<table><tr><td><a href=\"%s\">Report</a></td></tr></table><br>" % ("static"+info["output"].replace(meta.STATICFILES_DIRS[0], "")),
            "body$b3": "<table><tr><th>Script log</th></tr></table>",
            "body$b4": "<table>%s</table>" % output
        }
    else:
        initial_loading = {"body$b1": "Unable to Log"}
    return HTMLLoader.htmlstructure(**initial_loading)



@ensure_csrf_cookie
def Log_stat(request):
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
            try:
                start_time = request.POST["time"]
            except KeyError as k:
                print("Not enough attribute")
                return HttpResponse("")
            if tc is not None:
                tc = urllib.unquote(tc)
            #print(feature, suite, urllib.unquote(tc), start_time)
            return HttpResponse(log_load(runner.fetch_current(feature, suite, tc), runner.fetch_history(feature, suite, tc), start_time))
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

@ensure_csrf_cookie
def load_meta_run_with(request):
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
            if tc is not None:
                tc = urllib.unquote(tc)
            tags = Al_robot_parser.get_tag_list(Al_robot.fetch_All_suite()[feature], suite)

            if meta.Variable_File[feature] is not None:
                variable_file = Al_robot.list_variable_files(meta.Variable_File[feature])
                if type(variable_file) is not list:
                    print("Error", variable_file)
                else:
                    pass
            else:
                variable_file = []
            return HttpResponse(json.dumps({"tags": list(set(tags)), "vf": variable_file}))
        else:
            return HttpResponse("fail")
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

def editor_load():
        initial_loading = {
            "body$b1": "<div id=header name=header><h2 style=\"width:98%;padding:1%;text-align:left;\">"
                       "Robotframework Front End</h2></div>",
            "body$b2": "<div style=\"width:97%;padding:1%; height:84%; margin-left:0.5%; margin-right:0.5%; margin-top:0.5%;\"><textarea style=\"width:98%;height:98%;resize: none;\" id=\"editor\"></textarea></div>",
            "script$s1": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",
            "script$s2": "../static/he.js",
            "style$t1": "../static/RFE.css",
            "bscript$s1": "../static/rfeedit.js",
        }
        return HTMLLoader.htmlstructure(**initial_loading)

@ensure_csrf_cookie
def Core_Editor(request):
    try:
        if(request.method == "POST"):
            feature = request.POST["feature"]
            try:
                suite = request.POST["suite"]
            except KeyError as k:
                suite = None
            try:
                tc = request.POST["tc"]
                tc = urllib.unquote(tc)
            except KeyError as k:
                tc = None
            try:
                action = request.POST["action"]
            except KeyError as k:
                action = None

            if suite is not None and tc is None:
                suite_path = os.path.join(meta.Test_Suite_Folder[feature], suite)

                if action == "read":
                    content = Al_robot_parser.read_robot_content(suite_path)
                    return HttpResponse(json.dumps(content), status=200)

                elif action == "write":
                    try:
                        content = request.POST["content"]

                        wstatus = Al_robot_parser.write_robot_content(suite_path, content)
                        if wstatus is not None:
                            return HttpResponse("success", status=200)
                        else:
                            return HttpResponse("fail", status=500)

                    except KeyError as k:
                        return HttpResponse("fail", status=500)
                else:
                    print("unknown action provided")
                    return HttpResponse("fail", status=400)

            else:
                print("Either suite is missing and extra tc info provided")
                return HttpResponse("fail", status=400)
        elif(request.method == "GET"):
            return HttpResponse(editor_load(), status=400)
        else:
            return HttpResponse("fail", status=400)
    except Exception as e:
        raise e
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")

@ensure_csrf_cookie
def get_time(request):
    try:
        if(request.method == "POST"):
            return HttpResponse(str(time.time() * 1000))
        else:
            return HttpResponse("fail", status=400)
    except Exception as e:
        return HttpResponse("Some error occurred <div style='display: none;'>" + str(e) + "</div>")
