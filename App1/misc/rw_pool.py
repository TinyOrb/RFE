import threading
import time
import logging
import json

class rw_pool(threading.Thread):

    rw_threads = {}
    evt = threading.Event()
    gen_thread_id = 0
    thread_buffer = {}

    class meta_buffer:

        buff = None

        def __init__(self, _id):
            self.id = _id

        def get(self):
            return self.buff

        def set(self, buff):
            self.buff = buff

        def get_id(self):
            return self.id

    # pool with synchronized method
    def __init__(self, max_thread, _file):
        self.max_thread = max_thread
        self.end_flag = True
        self._file = _file
        self.evt.set()
        for i in range(max_thread):
            self.rw_threads[i] = None
        super(rw_pool, self).__init__()

    def action(self, do, data=None, operation=None):
        # Thread limit can sorted by initializing gen_thread_id by zero and reallocation by incremental iteration if it is not exist in thread_buff
        self.gen_thread_id = self.gen_thread_id + 1

        allocated = 0
        while allocated == 0:
            for pool_num in self.rw_threads.keys():
                if self.rw_threads[pool_num] is None or not self.rw_threads[pool_num].mutex:
                    alloc_pool = pool_num
                    allocated = 1
                    break
        self.thread_buffer[self.gen_thread_id] = self.meta_buffer(self.gen_thread_id)
        self.rw_threads[alloc_pool] = rw_thread(self.gen_thread_id, self.evt, self._file, self.thread_buffer[self.gen_thread_id], mutex=True,)
        self.rw_threads[alloc_pool].mode = do
        self.rw_threads[alloc_pool].data = data
        self.rw_threads[alloc_pool].operation = operation
        self.rw_threads[alloc_pool].start()
        return self.gen_thread_id

    def get_thread_buffer(self, thread_id):
        try:
            return self.thread_buffer[thread_id].get()
        except Exception as e:
            return "No thread"

    def remove_thread_buffer(self, thread_id):
        del self.thread_buffer[thread_id]

    def end_pool(self):
        self.end_flag = False

    def run(self):
        while self.end_flag:
            pass



class rw_thread(threading.Thread):

    def __init__(self, thread_number, evt, filename, buff, mutex=False):
        self.thread_number = thread_number
        self.mutex = mutex
        self.evt = evt
        self.buffer = buff
        self.filename = filename
        super(rw_thread, self).__init__()

    def multi_ops(self, operation):
        if not self.evt.is_set():
            self.evt.wait()
        self.evt.clear()
        with open(self.filename, 'r') as f:
            data = json.load(f)
        if "function" in str(type(operation)):
            x = operation(data)
            if x is not None:
                with open(self.filename, 'w') as f:
                    json.dump(x, f, indent=4)
            else:
                raise RuntimeError("Mode: multi takes function of a argument and return string as argument")
        else:
            raise RuntimeError("Mode: multi takes function of a argument as argument")


    def read(self):
        if not self.evt.is_set():
            self.evt.wait()
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data

    def write(self, data):
        if not self.evt.is_set():
            self.evt.wait()
        self.evt.clear()
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def run(self):
        self.mutex = True
        logging.info("Thread id: {}, data: {}, operation: {}".format(self.thread_number, self.data, self.mode))
        if self.mode == "read":
            try:
                self.buffer.set({"Read: success": self.read()})
            except Exception as e:
                self.buffer.set({"Read: failure": e})
        elif self.mode == "write":
            try:
                self.write(self.data)
                self.buffer.set({"Write: success": 0})
            except Exception as e:
                self.buffer.set({"Write: failure": e})
            finally:
                self.evt.set()
        elif self.mode == "multi":
            try:
                self.multi_ops(self.operation)
                self.buffer.set({"Operation: success": 0})
            except Exception as e:
                self.buffer.set({"Operation: failure": e})
            finally:
                self.evt.set()
        else:
            self.buffer.set({"No operation": -1})
        logging.info("Ending thread number: {}, iter: {}, buffer {}".format(self.thread_number, self.data, self.buffer))
        self.mutex = False
