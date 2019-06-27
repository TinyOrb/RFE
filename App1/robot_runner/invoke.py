import subprocess
import json
import datetime
import time
import os
import threading
import RFE.App1.Robot_loader.Al_robot as Al_robot
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

        update_current(current_state, feature, suite, tc)

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
        update_current(current_state, feature, suite, tc)

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
        update_current(current_state, feature, suite, tc)

    else:
        print("No input provided")
        return

    print("Main    : before creating thread")
    x = threading.Thread(target=run, args=(current_state, feature, suite, tc,))
    print("Main    : before running thread")
    x.start()


def get_run_state(feature, suite=None, tc=None):
    pass


def fetch_history(feature, suite=None, tc=None):
    print("Fetching query")
    with open('track.json') as json_file:
        data = json.load(json_file)
    flag = 0
    status = None
    for data_feature in data["features"]:
        if data_feature["name"] == feature:
            if suite is not None:
                for data_suite in data_feature["suites"]:
                    if data_suite["name"] == suite:
                        if tc != None:
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


def fetch_current(feature, suite=None, tc=None):
    print("Fetching query")
    with open('track.json') as json_file:
        data = json.load(json_file)
    flag = 0
    status = None
    for data_feature in data["features"]:
        if data_feature["name"] == feature:
            if suite is not None:
                for data_suite in data_feature["suites"]:
                    if data_suite["name"] == suite:
                        if tc != None:
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


def update_history(current_status, feature, suite=None, tc=None):
    print("Updating status")
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
        print("Insertion failed")
        return False
    elif flag == 1 or flag == 2 or flag == 3:
        try:
            with open('track.json', 'w') as outfile:
                json.dump(data, outfile)
            print("Insertion success")
            return True
        except:
            print("Unknown exception")
    else:
        print("Unknown state")
        return False


def update_current(current_status, feature, suite=None, tc=None):
    print("Updating status")
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
        print("Insertion failed")
        return False
    elif flag == 1 or flag == 2 or flag == 3:
        try:
            with open('track.json', 'w') as outfile:
                json.dump(data, outfile)
            print("Insertion success")
            return True
        except:
            print("Unknown exception")
    else:
        print("Unknown state")
        return False


def get_tc():
    pass


def get_suite():
    pass


def get_feature():
    pass


def run(current_state, feature, suite, tc):
    if not ensure_path(current_state["script_output"], type="file"):
        print("Failed to create script output file")
        return False
    subprocess.Popen(["echo ******start of script output****** > %s ; %s >> %s ; "
                      "echo ******end of script output****** >> %s " %
                      (current_state["script_output"], current_state["cmd"], current_state["script_output"], current_state["script_output"])], shell=True)

    current_state["status"] = "running"
    update_current(current_state, feature, suite, tc)

    line = subprocess.check_output(['tail', '-1', current_state["script_output"]])

    while "******end of script output******" not in str(line):
        time.sleep(5)
        line = subprocess.check_output(['tail', '-1', current_state["script_output"]])

    current_state["status"] = "done"
    cur_time = str(datetime.datetime.now())
    cur_time1 = cur_time.split(" ")[0] + "_" + cur_time.split(" ")[1]
    current_state["end_time"] = cur_time1
    update_current(current_state, feature, suite, tc)

    print("Thread ended")
    return True


def ensure_path(path, type="dir"):
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


def fetch_detail_traverse_data(data, feature, suite, tc):
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


def ensure_data_set(data, feature, suite, tc):
    global result_dir
    current_data_set = fetch_detail_traverse_data(data, feature, suite, tc)

    if current_data_set["feature"] is not None and suite is None:
        if current_data_set["suite"] is not None and tc is None:
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
    p_feature = "project2"
    p_suite = "mtu.robot"

    #p_tc = "TC_101"
    #trigger(feature=p_feature, suite=p_suite, tc=p_tc)

    trigger(feature=p_feature, suite=p_suite)