import time


class exec_manager:

    def __init__(self, pool):
        self.pool = pool

    def instantiate_ops(self, username, manual, automation):

        def instantiate(data):
            suite_id = "ES{}".format(data["next_exec_suite_id"])
            data["execution_suite"][suite_id] = {}
            data["execution_suite"][suite_id]["name"] = manual["name"]
            data["execution_suite"][suite_id]["creator"] = username
            data["execution_suite"][suite_id]["script_suite"] = manual.get("script_suite")
            data["execution_suite"][suite_id]["creation_date"] = time.asctime(time.localtime(time.time()))
            data["execution_suite"][suite_id]["script_project"] = manual.get("script_project")
            data["execution_suite"][suite_id]["m_cases"] = {}
            data["execution_suite"][suite_id]["a_cases"] = {}
            case_id = "EC{}".format(data["next_exec_case_id"])
            if manual.get("cases") is None:
                data["execution_suite"][suite_id]["m_cases"][case_id] = {}
                manual["cases"]
                case_id += 1

            data["execution_suite"][suite_id]["a_cases"] = {}
            data["next_exec_case_id"] = case_id
            data["next_exec_suite_id"] += 1
            return data

        return instantiate

    def instantiate(self, username, manual, automation):
        ops = self.instantiate_ops(username, manual, automation)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

    def get_suites(self):
        thread_id = self.pool.action("read")
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]["execution_suite"]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def get_suite(self, suite):
        thread_id = self.pool.action("read")
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]["execution_suite"][suite]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

