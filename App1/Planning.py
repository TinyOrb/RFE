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

import os
import json
import logging
import time

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from App1.misc.rw_pool import rw_pool
from modelling.HTMLLoader import htmlstructure
import App1.settings as meta
from App1.manual.man_manage import suite_manager
from App1.Robot_loader import Al_robot_parser
from App1.Robot_loader import Al_robot

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
pool_1 = rw_pool(20, "App1/all_manual.json")

header = "<div id=header name=header><h2 style=\"width:50%;padding:1%;text-align:left;float:left;\">" \
         "Robotframework Front End</h2><table style='padding:1%;float:right;color:white;'><tr><td>{}</td>" \
         "<td><button id=logout>logout</button></td></tr></table></div>"

def init_all_suite(username, suite):
    '''
    Return suite planning page html
    '''
    suites = suite_manager(pool_1)


    dct = {
        "body$b1": header.format(username),
        "script$s1": "../static/jquery.min.js",
        "script$s2": "static/he.js",
        "style$t1": "../static/plan.css",
        "bscript$s1": "../static/plan.js",
        "headrawmeta$m1": "<title>suites</title>"
    }
    if suite is None:
        all_suite = suites.get_suites()
        suites_list = all_suite.keys()

        table = "<div id=\"suites_block\" style=\"width:70%;float:left;margin:1% 2%;overflow-y:auto;background:#FFFFE0;height:80%;\">" \
                "<table style=\"width:100%;\">"
        table += "<tr style=\"background:#2f4f4f;color:white;\"><th style=\"width:12%;\">{}</th>" \
                 "<th style=\"width:50%;\">{}</th>" \
                 "<th style=\"width:8%;\">{}</th>" \
                 "<th colspan=3></th>" \
                 "<th style=\"width:10%;\">{}</th></tr>".format("Suite id.", "Suite name", "Owner", "Created On")
        for li in suites_list:
            edit_btn = "<button id=edit_suite suite_id={}>Edit</button>".format(li)
            del_btn = "<button id=del_suite suite_id={}>Delete</button>".format(li)
            table += "<tr style=\"background:lightgrey;\">" \
                     "<td>{}</td>" \
                     "<td>{}</td>" \
                     "<td>{}</td>" \
                     "<td style=\"width:5%;\"><a style=\"text-decoration:none;\" target=_blank href=/PLAN?suite={}>open</a></td>" \
                     "<td style=\"width:5%;\">{}</td>" \
                     "<td style=\"width:5%;\">{}</td>" \
                     "<td style=\"width:15%;\">{}</td></tr>".\
                format(li, all_suite[li]["name"], all_suite[li]["creator"], li, edit_btn, del_btn, all_suite[li]["created_date"])
        table += "</table></div>"
        dct["body$b2"] = table
        dct["body$b3"] = "<div style=\"width:20%;float:left;text-align:center;margin:1%;overflow-y:auto;background:#FFFFE0;height:80%;\">" \
                         "<h3 style=\"background:black;color:white;margin:1%;\">Future Scope</h3></div>"
        dct["body$b4"] = "<div style=\"width:94%;margin:1%;height:15%;\">" \
                         "<button style=\"padding:0.5% 1%;margin:0 1%;\" id=add_suite>Add Suite</button></div>"
    else:
        match_suite = suites.get_suite(suite)
        cases = match_suite.get("cases")
        name = match_suite.get("name")
        script_suite = match_suite.get("script_suite")
        automation_case = {}
        feature = match_suite.get("script_project")


        for script in script_suite:
            match_script = filter(lambda x : x["name"] == script, Al_robot_parser.get_testcases_list(feature, Al_robot.fetch_All_suite()[feature])["suites"])
            automation_case[script] = match_script[0]["tcs"]

        auto_case_html = "<table style=\"margin:1%; padding:1%;background:#EEEEEE; width:98%;border:1px solid black;\">"
        for script in automation_case.keys():
            auto_case_html += "<tr><th>Script: {}</th></tr>".format(script.replace(".robot", ""))
            for a_case in automation_case[script]:
                auto_case_html += "<tr><td style=\"border:1px solid black;\">{}</td></tr>".format(a_case.get("name"))
        auto_case_html += "</table>"

        case_html = "<table style=\"margin:1%; padding:1%;background:#EEEEEE; width:98%;border:1px solid black;\">"
        if cases is not None and len(cases) > 0:
            case_html += "<tr><th colspan=7 style=\"border:1px solid black;\">Manual Cases</th></tr>"
            case_html += "<tr><th style=\"border:1px solid black;\">{}</th>" \
                         "<th style=\"border:1px solid black;\">{}</th>" \
                         "<th style=\"border:1px solid black;\">{}</th>" \
                         "<th style=\"border:1px solid black;\">{}</th>" \
                         "<th colspan=3 style=\"border:1px solid black;\">{}</th></tr>".format("Case Id.", "Name", "Creator", "Created Date", "")
            for case in cases.keys():
                case_html += "<tr>"
                case_html += "<td style=\"border:1px solid black;\">{}</td>".format(case)
                case_html += "<td style=\"border:1px solid black;\">{}</td>".format(cases[case]["name"])
                case_html += "<td style=\"border:1px solid black;\">{}</td>".format(cases[case]["creator"])
                case_html += "<td style=\"border:1px solid black;\">{}</td>".format(cases[case]["created_date"])
                case_html += "<td style=\"border:1px solid black;\">" \
                             "<a style=\"text-decoration:none;\" target=_blank href=/PLAN?suite={}&case={}>" \
                             "open</a></td>".format(suite, case)
                case_html += "<td style=\"border:1px solid black;\">" \
                             "<button id=edit_case suite_id={} case_id={}>Edit</button></td>".format(suite, case)
                case_html += "<td style=\"border:1px solid black;\">" \
                             "<button id=del_case suite_id={} case_id={}>Delete</button></td>".format(suite, case)
                case_html += "</tr>"

        else:
            case_html += "<tr><th colspan=4>No Manual Cases</th></tr>"
        case_html += "</table>"

        table = "<div id=\"suites_block\" style=\"width:70%;float:left;margin:1% 2%;overflow-y:auto;background:#FFFFE0;height:80%;\">"
        table += "<h2>{}</h2>".format(name)
        table += auto_case_html
        table += case_html
        table += "</div>"
        dct["body$b2"] = table

        dct["body$b3"] = "<div style=\"width:20%;float:left;text-align:center;margin:1%;overflow-y:auto;background:#FFFFE0;height:80%;\">" \
                         "<h3 style=\"background:black;color:white;margin:1%;\">Future Scope</h3></div>"

        dct["body$b4"] = "<div style=\"width:94%;margin:1%;height:15%;\">" \
                         "<button style=\"padding:0.5% 1%;margin:0 1%;\" id=add_case>Add Test Case</button></div>"

    dct["body$b5"] = "<div id=load_message name=load_message></div>"
    return htmlstructure(**dct)

def form_suite():
    '''
    Return suite html form and project dict
    '''
    projects = meta.Test_Suite_Folder.keys()
    projects_dict = {}

    for project in projects:
        projects_dict[project] = Al_robot_parser.get_sub_suite(meta.Test_Suite_Folder[project]).values()
    table = "<div id=\"case_form\" style=\"width:40%;height:30%;\">" \
            "<table style=\"width:100%;\">"
    table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Suite Name </td>" \
             "<td style=\"width:60%;\"><input type=text id=suite_name style=\"width:auto;\"></td></tr>"
    table += "<tr><td> Automation projects </td><td><select id=selected_project>"
    for project in projects:
        table += "<option value={}>{}</option>".format(project, project)
    table += "</select></td></tr>"
    table += "<tr><td> Suite List </td><td> <select multiple=\"multiple\" id=select_suite></select></td></tr>"
    table += "<tr><td><button id=submit_suite> Add Suite </button></td>" \
             "<td><button id=cancel_form> Cancel </td></tr>"
    table += "</table></div>"

    return json.dumps({"form": table, "projects": projects_dict})

def form_case():
    '''
    Return case html form
    '''
    table = "<div id=\"case_form\" style=\"overflow-y:auto;\">" \
            "<table style=\"width:100%;\">"
    table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Case Name </td>" \
             "<td style=\"width:60%;\"><input type=text id=case_name style=\"width:auto;\"></td></tr>"
    table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Description </td>" \
             "<td style=\"width:60%;\"><textarea id=case_desc cols=30 rows=5></textarea></td></tr>"
    table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Steps </td>" \
             "<td style=\"width:60%;\"><textarea id=case_step cols=30 rows=5></textarea></td></tr>"
    table += "<tr><td><button id=submit_case> Add Case </button></td>" \
             "<td><button id=cancel_form> Cancel </td></tr>"
    table += "</table></div>"

    return json.dumps({"form": table})

@ensure_csrf_cookie
def suite_plan(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        if request.method == "GET":
            try:
                suite = request.GET["suite"]
            except Exception as e:
                suite = None
            return HttpResponse(init_all_suite(request.session.get("username"), suite=suite))
        elif request.method == "POST":
            try:
                action = request.POST["action"]
            except Exception as e:
                action = None
                logging.error(str(e))

            if action == "suite_form":
                return HttpResponse(form_suite())
            elif action == "case_form":
                return HttpResponse(form_case())
            elif action == "submit_suite_form":
                name = request.POST["name"]
                creator = request.session.get("username")
                project = request.POST["project"]
                if request.POST["suite_list"] == "":
                    suite_list = []
                else:
                    suite_list = request.POST["suite_list"].split(",")
                suites_manage = suite_manager(pool_1)
                return HttpResponse(suites_manage.add_suite(name, creator, suite_list, project))
            elif action == "submit_case_form":
                name = request.POST["name"]
                creator = request.session.get("username")
                desc = request.POST["desc"]
                steps = request.POST["steps"]
                suite = request.POST["suite"]
                suites_manage = suite_manager(pool_1)
                return HttpResponse(suites_manage.add_case(name, suite, creator, desc, steps))
            else:
                pass

        else:
            return HttpResponse(status=204)


@ensure_csrf_cookie
def test_plan(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        if request.method == "POST":
            date = str(time.time() * 1000)



@ensure_csrf_cookie
def suite_execution(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        if request.method == "POST":
            date = request.POST["date"]
            suite = request.POST["suite"]
            # create new instance of suite with S1000

            ## code here

        elif request.method == "PUT":
            instance_id = request.PUT["instance_id"]
            action = request.PUT["action"]
            if action == "update":
                tc = request.PUT["tc"]

                #update the run instance

                # code here

            elif action == "map_script_log":
                log_info = request.PUT["log"]

                #update the instance after after the script log

                # code here

            else:
                pass
                #future scope

        elif request.method == "GET":
            try:
                suite_id = request.GET["suite_id"]
            except Exception as e:
                suite_id = None
            if suite_id is None:
                # Get all the manual suite list with add, edit and delete controller
                pass
                # Code Here
            else:
                action = ""
        else:
            pass
            #future scope


@ensure_csrf_cookie
def test_execution(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        pass