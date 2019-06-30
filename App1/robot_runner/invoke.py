import subprocess
import json
import datetime
import time
import os
import signal
import threading

import App1.Robot_loader.Al_robot as Al_robot


class invoke:

    thread_list = {}

    def __init__(self, track, result_dir):
        self.track = track
        self.result_dir = result_dir

    def trigger(self, feature, suite=None, tc=None, variable=None, variablefile=None, include_tags=None, exclude_tags=None):
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
                current_state["dir"] = os.path.join(os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite), tc), cur_time1)
                current_state["script_output"] = os.path.join(current_state["dir"], "script.txt")
                current_state["log"] = os.path.join(current_state["dir"], "log.html")
                current_state["output"] = os.path.join(current_state["dir"], "report.html")
                current_state["xml"] = os.path.join(current_state["dir"], "output.html")
                current_state["cmd"] = "python -m robot "
                if include_tags is not None:
                    current_state["cmd"] += "--include \"%s\" " % include_tags
                if exclude_tags is not None:
                    current_state["cmd"] += "--exclude \"%s\" " % exclude_tags
                if variable is not None:
                    current_state["cmd"] += "--variable==\"%s\" " % variable
                if variablefile is not None:
                    current_state["cmd"] += "--variablefile==\"%s\" " % variablefile
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
                current_state["dir"] = os.path.join(os.path.join(os.path.join(self.result_dir, feature), suite), cur_time1)
                current_state["script_output"] = os.path.join(current_state["dir"], "script.txt")
                current_state["log"] = os.path.join(current_state["dir"], "log.html")
                current_state["output"] = os.path.join(current_state["dir"], "report.html")
                current_state["xml"] = os.path.join(current_state["dir"], "output.html")
                current_state["cmd"] = "python -m robot "
                if include_tags is not None:
                    current_state["cmd"] += "--include \"%s\" " % include_tags
                if exclude_tags is not None:
                    current_state["cmd"] += "--exclude \"%s\" " % exclude_tags
                if variable is not None:
                    current_state["cmd"] += "--variable==\"%s\" " % variable
                if variablefile is not None:
                    current_state["cmd"] += "--variablefile==\"%s\" " % variablefile
                current_state["cmd"] += "--outputdir \"%s\" " % current_state["dir"]
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
                current_state["dir"] = os.path.join(os.path.join(self.result_dir, feature), cur_time1)
                current_state["script_output"] = os.path.join(current_state["dir"], "script.txt")
                current_state["log"] = os.path.join(current_state["dir"], "log.html")
                current_state["output"] = os.path.join(current_state["dir"], "report.html")
                current_state["xml"] = os.path.join(current_state["dir"], "output.html")
                current_state["cmd"] = "python -m robot "
                if include_tags is not None:
                    current_state["cmd"] += "--include \"%s\" " % include_tags
                if exclude_tags is not None:
                    current_state["cmd"] += "--exclude \"%s\" " % exclude_tags
                if variable is not None:
                    current_state["cmd"] += "--variable==\"%s\" " % variable
                if variablefile is not None:
                    current_state["cmd"] += "--variablefile==\"%s\" " % variablefile
                current_state["cmd"] += "--outputdir \"%s\" " % current_state["dir"]
                current_state["cmd"] += Al_robot.fetch_All_suite()[feature]
                self.update_current(current_state, feature, suite, tc)

            else:
                print("No enough input provided")
                return "Fail"

            print("Main    : before creating thread")
            self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] = "continue"
            x = threading.Thread(target=self.run, args=(current_state, feature, suite, tc,))
            print("Main    : before running thread")
            x.start()

            return "Success"
        except Exception as e:
            print("Exception occur %s" % str(e))
            return "Fail"

    def abort_run(self, feature, suite=None, tc=None):
        try:
            self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] = "abort"
            time.sleep(5)
            if self.fetch_current(feature, suite, tc)["status"].lower() != "running":
                return "success"
            else:
                return "fail"
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
                            if d_suite["current_status"]["status"].lower() == "running":
                                suite["status"] = "Running"
                            else:
                                suite["status"] = "Run"
                            for tc in suite["tcs"]:
                                t_flag = 0
                                for d_tc in d_suite["tcs"]:
                                    if tc["name"] == d_tc["name"]:
                                        t_flag = 1
                                        if d_tc["current_status"]["status"].lower() == "running":
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
                                    if data_tc["name"] == tc:
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
                                    if data_tc["name"] == tc:
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
        if not self.ensure_path(current_state["script_output"], type="file"):
            print("Failed to create script output file")
            return False
        with open(current_state["script_output"], "wb") as out:
            process = subprocess.Popen(["echo ******start of script output******; %s ; "
                                        "echo ******end of script output****** " %
                                        current_state["cmd"]], stdout=out, stderr=out, shell=True, preexec_fn=os.setsid)

        current_state["status"] = "running"
        self.update_current(current_state, feature, suite, tc)

        line = subprocess.check_output(['tail', '-1', current_state["script_output"]])

        while "******end of script output******" not in str(line):
            if self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] == "abort":
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.kill()
                current_state["status"] = "aborted"
                self.update_current(current_state, feature, suite, tc)
                self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] = "Run"
                print("Thread ended: %s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc))
                return True
            time.sleep(5)
            line = subprocess.check_output(['tail', '-1', current_state["script_output"]])

        current_state["status"] = "done"
        cur_time = str(datetime.datetime.now())
        cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
        current_state["end_time"] = cur_time1
        self.update_current(current_state, feature, suite, tc)
        self.thread_list["%s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc)] = "Run"
        print("Thread ended: %s_%s_%s" % (feature, "" if suite is None else suite, "" if tc is None else tc))
        return True

    def ensure_path(self, path, type="dir"):
        try:
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
            print("Some unknown error", str(e))
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


if __name__ == "__main__":
    p_feature = "project2"
    #p_suite = "mtu.robot"
    p_suite = "span.robot"

    #p_tc = "TC_101"
    #trigger(feature=p_feature, suite=p_suite, tc=p_tc)
    import App1.settings as meta
    runner = invoke(track='App1/robot_runner/track.json', result_dir=os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT"))
    runner.trigger(feature=p_feature, suite=p_suite)