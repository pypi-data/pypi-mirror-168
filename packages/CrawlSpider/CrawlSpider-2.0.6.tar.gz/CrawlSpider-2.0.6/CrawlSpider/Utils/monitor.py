# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/5/21 23:49
# __fileName__ : XueshuSpider process_monitor.py
# __devIDE__ : PyCharm

import time
import psutil
import fire
import asyncio

class Monitor:
    interval = 60  # 获取CPU，内存使用情况轮询时间间隔
    num = 100
    processMetrics = [None]*num

    @staticmethod
    async def process_monitor(pid=0, pName=None, **kwargs):

        interval = kwargs.get('interval') or Monitor.interval

        pidList = []
        if pid:
            pidList = [pid]
        elif pName is not None:
            pidList = [p.pid for p in psutil.process_iter() if pName in p.name()]

        while 1:
            memTotal = 0.0
            cpuPercent = 0.0
            memPercent = 0.0
            current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
            for pId in pidList:
                p = psutil.Process(pId)
                cpu_percent = p.cpu_percent()  # better set interval second to calculate like:  p.cpu_percent(interval=0.5)
                cpuPercent += cpu_percent
                mem_percent = p.memory_percent()
                memPercent += mem_percent
                mem_MB = round(p.memory_info().rss / 1024 / 1024, 4)
                memTotal += mem_MB
            line = f"current_time:{current_time}--cpu_percent:{cpuPercent}--mem_percent:{memPercent}--memTotal:{memTotal}"
            print(line)
            await asyncio.sleep(interval)




def run(pid=0, pName=None, method='process_monitor',  **kwargs):

    loop = asyncio.get_event_loop()
    loop.run_until_complete(getattr(Monitor, method)(pid=pid, pName=pName, **kwargs))


if __name__ == '__main__':
    fire.Fire(run)