import json
import time

class suite_manager:

    def __init__(self, pool):
        self.pool = pool

    def get_suites(self):
        thread_id = self.pool.action("read")
        for iter in range(10):
            if self.pool.get_thread_buffer(thread_id) is not str and self.pool.get_thread_buffer(thread_id) != "No thread":
                data = self.pool.get_thread_buffer(thread_id)
                data = json.loads(data)
                self.pool.remove_thread_buffer(thread_id)
                return data["suites"]
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def get_suite(self, suite):
        pass

    def update_suite(self, suite_id, data):
        pass

    def update_test_execution(self, test_execution_id):
        pass

    def add_test_ops(self, data):
        data = json.loads(data)
        return data

    def add_test(self, suite_id, data):
        test_name = data["name"]
        test_desc = data["desc"]
        links = data["links"]
        self.pool.action("write", data="", operation=self.add_ops)
