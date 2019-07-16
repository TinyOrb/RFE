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
import re
import App1.settings as meta

Test_Suite_Folder = meta.Test_Suite_Folder


def list_robot_files(path):
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(f)]
        wkd = os.path.dirname(os.path.realpath(__file__))
        robot_file = re.compile("^[a-zA-Z0-9_-]+.robot$")
        l = []
        count = 1
        for f in files:
            if robot_file.match(f) is not None:
                count = count + 1
                l.append(f)
        return l
    except Exception as e:
        return "Error! " + str(e)


def list_variable_files(path):
    try:
        files = os.listdir(path)
        variable_file = re.compile("^[a-zA-Z0-9_-]+.py$")
        vl = []
        for f in files:
            if variable_file.match(f) is not None:
                vl.append(f)
        return vl
    except Exception as e:
        return "Error! " + str(e)


def fetch_All_suite():
    try:
        l = len(Test_Suite_Folder)
        return Test_Suite_Folder
    except Exception as e:
        return "Error! " + str(e)


def fetch_suite_test_cases(suite):
    try:
        path = Test_Suite_Folder[suite]
    except Exception as e:
        return "Error! " + str(e)


def fetch_suite_content(path):
    try:
        pass
    except Exception as e:
        return "Error! " + str(e)


def update_test_suite(path, content):
    try:
        pass
    except Exception as e:
        return "Error! " + str(e)


def execute_scenarios(path, cases):
    try:
        pass
    except Exception as e:
        return "Error! " + str(e)
