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
import logging
import time

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from App1.misc.rw_pool import rw_pool
from modelling.HTMLLoader import htmlstructure
import App1.settings as meta
from App1.manual.man_manage import suite_manager

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
pool_1 = rw_pool(20, "App1/all_manual.json")

def init_suite(username, suite):

    suites = suite_manager(pool_1)

    suite_detail = suites.get_suites()

    dct = {
        "body$b1": "<div id=header name=header><h2 style=\"width:98%;padding:1%;text-align:left;\">"
                   "Robotframework Front End</h2></div>",
        "script$s1": "../static/jquery.min.js",
        "script$s2": "../static/plan.js",
        "style$t1": "../static/plan.css",
        "headrawmeta$m1": "<title>suites</title>"
    }
    return htmlstructure(**dct)

@ensure_csrf_cookie
def suite_plan(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        if request.method == "GET":
            try:
                suite = request.GET["suite"]
            except ValueError as e:
                suite = None
            return HttpResponse(init_suite(request.session.get("username"), suite=suite))
        elif request.method == "POST":
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