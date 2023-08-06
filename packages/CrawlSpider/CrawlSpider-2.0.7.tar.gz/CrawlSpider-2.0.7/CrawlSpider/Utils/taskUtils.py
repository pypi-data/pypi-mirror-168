# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/8 9:42
# __fileName__ : CrawlSpider taskUtils.py
# __devIDE__ : PyCharm
import platform
import asyncio


def initEventLoop():
    sysType = platform.system()
    if sysType == 'Linux':
        try:
            import uvloop
            asyncio.set_event_loop(uvloop)
        except:
            pass
    return asyncio.get_event_loop()


def executeTask(ft: asyncio.Future):
    loop = initEventLoop()
    loop.run_until_complete(ft)

async def launchTasks(taskItems):
    tasks = [
        asyncio.create_task(item['fn'](**item['params']))
        for item in taskItems
    ]
    await asyncio.gather(*tasks)
    return tasks





