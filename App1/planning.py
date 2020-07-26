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

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from App1.misc.rw_pool import rw_pool
from App1.misc.parse_xml import parse_for_test
from modelling.html_loader import htmlstructure
import App1.settings as meta
from App1.manual.man_manage import suite_manager
from App1.manual.man_execution import exec_manager
from App1.Robot_loader import Al_robot_parser
from App1.Robot_loader import Al_robot
from robot_runner.invoke import Invoke as Invoke

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
pool_1 = rw_pool(20, "App1/all_manual.json")

header = "<div id=header name=header><h2 style=\"width:50%;padding:1%;text-align:left;float:left;\">" \
         "Robotframework Front End</h2><table style='padding:1%;float:right;color:white;'><tr>" \
         "<td><button><a style=\"text-decoration:none;\" href=\"/RFE\">Robot Automation</a></button></td>" \
         "<td><button><a style=\"text-decoration:none;\" href=\"/PLAN\">Test Planning</a></button></td>" \
         "<td><button><a style=\"text-decoration:none;\" href=\"/EXEC\">Test Execution</a></button></td>" \
         "<td>{}</td>" \
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
            edit_btn = "<button class=edit_suite suite_id={}>Edit</button>".format(li)
            del_btn = "<button class=del_suite suite_id={}>Delete</button>".format(li)
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
                             "<button class=edit_case suite_id={} case_id={}>Edit</button></td>".format(suite, case)
                case_html += "<td style=\"border:1px solid black;\">" \
                             "<button class=del_case suite_id={} case_id={}>Delete</button></td>".format(suite, case)
                case_html += "</tr>"

        else:
            case_html += "<tr><th colspan=4>No Manual Cases</th></tr>"
        case_html += "</table>"

        table = "<div id=\"suites_block\" style=\"width:70%;float:left;margin:1% 2%;background:#FFFFE0;height:80%;\">"
        table += "<h2>{}</h2>".format(name)
        table += "<div style=\"overflow-y:auto;height:90%;\">"
        table += auto_case_html
        table += case_html
        table += "</div></div>"
        dct["body$b2"] = table

        dct["body$b3"] = "<div style=\"width:20%;float:left;text-align:center;margin:1%;overflow-y:auto;background:#FFFFE0;height:80%;\">" \
                         "<h3 style=\"background:black;color:white;margin:1%;\">Future Scope</h3></div>"

        dct["body$b4"] = "<div style=\"width:94%;margin:1%;height:15%;\">" \
                         "<button style=\"padding:0.5% 1%;margin:0 1%;\" id=add_case>Add Test Case</button>" \
                         "<button style=\"padding:0.5% 1%;margin:0 1%;\" suite_id={} id=exec_suite>" \
                         "Execute Suite</button></div>".format(suite)

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


def edit_form(suite, case=None):
    '''
    Return edit form
    '''
    suites = suite_manager(pool_1)
    match_suite = suites.get_suite(suite)
    if case is None:
        projects = meta.Test_Suite_Folder.keys()
        projects_dict = {}

        for project in projects:
            projects_dict[project] = Al_robot_parser.get_sub_suite(meta.Test_Suite_Folder[project]).values()
        table = "<div id=\"edit_suite_form\" style=\"width:40%;height:30%;\">" \
                "<table style=\"width:100%;\">"
        table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Suite Name </td>" \
                 "<td style=\"width:60%;\">" \
                 "<input type=text id=suite_name style=\"width:auto;\" value=\"{}\"></td></tr>".format(match_suite["name"])
        table += "<tr><td> Automation projects </td><td><select id=selected_project>"
        for project in projects:
            if match_suite.get("script_project") is not None and match_suite["script_project"] == project:
                table += "<option selected value={}>{}</option>".format(project, project)
            else:
                table += "<option value={}>{}</option>".format(project, project)
        table += "</select></td></tr>"
        table += "<tr><td> Suite List </td><td> <select multiple=\"multiple\" id=select_suite></select></td></tr>"
        table += "<tr><td><button suite_id={} id=update_suite> Update Suite </button></td>" \
                 "<td><button id=cancel_form> Cancel </td></tr>".format(suite)
        table += "</table></div>"

        return json.dumps({"form": table, "projects": projects_dict})
    else:
        match_case = match_suite.get("cases")[case]
        table = "<div id=\"case_form\" style=\"overflow-y:auto;\">" \
                "<table style=\"width:100%;\">"
        table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Case Name </td>" \
                 "<td style=\"width:60%;\"><input type=text id=case_name style=\"width:auto;\" value=\"{}\"></td></tr>"\
            .format(match_case["name"])
        table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Description </td>" \
                 "<td style=\"width:60%;\"><textarea id=case_desc cols=30 rows=5>{}</textarea></td></tr>"\
            .format(match_case["description"])
        table += "<tr style=\"background:#2f4f4f;color:white;\"><td style=\"width:40%;\">Steps </td>" \
                 "<td style=\"width:60%;\"><textarea id=case_step cols=30 rows=5>{}</textarea></td></tr>"\
            .format(match_case["scenario"])
        table += "<tr><td><button id=update_case suite_id={} case_id={}> Update Case </button></td>" \
                 "<td><button id=cancel_form> Cancel </td></tr>".format(suite, case)
        table += "</table></div>"

        return json.dumps({"form": table})


def instantiate_suite(username, suite):
    suites_manage = suite_manager(pool_1)
    match_suite = suites_manage.get_suite(suite)
    feature = match_suite.get("script_project")
    script_suite = match_suite.get("script_suite")
    automation_case = {}

    for script in script_suite:
        match_script = filter(lambda x: x["name"] == script, Al_robot_parser.
                              get_testcases_list(feature, Al_robot.fetch_All_suite()[feature])["suites"])
        automation_case[script] = match_script[0]["tcs"]

    exec_manage = exec_manager(pool_1)
    return exec_manage.instantiate(username, manual=match_suite, automation=automation_case)


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

            elif action == "edit_suite_form":
                suite = request.POST["suite"]
                return HttpResponse(edit_form(suite))

            elif action == "edit_case_form":
                suite = request.POST["suite"]
                case = request.POST["case"]
                return HttpResponse(edit_form(suite, case))

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

            elif action == "update_suite":
                name = request.POST["name"]
                creator = request.session.get("username")
                suite = request.POST["suite"]
                project = request.POST["project"]
                if request.POST["suite_list"] == "":
                    suite_list = None
                else:
                    suite_list = request.POST["suite_list"].split(",")
                suites_manage = suite_manager(pool_1)
                return HttpResponse(suites_manage.update_suite(suite, name, creator, suite_list, project))

            elif action == "update_case":
                name = request.POST["name"]
                creator = request.session.get("username")
                desc = request.POST["desc"]
                steps = request.POST["steps"]
                suite = request.POST["suite"]
                case = request.POST["case"]
                suites_manage = suite_manager(pool_1)
                return HttpResponse(suites_manage.update_case(name, suite, case, creator, desc, steps))

            elif action == "del_suite":
                suite = request.POST["suite"]
                suites_manage = suite_manager(pool_1)
                return HttpResponse(suites_manage.del_suite(suite))

            elif action == "del_case":
                suite = request.POST["suite"]
                case = request.POST["case"]
                suites_manage = suite_manager(pool_1)
                return HttpResponse(suites_manage.del_case(suite, case))

            elif action == "instantiate_suite":
                suite = request.POST["suite"]
                return HttpResponse(instantiate_suite(request.session.get("username"), suite))
            else:
                return HttpResponse(status=404)

        else:
            return HttpResponse(status=204)


def format_select_case_result(select, suite, case, _type, script=0):
    if select == "passed":
        status_select = "<select class=result_exec es_id={} case_id={} type={} script={}><option value=passed selected=selected>passed</option>" \
                        "<option value=failed>failed</option>" \
                        "<option value=not_tested>not tested</option></select>".format(suite, case, _type, script)
    elif select == "failed":
        status_select = "<select class=result_exec es_id={} case_id={} type={} script={}><option value=passed>passed</option>" \
                        "<option value=failed selected=selected>failed</option>" \
                        "<option value=not_tested>not tested</option></select>".format(suite, case, _type, script)
    else:
        status_select = "<select class=result_exec es_id={} case_id={} type={} script={}><option value=passed>passed</option>" \
                        "<option value=failed>failed</option>" \
                        "<option value=not_tested  selected=selected>not tested</option></select>".format(suite, case, _type, script)
    return status_select


def log_map_form(suite, project, script):
    runner = Invoke(track='App1/robot_runner/track.json',
                    result_dir=os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT"))
    logs = runner.fetch_history(feature=project, suite=script, tc=None)

    if logs is not None:
        html = "<div><table>"
        for log in logs:
            html += "<tr><td><button class=map_log es_id={} proj={} script={} time=\"{}\">{}</button></td></tr>"\
                .format(suite, project, script, log["time"], log["time"])
        html += "<tr><td><button id=cancel>cancel</button></td></tr>"
        html += "</table></div>"
    else:
        html = "<div><table><tr><td>No log</td></tr><tr><td><button id=cancel>cancel</button></td></tr></div>"
    return json.dumps({"form": html})


def init_execution(username, suite):
    suites = exec_manager(pool_1)

    dct = {
        "body$b1": header.format(username),
        "script$s1": "../static/jquery.min.js",
        "script$s2": "static/he.js",
        "style$t1": "../static/plan.css",
        "bscript$s1": "../static/exec.js",
        "headrawmeta$m1": "<title>execution</title>"
    }
    if suite is None:
        all_suite = suites.get_suites()
        suites_list = all_suite.keys()
        if suites_list is not None or len(suites_list) > 0:
            html = "<div id=\"suites_block\" style=\"width:70%;float:left;margin:1% 2%;overflow-y:auto;background:#FFFFE0;height:80%;\">"
            html += "<table style=\"width:100%;\"><tr style=\"background:#2f4f4f;color:white;\">" \
                    "<th>{}</th><th>{}</th><th>{}</th><th colspan=2>{}</th></tr><tbody>"\
                .format("Id.", "Name", "Creator", "")
            for s in suites_list:
                html += "<tr style=\"background:lightgrey;\"><td>{}</td><td>{}</td><td>{}</td><td>" \
                        "<a href=\"/EXEC?es_id={}\" target=_blank>open</a></td>" \
                        "<td><button class=delete es_id={}>delete</button></td></tr>"\
                    .format(s, all_suite[s]["name"], all_suite[s]["creator"], s, s)
            html += "</tbody></table></div>"
            dct["body$b2"] = html
        else:
            dct["body$b2"] = "<div>No suite in execution</div>"
    else:
        match_suite = suites.get_suite(suite)
        html = "<div id=\"suites_block\" style=\"width:70%;float:left;margin:1% 2%;overflow-y:auto;background:#FFFFE0;height:80%;\">"
        html += "<table style=\"width:100%;\"><tr style=\"background:black;color:white;\">" \
                "<th colspan=3>{}</th></tr><tbody>".format(match_suite["name"])
        html += "<tr style=\"background:#2f4f4f;color:white;\"><th style=\"width:15%;\">{}</th><th>{}</th><th style=\"width:15%;\">{}</th></tr>"\
            .format("Id.", "Case", "Status")
        for case in match_suite["m_cases"].keys():
            html += "<tr style=\"background:lightgrey;\"><td>{}</td><td>{}</td><td>{}</td></tr>"\
                .format(case, match_suite["m_cases"][case]["name"],
                        format_select_case_result(match_suite["m_cases"][case]["result"], suite, case, "m"))
        for script in match_suite["a_cases"].keys():
            html += "<tr style=\"background:lightgrey;\"><th colspan=3>{} :: " \
                    "<button class=map_log_form es_id={} script={}>map log</button></th> " \
                .format(script.replace(".robot", ""), suite, script)
            for case in match_suite["a_cases"][script].keys():
                html += "<tr style=\"background:lightgrey;\"><td>{}</td><td>{}</td><td>{}</td></tr>" \
                    .format(case, match_suite["a_cases"][script][case]["name"],
                            format_select_case_result(match_suite["a_cases"][script][case]["result"], suite, case, "a", script))
        html += "</tbody></table></div>"
        dct["body$b2"] = html

    dct["body$b3"] = "<div style=\"width:20%;float:left;text-align:center;margin:1%;overflow-y:auto;background:#FFFFE0;height:80%;\">" \
                     "<h3 style=\"background:black;color:white;margin:1%;\">Future Scope</h3></div>"
    dct["body$b5"] = "<div id=load_message name=load_message></div>"
    return htmlstructure(**dct)


def map_log(suite, script, project, _time):
    runner = Invoke(track='App1/robot_runner/track.json',
                    result_dir=os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT"))
    logs = runner.fetch_history(feature=project, suite=script, tc=None)
    for log in logs:
        if log["time"] == _time:
            xml = log["xml"]
    case_status = parse_for_test(xml)
    exec_manage = exec_manager(pool_1)
    return exec_manage.map_log(suite, script, case_status)


@ensure_csrf_cookie
def suite_execution(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        if request.method == "GET":
            try:
                suite = request.GET["es_id"]
            except Exception as e:
                suite = None
            return HttpResponse(init_execution(request.session.get("username"), suite))

        elif request.method == "POST":
            try:
                action = request.POST["action"]
            except Exception as e:
                action = None
                logging.error(str(e))

            if action == "update_case":
                suite = request.POST["suite"]
                case = request.POST["case"]
                status = request.POST["status"]
                script = request.POST["script"]
                _type = request.POST["type"]
                exec_manage = exec_manager(pool_1)
                return HttpResponse(exec_manage.update_case(request.session.get("username"), suite, case, status, _type, script))

            elif action == "map_log_form":
                suite = request.POST["suite"]
                script = request.POST["script"]
                project = exec_manager(pool_1).get_suite(suite)["script_project"]
                return HttpResponse(log_map_form(suite, project, script))

            elif action == "map_log":
                suite = request.POST["suite"]
                script = request.POST["script"]
                project = request.POST["project"]
                _time = request.POST["time"]

                return HttpResponse(map_log(suite, script, project, _time))
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)
