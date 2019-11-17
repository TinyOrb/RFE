import json
import time

class suite_manager:

    def __init__(self, pool):
        self.pool = pool

    def get_suites(self):
        thread_id = self.pool.action("read")
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]["suites"]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def get_suite(self, suite):
        pass

    def update_suite(self, suite_id, data):
        pass

    def update_test_execution(self, test_execution_id):
        pass

    def add_suite_ops(self, name, creator, suite_list, project):

        def add_suite(data):
            suite_id = "S{}".format(data["next_suite_id"])
            data["suites"][suite_id] = {}
            data["suites"][suite_id]["name"] = name
            data["suites"][suite_id]["creator"] = creator
            data["suites"][suite_id]["script_suite"] = suite_list
            data["suites"][suite_id]["created_date"] = time.asctime(time.localtime(time.time()))
            data["suites"][suite_id]["script_project"] = project
            data["next_suite_id"] += 1
            return data

        return add_suite

    def add_suite(self, name, creator, suite_list, project):
        ops = self.add_suite_ops(name, creator, suite_list, project)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

    def add_test(self, suite_id, data):
        test_name = data["name"]
        test_desc = data["desc"]
        links = data["links"]
        self.pool.action("write", data="", operation=self.add_ops)
