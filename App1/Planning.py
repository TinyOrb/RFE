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
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie

import urllib

import App1.settings as meta

@ensure_csrf_cookie
def suite_manager(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        access_project = meta.user_list["project_access"]
        if request.method == "POST":
            # create suite
            pass
        elif request.method == "PUT":
            # update suite information
            pass
        elif request.method == "GET":
            # fetch the suite information
            action = request.GET["action"]
            if action == "load":
                # Get initial html load
                try:
                    suite = request.GET["suite"]
                except Exception as e:
                    suite = None
                if suite is None:
                    # if suite load all manual suite
                    pass
                else:


def test_instance(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        action = request.request["action"]
        date = request.POST["date"]
        suite_list = request.POST["suite_list"]


def manage_manual(request):
    if request.session.get("username") is None:
        return redirect("/expire")
    else:
        suite_list = request.POST["suite_list"]