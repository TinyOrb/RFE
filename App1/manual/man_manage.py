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
        thread_id = self.pool.action("read")
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]["suites"][suite]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def update_suite_ops(self, suite, name, creator, suite_list, project):

        def update_suite(data):
            data["suites"][suite]["name"] = name
            data["suites"][suite]["modifier"] = creator
            if suite_list is not None:
                data["suites"][suite]["script_project"] = project
                data["suites"][suite]["script_suite"] = suite_list
            data["suites"][suite]["modified_date"] = time.asctime(time.localtime(time.time()))
            return data

        return update_suite

    def update_suite(self, suite, name, creator, suite_list, project):
        ops = self.update_suite_ops(suite, name, creator, suite_list, project)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

    def del_suite_ops(self, suite):

        def del_suite(data):
            del data["suites"][suite]
            return data

        return del_suite

    def del_suite(self, suite):
        ops = self.del_suite_ops(suite)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

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

    def add_case_ops(self, name, suite, creator, desc, step):

        def add_case(data):
            case_id = "C{}".format(data["next_case_id"])
            if data["suites"][suite].get("cases") is None:
                data["suites"][suite]["cases"] = {}
            data["suites"][suite]["cases"][case_id] ={}
            data["suites"][suite]["cases"][case_id]["name"] = name
            data["suites"][suite]["cases"][case_id]["scenario"] = step
            data["suites"][suite]["cases"][case_id]["description"] = desc
            data["suites"][suite]["cases"][case_id]["creator"] = creator
            data["suites"][suite]["cases"][case_id]["created_date"] = time.asctime(time.localtime(time.time()))
            data["next_case_id"] += 1
            return data
        return add_case

    def add_case(self, name, suite, creator, desc, step):
        ops = self.add_case_ops(name, suite, creator, desc, step)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

    def update_case_ops(self, name, suite, case, creator, desc, steps):

        def update_case(data):
            data["suites"][suite]["cases"][case]["name"] = name
            data["suites"][suite]["cases"][case]["scenario"] = steps
            data["suites"][suite]["cases"][case]["description"] = desc
            data["suites"][suite]["cases"][case]["modifier"] = creator
            data["suites"][suite]["cases"][case]["modified_date"] = time.asctime(time.localtime(time.time()))
            return data

        return update_case

    def update_case(self, name, suite, case, creator, desc, steps):
        ops = self.update_case_ops(name, suite, case, creator, desc, steps)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

    def del_case_ops(self, suite, case):

        def del_case(data):
            del data["suites"][suite]["cases"][case]
            return data

        return del_case

    def del_case(self, suite, case):
        ops = self.del_case_ops(suite, case)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

