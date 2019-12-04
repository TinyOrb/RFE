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

import time


class exec_manager:

    def __init__(self, pool):
        self.pool = pool

    def instantiate_ops(self, username, manual, automation):

        def instantiate(data):
            suite_id = "ES{}".format(data["next_exec_suite_id"])
            data["execution_suites"][suite_id] = {}
            data["execution_suites"][suite_id]["name"] = manual["name"]
            data["execution_suites"][suite_id]["creator"] = username
            data["execution_suites"][suite_id]["script_suite"] = manual.get("script_suite")
            data["execution_suites"][suite_id]["creation_date"] = time.asctime(time.localtime(time.time()))
            data["execution_suites"][suite_id]["script_project"] = manual.get("script_project")
            data["execution_suites"][suite_id]["m_cases"] = {}
            data["execution_suites"][suite_id]["a_cases"] = {}
            case_id = data["next_exec_case_id"]
            if manual.get("cases") is not None and len(manual) > 0:
                for case in manual["cases"].keys():
                    data["execution_suites"][suite_id]["m_cases"]["EC{}".format(case_id)] = {}
                    data["execution_suites"][suite_id]["m_cases"]["EC{}".format(case_id)]["name"] = manual["cases"][case]["name"]
                    data["execution_suites"][suite_id]["m_cases"]["EC{}".format(case_id)]["description"] = manual["cases"][case]["description"]
                    data["execution_suites"][suite_id]["m_cases"]["EC{}".format(case_id)]["scenario"] = manual["cases"][case]["scenario"]
                    data["execution_suites"][suite_id]["m_cases"]["EC{}".format(case_id)]["result"] = "not tested"
                    case_id += 1
            if automation is not None and len(automation) > 0:
                for script in automation.keys():
                    data["execution_suites"][suite_id]["a_cases"][script] = {}
                    for case in automation[script]:
                        data["execution_suites"][suite_id]["a_cases"][script]["EC{}".format(case_id)] = {}
                        data["execution_suites"][suite_id]["a_cases"][script]["EC{}".format(case_id)]["name"] = case.get("name")
                        data["execution_suites"][suite_id]["a_cases"][script]["EC{}".format(case_id)]["result"] = "not tested"
                        #future bring automation case name with keyword step
                        case_id += 1
            data["next_exec_case_id"] = case_id
            data["next_exec_suite_id"] += 1
            return data

        return instantiate

    def instantiate(self, username, manual, automation):
        ops = self.instantiate_ops(username, manual, automation)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            print(result)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Multi operation: failure": "timeout"}

    def update_case_ops(self, username, suite, case, status, _type, script):

        def update_case(data):
            if _type == "a":
                data["execution_suites"][suite]["a_cases"][script][case]["result"] = status
                data["execution_suites"][suite]["a_cases"][script][case]["modified_on"] = time.asctime(time.localtime(time.time()))
                data["execution_suites"][suite]["a_cases"][script][case]["tested_by"] = username
            elif _type == "m":
                data["execution_suites"][suite]["m_cases"][case]["result"] = status
                data["execution_suites"][suite]["m_cases"][case]["modified_on"] = time.asctime(
                    time.localtime(time.time()))
                data["execution_suites"][suite]["m_cases"][case]["tested_by"] = username
            return data

        return update_case

    def update_case(self, username, suite, case, status, _type, script):
        ops = self.update_case_ops(username, suite, case, status, _type, script)
        thread_id = self.pool.action("multi", operation=ops)
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            print(result)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[
                0].lower():
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
                data = result.values()[0]["execution_suites"]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

    def get_suite(self, suite):
        thread_id = self.pool.action("read")
        for iter in range(10):
            result = self.pool.get_thread_buffer(thread_id)
            if result is not str and result != "No thread" and result is not None and "success" in result.keys()[0].lower():
                data = result.values()[0]["execution_suites"][suite]
                self.pool.remove_thread_buffer(thread_id)
                return data
            time.sleep(1)
        return {"Read: failure": "timeout"}

