# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/9/22 1:09
# __fileName__ : CrawlSpider ThreadClosable.py
# __devIDE__ : PyCharm


import threading
import ctypes

class ClosableThread(threading.Thread):


    def run(self):
        raise NotImplementedError()

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for tid, thread in threading._active.items():
            if thread is self:
                return tid

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
            ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def stop(self):
        self.raise_exception()
        self.join()



