# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/9/21 14:08
# __fileName__ : CrawlSpider OfficeUtils.py
# __devIDE__ : PyCharm

from collections import OrderedDict
import datetime
from pyexcel_xlsx import save_data, get_data


def parseExcel(excelPath):
    excelData = get_data(excelPath)
    return excelData


def saveToExcel(itemDic, outputFile=None):
    if not outputFile:
        outputFile = f"{datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')}_example.xlsx"
    data = OrderedDict()
    for k in itemDic:
        dataList = itemDic[k]
        rows = []
        ks = tuple(dataList[0].keys())
        rows.append(ks)
        rows.extend([tuple(data.values()) for data in dataList])
        data.setdefault(k, rows)
    save_data(outputFile, data)


if __name__ == '__main__':
    dispatch_pkg()





























