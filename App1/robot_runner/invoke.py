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

import subprocess
import json
import datetime
import time
import os
import signal
import threading
from sys import platform

import App1.Robot_loader.Al_robot as Al_robot


class Invoke:

    # Every key represent instance of running suite which is thread
    # Life cycle of thread Start -> Running -> Abort -> Aborted -> Done or Start -> Running -> Done
    thread_list = {}

    def __init__(self, track, result_dir, process_pool):
        self.track = track
        self.result_dir = result_dir
        self.cd_path = None
        self.Python_Path = None
        self.process_pool = process_pool

    def read_process_id(self):
        thread_id = self.process_pool.action("read")
        for iter in range(10):
            result = self.process_pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
                data = result.values()
                self.process_pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def write_process_id(self):
        thread_id = self.process_pool.action("write", data=self.thread_list)
        for iter in range(10):
            result = self.process_pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
                self.process_pool.remove_thread_buffer(thread_id)
                return True
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def trigger(self, feature, suite=None, tc=None, variable=None, variablefile=None, include_tags=None,
                exclude_tags=None):
        try:
            with open(self.track) as json_file:
                data = json.load(json_file)

            if not self.ensure_path(self.result_dir):
                return "Fail"
            else:
                self.ensure_data_set(data, feature, suite, tc)

                with open(self.track, 'w') as outfile:
                    json.dump(data, outfile)

            if tc is not None:
                current_state = self.fetch_current(feature, suite, tc)
                if len(current_state) != 0:
                    self.update_history(current_state, feature, suite, tc)

                current_state["status"] = "not started"
                cur_time = str(datetime.datetime.now())
                cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
                current_state["time"] = cur_time1
                current_state["dir"] = os.path.join(
                    os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite), tc),
                    cur_time1.replace(":", "-"))
                current_state["script_output"] = os.path.join(current_state["dir"], "script.txt")
                current_state["log"] = os.path.join(current_state["dir"], "log.html")
                current_state["output"] = os.path.join(current_state["dir"], "report.html")
                current_state["xml"] = os.path.join(current_state["dir"], "output.xml")
                current_state["cmd"] = "python -m robot "
                if include_tags is not None:
                    current_state["cmd"] += "--include \"%s\" " % include_tags
                if exclude_tags is not None:
                    current_state["cmd"] += "--exclude \"%s\" " % exclude_tags
                if variable is not None:
                    current_state["cmd"] += "--variable==\"%s\" " % variable
                if variablefile is not None:
                    current_state["cmd"] += "--variablefile=\"%s\" " % variablefile
                current_state["cmd"] += "--outputdir \"%s\" " % current_state["dir"]
                current_state["cmd"] += "-t \"%s\" " % tc
                current_state["cmd"] += os.path.join(Al_robot.fetch_All_suite()[feature], suite)

                self.update_current(current_state, feature, suite, tc)

            elif suite is not None:
                current_state = self.fetch_current(feature, suite, tc)
                if len(current_state) != 0:
                    self.update_history(current_state, feature, suite, tc)

                current_state["status"] = "not started"
                cur_time = str(datetime.datetime.now())
                cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
                current_state["time"] = cur_time1
                current_state["dir"] = os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite),
                                                    cur_time1.replace(":", "-"))
                current_state["script_output"] = os.path.join(current_state["dir"], "script.txt")
                current_state["log"] = os.path.join(current_state["dir"], "log.html")
                current_state["output"] = os.path.join(current_state["dir"], "report.html")
                current_state["xml"] = os.path.join(current_state["dir"], "output.xml")
                current_state["cmd"] = "python -m robot "
                if include_tags is not None:
                    current_state["cmd"] += "--include \"%s\" " % include_tags
                if exclude_tags is not None:
                    current_state["cmd"] += "--exclude \"%s\" " % exclude_tags
                if variable is not None:
                    current_state["cmd"] += "--variable==\"%s\" " % variable
                if variablefile is not None:
                    current_state["cmd"] += "--variablefile=\"%s\" " % variablefile
                current_state["cmd"] += "--outputdir \"%s\" " % current_state["dir"]
                current_state["cmd"] += os.path.join(Al_robot.fetch_All_suite()[feature], suite)
                self.update_current(current_state, feature, suite, tc)

            elif feature is not None:
                current_state = self.fetch_current(feature, suite, tc)
                if len(current_state) != 0:
                    self.update_history(current_state, feature, suite, tc)

                current_state["status"] = "not started"
                cur_time = str(datetime.datetime.now())
                cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
                current_state["time"] = cur_time1
                current_state["dir"] = os.path.join(os.path.join(self.result_dir, feature), cur_time1.replace(":", "-"))
                current_state["script_output"] = os.path.join(current_state["dir"], "script.txt")
                current_state["log"] = os.path.join(current_state["dir"], "log.html")
                current_state["output"] = os.path.join(current_state["dir"], "report.html")
                current_state["xml"] = os.path.join(current_state["dir"], "output.xml")
                current_state["cmd"] = "python -m robot "
                if include_tags is not None:
                    current_state["cmd"] += "--include \"%s\" " % include_tags
                if exclude_tags is not None:
                    current_state["cmd"] += "--exclude \"%s\" " % exclude_tags
                if variable is not None:
                    current_state["cmd"] += "--variable==\"%s\" " % variable
                if variablefile is not None:
                    current_state["cmd"] += "--variablefile=\"%s\" " % variablefile
                current_state["cmd"] += "--outputdir \"%s\" " % current_state["dir"]
                current_state["cmd"] += Al_robot.fetch_All_suite()[feature]
                self.update_current(current_state, feature, suite, tc)

            else:
                print("No enough input provided")
                return "Fail"
            if self.thread_list.get("%s_%s_%s" % (feature, "" if suite is None else suite,
                                                  "" if tc is None else tc)) is None or \
                    self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                                   "" if tc is None else tc)]["status"] == "Done":
                print("Main    : before creating thread")
                self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] \
                    = {"status": "Start"}
                x = threading.Thread(target=self.run, args=(current_state, feature, suite, tc,))
                print("Main    : before running thread")
                x.start()
            return "Success"
        except Exception as e:
            print("Exception occur %s" % str(e))
            return "Fail"

    def abort_run(self, feature, suite=None, tc=None):
        try:
            if self.thread_list.get(
                    "%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)) is None:
                print("No tracked process")
                current = self.fetch_current(feature, suite, tc)
                current["status"] = "unknown"
                self.update_current(current, feature, suite, tc)
                return "success"
            elif self.thread_list[
                    "%s_%s_%s" % (feature, "" if suite is None else suite,
                                  "" if tc is None else tc)]["status"] == "Aborted" or self.thread_list[
                    "%s_%s_%s" % (feature, "" if suite is None else suite,
                                  "" if tc is None else tc)]["status"] == "Done":
                print("Process is finished already")
                return "success"
            else:
                self.thread_list[
                    "%s_%s_%s" % (feature, "" if suite is None else suite,
                                  "" if tc is None else tc)]["status"] = "Abort"
                print("Mark process abortion")
                return "success"
        except Exception as e:
            print("Exception occurred %s" % str(e))
            return "fail"

    def get_run_state(self, stack_json):
        print("Fetching query")
        try:
            with open(self.track) as json_file:
                data = json.load(json_file)

            feature = stack_json["feature"]

            d_feature = None
            for f in data["features"]:
                if f["name"] == feature:
                    d_feature = f

            if d_feature is not None:
                for suite in stack_json["suites"]:
                    s_flag = 0
                    for d_suite in d_feature["suites"]:
                        if d_suite["name"] == suite["name"]:
                            s_flag = 1
                            if d_suite["current_status"].get("status") is not None and d_suite["current_status"].get(
                                    "status").lower() == "running":
                                suite["status"] = "Running"
                            else:
                                suite["status"] = "Run"
                            for tc in suite["tcs"]:
                                t_flag = 0
                                for d_tc in d_suite["tcs"]:
                                    if tc["name"] == d_tc["name"]:
                                        t_flag = 1
                                        if d_tc["current_status"].get("status") is not None and d_tc[
                                            "current_status"].get("status").lower() == "running":
                                            tc["status"] = "Running"
                                        else:
                                            tc["status"] = "Run"
                                        break
                                if t_flag == 0:
                                    tc["status"] = "Run"
                            break
                    if s_flag == 0:
                        suite["status"] = "Run"
                        for tc in suite["tcs"]:
                            tc["status"] = "Run"

            else:
                for suite in stack_json["suites"]:
                    suite["status"] = "Run"
                    for tc in suite["tcs"]:
                        tc["status"] = "Run"
        except Exception as e:
            print("Exception occur %s" % str(e))

        return stack_json

    def fetch_history(self, feature, suite=None, tc=None):
        print("Fetching query")
        with open(self.track) as json_file:
            data = json.load(json_file)
        flag = 0
        status = None
        for data_feature in data["features"]:
            if data_feature["name"] == feature:
                if suite is not None:
                    for data_suite in data_feature["suites"]:
                        if data_suite["name"] == suite:
                            if tc is not None:
                                for data_tc in data_suite["tcs"]:
                                    if data_tc["name"].strip() == tc.strip():
                                        flag = 1
                                        status = data_tc["history_status"]
                            else:
                                flag = 2
                                status = data_suite["history_status"]
                else:
                    flag = 3
                    status = data_feature["history_status"]
        if flag == 0:
            print("query failed")
        elif flag == 1 or flag == 2 or flag == 3:
            print("data fetch successfully")
        else:
            print("unknown query")
        return status

    def fetch_current(self, feature, suite=None, tc=None):
        print("Fetching query")
        with open(self.track) as json_file:
            data = json.load(json_file)
        flag = 0
        status = None
        for data_feature in data["features"]:
            if data_feature["name"] == feature:
                if suite is not None:
                    for data_suite in data_feature["suites"]:
                        if data_suite["name"] == suite:
                            if tc is not None:
                                for data_tc in data_suite["tcs"]:
                                    if data_tc["name"].strip() == tc.strip():
                                        flag = 1
                                        status = data_tc["current_status"]
                            else:
                                flag = 2
                                status = data_suite["current_status"]
                else:
                    flag = 3
                    status = data_feature["current_status"]
        if flag == 0:
            print("query failed")
        elif flag == 1 or flag == 2 or flag == 3:
            print("data fetch successfully")
        else:
            print("unknown query")
        return status

    def update_history(self, current_status, feature, suite=None, tc=None):
        print("Updating status")
        with open(self.track) as json_file:
            data = json.load(json_file)

        flag = 0

        for data_feature in data["features"]:
            if data_feature["name"] == feature:
                if suite is not None:
                    for data_suite in data_feature["suites"]:
                        if data_suite["name"] == suite:
                            if tc is not None:
                                for data_tc in data_suite["tcs"]:
                                    if data_tc["name"] == tc:
                                        data_tc["history_status"].append(current_status)
                                        flag = 1
                            else:
                                data_suite["history_status"].append(current_status)
                                flag = 2
                else:
                    data_feature["history_status"].append(current_status)
                    flag = 3

        if flag == 0:
            print("Insertion failed")
            return False
        elif flag == 1 or flag == 2 or flag == 3:
            try:
                with open(self.track, 'w') as outfile:
                    json.dump(data, outfile)
                print("Insertion success")
                return True
            except:
                print("Unknown exception")
        else:
            print("Unknown state")
            return False

    def update_current(self, current_status, feature, suite=None, tc=None):
        print("Updating status")
        with open(self.track) as json_file:
            data = json.load(json_file)
        flag = 0
        for data_feature in data["features"]:
            if data_feature["name"] == feature:
                if suite is not None:
                    for data_suite in data_feature["suites"]:
                        if data_suite["name"] == suite:
                            if tc is not None:
                                for data_tc in data_suite["tcs"]:
                                    if data_tc["name"] == tc:
                                        data_tc["current_status"] = current_status
                                        flag = 1
                            else:
                                data_suite["current_status"] = current_status
                                flag = 2
                else:
                    data_feature["current_status"] = current_status
                    flag = 3

        if flag == 0:
            print("Insertion failed")
            return False
        elif flag == 1 or flag == 2 or flag == 3:
            try:
                with open(self.track, 'w') as outfile:
                    json.dump(data, outfile)
                print("Insertion success")
                return True
            except:
                print("Unknown exception")
        else:
            print("Unknown state")
            return False

    def run(self, current_state, feature, suite, tc):
        if platform == "linux" or platform == "linux2":
            envs = self.Python_Path
            path_cmd = ""
            for env in envs.keys():
                path_cmd = "%s export %s=$%s" % (path_cmd, env, env)
                for path in envs[env]:
                    path_cmd = "%s:%s" % (path_cmd, path)
                path_cmd = "%s;" % path_cmd
            if not self.ensure_path(current_state["script_output"], type="file"):
                print("Failed to create script output file")
                return False
            with open(self.normal_path(current_state["script_output"]), "wb") as out:
                if self.cd_path is None:
                    cmd = "%s echo start of script output; %s ; echo end of script output " % \
                          (path_cmd, current_state["cmd"])
                    process = subprocess.Popen([cmd], stdout=out, stderr=out,
                                               shell=True, preexec_fn=os.setsid)

                else:
                    cmd = "%s echo start of script output; %s ; echo end of script output " % \
                          (path_cmd, current_state["cmd"])
                    process = subprocess.Popen([cmd], stdout=out, stderr=out,
                                               shell=True, cwd=self.cd_path, preexec_fn=os.setsid)

            current_state["status"] = "running"
            self.update_current(current_state, feature, suite, tc)
            self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] \
                = {"status": "Running", "cmd": cmd, "pid": process.pid}
            line = self.get_last_line(self.normal_path(current_state["script_output"]))

            while "end of script output" not in str(line):
                print(self.thread_list)
                if self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                                  "" if tc is None else tc)]["status"] == "Abort":
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    process.kill()
                    current_state["status"] = "aborted"

                    with open(self.normal_path(current_state["script_output"]), "a") as out:
                        subprocess.Popen("echo Script aborted!;", stdout=out, stderr=out, shell=True)
                    self.update_current(current_state, feature, suite, tc)
                    self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                                   "" if tc is None else tc)]["status"] = "Aborted"
                    print("Thread ended: %s_%s_%s" % (feature,
                                                      "" if suite is None else suite, "" if tc is None else tc))
                    break
                time.sleep(1)
                line = self.get_last_line(self.normal_path(current_state["script_output"]))

            current_state["status"] = "done"
            cur_time = str(datetime.datetime.now())
            cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
            current_state["end_time"] = cur_time1
            self.update_current(current_state, feature, suite, tc)
            self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                           "" if tc is None else tc)]["status"] = "Done"
            print("Thread ended: %s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc))
            return True

        elif platform == "win32":
            envs = self.Python_Path
            path_cmd = ""
            for env in envs.keys():
                path_cmd = "%s set %s=$%s" % (path_cmd, env, env)
                for path in envs[env]:
                    path_cmd = "%s:%s" % (path_cmd, path)
                path_cmd = "%s;" % path_cmd
            if not self.ensure_path(current_state["script_output"], type="file"):
                print("Failed to create script output file")
                return False
            with open(self.normal_path(current_state["script_output"]), "wb") as out:
                cmd = "%s echo start of script output & %s & echo end of script output " %\
                      (path_cmd, current_state["cmd"])
                process = subprocess.Popen(cmd, stdout=out, stderr=out, shell=True)

            current_state["status"] = "running"
            self.update_current(current_state, feature, suite, tc)
            self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] \
                = {"status": "Running", "cmd": cmd, "pid": process.pid}
            line = self.get_last_line(self.normal_path(current_state["script_output"]))

            while "end of script output" not in str(line):
                if self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                                  "" if tc is None else tc)]["status"] == "Abort":
                    process.kill()
                    process.terminate()
                    os.kill(process.pid, signal.CTRL_C_EVENT)
                    current_state["status"] = "aborted"
                    with open(self.normal_path(current_state["script_output"]), "a") as out:
                        subprocess.Popen("echo Script aborted!;", stdout=out, stderr=out, shell=True)
                    self.update_current(current_state, feature, suite, tc)
                    self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                                   "" if tc is None else tc)]["status"] = "Aborted"
                    print("Thread ended: %s_%s_%s" % (feature, "" if suite is None else suite,
                                                      "" if tc is None else tc))
                    break
                time.sleep(1)
                line = self.get_last_line(self.normal_path(current_state["script_output"]))

            current_state["status"] = "done"
            cur_time = str(datetime.datetime.now())
            cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
            current_state["end_time"] = cur_time1
            self.update_current(current_state, feature, suite, tc)
            self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite,
                                           "" if tc is None else tc)]["status"] = "Done"
            print("Thread ended: %s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc))
            return True

        elif platform == "darwin":
            return False
        else:
            return False

    def keep_eye(self, current_state, feature, suite, tc):
        if platform == "linux" or platform == "linux2":
            pass
        elif platform == "darwin":
            return False
        else:
            return False

    def normal_path(self, path):
        if platform == "linux" or platform == "linux2":
            pass
        elif platform == "darwin":
            pass
        elif platform == "win32":
            path = os.path.normpath(path)
        return path

    def get_last_line(self, path):
        try:
            with open(path) as f:
                data = f.readlines()
            lastline = data[-1]
            return lastline
        except Exception as e:
            print("Exception occured as %s" % str(e))
            return ""

    def ensure_path(self, path, type="dir"):
        try:
            if platform == "linux" or platform == "linux2":
                pass
            elif platform == "darwin":
                pass
            elif platform == "win32":
                path = os.path.normpath(path)

            if type == "dir":
                if not os.path.exists(path):
                    os.makedirs(path)
                else:
                    print("Directory all ready exist")
            elif type == "file":
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                else:
                    print("Directory all ready exist")
            return True
        except Exception as e:
            print("Some unknown error occured: %s" % str(e))
            return False

    def fetch_detail_traverse_data(self, data, feature, suite, tc):
        detail = {"feature": None, "suite": None, "tc": None}

        try:
            for data_feature in data["features"]:
                if feature == data_feature["name"]:
                    detail["feature"] = feature

                    if suite is not None:
                        for data_suite in data_feature["suites"]:
                            if suite == data_suite["name"]:
                                detail["suite"] = suite

                                if tc is not None:
                                    for data_tc in data_suite["tcs"]:
                                        if tc == data_tc["name"]:
                                            detail["tc"] = tc
        except Exception as e:
            print("Exception occurs %s" % str(e))

        return detail

    def ensure_data_set(self, data, feature, suite, tc):
        current_data_set = self.fetch_detail_traverse_data(data, feature, suite, tc)

        if current_data_set["feature"] is not None:
            if suite is None:
                print("Data set already exist")
            else:
                if current_data_set["suite"] is not None:
                    if tc is None:
                        print("Data set already exist")
                    else:
                        if current_data_set["tc"] is not None:
                            print("Data set already exist")
                        else:
                            print("Preparing test case data set")
                            d_tc = dict()
                            d_tc["name"] = tc
                            d_tc["id"] = data["tc_count"] + 1
                            d_tc["dir"] = os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite), tc)
                            d_tc["current_status"] = {}
                            d_tc["history_status"] = []
                            print("Inserting test case data set")
                            self.insert_data_set(data, feature, suite, TC=d_tc)
                            print("Insertion completed")
                else:
                    print("Preparing suite data set")
                    d_suite = dict()
                    d_suite["name"] = suite
                    d_suite["id"] = data["suite_count"] + 1
                    d_suite["dir"] = os.path.join(os.path.join(self.result_dir, feature), suite)
                    d_suite["current_status"] = {}
                    d_suite["history_status"] = []
                    d_suite["tcs"] = []
                    print("Inserting suite data set")
                    self.insert_data_set(data, feature, suite, SUITE=d_suite)
                    print("Insertion completed")
                    if tc is not None:
                        print("Preparing test case data set")
                        d_tc = dict()
                        d_tc["name"] = tc
                        d_tc["id"] = data["tc_count"] + 1
                        d_tc["dir"] = os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite), tc)
                        d_tc["current_status"] = {}
                        d_tc["history_status"] = []
                        print("Inserting test case data set")
                        self.insert_data_set(data, feature, suite, TC=d_tc)
                        print("Insertion completed")
        else:
            print("Preparing feature data set")
            d_feature = dict()
            d_feature["name"] = feature
            d_feature["id"] = data["feature_count"] + 1
            d_feature["dir"] = os.path.join(self.result_dir, feature)
            d_feature["current_status"] = {}
            d_feature["history_status"] = []
            d_feature["suites"] = []
            print("Inserting feature data set")
            self.insert_data_set(data, feature, suite, FEATURE=d_feature)
            print("Insertion completed")
            if suite is not None:
                print("Preparing suite data set")
                d_suite = dict()
                d_suite["name"] = suite
                d_suite["id"] = data["suite_count"] + 1
                d_suite["dir"] = os.path.join(os.path.join(self.result_dir, feature), suite)
                d_suite["current_status"] = {}
                d_suite["history_status"] = []
                d_suite["tcs"] = []
                print("Inserting suite data set")
                self.insert_data_set(data, feature, suite, SUITE=d_suite)
                print("Insertion completed")
                if tc is not None:
                    print("Preparing test case data set")
                    d_tc = dict()
                    d_tc["name"] = tc
                    d_tc["id"] = data["tc_count"] + 1
                    d_tc["dir"] = os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite), tc)
                    d_tc["current_status"] = {}
                    d_tc["history_status"] = []
                    print("Inserting test case data set")
                    self.insert_data_set(data, feature, suite, TC=d_tc)
                    print("Insertion completed")

    def insert_data_set(self, data, feature, suite, FEATURE=None, SUITE=None, TC=None):
        if FEATURE is not None:
            data["features"].append(FEATURE)
            data["feature_count"] = data["feature_count"] + 1
        elif SUITE is not None:
            for data_feature in data["features"]:
                if data_feature["name"] == feature:
                    data_feature["suites"].append(SUITE)
                    data["suite_count"] = data["suite_count"] + 1
        elif TC is not None:
            for data_feature in data["features"]:
                if data_feature["name"] == feature:
                    for data_suite in data_feature["suites"]:
                        if data_suite["name"] == suite:
                            data_suite["tcs"].append(TC)
                            data["tc_count"] = data["tc_count"] + 1

    def script_log(self, script_file):
        with open(script_file, "r") as file:
            log = file.read()
            if "end of script output" in log:
                return log.replace("start of script output", "").replace("end of script output", "") + "<br>Completed."
            elif "Script aborted!" in log or "signal will force exit" in log:
                return log.replace("start of script output", "") + "<br>Aborted!!!"
            else:
                return log.replace("start of script output", "") + "<br>Still Running..."


if __name__ == "__main__":
    p_feature = "project2"
    # p_suite = "mtu.robot"
    p_suite = "span.robot"

    # p_tc = "TC_101"
    # trigger(feature=p_feature, suite=p_suite, tc=p_tc)
    import App1.settings as meta

    runner = invoke(track='App1/robot_runner/track.json',
                    result_dir=os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT"))
    runner.trigger(feature=p_feature, suite=p_suite)
