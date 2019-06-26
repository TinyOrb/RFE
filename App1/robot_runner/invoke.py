import subprocess
import os
import sys
import json
import datetime

from RFE.App1.Robot_loader import Al_robot
from RFE.App1.Robot_loader import Al_robot_parser

import RFE.App1.settings as meta

result_dir = None


def trigger(feature, suite=None, tc=None, variable=None, variablefile=None, include_tags=None, exclude_tags=None):
    global result_dir
    with open('track.json') as json_file:
        data = json.load(json_file)

    result_dir = os.path.join(meta.STATICFILES_DIRS[0], "RFE_RESULT")
    if not ensure_path(result_dir):
        return False
    else:
        ensure_data_set(data, feature, suite, tc)

        with open('track.json', 'w') as outfile:
            json.dump(data, outfile)

    if tc is not None:
        current_state = fetch_current(feature, suite, tc)
        if len(current_state) != 0:
            update_history(current_state, feature, suite, tc)

        current_state["status"] = "not started"
        cur_time = str(datetime.datetime.now())
        cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
        current_state["time"] = cur_time1
        current_state["dir"] = os.path.join(os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc), cur_time1)
        current_state["script_output"] = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc), cur_time1), "script.txt")
        current_state["log"] = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc), cur_time1), "log.html")
        current_state["output"] = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc), cur_time1), "report.html")
        current_state["xml"] = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc), cur_time1), "output.html")
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

    elif suite is not None:
        current_state = fetch_current(feature, suite, tc)
        if len(current_state) != 0:
            update_history(current_state, feature, suite, tc)

        current_state["status"] = "not started"
        cur_time = str(datetime.datetime.now())
        cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
        current_state["time"] = cur_time1
        current_state["dir"] = os.path.join(os.path.join(os.path.join(result_dir, feature), suite), cur_time1)
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

    elif suite is not None:
        current_state = fetch_current(feature, suite, tc)
        if len(current_state) != 0:
            update_history(current_state, feature, suite, tc)

        current_state["status"] = "not started"
        cur_time = str(datetime.datetime.now())
        cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
        current_state["time"] = cur_time1
        current_state["dir"] = os.path.join(os.path.join(result_dir, feature), cur_time1)
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

    else:
        print("No input provided")

def create_track(feature, suite=None, tc=None):
    pass


def create_output_path(feature, suite=None, tc=None):
    pass


def get_run_state(feature, suite=None, tc=None):
    pass


def fetch_history(feature, suite=None, tc=None):
    pass


def fetch_current(feature, suite=None, tc=None):
    with open('track.json') as json_file:
        data = json.load(json_file)
    flag = 0
    for data_feature in data["features"]:
        if data_feature["name"] == feature:
            if suite is not None:
                for data_suite in data_feature["suites"]:
                    if data_suite["name"] == suite:
                        if tc != None:
                            for data_tc in data_suite["tcs"]:
                                if data_tc["name"] == tc:
                                    flag = 1
                                    return data_tc["current_status"]
                        else:
                            flag = 2
                            return data_suite["current_status"]
            else:
                flag = 3
                return data_feature["current_status"]
    if flag == 0:
        print("query failed")


def update_history(current_status, feature, suite=None, tc=None):
    with open('track.json') as json_file:
        data = json.load(json_file)

    flag = 0

    for data_feature in data["features"]:
        if data_feature["name"] == feature:
            if suite is not None:
                for data_suite in data_feature["suites"]:
                    if data_suite["name"] == suite:
                        if tc != None:
                            for data_tc in data_suite["tcs"]:
                                if data_tc["name"] == tc:
                                    data_tc["history_status"].append(current_status)
                                    flag = 1
                        else:
                            data_suite["current_status"].append(current_status)
                            flag = 2
            else:
                data_feature["current_status"].append(current_status)
                flag = 3

    if flag == 0:
        print("Insertion success")

    with open('track.json', 'w') as outfile:
        json.dump(data, outfile)


def update_current(current_status, feature, suite=None, tc=None):

    with open('track.json') as json_file:
        data = json.load(json_file)
    flag = 0
    for data_feature in data["features"]:
        if data_feature["name"] == feature:
            if suite is not None:
                for data_suite in data_feature["suites"]:
                    if data_suite["name"] == suite:
                        if tc != None:
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
        print("Insertion success")

    with open('track.json', 'w') as outfile:
        json.dump(data, outfile)


def get_tc():
    pass


def get_suite():
    pass


def get_feature():
    pass


def run(cmd):
    k = os.system(cmd)


def ensure_path(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print("Directory all ready exist")
        return True
    except Exception as e:
        print("Some unknown error", str(e))
        return False


def fetch_detail_traverse_data(data, feature, suite, tc):
    detail = {"feature":None, "suite":None, "tc":None}

    try:
        for data_feature in data["features"]:
            if feature == data_feature["name"]:
                detail["feature"] = feature

                if suite is None:
                    return data_feature
                else:
                    for data_suite in data_feature["suites"]:
                        if suite == data_suite["name"]:
                            detail["suite"] = suite

                            if tc is None:
                                return data_suite
                            else:
                                for data_tc in data_suite["tcs"]:
                                    if tc == data_tc["name"]:
                                        detail["tc"] = tc
    except Exception as e:
        print("Exception occurs %s" % str(e))

    return detail


def ensure_data_set(data, feature, suite, tc):

    current_data_set = fetch_detail_traverse_data(data, feature, suite, tc)

    if current_data_set["feature"] is not None:
        if current_data_set["suite"] is not None:
            if current_data_set["tc"] is not None:
                print("Data set already exist")
            else:
                print("Preparing test case data set")
                d_tc = dict()
                d_tc["name"] = tc
                d_tc["id"] = data["tc_count"] + 1
                d_tc["dir"] = os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc)
                d_tc["current_status"] = {}
                d_tc["history_status"] = []
                print("Inserting test case data set")
                insert_data_set(data, feature, suite, TC=d_tc)
                print("Insertion completed")
        else:
            print("Preparing suite data set")
            d_suite = dict()
            d_suite["name"] = suite
            d_suite["id"] = data["suite_count"] + 1
            d_suite["dir"] = os.path.join(os.path.join(result_dir, feature), suite)
            d_suite["current_status"] = {}
            d_suite["history_status"] = []
            d_suite["tcs"] = []
            print("Inserting suite data set")
            insert_data_set(data, feature, suite, SUITE=d_suite)
            print("Insertion completed")
            if tc is not None:
                print("Preparing test case data set")
                d_tc = dict()
                d_tc["name"] = tc
                d_tc["id"] = data["tc_count"] + 1
                d_tc["dir"] = os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc)
                d_tc["current_status"] = {}
                d_tc["history_status"] = []
                print("Inserting test case data set")
                insert_data_set(data, feature, suite, TC=d_tc)
                print("Insertion completed")
    else:
        print("Preparing feature data set")
        d_feature = dict()
        d_feature["name"] = feature
        d_feature["id"] = data["feature_count"] + 1
        d_feature["dir"] = os.path.join(result_dir, feature)
        d_feature["current_status"] = {}
        d_feature["history_status"] = []
        d_feature["suites"] = []
        print("Inserting feature data set")
        insert_data_set(data, feature, suite, FEATURE=d_feature)
        print("Insertion completed")
        if suite is not None:
            print("Preparing suite data set")
            d_suite = dict()
            d_suite["name"] = suite
            d_suite["id"] = data["suite_count"] + 1
            d_suite["dir"] = os.path.join(os.path.join(result_dir, feature), suite)
            d_suite["current_status"] = {}
            d_suite["history_status"] = []
            d_suite["tcs"] = []
            print("Inserting suite data set")
            insert_data_set(data, feature, suite, SUITE=d_suite)
            print("Insertion completed")
            if tc is not None:
                print("Preparing test case data set")
                d_tc = dict()
                d_tc["name"] = tc
                d_tc["id"] = data["tc_count"] + 1
                d_tc["dir"] = os.path.join(os.path.join(os.path.join(result_dir, feature), suite), tc)
                d_tc["current_status"] = {}
                d_tc["history_status"] = []
                print("Inserting test case data set")
                insert_data_set(data, feature, suite, TC=d_tc)
                print("Insertion completed")


def insert_data_set(data, feature, suite, FEATURE=None, SUITE=None, TC=None):
    if FEATURE is not None:
        data["features"].append(FEATURE)
    elif SUITE is not None:
        for data_feature in data["features"]:
            if data_feature["name"] == feature:
                data_feature["suites"].append(SUITE)
    elif TC is not None:
        for data_feature in data["features"]:
            if data_feature["name"] == feature:
                for data_suite in data_feature["suites"]:
                    if data_suite["name"] == suite:
                        data_suite["tcs"].append(TC)


if __name__ == "__main__":
    p_feature = "project1"
    p_suite = "mtu.robot"
    trigger(feature=p_feature, suite=p_suite)
